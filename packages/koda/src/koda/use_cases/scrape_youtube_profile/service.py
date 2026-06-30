import asyncio
import base64
import uuid
from contextlib import suppress

from crawlee.router import Router
from crawlee.crawlers import PlaywrightCrawlingContext, PlaywrightCrawler
from crawlee import Request, ConcurrencySettings
from playwright.async_api import Page

from koda.client import KodaClient
from koda.exceptions import TimeoutError, BrowserLaunchError
from koda.utils.webhook.service import webhook_dispatch
from koda.use_cases.service import wait_for_networkidle, scroll_to, screenshot
from koda.utils.file.main import File
from .schema import ScrapeYoutubeProfileRequest, ScrapeYoutubeProfileResponse

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
    {"name": "courses", "slug": "courses", "full_page": False}
]

VIEWPORT = {"width": 1366, "height": 768}
MAX_SCROLL_Y = 3072
MAX_SCREENSHOT_HEIGHT = 10000

router = Router[PlaywrightCrawlingContext]()

async def _push_screenshot_data(context: PlaywrightCrawlingContext, url: str, screenshot_bytes: bytes | str) -> None:
    if isinstance(screenshot_bytes, str):
        screenshot_bytes = screenshot_bytes.encode("utf-8")
    await context.push_data({
        "url": url,
        "screenshot_base64": base64.b64encode(screenshot_bytes).decode("utf-8"),
        "screenshot_filename": f"{uuid.uuid4().hex}.png"
    })

@router.default_handler
async def _handler(context: PlaywrightCrawlingContext) -> None:
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
                base_profile_url = base_profile_url[:-len(f"/{tab['slug']}")]
                break
        
    # Determine which tabs actually exist on the channel
    found_slugs = set()
    try:
        # Wait a moment for tabs to render
        await page.wait_for_selector('yt-tab-shape, tp-yt-paper-tab, [role="tab"]', timeout=5000)
        tab_texts = await page.evaluate('''() => {
            const tabs = Array.from(document.querySelectorAll('yt-tab-shape, tp-yt-paper-tab, [role="tab"]'));
            return tabs.map(tab => (tab.innerText || tab.textContent || '').trim().toLowerCase());
        }''')
        
        for text in tab_texts:
            for tab in TABS:
                if tab["name"] in text:
                    found_slugs.add(tab["slug"])
    except Exception:
        pass
        
    if not found_slugs:
        # Fallback to all if DOM parsing fails
        found_slugs = {tab["slug"] for tab in TABS}

    user_data = context.request.user_data or {}
    
    # 1. Enqueue Dialogs (About)
    await context.add_requests([
        Request.from_url(
            url=base_profile_url,
            unique_key=f"{base_profile_url}#DIALOG",
            label="DIALOG",
            user_data=user_data
        )
    ])
    
    # 2. Enqueue Tab Handlers
    for tab in TABS:
        slug = tab["slug"]
        if slug not in found_slugs:
            continue
            
        url = f"{base_profile_url}/{slug}"
        await context.add_requests([
            Request.from_url(
                url=url,
                unique_key=f"{url}#TAB",
                label="TAB",
                user_data={**user_data, "slug": slug, "full_page": tab["full_page"]}
            )
        ])


async def _validate_redirect(page: Page, expected_slug: str) -> bool:
    # Allow time for YouTube's client-side router to resolve any redirects
    with suppress(Exception):
        await page.wait_for_load_state("networkidle", timeout=3000)
    
    if not page.is_closed():
        with suppress(Exception):
            await page.wait_for_timeout(2000)
        
    current_url = page.url.split("?")[0].rstrip("/")
    if expected_slug and not current_url.lower().endswith(f"/{expected_slug.lower()}"):
        return False
    return True


