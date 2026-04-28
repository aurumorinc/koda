"""Core client for the Koda extraction engine."""

from __future__ import annotations

import asyncio
from typing import Union, List, Dict, Any, Optional
from pathlib import Path

from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from .config import ScrapeOptions, ScrapeResponse, Action, KodaError
from .services.scrape import Scraper
from .services.webhook import WebhookService

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
            
    async def _execute_actions(self, page: Page, actions: List[Action]) -> None:
        """Execute a list of predefined actions on the page before scraping.
        
        Args:
            page: The Playwright Page object.
            actions: List of Action objects.
        """
        for action in actions:
            if action.type == "wait" and isinstance(action.value, (int, float)):
                await asyncio.sleep(action.value / 1000.0)
            elif action.type == "wait_for_selector" and action.selector:
                await page.wait_for_selector(action.selector)
            elif action.type == "click" and action.selector:
                await page.click(action.selector)
            elif action.type == "type" and action.selector and action.value:
                await page.fill(action.selector, str(action.value))

    async def scrape(
        self,
        url: Union[str, Path],
        options: Optional[ScrapeOptions] = None,
        **kwargs: Any
    ) -> ScrapeResponse:
        """Scrape a URL or local file and extract the requested formats.
        
        Args:
            url: The HTTP URL or local Path to an MHTML/HTML file.
            options: Configuration options for extraction.
            **kwargs: Override specific ScrapeOptions fields (e.g., formats=["markdown"]).
            
        Returns:
            A ScrapeResponse containing the requested data.
            
        Raises:
            KodaError: If the browser is not started or extraction fails.
        """
        if self._browser is None:
            raise KodaError("Browser is not started. Call start() or use 'async with KodaClient():'")
            
        if options is None:
            options = ScrapeOptions()
            
        # Allow overriding options via kwargs
        for key, value in kwargs.items():
            if hasattr(options, key):
                setattr(options, key, value)
                
        context: Optional[BrowserContext] = None
        page: Optional[Page] = None
        
        try:
            context = await self._browser.new_context()
            page = await context.new_page()
            page.set_default_timeout(options.timeout or self.global_timeout)
            
            target_url = str(url)
            if isinstance(url, Path) or (isinstance(url, str) and not url.startswith("http")):
                # Ensure it's a valid file URI
                path_obj = Path(url)
                if path_obj.exists():
                    target_url = path_obj.absolute().as_uri()
                    
            await page.goto(target_url, wait_until="networkidle")
            
            if options.actions:
                await self._execute_actions(page, options.actions)
                
            response = await Scraper.extract(page, str(url), options)
            
            if options.webhook:
                # Await to ensure dispatch finishes before returning
                await WebhookService.dispatch(options.webhook, response)
                
            return response
            
        except Exception as e:
            error_response = ScrapeResponse(url=str(url), error=str(e))
            if options and options.webhook:
                await WebhookService.dispatch(options.webhook, error_response)
            return error_response
            
        finally:
            if page:
                await page.close()
            if context:
                await context.close()
