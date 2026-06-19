"""Extraction logic for processing web pages."""

from __future__ import annotations

import json
import asyncio
import base64
import uuid
from typing import Dict, Any, Optional

from crawl4ai import BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter

from koda.modules.page.schema import ScrapeRequest, ScrapeResponse, BatchScrapeRequest, BatchScrapeResponse
from koda.modules.file import service as file
from koda.modules.webhook.utils import dispatch_webhook
from koda.config.main import settings
from koda.utils import sanitize_filename
from koda.modules.browser.service import BrowserSession
from koda.integrations.crawl4ai import Crawl4AiTool

__all__ = ["scrape", "batch_scrape"]

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
            
        async with BrowserSession() as context:
            tool = Crawl4AiTool(browser_config=browser_config)
            
            result = await tool.execute(context, {
                "url": self.request.url,
                "run_config": run_config,
                "hook": self.execute_actions_hook
            })
            
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


class BatchScrapeJob:
    """Encapsulates the scraping logic and state for a batch of pages."""

    def __init__(self, request: BatchScrapeRequest):
        self.request = request
        self.action_results: Dict[str, Dict[str, list]] = {}
        
    def _init_url_action_results(self, url: str):
        if url not in self.action_results:
            self.action_results[url] = {
                "screenshots": [],
                "scrapes": [],
                "javascriptReturns": [],
                "pdfs": []
            }

    async def execute_actions_hook(self, page, context, **kwargs):
        """Hook to execute Firecrawl actions on the Playwright page before extraction."""
        if not self.request.actions:
            return page

        # page.url might be 'about:blank' initially if navigated differently,
        # but in crawl4ai hook 'before_retrieve_html' it should be the target URL.
        # We use a fallback if page.url is not meaningful, but it should be.
        url_key = page.url
        self._init_url_action_results(url_key)

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
                        self.action_results[url_key]["javascriptReturns"].append({
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
                        self.action_results[url_key]["screenshots"].append(f"data:image/{'jpeg' if action.quality else 'png'};base64,{b64_shot}")
                
                elif action.type == "pdf":
                    pdf_bytes = await page.pdf(
                        format=action.format or "Letter",
                        landscape=action.landscape or False,
                        scale=action.scale or 1.0
                    )
                    if pdf_bytes:
                        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
                        self.action_results[url_key]["pdfs"].append(f"data:application/pdf;base64,{b64_pdf}")
                    
                elif action.type == "scrape":
                    html = await page.content()
                    self.action_results[url_key]["scrapes"].append({
                        "url": page.url,
                        "html": html
                    })
                    
            except Exception as e:
                print(f"Action {action.type} failed for {url_key}: {str(e)}")

        return page

    async def run(self) -> BatchScrapeResponse:
        batch_id = uuid.uuid4().hex
        response = BatchScrapeResponse(
            success=True,
            id=batch_id,
            results=[],
            invalid_urls=[]
        )
        
        valid_urls = []
        for u in self.request.urls:
            if not u.startswith("http") and not u.startswith("file://"):
                # Simplistic invalid check, normally handled gracefully or by ignoring
                if self.request.ignore_invalid_urls:
                    response.invalid_urls.append(u)
                else:
                    valid_urls.append(u)
            else:
                valid_urls.append(u)
                
        if not valid_urls:
            response.success = False
            return response

        browser_config = BrowserConfig(
            headless=True
        )
        
        run_config = CrawlerRunConfig(
            page_timeout=self.request.timeout,
            screenshot="screenshot" in self.request.formats
        )
        
        if self.request.max_concurrency:
            run_config.semaphore_count = self.request.max_concurrency
            
        if self.request.only_main_content:
            run_config.content_filter = PruningContentFilter()
            
        async with BrowserSession() as context:
            tool = Crawl4AiTool(browser_config=browser_config)
            
            results = await tool.execute(context, {
                "urls": valid_urls,
                "run_config": run_config,
                "hook": self.execute_actions_hook
            })
            
            for res in results:
                s_resp = ScrapeResponse(url=res.url)
                if not res.success:
                    s_resp.error = res.error_message
                else:
                    if "metadata" in self.request.formats:
                        s_resp.metadata = res.metadata
                    if "markdown" in self.request.formats:
                        s_resp.markdown = res.markdown
                    if "html" in self.request.formats or "rawHtml" in self.request.formats:
                        s_resp.html = res.html
                    if "links" in self.request.formats:
                        s_resp.links = res.links
                    if "images" in self.request.formats:
                        s_resp.images = res.media.get("images", []) if res.media else []
                    if "screenshot" in self.request.formats and res.screenshot:
                        s_resp._screenshot_bytes = base64.b64decode(res.screenshot)
                        
                    # Find action results matching this URL
                    # Exact URL match might be tricky due to redirects,
                    # so we try to find the closest match or the exact match.
                    match_url = res.url
                    if match_url in self.action_results and any(self.action_results[match_url].values()):
                        s_resp.action_results = self.action_results[match_url]
                    else:
                        # try to find by redirected_url or just fallback
                        for u_key, acts in self.action_results.items():
                            if u_key == res.redirected_url or u_key.rstrip("/") == res.url.rstrip("/"):
                                if any(acts.values()):
                                    s_resp.action_results = acts
                                break

                response.results.append(s_resp)
                
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

async def _execute_batch_scrape_job(request: BatchScrapeRequest) -> BatchScrapeResponse:
    job = BatchScrapeJob(request)
    return await job.run()

async def batch_scrape(request: BatchScrapeRequest) -> BatchScrapeResponse:
    """Scrape a batch of URLs concurrently.
    
    Args:
        request: Configuration and targets for the batch scraping job.
        
    Returns:
        A BatchScrapeResponse containing the results for all requested URLs.
    """
    effective_timeout = request.timeout or settings.timeout
    request.timeout = effective_timeout
    
    try:
        response = await asyncio.wait_for(
            _execute_batch_scrape_job(request),
            timeout=effective_timeout / 1000.0  # Overall timeout for the whole batch
        )
        
        # File Domain handles persistence side-effects
        if request.s3_config and response.results:
            for s_resp in response.results:
                if hasattr(s_resp, "_screenshot_bytes"):
                    screenshot_bytes = getattr(s_resp, "_screenshot_bytes")
                    object_name = f"{sanitize_filename(s_resp.url)}_{uuid.uuid4().hex[:8]}.jpg"
                    
                    await asyncio.to_thread(
                        file.upload,
                        data=screenshot_bytes,
                        object_name=object_name,
                        mimetype="image/jpeg",
                        s3_config=request.s3_config
                    )
                    
                    s_resp.screenshot = file.generate_presigned_url(
                        object_name=object_name,
                        s3_config=request.s3_config
                    )
        
        # Webhook Domain handles outbound notifications
        if request.webhook:
            payload = {
                "success": response.success,
                "id": response.id,
                "invalid_urls": response.invalid_urls,
                "data": [r.model_dump(exclude_none=True) for r in response.results] if response.results else []
            }
            await dispatch_webhook(request.webhook, "batch_scrape.completed", payload)
            
        return response
        
    except asyncio.TimeoutError:
        error_msg = f"Batch scrape operation timed out after {effective_timeout}ms"
        error_response = BatchScrapeResponse(success=False, id=uuid.uuid4().hex, results=[])
        if request.webhook:
            await dispatch_webhook(request.webhook, "batch_scrape.failed", {"success": False, "error": error_msg})
        return error_response
    except Exception as e:
        print(f"BATCH SCRAPE EXCEPTION: {e}")
        error_response = BatchScrapeResponse(success=False, id=uuid.uuid4().hex, results=[])
        if request.webhook:
            await dispatch_webhook(request.webhook, "batch_scrape.failed", {"success": False, "error": str(e)})
        return error_response
    except Exception as e:
        error_response = ScrapeResponse(url=request.url, error=str(e))
        if request.webhook:
            await dispatch_webhook(request.webhook, "scrape.failed", {"success": False, "error": str(e)})
        return error_response
