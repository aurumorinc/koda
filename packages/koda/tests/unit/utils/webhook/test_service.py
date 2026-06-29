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
from pydantic import BaseModel, ConfigDict
from typing import Optional, Any

class MockRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    webhook: Optional[Any] = None
    data: str = "req_data"


class MockResponse(BaseModel):
    success: bool = True
    data: str = "resp_data"


@webhook_dispatch
async def dummy_success_func(request, webhook=None):
    return MockResponse(success=True)


@webhook_dispatch
async def dummy_failure_func(request, webhook=None):
    return MockResponse(success=False)


@webhook_dispatch
async def dummy_exception_func(request, webhook=None):
    raise ValueError("dummy error")


@pytest.mark.asyncio
async def test_webhook_dispatch_success(webhook):
    req = MockRequest(webhook=webhook)
    with patch("koda.utils.webhook.service.dispatch_webhook", new_callable=AsyncMock) as mock_dispatch:
        response = await dummy_success_func(req, webhook=webhook)
        
        assert response.success is True
        assert mock_dispatch.call_count == 2
        req_payload = req.model_dump(by_alias=True, exclude_none=True)
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.STARTED, payload={"request": req_payload, "webhook": webhook.model_dump(by_alias=True, exclude_none=True)})
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.COMPLETED, payload={"data": "resp_data", "success": True})


@pytest.mark.asyncio
async def test_webhook_dispatch_handled_failure(webhook):
    req = MockRequest(webhook=webhook)
    with patch("koda.utils.webhook.service.dispatch_webhook", new_callable=AsyncMock) as mock_dispatch:
        response = await dummy_failure_func(req, webhook=webhook)
        
        assert response.success is False
        assert mock_dispatch.call_count == 2
        req_payload = req.model_dump(by_alias=True, exclude_none=True)
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.STARTED, payload={"request": req_payload, "webhook": webhook.model_dump(by_alias=True, exclude_none=True)})
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.FAILED, payload={"data": "resp_data", "success": False})


@pytest.mark.asyncio
async def test_webhook_dispatch_unhandled_exception(webhook):
    req = MockRequest(webhook=webhook)
    with patch("koda.utils.webhook.service.dispatch_webhook", new_callable=AsyncMock) as mock_dispatch:
        with pytest.raises(ValueError, match="dummy error"):
            await dummy_exception_func(req, webhook=webhook)
        
        assert mock_dispatch.call_count == 2
        req_payload = req.model_dump(by_alias=True, exclude_none=True)
        # Note: the webhook itself gets added to payload if it's passed as a kwarg too.
        # Since payload is a mutable dict, the 'error' key added later modifies the recorded call's payload in the mock.
        expected_payload = {
            "request": req_payload,
            "webhook": webhook.model_dump(by_alias=True, exclude_none=True),
            "error": "dummy error"
        }
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.STARTED, payload=expected_payload)
        mock_dispatch.assert_any_call(webhook=webhook, event=WebhookEvent.FAILED, payload=expected_payload)


@pytest.mark.asyncio
async def test_webhook_dispatch_no_webhook():
    req = MockRequest(webhook=None)
    with patch("koda.utils.webhook.service.dispatch_webhook", new_callable=AsyncMock) as mock_dispatch:
        response = await dummy_success_func(req, webhook=None)
        
        assert response.success is True
        mock_dispatch.assert_not_called()

def test_serialize_files():
    from koda.utils.webhook.service import _serialize_files
    from koda.utils.file.main import File
    import os

    f1 = File.from_bytes(b"test1", "f1.png", "image/png")
    f2 = File.from_bytes(b"test2", "f2.png", "image/png")
    
    # Fake URL for f1
    f1._presigned_url = "https://example.com/f1.png"
    
    payload = {
        "a": 1,
        "nested": {
            "file": f1,
            "list": [f2]
        }
    }
    
    serialized = _serialize_files(payload)
    assert serialized["a"] == 1
    assert serialized["nested"]["file"] == "https://example.com/f1.png"
    assert serialized["nested"]["list"][0].startswith("data:image/png;base64,")

    f1.cleanup()
    f2.cleanup()

