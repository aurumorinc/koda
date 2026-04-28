"""Extraction logic for scraping pages."""

from __future__ import annotations

import io
import os
import asyncio
import tempfile
import uuid
import re
from typing import Optional
from pathlib import Path

from playwright.async_api import Page
from PIL import Image

from ..config import ScrapeOptions, ScrapeResponse, KodaError, ScrapeError
from ..utils import images_are_identical, extract_metadata, html_to_markdown
from .file import FileService

__all__ = ["Scraper"]

def _sanitize_filename(url: str) -> str:
    sanitized_name = re.sub(r"^https?://", "", url)
    sanitized_name = re.sub(r"[^a-zA-Z0-9]", "_", sanitized_name)
    return sanitized_name[:200]

class Scraper:
    """Service responsible for extracting data from a Playwright Page."""
    
    VIEWPORT_WIDTH = 1280
    VIEWPORT_HEIGHT = 800
    SCROLL_DELAY_MS = 500
    JPEG_QUALITY = 90
    
    @classmethod
    async def extract(cls, page: Page, url: str, options: ScrapeOptions) -> ScrapeResponse:
        """Extract data from a loaded page based on requested options.
        
        Args:
            page: The active Playwright Page object.
            url: The source URL or file path.
            options: Configuration options for extraction.
            
        Returns:
            A ScrapeResponse containing requested formats.
            
        Raises:
            ScrapeError: If extraction fails unexpectedly.
        """
        response = ScrapeResponse(url=url)
        
        try:
            html_content = await page.content()
            
            if "metadata" in options.formats:
                response.metadata = extract_metadata(html_content)
                
            if "markdown" in options.formats:
                response.markdown = html_to_markdown(
                    html_content, 
                    only_main_content=options.only_main_content
                )
                
            if "screenshot" in options.formats:
                if not options.s3_config:
                    raise ScrapeError("s3_config is required in ScrapeOptions to extract screenshots.")
                    
                screenshot_bytes = await cls._capture_full_page_screenshot(page)
                
                # Write to temp file and upload to S3
                fd, temp_path = tempfile.mkstemp(suffix=".jpg")
                try:
                    with open(temp_path, "wb") as f:
                        f.write(screenshot_bytes)
                        
                    object_name = f"{_sanitize_filename(url)}_{uuid.uuid4().hex[:8]}.jpg"
                    
                    presigned_url = await asyncio.to_thread(
                        FileService.upload_and_presign,
                        file_path=temp_path,
                        object_name=object_name,
                        mimetype="image/jpeg",
                        s3_config=options.s3_config
                    )
                    response.screenshot = presigned_url
                finally:
                    os.close(fd)
                    os.remove(temp_path)
                    
        except Exception as e:
            raise ScrapeError(f"Failed to extract content from {url}: {str(e)}") from e
            
        return response
        
    @classmethod
    async def _capture_full_page_screenshot(cls, page: Page) -> bytes:
        """Scrolls and captures a full page stitched screenshot as JPEG bytes.
        
        Args:
            page: The Playwright Page object.
            
        Returns:
            JPEG bytes of the screenshot.
        """
        # Ensure viewport is set to default initially
        await page.set_viewport_size({"width": cls.VIEWPORT_WIDTH, "height": cls.VIEWPORT_HEIGHT})
        
        # Move mouse to center to avoid hover effects on edges
        await page.mouse.move(cls.VIEWPORT_WIDTH / 2, cls.VIEWPORT_HEIGHT / 2)
        await asyncio.sleep(0.5)
        
        scroll_count = 0
        
        # Take initial screenshot for comparison
        screenshot_bytes = await page.screenshot(full_page=False)
        last_img = Image.open(io.BytesIO(screenshot_bytes))
        
        while True:
            # Scroll down by one viewport height
            await page.mouse.wheel(0, cls.VIEWPORT_HEIGHT)
            
            # Wait for any potential lazy loading or scroll animation
            await asyncio.sleep(cls.SCROLL_DELAY_MS / 1000.0)
            
            # Take new screenshot
            new_screenshot_bytes = await page.screenshot(full_page=False)
            new_img = Image.open(io.BytesIO(new_screenshot_bytes))
            
            if images_are_identical(last_img, new_img):
                break
            
            scroll_count += 1
            last_img = new_img
            
            # Put a hard cap to avoid infinite loops on dynamically expanding pages
            if scroll_count > 50:
                break

        # Calculate total height
        total_height = (scroll_count + 1) * cls.VIEWPORT_HEIGHT
        
        # Change viewport to the full height
        await page.set_viewport_size({"width": cls.VIEWPORT_WIDTH, "height": total_height})
        
        # Scroll back to top to ensure we capture from the start
        await page.mouse.wheel(0, -total_height)
        await asyncio.sleep(1) # Give it time to settle after resize
        
        # Take the final screenshot
        final_screenshot_bytes = await page.screenshot(full_page=True, type="jpeg", quality=cls.JPEG_QUALITY)
        return final_screenshot_bytes
