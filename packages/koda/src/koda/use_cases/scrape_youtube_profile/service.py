import asyncio
import base64
import uuid
from contextlib import suppress
from typing import Optional, List, Dict, Any, Union

from crawlee.router import Router
from crawlee.crawlers import PlaywrightCrawlingContext, PlaywrightCrawler
from crawlee import Request

from koda.client import KodaClient
from koda.exceptions import TimeoutError, BrowserLaunchError
from oort.webhook.service import webhook_dispatch
from oort.file.main import File
from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest, ScrapeYoutubeProfileResponse

__all__ = [
    "CHANNEL_PATH_PREFIXES",
    "MAX_SCREENSHOT_HEIGHT",
    "MAX_SCROLL_Y",
    "TABS",
    "VIEWPORT",
    "dialog_handler",
    "router",
    "scrape_youtube_profile",
    "tab_handler",
]

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

VIEWPORT = {"width": 1366, "height": 768}
MAX_SCROLL_Y = 3072
MAX_SCREENSHOT_HEIGHT = 10000

router = Router[PlaywrightCrawlingContext]()


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


async def _hydrate_images(page) -> None:
    """Forces all lazy-loaded thumbnails to load eagerly and waits for them to complete rendering."""
    with suppress(Exception):
        await page.evaluate("""async () => {
            window.scrollBy(0, 50);
            window.scrollBy(0, -50);

            const containers = Array.from(
                document.querySelectorAll('yt-core-image, yt-img-shadow, ytd-thumbnail, img')
            );
            const imgPromises = [];

            for (const el of containers) {
                const img = el.tagName === 'IMG' ? el : el.querySelector('img');
                if (!img) continue;

                img.setAttribute('loading', 'eager');

                const realSrc = el.src || el.getAttribute('src') || img.dataset.src || img.src;
                if (realSrc && (!img.src || img.src.includes('data:image'))) {
                    img.src = realSrc;
                }

                if (!img.complete) {
                    imgPromises.push(new Promise(resolve => {
                        img.addEventListener('load', resolve, { once: true });
                        img.addEventListener('error', resolve, { once: true });
                        setTimeout(resolve, 300);
                    }));
                }
            }
            await Promise.all(imgPromises);
        }""")


async def _screenshot(page, max_height_limit: int = MAX_SCROLL_Y) -> bytes:
    """Dynamically calculates document scroll height, adjusts viewport bounds, hydrates images, and returns screenshot."""
    doc_height = await page.evaluate(
        "Math.max(document.documentElement.scrollHeight, document.body.scrollHeight || 0)"
    )
    target_height = min(max(doc_height, VIEWPORT["height"]), max_height_limit)

    await page.set_viewport_size({"width": VIEWPORT["width"], "height": target_height})
    await _hydrate_images(page)

    return await page.screenshot(full_page=False)


async def _capture_about_dialog_in_place(context: PlaywrightCrawlingContext, base_profile_url: str) -> None:
    page = context.page
    try:
        await page.set_viewport_size({"width": VIEWPORT["width"], "height": MAX_SCROLL_Y})
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
            await page.set_viewport_size(VIEWPORT)
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(500)


@router.default_handler
async def _handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page

    with suppress(Exception):
        await page.wait_for_load_state("domcontentloaded", timeout=5000)

    user_data = context.request.user_data or {}
    max_scroll_y = user_data.get("max_scroll_y", MAX_SCROLL_Y)

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
    await _capture_about_dialog_in_place(context, base_profile_url)

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

        max_limit = MAX_SCREENSHOT_HEIGHT if full_page else max_scroll_y
        screenshot_bytes = await _screenshot(page, max_height_limit=max_limit)

        await _push_screenshot_data(context, tab_url, screenshot_bytes)


@router.handler("TAB")
async def tab_handler(context: PlaywrightCrawlingContext) -> None:
    pass


@router.handler("DIALOG")
async def dialog_handler(context: PlaywrightCrawlingContext) -> None:
    pass


@webhook_dispatch(event_prefix="scrape_youtube_profile")
async def _scrape_youtube_profile_dispatched(
    request: ScrapeYoutubeProfileRequest, webhook: Optional[dict] = None
) -> ScrapeYoutubeProfileResponse:
    try:
        from datetime import timedelta

        async with KodaClient(
            timeout=request.timeout,
            substitute_pixels=False,
        ) as client:
            crawler = PlaywrightCrawler(
                client=client,  # type: ignore
                request_handler=router,
                max_request_retries=3,
                request_handler_timeout=timedelta(milliseconds=request.timeout),
            )

            @crawler.pre_navigation_hook
            async def block_unnecessary_resources(context) -> None:
                # Force viewport
                await context.page.set_viewport_size(VIEWPORT)

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
            await crawler.run([
                Request.from_url(
                    url=request.url,
                    user_data={"max_scroll_y": request.max_scroll_y},
                )
            ])

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

            return ScrapeYoutubeProfileResponse(success=True, data=data_list)

    except (TimeoutError, asyncio.TimeoutError):
        return ScrapeYoutubeProfileResponse(
            success=False, error="Scrape operation timed out"
        )
    except BrowserLaunchError as e:
        return ScrapeYoutubeProfileResponse(success=False, error=f"Browser crash: {e}")
    except Exception as e:
        return ScrapeYoutubeProfileResponse(success=False, error=str(e))


async def scrape_youtube_profile(
    request: ScrapeYoutubeProfileRequest,
) -> ScrapeYoutubeProfileResponse:
    webhook_dict = request.webhook.model_dump() if request.webhook else None
    return await _scrape_youtube_profile_dispatched(request, webhook=webhook_dict)
