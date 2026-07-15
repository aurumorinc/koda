# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.14.0#subdirectory=packages/koda",
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
from koda.use_cases.batch_scrape.schema import BatchScrapeRequest
from koda.use_cases.batch_scrape.service import batch_scrape

def main(
    urls: List[str] = [],
    requests: List[ScrapeRequest] = [],
    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
    onlyMainContent: bool = True,
    actions: List[Action] = [],
    timeout: int = 60000,
    webhook: Optional[Webhook] = None,
    maxConcurrency: int = 10,
    ignoreInvalidURLs: bool = True,
) -> dict:
    """
    Scrape a batch of URLs concurrently using Koda infrastructure.
    """
    normalized_formats = []
    if formats:
        for f in formats:
            if isinstance(f, dict):
                normalized_formats.append(f.get("type", ""))
            else:
                normalized_formats.append(str(f))
                
    request = BatchScrapeRequest(
        urls=urls,
        requests=requests,
        formats=normalized_formats,
        onlyMainContent=onlyMainContent,
        timeout=timeout or settings.timeout,
        actions=actions,
        webhook=webhook,
        maxConcurrency=maxConcurrency,
        ignoreInvalidURLs=ignoreInvalidURLs
    )
    
    try:
        response = asyncio.run(batch_scrape(request))
        return response.model_dump(by_alias=True, exclude_none=True)
    except Exception as e:
        return {"success": False, "id": uuid.uuid4().hex, "data": [], "error": str(e)}
