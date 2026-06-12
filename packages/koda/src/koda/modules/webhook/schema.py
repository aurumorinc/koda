from __future__ import annotations
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

class WebhookConfig(BaseModel):
    """Configuration for a webhook callback.
    
    Attributes:
        url: The URL to send the webhook to.
        headers: Optional dictionary of headers to include.
        metadata: Optional dictionary of metadata to append to the root payload.
        events: Optional list of event types to trigger on (e.g., ['crawl.started', 'crawl.page', 'crawl.completed']).
    """
    url: str
    headers: Optional[Dict[str, str]] = None
    metadata: Optional[Dict[str, Any]] = None
    events: Optional[List[str]] = None
