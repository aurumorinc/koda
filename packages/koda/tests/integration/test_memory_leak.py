import pytest
import asyncio
import psutil
import os
import gc
from unittest.mock import patch, MagicMock, AsyncMock
from koda.client import KodaClient
from koda.modules.page.schema import ScrapeRequest, ScrapeResponse

@pytest.mark.asyncio
@patch("koda.client.page.scrape")
async def test_memory_leak_scrape(mock_scrape):
    """Test that repeated scraping does not leak memory or contexts."""
    
    # Mock the scrape response to avoid actual network calls during the leak test
    mock_response = ScrapeResponse(
        url="https://example.com",
        markdown="# Test Content",
        metadata={"title": "Dummy Page"}
    )
    mock_scrape.return_value = mock_response
    
    process = psutil.Process(os.getpid())
    
    # Run a warmup scrape to initialize everything (browser, etc.)
    async with KodaClient() as client:
        request = ScrapeRequest(url="https://example.com", formats=["markdown"])
        await client.scrape(request)
        
    # Force garbage collection
    gc.collect()
    
    # Record baseline memory
    baseline_memory = process.memory_info().rss
    
    # Run multiple scrapes
    iterations = 20
    for i in range(iterations):
        async with KodaClient() as client:
            request = ScrapeRequest(url="https://example.com", formats=["markdown"])
            await client.scrape(request)
            
        # Fail early if memory grows too much to prevent server crash
        current_memory = process.memory_info().rss
        diff_mb = (current_memory - baseline_memory) / (1024 * 1024)
        assert diff_mb < 100.0, f"Memory leak detected early! Grew by {diff_mb:.2f} MB at iteration {i}"
            
    # Force garbage collection again
    gc.collect()
    
    # Record final memory
    final_memory = process.memory_info().rss
    
    # Calculate difference in MB
    diff_mb = (final_memory - baseline_memory) / (1024 * 1024)
    
    # Assert that memory didn't grow by more than 50MB after 20 iterations
    # (Some small growth is expected due to Python's internal caching, but not a massive leak)
    assert diff_mb < 50.0, f"Memory leaked by {diff_mb:.2f} MB over {iterations} iterations"
