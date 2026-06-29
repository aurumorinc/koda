import pytest
from koda.config.main import settings
from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest
from koda.use_cases.scrape_youtube_profile.service import scrape_youtube_profile

@pytest.fixture
def disable_posthog():
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    yield
    settings.posthog_api_key = old_key

@pytest.mark.asyncio
async def test_scrape_youtube_home_screenshot(disable_posthog):
    """Test just the 'home' tab, extracting 'screenshot' (which is the only format now)."""
    url = "https://www.youtube.com/@mkbhd"
    
    req = ScrapeYoutubeProfileRequest(
        url=url,
        formats=["screenshot"],
        tabs=["home"],
        timeout=120000,
        maxConcurrency=1
    )
    
    result = await scrape_youtube_profile(req)
    assert result.success is True, f"Scrape failed: {getattr(result, 'error', 'Unknown Error')}"
    data = result.data or []
    
    tab_names = [d.get("tab_name") for d in data]
    assert "About" in tab_names
    assert "Home" in tab_names
    assert len(tab_names) == 2, f"Expected only Home and About, got: {tab_names}"
    
    for d in data:
        assert "screenshot" in d, f"Expected 'screenshot' in {d.get('tab_name')}"
        assert d["screenshot"].startswith("data:image/jpeg;base64,"), "Expected valid base64 image string"
        assert "markdown" not in d, "Did not request Markdown (deprecated)"
        assert "html" not in d, "Did not request HTML (deprecated)"

@pytest.mark.asyncio
async def test_scrape_youtube_multiple_tabs_screenshot(disable_posthog):
    """Test multiple tabs ('videos', 'podcasts'). Assert screenshots are populated."""
    url = "https://www.youtube.com/@mkbhd"
    
    req = ScrapeYoutubeProfileRequest(
        url=url,
        formats=["screenshot"],
        tabs=["videos", "podcasts"],
        timeout=120000,
        maxConcurrency=1
    )
    
    result = await scrape_youtube_profile(req)
    assert result.success is True, f"Scrape failed: {getattr(result, 'error', 'Unknown Error')}"
    data = result.data or []
    
    tab_names = [d.get("tab_name") for d in data]
    assert "About" in tab_names
    assert "Videos" in tab_names
    assert "Podcasts" in tab_names
    
    for d in data:
        assert "screenshot" in d, f"Expected 'screenshot' in {d.get('tab_name')}"
        assert d["screenshot"].startswith("data:image/jpeg;base64,"), "Expected valid base64 image string"

@pytest.mark.asyncio
async def test_scrape_youtube_fake_tab_exclusion(disable_posthog):
    """Test `['fake-tab']` to ensure it fails fast and only returns the default 'About' tab."""
    url = "https://www.youtube.com/@mkbhd"
    
    req = ScrapeYoutubeProfileRequest(
        url=url,
        formats=["screenshot"],
        tabs=["fake-tab"],
        timeout=120000,
        maxConcurrency=1
    )
    
    result = await scrape_youtube_profile(req)
    assert result.success is True, f"Scrape failed: {getattr(result, 'error', 'Unknown Error')}"
    data = result.data or []
    
    tab_names = [d.get("tab_name") for d in data]
    assert "About" in tab_names, "About tab should be extracted automatically"
    assert "Fake-tab" not in tab_names, "Fake tab should not be extracted"
    assert len(tab_names) == 1, f"Expected only About, got: {tab_names}"
    
    for d in data:
        assert "screenshot" in d, f"Expected 'screenshot' in {d.get('tab_name')}"
        assert d["screenshot"].startswith("data:image/jpeg;base64,")
