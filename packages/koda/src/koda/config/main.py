import os
from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class Settings:
    """
    Centralized configuration for Koda.
    Loads values from environment variables with sensible defaults.
    """

    # Storage Configuration
    storage_repository: str = os.getenv("STORAGE_REPOSITORY", "windmill")
    
    # Cache Configuration
    cache_repository: str = os.getenv("CACHE_REPOSITORY", "windmill")
    cache_prefix: str = os.getenv("CACHE_PREFIX", "koda.modules.cache:")

    # Windmill Configuration
    windmill_token: Optional[str] = os.getenv("WINDMILL_TOKEN")
    windmill_base_url: str = os.getenv("WINDMILL_BASE_URL", "https://app.windmill.dev")
    windmill_workspace: Optional[str] = os.getenv("WINDMILL_WORKSPACE")
    windmill_state_path: Optional[str] = os.getenv("WM_STATE_PATH")
    windmill_state_path_file: Optional[str] = os.getenv("WM_STATE_PATH_FILE")

    # Lock Configuration
    lock_repository: str = os.getenv("LOCK_REPOSITORY", "consul")
    lock_ttl_seconds: int = int(os.getenv("LOCK_TTL_SECONDS", "30"))
    lock_timeout_seconds: int = int(os.getenv("LOCK_TIMEOUT_SECONDS", "10"))
    
    # Consul Configuration
    consul_base_url: str = os.getenv("CONSUL_BASE_URL", "http://localhost:8500")

    # Redis Configuration (Upstash)
    upstash_redis_rest_url: Optional[str] = os.getenv("UPSTASH_REDIS_REST_URL")
    upstash_redis_rest_token: Optional[str] = os.getenv("UPSTASH_REDIS_REST_TOKEN")

    # S3 Configuration
    s3_endpoint_url: Optional[str] = os.getenv("S3_ENDPOINT_URL")
    s3_region_name: str = os.getenv("S3_REGION_NAME", "us-east-1")
    s3_access_key_id: Optional[str] = os.getenv("S3_ACCESS_KEY_ID")
    s3_secret_access_key: Optional[str] = os.getenv("S3_SECRET_ACCESS_KEY")
    s3_bucket_name: Optional[str] = os.getenv("S3_BUCKET_NAME")
    s3_addressing_style: Literal["auto", "virtual", "path"] = os.getenv("S3_ADDRESSING_STYLE", "auto") # type: ignore

    # Security Configuration
    encryption_key: Optional[str] = os.getenv("KODA_ENCRYPTION_KEY")

    # Email Configuration
    jmap_url: Optional[str] = os.getenv("JMAP_URL")
    jmap_token: Optional[str] = os.getenv("JMAP_TOKEN")
    imap_host: Optional[str] = os.getenv("IMAP_HOST")
    imap_port: int = int(os.getenv("IMAP_PORT", "993"))
    imap_user: Optional[str] = os.getenv("IMAP_USER")
    imap_password: Optional[str] = os.getenv("IMAP_PASSWORD")

    # Observability Configuration
    otel_exporter_otlp_endpoint: Optional[str] = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    otel_exporter_otlp_logs_endpoint: Optional[str] = os.getenv("OTEL_EXPORTER_OTLP_LOGS_ENDPOINT")

    # PostHog Configuration
    posthog_api_key: Optional[str] = os.getenv("POSTHOG_API_KEY")
    posthog_host: str = os.getenv("POSTHOG_HOST", "https://eu.i.posthog.com")

    # Sentry Configuration
    sentry_dsn: Optional[str] = os.getenv("SENTRY_DSN")

    # Dynamic OTel Context (Updated by logging module)
    trace_id: Optional[str] = None
    span_id: Optional[str] = None


# Global settings instance
settings = Settings()
