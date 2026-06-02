import pytest
import sys
from unittest.mock import MagicMock, patch, AsyncMock
from koda.infrastructure.crawl4ai import patch_crawl4ai

# Create a dummy class to represent AsyncWebCrawler
class DummyAsyncWebCrawler:
    def __init__(self, *args, **kwargs):
        pass
    async def arun(self, url: str, *args, **kwargs):
        pass
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

class DummyBrowserManager:
    async def start(self):
        pass
    async def close(self):
        pass
    async def get_page(self, crawlerRunConfig):
        return MagicMock(), MagicMock()
    async def create_browser_context(self, crawlerRunConfig=None):
        pass
    def _compute_browser_endpoint_key(self):
        return "mock_key"

@pytest.fixture(autouse=True)
def mock_crawl4ai_modules():
    mock_crawl4ai = MagicMock()
    mock_crawl4ai.AsyncWebCrawler = DummyAsyncWebCrawler
    
    mock_crawl4ai_bm = MagicMock()
    mock_crawl4ai_bm.BrowserManager = DummyBrowserManager
    
    with patch.dict("sys.modules", {
        "crawl4ai": mock_crawl4ai,
        "crawl4ai.browser_manager": mock_crawl4ai_bm
    }):
        yield

@pytest.fixture(autouse=True)
def reset_patch_state():
    import koda.infrastructure.crawl4ai as c4
    c4._patched = False
    # Restore original arun
    DummyAsyncWebCrawler.arun = AsyncMock(return_value=MagicMock(success=True, status_code=200, error_message=None))
    yield
    c4._patched = False

@pytest.mark.asyncio
async def test_patch_crawl4ai_patches_browser_manager():
    # Verify methods are original
    assert DummyBrowserManager.start != patch_crawl4ai
    
    patch_crawl4ai("phc_mock_key", "https://mock.posthog.com")
    
    # Verify methods are patched
    assert DummyBrowserManager.start.__name__ == "patched_start"
    assert DummyBrowserManager.close.__name__ == "patched_close"
    assert DummyBrowserManager.create_browser_context.__name__ == "patched_create_browser_context"
    assert DummyBrowserManager.get_page.__name__ == "patched_get_page"
