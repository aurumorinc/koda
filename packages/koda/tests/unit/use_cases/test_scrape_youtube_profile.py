import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from crawlee import Request

from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest
from koda.use_cases.scrape_youtube_profile.service import (
    scrape_youtube_profile,
    _handler,
    _screenshot,
)


@pytest.fixture
def mock_crawlee():
    with patch(
        "koda.use_cases.scrape_youtube_profile.service.PlaywrightCrawler", autospec=True
    ) as mock:
        yield mock


@pytest.fixture
def mock_koda_client():
    with patch(
        "koda.use_cases.scrape_youtube_profile.service.KodaClient", autospec=True
    ) as mock:
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
        {
            "url": "https://youtube.com/@test#about",
            "screenshot_base64": "AABB",
            "screenshot_filename": "about.png",
        },
        {
            "url": "https://youtube.com/@test/videos",
            "screenshot_base64": "AACC",
            "screenshot_filename": "videos.png",
        },
    ]
    dataset_mock.get_data.return_value = data_mock
    crawler_instance.get_dataset.return_value = dataset_mock

    req = ScrapeYoutubeProfileRequest(
        url="https://youtube.com/@test",
        formats=["screenshot"],
        max_scroll_y=3072,
    )
    res = await scrape_youtube_profile(req)

    assert res.success is True
    assert res.data is not None
    assert len(res.data) == 2
    assert res.data[0]["url"] == "https://youtube.com/@test#about"
    assert res.data[1]["url"] == "https://youtube.com/@test/videos"


@pytest.mark.asyncio
@patch("koda.use_cases.scrape_youtube_profile.service._screenshot", autospec=True)
async def test_default_handler_routing(mock_screenshot):
    mock_screenshot.return_value = b"fake_bytes"
    context_mock = AsyncMock()
    context_mock.page = AsyncMock()
    context_mock.page.url = "https://youtube.com/@testuser"
    context_mock.request = Request.from_url("https://youtube.com/@testuser")

    # Mocking page.evaluate to simulate tabs found
    def evaluate_side_effect(script, *args):
        if "querySelectorAll" in str(script):
            return ["home", "videos"]
        return 0

    context_mock.page.evaluate.side_effect = evaluate_side_effect

    # Mock tab locator visibility
    tab_loc_mock = AsyncMock()
    tab_loc_mock.is_visible.return_value = True
    context_mock.page.locator.return_value.first = tab_loc_mock

    await _handler(context_mock)

    # push_data called for featured and videos tabs
    assert context_mock.push_data.call_count >= 2
    pushed_urls = [call[0][0]["url"] for call in context_mock.push_data.call_args_list]
    assert "https://youtube.com/@testuser/featured" in pushed_urls
    assert "https://youtube.com/@testuser/videos" in pushed_urls


@pytest.mark.asyncio
@patch("koda.use_cases.scrape_youtube_profile.service._screenshot", autospec=True)
async def test_default_handler_no_home_tab(mock_screenshot):
    mock_screenshot.return_value = b"fake_bytes"
    context_mock = AsyncMock()
    context_mock.page = AsyncMock()
    context_mock.page.url = "https://youtube.com/@testuser"
    context_mock.request = Request.from_url("https://youtube.com/@testuser")

    def evaluate_side_effect(script, *args):
        if "querySelectorAll" in str(script):
            return ["videos", "shorts"]
        return 0

    context_mock.page.evaluate.side_effect = evaluate_side_effect

    tab_loc_mock = AsyncMock()
    tab_loc_mock.is_visible.return_value = True
    context_mock.page.locator.return_value.first = tab_loc_mock

    await _handler(context_mock)

    # Ensure none of the pushed items have URL ending with 'featured'
    pushed_urls = [call[0][0]["url"] for call in context_mock.push_data.call_args_list]
    for url in pushed_urls:
        assert not url.endswith("/featured")


@pytest.mark.asyncio
async def test_screenshot_dynamic_viewport_bounds():
    page_mock = AsyncMock()
    page_mock.evaluate.return_value = 1200
    page_mock.screenshot.return_value = b"bytes_1200"

    res = await _screenshot(page_mock, max_height_limit=3072)

    assert res == b"bytes_1200"
    page_mock.set_viewport_size.assert_called_once_with({"width": 1366, "height": 1200})
