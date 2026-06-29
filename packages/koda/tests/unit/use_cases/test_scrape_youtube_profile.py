import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from crawlee import Request
from crawlee.crawlers import PlaywrightCrawlingContext

from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest
from koda.use_cases.scrape_youtube_profile.service import scrape_youtube_profile, default_handler, _validate_redirect, videos_handler

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
        {"tab_name": "About", "url": "https://youtube.com/@test", "screenshot": "data:image/jpeg;base64,AABB"},
        {"tab_name": "Videos", "url": "https://youtube.com/@test/videos", "screenshot": "data:image/jpeg;base64,AACC"}
    ]
    dataset_mock.get_data.return_value = data_mock
    crawler_instance.get_dataset.return_value = dataset_mock

    req = ScrapeYoutubeProfileRequest(url="https://youtube.com/@test", formats=["screenshot"], tabs=["about", "videos"])
    res = await scrape_youtube_profile(req)
    
    assert res.success is True
    assert res.data is not None
    assert len(res.data) == 2
    assert res.data[0]["tab_name"] == "About"
    assert res.data[0]["screenshot"] == "data:image/jpeg;base64,AABB"
    assert res.data[1]["tab_name"] == "Videos"
    assert res.data[1]["screenshot"] == "data:image/jpeg;base64,AACC"

@pytest.mark.asyncio
async def test_default_handler_routing():
    context_mock = AsyncMock(spec=PlaywrightCrawlingContext)
    context_mock.page = AsyncMock()
    context_mock.page.url = "https://youtube.com/@testuser"
    context_mock.request = Request.from_url("https://youtube.com/@testuser", user_data={"tabs": ["videos", "store"]})
    
    await default_handler(context_mock)
    
    # Assert add_requests called multiple times (1 for ABOUT, 2 for TABS)
    assert context_mock.add_requests.call_count == 3
    
    # ABOUT
    about_call = context_mock.add_requests.call_args_list[0][0][0]
    assert about_call[0].label == "ABOUT"
    assert about_call[0].url == "https://youtube.com/@testuser"
    
    # VIDEOS
    videos_call = context_mock.add_requests.call_args_list[1][0][0]
    assert videos_call[0].label == "VIDEOS"
    assert videos_call[0].url == "https://youtube.com/@testuser/videos"

    # STORE
    store_call = context_mock.add_requests.call_args_list[2][0][0]
    assert store_call[0].label == "STORE"
    assert store_call[0].url == "https://youtube.com/@testuser/store"

@pytest.mark.asyncio
async def test_validate_redirect():
    page_mock = AsyncMock()
    
    # Valid redirect
    page_mock.url = "https://youtube.com/@test/videos"
    page_mock.locator.return_value.first.inner_text.return_value = "Videos"
    
    res = await _validate_redirect(page_mock, "videos")
    assert res is True
    
    # Invalid URL pattern
    page_mock.url = "https://youtube.com/@test/featured"
    res = await _validate_redirect(page_mock, "videos")
    assert res is False
    
    # Invalid selected tab
    page_mock.url = "https://youtube.com/@test/videos"
    page_mock.locator.return_value.first.inner_text.return_value = "Home"
    res = await _validate_redirect(page_mock, "videos")
    assert res is False
    
@pytest.mark.asyncio
async def test_missing_tab_handling():
    context_mock = AsyncMock(spec=PlaywrightCrawlingContext)
    context_mock.page = AsyncMock()
    context_mock.page.url = "https://youtube.com/@test/featured" # Wrong URL for videos
    
    await videos_handler(context_mock)
    
    # push_data should not be called because it aborted
    assert not context_mock.push_data.called
