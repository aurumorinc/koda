import logging
import os
import sys
from typing import Any, Tuple, Optional
from playwright.async_api import Browser

logger = logging.getLogger("koda.modules.browser")

class BrowserLaunchError(Exception):
    """Raised when the stealth browser fails to launch."""
    pass

# Keep track of the active InvisiblePlaywright context manager instance
_ip_instance: Optional[Any] = None

async def launch_stealth_browser(headless: bool = True, **kwargs: Any) -> Browser:
    """Launch the InvisiblePlaywright browser (Firefox) with stealth configurations."""
    global _ip_instance
    try:
        from invisible_playwright.async_api import InvisiblePlaywright
        
        # We merge any user-provided extra_prefs
        extra_prefs = kwargs.get("extra_prefs", {})
        
        # We instantiate InvisiblePlaywright with humanize=False
        # CSP overrides (if any) are handled by the BrowserSession's CSP strategy.
        _ip_instance = InvisiblePlaywright(
            headless=headless,
            humanize=kwargs.get("humanize", False),
            extra_prefs=extra_prefs
        )
        
        # Start the browser by entering the context manager manually
        browser = await _ip_instance.__aenter__()
        logger.info("Stealth browser (Firefox via invisible-playwright) launched successfully.")
        return browser
    except Exception as e:
        logger.error(f"Failed to launch stealth browser: {e}")
        raise BrowserLaunchError(f"Failed to launch stealth browser: {e}") from e

async def stop_stealth_browser() -> None:
    """Stop the active InvisiblePlaywright browser context manager."""
    global _ip_instance
    if _ip_instance is not None:
        try:
            await _ip_instance.__aexit__(None, None, None)
        except Exception as e:
            logger.error(f"Error exiting InvisiblePlaywright context manager: {e}")
        finally:
            _ip_instance = None
