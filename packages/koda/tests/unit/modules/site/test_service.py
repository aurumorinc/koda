import pytest
from unittest.mock import patch, MagicMock
from koda.modules.site.schema import CrawlRequest
from koda.modules.site.service import CrawlJob

def test_is_valid_link():
    request = CrawlRequest(url="https://example.com/docs")
    job = CrawlJob(request)
    
    # Test external links
    job.request.allowExternalLinks = True
    assert job._is_valid_link("https://other.com") is True
    job.request.allowExternalLinks = False
    assert job._is_valid_link("https://other.com") is False
    
    # Test subdomains
    job.request.allowSubdomains = True
    assert job._is_valid_link("https://sub.example.com") is True
    job.request.allowSubdomains = False
    assert job._is_valid_link("https://sub.example.com") is False
    
    # Test domain scope
    job.request.crawlEntireDomain = True
    assert job._is_valid_link("https://example.com/blog") is True
    job.request.crawlEntireDomain = False
    assert job._is_valid_link("https://example.com/blog") is False
    assert job._is_valid_link("https://example.com/docs/api") is True
    
    # Test exclude paths
    job.request.excludePaths = ["/api"]
    assert job._is_valid_link("https://example.com/docs/api") is False
    job.request.excludePaths = None
    
    # Test include paths
    job.request.includePaths = ["/api"]
    assert job._is_valid_link("https://example.com/docs/api") is True
    assert job._is_valid_link("https://example.com/docs/other") is False

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
    
    with patch("koda.modules.site.service.Crawl4AiTool") as mock_tool_cls:
        mock_tool = MagicMock()
        mock_tool_cls.return_value = mock_tool
        
        async def mock_execute_stream(*args, **kwargs):
            yield mock_result_1
            yield mock_result_2

        mock_tool.execute_stream = MagicMock(side_effect=mock_execute_stream)
        
        job = CrawlJob(request)
        response = await job.run()
        
        assert response.success is True
        assert response.total_pages_crawled == 2
        assert mock_tool.execute_stream.call_count == 1

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
    
    with patch("koda.modules.site.service.Crawl4AiTool") as mock_tool_cls, \
         patch("koda.modules.site.service.dispatch_webhook") as mock_dispatch:
        
        mock_tool = MagicMock()
        mock_tool_cls.return_value = mock_tool
        
        async def mock_execute_stream(*args, **kwargs):
            yield mock_result

        mock_tool.execute_stream = MagicMock(side_effect=mock_execute_stream)
        
        job = CrawlJob(request)
        await job.run()
        
        assert mock_dispatch.call_count == 3
        calls = mock_dispatch.call_args_list
        assert calls[0][0][1] == "crawl.started"
        assert calls[1][0][1] == "crawl.page"
        assert calls[2][0][1] == "crawl.completed"
