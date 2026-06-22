import pytest
from unittest.mock import AsyncMock, patch
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import import_script

crawl_script = import_script("f/koda/crawl.py", "crawl")

@pytest.mark.asyncio
@patch("crawl.KodaClient")
async def test_crawl_success(mock_client_class, wmill_mock):
    mock_client = AsyncMock()
    mock_client_class.return_value.__aenter__.return_value = mock_client
    
    from unittest.mock import MagicMock
    mock_response = MagicMock()
    mock_response.model_dump.return_value = {
        "success": True,
        "id": "crawl-123",
        "url": "https://example.com",
        "total_pages_crawled": 5
    }
    mock_client.crawl.return_value = mock_response

    result = await crawl_script._run_crawl(
        url="https://example.com",
        limit=10,
        maxDiscoveryDepth=2,
        allowExternalLinks=False,
        allowSubdomains=False,
        crawlEntireDomain=True,
        ignoreQueryParameters=True,
        regexOnFullURL=False,
        excludePaths=None,
        includePaths=None,
        maxConcurrency=5,
        delay=1.0,
        webhook=None,
        scrapeOptions={"formats": ["markdown"]}
    )

    assert result["success"] is True
    assert result["total_pages_crawled"] == 5
    
    call_args = mock_client.crawl.call_args[0][0]
    assert str(call_args.url) == "https://example.com/"
    assert call_args.limit == 10
    assert call_args.scrapeOptions.formats == ["markdown"]

@pytest.mark.asyncio
@patch("crawl.KodaClient")
async def test_crawl_exception(mock_client_class, wmill_mock):
    mock_client_class.return_value.__aenter__.side_effect = Exception("Crawl Error")
    
    result = await crawl_script._run_crawl(
        url="https://example.com",
        limit=10,
        maxDiscoveryDepth=2,
        allowExternalLinks=False,
        allowSubdomains=False,
        crawlEntireDomain=True,
        ignoreQueryParameters=True,
        regexOnFullURL=False,
        excludePaths=None,
        includePaths=None,
        maxConcurrency=5,
        delay=1.0,
        webhook=None,
        scrapeOptions=None
    )

    assert result["success"] is False
    assert "Crawl Error" in result["error"]
