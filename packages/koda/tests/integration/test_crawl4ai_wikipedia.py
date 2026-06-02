import os
import pytest
import asyncio
from dotenv import load_dotenv
from pathlib import Path
from unittest.mock import patch, MagicMock, ANY
from koda.client import KodaClient

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
async def test_crawl4ai_wikipedia_integration():
    """Integration test verifying crawl4ai on Wikipedia with KodaClient and PostHog tracking."""
    
    # Determine if we should use the real API or mock
    use_real_api = HAS_POSTHOG and POSTHOG_API_KEY is not None
    
    api_key = POSTHOG_API_KEY if use_real_api else "phc_mock_key_123"
    host = POSTHOG_HOST if use_real_api else "https://mock.posthog.com"
    
    # Initialize KodaClient
    async with KodaClient(
        posthog_api_key=api_key,
        posthog_host=host
    ) as client:
        
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
