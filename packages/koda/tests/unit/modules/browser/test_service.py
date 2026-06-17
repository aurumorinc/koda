import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from koda.modules.browser.service import BrowserSession

@pytest.mark.asyncio
@patch("koda.modules.browser.service._LAUNCHERS")
async def test_launch_browser_success(mock_launchers):
    # Arrange
    mock_launcher = MagicMock()
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    
    mock_browser.new_context.return_value = mock_context
    mock_launcher.return_value.__aenter__.return_value = mock_browser
    
    mock_launchers.get.return_value = mock_launcher
    
    with patch("koda.config.main.settings.browser", "test_browser"):
        # Act
        async with BrowserSession({"key": "value"}) as ctx:
            assert ctx == mock_context
            
        # Assert
        mock_launchers.get.assert_called_once_with("test_browser")
        mock_launcher.assert_called_once_with("", {"key": "value"})

@pytest.mark.asyncio
async def test_launch_browser_unsupported():
    # Act & Assert
    with patch("koda.config.main.settings.browser", "unsupported_browser"):
        with pytest.raises(ValueError, match="Unsupported browser type: unsupported_browser"):
            async with BrowserSession({}):
                pass
