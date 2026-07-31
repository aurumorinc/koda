# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.19.0#subdirectory=packages/koda",
# ]
# ///
import os

try:
    import wmill  # type: ignore
    _s3 = wmill.get_resource("f/koda/default_s3")
    if _s3:
        os.environ["S3_BUCKET"] = _s3.get("bucket", "")
        os.environ["S3_ENDPOINT_URL"] = _s3.get("endPoint", "")
        os.environ["S3_REGION"] = _s3.get("region", "")
        os.environ["S3_ACCESS_KEY"] = _s3.get("accessKey", "")
        os.environ["S3_SECRET_KEY"] = _s3.get("secretKey", "")
except Exception:
    pass

import asyncio
import base64
import uuid
from contextlib import suppress
from datetime import timedelta
from typing import Any, Dict, List, Optional, Union, cast

from pydantic import BaseModel, ConfigDict, Field
from crawlee import Request
from crawlee.crawlers import PlaywrightCrawlingContext, PlaywrightCrawler

from koda.client import KodaClient
from koda.exceptions import BrowserLaunchError, TimeoutError
from koda.modules.page.service import screenshot, scroll_to
from oort.file.main import File
from oort.webhook.schema import WebhookRequest as Webhook
from oort.webhook.service import webhook_dispatch


class ScrapeYoutubeProfileRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    url: str
    formats: List[Union[str, Dict[str, Any]]] = Field(
        default_factory=lambda: cast(List[Union[str, Dict[str, Any]]], ["markdown"])
    )
    timeout: int = 300000
    viewport: Dict[str, int] = Field(
        default_factory=lambda: {"width": 1366, "height": 768}
    )
    max_scroll_y: int = Field(default=3072, alias="maxScrollY")
    max_screenshot_height: int = Field(default=10000, alias="maxScreenshotHeight")
    webhook: Optional[Webhook] = None


class ScrapeYoutubeProfileResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


CHANNEL_PATH_PREFIXES = {"c", "user", "channel"}
TABS = [
    {"name": "home", "slug": "featured", "full_page": True},
    {"name": "videos", "slug": "videos", "full_page": False},
    {"name": "shorts", "slug": "shorts", "full_page": False},
    {"name": "live", "slug": "streams", "full_page": False},
    {"name": "podcasts", "slug": "podcasts", "full_page": False},
    {"name": "playlists", "slug": "playlists", "full_page": False},
    {"name": "posts", "slug": "posts", "full_page": False},
    {"name": "store", "slug": "store", "full_page": False},
    {"name": "courses", "slug": "courses", "full_page": False},
]


async def _push_screenshot_data(
    context: PlaywrightCrawlingContext, url: str, screenshot_bytes: bytes | str
) -> None:
    if isinstance(screenshot_bytes, str):
        screenshot_bytes = screenshot_bytes.encode("utf-8")
    await context.push_data(
        {
            "url": url,
            "screenshot_base64": base64.b64encode(screenshot_bytes).decode("utf-8"),
            "screenshot_filename": f"{uuid.uuid4().hex}.png",
        }
    )


async def _capture_about_dialog_in_place(
    context: PlaywrightCrawlingContext,
    base_profile_url: str,
    request: ScrapeYoutubeProfileRequest,
) -> None:
    page = context.page
    try:
        await page.set_viewport_size(
            {
                "width": request.viewport.get("width", 1366),
                "height": request.max_scroll_y,
            }
        )
        more_button = page.get_by_role("button").filter(has_text="...more")
        try:
            await more_button.wait_for(state="visible", timeout=5000)
            await more_button.click()
        except Exception:
            context.log.warning("No '...more' button found for About dialog.")
            return

        dialog = page.locator(
            "tp-yt-paper-dialog:has(ytd-engagement-panel-section-list-renderer[target-id='engagement-panel-about-channel']), tp-yt-paper-dialog:visible"
        ).first
        try:
            await dialog.wait_for(state="visible", timeout=5000)
            await page.wait_for_timeout(2000)
        except Exception:
            context.log.warning("About dialog did not appear.")
            return

        box = await dialog.bounding_box()
        if box:
            screenshot_bytes = await page.screenshot(clip=box)
            await _push_screenshot_data(context, f"{base_profile_url}#about", screenshot_bytes)
    except Exception as e:
        context.log.error(f"Failed to capture About dialog: {e}")
    finally:
        with suppress(Exception):
            await page.set_viewport_size(request.viewport)
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(500)


