"""Tests for page extraction logic."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from koda.services.page_service import scrape, _execute_actions_hook
from koda.schemas.page_schema import ScrapeRequest, Action

@pytest.mark.asyncio
async def test_execute_actions_hook():
    actions = [
        Action(type="wait", milliseconds=1000),
        Action(type="click", selector="#btn"),
        Action(type="write", text="hello"),
        Action(type="press", key="Enter"),
        Action(type="scroll", direction="down"),
        Action(type="executeJavascript", script="return 1+1;"),
        Action(type="screenshot", fullPage=True),
        Action(type="pdf", format="A4"),
        Action(type="scrape")
    ]
    request = ScrapeRequest(url="https://example.com", actions=actions)
    
    mock_page = AsyncMock()
    mock_page.evaluate.return_value = 2
    mock_page.screenshot.return_value = b"fake_screenshot"
    mock_page.pdf.return_value = b"fake_pdf"
    mock_page.content.return_value = "<html></html>"
    mock_page.url = "https://example.com"
    
    kwargs = {"request": request, "shared_state": {}}
    
    await _execute_actions_hook(mock_page, None, **kwargs)
    
    # Verify actions were executed
    mock_page.click.assert_called_once_with("#btn")
    mock_page.keyboard.type.assert_called_once_with("hello")
    mock_page.keyboard.press.assert_called_once_with("Enter")
    assert mock_page.evaluate.call_count == 2 # scroll and executeJavascript
    mock_page.screenshot.assert_called_once_with(full_page=True, quality=None, type="png", clip=None)
    mock_page.pdf.assert_called_once_with(format="A4", landscape=False, scale=1.0)
    mock_page.content.assert_called_once()
    
    # Verify results were stored
    results = kwargs["shared_state"]["action_results"]
    assert len(results["screenshots"]) == 1
    assert len(results["pdfs"]) == 1
    assert len(results["javascriptReturns"]) == 1
    assert results["javascriptReturns"][0]["value"] == 2
    assert len(results["scrapes"]) == 1
    assert results["scrapes"][0]["html"] == "<html></html>"

@pytest.mark.asyncio
async def test_scrape_basic():
    request = ScrapeRequest(url="https://example.com", formats=["markdown", "html", "metadata"])
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.markdown = "# Hello"
    mock_result.html = "<h1>Hello</h1>"
    mock_result.metadata = {"title": "Test"}
    
    with patch("koda.services.page_service.AsyncWebCrawler") as mock_crawler_cls:
        mock_crawler = AsyncMock()
        mock_crawler_cls.return_value.__aenter__.return_value = mock_crawler
        mock_crawler.arun.return_value = mock_result
        
        response = await scrape(request)
        
        assert response.error is None
        assert response.markdown == "# Hello"
        assert response.html == "<h1>Hello</h1>"
        assert response.metadata == {"title": "Test"}
        assert response.screenshot is None

@pytest.mark.asyncio
async def test_scrape_with_screenshot():
    request = ScrapeRequest(url="https://example.com", formats=["screenshot"])
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.screenshot = "YmFzZTY0" # base64 for "base64"
    
    with patch("koda.services.page_service.AsyncWebCrawler") as mock_crawler_cls:
        mock_crawler = AsyncMock()
        mock_crawler_cls.return_value.__aenter__.return_value = mock_crawler
        mock_crawler.arun.return_value = mock_result
        
        response = await scrape(request)
        
        assert response.error is None
        assert getattr(response, "_screenshot_bytes") == b"base64"
