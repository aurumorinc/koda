import logging
import time
from typing import Any
from koda.infrastructure.posthog import setup_playwright_transport, setup_network_capture, inject_posthog_monolith

logger = logging.getLogger("koda.patches.crawl4ai")

_patched = False

def patch_crawl4ai(api_key: str, host: str) -> None:
    """Monkey patch crawl4ai's AsyncWebCrawler and BrowserManager to use stealth browser and track events."""
    global _patched
    if _patched:
        return

    try:
        from crawl4ai import AsyncWebCrawler
        from crawl4ai.browser_manager import BrowserManager
        
        # 1. Patch BrowserManager.start to use our stealth browser
        original_start = BrowserManager.start

        async def patched_start(self):
            if self.playwright is not None:
                await self.close()

            # DO NOT start a new playwright driver here! It leaks Node.js processes.
            self.playwright = None

            # Use our stealth browser!
            from koda.modules.browser.service import get_browser
            self.browser = await get_browser(
                browser_type=self.config.browser_type,
                config={"headless": self.config.headless}
            )
            self.default_context = self.browser

            # Set the browser endpoint key for global page tracking
            self._browser_endpoint_key = self._compute_browser_endpoint_key()
            if self._browser_endpoint_key not in BrowserManager._global_pages_in_use:
                BrowserManager._global_pages_in_use[self._browser_endpoint_key] = set()

        BrowserManager.start = patched_start

        # 2. Patch BrowserManager.close to prevent closing our shared stealth browser
        original_close = BrowserManager.close

        async def patched_close(self):
            # Explicitly close the context we created to prevent memory leaks
            if hasattr(self, '_koda_context') and self._koda_context:
                try:
                    await self._koda_context.close()
                except Exception as e:
                    logger.error(f"Failed to close context during patched_close: {e}")
            
            # Properly exit the koda context manager to prevent browser process leaks
            if hasattr(self, 'browser') and self.browser and hasattr(self.browser, '_koda_context_manager'):
                try:
                    await self.browser._koda_context_manager.__aexit__(None, None, None)
                except Exception as e:
                    logger.error(f"Failed to close koda browser context manager: {e}")

            # Set self.browser to None so original_close doesn't close our shared browser
            self.browser = None
            await original_close(self)

        BrowserManager.close = patched_close

        # 3. Patch BrowserManager.create_browser_context to avoid Firefox ignore_https_errors protocol error
        original_create_browser_context = BrowserManager.create_browser_context

        async def patched_create_browser_context(self, crawlerRunConfig=None):
            old_val = self.config.ignore_https_errors
            self.config.ignore_https_errors = False
            try:
                context = await original_create_browser_context(self, crawlerRunConfig)
                self._koda_context = context  # Save reference for cleanup
                return context
            finally:
                self.config.ignore_https_errors = old_val

        BrowserManager.create_browser_context = patched_create_browser_context

        # 4. Patch BrowserManager.get_page to inject PostHog monolith and setup network capture
        original_get_page = BrowserManager.get_page

        async def patched_get_page(self, crawlerRunConfig):
            print("patched_get_page called!")
            page, context = await original_get_page(self, crawlerRunConfig)
            
            page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
            
            # Setup PostHog transport on context
            await setup_playwright_transport(context)
            
            # Setup network capture and inject monolith on page
            await setup_network_capture(page, api_key)
            await inject_posthog_monolith(page, api_key, host)
            
            return page, context

        BrowserManager.get_page = patched_get_page

        # 5. Patch AsyncWebCrawler.arun for event tracking
        original_arun = AsyncWebCrawler.arun

        async def patched_arun(self, url: str, *args: Any, **kwargs: Any) -> Any:
            try:
                result = await original_arun(self, url, *args, **kwargs)
                return result
            except Exception as e:
                raise

        AsyncWebCrawler.arun = patched_arun
        _patched = True
        logger.info("Successfully monkey patched crawl4ai AsyncWebCrawler and BrowserManager.")
    except ImportError:
        logger.debug("crawl4ai not installed, skipping patch.")
    except Exception as e:
        logger.error(f"Failed to patch crawl4ai: {e}")
