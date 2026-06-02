import asyncio
import wmill
from typing import Dict, Any

from koda.schemas.site_schema import CrawlRequest
from koda.services.site_service import crawl

async def main(**kwargs) -> Dict[str, Any]:
    """
    Crawl a site starting from a URL and extract information using Koda.
    """
    try:
        # Parse and validate the incoming payload
        request = CrawlRequest(**kwargs)
        
        # Execute the crawl
        response = await crawl(request)
        
        return response.model_dump()
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
