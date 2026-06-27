from typing import Any, Optional
from playwright.async_api import BrowserContext

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.browser_manager import BrowserManager
from crawl4ai.async_crawler_strategy import AsyncPlaywrightCrawlerStrategy

from koda.modules.browser.service import BrowserTool

class KodaBrowserManager(BrowserManager):
    """
    A custom BrowserManager for crawl4ai that bypasses its internal lifecycle management.
    It creates new pages from the Playwright BrowserContext provided by Koda.
    """
    def __init__(self, context: BrowserContext, *args, **kwargs):
        # We don't need to initialize the real BrowserManager stuff
        self.koda_context = context
        self.browser = context.browser
        self.default_context = context
        self.sessions = {}
        self.config = kwargs.get("browser_config") or BrowserConfig()
        self.logger = kwargs.get("logger")
        self._using_cached_cdp = False

    async def start(self):
        pass # No-op, Koda manages the browser

    async def close(self):
        pass # No-op, Koda manages the browser

    async def get_page(self, crawlerRunConfig: CrawlerRunConfig):
        # Create a new page from the Koda context
        page = await self.koda_context.new_page()
        
        # Enforce consistent viewport for screenshots if configured
        width = self.config.viewport_width or 1366
        height = self.config.viewport_height or 768
        await page.set_viewport_size({"width": width, "height": height})
        
        # Patch evaluate to prevent Crawl4AI from deadlocking the JS engine
        # on heavily obfuscated DOMs (like google.com) when combined with invisible_playwright
        import asyncio
        original_evaluate = page.evaluate
        async def safe_evaluate(expression, *args, **kwargs):
            try:
                # 5 second timeout for JS evaluations to prevent infinite hangs
                return await asyncio.wait_for(
                    original_evaluate(expression, *args, **kwargs),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                if self.logger:
                    self.logger.warning("page.evaluate timed out after 5s. Bypassing deadlock.")
                return True
                
        page.evaluate = safe_evaluate
        
        return page, self.koda_context
        
    async def release_page_with_context(self, page):
        # We can close the page here since Koda manages the context
        try:
            await page.close()
        except Exception:
            pass

class KodaAsyncWebCrawler(AsyncWebCrawler):
    """
    A custom AsyncWebCrawler that intercepts initialization to route browser
    management through Koda's infrastructure if a `client` is provided.
    """
    def __init__(self, **kwargs):
        self.client = kwargs.pop("client", None)
        self._koda_session = None
        super().__init__(**kwargs)

    async def start(self) -> "KodaAsyncWebCrawler":
        if self.client:
            from koda.modules.browser.service import BrowserSession
            
            # Start the Koda BrowserSession context manager
            self._koda_session = BrowserSession()
            koda_context = await self._koda_session.__aenter__()
            
            # Construct KodaBrowserManager using the obtained context
            manager = KodaBrowserManager(context=koda_context, browser_config=self.crawler_strategy.browser_config) # type: ignore[attr-defined]
            self.crawler_strategy.browser_manager = manager # type: ignore[attr-defined]
            
        await super().start()
        return self

    async def close(self):
        await super().close()
        if self._koda_session:
            await self._koda_session.__aexit__(None, None, None)
            self._koda_session = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

import sys
import crawl4ai

crawl4ai.AsyncWebCrawler = KodaAsyncWebCrawler  # type: ignore[attr-defined]

if 'crawl4ai' in sys.modules:
    sys.modules['crawl4ai'].AsyncWebCrawler = KodaAsyncWebCrawler  # type: ignore[attr-defined]

class Crawl4AiTool(BrowserTool):
    """
    Adapter for crawl4ai that implements the BrowserTool protocol.
    DEPRECATED: Use the native KodaAsyncWebCrawler wrapper instead.
    """
    def __init__(self, browser_config: Optional[BrowserConfig] = None):
        self.browser_config = browser_config or BrowserConfig(headless=True)

    async def execute(self, context_or_page: Any, request: Any) -> Any:
        """
        Execute a crawl4ai scrape using the provided context.
        """
        # Create our custom manager and strategy
        manager = KodaBrowserManager(context=context_or_page, browser_config=self.browser_config)
        strategy = AsyncPlaywrightCrawlerStrategy(
            browser_config=self.browser_config,
            browser_manager=manager
        )
        # Override the manager in the strategy since __init__ might recreate it
        strategy.browser_manager = manager

        run_config = request.get("run_config") or CrawlerRunConfig()

        async with AsyncWebCrawler(crawler_strategy=strategy, config=self.browser_config) as crawler:
            # If there's a hook, set it
            hook = request.get("hook")
            if hook:
                crawler.crawler_strategy.set_hook("before_retrieve_html", hook)  # type: ignore[attr-defined]
                
            urls = request.get("urls")
            if urls:
                # Batch mode
                return await crawler.arun_many(
                    urls=urls,
                    config=run_config
                )
            else:
                # Single URL mode
                return await crawler.arun(
                    url=request.get("url"),
                    config=run_config
                )

    async def execute_stream(self, context_or_page: Any, request: Any) -> Any:
        """
        Execute a crawl4ai scrape using the provided context, yielding results as they arrive.
        """
        manager = KodaBrowserManager(context=context_or_page, browser_config=self.browser_config)
        strategy = AsyncPlaywrightCrawlerStrategy(
            browser_config=self.browser_config,
            browser_manager=manager
        )
        strategy.browser_manager = manager

        run_config = request.get("run_config") or CrawlerRunConfig()
        # Enforce stream mode
        run_config.stream = True

        async with AsyncWebCrawler(crawler_strategy=strategy, config=self.browser_config) as crawler:
            hook = request.get("hook")
            if hook:
                crawler.crawler_strategy.set_hook("before_retrieve_html", hook)  # type: ignore[attr-defined]
                
            stream = await crawler.arun(
                url=request.get("url"),
                config=run_config
            )
            async for result in stream:
                yield result
