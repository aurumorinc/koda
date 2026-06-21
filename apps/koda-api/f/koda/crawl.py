# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@26.6.34#subdirectory=packages/koda",
# ]
# ///
import asyncio
import wmill
from typing import Dict, Any, Optional, List

from koda import KodaClient, CrawlRequest

async def _run_crawl(
    url: str,
    limit: int,
    maxDiscoveryDepth: int,
    allowExternalLinks: bool,
    allowSubdomains: bool,
    crawlEntireDomain: bool,
    ignoreQueryParameters: bool,
    regexOnFullURL: bool,
    excludePaths: Optional[List[str]],
    includePaths: Optional[List[str]],
    maxConcurrency: int,
    delay: Optional[float],
    webhook: Optional[Dict[str, Any]],
    scrapeOptions: Optional[Dict[str, Any]],
    **kwargs
) -> Dict[str, Any]:
    try:
        async with KodaClient() as client:
            request = CrawlRequest(
                url=url,
                limit=limit,
                maxDiscoveryDepth=maxDiscoveryDepth,
                allowExternalLinks=allowExternalLinks,
                allowSubdomains=allowSubdomains,
                crawlEntireDomain=crawlEntireDomain,
                ignoreQueryParameters=ignoreQueryParameters,
                regexOnFullURL=regexOnFullURL,
                excludePaths=excludePaths,
                includePaths=includePaths,
                maxConcurrency=maxConcurrency,
                delay=delay,
                webhook=webhook,
                scrapeOptions=scrapeOptions or {}
            )
            
            response = await client.crawl(request)
            
            return response.model_dump()
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main(
    url: str,
    limit: int = 10000,
    maxDiscoveryDepth: int = 0,
    allowExternalLinks: bool = False,
    allowSubdomains: bool = False,
    crawlEntireDomain: bool = False,
    ignoreQueryParameters: bool = False,
    regexOnFullURL: bool = False,
    excludePaths: Optional[List[str]] = None,
    includePaths: Optional[List[str]] = None,
    maxConcurrency: int = 10,
    delay: Optional[float] = None,
    webhook: Optional[Dict[str, Any]] = None,
    scrapeOptions: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Crawl a site starting from a URL and extract information using Koda.
    """
    return asyncio.run(_run_crawl(
        url=url,
        limit=limit,
        maxDiscoveryDepth=maxDiscoveryDepth,
        allowExternalLinks=allowExternalLinks,
        allowSubdomains=allowSubdomains,
        crawlEntireDomain=crawlEntireDomain,
        ignoreQueryParameters=ignoreQueryParameters,
        regexOnFullURL=regexOnFullURL,
        excludePaths=excludePaths,
        includePaths=includePaths,
        maxConcurrency=maxConcurrency,
        delay=delay,
        webhook=webhook,
        scrapeOptions=scrapeOptions,
        **kwargs
    ))
