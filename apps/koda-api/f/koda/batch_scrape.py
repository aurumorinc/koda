# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.4.2#subdirectory=packages/koda",
# ]
# ///
import asyncio
import base64
import uuid
import wmill  # type: ignore
from typing import Optional, List, Dict, Any, Union, cast
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
    webhook_dispatch
)

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
    formats: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: cast(List[Union[str, Dict[str, Any]]], ["markdown", "screenshot"]))
    only_main_content: bool = Field(default=True, alias="onlyMainContent")
    actions: List[Action] = Field(default_factory=list)
    timeout: Optional[int] = None

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

class BatchScrapeRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    urls: Optional[List[str]] = None
    requests: Optional[List[ScrapeRequest]] = None
    formats: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: cast(List[Union[str, Dict[str, Any]]], ["markdown", "screenshot"]))
    only_main_content: bool = Field(default=True, alias="onlyMainContent")
    actions: List[Action] = Field(default_factory=list)
    timeout: Optional[int] = None
    s3_config: Optional[Dict[str, Any]] = None
    webhook: Optional[Webhook] = None
    max_concurrency: Optional[int] = Field(default=None, alias="maxConcurrency")
    ignore_invalid_urls: Optional[bool] = Field(default=True, alias="ignoreInvalidURLs")

class BatchScrapeResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    success: bool
    id: str
    url: Optional[str] = None
    invalid_urls: List[str] = Field(default_factory=list, alias="invalidURLs")
    data: List[ScrapeResponse] = Field(default_factory=list)

class BatchScrapeJob:
    def __init__(self, request: BatchScrapeRequest):
        self.request = request
        self.action_results: Dict[str, Dict[str, list]] = {}
        self.target_requests: Dict[str, ScrapeRequest] = {}
        if self.request.requests:
            for req in self.request.requests:
                self.target_requests[req.url] = req
        
    def _init_url_action_results(self, url: str):
        if url not in self.action_results:
            self.action_results[url] = {
                "screenshots": [],
                "scrapes": [],
                "javascriptReturns": [],
                "pdfs": [],
                "errors": []
            }

    async def execute_actions_hook(self, page, context, **kwargs):
        url_key = page.url
        
        target_req = self.target_requests.get(url_key)
        if not target_req:
            for k, r in self.target_requests.items():
                if k.rstrip("/") == url_key.rstrip("/") or (k.split("?")[0] == url_key.split("?")[0] and k in url_key):
                    target_req = r
                    break
                    
        actions = target_req.actions if target_req else self.request.actions

        if not actions:
            return page

        self._init_url_action_results(url_key)

        for action in actions:
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
                self.action_results[url_key]["errors"].append({
                    "action": action.type,
                    "error": str(e)
                })
                if hasattr(action, 'ignoreError') and action.ignoreError is False:
                    raise

        return page

    async def run(self) -> BatchScrapeResponse:
        batch_id = uuid.uuid4().hex
        response = BatchScrapeResponse(
            success=True,
            id=batch_id,
            data=[],
            invalid_urls=[]
        )
        
        valid_urls = []
        source_urls = [r.url for r in self.request.requests] if self.request.requests else (self.request.urls or [])
        for u in source_urls:
            if not u.startswith("http") and not u.startswith("file://"):
                if self.request.ignore_invalid_urls:
                    response.invalid_urls.append(u)
                else:
                    valid_urls.append(u)
            else:
                valid_urls.append(u)
                
        if not valid_urls:
            response.success = False
            return response

        browser_kwargs = {
            "headless": True,
            "viewport_width": 1366,
            "viewport_height": 768
        }
        browser_config = BrowserConfig(**browser_kwargs)  # type: ignore
        
        has_screenshot = any(
            f == "screenshot" or (isinstance(f, dict) and f.get("type") == "screenshot")
            for f in self.request.formats
        )
        run_kwargs = {
            "page_timeout": self.request.timeout,
            "screenshot": has_screenshot
        }
        run_config = CrawlerRunConfig(**run_kwargs)  # type: ignore
        
        if self.request.max_concurrency:
            run_config.semaphore_count = self.request.max_concurrency
            
        if self.request.only_main_content:
            run_config.content_filter = PruningContentFilter()
            
        async with KodaClient() as client:
            async with AsyncWebCrawler(client=client, config=browser_config) as crawler:
                if self.request.actions or (self.request.requests and any(r.actions for r in self.request.requests)):
                    crawler.crawler_strategy.set_hook("before_retrieve_html", self.execute_actions_hook)  # type: ignore
                
                res_obj = await crawler.arun_many(urls=valid_urls, config=run_config)  # type: ignore
                results: List[Any] = []
                if hasattr(res_obj, "__aiter__"):
                    results = [r async for r in res_obj]  # type: ignore
                else:
                    results = list(res_obj)  # type: ignore
                
                ordered_results = []
                for u in valid_urls:
                    found_res = next((r for r in results if r.url == u), None)
                    if not found_res:
                        found_res = next((r for r in results if r.url.rstrip('/') == u.rstrip('/') or u in r.url), None)
                    if found_res:
                        ordered_results.append(found_res)
                    else:
                        from crawl4ai.models import CrawlResult
                        dummy = CrawlResult(url=u, html="", success=False, error_message="Scrape failed or timed out without result.")
                        ordered_results.append(dummy)
                
                for res in ordered_results:
                    s_resp = ScrapeResponse(url=res.url)
                    if not res.success:
                        s_resp.error = res.error_message
                    else:
                        if "metadata" in self.request.formats:
                            s_resp.metadata = res.metadata
                        if "markdown" in self.request.formats:
                            md_obj = res.markdown
                            s_resp.markdown = getattr(md_obj, "fit_markdown", "") or getattr(md_obj, "raw_markdown", "") or str(md_obj) if md_obj else None
                        if "html" in self.request.formats or "rawHtml" in self.request.formats:
                            s_resp.html = res.html
                        if "links" in self.request.formats:
                            s_resp.links = res.links
                        if "images" in self.request.formats:
                            s_resp.images = res.media.get("images", []) if res.media else []
                            
                        match_url = res.url
                        acts_to_use = None
                        if match_url in self.action_results:
                            acts_to_use = self.action_results[match_url]
                        else:
                            for u_key, acts in self.action_results.items():
                                if u_key == getattr(res, "redirected_url", None) or u_key.rstrip("/") == res.url.rstrip("/"):
                                    acts_to_use = acts
                                    break
    
                        has_screenshot_format = any(f == "screenshot" or (isinstance(f, dict) and f.get("type") == "screenshot") for f in self.request.formats)
                        if has_screenshot_format and res.screenshot:
                            s_resp._screenshot_bytes = base64.b64decode(res.screenshot)
    
                        if acts_to_use and any(acts_to_use.values()):
                            s_resp.action_results = acts_to_use
    
                    response.data.append(s_resp)
                
        return response

