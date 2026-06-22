import pytest
from unittest.mock import AsyncMock, patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import import_script

# Import the script
scrape_script = import_script("f/koda/scrape.py", "scrape")

@pytest.mark.asyncio
@patch("scrape.KodaClient")
async def test_scrape_success(mock_client_class, wmill_mock):
    mock_client = AsyncMock()
    mock_client_class.return_value.__aenter__.return_value = mock_client
    
    # Mock successful response
    from unittest.mock import MagicMock
    mock_response = MagicMock()
    mock_response.error = None
    mock_response.markdown = "# Success"
    mock_response.html = "<html>Success</html>"
    mock_response.links = {"internal": [{"href": "/test"}]}
    mock_response.images = None
    mock_response.metadata = {"title": "Test"}
    mock_response.screenshot = "data:image/jpeg;base64,123"
    mock_response.action_results = None
    
    mock_client.scrape.return_value = mock_response

    result = await scrape_script._run_scrape(
        url="https://example.com",
        formats=["markdown", {"type": "html"}, "links", "screenshot"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource="test_s3",
        webhook=None
    )

    assert result["success"] is True
    assert "data" in result
    assert result["data"]["markdown"] == "# Success"
    assert result["data"]["html"] == "<html>Success</html>"
    assert result["data"]["links"] == {"internal": [{"href": "/test"}]}
    assert result["data"]["screenshot"] == "data:image/jpeg;base64,123"
    
    # Verify formats normalization
    call_args = mock_client.scrape.call_args[0][0]
    assert call_args.formats == ["markdown", "html", "links", "screenshot"]
    assert call_args.s3_config is not None
    assert call_args.s3_config.bucket == "test-bucket"

@pytest.mark.asyncio
@patch("scrape.KodaClient")
async def test_scrape_client_error(mock_client_class, wmill_mock):
    mock_client = AsyncMock()
    mock_client_class.return_value.__aenter__.return_value = mock_client
    
    # Mock error response
    from unittest.mock import MagicMock
    mock_response = MagicMock()
    mock_response.error = "Timeout occurred"
    mock_client.scrape.return_value = mock_response

    result = await scrape_script._run_scrape(
        url="https://example.com",
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource=None,
        webhook=None
    )

    assert result["success"] is False
    assert result["error"] == "Timeout occurred"

@pytest.mark.asyncio
async def test_scrape_invalid_s3_resource(wmill_mock):
    # Pass an s3_resource that doesn't exist
    result = await scrape_script._run_scrape(
        url="https://example.com",
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource="invalid_s3",
        webhook=None
    )

    assert result["success"] is False
    assert "S3 Resource 'invalid_s3' not found" in result["error"]

@pytest.mark.asyncio
@patch("scrape.KodaClient")
async def test_scrape_exception(mock_client_class, wmill_mock):
    mock_client_class.return_value.__aenter__.side_effect = Exception("Unexpected connection error")
    
    result = await scrape_script._run_scrape(
        url="https://example.com",
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource=None,
        webhook=None
    )

    assert result["success"] is False
    assert "Unexpected connection error" in result["error"]
