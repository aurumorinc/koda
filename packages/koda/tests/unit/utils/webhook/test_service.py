import pytest
import httpx
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

from koda.utils.webhook.schema import Webhook, WebhookEvent
from koda.utils.webhook.service import dispatch_webhook, webhook_dispatch


@pytest.fixture
def webhook():
    return Webhook(
        url="https://example.com/webhook",
        headers={"Authorization": "Bearer token"},
        metadata={"user_id": "123"},
        events=[WebhookEvent.STARTED, WebhookEvent.COMPLETED],
    )


@pytest.mark.asyncio
async def test_dispatch_webhook_success(webhook):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        payload = {"data": "test"}
        await dispatch_webhook(webhook, WebhookEvent.STARTED, payload)
        
        await asyncio.sleep(0.01)

        mock_post.assert_called_once_with(
            "https://example.com/webhook",
            json={
                "event": "started",
                "payload": payload,
                "metadata": {"user_id": "123"},
            },
            headers={"Authorization": "Bearer token"},
        )
        mock_response.raise_for_status.assert_called_once()


@pytest.mark.asyncio
async def test_dispatch_webhook_no_webhook():
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        await dispatch_webhook(None, WebhookEvent.STARTED, {"data": "test"})
        await asyncio.sleep(0.01)
        mock_post.assert_not_called()


@pytest.mark.asyncio
async def test_dispatch_webhook_event_not_in_list(webhook):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        await dispatch_webhook(webhook, WebhookEvent.FAILED, {"data": "test"})
        await asyncio.sleep(0.01)
        mock_post.assert_not_called()


@pytest.mark.asyncio
async def test_dispatch_webhook_http_error(webhook, caplog):
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock()
        )
        mock_post.return_value = mock_response

        await dispatch_webhook(webhook, WebhookEvent.STARTED, {"data": "test"})
        await asyncio.sleep(0.01)

        assert "Failed to trigger webhook for event %s: %s" in caplog.text


# tests for webhook_dispatch decorator

class MockRequest:
    def __init__(self, webhook=None, data="req_data"):
        self.webhook = webhook
        self.data = data
        
    def model_dump(self):
        return {"data": self.data}


class MockResponse:
    def __init__(self, success=True, data="resp_data"):
        self.success = success
        self.data = data
        
    def model_dump(self):
        return {"data": self.data, "success": self.success}


@webhook_dispatch
async def dummy_success_func(request):
    return MockResponse(success=True)


@webhook_dispatch
async def dummy_failure_func(request):
    return MockResponse(success=False)


@webhook_dispatch
async def dummy_exception_func(request):
    raise ValueError("dummy error")


@pytest.mark.asyncio
async def test_webhook_dispatch_success(webhook):
    req = MockRequest(webhook=webhook)
    with patch("koda.utils.webhook.service.dispatch_webhook", new_callable=AsyncMock) as mock_dispatch:
        response = await dummy_success_func(req)
        
        assert response.success is True
        assert mock_dispatch.call_count == 2
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.STARTED, payload={"data": "req_data"})
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.COMPLETED, payload={"data": "resp_data", "success": True})


@pytest.mark.asyncio
async def test_webhook_dispatch_handled_failure(webhook):
    # If the webhook is not configured to receive FAILED events, dispatch_webhook will still be called but will return early internally.
    # However, for this test, we should add FAILED to the webhook so we are testing the decorator's behavior, not dispatch_webhook's filtering.
    # The decorator blindly calls dispatch_webhook.
    req = MockRequest(webhook=webhook)
    with patch("koda.utils.webhook.service.dispatch_webhook", new_callable=AsyncMock) as mock_dispatch:
        response = await dummy_failure_func(req)
        
        assert response.success is False
        assert mock_dispatch.call_count == 2
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.STARTED, payload={"data": "req_data"})
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.FAILED, payload={"data": "resp_data", "success": False})


@pytest.mark.asyncio
async def test_webhook_dispatch_unhandled_exception(webhook):
    req = MockRequest(webhook=webhook)
    with patch("koda.utils.webhook.service.dispatch_webhook", new_callable=AsyncMock) as mock_dispatch:
        with pytest.raises(ValueError, match="dummy error"):
            await dummy_exception_func(req)
        
        assert mock_dispatch.call_count == 2
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.STARTED, payload={"data": "req_data"})
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.FAILED, payload={"data": "req_data", "error": "dummy error"})


@pytest.mark.asyncio
async def test_webhook_dispatch_no_webhook():
    req = MockRequest(webhook=None)
    with patch("koda.utils.webhook.service.dispatch_webhook", new_callable=AsyncMock) as mock_dispatch:
        response = await dummy_success_func(req)
        
        assert response.success is True
        mock_dispatch.assert_not_called()
