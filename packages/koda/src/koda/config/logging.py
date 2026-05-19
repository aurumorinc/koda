import logging
import sys
from typing import Any, Dict

import structlog
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from koda.config.main import settings


def add_otel_context(
    logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]
) -> Dict[str, Any]:
    """Injects OpenTelemetry trace_id and span_id into the log record."""
    span = trace.get_current_span()
    if span and span.get_span_context().is_valid:
        ctx = span.get_span_context()
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    return event_dict


def _setup_otel_logger_provider() -> LoggerProvider:
    """Initializes the OpenTelemetry LoggerProvider with an OTLP exporter."""
    logger_provider = LoggerProvider()
    
    # Only add the exporter if an endpoint is configured
    if settings.otel_exporter_otlp_endpoint or settings.otel_exporter_otlp_logs_endpoint:
        exporter = OTLPLogExporter()
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    
    set_logger_provider(logger_provider)
    return logger_provider


def setup_logging(log_level: int = logging.INFO) -> None:
    """Configures structlog and routes standard logging through it."""
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        add_otel_context,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # 1. Console Handler (Human-readable)
    console_formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(colors=True),
        foreign_pre_chain=shared_processors,
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    # 2. OTLP Handler (Structured JSON/Protobuf)
    logger_provider = _setup_otel_logger_provider()
    otlp_handler = LoggingHandler(level=log_level, logger_provider=logger_provider)

    root_logger = logging.getLogger()
    # Remove existing handlers to avoid duplicate logs
    root_logger.handlers.clear()
    
    root_logger.addHandler(console_handler)
    
    # Only add OTLP handler if endpoint is configured to avoid connection errors
    if settings.otel_exporter_otlp_endpoint or settings.otel_exporter_otlp_logs_endpoint:
        root_logger.addHandler(otlp_handler)
        
    root_logger.setLevel(log_level)
