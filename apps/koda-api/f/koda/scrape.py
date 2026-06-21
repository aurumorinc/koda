# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@26.6.38#subdirectory=packages/koda",
# ]
# ///
import asyncio
import wmill
from typing import Optional, List, Dict, Any, Union

from koda import KodaClient, ScrapeRequest

async def _run_scrape(
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

    # 2. Normalize Formats (Windmill UI sometimes sends dicts)
    normalized_formats = []
    if formats:
        for f in formats:
            if isinstance(f, dict):
                normalized_formats.append(f.get("type", ""))
            else:
                normalized_formats.append(str(f))

    # 3. Instantiate Koda Client and Scrape
    try:
        async with KodaClient() as client:
            request = ScrapeRequest(
                url=url,
                formats=normalized_formats,
                onlyMainContent=onlyMainContent,
                timeout=timeout,
                actions=actions,
                s3_config=s3_config,
                webhook=webhook
            )
            response = await client.scrape(request)
            
            if response.error:
                return {
                    "success": False,
                    "error": response.error
                }
                
            data = {}
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
    timeout: int = 60000,
    s3_resource: Optional[str] = "f/koda/default_s3",
    webhook: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Scrape a single URL and extract information using Koda.
    """
    return asyncio.run(_run_scrape(
        url=url,
        formats=formats,
        onlyMainContent=onlyMainContent,
        actions=actions,
        timeout=timeout,
        s3_resource=s3_resource,
        webhook=webhook,
        **kwargs
    ))
