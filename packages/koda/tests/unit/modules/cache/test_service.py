from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest

from koda.config.main import settings
from koda.modules.cache.schema import CacheEntry
from koda.modules.cache.service import CacheService


@pytest.fixture
def mock_cache_repo():
    mock = AsyncMock()
    mock.get = AsyncMock()
    mock.set = AsyncMock()
    return mock


@pytest.fixture
def cache_service(mock_cache_repo):
    return CacheService(cache_repo=mock_cache_repo)


@pytest.fixture
def mock_settings():
    with patch("koda.modules.cache.service.settings", spec=True) as mock:
        mock.cache_prefix = "test:cache:"
        yield mock


@pytest.mark.asyncio
async def test_get_cache_hit(cache_service, mock_cache_repo, mock_settings):
    # Arrange
    key = "my_key"
    expected_value = "my_value"
    entry = CacheEntry(key=f"test:cache:{key}", value=expected_value)
    mock_cache_repo.get.return_value = entry

    # Act
    result = await cache_service.get(key)

    # Assert
    assert result == expected_value
    mock_cache_repo.get.assert_called_once_with("test:cache:my_key")


@pytest.mark.asyncio
async def test_get_cache_miss(cache_service, mock_cache_repo, mock_settings):
    # Arrange
    key = "my_key"
    mock_cache_repo.get.return_value = None

    # Act
    result = await cache_service.get(key)

    # Assert
    assert result is None
    mock_cache_repo.get.assert_called_once_with("test:cache:my_key")


@pytest.mark.asyncio
async def test_get_cache_expired(cache_service, mock_cache_repo, mock_settings):
    # Arrange
    key = "my_key"
    expired_time = datetime.now(timezone.utc) - timedelta(hours=1)
    entry = CacheEntry(key=f"test:cache:{key}", value="my_value", expires_at=expired_time)
    mock_cache_repo.get.return_value = entry

    # Act
    result = await cache_service.get(key)

    # Assert
    assert result is None
    mock_cache_repo.get.assert_called_once_with("test:cache:my_key")


@pytest.mark.asyncio
async def test_get_exception_handled(cache_service, mock_cache_repo, mock_settings):
    # Arrange
    key = "my_key"
    mock_cache_repo.get.side_effect = Exception("Backend error")

    # Act
    result = await cache_service.get(key)

    # Assert
    assert result is None
    mock_cache_repo.get.assert_called_once_with("test:cache:my_key")


@pytest.mark.asyncio
async def test_set_success(cache_service, mock_cache_repo, mock_settings):
    # Arrange
    key = "my_key"
    value = "my_value"

    # Act
    await cache_service.set(key, value)

    # Assert
    mock_cache_repo.set.assert_called_once()
    called_entry = mock_cache_repo.set.call_args[0][0]
    assert isinstance(called_entry, CacheEntry)
    assert called_entry.key == "test:cache:my_key"
    assert called_entry.value == "my_value"


@pytest.mark.asyncio
async def test_set_exception_handled(cache_service, mock_cache_repo, mock_settings):
    # Arrange
    key = "my_key"
    value = "my_value"
    mock_cache_repo.set.side_effect = Exception("Backend error")

    # Act
    # Should not raise an exception
    await cache_service.set(key, value)

    # Assert
    mock_cache_repo.set.assert_called_once()
