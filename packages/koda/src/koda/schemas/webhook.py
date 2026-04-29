from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class WebhookConfig:
    """Configuration for a webhook callback.
    
    Attributes:
        url: The URL to send the webhook to.
        headers: Optional dictionary of headers to include.
        metadata: Optional dictionary of metadata to append to the root payload.
    """
    url: str
    headers: Optional[Dict[str, str]] = None
    metadata: Optional[Dict[str, Any]] = None
