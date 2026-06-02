import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from koda.modules.site.schema import CrawlRequest
from koda.modules.site.service import crawl, _is_valid_link

def test_is_valid_link():
    base_url = "https://example.com/docs"
    
    # Test external links
    assert _is_valid_link("https://other.com", base_url, None, None, False, False, True, False) is True
    assert _is_valid_link("https://other.com", base_url, None, None, False, False, False, False) is False
    
    # Test subdomains
    assert _is_valid_link("https://sub.example.com", base_url, None, None, True, False, False, False) is True
    assert _is_valid_link("https://sub.example.com", base_url, None, None, False, False, False, False) is False
    
    # Test domain scope
    assert _is_valid_link("https://example.com/blog", base_url, None, None, False, True, False, False) is True
    assert _is_valid_link("https://example.com/blog", base_url, None, None, False, False, False, False) is False
    assert _is_valid_link("https://example.com/docs/api", base_url, None, None, False, False, False, False) is True
    
    # Test exclude paths
    assert _is_valid_link("https://example.com/docs/api", base_url, None, ["/api"], False, False, False, False) is False
    
    # Test include paths
    assert _is_valid_link("https://example.com/docs/api", base_url, ["/api"], None, False, False, False, False) is True
    assert _is_valid_link("https://example.com/docs/other", base_url, ["/api"], None, False, False, False, False) is False

@pytest.mark.asyncio
async def test_crawl_basic():
    request = CrawlRequest(url="https://example.com", limit=2, maxDiscoveryDepth=1)
    
    mock_result_1 = MagicMock()
    mock_result_1.success = True
    mock_result_1.url = "https://example.com"
    mock_result_1.links = {"internal": [{"href": "https://example.com/page1"}, {"href": "https://example.com/page2"}]}
    
    mock_result_2 = MagicMock()
    mock_result_2.success = True
    mock_result_2.url = "https://example.com/page1"
    mock_result_2.links = {"internal": []}
    
    with patch("koda.modules.site.service.AsyncWebCrawler") as mock_crawler_cls:
        mock_crawler = AsyncMock()
        mock_crawler_cls.return_value.__aenter__.return_value = mock_crawler
        
        # First batch returns root, second batch returns page1
        mock_crawler.arun_many.side_effect = [[mock_result_1], [mock_result_2]]
        
        response = await crawl(request)
        
        assert response.success is True
        assert response.total_pages_crawled == 2
        assert mock_crawler.arun_many.call_count == 2

@pytest.mark.asyncio
async def test_crawl_with_webhook():
    request = CrawlRequest(
        url="https://example.com", 
        limit=1,
        webhook={"url": "https://webhook.site"}
    )
    
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.url = "https://example.com"
    mock_result.links = {"internal": []}
    mock_result.markdown = "# Hello"
    mock_result.html = "<h1>Hello</h1>"
    mock_result.metadata = {"title": "Test"}
    
    with patch("koda.modules.site.service.AsyncWebCrawler") as mock_crawler_cls, \
         patch("koda.modules.site.service.dispatch_webhook") as mock_dispatch:
        
        mock_crawler = AsyncMock()
        mock_crawler_cls.return_value.__aenter__.return_value = mock_crawler
        mock_crawler.arun_many.return_value = [mock_result]
        
        await crawl(request)
        
        assert mock_dispatch.call_count == 3
        calls = mock_dispatch.call_args_list
        assert calls[0][0][1] == "crawl.started"
        assert calls[1][0][1] == "crawl.page"
        assert calls[2][0][1] == "crawl.completed"
