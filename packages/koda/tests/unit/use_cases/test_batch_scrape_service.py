import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from koda.use_cases.batch_scrape.schema import BatchScrapeRequest
from koda.use_cases.batch_scrape.service import batch_scrape, BatchScrapeJob


@pytest.fixture
def mock_crawl4ai():
    with patch(
        "koda.use_cases.batch_scrape.service.AsyncWebCrawler", autospec=True
    ) as mock:
        yield mock


@pytest.fixture
def mock_koda_client():
    with patch("koda.use_cases.batch_scrape.service.KodaClient", autospec=True) as mock:
        yield mock


@pytest.mark.asyncio
async def test_batch_scrape_job_initialization():
    req = BatchScrapeRequest(urls=["https://example.com/1", "https://example.com/2"])
    job = BatchScrapeJob(req)
    assert not job.target_requests


@pytest.mark.asyncio
async def test_batch_scrape_success(mock_crawl4ai, mock_koda_client):
    client_instance = AsyncMock()
    mock_koda_client.return_value.__aenter__.return_value = client_instance

    crawler_instance = AsyncMock()
    mock_crawl4ai.return_value.__aenter__.return_value = crawler_instance

    crawl_result_1 = MagicMock()
    crawl_result_1.url = "https://example.com/1"
    crawl_result_1.success = True
    crawl_result_1.markdown = "test markdown 1"
    crawl_result_1.html = "<html>1</html>"
    crawl_result_1.links = {}
    crawl_result_1.media = {}
    crawl_result_1.screenshot = None

    crawl_result_2 = MagicMock()
    crawl_result_2.url = "https://example.com/2"
    crawl_result_2.success = True
    crawl_result_2.markdown = "test markdown 2"
    crawl_result_2.html = "<html>2</html>"
    crawl_result_2.links = {}
    crawl_result_2.media = {}
    crawl_result_2.screenshot = None

    crawler_instance.arun_many.return_value = [crawl_result_1, crawl_result_2]

    req = BatchScrapeRequest(
        urls=["https://example.com/1", "https://example.com/2"],
        formats=["markdown", "html"],
    )
    res = await batch_scrape(req)

    assert res.success is True
    assert len(res.data) == 2
    assert res.data[0].url == "https://example.com/1"
    assert res.data[0].markdown == "test markdown 1"
    assert res.data[1].url == "https://example.com/2"
    assert res.data[1].markdown == "test markdown 2"


@pytest.mark.asyncio
async def test_batch_scrape_with_invalid_urls():
    req = BatchScrapeRequest(urls=["invalid_url"], ignoreInvalidURLs=True)
    res = await batch_scrape(req)

    assert res.success is False
    assert res.invalid_urls == ["invalid_url"]
