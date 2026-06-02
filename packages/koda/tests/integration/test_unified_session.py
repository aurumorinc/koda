import os
import pytest
import structlog
from unittest.mock import patch, MagicMock

from koda.config.logging import setup_logging
from koda.services.sentry import init_sentry
from koda.core.posthog import inject_posthog_monolith

@pytest.mark.asyncio
async def test_unified_session_linking(capsys):
    """
    End-to-end integration test that simulates a Windmill worker execution
    and verifies the tri-directional linking between OTel, Sentry, and PostHog.
    """
    # 1. Setup: Simulate Windmill passing the OTel context via TRACEPARENT
    traceparent = "00-integrationtrace123456789012345-integrationspan1-01"
    
    with patch.dict(os.environ, {"TRACEPARENT": traceparent}), \
         patch("koda.config.logging.OTLPLogExporter"), \
         patch("koda.config.logging.BatchLogRecordProcessor"), \
         patch("koda.services.sentry.sentry_sdk.init") as mock_sentry_init, \
         patch("koda.services.sentry.sentry_sdk.set_tag") as mock_sentry_set_tag, \
         patch("os.path.exists", return_value=True), \
         patch("builtins.open", MagicMock()):
        
        # 2. Logging: Call setup_logging() and verify trace_id is extracted
        setup_logging()
        
        from koda.config.main import settings
        assert settings.trace_id == "integrationtrace123456789012345"
        
        logger = structlog.get_logger("test_unified_session")
        logger.info("test_unified_log")
        
        captured = capsys.readouterr()
        assert "test_unified_log" in captured.out
        assert "trace_id" in captured.out
        assert "integrationtrace123456789012345" in captured.out
        
        # 3. Sentry: Call init_sentry() and verify the tag is set
        settings.sentry_dsn = "http://test@localhost/1"
        init_sentry()
        
        mock_sentry_init.assert_called_once()
        mock_sentry_set_tag.assert_called_with("trace_id", "integrationtrace123456789012345")
        
        # 4. PostHog: Call inject_posthog_monolith and verify the script contains the trace_id
        from unittest.mock import AsyncMock
        mock_page = AsyncMock()
        
        # Mock the file read for posthog-monolith.js
        with patch("builtins.open", MagicMock()) as mock_open_file:
            mock_open_file.return_value.__enter__.return_value.read.return_value = "console.log('monolith');"
            
            await inject_posthog_monolith(mock_page, "phc_test", "https://test.com")
            
            mock_page.add_init_script.assert_called_once()
            injected_script = mock_page.add_init_script.call_args[0][0]
            assert 'ph.register({ "$trace_id": "integrationtrace123456789012345" });' in injected_script
            
        # Cleanup
        settings.sentry_dsn = None
        settings.trace_id = None
        settings.span_id = None
