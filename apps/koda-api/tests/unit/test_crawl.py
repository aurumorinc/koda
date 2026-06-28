import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import import_script  # type: ignore

crawl_script = import_script("f/koda/crawl.py", "crawl")



@pytest.mark.asyncio
@patch.object(crawl_script, "crawl")
async def test_crawl_success(mock_execute_job, wmill_mock):
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.id = "test-id"
    mock_response.url = "https://example.com"
    mock_response.total_pages_crawled = 5
    mock_response.model_dump.return_value = {"success": True, "id": "test-id", "url": "https://example.com", "total_pages_crawled": 5}
    
    mock_execute_job.return_value = mock_response

    result = await crawl_script.main(
        url="https://example.com",
        prompt=None,
        excludePaths=["/exclude/*"],
        includePaths=["/include/*"],
        maxDiscoveryDepth=2,
        sitemap="include",
        ignoreQueryParameters=True,
        regexOnFullURL=False,
        limit=10,
        crawlEntireDomain=False,
        allowExternalLinks=False,
        allowSubdomains=False,
        ignoreRobotsTxt=False,
        robotsUserAgent="test-bot",
        delay=0.5,
        maxConcurrency=5,
        webhook=None,
        scrapeOptions={"formats": ["markdown", "html"]},
        zeroDataRetention=False
    )

    assert result["success"] is True
    assert result["total_pages_crawled"] == 5
    
    call_args = mock_execute_job.call_args[0][0]
    assert call_args.url == "https://example.com"
    assert call_args.limit == 10
    assert call_args.delay == 0.5
    assert call_args.scrapeOptions.formats == ["markdown", "html"]



@pytest.mark.asyncio
@patch.object(crawl_script, "crawl")
async def test_crawl_exception(mock_execute_job, wmill_mock):
    mock_execute_job.side_effect = Exception("System Crash")

    result = await crawl_script.main(
        url="https://example.com",
        prompt=None,
        excludePaths=None,
        includePaths=None,
        maxDiscoveryDepth=1,
        sitemap="include",
        ignoreQueryParameters=False,
        regexOnFullURL=False,
        limit=10,
        crawlEntireDomain=False,
        allowExternalLinks=False,
        allowSubdomains=False,
        ignoreRobotsTxt=False,
        robotsUserAgent=None,
        delay=None,
        maxConcurrency=5,
        webhook=None,
        scrapeOptions={},
        zeroDataRetention=False
    )

    assert result["success"] is False
    assert "Crash" in result["error"]
