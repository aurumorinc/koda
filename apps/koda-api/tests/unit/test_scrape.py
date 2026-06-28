import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import import_script  # type: ignore

scrape_script = import_script("f/koda/scrape.py", "scrape")



@pytest.mark.asyncio
@patch.object(scrape_script, "scrape")
async def test_scrape_success(mock_run_scrape, wmill_mock):
    # Setup mock response
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.data = {"markdown": "Test Content", "html": "<p>Test Content</p>"}
    mock_result.model_dump.return_value = {"success": True, "data": {"markdown": "Test Content", "html": "<p>Test Content</p>"}}
    mock_run_scrape.return_value = mock_result

    result = await scrape_script.main(
        url="https://example.com",
        formats=["markdown", "html"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource=None,
        webhook=None
    )

    assert result["success"] is True
    assert result["data"]["markdown"] == "Test Content"
    assert result["data"]["html"] == "<p>Test Content</p>"
    
    # Verify request payload creation
    request_obj = mock_run_scrape.call_args[0][0]
    assert request_obj.url == "https://example.com"
    assert request_obj.formats == ["markdown", "html"]


@pytest.mark.asyncio
@patch.object(scrape_script, "scrape")
async def test_scrape_client_error(mock_run_scrape, wmill_mock):
    mock_result = MagicMock()
    mock_result.success = False
    mock_result.error = "404 Not Found"
    mock_result.model_dump.return_value = {"success": False, "error": "404 Not Found"}
    mock_run_scrape.return_value = mock_result

    result = await scrape_script.main(
        url="https://example.com/404",
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource=None,
        webhook=None
    )

    assert result["success"] is False
    assert result["error"] == "404 Not Found"


@pytest.mark.asyncio
async def test_scrape_invalid_s3_resource(wmill_mock):
    # Pass an s3_resource that doesn't exist
    result = await scrape_script.main(
        url="https://example.com",
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource="invalid_s3",
        webhook=None
    )

    assert result["success"] is False
    assert "not found" in result["error"]


@pytest.mark.asyncio
@patch.object(scrape_script, "scrape")
async def test_scrape_exception(mock_run_scrape, wmill_mock):
    mock_run_scrape.side_effect = Exception("System Crash")

    result = await scrape_script.main(
        url="https://example.com",
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource=None,
        webhook=None
    )

    assert result["success"] is False
    assert "Crash" in result["error"]
