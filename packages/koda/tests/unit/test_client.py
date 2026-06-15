"""Integration tests for KodaClient."""

import pytest
import asyncio
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock, AsyncMock

from koda.client import KodaClient
from koda.modules.page.schema import ScrapeRequest, Action, ScrapeResponse
from koda.modules.webhook.schema import WebhookConfig

@pytest.mark.asyncio
@patch("koda.client.file.upload")
@patch("koda.client.file.generate_presigned_url")
@patch("koda.client.page.scrape")
async def test_kodaclient_scrape_local_file(mock_scrape, mock_presign, mock_upload):
    """Test scraping a local HTML file."""
    mock_presign.return_value = "https://mock-s3-url.com/image.jpg"
    
    mock_response = ScrapeResponse(
        url="file:///tmp/dummy.html",
        markdown="# Test Content",
        metadata={"title": "Dummy Page"}
    )
    setattr(mock_response, "_screenshot_bytes", b"fake_bytes")
    mock_scrape.return_value = mock_response
    
    async with KodaClient() as client:
        request = ScrapeRequest(
            url="file:///tmp/dummy.html",
            formats=["markdown", "metadata", "screenshot"],
            only_main_content=True,
            s3_config={"bucket": "test"}
        )
        response = await client.scrape(request)
        
        assert response.error is None
        assert response.metadata is not None
        assert response.metadata.get("title") == "Dummy Page"
        
        assert response.markdown is not None
        assert "Test Content" in response.markdown
        
        assert response.screenshot == "https://mock-s3-url.com/image.jpg"
        mock_upload.assert_called_once()

@pytest.mark.asyncio
@patch("koda.client.dispatch_webhook")
@patch("koda.client.page.scrape")
async def test_kodaclient_with_webhook(mock_scrape, mock_dispatch_webhook):
    """Test scraping with a webhook callback."""
    webhook_cfg = WebhookConfig(
        url="http://test-webhook.com/callback",
        metadata={"user_id": 123}
    )
    
    mock_response = ScrapeResponse(
        url="http://example.com",
        markdown="# Test Content"
    )
    mock_scrape.return_value = mock_response
    
    async with KodaClient() as client:
        request = ScrapeRequest(
            url="http://example.com",
            formats=["markdown"],
            webhook=webhook_cfg
        )
        response = await client.scrape(request)
        
        assert response.error is None
        mock_dispatch_webhook.assert_called_once()
        
        # Verify the webhook handle call
        args = mock_dispatch_webhook.call_args[0]
        assert args[0].url == "http://test-webhook.com/callback"
        assert args[1] == "scrape.completed"
        assert args[2]["data"]["markdown"] == "# Test Content"

@pytest.mark.asyncio
@patch("koda.client.dispatch_webhook")
@patch("koda.client.page.scrape")
async def test_kodaclient_scrape_timeout(mock_scrape, mock_dispatch_webhook):
    """Test that the client-level timeout correctly aborts a long-running scrape."""
    
    async def slow_scrape(*args, **kwargs):
        await asyncio.sleep(0.5)
        return ScrapeResponse(url="http://example.com", markdown="Too late")
        
    mock_scrape.side_effect = slow_scrape
    
    webhook_cfg = WebhookConfig(url="http://test-webhook.com/callback")
    
    # Set a very short timeout (100ms)
    async with KodaClient(timeout=100) as client:
        request = ScrapeRequest(
            url="http://example.com",
            formats=["markdown"],
            webhook=webhook_cfg
        )
        response = await client.scrape(request)
        
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
