import asyncio
import base64
from typing import Dict, List, Any, cast

from crawlee.router import Router
from crawlee.crawlers import PlaywrightCrawlingContext, PlaywrightCrawler
from crawlee import Request, ConcurrencySettings

from koda.client import KodaClient
from koda.config.main import settings
from koda.exceptions import TimeoutError, BrowserLaunchError
from koda.utils.webhook.service import webhook_dispatch
from .schema import ScrapeYoutubeProfileRequest, ScrapeYoutubeProfileResponse

router = Router[PlaywrightCrawlingContext]()

@router.default_handler
async def default_handler(context: PlaywrightCrawlingContext) -> None:
    # Resolve canonical URL
    page = context.page
    
    # Wait for the DOM to load instead of arbitrary sleep
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
        
    # Enqueue sub-tabs
    tabs = cast(List[str], context.request.user_data.get("tabs", ["home", "videos", "shorts", "streams", "podcasts", "playlists", "community", "store"]))
    
    # 1. Enqueue About (handled separately)
    await context.add_requests([
        Request.from_url(
            url=base_profile_url,
            unique_key=f"{base_profile_url}#ABOUT",
            user_data={"label": "ABOUT", "tab_name": "About", **context.request.user_data}
        )
    ])
    
    # 2. Enqueue Home Tab if requested
    if "home" in [str(t).lower() for t in tabs if t]:
        await context.add_requests([
            Request.from_url(
                url=base_profile_url,
                unique_key=f"{base_profile_url}#HOME",
                user_data={"label": "TAB", "tab_name": "Home", **context.request.user_data}
            )
        ])
    
    # 3. Enqueue Other Sub Tabs
    for tab in tabs:
        tab_lower = str(tab).lower()
        if tab_lower == "home":
            continue
        await context.add_requests([
            Request.from_url(
                url=f"{base_profile_url}/{tab_lower}",
                user_data={"label": "TAB", "tab_name": tab.capitalize(), **context.request.user_data}
            )
        ])

@router.handler('ABOUT')
async def about_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    user_data = context.request.user_data
    normalized_formats = cast(List[str], user_data.get("normalized_formats", ["markdown"]))
    has_screenshot = user_data.get("has_screenshot", False)
    
    # 1. Click consent
    try:
        consent_selector = "ytd-consent-bump-v2-lightbox button:has-text('Accept'), ytd-consent-bump-v2-lightbox button:has-text('Agree')"
        await page.locator(consent_selector).click(timeout=2000)
    except Exception:
        pass
        
    # 2. Click about
    modal_selector = "ytd-engagement-panel-section-list-renderer[target-id='engagement-panel-about-this-channel']"
    try:
        about_selector = "button[aria-label^=\"Description\"]:visible, button:has-text('...more'):visible, button:has-text('more links'):visible, ytd-channel-about-metadata-renderer:visible"
        await page.locator(about_selector).click(timeout=3000)
        await page.locator(modal_selector).wait_for(state="visible", timeout=3000)
    except Exception:
        pass
        
    extracted_data: Dict[str, Any] = {
        "url": page.url,
        "tab_name": "About"
    }
    
    if "screenshot" in normalized_formats or "screenshots" in normalized_formats or has_screenshot:
        try:
            modal = page.locator(modal_selector)
            try:
                await modal.wait_for(state="visible", timeout=1000)
            except Exception:
                pass
            if await modal.is_visible():
                screenshot_bytes = await modal.screenshot()
            else:
                screenshot_bytes = await page.screenshot(full_page=True)
            b64_str = base64.b64encode(screenshot_bytes).decode('utf-8')
            extracted_data["screenshot"] = f"data:image/jpeg;base64,{b64_str}"
        except Exception:
            pass
            
    if "html" in normalized_formats or "rawHtml" in normalized_formats:
        try:
            modal = page.locator(modal_selector)
            try:
                await modal.wait_for(state="visible", timeout=1000)
            except Exception:
                pass
            if await modal.is_visible():
                extracted_data["html"] = await modal.inner_html()
            else:
                extracted_data["html"] = await page.content()
        except Exception:
            extracted_data["html"] = await page.content()
            
    if "markdown" in normalized_formats:
        try:
            modal = page.locator(modal_selector)
            try:
                await modal.wait_for(state="visible", timeout=1000)
            except Exception:
                pass
            if await modal.is_visible():
                text = await modal.inner_text()
            else:
                text = await page.locator("body").inner_text()
            extracted_data["markdown"] = text
        except Exception:
            text = await page.locator("body").inner_text()
            extracted_data["markdown"] = text
            
    if "links" in normalized_formats:
        link_elements = await page.locator("a").all()
        links = []
        for el in link_elements:
            href = await el.get_attribute("href")
            if href:
                links.append(href)
        extracted_data["links"] = list(set(links))
        
    await context.push_data(extracted_data)

