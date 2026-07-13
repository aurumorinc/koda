# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.13.0#subdirectory=packages/koda",
# ]
# ///
import asyncio
import wmill  # type: ignore
from typing import Optional, List, Dict, Any, Union

from koda import Webhook
from koda.use_cases.scrape_youtube_profile.schema import ScrapeYoutubeProfileRequest
from koda.use_cases.scrape_youtube_profile.service import scrape_youtube_profile

def main(
    url: str,
    formats: List[Union[str, Dict[str, Any]]] = ["screenshot"],
    timeout: int = 600000,
    webhook: Optional[Webhook] = None,
    max_concurrency: int = 1,
) -> dict:
    """
    Scrape a YouTube profile URL. Extracts the channel handle and performs a multi-tab scrape behind the scenes.
    Uses Crawlee for orchestration and Playwright automation, passing S3/Webhook to global settings.
    """
    
    s3_resource = None

    try:
        s3_resource = wmill.get_resource("f/koda/default_s3")
    except Exception:
        pass

    kwargs_request = {
        "url": url,
        "formats": formats,
        "timeout": timeout,
        "s3_resource": s3_resource,
        "webhook": webhook,
        "max_concurrency": max_concurrency,
    }
    request = ScrapeYoutubeProfileRequest(**kwargs_request)
    
    try:
        response = asyncio.run(scrape_youtube_profile(request))
        if response.data:
            from koda.utils.file.main import File
            for item in response.data:
                if "screenshot" in item and isinstance(item["screenshot"], File):
                    f = item["screenshot"]
                    item["screenshot"] = f.presigned_url or f.base64
                    f.cleanup()
        return response.model_dump(exclude_none=True)
    except Exception as e:
        return {"success": False, "error": str(e)}
