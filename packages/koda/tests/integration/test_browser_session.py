import pytest
import asyncio
from unittest.mock import patch
from koda.modules.browser.service import BrowserSession
from koda.config.main import settings

@pytest.mark.asyncio
@patch("koda.integrations.posthog.setup_playwright_transport")
@patch("koda.integrations.posthog.setup_network_capture")
@patch("koda.integrations.posthog.inject_posthog_monolith")
@patch("koda.integrations.posthog.flush_telemetry")
async def test_browser_session_telemetry_injection(
    mock_flush, mock_inject, mock_network, mock_transport
):
    # Temporarily set posthog settings
    old_key = settings.posthog_api_key
    old_host = settings.posthog_host
    settings.posthog_api_key = "test_key"
    settings.posthog_host = "test_host"
    
    try:
        async with BrowserSession() as context:
            # Transport should be setup on context
            mock_transport.assert_called_once_with(context)
            
            # Create a page to trigger the "page" event
            page = await context.new_page()
            
            # Wait a bit for the event handler to run
            await asyncio.sleep(0.1)
            
            # Network capture and monolith injection should be called on the new page
            mock_network.assert_called_once_with(page, "test_key")
            mock_inject.assert_called_once_with(page, "test_key", "test_host")
            
        # Flush should be called on exit
        mock_flush.assert_called_once()
    finally:
        settings.posthog_api_key = old_key
        settings.posthog_host = old_host

@pytest.mark.asyncio
@patch("koda.integrations.posthog.flush_telemetry")
async def test_browser_session_no_telemetry(mock_flush):
    # Temporarily unset posthog settings
    old_key = settings.posthog_api_key
    settings.posthog_api_key = None
    
    try:
        async with BrowserSession() as context:
            page = await context.new_page()
            # Should not raise any errors
            
        # Flush should still be called on exit
        mock_flush.assert_called_once()
    finally:
        settings.posthog_api_key = old_key
