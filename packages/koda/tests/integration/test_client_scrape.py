import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

from koda.client import KodaClient
from koda.modules.page.schema import ScrapeRequest
from koda.modules.file.schema import S3Config
from koda.modules.webhook.schema import WebhookConfig

@pytest.mark.asyncio
@patch("koda.modules.page.service.Crawl4AiTool")
async def test_scrape_success_with_markdown(mock_tool_class):
    """Test successful scrape returning markdown."""
    mock_tool = AsyncMock()
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.markdown = "# Test Markdown"
    mock_tool.execute.return_value = mock_result
    mock_tool_class.return_value = mock_tool

    async with KodaClient() as client:
        request = ScrapeRequest(url="http://example.com", formats=["markdown"])
        response = await client.scrape(request)

        assert response.error is None
        assert response.markdown == "# Test Markdown"
        mock_tool.execute.assert_called_once()

@pytest.mark.asyncio
@patch("koda.modules.page.service.Crawl4AiTool")
async def test_scrape_timeout_handling(mock_tool_class):
    """Test scrape timeout handling."""
    mock_tool = AsyncMock()
    
    async def slow_execute(*args, **kwargs):
        await asyncio.sleep(0.2)
        return MagicMock(success=True)
        
    mock_tool.execute.side_effect = slow_execute
    mock_tool_class.return_value = mock_tool

    async with KodaClient() as client:
        # Set a very short timeout
        request = ScrapeRequest(url="http://example.com", timeout=100)
        response = await client.scrape(request)

        assert response.error is not None
        assert "timed out" in response.error

@pytest.mark.asyncio
@patch("koda.modules.page.service.Crawl4AiTool")
@patch("koda.modules.page.service.file.upload")
@patch("koda.modules.page.service.file.generate_presigned_url")
async def test_scrape_with_s3_upload(mock_generate_url, mock_upload, mock_tool_class):
    """Test scrape with S3 upload for screenshot."""
    mock_tool = AsyncMock()
    mock_result = MagicMock()
    mock_result.success = True
    # Base64 encoded "test"
    mock_result.screenshot = "dGVzdA=="
    mock_tool.execute.return_value = mock_result
    mock_tool_class.return_value = mock_tool
    
    mock_generate_url.return_value = "https://s3.example.com/screenshot.jpg"

    async with KodaClient() as client:
        s3_config = S3Config(
            endpoint="s3.example.com",
            bucket="test-bucket",
            access_key="key",
            secret_key="secret"
        )
        request = ScrapeRequest(
            url="http://example.com", 
            formats=["screenshot"],
            s3_config=s3_config
        )
        response = await client.scrape(request)

        assert response.error is None
        assert response.screenshot == "https://s3.example.com/screenshot.jpg"
        mock_upload.assert_called_once()
        mock_generate_url.assert_called_once()

@pytest.mark.asyncio
@patch("koda.modules.page.service.Crawl4AiTool")
@patch("koda.modules.page.service.dispatch_webhook")
async def test_scrape_webhook_dispatch(mock_dispatch, mock_tool_class):
    """Test scrape webhook dispatch."""
    mock_tool = AsyncMock()
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.markdown = "# Test"
    mock_tool.execute.return_value = mock_result
    mock_tool_class.return_value = mock_tool

    async with KodaClient() as client:
        webhook_config = WebhookConfig(url="http://webhook.example.com")
        request = ScrapeRequest(
            url="http://example.com", 
            formats=["markdown"],
            webhook=webhook_config
        )
        response = await client.scrape(request)

        assert response.error is None
        mock_dispatch.assert_called_once()
        args, kwargs = mock_dispatch.call_args
        assert args[0] == webhook_config
        assert args[1] == "scrape.completed"
        assert args[2]["success"] is True
        assert args[2]["data"]["markdown"] == "# Test"
