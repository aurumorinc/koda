import asyncio
from datetime import datetime, timezone, timedelta
from typing import Any, Mapping, Sequence, Optional
from types import TracebackType

from playwright.async_api import BrowserContext, Page
from crawlee.browsers._browser_controller import BrowserController
from crawlee.browsers._browser_plugin import BrowserPlugin
from crawlee.browsers._types import BrowserType
from crawlee.proxy_configuration import ProxyInfo
from crawlee.crawlers import PlaywrightCrawler as NativePlaywrightCrawler
from crawlee.browsers import BrowserPool


class KodaBrowserController(BrowserController):
    """A browser controller that simply yields pages from a pre-existing Koda BrowserContext."""
    
    AUTOMATION_LIBRARY = 'playwright'

    def __init__(self, context: BrowserContext):
        self._context = context
        self._pages: list[Page] = []
        self._total_opened_pages = 0
        self._last_page_opened_at = datetime.now(timezone.utc)
        self._is_closed = False

    @property
    def pages(self) -> list[Page]:
        return self._pages.copy()

    @property
    def total_opened_pages(self) -> int:
        return self._total_opened_pages

    @property
    def pages_count(self) -> int:
        return len(self._pages)

    @property
    def last_page_opened_at(self) -> datetime:
        return self._last_page_opened_at

    @property
    def idle_time(self) -> timedelta:
        return datetime.now(timezone.utc) - self._last_page_opened_at

    @property
    def has_free_capacity(self) -> bool:
        # Koda manages capacity globally, we can just allow it
        return True

    @property
    def is_browser_connected(self) -> bool:
        return not self._is_closed

    @property
    def browser_type(self) -> BrowserType:
        return 'chromium'

    async def new_page(
        self,
        browser_new_context_options: Mapping[str, Any] | None = None,
        proxy_info: ProxyInfo | None = None,
    ) -> Page:
        page = await self._context.new_page()
        
        async def _on_close(*args, **kwargs):
            if page in self._pages:
                self._pages.remove(page)

        page.on('close', _on_close)
        
        self._pages.append(page)
        self._total_opened_pages += 1
        self._last_page_opened_at = datetime.now(timezone.utc)
        return page

    async def close(self, *, force: bool = False) -> None:
        """
        We DO NOT close the underlying context because Koda's BrowserSession manages its lifecycle.
        We only close the pages that were opened by this controller.
        """
        self._is_closed = True
        for page in self._pages:
            try:
                await page.close()
            except Exception:
                pass
        self._pages.clear()

class KodaBrowserPlugin(BrowserPlugin):
    """A browser plugin that returns a KodaBrowserController wrapped around a pre-existing Koda context."""
    
    AUTOMATION_LIBRARY = 'playwright'
    
    def __init__(self, context: BrowserContext):
        self._context = context
        self._active = False

    @property
    def active(self) -> bool:
        return self._active

    @property
    def browser_type(self) -> BrowserType:
        return 'chromium'

    @property
    def browser_launch_options(self) -> Mapping[str, Any]:
        return {}

    @property
    def browser_new_context_options(self) -> Mapping[str, Any]:
        return {}

    @property
    def max_open_pages_per_browser(self) -> int:
        return 100000  # Arbitrary high number since Koda manages capacity

    async def __aenter__(self) -> 'KodaBrowserPlugin':
        self._active = True
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_traceback: TracebackType | None) -> None:
        self._active = False

    async def new_browser(self) -> BrowserController:
        return KodaBrowserController(self._context)

class PlaywrightCrawler(NativePlaywrightCrawler):
    """
    A Koda-integrated PlaywrightCrawler that injects the KodaClient and
    wraps the entire crawl execution within Koda's BrowserSession.
    """
    def __init__(
        self,
        *args,
        client: Optional['KodaClient'] = None,  # type: ignore
        **kwargs
    ):
        self.client = client
        # We don't initialize the browser_pool here because we need the context
        # which is only available inside the run() async context.
        # But Crawlee might require it. We will override it in run().
        super().__init__(*args, **kwargs)

    async def run(self, *args, **kwargs) -> None:
        """
        Executes the crawl inside a Koda BrowserSession, ensuring that
        we use Koda's invisible-playwright instance and telemetry.
        """
        from koda.modules.browser.service import BrowserSession
        
        async with BrowserSession() as koda_context:
            # We construct a custom BrowserPool using our KodaBrowserPlugin
            # to intercept browser launches and use Koda's context.
            plugin = KodaBrowserPlugin(koda_context)
            
            # Create a custom pool that uses our plugin
            koda_browser_pool = BrowserPool(
                plugins=[plugin],
                # Disable retiring browsers since Koda manages the context lifetime
                retire_browser_after_page_count=0
            )
            
            # Replace the crawler's default browser pool with our custom one
            self._browser_pool = koda_browser_pool
            
            # Also ensure the pool is started correctly.
            # NativePlaywrightCrawler normally starts the pool in its own run method.
            # We can let the parent run() handle the execution.
            await super().run(*args, **kwargs)
