"""Service for crawling sites."""

from __future__ import annotations

import re
import asyncio
from typing import List, Set, Tuple, Any
from urllib.parse import urljoin, urlparse, urldefrag

from crawl4ai import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy, FilterChain, URLPatternFilter
from crawl4ai.async_configs import SeedingConfig
from crawl4ai.async_url_seeder import AsyncUrlSeeder

from koda.modules.site.schema import CrawlRequest, CrawlResponse
from koda.modules.webhook.utils import dispatch_webhook
from koda.modules.browser.service import BrowserSession
from koda.integrations.crawl4ai import Crawl4AiTool
from koda.modules.page.service import ScrapeJob

__all__ = ["crawl"]

class CrawlJob:
    """Encapsulates the BFS crawling logic and state for a site."""

    def __init__(self, request: CrawlRequest):
        self.request = request
        self.base_url = str(request.url)
        self.total_crawled = 0

    async def _dispatch_page_webhook(self, result):
        """Dispatch a webhook for a successfully crawled page."""
        if not self.request.webhook:
            return

        page_data = {
            "url": result.url,
            "metadata": result.metadata
        }
        
        formats = self.request.scrapeOptions.formats
        if "markdown" in formats:
            page_data["markdown"] = result.markdown
        if "html" in formats or "rawHtml" in formats:
            page_data["html"] = result.html
        if "links" in formats:
            page_data["links"] = result.links
        if "images" in formats:
            page_data["images"] = result.media.get("images", []) if result.media else []
        if "screenshot" in formats:
            page_data["screenshot"] = result.screenshot

        await dispatch_webhook(self.request.webhook, "crawl.page", page_data)

    async def run(self) -> CrawlResponse:
        """Execute the deep crawl starting from the request URL."""
        if self.request.webhook:
            await dispatch_webhook(self.request.webhook, "crawl.started", {"url": self.base_url})

        # Map filtering rules
        filters = []
        if self.request.includePaths:
            for p in self.request.includePaths:
                filters.append(URLPatternFilter(pattern=p))
        if self.request.excludePaths:
            for p in self.request.excludePaths:
                filters.append(URLPatternFilter(pattern=p, reverse=True))

        filter_chain = FilterChain(filters=filters) if filters else None

        # Sitemap logic
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
            finally:
                await seeder.close()

        # Browser Config
        browser_kwargs = {
            "headless": True,
            "proxy": self.request.scrapeOptions.proxy if self.request.scrapeOptions.proxy != "auto" else None,
            "headers": self.request.scrapeOptions.headers
        }
        if self.request.robotsUserAgent:
            browser_kwargs["user_agent"] = self.request.robotsUserAgent

        browser_config = BrowserConfig(**browser_kwargs)

        # Scrape Actions Hook (reuse from page.service if possible, or build equivalent)
        # We instantiate a dummy ScrapeJob to reuse its execute_actions_hook
        # Note: ScrapeRequest schema in koda.modules.page.schema must be matched
        dummy_scrape_job = None
        if self.request.scrapeOptions.actions:
            from koda.modules.page.schema import ScrapeRequest as PageScrapeRequest
            dummy_request = PageScrapeRequest(url=self.base_url, actions=self.request.scrapeOptions.actions)
            dummy_scrape_job = ScrapeJob(dummy_request)

        # Crawler Config
        run_config = CrawlerRunConfig(
            page_timeout=self.request.scrapeOptions.timeout,
            cache_mode=CacheMode.ENABLED if self.request.scrapeOptions.storeInCache else CacheMode.BYPASS,
            wait_for=f"delay:{self.request.scrapeOptions.waitFor}" if self.request.scrapeOptions.waitFor > 0 else None,
            exclude_external_links=not self.request.allowExternalLinks,
            screenshot="screenshot" in self.request.scrapeOptions.formats,
            check_robots_txt=not self.request.ignoreRobotsTxt,
            remove_overlay_elements=self.request.scrapeOptions.blockAds,
            remove_consent_popups=self.request.scrapeOptions.blockAds,
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=self.request.maxDiscoveryDepth,
                max_pages=self.request.limit,
                include_external=self.request.allowExternalLinks,
                filter_chain=filter_chain
            ) if self.request.sitemap != "only" else None # Don't deep crawl if sitemap only
        )

        if self.request.scrapeOptions.onlyMainContent:
            run_config.content_filter = PruningContentFilter()

        async with BrowserSession() as context:
            tool = Crawl4AiTool(browser_config=browser_config)
            
            # If sitemap="only", we might have thousands of URLs. We don't want to use deep_crawl.
            if self.request.sitemap == "only":
                # We chunk them to avoid passing thousands of URLs to execute() at once
                chunk_size = self.request.maxConcurrency or 10
                for i in range(0, min(len(urls_to_crawl), self.request.limit), chunk_size):
                    chunk = urls_to_crawl[i:i+chunk_size]
                    if self.request.delay and self.total_crawled > 0:
                        await asyncio.sleep(self.request.delay)
                        
                    results = await tool.execute(context, {
                        "urls": chunk,
                        "run_config": run_config,
                        "hook": dummy_scrape_job.execute_actions_hook if dummy_scrape_job else None
                    })
                    for result in results:
                        if result.success:
                            self.total_crawled += 1
                            await self._dispatch_page_webhook(result)
                        elif self.request.webhook:
                            await dispatch_webhook(self.request.webhook, "crawl.failed", {
                                "url": result.url,
                                "error": result.error_message
                            })
            else:
                # Use native BFS deep crawling with stream
                hook = dummy_scrape_job.execute_actions_hook if dummy_scrape_job else None
                async for result in tool.execute_stream(context, {
                    "url": self.base_url,
                    "run_config": run_config,
                    "hook": hook
                }):
                    if self.request.delay and self.total_crawled > 0:
                        await asyncio.sleep(self.request.delay)
                        
                    if result.success:
                        self.total_crawled += 1
                        await self._dispatch_page_webhook(result)
                    elif self.request.webhook:
                        await dispatch_webhook(self.request.webhook, "crawl.failed", {
                            "url": result.url,
                            "error": result.error_message
                        })
                        
                    if self.total_crawled >= self.request.limit:
                        break

        if self.request.webhook:
            await dispatch_webhook(self.request.webhook, "crawl.completed", {
                "url": self.base_url,
                "total_pages_crawled": self.total_crawled
            })

        return CrawlResponse(
            success=True,
            id="sync-crawl", # Windmill handles the real async job ID
            url=self.base_url,
            total_pages_crawled=self.total_crawled
        )


async def crawl(request: CrawlRequest) -> CrawlResponse:
    """
    Execute a BFS crawl starting from the request URL.
    
    Args:
        request: The crawl configuration.
        
    Returns:
        A CrawlResponse summary.
    """
    job = CrawlJob(request)
    return await job.run()
