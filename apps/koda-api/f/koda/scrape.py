# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.16.0#subdirectory=packages/koda",
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
import uuid
from typing import Optional, List, Dict, Any, Union

from oort.webhook.schema import WebhookRequest as Webhook
from koda import settings
from koda.use_cases.schema import Action
from koda.use_cases.scrape.schema import ScrapeRequest
from koda.use_cases.scrape.service import scrape

def main(
    url: str,
    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
    onlyMainContent: bool = True,
    actions: List[Action] = [],
    timeout: int = 60000,
    webhook: Optional[Webhook] = None,
) -> dict:
    """
    Scrape a single URL and extract information using Koda infrastructure.
    """
    normalized_formats = []
    if formats:
        for f in formats:
            if isinstance(f, dict):
                normalized_formats.append(f.get("type", ""))
            else:
                normalized_formats.append(str(f))
                
    request = ScrapeRequest(
        url=url,
        formats=normalized_formats,
        onlyMainContent=onlyMainContent,
        timeout=timeout or settings.timeout,
        actions=actions,
        webhook=webhook
    )

    try:
        result = asyncio.run(scrape(request))
        return result.model_dump(by_alias=True, exclude_none=True)
    except Exception as e:
        return {"success": False, "error": str(e)}
