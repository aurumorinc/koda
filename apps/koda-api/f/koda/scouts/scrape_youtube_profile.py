# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.6.0#subdirectory=packages/koda",
# ]
# ///
import wmill  # type: ignore
from typing import Optional, List, Dict, Any, Union

from koda import Webhook
from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest
from koda.use_cases.scrape_youtube_profile.service import scrape_youtube_profile

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
    maxConcurrency = kwargs.pop("maxConcurrency", 1)
    
    s3_dict = None
    if s3_resource:
        try:
            s3_dict = wmill.get_resource(s3_resource)
        except Exception:
            pass
        if not s3_dict:
            return {"success": False, "error": f"S3 Resource '{s3_resource}' not found."}

    request = ScrapeYoutubeProfileRequest(
        url=url,
        formats=formats,
        timeout=timeout,
        s3_resource=s3_dict,
        webhook=webhook,
        maxConcurrency=maxConcurrency
    )
    
    response = await scrape_youtube_profile(request)
    return response.model_dump(exclude_none=True)
