# /// script
# dependencies = [
#   "koda @ git+https://github.com/aurumorinc/koda.git@26.6.17#subdirectory=packages/koda",
# ]
# ///
import asyncio
import wmill
from typing import Optional, List, Dict, Any, Union

from koda import KodaClient, BatchScrapeRequest

async def _run_batch_scrape(
    urls: List[str],
    formats: List[Union[str, Dict[str, Any]]],
    onlyMainContent: bool,
    actions: List[Dict[str, Any]],
    timeout: int,
    s3_resource: Optional[str],
    webhook: Optional[Dict[str, Any]],
    maxConcurrency: Optional[int],
    ignoreInvalidURLs: bool,
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

    # 3. Instantiate Koda Client and Batch Scrape
    try:
        async with KodaClient() as client:
            request = BatchScrapeRequest(
                urls=urls,
                formats=normalized_formats,
                onlyMainContent=onlyMainContent,
                timeout=timeout,
                actions=actions,
                s3_config=s3_config,
                webhook=webhook,
                maxConcurrency=maxConcurrency,
                ignoreInvalidURLs=ignoreInvalidURLs
            )
            response = await client.batch_scrape(request)
            
            return response.model_dump(exclude_none=True)
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main(
    urls: List[str],
    formats: List[Union[str, Dict[str, Any]]] = ["markdown"],
    onlyMainContent: bool = True,
    actions: List[Dict[str, Any]] = [],
    timeout: int = 60000,
    s3_resource: Optional[str] = "f/koda/default_s3",
    webhook: Optional[Dict[str, Any]] = None,
    maxConcurrency: Optional[int] = None,
    ignoreInvalidURLs: bool = True,
    **kwargs
) -> Dict[str, Any]:
    """
    Scrape multiple URLs concurrently and extract information using Koda.
    """
    return asyncio.run(_run_batch_scrape(
        urls=urls,
        formats=formats,
        onlyMainContent=onlyMainContent,
        actions=actions,
        timeout=timeout,
        s3_resource=s3_resource,
        webhook=webhook,
        maxConcurrency=maxConcurrency,
        ignoreInvalidURLs=ignoreInvalidURLs,
        **kwargs
    ))
