"""Core client for the Koda extraction engine."""

from __future__ import annotations

import asyncio
import uuid
from typing import Union, List, Dict, Any, Optional
from pathlib import Path

from playwright.async_api import async_playwright, Browser, Page

from .exceptions import KodaError
from .schemas.page import ScrapeRequest, ScrapeResponse, Action
from .schemas.webhook import WebhookConfig
from .utils import sanitize_filename
from .services import page, file, webhook

__all__ = ["KodaClient"]

class KodaClient:
    """Primary interface for web scraping and extraction.
    
    Attributes:
        browser_url: Optional WebSocket/CDP endpoint for remote browsers (e.g., Moon).
        proxy: Optional proxy configuration dictionary.
        global_timeout: Default timeout for all operations in milliseconds.
    """
    
    def __init__(
        self, 
        browser_url: Optional[str] = None,
        proxy: Optional[Dict[str, str]] = None,
        global_timeout: int = 30000
    ) -> None:
        """Initialize the KodaClient."""
        self.browser_url = browser_url
        self.proxy = proxy
        self.global_timeout = global_timeout
        self._playwright = None
        self._browser: Optional[Browser] = None
        
    async def __aenter__(self) -> KodaClient:
        await self.start()
        return self
        
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
        
    async def start(self) -> None:
        """Start the underlying Playwright browser session."""
        if self._playwright is None:
            self._playwright = await async_playwright().start()
            
        if self._browser is None:
            if self.browser_url:
                self._browser = await self._playwright.chromium.connect_over_cdp(self.browser_url)
            else:
                self._browser = await self._playwright.chromium.launch(
                    headless=True,
                    proxy=self.proxy
                )

    async def close(self) -> None:
        """Close the browser session."""
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
            
    async def _execute_actions(self, playwright_page: Page, actions: List[Action]) -> None:
        """Execute a list of predefined actions on the page before scraping."""
        for action in actions:
            if action.type == "wait" and isinstance(action.value, (int, float)):
                await asyncio.sleep(action.value / 1000.0)
            elif action.type == "wait_for_selector" and action.selector:
                await playwright_page.wait_for_selector(action.selector)
            elif action.type == "click" and action.selector:
                await playwright_page.click(action.selector)
            elif action.type == "type" and action.selector and action.value:
                await playwright_page.fill(action.selector, str(action.value))

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
        if self._browser is None:
            raise KodaError("Browser is not started. Call start() or use 'async with KodaClient():'")
            
        playwright_page: Optional[Page] = None
        context = None
        
        try:
            context = await self._browser.new_context()
            playwright_page = await context.new_page()
            playwright_page.set_default_timeout(request.timeout or self.global_timeout)
            
            target_url = request.url
            url_path = Path(request.url)
            if url_path.exists() and not request.url.startswith("http"):
                target_url = url_path.absolute().as_uri()
                    
            await playwright_page.goto(target_url, wait_until="networkidle")
            
            if request.actions:
                await self._execute_actions(playwright_page, request.actions)
                
            # 1. Page Domain handles the extraction logic
            response = await page.scrape(playwright_page, request)
            
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
                await webhook.handle(request.webhook, response)
                
            return response
            
        except Exception as e:
            error_response = ScrapeResponse(url=request.url, error=str(e))
            if request.webhook:
                await webhook.handle(request.webhook, error_response)
            return error_response
            
        finally:
            if playwright_page:
                await playwright_page.close()
            if context:
                await context.close()
