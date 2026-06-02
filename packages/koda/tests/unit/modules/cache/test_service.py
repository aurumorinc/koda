from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest

from koda.config.main import settings
from koda.modules.cache.schema import CacheEntry
from koda.modules.cache import service as cache_service


@pytest.fixture
def mock_windmill():
    with patch("koda.modules.cache.service.windmill", spec=True) as mock:
        mock.get = AsyncMock()
        mock.set = AsyncMock()
        yield mock


@pytest.fixture
def mock_settings():
    with patch("koda.modules.cache.service.settings", spec=True) as mock:
        mock.cache_repository = "windmill"
        mock.cache_prefix = "test:cache:"
        yield mock


@pytest.mark.asyncio
async def test_get_cache_hit(mock_windmill, mock_settings):
    # Arrange
    key = "my_key"
    expected_value = "my_value"
    entry = CacheEntry(key=f"test:cache:{key}", value=expected_value)
    mock_windmill.get.return_value = entry

    # Act
    result = await cache_service.get(key)

    # Assert
    assert result == expected_value
    mock_windmill.get.assert_called_once_with("test:cache:my_key")


@pytest.mark.asyncio
async def test_get_cache_miss(mock_windmill, mock_settings):
    # Arrange
    key = "my_key"
    mock_windmill.get.return_value = None

    # Act
    result = await cache_service.get(key)

    # Assert
    assert result is None
    mock_windmill.get.assert_called_once_with("test:cache:my_key")


@pytest.mark.asyncio
async def test_get_cache_expired(mock_windmill, mock_settings):
    # Arrange
    key = "my_key"
    expired_time = datetime.now(timezone.utc) - timedelta(hours=1)
    entry = CacheEntry(key=f"test:cache:{key}", value="my_value", expires_at=expired_time)
    mock_windmill.get.return_value = entry

    # Act
    result = await cache_service.get(key)

    # Assert
    assert result is None
    mock_windmill.get.assert_called_once_with("test:cache:my_key")


@pytest.mark.asyncio
async def test_get_unsupported_repository(mock_windmill, mock_settings):
    # Arrange
    mock_settings.cache_repository = "unsupported"
    key = "my_key"

    # Act
    result = await cache_service.get(key)

    # Assert
    assert result is None
    mock_windmill.get.assert_not_called()


@pytest.mark.asyncio
async def test_get_exception_handled(mock_windmill, mock_settings):
    # Arrange
    key = "my_key"
    mock_windmill.get.side_effect = Exception("Backend error")

    # Act
    result = await cache_service.get(key)

    # Assert
    assert result is None
    mock_windmill.get.assert_called_once_with("test:cache:my_key")


@pytest.mark.asyncio
async def test_set_success(mock_windmill, mock_settings):
    # Arrange
    key = "my_key"
    value = "my_value"

    # Act
    await cache_service.set(key, value)

    # Assert
    mock_windmill.set.assert_called_once()
    called_entry = mock_windmill.set.call_args[0][0]
    assert isinstance(called_entry, CacheEntry)
    assert called_entry.key == "test:cache:my_key"
    assert called_entry.value == "my_value"


@pytest.mark.asyncio
async def test_set_unsupported_repository(mock_windmill, mock_settings):
    # Arrange
    mock_settings.cache_repository = "unsupported"
    key = "my_key"
    value = "my_value"

    # Act
    await cache_service.set(key, value)

    # Assert
    mock_windmill.set.assert_not_called()


@pytest.mark.asyncio
async def test_set_exception_handled(mock_windmill, mock_settings):
    # Arrange
    key = "my_key"
    value = "my_value"
    mock_windmill.set.side_effect = Exception("Backend error")

    # Act
    # Should not raise an exception
    await cache_service.set(key, value)

    # Assert
    mock_windmill.set.assert_called_once()
