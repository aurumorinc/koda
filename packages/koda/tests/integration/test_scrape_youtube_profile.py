import pytest
from unittest.mock import AsyncMock, patch, MagicMock

import sys
import os
import importlib.util

# Mock wmill before loading
class MockWmill:
    @staticmethod
    def get_resource(res):
        return {
            "bucket": "test-bucket",
            "accessKey": "test-key",
            "secretKey": "test-secret",
            "endPoint": "https://s3.test",
            "region": "us-east-1"
        }

sys.modules["wmill"] = MagicMock()
sys.modules["wmill"].get_resource = MockWmill.get_resource

script_path = os.path.join(os.path.dirname(__file__), "../../../../apps/koda-api/f/koda/scouts/scrape_youtube_profile.py")
spec = importlib.util.spec_from_file_location("scrape_youtube_profile", script_path)
yp = importlib.util.module_from_spec(spec)
sys.modules["scrape_youtube_profile"] = yp
spec.loader.exec_module(yp)

_run_youtube_scrape = yp._run_youtube_scrape

@pytest.mark.asyncio
@patch("scrape_youtube_profile.PlaywrightCrawler")
@patch("scrape_youtube_profile.KodaClient")
async def test_youtube_orchestrator_success(mock_client_class, mock_crawler_class):
    mock_client = AsyncMock()
    mock_client_class.return_value.__aenter__.return_value = mock_client
    
    mock_crawler_instance = AsyncMock()
    mock_crawler_class.return_value = mock_crawler_instance
    
    mock_dataset = AsyncMock()
    mock_data = MagicMock()
    mock_data.items = [
        {"tab_name": "Home", "url": "https://www.youtube.com/@youtube", "markdown": "Home Page Markdown", "html": "<html>Home</html>", "links": ["test1"], "screenshot": "data:image/jpeg;base64,home_b64"},
        {"tab_name": "About", "url": "https://www.youtube.com/@youtube?about=1", "markdown": "About Markdown", "html": "<html>About</html>", "links": ["test_about"], "screenshot": "data:image/jpeg;base64,about_b64"},
        {"tab_name": "Videos", "url": "https://www.youtube.com/@youtube/videos", "markdown": "Videos Markdown", "html": "<html>Videos</html>", "links": ["test2"], "screenshot": "data:image/jpeg;base64,videos_b64"},
    ]
    mock_dataset.get_data.return_value = mock_data
    mock_crawler_instance.get_dataset.return_value = mock_dataset

    result = await _run_youtube_scrape(
        url="https://www.youtube.com/@youtube",
        formats=["markdown", "links", "screenshot"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource="test_s3",
        webhook={"url": "https://webhook.test"},
        tabs=["videos"]
    )

    assert result["success"] is True
    assert "data" in result
    assert "markdown" in result["data"]
    assert "links" in result["data"]
    assert "screenshots" in result["data"]

    assert "Home Page Markdown" in result["data"]["markdown"]
    assert "Videos Markdown" in result["data"]["markdown"]
    assert "About Markdown" in result["data"]["markdown"]

    assert result["data"]["links"]["Home"] == ["test1"]
    assert result["data"]["links"]["Videos"] == ["test2"]
    assert result["data"]["links"]["About"] == ["test_about"]

    assert result["data"]["screenshots"]["Home"] == "data:image/jpeg;base64,home_b64"
    assert result["data"]["screenshots"]["About"] == "data:image/jpeg;base64,about_b64"

    # Assert that the settings were updated
    from koda.config.main import settings
    assert settings.s3_bucket_name == "test-bucket"
    assert settings.webhook_url == "https://webhook.test"
    
@pytest.mark.asyncio
@patch("scrape_youtube_profile.PlaywrightCrawler")
@patch("scrape_youtube_profile.KodaClient")
async def test_youtube_orchestrator_redirect(mock_client_class, mock_crawler_class):
    mock_client = AsyncMock()
    mock_client_class.return_value.__aenter__.return_value = mock_client
    
    mock_crawler_instance = AsyncMock()
    mock_crawler_class.return_value = mock_crawler_instance
    
    mock_dataset = AsyncMock()
    mock_data = MagicMock()
    mock_data.items = [
        {"tab_name": "Home", "url": "https://www.youtube.com/@mkbhd", "markdown": "Home Markdown"}
    ]
    mock_dataset.get_data.return_value = mock_data
    mock_crawler_instance.get_dataset.return_value = mock_dataset

    result = await _run_youtube_scrape(
        url="https://crm.link/123",
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource=None,
        webhook=None,
        tabs=[]
    )

    assert result["success"] is True

    # Ensure crawler was initialized
    mock_crawler_class.assert_called_once()
    
    # Ensure crawler.run was called with the initial request
    run_calls = mock_crawler_instance.run.call_args_list
    assert len(run_calls) == 1
    requests = run_calls[0][0][0]
    assert len(requests) == 1
    assert requests[0]["url"] == "https://crm.link/123"

@pytest.mark.asyncio
@patch("scrape_youtube_profile.PlaywrightCrawler")
@patch("scrape_youtube_profile.KodaClient")
async def test_youtube_orchestrator_invalid_handle(mock_client_class, mock_crawler_class):
    mock_client = AsyncMock()
    mock_client_class.return_value.__aenter__.return_value = mock_client
    
    mock_crawler_instance = AsyncMock()
    mock_crawler_class.return_value = mock_crawler_instance
    
    mock_dataset = AsyncMock()
    mock_data = MagicMock()
    mock_data.items = [
        {"tab_name": "Home", "url": "https://www.youtube.com/404", "markdown": "Error: 404 Not Found"}
    ]
    mock_dataset.get_data.return_value = mock_data
    mock_crawler_instance.get_dataset.return_value = mock_dataset

    result = await _run_youtube_scrape(
        url="https://youtube.com/404",
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource=None,
        webhook=None,
        tabs=[]
    )

    assert result["success"] is True
    assert "Error: 404 Not Found" in result["data"]["markdown"]
