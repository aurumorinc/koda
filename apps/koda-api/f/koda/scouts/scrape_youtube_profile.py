# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.1.0#subdirectory=packages/koda",
# ]
# ///
import asyncio
import wmill
import base64
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, ConfigDict, Field

from crawlee.router import Router
from crawlee.crawlers import PlaywrightCrawlingContext
from crawlee import Request

from koda import KodaClient, Webhook, settings, webhook_dispatch
from crawlee import PlaywrightCrawler

router = Router[PlaywrightCrawlingContext]()

@router.default_handler
async def default_handler(context: PlaywrightCrawlingContext) -> None:
    # Resolve canonical URL
    page = context.page
    
    # Wait for the page to load, but we don't need a deep crawl
    await page.wait_for_timeout(2000)
    
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
    tabs = context.request.user_data.get("tabs", ["home", "videos", "shorts", "streams", "podcasts", "playlists", "community", "store"])
    
    # 1. Enqueue About (handled separately)
    await context.add_requests([
        Request.from_url(
            url=base_profile_url,
            unique_key=f"{base_profile_url}#ABOUT",
            user_data={"label": "ABOUT", "tab_name": "About", **context.request.user_data}
        )
    ])
    
    # 2. Enqueue Home Tab if requested
    if "home" in [t.lower() for t in tabs]:
        await context.add_requests([
            Request.from_url(
                url=base_profile_url,
                unique_key=f"{base_profile_url}#HOME",
                user_data={"label": "TAB", "tab_name": "Home", **context.request.user_data}
            )
        ])
    
    # 3. Enqueue Other Sub Tabs
    for tab in tabs:
        tab_lower = tab.lower()
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
    normalized_formats = user_data.get("normalized_formats", ["markdown"])
    has_screenshot = user_data.get("has_screenshot", False)
    
    # 1. Click consent
    try:
        consent_selector = "ytd-consent-bump-v2-lightbox button:has-text('Accept'), ytd-consent-bump-v2-lightbox button:has-text('Agree')"
        await page.locator(consent_selector).click(timeout=2000)
        await page.wait_for_timeout(1000)
    except Exception:
        pass
        
    # 2. Click about
    try:
        about_selector = "button[aria-label^=\"Description\"]:visible, button:has-text('...more'):visible, button:has-text('more links'):visible, ytd-channel-about-metadata-renderer:visible"
        await page.locator(about_selector).click(timeout=3000)
        await page.wait_for_timeout(2000)
    except Exception:
        pass
        
    extracted_data = {
        "url": page.url,
        "tab_name": "About"
    }
    
    modal_selector = "ytd-engagement-panel-section-list-renderer[target-id='engagement-panel-about-this-channel']"
    
    if "screenshot" in normalized_formats or "screenshots" in normalized_formats or has_screenshot:
        try:
            modal = page.locator(modal_selector)
            if await modal.is_visible(timeout=2000):
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
            if await modal.is_visible(timeout=2000):
                extracted_data["html"] = await modal.inner_html()
            else:
                extracted_data["html"] = await page.content()
        except Exception:
            extracted_data["html"] = await page.content()
            
    if "markdown" in normalized_formats:
        try:
            modal = page.locator(modal_selector)
            if await modal.is_visible(timeout=2000):
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
    tab_name = user_data["tab_name"]
    normalized_formats = user_data.get("normalized_formats", ["markdown"])
    has_screenshot = user_data.get("has_screenshot", False)
    
    # 1. Click consent
    try:
        consent_selector = "ytd-consent-bump-v2-lightbox button:has-text('Accept'), ytd-consent-bump-v2-lightbox button:has-text('Agree')"
        await page.locator(consent_selector).click(timeout=2000)
        await page.wait_for_timeout(1000)
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
        await page.mouse.wheel(0, 1000)
        await page.wait_for_timeout(1500)
        await page.mouse.wheel(0, 1000)
        await page.wait_for_timeout(1500)
        await page.mouse.wheel(0, 780)
        await page.wait_for_timeout(1500)
            
    # 3. Extraction
    extracted_data = {
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

class ScrapeYoutubeProfileRequest(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    url: str
    formats: List[Union[str, Dict[str, Any]]] = Field(default_factory=lambda: ["markdown"])
    timeout: int = 300000
    s3_resource: Optional[str] = "f/koda/default_s3"
    webhook: Optional[Webhook] = None
    tabs: List[str] = Field(default_factory=lambda: ["home", "videos", "shorts", "streams", "podcasts", "playlists", "community", "store"])

class ScrapeYoutubeProfileResponse(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None

async def _run_youtube_scrape(request: ScrapeYoutubeProfileRequest) -> ScrapeYoutubeProfileResponse:
    # Fetch S3 config if resource is provided and set globally
    if request.s3_resource:
        s3_config_dict = wmill.get_resource(request.s3_resource)
        if not s3_config_dict:
            return ScrapeYoutubeProfileResponse(success=False, error=f"S3 Resource '{request.s3_resource}' not found.")
            
        settings.s3_bucket_name = s3_config_dict.get("bucket")
        settings.s3_access_key_id = s3_config_dict.get("accessKey") or s3_config_dict.get("access_key")
        settings.s3_secret_access_key = s3_config_dict.get("secretKey") or s3_config_dict.get("secret_key")
        settings.s3_endpoint_url = s3_config_dict.get("endPoint") or s3_config_dict.get("endpoint_url")
        settings.s3_region_name = s3_config_dict.get("region", "us-east-1")
        if "pathStyle" in s3_config_dict or "path_style" in s3_config_dict:
            settings.s3_addressing_style = "path" if s3_config_dict.get("pathStyle", s3_config_dict.get("path_style")) else "auto"

    normalized_formats = []
    for f in request.formats:
        if isinstance(f, dict):
            normalized_formats.append(f.get("type", ""))
        else:
            normalized_formats.append(str(f))

    has_screenshot = any(f == "screenshot" for f in normalized_formats)

    try:
        async with KodaClient() as client:
            crawler = PlaywrightCrawler(
                client=client,
                request_handler=router,
                max_request_retries=1
            )
            
            # Start Crawl
            await crawler.run([
                Request.from_url(
                    url=request.url,
                    user_data={
                        "tabs": request.tabs,
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
                
            # Note: The global Crawler hook (PlaywrightCrawler extended natively)
            # will have already zipped/uploaded the dataset to S3 during its teardown if S3 is configured!
            
            return ScrapeYoutubeProfileResponse(success=True, data=data_list)

    except Exception as e:
        return ScrapeYoutubeProfileResponse(success=False, error=str(e))

@webhook_dispatch
async def main(
    url: str,
    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
    timeout: int = 300000,
    s3_resource: Optional[str] = "f/koda/default_s3",
    webhook: Optional[Webhook] = None,
    **kwargs
) -> dict:
    """
    Scrape a YouTube profile URL. Extracts the channel handle and performs a multi-tab scrape behind the scenes.
    Uses Crawlee for orchestration and Playwright automation, passing S3/Webhook to global settings.
    """
    tabs = kwargs.pop("tabs", ["home", "videos", "shorts", "streams", "podcasts", "playlists", "community", "store"])
    request = ScrapeYoutubeProfileRequest(
        url=url,
        formats=formats,
        timeout=timeout,
        s3_resource=s3_resource,
        webhook=webhook,
        tabs=tabs,
        **kwargs
    )
    response = await _run_youtube_scrape(request)
    return response.model_dump(exclude_none=True)

def _run_main_sync(*args, **kwargs):
    return asyncio.run(main(*args, **kwargs))
