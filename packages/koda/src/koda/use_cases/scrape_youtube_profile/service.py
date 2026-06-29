import asyncio
import base64
from typing import Dict, List, Any, cast

from crawlee.router import Router
from crawlee.crawlers import PlaywrightCrawlingContext, PlaywrightCrawler
from crawlee import Request, ConcurrencySettings
from playwright.async_api import Page

from koda.client import KodaClient
from koda.config.main import settings
from koda.exceptions import TimeoutError, BrowserLaunchError
from koda.utils.webhook.service import webhook_dispatch
from koda.use_cases.service import wait_for_networkidle, scroll_to, screenshot
from .schema import ScrapeYoutubeProfileRequest, ScrapeYoutubeProfileResponse

router = Router[PlaywrightCrawlingContext]()

@router.default_handler
async def default_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    
    try:
        await page.wait_for_load_state("domcontentloaded", timeout=5000)
    except Exception:
        pass
    
    resolved_url = page.url
    
    parts = resolved_url.split("/")
    if len(parts) > 4 and parts[3].startswith("@"):
        base_profile_url = "/".join(parts[:4])
    elif len(parts) > 4 and parts[3] in ['c', 'user', 'channel']:
        base_profile_url = "/".join(parts[:5])
    else:
        base_profile_url = resolved_url.split("?")[0].rstrip("/")
        for suffix in ["/featured", "/videos", "/shorts", "/streams", "/podcasts", "/playlists", "/community", "/store"]:
            if base_profile_url.endswith(suffix):
                base_profile_url = base_profile_url[:-len(suffix)]
                break
        
    tabs = cast(List[str], context.request.user_data.get("tabs", ["home", "videos", "shorts", "streams", "podcasts", "playlists", "community", "store"]))
    
    # 1. Enqueue About
    await context.add_requests([
        Request.from_url(
            url=base_profile_url,
            unique_key=f"{base_profile_url}#ABOUT",
            label="ABOUT",
            user_data={"tab_name": "About", **context.request.user_data}
        )
    ])
    
    # 2. Enqueue Tab Handlers
    valid_handlers = ["HOME", "VIDEOS", "SHORTS", "STREAMS", "PODCASTS", "PLAYLISTS", "COMMUNITY", "STORE"]
    for tab in tabs:
        tab_upper = str(tab).upper()
        if tab_upper in valid_handlers:
            url = base_profile_url if tab_upper == "HOME" else f"{base_profile_url}/{tab_upper.lower()}"
            await context.add_requests([
                Request.from_url(
                    url=url,
                    unique_key=f"{base_profile_url}#{tab_upper}",
                    label=tab_upper,
                    user_data={"tab_name": str(tab).capitalize(), **context.request.user_data}
                )
            ])


async def _validate_redirect(page: Page, expected_tab: str) -> bool:
    current_url = page.url
    if expected_tab.lower() != "home" and f"/{expected_tab.lower()}" not in current_url.lower():
        return False
    try:
        selected_tab = await page.locator('yt-tab-shape[aria-selected="true"], tp-yt-paper-tab.iron-selected').first.inner_text(timeout=1500)
        if selected_tab:
            selected_tab_clean = selected_tab.strip().lower()
            if expected_tab.lower() != selected_tab_clean:
                return False
    except Exception:
        return False
    return True


@router.handler('HOME')
async def home_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    await wait_for_networkidle(page)
    await scroll_to(page, y=None, wait_callback=lambda: wait_for_networkidle(page))
    b64_str = base64.b64encode(await screenshot(page, max_height=10000)).decode('utf-8')
    await context.push_data({"url": page.url, "tab_name": "Home", "screenshot": f"data:image/png;base64,{b64_str}"})

@router.handler('VIDEOS')
async def videos_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    if not await _validate_redirect(page, "videos"):
        return
    await wait_for_networkidle(page)
    await scroll_to(page, y=3072, wait_callback=lambda: wait_for_networkidle(page))
    b64_str = base64.b64encode(await screenshot(page, max_height=3072)).decode('utf-8')
    await context.push_data({"url": page.url, "tab_name": "Videos", "screenshot": f"data:image/png;base64,{b64_str}"})

@router.handler('SHORTS')
async def shorts_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    if not await _validate_redirect(page, "shorts"):
        return
    await wait_for_networkidle(page)
    await scroll_to(page, y=3072, wait_callback=lambda: wait_for_networkidle(page))
    b64_str = base64.b64encode(await screenshot(page, max_height=3072)).decode('utf-8')
    await context.push_data({"url": page.url, "tab_name": "Shorts", "screenshot": f"data:image/png;base64,{b64_str}"})

@router.handler('STREAMS')
async def streams_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    if not await _validate_redirect(page, "streams"):
        return
    await wait_for_networkidle(page)
    await scroll_to(page, y=3072, wait_callback=lambda: wait_for_networkidle(page))
    b64_str = base64.b64encode(await screenshot(page, max_height=3072)).decode('utf-8')
    await context.push_data({"url": page.url, "tab_name": "Streams", "screenshot": f"data:image/png;base64,{b64_str}"})

