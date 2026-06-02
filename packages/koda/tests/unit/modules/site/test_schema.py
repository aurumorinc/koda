import pytest
from pydantic import ValidationError
from koda.modules.site.schema import CrawlRequest, ScrapeOptions

def test_crawl_request_valid():
    request = CrawlRequest(url="https://example.com")
    assert str(request.url) == "https://example.com/"
    assert request.limit == 10000
    assert request.maxDiscoveryDepth == 0
    assert request.maxConcurrency == 10
    assert request.scrapeOptions.formats == ["markdown"]

def test_crawl_request_invalid_url():
    with pytest.raises(ValidationError):
        CrawlRequest(url="not-a-url")

def test_crawl_request_custom_options():
    request = CrawlRequest(
        url="https://example.com",
        limit=50,
        maxDiscoveryDepth=2,
        excludePaths=["/blog/.*"],
        scrapeOptions=ScrapeOptions(
            formats=["html", "markdown"],
            onlyMainContent=False
        )
    )
    assert request.limit == 50
    assert request.maxDiscoveryDepth == 2
    assert request.excludePaths == ["/blog/.*"]
    assert request.scrapeOptions.formats == ["html", "markdown"]
    assert request.scrapeOptions.onlyMainContent is False
