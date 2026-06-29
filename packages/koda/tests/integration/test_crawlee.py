import os
import pytest
import koda # triggers patching
from koda.client import KodaClient
from crawlee.crawlers import PlaywrightCrawler, PlaywrightCrawlingContext

@pytest.mark.asyncio
async def test_crawlee_headed_propagation(monkeypatch, local_test_server):
    """Test that KODA_HEADLESS=false propagates successfully to the browser config."""
    from koda.modules.browser.service import BrowserSession
    import copy
    
    # Temporarily set KODA_HEADLESS
    monkeypatch.setenv("KODA_HEADLESS", "false")
    
    # Reload settings to capture environment change
    from koda.config.main import Settings, settings
    original_headless = settings.headless
    settings.headless = False
    
    captured_config = {}
    
    # Mock the internal launcher to just capture config
    from koda.modules.browser.service import _LAUNCHERS
    
    original_launcher = _LAUNCHERS.get(settings.browser)
    
    from contextlib import asynccontextmanager
    
    class MockContext:
        async def grant_permissions(self, *args, **kwargs):
            pass
        async def close(self):
            pass
        def on(self, *args, **kwargs):
            pass
        async def route(self, *args, **kwargs):
            pass
        @property
        def pages(self):
            return []
            
    @asynccontextmanager
    async def mock_launcher(user_data_dir, config):
        captured_config.update(config)
        yield MockContext()
        
    _LAUNCHERS[settings.browser] = mock_launcher
    
    try:
        async with BrowserSession() as ctx:
            pass
            
        assert captured_config.get("headless") is False
    finally:
        _LAUNCHERS[settings.browser] = original_launcher
        settings.headless = original_headless


@pytest.mark.asyncio
async def test_crawlee_integration(local_test_server):
    """Test that Crawlee can successfully mount to a BrowserSession and navigate via KodaClient."""
    visited = []
    koda_client_instance = KodaClient()
    
    crawler = PlaywrightCrawler(client=koda_client_instance, headless=True, max_requests_per_crawl=1)  # type: ignore[call-arg]
    
    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        visited.append(context.request.url)
        
    await crawler.run([f"{local_test_server}/index.html"])
    
    assert len(visited) == 1
    assert visited[0] == f"{local_test_server}/index.html"
