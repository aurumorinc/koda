import asyncio
from typing import Dict, List, Any

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, FilterChain, URLPatternFilter
from crawl4ai.async_configs import SeedingConfig
from crawl4ai.async_url_seeder import AsyncUrlSeeder

from koda.client import KodaClient
from koda.utils.webhook.service import webhook_dispatch
from koda.use_cases.service import execute_actions
from .schema import CrawlRequest, CrawlResponse

class CrawlJob:
    def __init__(self, request: CrawlRequest):
        self.request = request
        self.base_url = str(request.url)
        self.total_crawled = 0

    async def execute_actions_hook(self, page, context, **kwargs):
        if not self.request.scrapeOptions.actions:
            return page

        # Pass a dummy action results since crawl doesn't collect them currently, 
        # or we can pass an empty dict
        dummy_results: Dict[str, list] = {}
        await execute_actions(page, self.request.scrapeOptions.actions, dummy_results)
        return page

    async def run(self) -> CrawlResponse:
        filters = []
        if self.request.includePaths:
            for p in self.request.includePaths:
                filters.append(URLPatternFilter(patterns=[p]))
        if self.request.excludePaths:
            for p in self.request.excludePaths:
                filters.append(URLPatternFilter(patterns=[p], reverse=True))

        filter_chain = FilterChain(filters=filters) if filters else None  # type: ignore

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

        browser_config = BrowserConfig(**browser_kwargs)  # type: ignore

        normalized_formats = []
        for f in self.request.scrapeOptions.formats:
            if isinstance(f, dict):
                normalized_formats.append(f.get("type", ""))
            else:
                normalized_formats.append(str(f))

        run_kwargs = {
            "page_timeout": self.request.scrapeOptions.timeout,
            "cache_mode": CacheMode.ENABLED if self.request.scrapeOptions.storeInCache else CacheMode.BYPASS,
            "wait_for": f"delay:{self.request.scrapeOptions.waitFor}" if self.request.scrapeOptions.waitFor > 0 else None,
            "exclude_external_links": not self.request.allowExternalLinks,
            "screenshot": "screenshot" in normalized_formats,
            "check_robots_txt": not self.request.ignoreRobotsTxt,
            "remove_overlay_elements": self.request.scrapeOptions.blockAds,
            "remove_consent_popups": self.request.scrapeOptions.blockAds,
            "deep_crawl_strategy": BFSDeepCrawlStrategy(
                max_depth=self.request.maxDiscoveryDepth,
                max_pages=self.request.limit,
                include_external=self.request.allowExternalLinks,
                filter_chain=filter_chain  # type: ignore
            ) if self.request.sitemap != "only" else None
        }
        run_config = CrawlerRunConfig(**run_kwargs)  # type: ignore

        if self.request.scrapeOptions.onlyMainContent:
            run_config.content_filter = PruningContentFilter()

        async with KodaClient() as client:
            async with AsyncWebCrawler(client=client, config=browser_config) as crawler:
                if self.request.scrapeOptions.actions:
                    crawler.crawler_strategy.set_hook("before_retrieve_html", self.execute_actions_hook)  # type: ignore

                if self.request.sitemap == "only":
                    chunk_size = self.request.maxConcurrency or 10
                    for i in range(0, min(len(urls_to_crawl), self.request.limit), chunk_size):
                        chunk = urls_to_crawl[i:i+chunk_size]
                        if self.request.delay and self.total_crawled > 0:
                            await asyncio.sleep(self.request.delay)
                            
                        res_obj = await crawler.arun_many(urls=chunk, config=run_config)  # type: ignore
                        results: List[Any] = []
                        if hasattr(res_obj, "__aiter__"):
                            results = [r async for r in res_obj]  # type: ignore
                        else:
                            results = list(res_obj)  # type: ignore
                            
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

@webhook_dispatch
async def crawl(request: CrawlRequest) -> CrawlResponse:
    job = CrawlJob(request)
    return await job.run()