async def _run_batch_scrape(request: BatchScrapeRequest) -> BatchScrapeResponse:
    job = BatchScrapeJob(request)
    
    try:
        response = await asyncio.wait_for(
            job.run(),
            timeout=request.timeout / 1000.0 if request.timeout else settings.timeout / 1000.0
        )
        
        if request.s3_config and response.data:
            from koda.modules.file.schema import S3Config
            s3_conf_obj = S3Config(**request.s3_config) if isinstance(request.s3_config, dict) else request.s3_config
            for s_resp in response.data:
                if getattr(s_resp, "_screenshot_bytes", None):
                    screenshot_bytes = s_resp._screenshot_bytes
                    object_name = f"{sanitize_filename(s_resp.url)}_{uuid.uuid4().hex[:8]}.jpg"
                    
                    await asyncio.to_thread(
                        upload,
                        data=screenshot_bytes,
                        object_name=object_name,
                        mimetype="image/jpeg",
                        s3_config=s3_conf_obj
                    )
                    
                    s_resp.screenshot = generate_presigned_url(
                        object_name=object_name,
                        s3_config=s3_conf_obj
                    )
        
        return response
        
    except asyncio.TimeoutError:
        error_msg = "Batch scrape operation timed out"
        response = BatchScrapeResponse(success=False, id=uuid.uuid4().hex, data=[])
        response.data = []
        response.success = False
        raise Exception(error_msg)
    except Exception as e:
        error_msg = str(e)
        raise Exception(error_msg)

@webhook_dispatch
async def async_main(
    urls: List[str] = [],
    requests: List[ScrapeRequest] = [],
    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
    onlyMainContent: bool = True,
    actions: List[Action] = [],
    timeout: int = 60000,
    s3_resource: Optional[str] = "f/koda/default_s3",
    webhook: Optional[Webhook] = None,
    maxConcurrency: int = 10,
    ignoreInvalidURLs: bool = True,
    **kwargs
) -> dict:
    """
    Scrape a batch of URLs concurrently using Koda infrastructure.
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
                
    request = BatchScrapeRequest(
        urls=urls,
        requests=requests,
        formats=normalized_formats,
        onlyMainContent=onlyMainContent,
        timeout=timeout or settings.timeout,
        actions=actions,
        s3_config=s3_config,
        webhook=webhook,
        maxConcurrency=maxConcurrency,
        ignoreInvalidURLs=ignoreInvalidURLs
    )
    
    try:
        response = await _run_batch_scrape(request)
        return response.model_dump(by_alias=True, exclude_none=True)
    except Exception as e:
        return {"success": False, "id": uuid.uuid4().hex, "data": [], "error": str(e)}

def main(
    urls: List[str] = [],
    requests: List[ScrapeRequest] = [],
    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
    onlyMainContent: bool = True,
    actions: List[Action] = [],
    timeout: int = 60000,
    s3_resource: Optional[str] = "f/koda/default_s3",
    webhook: Optional[Webhook] = None,
    maxConcurrency: int = 10,
    ignoreInvalidURLs: bool = True,
    **kwargs
) -> dict:
    """Synchronous entrypoint for Windmill execution."""
    return asyncio.run(async_main(
        urls=urls,
        requests=requests,
        formats=formats,
        onlyMainContent=onlyMainContent,
        actions=actions,
        timeout=timeout,
        s3_resource=s3_resource,
        webhook=webhook,
        maxConcurrency=maxConcurrency,
        ignoreInvalidURLs=ignoreInvalidURLs,
        **kwargs
    ))
