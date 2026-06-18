import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

from koda.client import KodaClient
from koda.modules.site.schema import CrawlRequest
from koda.modules.webhook.schema import WebhookConfig

@pytest.fixture
def mock_browser_session():
    from contextlib import asynccontextmanager
    @asynccontextmanager
    async def _mock_session():
        yield AsyncMock()
    return _mock_session

@pytest.mark.asyncio
@patch("koda.modules.site.service.BrowserSession")
@patch("koda.modules.site.service.Crawl4AiTool")
async def test_crawl_success_basic(mock_tool_class, mock_browser_session_class, mock_browser_session):
    """Test basic successful crawl."""
    mock_browser_session_class.return_value = mock_browser_session()
    mock_tool = AsyncMock()
    
    mock_result_1 = MagicMock()
    mock_result_1.success = True
    mock_result_1.url = "http://example.com"
    
    mock_result_2 = MagicMock()
    mock_result_2.success = True
    mock_result_2.url = "http://example.com/page1"
    
    async def mock_execute_stream(*args, **kwargs):
        yield mock_result_1
        yield mock_result_2
        
    mock_tool.execute_stream = mock_execute_stream
    mock_tool_class.return_value = mock_tool

    async with KodaClient() as client:
        # For simplicity, sitemap="skip" bypasses seeder in this test
        request = CrawlRequest(url="http://example.com", limit=2, maxDiscoveryDepth=1, sitemap="skip")
        response = await client.crawl(request)

        assert response.success is True
        assert response.total_pages_crawled == 2

@pytest.mark.asyncio
@patch("koda.modules.site.service.BrowserSession")
@patch("koda.modules.site.service.Crawl4AiTool")
async def test_crawl_respects_depth_limit(mock_tool_class, mock_browser_session_class, mock_browser_session):
    mock_browser_session_class.return_value = mock_browser_session()
    """Test crawl respects limit constraint."""
    mock_tool = AsyncMock()
    
    mock_result_0 = MagicMock()
    mock_result_0.success = True
    mock_result_0.url = "http://example.com"
    
    mock_result_1 = MagicMock()
    mock_result_1.success = True
    mock_result_1.url = "http://example.com/depth1"
    
    mock_result_2 = MagicMock()
    mock_result_2.success = True
    mock_result_2.url = "http://example.com/depth2"
    
    async def mock_execute_stream(*args, **kwargs):
        yield mock_result_0
        yield mock_result_1
        yield mock_result_2 # The service loop should break before using this if limit is hit
        
    mock_tool.execute_stream = mock_execute_stream
    mock_tool_class.return_value = mock_tool

    async with KodaClient() as client:
        request = CrawlRequest(
            url="http://example.com",
            limit=2,
            maxDiscoveryDepth=1,
            sitemap="skip"
        )
        response = await client.crawl(request)

        assert response.success is True
        assert response.total_pages_crawled == 2

@pytest.mark.asyncio
@patch("koda.modules.site.service.BrowserSession")
@patch("koda.modules.site.service.Crawl4AiTool")
@patch("koda.modules.site.service.dispatch_webhook")
async def test_crawl_webhook_dispatch(mock_dispatch, mock_tool_class, mock_browser_session_class, mock_browser_session):
    mock_browser_session_class.return_value = mock_browser_session()
    """Test crawl webhook dispatching."""
    mock_tool = AsyncMock()
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.url = "http://example.com"
    mock_result.links = {"internal": []}
    mock_result.markdown = "# Test"
    mock_result.metadata = {"title": "Test"}
    
    async def mock_execute_stream(*args, **kwargs):
        yield mock_result
        
    mock_tool.execute_stream = mock_execute_stream
    mock_tool_class.return_value = mock_tool

    async with KodaClient() as client:
        webhook_config = WebhookConfig(url="http://webhook.example.com")
        request = CrawlRequest(
            url="http://example.com",
            limit=1,
            webhook=webhook_config,
            sitemap="skip"
        )
        response = await client.crawl(request)

        assert response.success is True
        assert mock_dispatch.call_count == 3 # started, page, completed
        
        calls = mock_dispatch.call_args_list
        assert calls[0][0][1] == "crawl.started"
        assert calls[1][0][1] == "crawl.page"
        assert calls[2][0][1] == "crawl.completed"
