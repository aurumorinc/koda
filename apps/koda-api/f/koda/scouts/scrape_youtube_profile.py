# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.15.2#subdirectory=packages/koda",
# ]
# ///
import os
import wmill  # type: ignore

try:
    _s3 = wmill.get_resource("f/koda/default_s3")
    if _s3:
        os.environ["S3_BUCKET"] = _s3.get("bucket", "")
        os.environ["S3_ENDPOINT_URL"] = _s3.get("endPoint", "")
        os.environ["S3_REGION"] = _s3.get("region", "")
        os.environ["S3_ACCESS_KEY"] = _s3.get("accessKey", "")
        os.environ["S3_SECRET_KEY"] = _s3.get("secretKey", "")
except Exception:
    pass

import asyncio
from typing import Optional, List, Dict, Any, Union

from oort.webhook.schema import WebhookRequest as Webhook
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
    Uses Crawlee for orchestration and Playwright automation, passing Webhook to global settings.
    """
    
    kwargs_request = {
        "url": url,
        "formats": formats,
        "timeout": timeout,
        "webhook": webhook,
        "max_concurrency": max_concurrency,
    }
    request = ScrapeYoutubeProfileRequest(**kwargs_request)
    
    try:
        response = asyncio.run(scrape_youtube_profile(request))
        if response.data:
            from oort.file.main import File
            for item in response.data:
                if "screenshot" in item and isinstance(item["screenshot"], File):
                    f = item["screenshot"]
                    item["screenshot"] = f.presigned_url or f.base64
                    f.cleanup()
        return response.model_dump(exclude_none=True)
    except Exception as e:
        return {"success": False, "error": str(e)}
