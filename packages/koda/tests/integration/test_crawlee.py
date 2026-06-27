import pytest
import koda # triggers patching
from koda.client import KodaClient
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext

@pytest.mark.asyncio
async def test_crawlee_integration(local_test_server):
    """Test that Crawlee can successfully mount to a BrowserSession and navigate via KodaClient."""
    visited = []
    koda_client_instance = KodaClient()
    
    crawler = PlaywrightCrawler(client=koda_client_instance, headless=True, max_requests_per_crawl=1)  # type: ignore[call-arg]
    
    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        visited.append(context.request.url)
        
    await crawler.run([f"{local_test_server}/index.html"])
    
    assert len(visited) == 1
    assert visited[0] == f"{local_test_server}/index.html"
