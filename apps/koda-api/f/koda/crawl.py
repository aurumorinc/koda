# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.7.0#subdirectory=packages/koda",
# ]
# ///
import asyncio
from typing import Optional, List, Dict, Any

from koda import Webhook
from koda.use_cases.crawl.schema import CrawlRequest, ScrapeOptions
from koda.use_cases.crawl.service import crawl

def main(
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
        response = asyncio.run(crawl(request))
        return response.model_dump(by_alias=True, exclude_none=True)
    except Exception as e:
        error_msg = str(e)
        return {"success": False, "id": "sync-crawl", "url": url, "error": error_msg}
