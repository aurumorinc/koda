import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

from koda.client import KodaClient
from koda.modules.site.schema import CrawlRequest
from koda.modules.webhook.schema import WebhookConfig

@pytest.mark.asyncio
@patch("koda.modules.site.service.AsyncWebCrawler")
async def test_crawl_success_basic(mock_crawler_class):
    """Test basic successful crawl."""
    mock_crawler = AsyncMock()
    
    # Mock results for two pages
    mock_result_1 = MagicMock()
    mock_result_1.success = True
    mock_result_1.url = "http://example.com"
    mock_result_1.links = {"internal": [{"href": "http://example.com/page1"}]}
    
    mock_result_2 = MagicMock()
    mock_result_2.success = True
    mock_result_2.url = "http://example.com/page1"
    mock_result_2.links = {"internal": []}
    
    # arun_many returns a list of results for the batch
    mock_crawler.arun_many.side_effect = [
        [mock_result_1],
        [mock_result_2]
    ]
    
    mock_crawler_class.return_value.__aenter__.return_value = mock_crawler

    async with KodaClient() as client:
        request = CrawlRequest(url="http://example.com", limit=2, maxDiscoveryDepth=1)
        response = await client.crawl(request)

        assert response.success is True
        assert response.total_pages_crawled == 2
        assert mock_crawler.arun_many.call_count == 2

@pytest.mark.asyncio
@patch("koda.modules.site.service.AsyncWebCrawler")
async def test_crawl_respects_depth_limit(mock_crawler_class):
    """Test crawl respects maxDiscoveryDepth."""
    mock_crawler = AsyncMock()
    
    # Depth 0
    mock_result_0 = MagicMock()
    mock_result_0.success = True
    mock_result_0.url = "http://example.com"
    mock_result_0.links = {"internal": [{"href": "http://example.com/depth1"}]}
    
    # Depth 1
    mock_result_1 = MagicMock()
    mock_result_1.success = True
    mock_result_1.url = "http://example.com/depth1"
    mock_result_1.links = {"internal": [{"href": "http://example.com/depth2"}]}
    
    # Depth 2 (should not be crawled if maxDiscoveryDepth=1)
    mock_result_2 = MagicMock()
    mock_result_2.success = True
    mock_result_2.url = "http://example.com/depth2"
    mock_result_2.links = {"internal": []}
    
    mock_crawler.arun_many.side_effect = [
        [mock_result_0],
        [mock_result_1],
        [mock_result_2] # This shouldn't be reached
    ]
    
    mock_crawler_class.return_value.__aenter__.return_value = mock_crawler

    async with KodaClient() as client:
        request = CrawlRequest(
            url="http://example.com", 
            limit=10,
            maxDiscoveryDepth=1
        )
        response = await client.crawl(request)

        assert response.success is True
        assert response.total_pages_crawled == 2
        assert mock_crawler.arun_many.call_count == 2

@pytest.mark.asyncio
@patch("koda.modules.site.service.AsyncWebCrawler")
@patch("koda.modules.site.service.dispatch_webhook")
async def test_crawl_webhook_dispatch(mock_dispatch, mock_crawler_class):
    """Test crawl webhook dispatching."""
    mock_crawler = AsyncMock()
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.url = "http://example.com"
    mock_result.links = {"internal": []}
    mock_result.markdown = "# Test"
    mock_result.metadata = {"title": "Test"}
    
    mock_crawler.arun_many.return_value = [mock_result]
    mock_crawler_class.return_value.__aenter__.return_value = mock_crawler

    async with KodaClient() as client:
        webhook_config = WebhookConfig(url="http://webhook.example.com")
        request = CrawlRequest(
            url="http://example.com", 
            limit=1,
            webhook=webhook_config
        )
        response = await client.crawl(request)

        assert response.success is True
        assert mock_dispatch.call_count == 3 # started, page, completed
        
        calls = mock_dispatch.call_args_list
        assert calls[0][0][1] == "crawl.started"
        assert calls[1][0][1] == "crawl.page"
        assert calls[2][0][1] == "crawl.completed"
