import asyncio
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from koda.client import KodaClient
from koda.exceptions import TimeoutError, BrowserLaunchError
from koda.integrations.crawlee import KodaPlaywrightCrawler, KodaBrowserController
from playwright.async_api import BrowserContext

@pytest.mark.asyncio
async def test_koda_playwright_crawler_timeout():
    """Test that KodaPlaywrightCrawler raises TimeoutError when run takes too long."""
    async with KodaClient(timeout=100) as client:
        # We need to mock super().run so it sleeps for longer than the timeout
        OriginalCrawler = KodaPlaywrightCrawler.__bases__[0]
        with patch.object(OriginalCrawler, "run", new_callable=AsyncMock) as mock_super_run:
            async def mock_run(*args, **kwargs):
                await asyncio.sleep(0.5)
            mock_super_run.side_effect = mock_run
            
            crawler = KodaPlaywrightCrawler(client=client)
            
            with pytest.raises(TimeoutError, match="Crawler execution timed out."):
                await crawler.run([])

@pytest.mark.asyncio
async def test_koda_browser_controller_crash():
    """Test that KodaBrowserController catches TargetClosedError and marks _is_closed."""
    
    mock_context = MagicMock(spec=BrowserContext)
    
    # Simulate Playwright throwing TargetClosedError
    class PlaywrightError(Exception):
        pass
        
    mock_context.new_page = AsyncMock(side_effect=PlaywrightError("TargetClosedError: Target page, context or browser has been closed"))
    
    controller = KodaBrowserController(mock_context)
    
    with pytest.raises(BrowserLaunchError, match="Browser crashed or context closed prematurely"):
        await controller.new_page()
        
    assert controller._is_closed is True
    assert controller.is_browser_connected is False

@pytest.mark.asyncio
async def test_koda_browser_controller_protocol_error():
    """Test that KodaBrowserController catches protocol errors and marks _is_closed."""
    
    mock_context = MagicMock(spec=BrowserContext)
    
    # Simulate Playwright throwing Protocol error
    class PlaywrightError(Exception):
        pass
        
    mock_context.new_page = AsyncMock(side_effect=PlaywrightError("Page.goto: Protocol error (Page.navigate): can't access property 'loadURI', browsingContext is undefined."))
    
    controller = KodaBrowserController(mock_context)
    
    with pytest.raises(BrowserLaunchError, match="Browser crashed or context closed prematurely"):
        await controller.new_page()
        
    assert controller._is_closed is True
    assert controller.is_browser_connected is False
