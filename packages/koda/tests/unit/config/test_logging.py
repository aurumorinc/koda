import logging
import os
from unittest.mock import MagicMock, patch

import pytest
import structlog
from opentelemetry import trace
from opentelemetry.trace import SpanContext, TraceFlags

from koda.config.logging import setup_logging


@pytest.fixture
def capture_stdout(capsys):
    """Fixture to capture stdout."""
    return capsys


@pytest.fixture
def mock_otlp_env():
    """Fixture to mock OTLP endpoint environment variable."""
    with patch("koda.config.logging.settings") as mock_settings:
        mock_settings.otel_exporter_otlp_endpoint = "http://localhost:4317"
        mock_settings.otel_exporter_otlp_logs_endpoint = None
        yield


def test_logging_with_otel_context(capsys, mock_otlp_env):
    """Test that OTel context is injected into logs when a valid span exists."""
    # Mock the OTLP exporter and use SimpleLogRecordProcessor to avoid background thread issues
    with patch("koda.config.logging.OTLPLogExporter") as mock_exporter_cls, \
         patch("koda.config.logging.BatchLogRecordProcessor") as mock_processor_cls:
        
        mock_exporter = MagicMock()
        mock_exporter_cls.return_value = mock_exporter
        
        # Use SimpleLogRecordProcessor instead of BatchLogRecordProcessor for synchronous export
        from opentelemetry.sdk._logs.export import SimpleLogRecordProcessor
        mock_processor_cls.side_effect = lambda exporter: SimpleLogRecordProcessor(exporter)
        
        setup_logging()
        logger = structlog.get_logger("test_logger")

        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.id_generator import RandomIdGenerator
        
        # Create a deterministic ID generator for testing
        class DeterministicIdGenerator(RandomIdGenerator):
            def generate_trace_id(self):
                return 0xDEADBEEFDEADBEEFDEADBEEFDEADBEEF
            def generate_span_id(self):
                return 0xDEADBEEFDEADBEEF
                
        provider = TracerProvider(id_generator=DeterministicIdGenerator())
        trace.set_tracer_provider(provider)
        tracer = trace.get_tracer(__name__)

        with tracer.start_as_current_span("test_span"):
            logger.info("test_message", extra_field="extra_value")

        # 1. Check Console Output (Human-readable)
        captured = capsys.readouterr()
        assert "test_message" in captured.out
        assert "extra_field" in captured.out
        assert "extra_value" in captured.out
        assert "trace_id" in captured.out
        assert "deadbeefdeadbeefdeadbeefdeadbeef" in captured.out
        assert "span_id" in captured.out
        assert "deadbeefdeadbeef" in captured.out

        # 2. Check OTLP Exporter Output (Structured)
        assert mock_exporter.export.called
        batch = mock_exporter.export.call_args[0][0]
        assert len(batch) == 1
        log_record = batch[0].log_record
        
        assert log_record.body["event"] == "test_message"
        assert log_record.body["extra_field"] == "extra_value"
        assert log_record.body["trace_id"] == "deadbeefdeadbeefdeadbeefdeadbeef"
        assert log_record.body["span_id"] == "deadbeefdeadbeef"
        assert log_record.trace_id == 0xDEADBEEFDEADBEEFDEADBEEFDEADBEEF
        assert log_record.span_id == 0xDEADBEEFDEADBEEF


def test_logging_without_otel_context(capsys, mock_otlp_env):
    """Test that logs do not contain OTel context when no valid span exists."""
    # Mock an invalid OTel span
    mock_span = MagicMock()
    mock_span.get_span_context().is_valid = False

    with patch("koda.config.logging.OTLPLogExporter") as mock_exporter_cls, \
         patch("koda.config.logging.BatchLogRecordProcessor") as mock_processor_cls:
        
        mock_exporter = MagicMock()
        mock_exporter_cls.return_value = mock_exporter
        
        from opentelemetry.sdk._logs.export import SimpleLogRecordProcessor
        mock_processor_cls.side_effect = lambda exporter: SimpleLogRecordProcessor(exporter)
        
        setup_logging()
        logger = structlog.get_logger("test_logger")

        with patch("opentelemetry.trace.get_current_span", return_value=mock_span):
            logger.info("test_message_no_span")

        # 1. Check Console Output
        captured = capsys.readouterr()
        assert "test_message_no_span" in captured.out
        assert "trace_id=" not in captured.out
        assert "span_id=" not in captured.out

        # 2. Check OTLP Exporter Output
        assert mock_exporter.export.called
        batch = mock_exporter.export.call_args[0][0]
        log_record = batch[0].log_record
        assert log_record.body["event"] == "test_message_no_span"
        assert "trace_id" not in log_record.body
        assert "span_id" not in log_record.body


def test_standard_logging_routing(capsys, mock_otlp_env):
    """Test that standard library logging is routed through structlog."""
    with patch("koda.config.logging.OTLPLogExporter") as mock_exporter_cls, \
         patch("koda.config.logging.BatchLogRecordProcessor") as mock_processor_cls:
        
        mock_exporter = MagicMock()
        mock_exporter_cls.return_value = mock_exporter
        
        from opentelemetry.sdk._logs.export import SimpleLogRecordProcessor
        mock_processor_cls.side_effect = lambda exporter: SimpleLogRecordProcessor(exporter)
        
        setup_logging()
        std_logger = logging.getLogger("standard_logger")
        
        std_logger.info("standard_log_message")

        # 1. Check Console Output
        captured = capsys.readouterr()
        assert "standard_log_message" in captured.out
        assert "standard_logger" in captured.out

        # 2. Check OTLP Exporter Output
        assert mock_exporter.export.called
        batch = mock_exporter.export.call_args[0][0]
        log_record = batch[0].log_record
        assert log_record.body == "standard_log_message"
