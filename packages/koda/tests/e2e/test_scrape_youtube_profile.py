import pytest
from koda.config.main import settings
from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest
from koda.use_cases.scrape_youtube_profile.service import scrape_youtube_profile

@pytest.mark.asyncio
async def test_scrape_youtube_profile_e2e():
    """Test scraping a real YouTube profile."""
    # Temporarily disable posthog to speed up/avoid issues
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    url = "https://www.youtube.com/@mkbhd"
    
    try:
        # We only want to test a couple of tabs to keep the test fast
        req = ScrapeYoutubeProfileRequest(
            url=url,
            formats=["markdown"],
            tabs=["home", "videos", "fake-tab-that-does-not-exist"],
            timeout=120000,
            s3_resource=None,
            webhook=None,
            maxConcurrency=2
        )
        
        result = await scrape_youtube_profile(req)
        
        assert result.success is True, f"Scrape failed: {getattr(result, 'error', 'Unknown Error')}"
        data = result.data or []
        
        assert isinstance(data, list)
        
        # Verify the tabs returned
        tab_names = [d.get("tab_name") for d in data]
        
        assert "About" in tab_names, "About tab should be extracted automatically"
        assert "Home" in tab_names, "Home tab should be extracted"
        assert "Videos" in tab_names, "Videos tab should be extracted"
        
        # 'fake-tab-that-does-not-exist' should have failed fast and not be in the output
        assert "Fake-tab-that-does-not-exist" not in tab_names
        
    finally:
        settings.posthog_api_key = old_key

@pytest.mark.asyncio
async def test_scrape_youtube_profile_performance():
    """Test scraping a heavy YouTube profile to ensure it completes quickly and successfully with optimizations."""
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    url = "https://www.youtube.com/@LinusTechTips"
    
    import time
    start_time = time.time()
    
    try:
        req = ScrapeYoutubeProfileRequest(
            url=url,
            formats=["markdown"],
            tabs=["home", "videos", "shorts", "streams", "podcasts", "playlists", "community", "store"],
            timeout=120000,
            s3_resource=None,
            webhook=None,
            maxConcurrency=3
        )
        
        result = await scrape_youtube_profile(req)
        
        elapsed_time = time.time() - start_time
        
        assert result.success is True, f"Scrape failed: {getattr(result, 'error', 'Unknown error')}"
        data = result.data or []
        assert isinstance(data, list)
        
        # Ensure that it completes reasonably fast (e.g. < 200 seconds for all 8 tabs).
        # We use 200 seconds to be generous in CI environments, but it should typically run much faster now.
        assert elapsed_time < 200, f"Scrape took too long: {elapsed_time}s"
            
    finally:
        settings.posthog_api_key = old_key
