"""Webhook utility for dispatching HTTP callbacks."""

import sys
import json
import asyncio
import httpx
from typing import Dict, Any, Optional

from koda.modules.webhook.schema import WebhookConfig

__all__ = ["dispatch_webhook"]

async def dispatch_webhook(config: WebhookConfig, event_type: str, payload: Dict[str, Any]) -> None:
    """
    Asynchronously sends a payload to the configured webhook URL.
    
    Args:
        config: The webhook configuration containing url, headers, metadata, and events.
        event_type: The type of event (e.g., 'crawl.started', 'crawl.page', 'crawl.completed').
        payload: The data to send in the webhook.
    """
    # Check if this event type should be dispatched
    if config.events and event_type not in config.events:
        return

    # Build the final payload
    final_payload: Dict[str, Any] = {
        "type": event_type,
        **payload
    }

    # Add custom metadata to the root payload if requested
    if config.metadata:
        final_payload.update(config.metadata)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Koda-Webhook-Client/1.0"
    }
    if config.headers:
        headers.update(config.headers)

    async def _send() -> None:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    config.url,
                    json=final_payload,
                    headers=headers
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"Webhook dispatch failed with status {e.response.status_code}: {e.response.text}", file=sys.stderr)
        except httpx.RequestError as e:
            print(f"Webhook dispatch failed to reach URL: {str(e)}", file=sys.stderr)
        except Exception as e:
            print(f"Webhook dispatch failed with an unexpected error: {str(e)}", file=sys.stderr)

    # Fire and forget
    asyncio.create_task(_send())
