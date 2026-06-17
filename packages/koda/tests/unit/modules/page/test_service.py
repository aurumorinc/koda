"""Tests for page extraction logic."""

import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from koda.modules.page.service import ScrapeJob, scrape
from koda.modules.page.schema import ScrapeRequest, Action
from koda.modules.webhook.schema import WebhookConfig

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
    
    job = ScrapeJob(request)
    await job.execute_actions_hook(mock_page, None)
    
    # Verify actions were executed
    mock_page.click.assert_called_once_with("#btn")
    mock_page.keyboard.type.assert_called_once_with("hello")
    mock_page.keyboard.press.assert_called_once_with("Enter")
    assert mock_page.evaluate.call_count == 2 # scroll and executeJavascript
    mock_page.screenshot.assert_called_once_with(full_page=True, quality=None, type="png", clip=None)
    mock_page.pdf.assert_called_once_with(format="A4", landscape=False, scale=1.0)
    mock_page.content.assert_called_once()
    
    # Verify results were stored
    results = job.action_results
    assert len(results["screenshots"]) == 1
    assert len(results["pdfs"]) == 1
    assert len(results["javascriptReturns"]) == 1
    assert results["javascriptReturns"][0]["value"] == 2
    assert len(results["scrapes"]) == 1
    assert results["scrapes"][0]["html"] == "<html></html>"

@pytest.mark.asyncio
async def test_scrape_job_basic():
    request = ScrapeRequest(url="https://example.com", formats=["markdown", "html", "metadata"])
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.markdown = "# Hello"
    mock_result.html = "<h1>Hello</h1>"
    mock_result.metadata = {"title": "Test"}
    
    with patch("koda.modules.page.service.Crawl4AiTool") as mock_tool_cls:
        mock_tool = MagicMock()
        mock_tool.execute = AsyncMock(return_value=mock_result)
        mock_tool_cls.return_value = mock_tool
        
        job = ScrapeJob(request)
        response = await job.run()
        
        assert response.error is None
        assert response.markdown == "# Hello"
        assert response.html == "<h1>Hello</h1>"
        assert response.metadata == {"title": "Test"}
        assert response.screenshot is None

@pytest.mark.asyncio
async def test_scrape_job_with_screenshot():
    request = ScrapeRequest(url="https://example.com", formats=["screenshot"])
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.screenshot = "YmFzZTY0" # base64 for "base64"
    
    with patch("koda.modules.page.service.Crawl4AiTool") as mock_tool_cls:
        mock_tool = MagicMock()
        mock_tool.execute = AsyncMock(return_value=mock_result)
        mock_tool_cls.return_value = mock_tool
        
        job = ScrapeJob(request)
        response = await job.run()
        
        assert response.error is None
        assert getattr(response, "_screenshot_bytes") == b"base64"

@pytest.mark.asyncio
@patch("koda.modules.page.service.file.upload")
@patch("koda.modules.page.service.file.generate_presigned_url")
@patch("koda.modules.page.service._execute_scrape_job")
async def test_scrape_orchestration_local_file(mock_execute, mock_presign, mock_upload):
    """Test scraping a local HTML file with S3 upload."""
    mock_presign.return_value = "https://mock-s3-url.com/image.jpg"
    
    mock_response = MagicMock()
    mock_response.url = "file:///tmp/dummy.html"
    mock_response.markdown = "# Test Content"
    mock_response.metadata = {"title": "Dummy Page"}
    mock_response.html = None
    mock_response.links = None
    mock_response.images = None
    mock_response.screenshot = None
    setattr(mock_response, "_screenshot_bytes", b"fake_bytes")
    mock_execute.return_value = mock_response
    
    request = ScrapeRequest(
        url="file:///tmp/dummy.html",
        formats=["markdown", "metadata", "screenshot"],
        only_main_content=True,
        s3_config={"bucket": "test"}
    )
    response = await scrape(request)
    
    assert response.screenshot == "https://mock-s3-url.com/image.jpg"
    mock_upload.assert_called_once()

@pytest.mark.asyncio
@patch("koda.modules.page.service.dispatch_webhook")
@patch("koda.modules.page.service._execute_scrape_job")
async def test_scrape_orchestration_with_webhook(mock_execute, mock_dispatch_webhook):
    """Test scraping with a webhook callback."""
    webhook_cfg = WebhookConfig(
        url="http://test-webhook.com/callback",
        metadata={"user_id": 123}
    )
    
    mock_response = MagicMock()
    mock_response.url = "http://example.com"
    mock_response.markdown = "# Test Content"
    mock_response.html = None
    mock_response.links = None
    mock_response.images = None
    mock_response.metadata = None
    mock_response.screenshot = None
    mock_execute.return_value = mock_response
    
    request = ScrapeRequest(
        url="http://example.com",
        formats=["markdown"],
        webhook=webhook_cfg
    )
    response = await scrape(request)
    
    mock_dispatch_webhook.assert_called_once()
    
    # Verify the webhook handle call
    args = mock_dispatch_webhook.call_args[0]
    assert args[0].url == "http://test-webhook.com/callback"
    assert args[1] == "scrape.completed"
    assert args[2]["data"]["markdown"] == "# Test Content"

@pytest.mark.asyncio
@patch("koda.modules.page.service.dispatch_webhook")
@patch("koda.modules.page.service._execute_scrape_job")
async def test_scrape_orchestration_timeout(mock_execute, mock_dispatch_webhook):
    """Test that the timeout correctly aborts a long-running scrape."""
    
    async def slow_scrape(*args, **kwargs):
        await asyncio.sleep(0.5)
        return MagicMock()
        
    mock_execute.side_effect = slow_scrape
    
    webhook_cfg = WebhookConfig(url="http://test-webhook.com/callback")
    
    request = ScrapeRequest(
        url="http://example.com",
        formats=["markdown"],
        webhook=webhook_cfg,
        timeout=100 # Set a very short timeout (100ms)
    )
    response = await scrape(request)
    
    # Verify the response contains a timeout error
    assert response.error is not None
    assert "timed out after 100ms" in response.error
    
    # Verify the failure webhook was dispatched
    mock_dispatch_webhook.assert_called_once()
    args = mock_dispatch_webhook.call_args[0]
    assert args[0].url == "http://test-webhook.com/callback"
    assert args[1] == "scrape.failed"
    assert args[2]["success"] is False
    assert "timed out after 100ms" in args[2]["error"]
