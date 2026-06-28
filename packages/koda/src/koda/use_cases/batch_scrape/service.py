import asyncio
import base64
import uuid
from typing import Dict, List, Any

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter

from koda.client import KodaClient
from koda.config.main import settings
from koda.modules.file.service import upload, generate_presigned_url
from koda.utils import sanitize_filename
from koda.use_cases.service import execute_actions
from koda.utils.webhook.service import webhook_dispatch
from koda.use_cases.scrape.schema import ScrapeRequest, ScrapeResponse
from .schema import BatchScrapeRequest, BatchScrapeResponse

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
        await execute_actions(page, actions, self.action_results[url_key])
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
            
        async with KodaClient(s3_resource=self.request.s3_resource) as client:
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

@webhook_dispatch
async def batch_scrape(request: BatchScrapeRequest) -> BatchScrapeResponse:
    job = BatchScrapeJob(request)
    
    try:
        response = await asyncio.wait_for(
            job.run(),
            timeout=request.timeout / 1000.0 if request.timeout else settings.timeout / 1000.0
        )
        
        if settings.s3 and response.data:
            for s_resp in response.data:
                if getattr(s_resp, "_screenshot_bytes", None):
                    screenshot_bytes = s_resp._screenshot_bytes
                    object_name = f"{sanitize_filename(s_resp.url)}_{uuid.uuid4().hex[:8]}.jpg"
                    
                    await asyncio.to_thread(
                        upload,
                        data=screenshot_bytes,
                        object_name=object_name,
                        mimetype="image/jpeg"
                    )
                    
                    s_resp.screenshot = generate_presigned_url(
                        object_name=object_name
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
