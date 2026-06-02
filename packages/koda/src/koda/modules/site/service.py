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

def _normalize_url(url: str, ignore_query: bool = False) -> str:
    """Normalize a URL by removing fragments and optionally query parameters."""
    url, _ = urldefrag(url)
    if ignore_query:
        parsed = urlparse(url)
        url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return url

def _is_valid_link(
    link: str,
    base_url: str,
    include_paths: List[str] | None,
    exclude_paths: List[str] | None,
    allow_subdomains: bool,
    crawl_entire_domain: bool,
    allow_external: bool,
    regex_on_full_url: bool
) -> bool:
    """Check if a link should be crawled based on the request configuration."""
    try:
        parsed_link = urlparse(link)
        parsed_base = urlparse(base_url)
    except Exception:
        return False

    # Check external
    is_external = parsed_link.netloc != parsed_base.netloc
    if is_external:
        if not allow_external:
            # Check subdomains
            if allow_subdomains and parsed_link.netloc.endswith(f".{parsed_base.netloc}"):
                pass
            else:
                return False

    # Check domain scope (if not external)
    if not is_external and not crawl_entire_domain:
        # Must be a child path
        if not parsed_link.path.startswith(parsed_base.path):
            return False

    # Check include/exclude paths
    target_for_regex = link if regex_on_full_url else parsed_link.path

    if exclude_paths:
        for pattern in exclude_paths:
            if re.search(pattern, target_for_regex):
                return False

    if include_paths:
        matched = False
        for pattern in include_paths:
            if re.search(pattern, target_for_regex):
                matched = True
                break
        if not matched:
            return False

    return True

async def crawl(request: CrawlRequest) -> CrawlResponse:
    """
    Execute a BFS crawl starting from the request URL.
    
    Args:
        request: The crawl configuration.
        
    Returns:
        A CrawlResponse summary.
    """
    base_url = str(request.url)
    
    # Initialize webhook if configured
    if request.webhook:
        await dispatch_webhook(request.webhook, "crawl.started", {"url": base_url})

    # Configure browser
    browser_config = BrowserConfig(
        headless=True,
        proxy=request.scrapeOptions.proxy if request.scrapeOptions.proxy != "auto" else None
    )

    # Configure crawler run
    run_config = CrawlerRunConfig(
        page_timeout=request.scrapeOptions.timeout,
        cache_mode=CacheMode.ENABLED if request.scrapeOptions.storeInCache else CacheMode.BYPASS,
        wait_for=f"delay:{request.scrapeOptions.waitFor}" if request.scrapeOptions.waitFor > 0 else None,
        exclude_external_links=not request.allowExternalLinks,
        screenshot="screenshot" in request.scrapeOptions.formats
    )

    if request.scrapeOptions.onlyMainContent:
        run_config.content_filter = PruningContentFilter()

    queue: List[Tuple[str, int]] = [(base_url, 0)]
    visited: Set[str] = set()
    total_crawled = 0

    async with AsyncWebCrawler(config=browser_config) as crawler:
        while queue and len(visited) < request.limit:
            # Pop up to maxConcurrency items
            batch_size = min(request.maxConcurrency, request.limit - len(visited), len(queue))
            current_batch = queue[:batch_size]
            queue = queue[batch_size:]

            urls_to_crawl = []
            depth_map = {}
            for url, depth in current_batch:
                norm_url = _normalize_url(url, request.ignoreQueryParameters)
                if norm_url not in visited:
                    visited.add(norm_url)
                    urls_to_crawl.append(url)
                    depth_map[url] = depth

            if not urls_to_crawl:
                continue

            # Add delay if specified
            if request.delay and total_crawled > 0:
                await asyncio.sleep(request.delay)

            # Execute batch
            results = await crawler.arun_many(urls=urls_to_crawl, config=run_config)

            for result in results:
                if not result.success:
                    if request.webhook:
                        await dispatch_webhook(request.webhook, "crawl.failed", {
                            "url": result.url,
                            "error": result.error_message
                        })
                    continue

                total_crawled += 1
                current_depth = depth_map.get(result.url, 0)

                # Dispatch page webhook
                if request.webhook:
                    page_data = {
                        "url": result.url,
                        "metadata": result.metadata
                    }
                    
                    formats = request.scrapeOptions.formats
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

                    await dispatch_webhook(request.webhook, "crawl.page", page_data)

                # Discover links if within depth
                if current_depth < request.maxDiscoveryDepth:
                    all_links = result.links.get("internal", [])
                    if request.allowExternalLinks:
                        all_links.extend(result.links.get("external", []))

                    for link_dict in all_links:
                        link_href = link_dict.get("href")
                        if not link_href:
                            continue
                            
                        norm_link = _normalize_url(link_href, request.ignoreQueryParameters)
                        if norm_link in visited:
                            continue

                        if _is_valid_link(
                            link_href,
                            base_url,
                            request.includePaths,
                            request.excludePaths,
                            request.allowSubdomains,
                            request.crawlEntireDomain,
                            request.allowExternalLinks,
                            request.regexOnFullURL
                        ):
                            queue.append((link_href, current_depth + 1))

    # Final completion webhook
    if request.webhook:
        await dispatch_webhook(request.webhook, "crawl.completed", {
            "url": base_url,
            "total_pages_crawled": total_crawled
        })

    return CrawlResponse(
        success=True,
        id="sync-crawl", # Windmill handles the real async job ID
        url=base_url,
        total_pages_crawled=total_crawled
    )
