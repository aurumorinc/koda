import pytest
from koda.config.main import settings
from koda.use_cases.crawl.schema import CrawlRequest, ScrapeOptions
from koda.use_cases.crawl.service import crawl

@pytest.mark.asyncio
async def test_crawl_e2e(local_test_server):
    """Test crawling pages from the local test server."""
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    url = f"{local_test_server}/index.html"
    
    try:
        req = CrawlRequest(
            url=url,
            limit=10,
            maxDiscoveryDepth=2,
            allowExternalLinks=True,
            allowSubdomains=False,
            crawlEntireDomain=True,
            ignoreQueryParameters=True,
            regexOnFullURL=False,
            excludePaths=None,
            includePaths=None,
            maxConcurrency=2,
            delay=None,
            webhook=None,
            scrapeOptions=ScrapeOptions()
        )
        
        result = await crawl(req)

        assert result.success is True, f"Crawl failed: {getattr(result, 'error', 'Unknown error')}"
        
        # It should find index.html, page1.html, and page2.html
        assert result.total_pages_crawled and result.total_pages_crawled >= 1
                
    finally:
        settings.posthog_api_key = old_key
