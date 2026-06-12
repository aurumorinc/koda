"""Service for crawling sites."""

from __future__ import annotations

import re
import asyncio
from typing import List, Set, Tuple
from urllib.parse import urljoin, urlparse, urldefrag

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter

from koda.modules.site.schema import CrawlRequest, CrawlResponse
from koda.modules.webhook.utils import dispatch_webhook

__all__ = ["crawl"]

class CrawlJob:
    """Encapsulates the BFS crawling logic and state for a site."""

    def __init__(self, request: CrawlRequest):
        self.request = request
        self.base_url = str(request.url)
        self.queue: List[Tuple[str, int]] = [(self.base_url, 0)]
        self.visited: Set[str] = set()
        self.total_crawled = 0

    def _normalize_url(self, url: str) -> str:
        """Normalize a URL by removing fragments and optionally query parameters."""
        url, _ = urldefrag(url)
        if self.request.ignoreQueryParameters:
            parsed = urlparse(url)
            url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        return url

    def _is_valid_link(self, link: str) -> bool:
        """Check if a link should be crawled based on the request configuration."""
        try:
            parsed_link = urlparse(link)
            parsed_base = urlparse(self.base_url)
        except Exception:
            return False

        # Check external
        is_external = parsed_link.netloc != parsed_base.netloc
        if is_external:
            if not self.request.allowExternalLinks:
                # Check subdomains
                if self.request.allowSubdomains and parsed_link.netloc.endswith(f".{parsed_base.netloc}"):
                    pass
                else:
                    return False

        # Check domain scope (if not external)
        if not is_external and not self.request.crawlEntireDomain:
            # Must be a child path
            if not parsed_link.path.startswith(parsed_base.path):
                return False

        # Check include/exclude paths
        target_for_regex = link if self.request.regexOnFullURL else parsed_link.path

        if self.request.excludePaths:
            for pattern in self.request.excludePaths:
                if re.search(pattern, target_for_regex):
                    return False

        if self.request.includePaths:
            matched = False
            for pattern in self.request.includePaths:
                if re.search(pattern, target_for_regex):
                    matched = True
                    break
            if not matched:
                return False

        return True

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

    async def _process_batch(self, crawler: AsyncWebCrawler, run_config: CrawlerRunConfig):
        """Process a batch of URLs from the queue."""
        batch_size = min(self.request.maxConcurrency, self.request.limit - len(self.visited), len(self.queue))
        current_batch = self.queue[:batch_size]
        self.queue = self.queue[batch_size:]

        urls_to_crawl = []
        depth_map = {}
        for url, depth in current_batch:
            norm_url = self._normalize_url(url)
            if norm_url not in self.visited:
                self.visited.add(norm_url)
                urls_to_crawl.append(url)
                depth_map[url] = depth

        if not urls_to_crawl:
            return

        # Add delay if specified
        if self.request.delay and self.total_crawled > 0:
            await asyncio.sleep(self.request.delay)

        # Execute batch
        results = await crawler.arun_many(urls=urls_to_crawl, config=run_config)

        for result in results:
            if not result.success:
                if self.request.webhook:
                    await dispatch_webhook(self.request.webhook, "crawl.failed", {
                        "url": result.url,
                        "error": result.error_message
                    })
                continue

            self.total_crawled += 1
            current_depth = depth_map.get(result.url, 0)

            await self._dispatch_page_webhook(result)

            # Discover links if within depth
            if current_depth < self.request.maxDiscoveryDepth:
                all_links = result.links.get("internal", [])
                if self.request.allowExternalLinks:
                    all_links.extend(result.links.get("external", []))

                for link_dict in all_links:
                    link_href = link_dict.get("href")
                    if not link_href:
                        continue
                        
                    norm_link = self._normalize_url(link_href)
                    if norm_link in self.visited:
                        continue

                    if self._is_valid_link(link_href):
                        self.queue.append((link_href, current_depth + 1))

    async def run(self) -> CrawlResponse:
        """Execute the BFS crawl starting from the request URL."""
        if self.request.webhook:
            await dispatch_webhook(self.request.webhook, "crawl.started", {"url": self.base_url})

        browser_config = BrowserConfig(
            headless=True,
            proxy=self.request.scrapeOptions.proxy if self.request.scrapeOptions.proxy != "auto" else None
        )

        run_config = CrawlerRunConfig(
            page_timeout=self.request.scrapeOptions.timeout,
            cache_mode=CacheMode.ENABLED if self.request.scrapeOptions.storeInCache else CacheMode.BYPASS,
            wait_for=f"delay:{self.request.scrapeOptions.waitFor}" if self.request.scrapeOptions.waitFor > 0 else None,
            exclude_external_links=not self.request.allowExternalLinks,
            screenshot="screenshot" in self.request.scrapeOptions.formats
        )

        if self.request.scrapeOptions.onlyMainContent:
            run_config.content_filter = PruningContentFilter()

        async with AsyncWebCrawler(config=browser_config) as crawler:
            while self.queue and len(self.visited) < self.request.limit:
                await self._process_batch(crawler, run_config)

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
