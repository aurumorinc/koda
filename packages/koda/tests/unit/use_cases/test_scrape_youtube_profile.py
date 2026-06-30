import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from crawlee import Request
from crawlee.crawlers import PlaywrightCrawlingContext

from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest
from koda.use_cases.scrape_youtube_profile.service import scrape_youtube_profile, _handler, _validate_redirect, tab_handler

@pytest.fixture
def mock_crawlee():
    with patch("koda.use_cases.scrape_youtube_profile.service.PlaywrightCrawler", autospec=True) as mock:
        yield mock

@pytest.fixture
def mock_koda_client():
    with patch("koda.use_cases.scrape_youtube_profile.service.KodaClient", autospec=True) as mock:
        yield mock

@pytest.mark.asyncio
async def test_scrape_youtube_profile_success(mock_crawlee, mock_koda_client):
    client_instance = AsyncMock()
    mock_koda_client.return_value.__aenter__.return_value = client_instance
    
    crawler_instance = AsyncMock()
    mock_crawlee.return_value = crawler_instance
    
    # Mock crawler dataset
    dataset_mock = AsyncMock()
    data_mock = MagicMock()
    data_mock.items = [
        {"url": "https://youtube.com/@test", "screenshot_base64": "AABB", "screenshot_filename": "about.png"},
        {"url": "https://youtube.com/@test/videos", "screenshot_base64": "AACC", "screenshot_filename": "videos.png"}
    ]
    dataset_mock.get_data.return_value = data_mock
    crawler_instance.get_dataset.return_value = dataset_mock

    req = ScrapeYoutubeProfileRequest(url="https://youtube.com/@test", formats=["screenshot"], tabs=["about", "videos"])
    res = await scrape_youtube_profile(req)
    
    # Verify PlaywrightCrawler was initialized with the 2048MB memory limit
    _, crawler_kwargs = mock_crawlee.call_args
    assert "configuration" in crawler_kwargs, "Configuration was not passed to PlaywrightCrawler"
    assert crawler_kwargs["configuration"].memory_mbytes == 2048, "Memory limit was not set to 2048MB"
    
    assert res.success is True
    assert res.data is not None
    assert len(res.data) == 2
    assert res.data[0]["url"] == "https://youtube.com/@test"
    assert res.data[1]["url"] == "https://youtube.com/@test/videos"

@pytest.mark.asyncio
async def test_default_handler_routing():
    context_mock = AsyncMock()
    context_mock.page = AsyncMock()
    context_mock.page.url = "https://youtube.com/@testuser"
    context_mock.request = Request.from_url("https://youtube.com/@testuser")
    
    # Mocking page.evaluate to simulate tabs found
    context_mock.page.evaluate.return_value = ["home", "videos"]
    
    await _handler(context_mock)
    
    # DIALOG (1) + home (1) + videos (1) = 3
    assert context_mock.add_requests.call_count == 3
    
    dialog_call = context_mock.add_requests.call_args_list[0][0][0]
    assert dialog_call[0].label == "DIALOG"
    assert dialog_call[0].url == "https://youtube.com/@testuser"

@pytest.mark.asyncio
async def test_default_handler_no_home_tab():
    context_mock = AsyncMock()
    context_mock.page = AsyncMock()
    context_mock.page.url = "https://youtube.com/@testuser"
    context_mock.request = Request.from_url("https://youtube.com/@testuser")
    
    # Mocking page.evaluate to simulate no 'home' tab
    context_mock.page.evaluate.return_value = ["videos", "shorts"]
    
    await _handler(context_mock)
    
    # DIALOG (1) + videos (1) + shorts (1) = 3 requests
    assert context_mock.add_requests.call_count == 3
    
    # Ensure none of the enqueued tabs have slug 'featured'
    for i in range(1, 3):
        tab_call = context_mock.add_requests.call_args_list[i][0][0]
        assert "featured" not in tab_call[0].url

@pytest.mark.asyncio
async def test_validate_redirect():
    page_mock = AsyncMock()
    page_mock.is_closed = MagicMock(return_value=False)
    
    # Valid redirect
    page_mock.url = "https://youtube.com/@test/videos"
    
    res = await _validate_redirect(page_mock, "videos")
    assert res is True
    
    # Invalid URL pattern
    page_mock.url = "https://youtube.com/@test/featured"
    res = await _validate_redirect(page_mock, "videos")
    assert res is False
    
    # Test featured slug valid redirect
    page_mock.url = "https://youtube.com/@test/featured"
    res = await _validate_redirect(page_mock, "featured")
    assert res is True

    # Test featured slug invalid redirect (e.g. redirected to videos because home doesn't exist)
    page_mock.url = "https://youtube.com/@test/videos"
    res = await _validate_redirect(page_mock, "featured")
    assert res is False
    
@pytest.mark.asyncio
@patch("koda.use_cases.scrape_youtube_profile.service.scroll_to", autospec=True)
@patch("koda.use_cases.scrape_youtube_profile.service.screenshot", autospec=True)
async def test_tab_handler_scroll_bounds(mock_screenshot, mock_scroll_to):
    context_mock = AsyncMock()
    context_mock.page = AsyncMock()
    context_mock.page.is_closed = MagicMock(return_value=False)
    context_mock.page.url = "https://youtube.com/@test/videos"
    context_mock.request = Request.from_url("https://youtube.com/@test/videos", user_data={"slug": "videos", "full_page": True})
    
    # Mock screenshot to return bytes
    mock_screenshot.return_value = b"bytes"
    
    await tab_handler(context_mock)
    
    # Assert scroll_to bounded properly even on full_page=True
    assert mock_scroll_to.call_count == 1
    _, kwargs = mock_scroll_to.call_args
    assert kwargs.get("y") == 10000  # MAX_SCREENSHOT_HEIGHT
    assert "wait_callback" in kwargs

@pytest.mark.asyncio
async def test_missing_tab_handling():
    context_mock = AsyncMock()
    context_mock.page = AsyncMock()
    context_mock.page.is_closed = MagicMock(return_value=False)
    context_mock.request = Request.from_url("https://youtube.com/@test/featured", user_data={"slug": "videos"})
    context_mock.page.url = "https://youtube.com/@test/featured" # Wrong URL for videos
    
    await tab_handler(context_mock)
    
    # push_data should not be called because it aborted
    assert not context_mock.push_data.called
