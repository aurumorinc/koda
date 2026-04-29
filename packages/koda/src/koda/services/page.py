"""Extraction logic for processing web pages."""

from __future__ import annotations

import io
import asyncio
from typing import Dict, Any, Optional
from playwright.async_api import Page
from PIL import Image
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from koda.utils import images_are_identical
from koda.schemas.page import ScrapeRequest, ScrapeResponse

__all__ = ["scrape"]

# Constants
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 800
SCROLL_DELAY_MS = 500
JPEG_QUALITY = 90

async def scrape(page: Page, request: ScrapeRequest) -> ScrapeResponse:
    """Extract data from a loaded page based on requested options.
    
    This function orchestrates the extraction of markdown, metadata, and screenshots.
    It returns a ScrapeResponse containing the extracted data.
    """
    response = ScrapeResponse(url=request.url)
    
    html_content = await page.content()
    
    if "metadata" in request.formats:
        response.metadata = _extract_metadata(html_content)
        
    if "markdown" in request.formats:
        response.markdown = _to_markdown(
            html_content, 
            only_main_content=request.only_main_content
        )
        
    if "screenshot" in request.formats:
        # We attach the bytes to the response object temporarily for the client to handle.
        setattr(response, "_screenshot_bytes", await _capture_screenshot(page, request.url))
        
    return response

def _is_mhtml(url: str) -> bool:
    """Helper to detect if the target is an MHTML file."""
    from urllib.parse import urlparse
    path = urlparse(url).path.lower()
    return path.endswith(".mhtml") or path.endswith(".mht")

async def _capture_screenshot(page: Page, url: str) -> bytes:
    """Routes the screenshot request based on the target type."""
    if _is_mhtml(url):
        return await _capture_mhtml_screenshot(page)
    else:
        return await _capture_live_screenshot(page)

async def _capture_live_screenshot(page: Page) -> bytes:
    """Captures a screenshot of a live web page.
    
    TODO: Update to use javascript for scrollHeight and rapid scrolling
    for triggering lazy-loaded images before capture.
    """
    return await page.screenshot(full_page=True, type="jpeg", quality=JPEG_QUALITY)

async def _capture_mhtml_screenshot(page: Page) -> bytes:
    """Scrolls and captures a full page stitched screenshot as JPEG bytes."""
    # Ensure viewport is set to default initially
    await page.set_viewport_size({"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT})
    
    # Move mouse to center to avoid hover effects on edges
    await page.mouse.move(VIEWPORT_WIDTH / 2, VIEWPORT_HEIGHT / 2)
    await asyncio.sleep(0.5)
    
    scroll_count = 0
    
    # Take initial screenshot for comparison
    screenshot_bytes = await page.screenshot(full_page=False)
    last_img = Image.open(io.BytesIO(screenshot_bytes))
    
    while True:
        # Scroll down by one viewport height
        await page.mouse.wheel(0, VIEWPORT_HEIGHT)
        
        # Wait for any potential lazy loading or scroll animation
        await asyncio.sleep(SCROLL_DELAY_MS / 1000.0)
        
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
    total_height = (scroll_count + 1) * VIEWPORT_HEIGHT
    
    # Change viewport to the full height
    await page.set_viewport_size({"width": VIEWPORT_WIDTH, "height": total_height})
    
    # Scroll back to top to ensure we capture from the start
    await page.mouse.wheel(0, -total_height)
    await asyncio.sleep(1) # Give it time to settle after resize
    
    # Take the final screenshot
    final_screenshot_bytes = await page.screenshot(full_page=True, type="jpeg", quality=JPEG_QUALITY)
    return final_screenshot_bytes

def _extract_metadata(html_content: str) -> Dict[str, Any]:
    """Extract metadata (title, description, open graph) from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    metadata: Dict[str, Any] = {}
    
    # Extract title
    title_tag = soup.find('title')
    if title_tag and title_tag.string:
        metadata['title'] = title_tag.string.strip()
        
    # Extract meta tags
    for meta in soup.find_all('meta'):
        name = meta.get('name') or meta.get('property')
        content = meta.get('content')
        if name and content:
            metadata[name] = content.strip()
            
    return metadata

def _to_markdown(html_content: str, only_main_content: bool = True) -> str:
    """Convert HTML content to clean Markdown."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    if only_main_content:
        # Strip out common noise elements
        for element in soup.find_all(['nav', 'header', 'footer', 'aside', 'script', 'style', 'noscript']):
            element.decompose()
            
        # Try to find main content block
        main_block = soup.find('main') or soup.find(id='main-content') or soup.find(class_='main-content')
        if main_block:
            soup = main_block
            
    return md(str(soup), heading_style="ATX", strip=['a', 'img']).strip()
