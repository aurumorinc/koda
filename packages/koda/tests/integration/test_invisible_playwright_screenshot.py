import pytest
from koda.modules.browser.service import BrowserSession
from koda.config.main import settings
import png  # type: ignore[missing-import]

@pytest.mark.asyncio
async def test_invisible_screenshot_color_fidelity():
    """
    Verifies that Playwright screenshots taken inside the invisible-playwright browser 
    function exactly like standard Playwright screenshots, without visual corruption or static.
    """
    # Temporarily force the browser to invisible_playwright
    original_browser = settings.browser
    settings.browser = "invisible_playwright"
    settings.browser_type = "firefox"
    
    try:
        config = {"headless": True, "substitute_pixels": False}
        async with BrowserSession(config=config) as context:
            page = await context.new_page()
            
            # Navigate to a minimal page with a distinct solid red background
            await page.goto("data:text/html,<body style='background: rgb(250, 0, 0); margin: 0;'></body>")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(1000)
            
            # Take screenshot
            screenshot_bytes = await page.screenshot(type="png")
            
            assert len(screenshot_bytes) > 0
            
            # Decode PNG bytes using pypng
            width, height, rows, info = png.Reader(bytes=screenshot_bytes).read_flat()
            
            has_alpha = info.get("alpha", False)
            channels = 4 if has_alpha else 3
            
            total_r = 0
            total_g = 0
            total_b = 0
            num_pixels = width * height
            
            for i in range(0, len(rows), channels):
                total_r += rows[i]
                total_g += rows[i + 1]
                total_b += rows[i + 2]
                
            avg_r = total_r / num_pixels
            avg_g = total_g / num_pixels
            avg_b = total_b / num_pixels
            
            # We expect a solid red image. The substitute_pixels patch may add 
            # minor invisible noise (+- 1 to rgb), so we use a threshold
            # instead of strict equality. Static noise averages to ~127 per channel.
            assert avg_r > 240, f"Average red channel is too low ({avg_r}), rendering is corrupted."
            assert avg_g < 10, f"Average green channel is too high ({avg_g}), rendering is corrupted."
            assert avg_b < 10, f"Average blue channel is too high ({avg_b}), rendering is corrupted."

    finally:
        settings.browser = original_browser

@pytest.mark.asyncio
async def test_invisible_screenshot_color_fidelity_static():
    """
    Verifies that when substitute_pixels=True (default), invisible-playwright's
    stealth patch intentionally scrambles the screenshot into static noise.
    """
    original_browser = settings.browser
    settings.browser = "invisible_playwright"
    settings.browser_type = "firefox"
    
    try:
        # Default behavior: substitute_pixels is True
        config = {"headless": True, "substitute_pixels": True}
        async with BrowserSession(config=config) as context:
            page = await context.new_page()
            
            await page.goto("data:text/html,<body style='background: rgb(250, 0, 0); margin: 0;'></body>")
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(1000)
            
            screenshot_bytes = await page.screenshot(type="png")
            
            assert len(screenshot_bytes) > 0
            
            # Decode PNG bytes using pypng
            width, height, rows, info = png.Reader(bytes=screenshot_bytes).read_flat()
            
            has_alpha = info.get("alpha", False)
            channels = 4 if has_alpha else 3
            
            total_r = 0
            total_g = 0
            total_b = 0
            num_pixels = width * height
            
            for i in range(0, len(rows), channels):
                total_r += rows[i]
                total_g += rows[i + 1]
                total_b += rows[i + 2]
                
            avg_r = total_r / num_pixels
            avg_g = total_g / num_pixels
            avg_b = total_b / num_pixels
            
            # Static noise averages to ~127 per channel.
            # So even though the page is bright red, the screenshot will have an average
            # color that is perfectly gray (entropy).
            assert 100 < avg_r < 150, f"Expected static noise for red channel, got {avg_r}"
            assert 100 < avg_g < 150, f"Expected static noise for green channel, got {avg_g}"
            assert 100 < avg_b < 150, f"Expected static noise for blue channel, got {avg_b}"

    finally:
        settings.browser = original_browser
