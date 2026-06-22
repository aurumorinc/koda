import pytest
from unittest.mock import AsyncMock, patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import import_script

batch_scrape_script = import_script("f/koda/batch_scrape.py", "batch_scrape")

@pytest.mark.asyncio
@patch("batch_scrape.KodaClient")
async def test_batch_scrape_success(mock_client_class, wmill_mock):
    mock_client = AsyncMock()
    mock_client_class.return_value.__aenter__.return_value = mock_client
    
    from unittest.mock import MagicMock
    mock_response = MagicMock()
    mock_response.model_dump.return_value = {
        "success": True,
        "results": [{"url": "https://example.com", "success": True, "markdown": "Test"}]
    }
    mock_client.batch_scrape.return_value = mock_response

    result = await batch_scrape_script._run_batch_scrape(
        urls=["https://example.com"],
        formats=["markdown", {"type": "html"}],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource="test_s3",
        webhook=None,
        maxConcurrency=5,
        ignoreInvalidURLs=True
    )

    assert result["success"] is True
    assert "results" in result
    
    call_args = mock_client.batch_scrape.call_args[0][0]
    assert [str(u).rstrip("/") for u in call_args.urls] == ["https://example.com"]
    assert call_args.formats == ["markdown", "html"]
    assert call_args.max_concurrency == 5
    assert call_args.ignore_invalid_urls is True

@pytest.mark.asyncio
async def test_batch_scrape_invalid_s3(wmill_mock):
    result = await batch_scrape_script._run_batch_scrape(
        urls=["https://example.com"],
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource="invalid_s3",
        webhook=None,
        maxConcurrency=5,
        ignoreInvalidURLs=True
    )

    assert result["success"] is False
    assert "not found" in result["error"]

@pytest.mark.asyncio
@patch("batch_scrape.KodaClient")
async def test_batch_scrape_exception(mock_client_class, wmill_mock):
    mock_client_class.return_value.__aenter__.side_effect = Exception("Crash")
    
    result = await batch_scrape_script._run_batch_scrape(
        urls=["https://example.com"],
        formats=["markdown"],
        onlyMainContent=True,
        actions=[],
        timeout=60000,
        s3_resource=None,
        webhook=None,
        maxConcurrency=5,
        ignoreInvalidURLs=True
    )

    assert result["success"] is False
    assert "Crash" in result["error"]
