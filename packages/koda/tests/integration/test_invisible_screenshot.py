import pytest
from koda.modules.browser.service import BrowserSession
from koda.config.main import settings
import io
import zlib

@pytest.mark.asyncio
async def test_invisible_playwright_screenshot_substitute_pixels():
    """
    Test that when substitute_pixels is False, the screenshot is not random static.
    Random static PNGs have high entropy (do not compress well), whereas a screenshot
    of a simple webpage will compress very well.
    """
    # Temporarily force the browser to invisible_playwright
    original_browser = settings.browser
    settings.browser = "invisible_playwright"
    settings.browser_type = "firefox"
    
    try:
        # Launch with substitute_pixels = False
        config = {"headless": True, "substitute_pixels": False}
        async with BrowserSession(config=config) as context:
            page = await context.new_page()
            # Use data URI to avoid CSP issues with set_content
            await page.goto("data:text/html,<html><body style='background: white;'><h1>Hello</h1></body></html>")
            
            # Take screenshot
            screenshot_bytes = await page.screenshot(type="png")
            
            # Assert screenshot is not empty
            assert len(screenshot_bytes) > 0
            
            # Check file size as a proxy for entropy/static
            # Pure random noise creates massive PNGs (typically > 5MB)
            # A simple white page with some text will be < 1MB
            
            assert len(screenshot_bytes) < 1000000, f"Screenshot size {len(screenshot_bytes)} is too large, suggesting pixel substitution is still active."
    finally:
        settings.browser = original_browser
        
@pytest.mark.asyncio
async def test_invisible_playwright_screenshot_substitute_pixels_true():
    """
    Test that when substitute_pixels is True (default), the screenshot is random static.
    """
    original_browser = settings.browser
    settings.browser = "invisible_playwright"
    settings.browser_type = "firefox"
    
    try:
        # Launch with substitute_pixels = True (default)
        config = {"headless": True, "substitute_pixels": True}
        async with BrowserSession(config=config) as context:
            page = await context.new_page()
            # Navigate to a minimal page via data URI
            await page.goto("data:text/html,<html><body style='background: white;'><h1>Hello</h1></body></html>")
            
            # Take screenshot
            screenshot_bytes = await page.screenshot(type="png")
            
            # Assert screenshot is not empty
            assert len(screenshot_bytes) > 0
            
            # Check file size as a proxy for entropy/static
            # Static noise should result in a massive PNG (typically > 5MB)
            assert len(screenshot_bytes) > 2000000, f"Screenshot size {len(screenshot_bytes)} is too small, suggesting pixel substitution is NOT active when it should be."
    finally:
        settings.browser = original_browser
