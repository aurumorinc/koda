"""Core client for the Koda extraction engine."""

from __future__ import annotations

import asyncio
import uuid
from typing import Union, List, Dict, Any, Optional
from pathlib import Path

from koda.exceptions import KodaError
from koda.modules.page.schema import ScrapeRequest, ScrapeResponse, Action
from koda.modules.site.schema import CrawlRequest, CrawlResponse
from koda.modules.webhook.schema import WebhookConfig
from koda.utils import sanitize_filename
from koda.modules.page import service as page
from koda.modules.site import service as site
from koda.modules.file import service as file
from koda.modules.webhook.utils import dispatch_webhook
from koda.config.main import settings
from koda.infrastructure.crawl4ai import patch_crawl4ai
from koda.modules.cache import service as cache

__all__ = ["KodaClient"]

class KodaClient:
    """Primary interface for web scraping and extraction."""
    
    def __init__(self) -> None:
        """Initialize the KodaClient."""
        # Expose the unified cache adapter
        self.cache = cache
        
        # Apply monkey patches to third-party crawlers
        patch_crawl4ai(settings.posthog_api_key, settings.posthog_host)
        
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
        url_path = Path(request.url)
        if url_path.exists() and not request.url.startswith("http"):
            request.url = url_path.absolute().as_uri()
            
        return await page.scrape(request)

    async def crawl(
        self,
        request: CrawlRequest
    ) -> CrawlResponse:
        """Crawl a site starting from a URL and extract information.
        
        Args:
            request: Configuration and target for the crawling job.
            
        Returns:
            A CrawlResponse containing the summary of the crawl.
        """
        url_str = str(request.url)
        url_path = Path(url_str)
        if url_path.exists() and not url_str.startswith("http"):
            request.url = url_path.absolute().as_uri()
            
        return await site.crawl(request)
