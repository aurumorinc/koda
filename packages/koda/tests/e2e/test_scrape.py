import pytest
import asyncio

from koda.client import KodaClient
from koda.modules.page.schema import ScrapeRequest, Action

from koda.config.main import settings

@pytest.mark.asyncio
async def test_scrape_local_server(local_test_server):
    """Test scraping a page from the local test server."""
    # Set mock posthog key to exercise telemetry paths
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    url = f"{local_test_server}/index.html"
    
    async with KodaClient() as client:
        request = ScrapeRequest(
            url=url,
            formats=["markdown", "html", "metadata", "links"],
            only_main_content=False
        )
        try:
            response = await client.scrape(request)
            
            assert response.error is None
            assert response.url == url
            
            # Check markdown content
            assert "Welcome to the Test Server" in response.markdown
            assert "This is the main content." in response.markdown
            
            # Check HTML content
            assert "<h1>Welcome to the Test Server</h1>" in response.html
            
            # Check metadata
            assert response.metadata is not None
            assert response.metadata.get("title") == "Test Index"
            
            # Check links
            assert response.links is not None
            internal_links = [link.get("href") for link in response.links.get("internal", [])]
            assert any("page1.html" in link for link in internal_links)
            assert any("page2.html" in link for link in internal_links)
        finally:
            settings.posthog_api_key = old_key

@pytest.mark.asyncio
async def test_scrape_with_actions(local_test_server):
    """Test scraping a page with actions (clicking a button to reveal text)."""
    url = f"{local_test_server}/index.html"
    
    async with KodaClient() as client:
        # First, scrape without action to ensure text is hidden/not in main content
        # Note: crawl4ai might still extract hidden text depending on its pruning strategy,
        # but we definitely want to see it after the action.
        
        # Now scrape with the click action
        action = Action(type="click", selector="#reveal-btn")
        request = ScrapeRequest(
            url=url,
            formats=["markdown"],
            actions=[action],
            only_main_content=False
        )
        response = await client.scrape(request)
        
        assert response.error is None
        assert "Hidden Content Revealed!" in response.markdown

@pytest.mark.asyncio
async def test_scrape_example_com():
    """Test scraping example.com."""
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    try:
        async with KodaClient() as client:
            request = ScrapeRequest(
                url="https://example.com",
                formats=["markdown", "html"],
                only_main_content=False
            )
            response = await client.scrape(request)
            
            assert response.error is None
            assert "Example Domain" in response.markdown
    finally:
        settings.posthog_api_key = old_key

@pytest.mark.asyncio
async def test_scrape_google_com():
    """Test scraping google.com (has strict CSP)."""
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    try:
        async with KodaClient() as client:
            request = ScrapeRequest(
                url="https://google.com",
                formats=["markdown", "html"],
                only_main_content=False
            )
            response = await client.scrape(request)

            # Google should not timeout now that we patched the evaluation deadlock
            assert response.error is None, f"Expected success but got error: {response.error}"
            assert response.markdown is not None, "Expected markdown to be extracted"
    finally:
        settings.posthog_api_key = old_key

@pytest.mark.asyncio
async def test_scrape_linkedin_com():
    """Test scraping linkedin.com (has strict anti-bot)."""
    old_key = settings.posthog_api_key
    settings.posthog_api_key = "mock_e2e_key"
    
    try:
        async with KodaClient() as client:
            request = ScrapeRequest(
                url="https://linkedin.com",
                formats=["markdown", "html"],
                only_main_content=False
            )
            response = await client.scrape(request)
            
            # LinkedIn should not timeout, though it might return a captcha. We just want to ensure it completes.
            assert response.error is None, f"Expected success but got error: {response.error}"
            assert response.markdown is not None, "Expected markdown to be extracted"
    finally:
        settings.posthog_api_key = old_key
