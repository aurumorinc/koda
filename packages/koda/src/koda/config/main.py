import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Settings:
    """
    Centralized configuration for Koda.
    Loads values from environment variables with sensible defaults.
    """

    # Storage Configuration
    storage_repository: str = os.getenv("STORAGE_REPOSITORY", "windmill")
    
    # Windmill Configuration
    windmill_token: Optional[str] = os.getenv("WINDMILL_TOKEN")
    windmill_base_url: str = os.getenv("WINDMILL_BASE_URL", "https://app.windmill.dev")
    windmill_workspace: Optional[str] = os.getenv("WINDMILL_WORKSPACE")

    # Lock Configuration
    lock_repository: str = os.getenv("LOCK_REPOSITORY", "consul")
    lock_ttl_seconds: int = int(os.getenv("LOCK_TTL_SECONDS", "30"))
    lock_timeout_seconds: int = int(os.getenv("LOCK_TIMEOUT_SECONDS", "10"))
    
    # Consul Configuration
    consul_base_url: str = os.getenv("CONSUL_BASE_URL", "http://localhost:8500")

    # Redis Configuration (Upstash)
    upstash_redis_rest_url: Optional[str] = os.getenv("UPSTASH_REDIS_REST_URL")
    upstash_redis_rest_token: Optional[str] = os.getenv("UPSTASH_REDIS_REST_TOKEN")

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


# Global settings instance
settings = Settings()
