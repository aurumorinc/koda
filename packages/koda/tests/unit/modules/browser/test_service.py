import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from koda.modules.browser.service import (
    BrowserSession, 
    _strip_csp_headers, 
    _native_playwright_interceptor,
    _invisible_playwright_modifier
)

@pytest.mark.asyncio
async def test_native_playwright_interceptor():
    mock_context = AsyncMock()
    await _native_playwright_interceptor(mock_context)
    mock_context.route.assert_awaited_once_with("**/*", _strip_csp_headers)

def test_invisible_playwright_modifier():
    config = {"headless": True, "extra_prefs": {"existing": True}}
    new_config = _invisible_playwright_modifier(config)
    
    assert new_config["headless"] is True
    assert new_config["extra_prefs"]["existing"] is True
    assert new_config["extra_prefs"]["security.csp.enable"] is False
    assert new_config["extra_prefs"]["dom.security.trusted_types.enabled"] is False
    
    # Original config is unmodified
    assert "security.csp.enable" not in config["extra_prefs"]

@pytest.mark.asyncio
async def test_strip_csp_headers_non_document():
    mock_route = AsyncMock()
    mock_route.request.resource_type = "script"
    
    await _strip_csp_headers(mock_route)
    
    mock_route.continue_.assert_awaited_once()
    mock_route.fetch.assert_not_awaited()

@pytest.mark.asyncio
async def test_strip_csp_headers_document():
    mock_route = AsyncMock()
    mock_route.request.resource_type = "document"
    
    mock_response = AsyncMock()
    mock_response.headers = {
        "Content-Type": "text/html",
        "Content-Security-Policy": "default-src 'self'",
        "content-security-policy-report-only": "default-src 'self'"
    }
    mock_route.fetch.return_value = mock_response
    
    await _strip_csp_headers(mock_route)
    
    mock_route.fetch.assert_awaited_once()
    mock_route.fulfill.assert_awaited_once_with(
        response=mock_response,
        headers={"Content-Type": "text/html"}
    )

@pytest.mark.asyncio
async def test_strip_csp_headers_fetch_fails():
    mock_route = AsyncMock()
    mock_route.request.resource_type = "document"
    mock_route.fetch.side_effect = Exception("Fetch failed")
    
    await _strip_csp_headers(mock_route)
    
    mock_route.continue_.assert_awaited_once()

@pytest.mark.asyncio
@patch("koda.modules.browser.service._LAUNCHERS")
async def test_launch_browser_yields_browser(mock_launchers):
    # Arrange
    mock_launcher = MagicMock()
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    
    mock_browser.new_context.return_value = mock_context
    mock_launcher.return_value.__aenter__.return_value = mock_browser
    
    mock_launchers.get.return_value = mock_launcher
    
    with patch("koda.config.main.settings.browser", "default"):
        # Act
        async with BrowserSession({"key": "value"}) as ctx:
            assert ctx == mock_context
            
        # Assert
        mock_launchers.get.assert_called_once_with("default")
        mock_launcher.assert_called_once_with("", {"key": "value"})
        mock_browser.new_context.assert_awaited_once_with(
            permissions=["geolocation", "notifications"],
            bypass_csp=True
        )
        mock_context.on.assert_called_once()
        mock_context.route.assert_awaited_once_with("**/*", _strip_csp_headers)

@pytest.mark.asyncio
@patch("koda.modules.browser.service._LAUNCHERS")
async def test_launch_browser_yields_context(mock_launchers):
    # Arrange
    mock_launcher = MagicMock()
    mock_context = AsyncMock()
    # Ensure it doesn't have new_context attribute
    del mock_context.new_context
    
    mock_launcher.return_value.__aenter__.return_value = mock_context
    
    mock_launchers.get.return_value = mock_launcher
    
    with patch("koda.config.main.settings.browser", "default"):
        # Act
        async with BrowserSession({"key": "value"}) as ctx:
            assert ctx == mock_context
            
        # Assert
        mock_context.grant_permissions.assert_awaited_once_with(
            ["geolocation", "notifications"]
        )
        mock_context.on.assert_called_once()
        mock_context.route.assert_awaited_once_with("**/*", _strip_csp_headers)

@pytest.mark.asyncio
async def test_launch_browser_unsupported():
    # Act & Assert
    with patch("koda.config.main.settings.browser", "unsupported_browser"):
        with pytest.raises(ValueError, match="Unsupported browser type: unsupported_browser"):
            async with BrowserSession({}):
                pass
