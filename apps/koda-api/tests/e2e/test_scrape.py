import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import import_script
from koda.config.main import settings

scrape_script = import_script("f/koda/scrape.py", "scrape")

@pytest.mark.asyncio
async def test_scrape_e2e(local_test_server, wmill_mock):
    """Test scraping a page from the local test server via the Windmill script."""
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    url = f"{local_test_server}/index.html"
    
    try:
        result = await scrape_script.main(
            url=url,
            formats=["markdown", "html", "links"],
            onlyMainContent=False,
            actions=[],
            timeout=60000,
            s3_resource=None,
            webhook=None
        )
        
        assert result.get("success") is True, f"Scrape failed: {result.get('error')}"
        data = result.get("data", {})
        
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
