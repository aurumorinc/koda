# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.4.2#subdirectory=packages/koda",
# ]
# ///
import asyncio
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, ConfigDict

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, FilterChain, URLPatternFilter
from crawl4ai.async_configs import SeedingConfig
from crawl4ai.async_url_seeder import AsyncUrlSeeder

from koda import (
    KodaClient,
    Webhook,
    webhook_dispatch,
)

class Action(BaseModel):
    type: str
    selector: Optional[str] = None
    value: Optional[Any] = None
    milliseconds: Optional[int] = None
    text: Optional[str] = None
    key: Optional[str] = None
    script: Optional[str] = None
    direction: Optional[str] = None
    amount: Optional[int] = None
    all: Optional[bool] = None
    fullPage: Optional[bool] = None
    quality: Optional[int] = None
    viewport: Optional[Dict[str, int]] = None
    format: Optional[str] = None
    landscape: Optional[bool] = None
    scale: Optional[float] = None
    timeout: Optional[int] = None
    ignoreError: Optional[bool] = Field(default=True)

class ScrapeOptions(BaseModel):
    formats: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: ["markdown"])
    onlyMainContent: bool = True
    onlyCleanContent: bool = False
    includeTags: Optional[List[str]] = None
    excludeTags: Optional[List[str]] = None
    maxAge: int = 172800000
    minAge: Optional[int] = None
    headers: Optional[Dict[str, str]] = None
    waitFor: int = 0
    mobile: bool = False
    skipTlsVerification: bool = True
    timeout: int = Field(default=60000, ge=1000, le=300000)
    parsers: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: ["pdf"])
    actions: Optional[List[Action]] = None
    location: Optional[Dict[str, Any]] = None
    removeBase64Images: bool = True
    blockAds: bool = True
    proxy: str = "auto"
    storeInCache: bool = True
    lockdown: bool = False
    profile: Optional[Dict[str, Any]] = None

class CrawlRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    url: str
    prompt: Optional[str] = None
    excludePaths: Optional[List[str]] = None
    includePaths: Optional[List[str]] = None
    maxDiscoveryDepth: int = 0
    sitemap: str = "include"
    ignoreQueryParameters: bool = False
    regexOnFullURL: bool = False
    limit: int = 10000
    crawlEntireDomain: bool = False
    allowExternalLinks: bool = False
    allowSubdomains: bool = False
    ignoreRobotsTxt: bool = False
    robotsUserAgent: Optional[str] = None
    delay: Optional[float] = None
    maxConcurrency: int = 10
    webhook: Optional[Webhook] = None
    scrapeOptions: ScrapeOptions = Field(default_factory=ScrapeOptions)
    zeroDataRetention: bool = False

class CrawlResponse(BaseModel):
    success: bool
    id: str
    url: str
    total_pages_crawled: Optional[int] = None
    error: Optional[str] = None

