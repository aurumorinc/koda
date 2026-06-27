import pytest
from koda.client import KodaClient
from koda.modules.cache import service as cache

@pytest.mark.asyncio
async def test_client_initialization():
    """Test that KodaClient initializes and exposes infrastructure layers."""
    client = KodaClient()
    assert client.cache is cache

@pytest.mark.asyncio
async def test_client_async_context():
    """Test that KodaClient can be used as an async context manager."""
    async with KodaClient() as client:
        assert client is not None
        assert client.cache is cache
