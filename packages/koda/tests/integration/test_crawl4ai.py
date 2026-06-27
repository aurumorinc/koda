import pytest
import koda # triggers patching
from koda.client import KodaClient
from crawl4ai import AsyncWebCrawler

@pytest.mark.asyncio
async def test_crawl4ai_integration(local_test_server):
    """Test that Crawl4AI can successfully use a KodaClient."""
    koda_client_instance = KodaClient()
    
    async with AsyncWebCrawler(client=koda_client_instance) as crawler:
        result = await crawler.arun(url=f"{local_test_server}/index.html")
        
        assert result.success is True
        assert "Welcome to the Test Server" in result.html
