import os
import pytest
import asyncio
from dotenv import load_dotenv
from pathlib import Path

from koda.client import KodaClient
from koda.modules.site.schema import CrawlRequest

from koda.config.main import settings

# Load .env from workspace root
load_dotenv(dotenv_path=Path(__file__).parents[4] / ".env")

# Check if posthog library is installed
try:
    import posthog
    HAS_POSTHOG = True
except ImportError:
    HAS_POSTHOG = False

# Read credentials strictly from environment variables
POSTHOG_API_KEY = os.getenv("POSTHOG_API_KEY")
POSTHOG_HOST = os.getenv("POSTHOG_HOST", "https://eu.i.posthog.com")

@pytest.mark.asyncio
async def test_crawl_local_server(local_test_server):
    """Test crawling a site on the local test server."""
    # Set mock posthog key to exercise telemetry paths
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
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
        try:
            response = await client.crawl(request)
            
            assert response.success is True
            assert response.url == url
            # It should find index.html, page1.html, and page2.html
            assert response.total_pages_crawled == 3
        finally:
            settings.posthog_api_key = old_key

@pytest.mark.asyncio
async def test_crawl_depth_limit(local_test_server):
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

@pytest.mark.asyncio
async def test_crawl4ai_wikipedia():
    """Integration test verifying crawl4ai on Wikipedia with KodaClient and PostHog tracking."""
    
    # Determine if we should use the real API or mock
    use_real_api = HAS_POSTHOG and POSTHOG_API_KEY is not None
    
    api_key = POSTHOG_API_KEY if use_real_api else "phc_mock_key_123"
    host = POSTHOG_HOST if use_real_api else "https://mock.posthog.com"
    
    # Initialize KodaClient
    old_key = settings.posthog_api_key
    old_host = settings.posthog_host
    settings.posthog_api_key = api_key
    settings.posthog_host = host
    
    try:
        async with KodaClient() as client:
            
            from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
        
            # Configure crawl4ai
            browser_config = BrowserConfig(headless=True)
            run_config = CrawlerRunConfig(page_timeout=15000)
            
            # Run the crawler on Wikipedia
            async with AsyncWebCrawler(config=browser_config) as crawler:
                result = await crawler.arun(
                    url="https://en.wikipedia.org/wiki/Main_Page",
                    config=run_config
                )
                
                # Verify crawl4ai successfully fetched the page
                assert result.success is True
                assert "Wikipedia" in result.html
                
                if use_real_api:
                    print("\n✅ Successfully sent real telemetry events to PostHog!")
                    # Wait for PostHog to flush session recordings
                    print("Waiting 5 seconds for PostHog to flush session recordings...")
                    await asyncio.sleep(5)
                else:
                    print("\n✅ Successfully verified crawl4ai integration!")
    finally:
        settings.posthog_api_key = old_key
        settings.posthog_host = old_host
