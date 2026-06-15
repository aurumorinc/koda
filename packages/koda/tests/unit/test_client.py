"""Integration tests for KodaClient."""

import pytest
import asyncio
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock, AsyncMock

from koda.client import KodaClient
from koda.modules.page.schema import ScrapeRequest, Action, ScrapeResponse
from koda.modules.site.schema import CrawlRequest, CrawlResponse
from koda.modules.webhook.schema import WebhookConfig

@pytest.mark.asyncio
@patch("koda.client.page.scrape")
async def test_kodaclient_scrape_routes_to_page_service(mock_scrape):
    """Test that KodaClient.scrape correctly routes to page.scrape."""
    mock_response = ScrapeResponse(
        url="http://example.com",
        markdown="# Test Content"
    )
    mock_scrape.return_value = mock_response
    
    async with KodaClient() as client:
        request = ScrapeRequest(
            url="http://example.com",
            formats=["markdown"]
        )
        response = await client.scrape(request)
        
        assert response.error is None
        assert response.markdown == "# Test Content"
        mock_scrape.assert_called_once_with(request)

@pytest.mark.asyncio
@patch("koda.client.site.crawl")
async def test_kodaclient_crawl_routes_to_site_service(mock_crawl):
    """Test that KodaClient.crawl correctly routes to site.crawl."""
    mock_response = CrawlResponse(
        success=True,
        id="test-id",
        url="http://example.com",
        total_pages_crawled=5
    )
    mock_crawl.return_value = mock_response
    
    async with KodaClient() as client:
        request = CrawlRequest(
            url="http://example.com",
            limit=5
        )
        response = await client.crawl(request)
        
        assert response.success is True
        assert response.total_pages_crawled == 5
        mock_crawl.assert_called_once_with(request)
