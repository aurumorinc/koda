import asyncio
from worldline import structlog
from typing import Any, Callable, Dict, Optional
import functools

import httpx

from koda.utils.webhook.schema import Webhook, WebhookEvent

logger = structlog.get_logger(__name__)


async def dispatch_webhook(
    webhook: Optional[Webhook], event: WebhookEvent, payload: Dict[str, Any]
) -> None:
    """Trigger an HTTP callback based on the webhook spec asynchronously."""
    if not webhook:
        return

    if webhook.events and event not in webhook.events:
        return

    request_payload = {"event": event.value, "payload": payload}
    if webhook.metadata:
        request_payload["metadata"] = webhook.metadata

    headers = webhook.headers or {}

    async def _send() -> None:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    str(webhook.url),
                    json=request_payload,
                    headers=headers,
                )
                response.raise_for_status()
        except Exception as e:
            logger.warning("Failed to trigger webhook for event %s: %s", event.value, e)

    asyncio.create_task(_send())


def webhook_dispatch(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to handle webhook lifecycle events (STARTED, COMPLETED, FAILED)."""
    @functools.wraps(func)
    async def wrapper(request: Any, *args: Any, **kwargs: Any) -> Any:
        webhook = getattr(request, "webhook", None)
        
        if webhook:
            await dispatch_webhook(
                webhook=webhook,
                event=WebhookEvent.STARTED,
                payload=request.model_dump()
            )

        try:
            response = await func(request, *args, **kwargs)
        except Exception as e:
            if webhook:
                payload = request.model_dump()
                payload["error"] = str(e)
                await dispatch_webhook(
                    webhook=webhook,
                    event=WebhookEvent.FAILED,
                    payload=payload
                )
            raise e

        success = getattr(response, "success", True)
        event = WebhookEvent.COMPLETED if success else WebhookEvent.FAILED
        if webhook:
            await dispatch_webhook(
                webhook=webhook,
                event=event,
                payload=response.model_dump()
            )
        return response

    return wrapper
