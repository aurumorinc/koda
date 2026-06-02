"""Core client for the Koda extraction engine."""

from __future__ import annotations

import asyncio
import uuid
from typing import Union, List, Dict, Any, Optional
from pathlib import Path

from koda.exceptions import KodaError
from koda.modules.page.schema import ScrapeRequest, ScrapeResponse, Action
from koda.modules.webhook.schema import WebhookConfig
from koda.utils import sanitize_filename
from koda.modules.page import service as page
from koda.modules.file import service as file
from koda.modules.webhook.utils import dispatch_webhook
from koda.config.main import settings
from koda.infrastructure.crawl4ai import patch_crawl4ai
from koda.modules.cache import service as cache

__all__ = ["KodaClient"]

class KodaClient:
    """Primary interface for web scraping and extraction.
    
    Attributes:
        global_timeout: Default timeout for all operations in milliseconds.
    """
    
    def __init__(
        self,
        global_timeout: int = 30000,
        browser_type: str = "firefox",
        posthog_api_key: Optional[str] = None,
        posthog_host: Optional[str] = None
    ) -> None:
        """Initialize the KodaClient."""
        self.global_timeout = global_timeout
        self.browser_type = browser_type
        self.posthog_api_key = posthog_api_key or settings.posthog_api_key
        self.posthog_host = posthog_host or settings.posthog_host
        
        # Expose the unified cache adapter
        self.cache = cache
        
        # Apply monkey patches to third-party crawlers
        patch_crawl4ai(self.posthog_api_key, self.posthog_host)
        
    async def __aenter__(self) -> KodaClient:
        return self
        
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    async def scrape(
        self,
        request: ScrapeRequest
    ) -> ScrapeResponse:
        """Scrape a URL or local file and extract the requested domains.
        
        Args:
            request: Configuration and target for the scraping job.
            
        Returns:
            A ScrapeResponse containing the requested data.
        """
        try:
            if not request.timeout:
                request.timeout = self.global_timeout
                
            url_path = Path(request.url)
            if url_path.exists() and not request.url.startswith("http"):
                request.url = url_path.absolute().as_uri()
                    
            # 1. Page Domain handles the extraction logic
            response = await page.scrape(request)
            
            # 2. File Domain handles persistence side-effects
            if hasattr(response, "_screenshot_bytes") and request.s3_config:
                screenshot_bytes = getattr(response, "_screenshot_bytes")
                object_name = f"{sanitize_filename(request.url)}_{uuid.uuid4().hex[:8]}.jpg"
                
                await asyncio.to_thread(
                    file.upload,
                    data=screenshot_bytes,
                    object_name=object_name,
                    mimetype="image/jpeg",
                    s3_config=request.s3_config
                )
                
                response.screenshot = file.generate_presigned_url(
                    object_name=object_name,
                    s3_config=request.s3_config
                )
            
            # 3. Webhook Domain handles outbound notifications
            if request.webhook:
                payload = {"success": True, "data": {}}
                if response.markdown: payload["data"]["markdown"] = response.markdown
                if response.html: payload["data"]["html"] = response.html
                if response.links: payload["data"]["links"] = response.links
                if response.images: payload["data"]["images"] = response.images
                if response.metadata: payload["data"]["metadata"] = response.metadata
                if response.screenshot: payload["data"]["screenshot"] = response.screenshot
                await dispatch_webhook(request.webhook, "scrape.completed", payload)
                
            return response
            
        except Exception as e:
            error_response = ScrapeResponse(url=request.url, error=str(e))
            if request.webhook:
                await dispatch_webhook(request.webhook, "scrape.failed", {"success": False, "error": str(e)})
            return error_response
