import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from koda.modules.browser.service import launch_browser

@pytest.mark.asyncio
@patch("koda.modules.browser.service._LAUNCHERS")
async def test_launch_browser_success(mock_launchers):
    # Arrange
    mock_launcher = MagicMock()
    mock_context = MagicMock()
    mock_launcher.return_value.__aenter__.return_value = mock_context
    
    mock_launchers.get.return_value = mock_launcher
    
    # Act
    async with launch_browser("test_browser", "/tmp/dir", {"key": "value"}) as ctx:
        assert ctx == mock_context
        
    # Assert
    mock_launchers.get.assert_called_once_with("test_browser")
    mock_launcher.assert_called_once_with("/tmp/dir", {"key": "value"})

@pytest.mark.asyncio
async def test_launch_browser_unsupported():
    # Act & Assert
    with pytest.raises(ValueError, match="Unsupported browser type: unsupported_browser"):
        async with launch_browser("unsupported_browser", "/tmp/dir", {}):
            pass
