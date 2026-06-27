# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.1.0#subdirectory=packages/koda",
# ]
# ///
import asyncio
import base64
import uuid
import wmill
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, ConfigDict

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from koda import (
    KodaClient,
    Webhook,
    generate_presigned_url,
    sanitize_filename,
    settings,
    upload,
)
from koda.utils.webhook.service import webhook_dispatch

class Action(BaseModel):
    type: str
    selector: Optional[str] = None
    value: Optional[Any] = None
    milliseconds: Optional[int] = None
    text: Optional[str] = None
    key: Optional[str] = None
    script: Optional[str] = None
    direction: Optional[str] = None
    amount: Optional[int] = None
    all: Optional[bool] = None
    fullPage: Optional[bool] = None
    quality: Optional[int] = None
    viewport: Optional[Dict[str, int]] = None
    format: Optional[str] = None
    landscape: Optional[bool] = None
    scale: Optional[float] = None
    timeout: Optional[int] = None
    ignoreError: Optional[bool] = Field(default=True)

class ScrapeRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    url: str
    formats: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: ["markdown", "screenshot"])
    only_main_content: bool = Field(default=True, alias="onlyMainContent")
    actions: List[Action] = Field(default_factory=list)
    timeout: Optional[int] = None
    s3_config: Optional[Dict[str, Any]] = None
    webhook: Optional[Webhook] = None

class ScrapeResponse(BaseModel):
    url: str
    markdown: Optional[str] = None
    html: Optional[str] = None
    links: Optional[Dict[str, Any]] = None
    images: Optional[List[Dict[str, Any]]] = None
    screenshot: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    action_results: Optional[Dict[str, Any]] = None
    _screenshot_bytes: Optional[bytes] = None

class ScrapeResult(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ScrapeJob:
    def __init__(self, request: ScrapeRequest):
        self.request = request
        self.action_results: Dict[str, list] = {
            "screenshots": [],
            "scrapes": [],
            "javascriptReturns": [],
            "pdfs": [],
            "errors": []
        }

    async def execute_actions_hook(self, page, context, **kwargs):
        if not self.request.actions:
            return page

        for action in self.request.actions:
            try:
                if action.type == "wait":
                    if action.milliseconds:
                        await asyncio.sleep(action.milliseconds / 1000.0)
                    elif action.selector:
                        kwargs_wait = {}
                        if action.timeout is not None:
                            kwargs_wait["timeout"] = action.timeout
                        await page.wait_for_selector(action.selector, **kwargs_wait)
                
                elif action.type == "click":
                    kwargs_click = {}
                    if action.timeout is not None:
                        kwargs_click["timeout"] = action.timeout
                    if action.selector:
                        if action.all:
                            elements = await page.query_selector_all(action.selector)
                            for el in elements:
                                await el.click(**kwargs_click)
                        else:
                            await page.click(action.selector, **kwargs_click)
                
                elif action.type == "write":
                    if action.text:
                        await page.keyboard.type(action.text)
                
                elif action.type == "press":
                    if action.key:
                        await page.keyboard.press(action.key)
                
                elif action.type == "scroll":
                    direction = action.direction or "down"
                    amount = action.amount or 1000
                    if action.selector:
                        await page.evaluate(f"""
                            const el = document.querySelector('{action.selector}');
                            if (el) {{
                                el.scrollBy(0, {amount if direction == 'down' else -amount});
                            }}
                        """)
                    else:
                        await page.mouse.wheel(0, amount if direction == 'down' else -amount)
                
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
                self.action_results["errors"].append({
                    "action": action.type,
                    "error": str(e)
                })
                if hasattr(action, 'ignoreError') and action.ignoreError is False:
                    raise

        return page

    async def run(self) -> ScrapeResponse:
        response = ScrapeResponse(url=self.request.url)
        
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1366,
            viewport_height=768
        )
        
        has_screenshot = any(
            f == "screenshot" or (isinstance(f, dict) and f.get("type") == "screenshot")
            for f in self.request.formats
        )
        run_config = CrawlerRunConfig(
            page_timeout=self.request.timeout,
            screenshot=has_screenshot
        )
        
        if self.request.only_main_content:
            run_config.content_filter = PruningContentFilter()
            
        async with KodaClient() as client:
            async with AsyncWebCrawler(client=client, config=browser_config) as crawler:
                if self.request.actions:
                    crawler.crawler_strategy.set_hook("before_retrieve_html", self.execute_actions_hook)
                
                result = await crawler.arun(url=self.request.url, config=run_config)
                
                if not result.success:
                    response.error = result.error_message
                    return response
                    
                if "metadata" in self.request.formats:
                    response.metadata = result.metadata
                    
                if "markdown" in self.request.formats:
                    md_obj = result.markdown
                    response.markdown = getattr(md_obj, "fit_markdown", "") or getattr(md_obj, "raw_markdown", "") or str(md_obj) if md_obj else None
                    
                if "html" in self.request.formats or "rawHtml" in self.request.formats:
                    response.html = result.html
                    
                if "links" in self.request.formats:
                    response.links = result.links
                    
                if "images" in self.request.formats:
                    response.images = result.media.get("images", []) if result.media else []
                    
                if "_format_screenshot_bytes" in self.action_results:
                    setattr(response, "_screenshot_bytes", self.action_results["_format_screenshot_bytes"])
                else:
                    has_screenshot_format = any(f == "screenshot" or (isinstance(f, dict) and f.get("type") == "screenshot") for f in self.request.formats)
                    if has_screenshot_format and result.screenshot:
                        screenshot_bytes = base64.b64decode(result.screenshot)
                        setattr(response, "_screenshot_bytes", screenshot_bytes)
                    
                if any(self.action_results.values()):
                    response.action_results = self.action_results
                    
        return response

