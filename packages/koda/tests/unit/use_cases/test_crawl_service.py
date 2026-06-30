import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from koda.use_cases.crawl.schema import CrawlRequest
from koda.use_cases.crawl.service import crawl, CrawlJob


@pytest.fixture
def mock_crawl4ai():
    with patch("koda.use_cases.crawl.service.AsyncWebCrawler", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_koda_client():
    with patch("koda.use_cases.crawl.service.KodaClient", autospec=True) as mock:
        yield mock


@pytest.fixture
def mock_url_seeder():
    with patch("koda.use_cases.crawl.service.AsyncUrlSeeder", autospec=True) as mock:
        yield mock


@pytest.mark.asyncio
async def test_crawl_job_initialization():
    req = CrawlRequest(url="https://example.com")
    job = CrawlJob(req)
    assert job.base_url == "https://example.com"
    assert job.total_crawled == 0


@pytest.mark.asyncio
async def test_crawl_success_stream(mock_crawl4ai, mock_koda_client):
    client_instance = AsyncMock()
    mock_koda_client.return_value.__aenter__.return_value = client_instance

    crawler_instance = AsyncMock()
    mock_crawl4ai.return_value.__aenter__.return_value = crawler_instance

    # Mocking the async generator for crawler.arun
    async def mock_stream():
        yield MagicMock(success=True)
        yield MagicMock(success=True)
        yield MagicMock(success=False)
        yield MagicMock(success=True)

    crawler_instance.arun.return_value = mock_stream()

    req = CrawlRequest(url="https://example.com", limit=3, sitemap="exclude")
    res = await crawl(req)

    assert res.success is True
    assert res.url == "https://example.com"
    assert res.total_pages_crawled == 3


@pytest.mark.asyncio
async def test_crawl_sitemap_only(mock_crawl4ai, mock_koda_client, mock_url_seeder):
    client_instance = AsyncMock()
    mock_koda_client.return_value.__aenter__.return_value = client_instance

    crawler_instance = AsyncMock()
    mock_crawl4ai.return_value.__aenter__.return_value = crawler_instance

    seeder_instance = AsyncMock()
    seeder_instance.urls.return_value = [
        {"url": "https://example.com/1"},
        {"url": "https://example.com/2"},
    ]
    mock_url_seeder.return_value = seeder_instance

    crawl_res_1 = MagicMock(success=True)
    crawl_res_2 = MagicMock(success=False)

    crawler_instance.arun_many.return_value = [crawl_res_1, crawl_res_2]

    req = CrawlRequest(url="https://example.com", sitemap="only", limit=10)
    res = await crawl(req)

    assert res.success is True
    assert res.total_pages_crawled == 1
