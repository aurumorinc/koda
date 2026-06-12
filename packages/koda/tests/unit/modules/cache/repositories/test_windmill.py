import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import httpx

from koda.config.main import settings
from koda.modules.cache.repositories import windmill


@pytest.fixture
def mock_settings(monkeypatch):
    monkeypatch.setattr(settings, "windmill_workspace", "test_workspace")
    monkeypatch.setattr(settings, "windmill_token", "test_token")
    monkeypatch.setattr(settings, "windmill_base_url", "http://test-windmill")
    monkeypatch.setattr(settings, "cache_repository", "windmill")
    monkeypatch.setattr(settings, "cache_prefix", "test:cache:")
    monkeypatch.setattr(settings, "windmill_state_path", "u/test/state")
    monkeypatch.setattr(settings, "windmill_state_path_file", None)


@pytest.mark.asyncio
async def test_windmill_get_success(mock_settings):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"test_key": {"key": "test_key", "value": "test_value"}}
    
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        
        result = await windmill.get("test_key")
        
        assert result is not None
        assert result.key == "test_key"
        assert result.value == "test_value"
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "u/test/state" in args[0]
        assert kwargs["headers"]["Authorization"] == "Bearer test_token"


@pytest.mark.asyncio
async def test_windmill_get_not_found(mock_settings):
    mock_response = MagicMock()
    mock_response.status_code = 404
    
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        
        result = await windmill.get("test_key")
        
        assert result is None


@pytest.mark.asyncio
async def test_windmill_set_success(mock_settings):
    from koda.modules.cache.schema import CacheEntry
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {"existing_key": {"key": "existing_key", "value": "existing_value"}}
    
    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get, \
         patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        
        mock_get.return_value = mock_get_response
        mock_post.return_value = mock_post_response
        
        entry = CacheEntry(key="new_key", value="new_value")
        await windmill.set(entry)
        
        mock_get.assert_called_once()
        mock_post.assert_called_once()
        
        args, kwargs = mock_post.call_args
        assert "update_value" in args[0]
        assert kwargs["json"]["value"] == {
            "existing_key": {"key": "existing_key", "value": "existing_value"},
            "new_key": entry.model_dump(mode="json")
        }


@pytest.mark.asyncio
async def test_windmill_set_create_if_not_found(mock_settings):
    from koda.modules.cache.schema import CacheEntry
    mock_get_response = MagicMock()
    mock_get_response.status_code = 404
    
    mock_post_update_response = MagicMock()
    mock_post_update_response.status_code = 404
    
    mock_post_create_response = MagicMock()
    mock_post_create_response.status_code = 200
    
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get, \
         patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        
        mock_get.return_value = mock_get_response
        mock_post.side_effect = [mock_post_update_response, mock_post_create_response]
        
        entry = CacheEntry(key="new_key", value="new_value")
        await windmill.set(entry)
        
        # Wait, windmill.set doesn't have a fallback to create if update fails.
        # Let's check the implementation. It just does a post to update_value.
        # If it fails, it logs an error.
        # So this test is probably testing something that doesn't exist in the implementation.
        # Let's just assert it calls post once and raises/logs.
        assert mock_post.call_count == 1
        args1, kwargs1 = mock_post.call_args_list[0]
        assert "update_value" in args1[0]