@router.handler('TAB')
async def tab_handler(context: PlaywrightCrawlingContext) -> None:
    page = context.page
    user_data = context.request.user_data
    tab_name = str(user_data.get("tab_name", ""))
    normalized_formats = cast(List[str], user_data.get("normalized_formats", ["markdown"]))
    has_screenshot = user_data.get("has_screenshot", False)
    
    # 1. Click consent
    try:
        consent_selector = "ytd-consent-bump-v2-lightbox button:has-text('Accept'), ytd-consent-bump-v2-lightbox button:has-text('Agree')"
        await page.locator(consent_selector).click(timeout=2000)
    except Exception:
        pass # Consent might not exist
        
    # Fail fast: check if the tab actually exists
    current_url = page.url
    
    if tab_name.lower() != "home":
        # If the current URL does not contain the tab name, it doesn't exist
        # E.g., we want "/store", but URL redirected to "/featured" or "/"
        if f"/{tab_name.lower()}" not in current_url.lower():
            return

    # Check active tab in DOM as secondary verification
    try:
        selected_tab = await page.locator('yt-tab-shape[aria-selected="true"], tp-yt-paper-tab.iron-selected').first.inner_text(timeout=5000)
        if selected_tab:
            selected_tab_clean = selected_tab.strip().lower()
            if tab_name.lower() != selected_tab_clean:
                return
    except Exception:
        # If there's no active tab indicator at all, it's likely a 404 or invalid page
        return

    # 2. Scroll specific actions
    if tab_name.lower() != "home":
        for _ in range(3):
            await page.mouse.wheel(0, 1000)
            try:
                await page.locator("ytd-rich-item-renderer").last.wait_for(state="attached", timeout=1000)
            except Exception:
                pass
            
    # 3. Extraction
    extracted_data: Dict[str, Any] = {
        "url": page.url,
        "tab_name": tab_name
    }
    
    if "html" in normalized_formats or "rawHtml" in normalized_formats:
        extracted_data["html"] = await page.content()
        
    # Simple Readability fallback for Markdown
    if "markdown" in normalized_formats:
        # Since Koda's extractors aren't easily imported as a standalone function for a raw PW page,
        # we pull basic text content or evaluate readability if needed.
        text = await page.locator("body").inner_text()
        extracted_data["markdown"] = text
        
    if "links" in normalized_formats:
        link_elements = await page.locator("a").all()
        links = []
        for el in link_elements:
            href = await el.get_attribute("href")
            if href:
                links.append(href)
        extracted_data["links"] = list(set(links))
        
    if "screenshot" in normalized_formats or "screenshots" in normalized_formats or has_screenshot:
        screenshot_bytes = await page.screenshot(full_page=True)
        b64_str = base64.b64encode(screenshot_bytes).decode('utf-8')
        extracted_data["screenshot"] = f"data:image/jpeg;base64,{b64_str}"
        
    # 4. Push to Dataset
    await context.push_data(extracted_data)


@webhook_dispatch
async def scrape_youtube_profile(ScrapeYoutubeProfileRequest: ScrapeYoutubeProfileRequest) -> ScrapeYoutubeProfileResponse:
    normalized_formats = []
    for f in ScrapeYoutubeProfileRequest.formats:
        if isinstance(f, dict):
            normalized_formats.append(str(f.get("type", "")))
        else:
            normalized_formats.append(str(f))

    has_screenshot = any(f == "screenshot" for f in normalized_formats)

    try:
        from datetime import timedelta

        async with KodaClient(s3_resource=ScrapeYoutubeProfileRequest.s3_resource, timeout=ScrapeYoutubeProfileRequest.timeout) as client:
            crawler = PlaywrightCrawler(
                client=client,  # type: ignore
                request_handler=router,
                max_request_retries=1,
                request_handler_timeout=timedelta(milliseconds=ScrapeYoutubeProfileRequest.timeout),
                concurrency_settings=ConcurrencySettings(
                    max_concurrency=ScrapeYoutubeProfileRequest.maxConcurrency,
                    desired_concurrency=min(10, ScrapeYoutubeProfileRequest.maxConcurrency)
                )
            )

            @crawler.pre_navigation_hook
            async def block_unnecessary_resources(context) -> None:
                has_screenshot = context.request.user_data.get("has_screenshot", False)
                if not has_screenshot:
                    await context.page.route(
                        "**/*",
                        lambda route: route.abort() if route.request.resource_type in ["image", "media", "font", "stylesheet"] else route.continue_()
                    )
            
            # Start Crawl
            await crawler.run([
                Request.from_url(
                    url=ScrapeYoutubeProfileRequest.url,
                    user_data={
                        "tabs": ["home", "videos", "shorts", "streams", "podcasts", "playlists", "community", "store"],
                        "normalized_formats": normalized_formats,
                        "has_screenshot": has_screenshot
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
                
                if "markdown" in item:
                    tab_data["markdown"] = item["markdown"]
                if "html" in item:
                    tab_data["html"] = item["html"]
                if "links" in item:
                    tab_data["links"] = item["links"]
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
