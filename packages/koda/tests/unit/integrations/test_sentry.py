import pytest
from unittest.mock import patch, PropertyMock

from koda.infrastructure.sentry import init_sentry

def test_init_sentry_tagging():
    """Test init_sentry calls sentry_sdk.set_tag with the value from settings."""
    with patch("koda.infrastructure.sentry.sentry_sdk.init") as mock_init, \
         patch("koda.infrastructure.sentry.sentry_sdk.set_tag") as mock_set_tag, \
         patch("koda.config.main.Settings.trace_id", new_callable=PropertyMock, return_value="sentry_trace_456"):
        
        from koda.config.main import settings
        settings.sentry_dsn = "http://test@localhost/1"
        
        init_sentry()
        
        mock_init.assert_called_once()
        mock_set_tag.assert_called_with("trace_id", "sentry_trace_456")
        
        settings.sentry_dsn = None

def test_init_sentry_no_dsn():
    """Test init_sentry gracefully exits if no DSN is provided."""
    with patch("koda.infrastructure.sentry.sentry_sdk.init") as mock_init:
        from koda.config.main import settings
        settings.sentry_dsn = None
        
        init_sentry()
        
        mock_init.assert_not_called()