async def _handler(
    context: PlaywrightCrawlingContext, request: ScrapeYoutubeProfileRequest
) -> None:
    page = context.page

    with suppress(Exception):
        await page.wait_for_load_state("domcontentloaded", timeout=5000)

    resolved_url = page.url

    parts = resolved_url.split("/")
    if len(parts) > 4 and parts[3].startswith("@"):
        base_profile_url = "/".join(parts[:4])
    elif len(parts) > 4 and parts[3] in CHANNEL_PATH_PREFIXES:
        base_profile_url = "/".join(parts[:5])
    else:
        base_profile_url = resolved_url.split("?")[0].rstrip("/")
        for tab in TABS:
            if tab["slug"] and base_profile_url.endswith(f"/{tab['slug']}"):
                base_profile_url = base_profile_url[: -len(f"/{tab['slug']}")]
                break

    # Determine which tabs actually exist on the channel
    found_slugs = set()
    try:
        await page.wait_for_selector(
            'yt-tab-shape, tp-yt-paper-tab, [role="tab"]', timeout=3000
        )
        tab_texts = await page.evaluate("""() => {
            const tabs = Array.from(document.querySelectorAll('yt-tab-shape, tp-yt-paper-tab, [role="tab"]'));
            return tabs.map(tab => (tab.innerText || tab.textContent || '').trim().toLowerCase());
        }""")

        for text in tab_texts:
            for tab in TABS:
                if tab["name"] in text:
                    found_slugs.add(tab["slug"])
    except Exception:
        pass

    if not found_slugs:
        found_slugs = {tab["slug"] for tab in TABS}

    # 1. Capture About Dialog (In-place)
    await _capture_about_dialog_in_place(context, base_profile_url, request)

    # 2. Process Tabs (In-place SPA navigation)
    for tab in TABS:
        slug = tab["slug"]
        if slug not in found_slugs:
            continue

        tab_url = f"{base_profile_url}/{slug}"
        full_page = tab["full_page"]
        tab_name_cap = tab["name"].capitalize()

        with suppress(Exception):
            tab_locator = page.locator(
                f"yt-tab-shape:has-text('{tab_name_cap}'), tp-yt-paper-tab:has-text('{tab_name_cap}'), [role='tab']:has-text('{tab_name_cap}'), yt-tab-shape:has-text('{tab['name']}'), [role='tab']:has-text('{tab['name']}')"
            ).first
            if await tab_locator.is_visible(timeout=1000):
                await tab_locator.click()
            else:
                await page.evaluate(f"window.location.href = '{tab_url}'")

        with suppress(Exception):
            await page.wait_for_selector(
                "ytd-rich-grid-renderer, ytd-section-list-renderer, ytd-tabbed-header-renderer",
                timeout=2000,
            )

        max_limit = (
            request.max_screenshot_height if full_page else request.max_scroll_y
        )

        await scroll_to(
            page,
            y=max_limit,
            wait_callback=lambda: page.wait_for_timeout(200),
        )

        screenshot_bytes = await screenshot(page, max_height=max_limit)

        await _push_screenshot_data(context, tab_url, screenshot_bytes)


@webhook_dispatch(event_prefix="scrape_youtube_profile")
async def amain(
    request: ScrapeYoutubeProfileRequest, webhook: Optional[Webhook] = None
) -> ScrapeYoutubeProfileResponse:
    try:
        async with KodaClient(
            timeout=request.timeout,
            substitute_pixels=False,
        ) as client:
            async def request_handler(context: PlaywrightCrawlingContext) -> None:
                await _handler(context, request)

            crawler = PlaywrightCrawler(
                client=client,  # type: ignore
                request_handler=request_handler,
                max_request_retries=3,
                request_handler_timeout=timedelta(milliseconds=request.timeout),
            )

            @crawler.pre_navigation_hook
            async def block_unnecessary_resources(context) -> None:
                # Force viewport
                await context.page.set_viewport_size(request.viewport)

                # Add consent cookies
                with suppress(Exception):
                    await context.page.context.add_cookies(
                        [
                            {
                                "name": "CONSENT",
                                "value": "YES+cb",
                                "domain": ".youtube.com",
                                "path": "/",
                            }
                        ]
                    )

            # Start Crawl
            await crawler.run([Request.from_url(url=request.url)])

            # Post Crawl Formatting
            dataset = await crawler.get_dataset()
            data = await dataset.get_data()
            items = data.items

            data_list = []

            for item in items:
                tab_data: dict = {"url": str(item.get("url", ""))}

                if "screenshot_base64" in item and "screenshot_filename" in item:
                    f = File.from_base64(
                        str(item["screenshot_base64"]),
                        str(item["screenshot_filename"]),
                        "image/png",
                    )
                    tab_data["screenshot"] = f

                data_list.append(tab_data)

            if not data_list:
                return ScrapeYoutubeProfileResponse(
                    success=False,
                    error="Scrape operation failed or timed out with no data extracted.",
                )

            return ScrapeYoutubeProfileResponse(success=True, data=data_list)

    except (TimeoutError, asyncio.TimeoutError):
        return ScrapeYoutubeProfileResponse(
            success=False, error="Scrape operation timed out"
        )
    except BrowserLaunchError as e:
        return ScrapeYoutubeProfileResponse(success=False, error=f"Browser crash: {e}")
    except Exception as e:
        return ScrapeYoutubeProfileResponse(success=False, error=str(e))


def main(
    url: str,
    formats: List[Union[str, Dict[str, Any]]] = ["screenshot"],
    timeout: int = 600000,
    viewport: Optional[Dict[str, int]] = None,
    maxScrollY: int = 3072,
    maxScreenshotHeight: int = 10000,
    webhook: Optional[Webhook] = None,
) -> Any:
    """
    Scrape a YouTube profile URL. Extracts the channel handle and performs a multi-tab scrape behind the scenes.
    Uses Crawlee for orchestration and Playwright automation, passing Webhook to global settings.
    """
    kwargs_request = {
        "url": url,
        "formats": formats,
        "timeout": timeout,
        "maxScrollY": maxScrollY,
        "maxScreenshotHeight": maxScreenshotHeight,
        "webhook": webhook,
    }
    if viewport is not None:
        kwargs_request["viewport"] = viewport

    request = ScrapeYoutubeProfileRequest(**kwargs_request)
    webhook_dict = request.webhook.model_dump() if request.webhook else None

    response = asyncio.run(amain(request, webhook=webhook_dict))

    if not response.success or response.error:
        error_msg = response.error or "Scrape operation failed."
        raise RuntimeError(error_msg)

    data_list = response.data or []
    for item in data_list:
        if "screenshot" in item and isinstance(item["screenshot"], File):
            f = item["screenshot"]
            item["screenshot"] = f.presigned_url or f.base64
            f.cleanup()

    return data_list