async def _run_scrape(request: ScrapeRequest) -> ScrapeResult:
    job = ScrapeJob(request)
    try:
        response = await asyncio.wait_for(
            job.run(),
            timeout=request.timeout / 1000.0 if request.timeout else settings.timeout / 1000.0
        )
        if response.error:
            return ScrapeResult(success=False, error=response.error)
            
        if getattr(response, "_screenshot_bytes", None) and request.s3_config:
            from koda.modules.file.schema import S3Config
            s3_conf_obj = S3Config(**request.s3_config) if isinstance(request.s3_config, dict) else request.s3_config
            screenshot_bytes = response._screenshot_bytes
            object_name = f"{sanitize_filename(request.url)}_{uuid.uuid4().hex[:8]}.jpg"
            
            await asyncio.to_thread(
                upload,
                data=screenshot_bytes,
                object_name=object_name,
                mimetype="image/jpeg",
                s3_config=s3_conf_obj
            )
            
            response.screenshot = generate_presigned_url(
                object_name=object_name,
                s3_config=s3_conf_obj
            )
            
        data = {}
        if response.markdown is not None:
            data["markdown"] = response.markdown
        if response.html is not None:
            data["html"] = response.html
        if response.links is not None:
            data["links"] = response.links
        if response.images is not None:
            data["images"] = response.images
        if response.metadata is not None:
            data["metadata"] = response.metadata
        if response.screenshot is not None:
            data["screenshot"] = response.screenshot
        if response.action_results is not None:
            data["actions"] = response.action_results
            
        return ScrapeResult(success=True, data=data)
    except asyncio.TimeoutError:
        error_msg = "Scrape operation timed out"
        return ScrapeResult(success=False, error=error_msg)
    except Exception as e:
        error_msg = str(e)
        return ScrapeResult(success=False, error=error_msg)

@webhook_dispatch
async def main(
    url: str,
    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
    onlyMainContent: bool = True,
    actions: List[Action] = [],
    timeout: int = 60000,
    s3_resource: Optional[str] = "f/koda/default_s3",
    webhook: Optional[Webhook] = None,
    **kwargs
) -> dict:
    """
    Scrape a single URL and extract information using Koda infrastructure.
    """
    s3_config = None
    if s3_resource:
        s3_config = wmill.get_resource(s3_resource)
        if not s3_config:
            return {"success": False, "error": f"S3 Resource '{s3_resource}' not found."}

    normalized_formats = []
    if formats:
        for f in formats:
            if isinstance(f, dict):
                normalized_formats.append(f.get("type", ""))
            else:
                normalized_formats.append(str(f))
                
    request = ScrapeRequest(
        url=url,
        formats=normalized_formats,
        onlyMainContent=onlyMainContent,
        timeout=timeout or settings.timeout,
        actions=actions,
        s3_config=s3_config,
        webhook=webhook
    )

    try:
        result = await _run_scrape(request)
        return result.model_dump(by_alias=True, exclude_none=True)
    except Exception as e:
        return {"success": False, "error": str(e)}

def _run_main_sync(*args, **kwargs):
    return asyncio.run(main(*args, **kwargs))
