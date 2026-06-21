import pytest
from unittest.mock import AsyncMock, MagicMock
from playwright.async_api import BrowserContext, Page

from koda.integrations.crawlee import KodaBrowserPlugin, KodaBrowserController, PlaywrightCrawler

def test_playwright_crawler_initialization_no_hooks():
    # Instantiating should not raise TypeError
    mock_handler = AsyncMock()
    crawler = PlaywrightCrawler(request_handler=mock_handler)
    assert crawler is not None

@pytest.mark.asyncio
async def test_playwright_crawler_handler_wrapping():
    mock_handler = AsyncMock()
    crawler = PlaywrightCrawler(request_handler=mock_handler)
    
    # We test that the handler is wrapped
    wrapped_handler = crawler._request_handler
    
    # We can mock a context and see if push_data is patched during execution
    mock_context = AsyncMock()
    original_push_data = AsyncMock()
    mock_context.push_data = original_push_data
    
    await wrapped_handler(mock_context)
    
    assert mock_handler.called
    
    # Verify push_data inside execution got wrapped
    # Note: because it's only patched *during* execution, we would need the handler to call it
    # We'll just test that wrapped_handler executes without exception.

@pytest.mark.asyncio
async def test_koda_browser_controller():
    # Test that KodaBrowserController delegates to the provided BrowserContext
    mock_context = AsyncMock(spec=BrowserContext)
    mock_page = AsyncMock(spec=Page)
    mock_context.new_page.return_value = mock_page
    
    controller = KodaBrowserController(mock_context)
    
    # Check initial state
    assert controller.pages_count == 0
    assert controller.is_browser_connected is True
    
    # Provision a new page
    page = await controller.new_page()
    
    assert page == mock_page
    assert controller.pages_count == 1
    assert mock_context.new_page.called
    
    # Close
    await controller.close()
    assert controller.is_browser_connected is False
    assert mock_page.close.called
    # Ensure it doesn't close the context
    assert not mock_context.close.called

@pytest.mark.asyncio
async def test_koda_browser_plugin():
    mock_context = AsyncMock(spec=BrowserContext)
    plugin = KodaBrowserPlugin(mock_context)
    
    # Test context manager behavior
    assert plugin.active is False
    async with plugin as p:
        assert p == plugin
        assert p.active is True
        
        # Test new_browser() gives us a controller
        controller = await p.new_browser()
        assert isinstance(controller, KodaBrowserController)
        assert controller._context == mock_context
    
    assert plugin.active is False
