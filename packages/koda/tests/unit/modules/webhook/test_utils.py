import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from koda.modules.webhook.utils import dispatch_webhook
from koda.modules.webhook.schema import WebhookConfig

@pytest.mark.asyncio
async def test_dispatch_webhook_success():
    config = WebhookConfig(url="https://example.com/webhook", events=["crawl.started"])
    payload = {"url": "https://test.com"}
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        from unittest.mock import MagicMock
        mock_post.return_value.raise_for_status = MagicMock()
        
        await dispatch_webhook(config, "crawl.started", payload)
        
        # Wait a tiny bit for the background task to execute
        await asyncio.sleep(0.01)
        
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "https://example.com/webhook"
        assert kwargs["json"]["type"] == "crawl.started"
        assert kwargs["json"]["url"] == "https://test.com"

@pytest.mark.asyncio
async def test_dispatch_webhook_filtered_event():
    config = WebhookConfig(url="https://example.com/webhook", events=["crawl.completed"])
    payload = {"url": "https://test.com"}
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        await dispatch_webhook(config, "crawl.started", payload)
        
        await asyncio.sleep(0.01)
        
        mock_post.assert_not_called()

@pytest.mark.asyncio
async def test_dispatch_webhook_with_metadata():
    config = WebhookConfig(
        url="https://example.com/webhook", 
        metadata={"custom_id": "123"}
    )
    payload = {"url": "https://test.com"}
    
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        from unittest.mock import MagicMock
        mock_post.return_value.raise_for_status = MagicMock()
        
        await dispatch_webhook(config, "crawl.started", payload)
        
        await asyncio.sleep(0.01)
        
        mock_post.assert_called_once()
        assert mock_post.call_args[1]["json"]["custom_id"] == "123"