@router.handler('TAB')
async def tab_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    user_data = context.request.user_data or {}
    slug = user_data.get("slug")
    full_page = user_data.get("full_page", False)
    
    if not await _validate_redirect(page, slug):
        return
        
    await wait_for_networkidle(page)
    
    if full_page:
        await scroll_to(page, y=MAX_SCREENSHOT_HEIGHT, wait_callback=lambda: page.wait_for_timeout(1000))
        screenshot_bytes = await screenshot(page, max_height=MAX_SCREENSHOT_HEIGHT)
    else:
        await scroll_to(page, y=MAX_SCROLL_Y, wait_callback=lambda: page.wait_for_timeout(1000))
        screenshot_bytes = await screenshot(page, max_height=MAX_SCROLL_Y)
        
    await _push_screenshot_data(context, context.request.url, screenshot_bytes)


@router.handler('DIALOG')
async def dialog_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    
    await page.set_viewport_size({"width": VIEWPORT["width"], "height": MAX_SCROLL_Y})
    try:
        # Some channels don't have the "...more" button. Fail fast if it doesn't exist within 5 seconds.
        more_button = page.get_by_role("button").filter(has_text="...more")
        try:
            await more_button.wait_for(state="visible", timeout=5000)
            await more_button.click()
        except Exception:
            context.log.warning("No '...more' button found for About dialog.")
            return

        # In YouTube's DOM, there are multiple tp-yt-paper-dialog elements.
        # We explicitly filter for the one that has the About channel content.
        dialog = page.locator("tp-yt-paper-dialog:has(ytd-engagement-panel-section-list-renderer[target-id='engagement-panel-about-channel']), tp-yt-paper-dialog:visible").first
        try:
            await dialog.wait_for(state="visible", timeout=5000)
        except Exception:
            context.log.warning("About dialog did not appear.")
            return

        await wait_for_networkidle(page)
        
        box = await dialog.bounding_box()
        if not box:
            raise Exception("Dialog bounding box is null (element hidden?)")
            
        screenshot_bytes = await page.screenshot(clip=box)
        await _push_screenshot_data(context, f"{context.request.url}#about", screenshot_bytes)
    except Exception as e:
        context.log.error(f"Failed to capture About dialog: {e}")
    finally:
        with suppress(Exception):
            await page.set_viewport_size(VIEWPORT)


@webhook_dispatch
async def scrape_youtube_profile(request: ScrapeYoutubeProfileRequest) -> ScrapeYoutubeProfileResponse:
    try:
        from datetime import timedelta

        async with KodaClient(s3_resource=request.s3_resource, timeout=request.timeout, substitute_pixels=False) as client:
            crawler = PlaywrightCrawler(
                client=client,  # type: ignore
                request_handler=router,
                max_request_retries=3,
                request_handler_timeout=timedelta(milliseconds=request.timeout),
                concurrency_settings=ConcurrencySettings(
                    max_concurrency=request.max_concurrency,
                    desired_concurrency=min(10, request.max_concurrency)
                )
            )

            @crawler.pre_navigation_hook
            async def block_unnecessary_resources(context) -> None:
                # Force viewport
                await context.page.set_viewport_size(VIEWPORT)
                
                # Add consent cookies
                with suppress(Exception):
                    await context.page.context.add_cookies([{
                        "name": "CONSENT",
                        "value": "YES+cb",
                        "domain": ".youtube.com",
                        "path": "/"
                    }])

                # We deliberately do not block images, media, or stylesheets because screenshots are the primary objective.
            
            # Start Crawl
            await crawler.run([
                Request.from_url(
                    url=request.url
                )
            ])
            
            # Post Crawl Formatting
            dataset = await crawler.get_dataset()
            data = await dataset.get_data()
            items = data.items
            
            data_list = []
            
            for item in items:
                tab_data = {
                    "url": item.get("url", "")
                }
                
                if "screenshot_base64" in item and "screenshot_filename" in item:
                    f = File.from_base64(item["screenshot_base64"], item["screenshot_filename"], "image/png")
                    tab_data["screenshot"] = f
                
                data_list.append(tab_data)
                
            return ScrapeYoutubeProfileResponse(success=True, data=data_list)

    except (TimeoutError, asyncio.TimeoutError):
        return ScrapeYoutubeProfileResponse(success=False, error="Scrape operation timed out")
    except BrowserLaunchError as e:
        return ScrapeYoutubeProfileResponse(success=False, error=f"Browser crash: {e}")
    except Exception as e:
        return ScrapeYoutubeProfileResponse(success=False, error=str(e))
