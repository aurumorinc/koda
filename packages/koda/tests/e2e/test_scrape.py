import pytest
from koda.config.main import settings
from koda.use_cases.scrape.schema import ScrapeRequest
from koda.use_cases.scrape.service import scrape

@pytest.mark.asyncio
async def test_scrape_e2e(local_test_server):
    """Test scraping a page from the local test server."""
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    url = f"{local_test_server}/index.html"
    
    try:
        req = ScrapeRequest(
            url=url,
            formats=["markdown", "html", "links"],
            onlyMainContent=False,
            actions=[],
            timeout=60000,
            s3_resource=None,
            webhook=None
        )
        
        result = await scrape(req)
        
        assert result.success is True, f"Scrape failed: {getattr(result, 'error', 'Unknown error')}"
        data = result.data or {}
        
        # Check markdown content
        assert "markdown" in data
        assert len(data["markdown"]) > 0, "Markdown should not be empty"
        assert "Welcome to the Test Server" in data["markdown"]
        
        # Check HTML content
        assert "html" in data
        assert "<h1>Welcome to the Test Server</h1>" in data["html"]
        
        # Check links
        assert "links" in data
        internal_links = [link.get("href") for link in data["links"].get("internal", [])]
        assert any("page1.html" in link for link in internal_links)
        
    finally:
        settings.posthog_api_key = old_key
