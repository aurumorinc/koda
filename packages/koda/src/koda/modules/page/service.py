"""Extraction logic for processing web pages."""

from __future__ import annotations

import json
import asyncio
import base64
import uuid
from typing import Dict, Any, Optional

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter

from koda.modules.page.schema import ScrapeRequest, ScrapeResponse
from koda.modules.file import service as file
from koda.modules.webhook.utils import dispatch_webhook
from koda.config.main import settings
from koda.utils import sanitize_filename

__all__ = ["scrape"]

class ScrapeJob:
    """Encapsulates the scraping logic and state for a single page."""

    def __init__(self, request: ScrapeRequest):
        self.request = request
        self.action_results: Dict[str, list] = {
            "screenshots": [],
            "scrapes": [],
            "javascriptReturns": [],
            "pdfs": []
        }

    async def execute_actions_hook(self, page, context, **kwargs):
        """Hook to execute Firecrawl actions on the Playwright page before extraction."""
        if not self.request.actions:
            return page

        for action in self.request.actions:
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
                        await page.keyboard.type(action.text)
                
                elif action.type == "press":
                    if action.key:
                        await page.keyboard.press(action.key)
                
                elif action.type == "scroll":
                    direction = action.direction or "down"
                    if action.selector:
                        await page.evaluate(f"""
                            const el = document.querySelector('{action.selector}');
                            if (el) {{
                                el.scrollBy(0, {1000 if direction == 'down' else -1000});
                            }}
                        """)
                    else:
                        await page.evaluate(f"window.scrollBy(0, {1000 if direction == 'down' else -1000})")
                
                elif action.type == "executeJavascript":
                    if action.script:
                        result = await page.evaluate(action.script)
                        self.action_results["javascriptReturns"].append({
                            "type": str(type(result).__name__),
                            "value": result
                        })
                
                elif action.type == "screenshot":
                    clip = None
                    if action.viewport and "width" in action.viewport and "height" in action.viewport:
                        clip = {"x": 0, "y": 0, "width": action.viewport["width"], "height": action.viewport["height"]}
                    
                    shot_bytes = await page.screenshot(
                        full_page=action.fullPage or False,
                        quality=action.quality,
                        type="jpeg" if action.quality else "png",
                        clip=clip
                    )
                    if shot_bytes:
                        b64_shot = base64.b64encode(shot_bytes).decode("utf-8")
                        self.action_results["screenshots"].append(f"data:image/{'jpeg' if action.quality else 'png'};base64,{b64_shot}")
                
                elif action.type == "pdf":
                    pdf_bytes = await page.pdf(
                        format=action.format or "Letter",
                        landscape=action.landscape or False,
                        scale=action.scale or 1.0
                    )
                    if pdf_bytes:
                        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
                        self.action_results["pdfs"].append(f"data:application/pdf;base64,{b64_pdf}")
                    
                elif action.type == "scrape":
                    html = await page.content()
                    url = page.url
                    self.action_results["scrapes"].append({
                        "url": url,
                        "html": html
                    })
                    
            except Exception as e:
                print(f"Action {action.type} failed: {str(e)}")

        return page

    async def run(self) -> ScrapeResponse:
        """Execute the scrape job and return the response."""
        response = ScrapeResponse(url=self.request.url)
        
        browser_config = BrowserConfig(
            headless=True
        )
        
        run_config = CrawlerRunConfig(
            page_timeout=self.request.timeout,
            screenshot="screenshot" in self.request.formats
        )
        
        if self.request.only_main_content:
            run_config.content_filter = PruningContentFilter()
            
        async with AsyncWebCrawler(config=browser_config) as crawler:
            crawler.crawler_strategy.set_hook("before_retrieve_html", self.execute_actions_hook)
            
            result = await crawler.arun(
                url=self.request.url,
                config=run_config
            )
            
            if not result.success:
                response.error = result.error_message
                return response
                
            if "metadata" in self.request.formats:
                response.metadata = result.metadata
                
            if "markdown" in self.request.formats:
                response.markdown = result.markdown
                
            if "html" in self.request.formats or "rawHtml" in self.request.formats:
                response.html = result.html
                
            if "links" in self.request.formats:
                response.links = result.links
                
            if "images" in self.request.formats:
                response.images = result.media.get("images", []) if result.media else []
                
            if "screenshot" in self.request.formats and result.screenshot:
                screenshot_bytes = base64.b64decode(result.screenshot)
                setattr(response, "_screenshot_bytes", screenshot_bytes)
                
            if any(self.action_results.values()):
                response.action_results = self.action_results
                
        return response


async def _execute_scrape_job(request: ScrapeRequest) -> ScrapeResponse:
    """Extract data from a URL based on requested options using crawl4ai.
    
    This function orchestrates the extraction of markdown, metadata, and screenshots.
    It returns a ScrapeResponse containing the extracted data.
    """
    job = ScrapeJob(request)
    return await job.run()

async def scrape(request: ScrapeRequest) -> ScrapeResponse:
    """Scrape a URL or local file and extract the requested domains.
    
    Args:
        request: Configuration and target for the scraping job.
        
    Returns:
        A ScrapeResponse containing the requested data.
    """
    effective_timeout = request.timeout or settings.timeout
    request.timeout = effective_timeout
    
    try:
        response = await asyncio.wait_for(
            _execute_scrape_job(request),
            timeout=effective_timeout / 1000.0
        )
        
        # File Domain handles persistence side-effects
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
        
        # Webhook Domain handles outbound notifications
        if request.webhook:
            payload = {"success": True, "data": {}}
            if response.markdown: payload["data"]["markdown"] = response.markdown
            if response.html: payload["data"]["html"] = response.html
            if response.links: payload["data"]["links"] = response.links
            if response.images: payload["data"]["images"] = response.images
            if response.metadata: payload["data"]["metadata"] = response.metadata
            if response.screenshot: payload["data"]["screenshot"] = response.screenshot
            await dispatch_webhook(request.webhook, "scrape.completed", payload)
            
        return response
        
    except asyncio.TimeoutError:
        error_msg = f"Scrape operation timed out after {effective_timeout}ms"
        error_response = ScrapeResponse(url=request.url, error=error_msg)
        if request.webhook:
            await dispatch_webhook(request.webhook, "scrape.failed", {"success": False, "error": error_msg})
        return error_response
    except Exception as e:
        error_response = ScrapeResponse(url=request.url, error=str(e))
        if request.webhook:
            await dispatch_webhook(request.webhook, "scrape.failed", {"success": False, "error": str(e)})
        return error_response
