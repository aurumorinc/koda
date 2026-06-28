import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest
from koda.use_cases.scrape_youtube_profile.service import scrape_youtube_profile

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
        {"tab_name": "About", "url": "https://youtube.com/@test/about", "markdown": "Description"},
        {"tab_name": "Videos", "url": "https://youtube.com/@test/videos", "links": ["video1", "video2"]}
    ]
    dataset_mock.get_data.return_value = data_mock
    crawler_instance.get_dataset.return_value = dataset_mock

    req = ScrapeYoutubeProfileRequest(url="https://youtube.com/@test", formats=["markdown", "links"])
    res = await scrape_youtube_profile(req)
    
    assert res.success is True
    assert res.data is not None
    assert len(res.data) == 2
    assert res.data[0]["tab_name"] == "About"
    assert res.data[0]["markdown"] == "Description"
    assert res.data[1]["tab_name"] == "Videos"
    assert res.data[1]["links"] == ["video1", "video2"]
