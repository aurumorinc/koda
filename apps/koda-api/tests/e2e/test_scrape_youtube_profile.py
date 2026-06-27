import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import import_script
from koda.config.main import settings

scrape_yt = import_script("f/koda/scouts/scrape_youtube_profile.py", "scrape_yt")

@pytest.mark.asyncio
async def test_scrape_youtube_profile_e2e(wmill_mock):
    """Test scraping a real YouTube profile."""
    # Temporarily disable posthog to speed up/avoid issues
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    url = "https://www.youtube.com/@mkbhd"
    
    try:
        # We only want to test a couple of tabs to keep the test fast
        result = await scrape_yt.main(
            url=url,
            formats=["markdown"],
            tabs=["home", "videos", "fake-tab-that-does-not-exist"],
            timeout=120000,
            s3_resource=None,
            webhook=None
        )
        
        assert result.get("success") is True, f"Scrape failed: {result.get('error')}"
        data = result.get("data", [])
        
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
