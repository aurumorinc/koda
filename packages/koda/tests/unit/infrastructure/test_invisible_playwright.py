import sys
import pytest
from unittest.mock import MagicMock, patch, AsyncMock

# Mock invisible_playwright module before importing
mock_ip_module = MagicMock()
sys.modules["invisible_playwright"] = mock_ip_module
sys.modules["invisible_playwright.async_api"] = mock_ip_module

from koda.infrastructure.invisible_playwright import launch_stealth_browser, stop_stealth_browser, BrowserLaunchError

@pytest.mark.asyncio
async def test_launch_stealth_browser_success():
    mock_ip_class = MagicMock()
    mock_ip_instance = MagicMock()
    mock_ip_class.return_value = mock_ip_instance
    mock_ip_instance.__aenter__ = AsyncMock(return_value="mock_browser")
    
    mock_ip_module.InvisiblePlaywright = mock_ip_class
    
    browser = await launch_stealth_browser(headless=True)
    assert browser == "mock_browser"
    mock_ip_class.assert_called_once_with(
        headless=True,
        humanize=False,
        extra_prefs={"security.csp.enable": False, "dom.security.trusted_types.enabled": False}
    )

@pytest.mark.asyncio
async def test_launch_stealth_browser_failure():
    mock_ip_class = MagicMock()
    mock_ip_instance = MagicMock()
    mock_ip_class.return_value = mock_ip_instance
    mock_ip_instance.__aenter__ = AsyncMock(side_effect=Exception("Launch failed"))
    
    mock_ip_module.InvisiblePlaywright = mock_ip_class
    
    with pytest.raises(BrowserLaunchError):
        await launch_stealth_browser(headless=True)

@pytest.mark.asyncio
async def test_stop_stealth_browser():
    mock_ip_instance = MagicMock()
    mock_ip_instance.__aexit__ = AsyncMock()
    
    with patch("koda.infrastructure.invisible_playwright._ip_instance", mock_ip_instance):
        await stop_stealth_browser()
        mock_ip_instance.__aexit__.assert_called_once_with(None, None, None)
        
        # Verify it was set to None inside the module
        import koda.infrastructure.invisible_playwright as ip
        assert ip._ip_instance is None
