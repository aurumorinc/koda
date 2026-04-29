"""Webhook service for sending callback responses."""

import sys
import json
import asyncio
import urllib.request
import urllib.error
from typing import Dict, Any

from ..schemas.webhook import WebhookConfig
from ..schemas.page import ScrapeResponse

__all__ = ["handle"]

async def handle(config: WebhookConfig, response: ScrapeResponse) -> None:
    """
    Asynchronously sends a ScrapeResponse to the configured webhook URL.
    
    Args:
        config: The webhook configuration containing url, headers, and metadata.
        response: The ScrapeResponse to serialize and send.
    """
    # Build the payload similar to Firecrawl response
    data: Dict[str, Any] = {}
    if response.markdown is not None:
        data["markdown"] = response.markdown
    if response.metadata is not None:
        data["metadata"] = response.metadata
    if response.screenshot is not None:
        data["screenshot"] = response.screenshot

    payload: Dict[str, Any] = {
        "success": response.error is None
    }
    
    if response.error:
        payload["error"] = response.error
    else:
        payload["data"] = data

    # Add custom metadata to the root payload if requested
    if config.metadata:
        payload.update(config.metadata)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Koda-Webhook-Client/1.0"
    }
    if config.headers:
        headers.update(config.headers)

    payload_bytes = json.dumps(payload).encode("utf-8")

    def _send() -> None:
        try:
            req = urllib.request.Request(
                config.url,
                data=payload_bytes,
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as http_response:
                # Successfully sent, no action needed on success
                pass
        except urllib.error.HTTPError as e:
            print(f"Webhook dispatch failed with status {e.code}: {e.reason}", file=sys.stderr)
        except urllib.error.URLError as e:
            print(f"Webhook dispatch failed to reach URL: {e.reason}", file=sys.stderr)
        except Exception as e:
            print(f"Webhook dispatch failed with an unexpected error: {str(e)}", file=sys.stderr)

    # Offload network I/O to a background thread
    await asyncio.to_thread(_send)
