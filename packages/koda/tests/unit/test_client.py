import pytest
from pydantic import ValidationError
from koda.client import KodaClient
from koda.modules.cache import service as cache
from koda.config.main import settings

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

def test_client_settings_override():
    """Test that KodaClient kwargs override global settings."""
    original_timeout = settings.timeout
    
    # Initialize with new timeout
    _ = KodaClient(timeout=60000)
    
    # Assert global settings were mutated
    assert settings.timeout == 60000
    
    # Restore original for other tests
    _ = KodaClient(timeout=original_timeout)

def test_client_settings_validation_error():
    """Test that invalid KodaClient kwargs trigger Pydantic validation."""
    with pytest.raises(ValidationError):
        # This should fail because invisible_playwright cannot be used with chromium
        _ = KodaClient(browser="invisible_playwright", browser_type="chromium")
