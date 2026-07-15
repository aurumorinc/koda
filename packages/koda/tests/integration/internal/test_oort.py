import asyncio
import pytest
from typing import Optional
from pydantic import BaseModel

from oort.webhook.service import webhook_dispatch
from oort.webhook.schema import WebhookRequest
from oort.file.main import File
from koda.config.main import settings

class DummyResponse(BaseModel):
    success: bool
    data: list
    error: Optional[str] = None

@webhook_dispatch(event_prefix="test_oort_integration")
async def dummy_async_endpoint(request_id: str, webhook: Optional[WebhookRequest] = None) -> DummyResponse:
    # Mimics the return payload structure of scrape_youtube_profile
    # We return an oort.file.main.File object to ensure it gets serialized successfully.
    f = File.from_bytes(b"dummy image content", "dummy_screenshot.png", "image/png")
    
    # We can simulate an asyncio background task that must not be abandoned.
    # If a RuntimeError is thrown, the task might be cancelled or abandoned.
    # Here we just make sure we can reach the return statement.
    return DummyResponse(success=True, data=[{"screenshot": f}])

@pytest.mark.asyncio
async def test_oort_async_webhook_dispatch_serialization_deadlock():
    """
    Tests that a File object returned from an async function wrapped by
    webhook_dispatch can be serialized asynchronously without raising
    a RuntimeError from async_to_sync.
    """
    # We don't strictly need live S3 credentials, as the bug triggers BEFORE upload
    # when async_to_sync attempts to get the running loop. But we want to ensure
    # the endpoint runs smoothly.
    webhook = WebhookRequest(url="http://localhost:12345/webhook", events=["completed"])

    # If the bug is present, this will raise a RuntimeError:
    # "You cannot use AsyncToSync in the same thread as an async event loop"
    response = await dummy_async_endpoint(request_id="123", webhook=webhook)

    assert response.success is True
    # The endpoint ran successfully. We also know that the webhook_dispatch
    # did not crash the event loop because we reached this assertion.
