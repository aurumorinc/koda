import os
import pytest
from unittest.mock import patch, MagicMock

from python_logging.main import setup_logging, get_logger
from koda.integrations.sentry import init_sentry
from koda.integrations.posthog import inject_posthog_monolith

@pytest.mark.asyncio
async def test_unified_session_linking(capsys):
    """
    End-to-end integration test that simulates a Windmill worker execution
    and verifies the tri-directional linking between OTel, Sentry, and PostHog.
    """
    # 1. Setup: Simulate Windmill passing the OTel context via TRACEPARENT
    traceparent = "00-integrationtrace123456789012345-integrationspan1-01"
    
    from koda.config.main import settings
    import python_logging.config
    
    with patch.dict(os.environ, {"TRACEPARENT": traceparent}), \
         patch.object(settings, "traceparent", traceparent), \
         patch.object(python_logging.config.settings, "traceparent", traceparent), \
         patch("python_logging.service.OTLPLogExporter"), \
         patch("python_logging.service.BatchLogRecordProcessor"), \
         patch("koda.integrations.sentry.sentry_sdk.init") as mock_sentry_init, \
         patch("koda.integrations.sentry.sentry_sdk.set_tag") as mock_sentry_set_tag, \
         patch("os.path.exists", return_value=True), \
         patch("builtins.open", MagicMock()):
        
        # 2. Logging: Call setup_logging() and verify trace_id is extracted
        setup_logging(settings)
        
        assert python_logging.config.settings.trace_id == "integrationtrace123456789012345"
        
        logger = get_logger("test_unified_session")
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
