import pytest
import asyncio

from koda.client import KodaClient
from koda.modules.site.schema import CrawlRequest

@pytest.mark.asyncio
async def test_e2e_crawl_local_server(local_test_server):
    """Test crawling a site on the local test server."""
    url = f"{local_test_server}/index.html"
    
    async with KodaClient() as client:
        # The local server has index.html, page1.html, and page2.html
        # index.html links to page1 and page2.
        # page1 and page2 link back to index.
        # So crawling from index.html with sufficient depth should find 3 pages.
        
        request = CrawlRequest(
            url=url,
            limit=10,
            maxDiscoveryDepth=2,
            crawlEntireDomain=True, # Allow crawling within the same domain
            maxConcurrency=1
        )
        response = await client.crawl(request)
        
        assert response.success is True
        assert response.url == url
        # It should find index.html, page1.html, and page2.html
        assert response.total_pages_crawled == 3

@pytest.mark.asyncio
async def test_e2e_crawl_depth_limit(local_test_server):
    """Test crawling with a depth limit."""
    url = f"{local_test_server}/index.html"
    
    async with KodaClient() as client:
        # With depth 0, it should only crawl the index page
        request = CrawlRequest(
            url=url,
            limit=10,
            maxDiscoveryDepth=0,
            crawlEntireDomain=True
        )
        response = await client.crawl(request)
        
        assert response.success is True
        assert response.total_pages_crawled == 1
