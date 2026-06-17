import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from koda.integrations.crawl4ai import KodaBrowserManager, Crawl4AiTool

@pytest.mark.asyncio
async def test_koda_browser_manager():
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    mock_context.new_page.return_value = mock_page

    manager = KodaBrowserManager(context=mock_context)
    
    # start and close should be no-ops
    await manager.start()
    await manager.close()
    
    # get_page should return a new page from the context
    page, context = await manager.get_page(None)
    assert page == mock_page
    assert context == mock_context
    mock_context.new_page.assert_called_once()

@pytest.mark.asyncio
@patch("koda.integrations.crawl4ai.AsyncWebCrawler")
async def test_crawl4ai_tool_single_url(mock_crawler_cls):
    mock_crawler = AsyncMock()
    mock_crawler_cls.return_value.__aenter__.return_value = mock_crawler
    
    mock_context = AsyncMock()
    
    tool = Crawl4AiTool()
    request = {
        "url": "https://example.com",
        "run_config": MagicMock()
    }
    
    await tool.execute(mock_context, request)
    
    mock_crawler.arun.assert_called_once()
    assert mock_crawler.arun.call_args[1]["url"] == "https://example.com"

@pytest.mark.asyncio
@patch("koda.integrations.crawl4ai.AsyncWebCrawler")
async def test_crawl4ai_tool_batch_urls(mock_crawler_cls):
    mock_crawler = AsyncMock()
    mock_crawler_cls.return_value.__aenter__.return_value = mock_crawler
    
    mock_context = AsyncMock()
    
    tool = Crawl4AiTool()
    request = {
        "urls": ["https://example.com/1", "https://example.com/2"],
        "run_config": MagicMock()
    }
    
    await tool.execute(mock_context, request)
    
    mock_crawler.arun_many.assert_called_once()
    assert mock_crawler.arun_many.call_args[1]["urls"] == ["https://example.com/1", "https://example.com/2"]