@router.handler('PODCASTS')
async def podcasts_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    if not await _validate_redirect(page, "podcasts"):
        return
    await wait_for_networkidle(page)
    await scroll_to(page, y=3072, wait_callback=lambda: wait_for_networkidle(page))
    b64_str = base64.b64encode(await screenshot(page, max_height=3072)).decode('utf-8')
    await context.push_data({"url": page.url, "tab_name": "Podcasts", "screenshot": f"data:image/png;base64,{b64_str}"})

@router.handler('PLAYLISTS')
async def playlists_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    if not await _validate_redirect(page, "playlists"):
        return
    await wait_for_networkidle(page)
    await scroll_to(page, y=3072, wait_callback=lambda: wait_for_networkidle(page))
    b64_str = base64.b64encode(await screenshot(page, max_height=3072)).decode('utf-8')
    await context.push_data({"url": page.url, "tab_name": "Playlists", "screenshot": f"data:image/png;base64,{b64_str}"})

@router.handler('COMMUNITY')
async def community_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    if not await _validate_redirect(page, "community"):
        return
    await wait_for_networkidle(page)
    await scroll_to(page, y=3072, wait_callback=lambda: wait_for_networkidle(page))
    b64_str = base64.b64encode(await screenshot(page, max_height=3072)).decode('utf-8')
    await context.push_data({"url": page.url, "tab_name": "Community", "screenshot": f"data:image/png;base64,{b64_str}"})

@router.handler('STORE')
async def store_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    if not await _validate_redirect(page, "store"):
        return
    await wait_for_networkidle(page)
    await scroll_to(page, y=3072, wait_callback=lambda: wait_for_networkidle(page))
    b64_str = base64.b64encode(await screenshot(page, max_height=3072)).decode('utf-8')
    await context.push_data({"url": page.url, "tab_name": "Store", "screenshot": f"data:image/png;base64,{b64_str}"})

@router.handler('ABOUT')
async def about_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    
    await page.set_viewport_size({"width": 1366, "height": 3072})
    try:
        about_selector = "button[aria-label^=\"Description\"]:visible, button:has-text('...more'):visible, button:has-text('more links'):visible, ytd-channel-about-metadata-renderer:visible"
        await page.locator(about_selector).click(timeout=2000)
        dialog = page.locator("tp-yt-paper-dialog").first
        await dialog.wait_for(state="visible", timeout=2000)
        await wait_for_networkidle(page)
        
        screenshot_bytes = await dialog.screenshot()
        b64_str = base64.b64encode(screenshot_bytes).decode('utf-8')
        await context.push_data({"url": page.url, "tab_name": "About", "screenshot": f"data:image/png;base64,{b64_str}"})
    except Exception:
        pass
    finally:
        await page.set_viewport_size({"width": 1366, "height": 768})


@webhook_dispatch
async def scrape_youtube_profile(request: ScrapeYoutubeProfileRequest) -> ScrapeYoutubeProfileResponse:
    try:
        from datetime import timedelta

        async with KodaClient(s3_resource=request.s3_resource, timeout=request.timeout) as client:
            crawler = PlaywrightCrawler(
                client=client,  # type: ignore
                request_handler=router,
                max_request_retries=1,
                request_handler_timeout=timedelta(milliseconds=request.timeout),
                concurrency_settings=ConcurrencySettings(
                    max_concurrency=request.max_concurrency,
                    desired_concurrency=min(10, request.max_concurrency)
                )
            )

            @crawler.pre_navigation_hook
            async def block_unnecessary_resources(context) -> None:
                # Force viewport
                await context.page.set_viewport_size({"width": 1366, "height": 768})
                
                # Add consent cookies
                try:
                    await context.page.context.add_cookies([{
                        "name": "CONSENT",
                        "value": "YES+cb",
                        "domain": ".youtube.com",
                        "path": "/"
                    }])
                except Exception:
                    pass

                # We deliberately do not block images, media, or stylesheets because screenshots are the primary objective.
            
            # Start Crawl
            await crawler.run([
                Request.from_url(
                    url=request.url,
                    user_data={
                        "tabs": request.tabs
                    }
                )
            ])
            
            # Post Crawl Formatting
            dataset = await crawler.get_dataset()
            data_obj = await dataset.get_data()
            items = data_obj.items
            
            data_list = []
            
            for item in items:
                tab_data = {
                    "tab_name": item.get("tab_name", "Unknown"),
                    "url": item.get("url", "")
                }
                
                if "screenshot" in item:
                    tab_data["screenshot"] = item["screenshot"]
                
                data_list.append(tab_data)
                
            return ScrapeYoutubeProfileResponse(success=True, data=data_list)

    except (TimeoutError, asyncio.TimeoutError):
        return ScrapeYoutubeProfileResponse(success=False, error="Scrape operation timed out")
    except BrowserLaunchError as e:
        return ScrapeYoutubeProfileResponse(success=False, error=f"Browser crash: {e}")
    except Exception as e:
        return ScrapeYoutubeProfileResponse(success=False, error=str(e))
