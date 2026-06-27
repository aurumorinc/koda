import os
import pytest
from unittest.mock import patch, MagicMock

from worldline import structlog
from koda.integrations.posthog import inject_posthog_monolith

@pytest.mark.asyncio
async def test_unified_session_linking(capsys):
    """
    End-to-end integration test that simulates a Windmill worker execution
    and verifies the bi-directional linking between OTel and PostHog.
    """
    # 1. Setup: Simulate Windmill passing the OTel context via TRACEPARENT
    traceparent = "00-integrationtrace123456789012345-integrationspan1-01"
    
    from koda.config.main import settings
    from worldline import config as worldline_config
    
    with patch.dict(os.environ, {"TRACEPARENT": traceparent}), \
         patch.object(settings, "traceparent", traceparent), \
         patch.object(worldline_config.settings, "traceparent", traceparent), \
         patch("worldline.service.OTLPLogExporter"), \
         patch("worldline.service.BatchLogRecordProcessor"), \
         patch("os.path.exists", return_value=True), \
         patch("builtins.open", MagicMock()):
        
        # 2. Logging: Verify trace_id is extracted
        
        assert worldline_config.settings.trace_id == "integrationtrace123456789012345"
        
        logger = structlog.get_logger("test_unified_session")
        logger.info("test_unified_log")
        
        captured = capsys.readouterr()
        assert "test_unified_log" in captured.out
        
        # 3. PostHog: Call inject_posthog_monolith and verify the script contains the trace_id
        from unittest.mock import AsyncMock
        mock_page = AsyncMock()
        
        # Mock the file read for posthog-monolith.js
        with patch("builtins.open", MagicMock()) as mock_open_file:
            mock_open_file.return_value.__enter__.return_value.read.return_value = "console.log('monolith');"
            
            await inject_posthog_monolith(mock_page, "phc_test", "https://test.com")
            
            mock_page.add_init_script.assert_called_once()
            injected_script = mock_page.add_init_script.call_args[0][0]
            assert 'ph.register({ "$trace_id": "integrationtrace123456789012345" });' in injected_script
