import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from koda.use_cases.scrape.schema import ScrapeRequest
from koda.use_cases.scrape.service import scrape, ScrapeJob


@pytest.fixture
def mock_crawl4ai():
    with patch("koda.use_cases.scrape.service.AsyncWebCrawler", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_koda_client():
    with patch("koda.use_cases.scrape.service.KodaClient", autospec=True) as mock:
        yield mock


@pytest.mark.asyncio
async def test_scrape_job_initialization():
    req = ScrapeRequest(url="https://example.com")
    job = ScrapeJob(req)
    assert job.request.url == "https://example.com"
    assert len(job.action_results["screenshots"]) == 0


@pytest.mark.asyncio
async def test_scrape_success(mock_crawl4ai, mock_koda_client):
    # Mocking the client and crawler
    client_instance = AsyncMock()
    mock_koda_client.return_value.__aenter__.return_value = client_instance

    crawler_instance = AsyncMock()
    mock_crawl4ai.return_value.__aenter__.return_value = crawler_instance

    crawl_result = MagicMock()
    crawl_result.success = True
    crawl_result.markdown = "test markdown"
    crawl_result.html = "<html></html>"
    crawl_result.links = {}
    crawl_result.media = {}
    crawl_result.screenshot = None
    crawler_instance.arun.return_value = crawl_result

    req = ScrapeRequest(url="https://example.com", formats=["markdown", "html"])
    res = await scrape(req)

    assert res.success is True
    assert res.data is not None
    assert res.data["markdown"] == "test markdown"
    assert res.data["html"] == "<html></html>"


@pytest.mark.asyncio
async def test_scrape_failure(mock_crawl4ai, mock_koda_client):
    client_instance = AsyncMock()
    mock_koda_client.return_value.__aenter__.return_value = client_instance

    crawler_instance = AsyncMock()
    mock_crawl4ai.return_value.__aenter__.return_value = crawler_instance

    crawl_result = MagicMock()
    crawl_result.success = False
    crawl_result.error_message = "Failed to load page"
    crawler_instance.arun.return_value = crawl_result

    req = ScrapeRequest(url="https://example.com")
    res = await scrape(req)

    assert res.success is False
    assert res.error == "Failed to load page"
