import asyncio
import base64
import uuid
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
from koda.utils.file.main import File
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
        for suffix in ["/featured", "/videos", "/shorts", "/streams", "/podcasts", "/playlists", "/posts", "/store"]:
            if base_profile_url.endswith(suffix):
                base_profile_url = base_profile_url[:-len(suffix)]
                break
        
    # Determine which tabs actually exist on the channel
    try:
        # Wait a moment for tabs to render
        await page.wait_for_selector('yt-tab-shape a, tp-yt-paper-tab a', timeout=5000)
        found_tabs = await page.evaluate('''() => {
            const tabs = Array.from(document.querySelectorAll('yt-tab-shape a, tp-yt-paper-tab a'));
            return tabs.map(tab => ({
                href: tab.href,
                text: tab.innerText.trim().toLowerCase()
            })).filter(tab => tab.href);
        }''')
    except Exception:
        # Fallback to home if DOM parsing fails
        found_tabs = [{"href": base_profile_url, "text": "home"}]

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
    for tab in found_tabs:
        url = tab["href"]
        
        # Extract slug from URL for the handler logic
        slug = "home"
        current_url = url.split("?")[0].rstrip("/")
        if current_url != base_profile_url:
            slug = current_url.split("/")[-1]
            
        await context.add_requests([
            Request.from_url(
                url=url,
                unique_key=f"{url}#TAB",
                label="TAB",
                user_data={**user_data, "slug": slug}
            )
        ])


async def _validate_redirect(page: Page, expected_tab: str) -> bool:
    # Allow time for YouTube's client-side router to resolve any redirects
    try:
        await page.wait_for_load_state("networkidle", timeout=3000)
    except Exception:
        await page.wait_for_timeout(2000)
        
    current_url = page.url.split("?")[0].rstrip("/")
    if expected_tab.lower() not in ["home", "featured"] and not current_url.lower().endswith(f"/{expected_tab.lower()}"):
        return False
    return True


@router.handler('TAB')
async def tab_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    user_data = context.request.user_data or {}
    slug = user_data.get("slug", "home")
    
    if not await _validate_redirect(page, slug):
        return
        
    await wait_for_networkidle(page)
    
    if slug in ["home", "featured"]:
        await scroll_to(page, y=None, wait_callback=lambda: wait_for_networkidle(page))
        screenshot_bytes = await screenshot(page, max_height=10000)
    else:
        await scroll_to(page, y=3072, wait_callback=lambda: wait_for_networkidle(page))
        screenshot_bytes = await screenshot(page, max_height=3072)
        
    if isinstance(screenshot_bytes, str): screenshot_bytes = screenshot_bytes.encode("utf-8")
    await context.push_data({"url": page.url, "screenshot_base64": base64.b64encode(screenshot_bytes).decode("utf-8"), "screenshot_filename": f"{uuid.uuid4().hex}.png"})


@router.handler('DIALOG')
async def dialog_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    
    await page.set_viewport_size({"width": 1366, "height": 3072})
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
        if isinstance(screenshot_bytes, str): screenshot_bytes = screenshot_bytes.encode("utf-8")
        await context.push_data({"url": page.url, "screenshot_base64": base64.b64encode(screenshot_bytes).decode("utf-8"), "screenshot_filename": f"{uuid.uuid4().hex}.png"})
    except Exception as e:
        context.log.error(f"Failed to capture About dialog: {e}")
    finally:
        await page.set_viewport_size({"width": 1366, "height": 768})


@webhook_dispatch
async def scrape_youtube_profile(request: ScrapeYoutubeProfileRequest) -> ScrapeYoutubeProfileResponse:
    try:
        from datetime import timedelta

        async with KodaClient(s3_resource=request.s3_resource, timeout=request.timeout, substitute_pixels=False) as client:
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
