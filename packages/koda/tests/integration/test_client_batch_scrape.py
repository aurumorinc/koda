import pytest
from typing import Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch

from koda import KodaClient
from koda.modules.page.schema import BatchScrapeRequest, ScrapeResponse

@pytest.mark.asyncio
@patch("koda.modules.page.service.BrowserSession")
@patch("koda.modules.page.service.Crawl4AiTool")
async def test_client_batch_scrape(mock_tool_class, mock_browser_session):
    """Test batch scraping multiple URLs concurrently."""
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    mock_tool = AsyncMock()
    mock_results = [
        MagicMock(url="https://example.com", success=True, markdown="# Example 1"),
        MagicMock(url="https://example.org", success=True, markdown="# Example 2"),
        MagicMock(url="https://example.net", success=True, markdown="# Example 3"),
    ]
    # Set up some attributes that might be checked
    for res in mock_results:
        res.metadata = {}
        res.html = "<html></html>"
        res.links = {}
        res.media = {}
        res.screenshot = None
        res.redirected_url = res.url
    
    mock_tool.execute.return_value = mock_results
    mock_tool_class.return_value = mock_tool
    
    mock_context = AsyncMock()
    mock_browser_session.return_value.__aenter__.return_value = mock_context

    async with KodaClient() as client:
        request = BatchScrapeRequest(
            urls=urls,
            formats=["markdown"],
            onlyMainContent=True
        )
        response = await client.batch_scrape(request)
        
        assert response.success is True
        assert response.id is not None
        assert response.results is not None
        assert len(response.results) == 3
        
        # Verify that all results contain markdown
        for res in response.results:
            assert isinstance(res, ScrapeResponse)
            assert res.url in urls
            assert res.markdown is not None
            assert len(res.markdown) > 0
            
@pytest.mark.asyncio
@patch("koda.modules.page.service.BrowserSession")
@patch("koda.modules.page.service.Crawl4AiTool")
async def test_client_batch_scrape_invalid_urls(mock_tool_class, mock_browser_session):
    """Test batch scraping with an invalid URL mixed in."""
    urls = [
        "https://example.com",
        "not_a_valid_url://test",
    ]
    
    mock_tool = AsyncMock()
    res1 = MagicMock(url="https://example.com", success=True, markdown="# Example 1")
    res1.metadata = {}
    res1.html = "<html></html>"
    res1.links = {}
    res1.media = {}
    res1.screenshot = None
    res1.redirected_url = res1.url

    mock_tool.execute.return_value = [res1]
    mock_tool_class.return_value = mock_tool
    
    mock_context = AsyncMock()
    mock_browser_session.return_value.__aenter__.return_value = mock_context

    async with KodaClient() as client:
        request = BatchScrapeRequest(
            urls=urls,
            formats=["markdown"],
            onlyMainContent=True,
            ignoreInvalidURLs=True
        )
        response = await client.batch_scrape(request)
        
        assert response.success is True
        assert len(response.invalid_urls) == 1
        assert "not_a_valid_url://test" in response.invalid_urls
        assert len(response.results) == 1
        assert response.results[0].url == "https://example.com"
