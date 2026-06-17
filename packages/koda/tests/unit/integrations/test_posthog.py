import pytest
from unittest.mock import MagicMock, patch, AsyncMock, ANY, mock_open, PropertyMock
from playwright.async_api import Request, Response

from koda.infrastructure.posthog import (
    _get_otel_trace_id,
    setup_playwright_transport,
    setup_network_capture,
    inject_posthog_monolith
)

def test_get_otel_trace_id_fallback():
    """Test _get_otel_trace_id falls back to settings when no active span exists."""
    mock_span = MagicMock()
    mock_span.get_span_context().is_valid = False

    with patch("opentelemetry.trace.get_current_span", return_value=mock_span), \
         patch("koda.config.main.Settings.trace_id", new_callable=PropertyMock, return_value="test_trace_123"):
        assert _get_otel_trace_id() == "test_trace_123"

@pytest.mark.asyncio
async def test_inject_posthog_monolith():
    """Test inject_posthog_monolith includes the trace_id in the injected JS."""
    mock_page = AsyncMock()
    
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data="console.log('monolith');")), \
         patch("koda.infrastructure.posthog._get_otel_trace_id", return_value="test_trace_123"):
        
        await inject_posthog_monolith(mock_page, "phc_test", "https://test.com")
        
        mock_page.add_init_script.assert_called_once()
        injected_script = mock_page.add_init_script.call_args[0][0]
        assert 'ph.register({ "$trace_id": "test_trace_123" });' in injected_script

@pytest.mark.asyncio
async def test_setup_playwright_transport():
    mock_context = AsyncMock()
    await setup_playwright_transport(mock_context)
    mock_context.expose_function.assert_called_once_with("__playwright_posthog_send", ANY)

@pytest.mark.asyncio
async def test_setup_network_capture():
    mock_page = MagicMock()
    await setup_network_capture(mock_page, "phc_test")
    assert mock_page.on.call_count == 2
