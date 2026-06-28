import pytest
from unittest.mock import AsyncMock, patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import import_script  # type: ignore

batch_scrape_script = import_script("f/koda/batch_scrape.py", "batch_scrape")


@patch.object(batch_scrape_script, "_run_batch_scrape")
def test_batch_scrape_success(mock_execute_job, wmill_mock):
    from unittest.mock import MagicMock
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.id = "test-id"
    mock_response.invalid_urls = []
    
    mock_res_item = MagicMock()
    del mock_res_item._screenshot_bytes
    mock_res_item.model_dump.return_value = {"url": "https://example.com", "success": True, "markdown": "Test"}
    mock_response.data = [mock_res_item]
    mock_response.model_dump.return_value = {"success": True, "id": "test-id", "data": [{"url": "https://example.com", "success": True, "markdown": "Test"}]}
    
    mock_execute_job.return_value = mock_response

    result =  batch_scrape_script.main(
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

    assert result["success"] is True, result.get("error")
    assert "data" in result
    
    call_args = mock_execute_job.call_args[0][0]
    assert [str(u).rstrip("/") for u in call_args.urls] == ["https://example.com"]
    assert call_args.formats == ["markdown", "html"]
    assert call_args.max_concurrency == 5
    assert call_args.ignore_invalid_urls is True


def test_batch_scrape_invalid_s3(wmill_mock):
    result =  batch_scrape_script.main(
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


@patch.object(batch_scrape_script, "_run_batch_scrape")
def test_batch_scrape_exception(mock_execute_job, wmill_mock):
    mock_execute_job.side_effect = Exception("Crash")
    
    result =  batch_scrape_script.main(
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
