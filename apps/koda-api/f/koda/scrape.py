# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@0.10.4#subdirectory=packages/koda",
# ]
# ///
import asyncio
import uuid
import wmill  # type: ignore
from typing import Optional, List, Dict, Any, Union

from koda import Webhook, settings
from koda.use_cases.schema import Action
from koda.use_cases.scrape.schema import ScrapeRequest
from koda.use_cases.scrape.service import scrape

def main(
    url: str,
    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
    onlyMainContent: bool = True,
    actions: List[Action] = [],
    timeout: int = 60000,
    s3_resource: Optional[str] = "f/koda/default_s3",
    webhook: Optional[Webhook] = None,
) -> dict:
    """
    Scrape a single URL and extract information using Koda infrastructure.
    """
    s3_dict = None
    if s3_resource:
        try:
            s3_dict = wmill.get_resource(s3_resource)
        except Exception:
            pass
        if not s3_dict:
            return {"success": False, "error": f"S3 Resource '{s3_resource}' not found."}

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
        s3_resource=s3_dict,
        webhook=webhook
    )

    try:
        result = asyncio.run(scrape(request))
        return result.model_dump(by_alias=True, exclude_none=True)
    except Exception as e:
        return {"success": False, "error": str(e)}
