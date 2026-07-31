import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from crawlee import Request

from f.koda.scouts.scrape_youtube_profile import (
    ScrapeYoutubeProfileRequest,
    ScrapeYoutubeProfileResponse,
    amain,
    main,
    _handler,
)


@pytest.fixture
def mock_crawlee():
    with patch(
        "f.koda.scouts.scrape_youtube_profile.PlaywrightCrawler", autospec=True
    ) as mock:
        yield mock


@pytest.fixture
def mock_koda_client():
    with patch(
        "f.koda.scouts.scrape_youtube_profile.KodaClient", autospec=True
    ) as mock:
        yield mock


def test_scrape_youtube_profile_request_defaults():
    req = ScrapeYoutubeProfileRequest(url="https://youtube.com/@test")
    assert req.viewport == {"width": 1366, "height": 768}
    assert req.max_scroll_y == 3072
    assert req.max_screenshot_height == 10000


@pytest.mark.asyncio
async def test_scrape_youtube_profile_amain_success(mock_crawlee, mock_koda_client):
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
    )
    res = await amain(req)

    assert res.success is True
    assert res.data is not None
    assert len(res.data) == 2
    assert res.data[0]["url"] == "https://youtube.com/@test#about"
    assert res.data[1]["url"] == "https://youtube.com/@test/videos"


@pytest.mark.asyncio
async def test_scrape_youtube_profile_amain_empty_dataset_returns_failure(
    mock_crawlee, mock_koda_client
):
    client_instance = AsyncMock()
    mock_koda_client.return_value.__aenter__.return_value = client_instance

    crawler_instance = AsyncMock()
    mock_crawlee.return_value = crawler_instance

    # Mock empty crawler dataset (simulating timeout / no items extracted)
    dataset_mock = AsyncMock()
    data_mock = MagicMock()
    data_mock.items = []
    dataset_mock.get_data.return_value = data_mock
    crawler_instance.get_dataset.return_value = dataset_mock

    req = ScrapeYoutubeProfileRequest(url="https://youtube.com/@test")
    res = await amain(req)

    assert res.success is False
    assert "failed or timed out" in res.error.lower()


@patch("f.koda.scouts.scrape_youtube_profile.amain", autospec=True)
def test_scrape_youtube_profile_main_raises_runtime_error_on_failure(mock_amain):
    mock_amain.return_value = ScrapeYoutubeProfileResponse(
        success=False, error="Scrape operation timed out"
    )

    with pytest.raises(RuntimeError) as exc_info:
        main(url="https://youtube.com/@test")

    assert "Scrape operation timed out" in str(exc_info.value)


@patch("f.koda.scouts.scrape_youtube_profile.amain", autospec=True)
def test_scrape_youtube_profile_main_returns_unwrapped_data_on_success(mock_amain):
    mock_amain.return_value = ScrapeYoutubeProfileResponse(
        success=True,
        data=[
            {"url": "https://youtube.com/@test/featured", "screenshot": "https://s3.url/1.png"},
            {"url": "https://youtube.com/@test/videos", "screenshot": "https://s3.url/2.png"},
        ],
    )

    res = main(url="https://youtube.com/@test")

    assert isinstance(res, list)
    assert len(res) == 2
    assert res[0]["url"] == "https://youtube.com/@test/featured"


@pytest.mark.asyncio
@patch("f.koda.scouts.scrape_youtube_profile.screenshot", autospec=True)
async def test_default_handler_routing(mock_screenshot):
    mock_screenshot.return_value = b"fake_bytes"
    context_mock = AsyncMock()
    context_mock.page = AsyncMock()
    context_mock.page.url = "https://youtube.com/@testuser"
    context_mock.request = Request.from_url("https://youtube.com/@testuser")

    def evaluate_side_effect(script, *args):
        if "querySelectorAll" in str(script):
            return ["home", "videos"]
        return 0

    context_mock.page.evaluate.side_effect = evaluate_side_effect

    tab_loc_mock = AsyncMock()
    tab_loc_mock.is_visible.return_value = True
    context_mock.page.locator.return_value.first = tab_loc_mock

    req = ScrapeYoutubeProfileRequest(url="https://youtube.com/@testuser")
    await _handler(context_mock, req)

    # push_data called for featured and videos tabs
    assert context_mock.push_data.call_count >= 2
    pushed_urls = [call[0][0]["url"] for call in context_mock.push_data.call_args_list]
    assert "https://youtube.com/@testuser/featured" in pushed_urls
    assert "https://youtube.com/@testuser/videos" in pushed_urls
