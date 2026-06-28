import pytest
from koda.config.main import settings
from koda.use_cases.batch_scrape.schema import BatchScrapeRequest
from koda.use_cases.batch_scrape.service import batch_scrape

@pytest.mark.asyncio
async def test_batch_scrape_e2e(local_test_server):
    """Test batch scraping pages from the local test server."""
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    url1 = f"{local_test_server}/index.html"
    url2 = f"{local_test_server}/page1.html"
    
    try:
        req = BatchScrapeRequest(
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
        result = await batch_scrape(req)
        
        assert result.success is True, f"Batch scrape failed: {getattr(result, 'error', 'Unknown Error')}"
        results = result.data
        
        assert len(results) == 2
        
        # Verify results
        urls_crawled = [r.url for r in results if r.error is None]
        assert url1 in urls_crawled
        assert url2 in urls_crawled
        
        for r in results:
            assert r.markdown and len(r.markdown) > 0, f"Markdown should not be empty for {r.url}"
            if r.url == url1:
                assert "Welcome to the Test Server" in r.markdown
            elif r.url == url2:
                assert "Content for page 1" in r.markdown
                
    finally:
        settings.posthog_api_key = old_key
