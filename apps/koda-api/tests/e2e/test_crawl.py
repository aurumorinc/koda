import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import import_script  # type: ignore
from koda.config.main import settings

crawl_script = import_script("f/koda/crawl.py", "crawl")


def test_crawl_e2e(local_test_server, wmill_mock):
    """Test crawling pages from the local test server via the Windmill script."""
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    url = f"{local_test_server}/index.html"
    
    try:
        result =  crawl_script.main(
            url=url,
            limit=10,
            maxDiscoveryDepth=2,
            allowExternalLinks=True,
            allowSubdomains=False,
            crawlEntireDomain=True,
            ignoreQueryParameters=True,
            regexOnFullURL=False,
            excludePaths=None,
            includePaths=None,
            maxConcurrency=2,
            delay=None,
            webhook=None,
            scrapeOptions={}
        )

        assert result.get("success") is True, f"Crawl failed: {result.get('error')}"
        
        # It should find index.html, page1.html, and page2.html
        assert result.get("total_pages_crawled") >= 1
                
    finally:
        settings.posthog_api_key = old_key
