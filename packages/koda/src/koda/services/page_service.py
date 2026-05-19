"""Extraction logic for processing web pages."""

from __future__ import annotations

import json
import asyncio
import base64
from typing import Dict, Any, Optional

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter

from koda.schemas.page_schema import ScrapeRequest, ScrapeResponse

__all__ = ["scrape"]

async def _execute_actions_hook(page, context, **kwargs):
    """Hook to execute Firecrawl actions on the Playwright page before extraction."""
    request: ScrapeRequest = kwargs.get("request")
    if not request or not request.actions:
        return page

    action_results = {
        "screenshots": [],
        "scrapes": [],
        "javascriptReturns": [],
        "pdfs": []
    }

    for action in request.actions:
        try:
            if action.type == "wait":
                if action.milliseconds:
                    await asyncio.sleep(action.milliseconds / 1000.0)
                elif action.selector:
                    await page.wait_for_selector(action.selector)
            
            elif action.type == "click":
                if action.selector:
                    if action.all:
                        elements = await page.query_selector_all(action.selector)
                        for el in elements:
                            await el.click()
                    else:
                        await page.click(action.selector)
            
            elif action.type == "write":
                if action.text:
                    # Firecrawl says: "Note: You must first focus the element using a 'click' action before writing."
                    # But we can just use keyboard.type if focused, or fill if we have a selector.
                    # Since Firecrawl's write action doesn't have a selector in the spec (wait, let me check the spec).
                    # Spec: "Write text into an input field... Note: You must first focus the element using a 'click' action before writing."
                    # So we just type on the currently focused element.
                    await page.keyboard.type(action.text)
            
            elif action.type == "press":
                if action.key:
                    await page.keyboard.press(action.key)
            
            elif action.type == "scroll":
                direction = action.direction or "down"
                if action.selector:
                    # Scroll a specific element
                    await page.evaluate(f"""
                        const el = document.querySelector('{action.selector}');
                        if (el) {{
                            el.scrollBy(0, {1000 if direction == 'down' else -1000});
                        }}
                    """)
                else:
                    # Scroll the window
                    await page.evaluate(f"window.scrollBy(0, {1000 if direction == 'down' else -1000})")
            
            elif action.type == "executeJavascript":
                if action.script:
                    result = await page.evaluate(action.script)
                    action_results["javascriptReturns"].append({
                        "type": str(type(result).__name__),
                        "value": result
                    })
            
            elif action.type == "screenshot":
                # Capture screenshot
                clip = None
                if action.viewport and "width" in action.viewport and "height" in action.viewport:
                    clip = {"x": 0, "y": 0, "width": action.viewport["width"], "height": action.viewport["height"]}
                
                shot_bytes = await page.screenshot(
                    full_page=action.fullPage or False,
                    quality=action.quality,
                    type="jpeg" if action.quality else "png",
                    clip=clip
                )
                # Store as base64
                b64_shot = base64.b64encode(shot_bytes).decode("utf-8")
                action_results["screenshots"].append(f"data:image/{'jpeg' if action.quality else 'png'};base64,{b64_shot}")
            
            elif action.type == "pdf":
                pdf_bytes = await page.pdf(
                    format=action.format or "Letter",
                    landscape=action.landscape or False,
                    scale=action.scale or 1.0
                )
                b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
                action_results["pdfs"].append(f"data:application/pdf;base64,{b64_pdf}")
                
            elif action.type == "scrape":
                html = await page.content()
                url = page.url
                action_results["scrapes"].append({
                    "url": url,
                    "html": html
                })
                
        except Exception as e:
            # Firecrawl typically continues or fails depending on the action, we'll log and continue
            print(f"Action {action.type} failed: {str(e)}")

    # Store results in kwargs so we can retrieve them later
    if "shared_state" in kwargs:
        kwargs["shared_state"]["action_results"] = action_results
    return page

async def scrape(request: ScrapeRequest) -> ScrapeResponse:
    """Extract data from a URL based on requested options using crawl4ai.
    
    This function orchestrates the extraction of markdown, metadata, and screenshots.
    It returns a ScrapeResponse containing the extracted data.
    """
    response = ScrapeResponse(url=request.url)
    
    browser_config = BrowserConfig(
        headless=True
    )
    
    run_config = CrawlerRunConfig(
        page_timeout=request.timeout,
        screenshot="screenshot" in request.formats
    )
    
    if request.only_main_content:
        run_config.content_filter = PruningContentFilter()
        
    # We use a dictionary to pass state between the hook and this function
    shared_state = {"request": request}
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Register the hook
        crawler.crawler_strategy.set_hook("before_retrieve_html", _execute_actions_hook)
        
        result = await crawler.arun(
            url=request.url, 
            config=run_config,
            shared_state=shared_state
        )
        
        if not result.success:
            response.error = result.error_message
            return response
            
        if "metadata" in request.formats:
            response.metadata = result.metadata
            
        if "markdown" in request.formats:
            response.markdown = result.markdown
            
        if "html" in request.formats or "rawHtml" in request.formats:
            response.html = result.html
            
        if "links" in request.formats:
            response.links = result.links
            
        if "images" in request.formats:
            response.images = result.media.get("images", []) if result.media else []
            
        if "screenshot" in request.formats and result.screenshot:
            # We attach the bytes to the response object temporarily for the client to handle S3 upload.
            screenshot_bytes = base64.b64decode(result.screenshot)
            setattr(response, "_screenshot_bytes", screenshot_bytes)
            
        # Attach action results if any
        if "action_results" in shared_state:
            response.action_results = shared_state["action_results"]
            
    return response