class CrawlJob:
    def __init__(self, request: CrawlRequest):
        self.request = request
        self.base_url = str(request.url)
        self.total_crawled = 0

    async def execute_actions_hook(self, page, context, **kwargs):
        if not self.request.scrapeOptions.actions:
            return page

        for action in self.request.scrapeOptions.actions:
            try:
                if action.type == "wait":
                    if action.milliseconds:
                        await asyncio.sleep(action.milliseconds / 1000.0)
                    elif action.selector:
                        kwargs_wait = {}
                        if action.timeout is not None:
                            kwargs_wait["timeout"] = action.timeout
                        await page.wait_for_selector(action.selector, **kwargs_wait)
                
                elif action.type == "click":
                    kwargs_click = {}
                    if action.timeout is not None:
                        kwargs_click["timeout"] = action.timeout
                    if action.selector:
                        if action.all:
                            elements = await page.query_selector_all(action.selector)
                            for el in elements:
                                await el.click(**kwargs_click)
                        else:
                            await page.click(action.selector, **kwargs_click)
                
                elif action.type == "write":
                    if action.text:
                        await page.keyboard.type(action.text)
                
                elif action.type == "press":
                    if action.key:
                        await page.keyboard.press(action.key)
                
                elif action.type == "scroll":
                    direction = action.direction or "down"
                    amount = action.amount or 1000
                    if action.selector:
                        await page.evaluate(f"""
                            const el = document.querySelector('{action.selector}');
                            if (el) {{
                                el.scrollBy(0, {amount if direction == 'down' else -amount});
                            }}
                        """)
                    else:
                        await page.mouse.wheel(0, amount if direction == 'down' else -amount)
                
                elif action.type == "executeJavascript":
                    if action.script:
                        await page.evaluate(action.script)
                    
            except Exception as e:
                print(f"Action {action.type} failed: {str(e)}")
                if hasattr(action, 'ignoreError') and action.ignoreError is False:
                    raise
        return page

    async def run(self) -> CrawlResponse:
        filters = []
        if self.request.includePaths:
            for p in self.request.includePaths:
                filters.append(URLPatternFilter(pattern=p))
        if self.request.excludePaths:
            for p in self.request.excludePaths:
                filters.append(URLPatternFilter(pattern=p, reverse=True))

        filter_chain = FilterChain(filters=filters) if filters else None

        urls_to_crawl = [self.base_url]
        if self.request.sitemap in ("only", "include"):
            seeder = AsyncUrlSeeder()
            try:
                sitemap_results = await seeder.urls(
                    self.base_url,
                    SeedingConfig(source="sitemap", extract_head=False)
                )
                if self.request.sitemap == "only":
                    urls_to_crawl = [r["url"] for r in sitemap_results]
                else:
                    urls_to_crawl.extend([r["url"] for r in sitemap_results])
            except Exception:
                pass
            finally:
                await seeder.close()

        browser_kwargs = {
            "headless": True,
            "proxy": self.request.scrapeOptions.proxy if self.request.scrapeOptions.proxy != "auto" else None,
            "headers": self.request.scrapeOptions.headers
        }
        if self.request.robotsUserAgent:
            browser_kwargs["user_agent"] = self.request.robotsUserAgent

        browser_config = BrowserConfig(**browser_kwargs)

        normalized_formats = []
        for f in self.request.scrapeOptions.formats:
            if isinstance(f, dict):
                normalized_formats.append(f.get("type", ""))
            else:
                normalized_formats.append(str(f))

        run_config = CrawlerRunConfig(
            page_timeout=self.request.scrapeOptions.timeout,
            cache_mode=CacheMode.ENABLED if self.request.scrapeOptions.storeInCache else CacheMode.BYPASS,
            wait_for=f"delay:{self.request.scrapeOptions.waitFor}" if self.request.scrapeOptions.waitFor > 0 else None,
            exclude_external_links=not self.request.allowExternalLinks,
            screenshot="screenshot" in normalized_formats,
            check_robots_txt=not self.request.ignoreRobotsTxt,
            remove_overlay_elements=self.request.scrapeOptions.blockAds,
            remove_consent_popups=self.request.scrapeOptions.blockAds,
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=self.request.maxDiscoveryDepth,
                max_pages=self.request.limit,
                include_external=self.request.allowExternalLinks,
                filter_chain=filter_chain
            ) if self.request.sitemap != "only" else None
        )

        if self.request.scrapeOptions.onlyMainContent:
            run_config.content_filter = PruningContentFilter()

        async with KodaClient() as client:
            async with AsyncWebCrawler(client=client, config=browser_config) as crawler:
                if self.request.scrapeOptions.actions:
                    crawler.crawler_strategy.set_hook("before_retrieve_html", self.execute_actions_hook)

                if self.request.sitemap == "only":
                    chunk_size = self.request.maxConcurrency or 10
                    for i in range(0, min(len(urls_to_crawl), self.request.limit), chunk_size):
                        chunk = urls_to_crawl[i:i+chunk_size]
                        if self.request.delay and self.total_crawled > 0:
                            await asyncio.sleep(self.request.delay)
                            
                        results = await crawler.arun_many(urls=chunk, config=run_config)
                        for result in results:
                            if result.success:
                                self.total_crawled += 1
                else:
                    run_config.stream = True
                    stream = await crawler.arun(url=self.base_url, config=run_config)
                    async for result in stream:
                        if self.request.delay and self.total_crawled > 0:
                            await asyncio.sleep(self.request.delay)
                            
                        if result.success:
                            self.total_crawled += 1
                            
                        if self.total_crawled >= self.request.limit:
                            break

        return CrawlResponse(
            success=True,
            id="sync-crawl",
            url=self.base_url,
            total_pages_crawled=self.total_crawled
        )

async def _execute_crawl_job(request: CrawlRequest) -> CrawlResponse:
    job = CrawlJob(request)
    return await job.run()

@webhook_dispatch
async def main(
    url: str,
    prompt: Optional[str] = None,
    excludePaths: Optional[List[str]] = None,
    includePaths: Optional[List[str]] = None,
    maxDiscoveryDepth: int = 0,
    sitemap: str = "include",
    ignoreQueryParameters: bool = False,
    regexOnFullURL: bool = False,
    limit: int = 10000,
    crawlEntireDomain: bool = False,
    allowExternalLinks: bool = False,
    allowSubdomains: bool = False,
    ignoreRobotsTxt: bool = False,
    robotsUserAgent: Optional[str] = None,
    delay: Optional[float] = None,
    maxConcurrency: int = 10,
    webhook: Optional[Webhook] = None,
    scrapeOptions: ScrapeOptions = ScrapeOptions(),
    zeroDataRetention: bool = False,
    **kwargs
) -> dict:
    """
    Execute a BFS crawl starting from the request URL using Koda infrastructure.
    """
    request = CrawlRequest(
        url=url,
        prompt=prompt,
        excludePaths=excludePaths,
        includePaths=includePaths,
        maxDiscoveryDepth=maxDiscoveryDepth,
        sitemap=sitemap,
        ignoreQueryParameters=ignoreQueryParameters,
        regexOnFullURL=regexOnFullURL,
        limit=limit,
        crawlEntireDomain=crawlEntireDomain,
        allowExternalLinks=allowExternalLinks,
        allowSubdomains=allowSubdomains,
        ignoreRobotsTxt=ignoreRobotsTxt,
        robotsUserAgent=robotsUserAgent,
        delay=delay,
        maxConcurrency=maxConcurrency,
        webhook=webhook,
        scrapeOptions=scrapeOptions,
        zeroDataRetention=zeroDataRetention
    )
    
    try:
        response = await _execute_crawl_job(request)
        return response.model_dump(by_alias=True, exclude_none=True)
    except Exception as e:
        error_msg = str(e)
        return {"success": False, "id": "sync-crawl", "url": url, "error": error_msg}

def _run_main_sync(*args, **kwargs):
    return asyncio.run(main(*args, **kwargs))
