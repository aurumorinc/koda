import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from koda.integrations.crawl4ai import KodaBrowserManager, Crawl4AiTool, KodaAsyncWebCrawler

def test_crawl4ai_module_patching():
    # Verify that the native crawl4ai library has been patched
    import crawl4ai
    assert crawl4ai.AsyncWebCrawler is KodaAsyncWebCrawler

@pytest.mark.asyncio
@patch("koda.modules.browser.service.BrowserSession")
async def test_koda_async_web_crawler_lifecycle(mock_browser_session_cls):
    mock_session = AsyncMock()
    mock_browser_session_cls.return_value = mock_session
    mock_context = AsyncMock()
    mock_session.__aenter__.return_value = mock_context
    
    mock_client = MagicMock()
    crawler = KodaAsyncWebCrawler(client=mock_client)
    
    # Since we monkeypatched crawl4ai.AsyncWebCrawler, we need to patch the actual base class
    # which is accessible via KodaAsyncWebCrawler.__bases__[0]
    BaseClass = crawler.__class__.__bases__[0]
    with patch.object(BaseClass, "start", new_callable=AsyncMock) as mock_super_start:
        with patch.object(BaseClass, "close", new_callable=AsyncMock) as mock_super_close:
            await crawler.start()

            assert crawler._koda_session == mock_session
            mock_session.__aenter__.assert_called_once()
            mock_super_start.assert_called_once()
            
            await crawler.close()
            
            mock_super_close.assert_called_once()
            mock_session.__aexit__.assert_called_once()
            assert crawler._koda_session is None

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
    from crawl4ai import CrawlerRunConfig
    page, context = await manager.get_page(CrawlerRunConfig())
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
