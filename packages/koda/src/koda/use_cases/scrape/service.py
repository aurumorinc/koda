import asyncio
import base64
import uuid
from typing import Dict, Any

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter

from koda.client import KodaClient
from koda.config.main import settings
from oort.file.main import File
from koda.utils import sanitize_filename
from oort.webhook.service import webhook_dispatch
from koda.modules.page.service import execute_actions
from koda.use_cases.scrape.schema import ScrapeRequest, ScrapeResponse, ScrapeResult
from typing import Optional


class ScrapeJob:
    def __init__(self, request: ScrapeRequest):
        self.request = request
        self.action_results: Dict[str, list] = {
            "screenshots": [],
            "scrapes": [],
            "javascriptReturns": [],
            "pdfs": [],
            "errors": [],
        }

    async def execute_actions_hook(self, page, context, **kwargs):
        if not self.request.actions:
            return page
        await execute_actions(page, self.request.actions, self.action_results)
        return page

    async def run(self) -> ScrapeResponse:
        response = ScrapeResponse(url=self.request.url)

        browser_kwargs = {
            "headless": True,
            "viewport_width": 1366,
            "viewport_height": 768,
        }
        browser_config = BrowserConfig(**browser_kwargs)  # type: ignore

        has_screenshot = any(
            f == "screenshot" or (isinstance(f, dict) and f.get("type") == "screenshot")
            for f in self.request.formats
        )
        run_kwargs = {
            "page_timeout": self.request.timeout,
            "screenshot": has_screenshot,
        }
        run_config = CrawlerRunConfig(**run_kwargs)  # type: ignore

        if self.request.only_main_content:
            run_config.content_filter = PruningContentFilter()

        async with KodaClient() as client:
            async with AsyncWebCrawler(client=client, config=browser_config) as crawler:
                if self.request.actions:
                    crawler.crawler_strategy.set_hook(  # type: ignore[missing-attribute]
                        "before_retrieve_html", self.execute_actions_hook
                    )  # type: ignore

                result = await crawler.arun(url=self.request.url, config=run_config)

                if not result.success:
                    response.error = result.error_message
                    return response

                if "metadata" in self.request.formats:
                    response.metadata = result.metadata

                if "markdown" in self.request.formats:
                    md_obj = result.markdown
                    response.markdown = (
                        getattr(md_obj, "fit_markdown", "")
                        or getattr(md_obj, "raw_markdown", "")
                        or str(md_obj)
                        if md_obj
                        else None
                    )

                if "html" in self.request.formats or "rawHtml" in self.request.formats:
                    response.html = result.html

                if "links" in self.request.formats:
                    response.links = result.links

                if "images" in self.request.formats:
                    response.images = (
                        result.media.get("images", []) if result.media else []
                    )

                if "_format_screenshot_bytes" in self.action_results:
                    setattr(
                        response,
                        "_screenshot_bytes",
                        self.action_results["_format_screenshot_bytes"],
                    )
                else:
                    has_screenshot_format = any(
                        f == "screenshot"
                        or (isinstance(f, dict) and f.get("type") == "screenshot")
                        for f in self.request.formats
                    )
                    if has_screenshot_format and result.screenshot:
                        screenshot_bytes = base64.b64decode(result.screenshot)
                        setattr(response, "_screenshot_bytes", screenshot_bytes)

                if any(self.action_results.values()):
                    response.action_results = self.action_results

        return response


@webhook_dispatch(event_prefix="scrape")
async def _scrape_dispatched(request: ScrapeRequest, webhook: Optional[dict] = None) -> ScrapeResult:
    job = ScrapeJob(request)
    try:
        response = await asyncio.wait_for(
            job.run(),
            timeout=request.timeout / 1000.0
            if request.timeout
            else settings.timeout / 1000.0,
        )
        if response.error:
            return ScrapeResult(success=False, error=response.error)

        if getattr(response, "_screenshot_bytes", None):
            screenshot_bytes = response._screenshot_bytes
            object_name = f"{sanitize_filename(request.url)}_{uuid.uuid4().hex[:8]}.jpg"

            f = File.from_bytes(screenshot_bytes, object_name, "image/jpeg")
            response.screenshot = await f.presigned_url  # type: ignore[not-async]

        data: Dict[str, Any] = {}
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

async def scrape(request: ScrapeRequest) -> ScrapeResult:
    webhook_dict = request.webhook.model_dump() if request.webhook else None
    return await _scrape_dispatched(request, webhook=webhook_dict)
