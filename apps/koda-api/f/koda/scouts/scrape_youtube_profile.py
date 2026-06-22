# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@26.6.43#subdirectory=packages/koda",
# ]
# ///
import asyncio
import wmill
import base64
from typing import Optional, List, Dict, Any, Union

from crawlee.router import Router
from crawlee.crawlers import PlaywrightCrawlingContext
from crawlee import Request

from koda import KodaClient
from koda.config.main import settings
from koda.integrations.crawlee import PlaywrightCrawler

router = Router[PlaywrightCrawlingContext]()

@router.default_handler
async def default_handler(context: PlaywrightCrawlingContext) -> None:
    # Resolve canonical URL
    page = context.page
    
    # Wait for the page to load, but we don't need a deep crawl
    await page.wait_for_timeout(2000)
    
    resolved_url = page.url
    
    # Extract canonical URL if possible
    try:
        og_url = await page.locator('meta[property="og:url"]').get_attribute('content', timeout=2000)
        if og_url:
            resolved_url = og_url
    except Exception:
        pass
        
    parts = resolved_url.split("/")
    if len(parts) > 4 and "@" in parts[3]:
        base_profile_url = "/".join(parts[:4])
    else:
        base_profile_url = resolved_url.rstrip("/")
        
    # Enqueue sub-tabs
    tabs = context.request.user_data.get("tabs", ["videos", "shorts"])
    
    # 1. Home
    await context.enqueue_links(
        urls=[base_profile_url],
        user_data={"label": "TAB", "tab_name": "Home", **context.request.user_data}
    )
    
    # 2. About
    await context.enqueue_links(
        urls=[f"{base_profile_url}?about=1"],
        user_data={"label": "TAB", "tab_name": "About", **context.request.user_data}
    )
    
    # 3. Sub Tabs
    for tab in tabs:
        await context.enqueue_links(
            urls=[f"{base_profile_url}/{tab}"],
            user_data={"label": "TAB", "tab_name": tab.capitalize(), **context.request.user_data}
        )

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
        
    # About specific click
    if tab_name == "About":
        try:
            about_selector = "button[aria-label^=\"Description\"]:visible, button:has-text('...more'):visible, button:has-text('more links'):visible, ytd-channel-about-metadata-renderer:visible"
            await page.locator(about_selector).click(timeout=2000)
            await page.wait_for_timeout(2000)
        except Exception:
            pass

    # 2. Scroll specific actions
    if tab_name not in ["Home", "About"]:
        await page.evaluate("window.scrollBy(0, 1000);")
        await page.wait_for_timeout(1500)
        await page.evaluate("window.scrollBy(0, 1000);")
        await page.wait_for_timeout(1500)
        await page.evaluate("window.scrollBy(0, 780);")
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
        # For this script we will use page.evaluate to extract text.
        text = await page.evaluate("document.body.innerText")
        extracted_data["markdown"] = text
        
    if "links" in normalized_formats:
        links = await page.evaluate("Array.from(document.querySelectorAll('a')).map(a => a.href)")
        extracted_data["links"] = list(set(links))
        
    if "screenshot" in normalized_formats or "screenshots" in normalized_formats or has_screenshot:
        screenshot_bytes = await page.screenshot(full_page=True)
        b64_str = base64.b64encode(screenshot_bytes).decode('utf-8')
        extracted_data["screenshot"] = f"data:image/jpeg;base64,{b64_str}"
        
    # 4. Push to Dataset
    await context.push_data(extracted_data)


async def _run_youtube_scrape(
    url: str,
    formats: List[str],
    timeout: int,
    s3_resource: Optional[str],
    webhook: Optional[Dict[str, Any]],
    **kwargs
) -> Dict[str, Any]:
    
    # Set Webhook globally
    if webhook:
        settings.webhook_url = webhook.get("url")
        settings.webhook_events = webhook.get("events")
        settings.webhook_headers = webhook.get("headers")

    # Fetch S3 config if resource is provided and set globally
    if s3_resource:
        s3_config_dict = wmill.get_resource(s3_resource)
        if not s3_config_dict:
            return {"success": False, "error": f"S3 Resource '{s3_resource}' not found."}
            
        settings.s3_bucket_name = s3_config_dict.get("bucket")
        settings.s3_access_key_id = s3_config_dict.get("accessKey") or s3_config_dict.get("access_key")
        settings.s3_secret_access_key = s3_config_dict.get("secretKey") or s3_config_dict.get("secret_key")
        settings.s3_endpoint_url = s3_config_dict.get("endPoint") or s3_config_dict.get("endpoint_url")
        settings.s3_region_name = s3_config_dict.get("region", "us-east-1")
        if "pathStyle" in s3_config_dict or "path_style" in s3_config_dict:
            settings.s3_addressing_style = "path" if s3_config_dict.get("pathStyle", s3_config_dict.get("path_style")) else "auto"

    normalized_formats = formats if formats else []

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
                    url=url,
                    user_data={
                        "tabs": kwargs.get("tabs", ["videos", "shorts"]),
                        "normalized_formats": normalized_formats,
                        "has_screenshot": has_screenshot
                    }
                )
            ])
            
            # Post Crawl Formatting
            dataset = await crawler.get_dataset()
            data_obj = await dataset.get_data()
            items = data_obj.items
            
            aggregated_markdown = ""
            aggregated_html = ""
            aggregated_links = {}
            aggregated_screenshots = {}
            
            for item in items:
                tab_name = item.get("tab_name", "Unknown")
                
                if "markdown" in item:
                    aggregated_markdown += f"\n\n# {tab_name}\n{item['markdown']}\n"
                if "html" in item:
                    aggregated_html += f"<!-- Tab: {tab_name} -->\n{item['html']}\n"
                if "links" in item:
                    aggregated_links[tab_name] = item["links"]
                if "screenshot" in item:
                    aggregated_screenshots[tab_name] = item["screenshot"]
            
            data = {}
            if "markdown" in normalized_formats:
                data["markdown"] = aggregated_markdown.strip()
            if "html" in normalized_formats or "rawHtml" in normalized_formats:
                data["html"] = aggregated_html.strip()
            if "links" in normalized_formats:
                data["links"] = aggregated_links
            if "screenshot" in normalized_formats or "screenshots" in normalized_formats or has_screenshot:
                data["screenshots"] = aggregated_screenshots
                
            # Note: The global Crawler hook (PlaywrightCrawler extended natively) 
            # will have already zipped/uploaded the dataset to S3 during its teardown if S3 is configured!
            
            return {
                "success": True,
                "data": data
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main(
    url: str,
    formats: List[str] = ["markdown"],
    timeout: int = 300000,
    s3_resource: Optional[str] = "f/koda/default_s3",
    webhook: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Scrape a YouTube profile URL. Extracts the channel handle and performs a multi-tab scrape behind the scenes.
    Uses Crawlee for orchestration and Playwright automation, passing S3/Webhook to global settings.
    """
    return asyncio.run(_run_youtube_scrape(
        url=url,
        formats=formats,
        timeout=timeout,
        s3_resource=s3_resource,
        webhook=webhook,
        **kwargs
    ))
