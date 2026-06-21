# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@26.6.29#subdirectory=packages/koda",
# ]
# ///
import asyncio
import wmill
from typing import Optional, List, Dict, Any, Union

from koda import KodaClient, ScrapeRequest, BatchScrapeRequest

async def _run_youtube_scrape(
    url: str,
    formats: List[Union[str, Dict[str, Any]]],
    onlyMainContent: bool,
    actions: List[Dict[str, Any]],
    timeout: int,
    s3_resource: Optional[str],
    webhook: Optional[Dict[str, Any]],
    **kwargs
) -> Dict[str, Any]:
    # 1. Fetch S3 config if resource is provided
    s3_config = None
    if s3_resource:
        s3_config = wmill.get_resource(s3_resource)
        if not s3_config:
            return {"success": False, "error": f"S3 Resource '{s3_resource}' not found."}

    # 2. Normalize Formats
    normalized_formats = []
    if formats:
        for f in formats:
            if isinstance(f, dict):
                normalized_formats.append(f.get("type", ""))
            else:
                normalized_formats.append(str(f))

    # Configuration Overrides
    tabs = kwargs.get("tabs", ["videos", "shorts"])
    scroll_limit = kwargs.get("scroll_limit", 5)

    try:
        async with KodaClient() as client:
            # 3. Resolve Canonical URL
            # Execute a fast targeted scrape to get the resolved URL
            initial_req = ScrapeRequest(
                url=url,
                formats=["metadata"], # No need for markdown, we just want the URL
                onlyMainContent=False,
                timeout=timeout,
                actions=[
                    {"type": "wait", "milliseconds": 2000}
                ]
            )
            initial_res = await client.scrape(initial_req)
            if initial_res.error:
                return {"success": False, "error": f"Failed to resolve URL: {initial_res.error}"}

            resolved_url = url
            # The ScrapeResponse URL will not be updated from crawl4ai internally in ScrapeJob yet,
            # but we can try to extract from metadata if available, 
            # OR we can just rely on the user input url since the batch scrape handles redirects.
            # However, batch targets need to be built off the resolved url.
            # Wait, `initial_res.metadata` might have `og:url`!
            if initial_res.metadata and isinstance(initial_res.metadata, dict) and initial_res.metadata.get("og:url"):
                resolved_url = initial_res.metadata.get("og:url")
            elif initial_res.metadata and isinstance(initial_res.metadata, dict) and initial_res.metadata.get("url"):
                resolved_url = initial_res.metadata.get("url")

            # Parse base profile URL (remove any trailing tab paths)
            parts = resolved_url.split("/")
            # A typical youtube URL is https://www.youtube.com/@handle or https://www.youtube.com/@handle/videos
            if len(parts) > 4 and "@" in parts[3]:
                base_profile_url = "/".join(parts[:4])
            else:
                base_profile_url = resolved_url.rstrip("/")

            # 4. Construct Heterogeneous Batch Scrape Requests
            target_requests = []
            
            consent_action = {
                "type": "click",
                "selector": "ytd-consent-bump-v2-lightbox button:has-text('Accept'), ytd-consent-bump-v2-lightbox button:has-text('Agree')",
                "all": True,
                "timeout": 2000
            }
            
            # Specific sequence to scroll exactly 2780px
            scroll_actions_2780 = [
                {"type": "executeJavascript", "script": "window.scrollBy(0, 1000);"},
                {"type": "wait", "milliseconds": 1500},
                {"type": "executeJavascript", "script": "window.scrollBy(0, 1000);"},
                {"type": "wait", "milliseconds": 1500},
                {"type": "executeJavascript", "script": "window.scrollBy(0, 780);"},
                {"type": "wait", "milliseconds": 1500}
            ]
            
            # Explicitly enforce fullPage screenshots by passing the Firecrawl format object
            request_formats = normalized_formats.copy()
            has_screenshot = False
            for i, f in enumerate(request_formats):
                if f == "screenshot":
                    request_formats[i] = {"type": "screenshot", "fullPage": True}
                    has_screenshot = True
                elif isinstance(f, dict) and f.get("type") == "screenshot":
                    has_screenshot = True
                    if "fullPage" not in f:
                        request_formats[i]["fullPage"] = True

            if not has_screenshot and ("screenshot" in formats or "screenshots" in formats):
                request_formats.append({"type": "screenshot", "fullPage": True})
                
            # Job 1: Home Page - Click consent and take full page screenshot
            target_requests.append(ScrapeRequest(
                url=base_profile_url,
                formats=request_formats,
                actions=[consent_action, {"type": "wait", "milliseconds": 2000}] + actions,
                onlyMainContent=onlyMainContent,
                timeout=timeout,
                s3_config=s3_config,
                webhook=webhook
            ))
            
            # Job 2: About Popup - Click consent, open popup, take full page screenshot
            target_requests.append(ScrapeRequest(
                url=f"{base_profile_url}?about=1",
                formats=request_formats,
                actions=[
                    consent_action,
                    {"type": "wait", "milliseconds": 1000},
                    {
                        "type": "click",
                        "selector": "button[aria-label^=\"Description\"]:visible, button:has-text('...more'):visible, button:has-text('more links'):visible, ytd-channel-about-metadata-renderer:visible",
                        "timeout": 5000
                    },
                    {"type": "wait", "milliseconds": 2000}
                ] + actions,
                onlyMainContent=onlyMainContent,
                timeout=timeout,
                s3_config=s3_config,
                webhook=webhook
            ))
            
            # Jobs 3-9: Sub-Tabs - Consent, scroll exactly 2780px, take full page screenshot
            for tab in tabs:
                target_requests.append(ScrapeRequest(
                    url=f"{base_profile_url}/{tab}",
                    formats=request_formats,
                    actions=[consent_action] + scroll_actions_2780 + actions,
                    onlyMainContent=onlyMainContent,
                    timeout=timeout,
                    s3_config=s3_config,
                    webhook=webhook
                ))

            # 5. Execute Heterogeneous Batch Scrape
            batch_req = BatchScrapeRequest(
                requests=target_requests,
                timeout=timeout,
                ignoreInvalidURLs=True
            )
            
            batch_response = await client.batch_scrape(batch_req)
            
            if not batch_response.success:
                return {"success": False, "error": "Batch scrape initialization failed."}

            # 6. Format Response
            aggregated_markdown = ""
            aggregated_html = ""
            aggregated_links = {}
            aggregated_screenshots = {}

            tab_names = ["Home", "About"] + [t.capitalize() for t in tabs]

            if batch_response.results:
                for idx, result in enumerate(batch_response.results):
                    # Robust tab matching based on request order, avoiding URL normalization collisions
                    tab_name = tab_names[idx] if idx < len(tab_names) else f"Tab_{idx}"
                        
                    if result.error:
                        aggregated_markdown += f"\n\n# {tab_name}\nError: {result.error}\n"
                        continue

                    if result.markdown:
                        aggregated_markdown += f"\n\n# {tab_name}\n{result.markdown}\n"
                    if result.html:
                        aggregated_html += f"<!-- Tab: {tab_name} -->\n{result.html}\n"
                    if result.links:
                        aggregated_links[tab_name] = result.links
                    if result.screenshot:
                        aggregated_screenshots[tab_name] = result.screenshot
                    elif hasattr(result, "_screenshot_bytes"):
                        import base64
                        b64_str = base64.b64encode(getattr(result, "_screenshot_bytes")).decode('utf-8')
                        aggregated_screenshots[tab_name] = f"data:image/jpeg;base64,{b64_str}"

            data = {}
            if "markdown" in normalized_formats:
                data["markdown"] = aggregated_markdown.strip()
            if "html" in normalized_formats or "rawHtml" in normalized_formats:
                data["html"] = aggregated_html.strip()
            if "links" in normalized_formats:
                data["links"] = aggregated_links
            if "screenshot" in normalized_formats or "screenshots" in normalized_formats or has_screenshot:
                # Return the dictionary mapping tabs to screenshots
                data["screenshots"] = aggregated_screenshots

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
    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
    onlyMainContent: bool = True,
    actions: List[Dict[str, Any]] = [],
    timeout: int = 300000,
    s3_resource: Optional[str] = "f/koda/default_s3",
    webhook: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Scrape a YouTube profile URL. Extracts the channel handle and performs a multi-tab scrape behind the scenes.
    """
    return asyncio.run(_run_youtube_scrape(
        url=url,
        formats=formats,
        onlyMainContent=onlyMainContent,
        actions=actions,
        timeout=timeout,
        s3_resource=s3_resource,
        webhook=webhook,
        **kwargs
    ))
