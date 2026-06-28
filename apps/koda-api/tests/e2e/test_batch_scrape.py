import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import import_script  # type: ignore
from koda.config.main import settings

batch_scrape_script = import_script("f/koda/batch_scrape.py", "batch_scrape")


@pytest.mark.asyncio
async def test_batch_scrape_e2e(local_test_server, wmill_mock):
    """Test batch scraping pages from the local test server via the Windmill script."""
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    url1 = f"{local_test_server}/index.html"
    url2 = f"{local_test_server}/page1.html"
    
    try:
        result = await batch_scrape_script.main(
            urls=[url1, url2],
            formats=["markdown"],
            onlyMainContent=False,
            actions=[],
            timeout=60000,
            s3_resource=None,
            webhook=None,
            maxConcurrency=2,
            ignoreInvalidURLs=True
        )
        
        assert result.get("success") is True, f"Batch scrape failed: {result.get('error')}"
        results = result.get("data", result.get("results", []))
        
        assert len(results) == 2
        
        # Verify results
        urls_crawled = [r["url"] for r in results if r.get("error") is None]
        assert url1 in urls_crawled
        assert url2 in urls_crawled
        
        for r in results:
            assert len(r.get("markdown", "")) > 0, f"Markdown should not be empty for {r['url']}"
            if r["url"] == url1:
                assert "Welcome to the Test Server" in r["markdown"]
            elif r["url"] == url2:
                assert "Content for page 1" in r["markdown"]
                
    finally:
        settings.posthog_api_key = old_key
