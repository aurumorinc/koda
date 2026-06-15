"""Integration tests for KodaClient."""

import pytest
import asyncio
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock, AsyncMock

from koda.client import KodaClient
from koda.modules.page.schema import ScrapeRequest, Action, ScrapeResponse
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
