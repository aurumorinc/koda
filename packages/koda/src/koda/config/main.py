from typing import Optional, Literal
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from python_logging.config import LoggingSettings
from python_logging.main import setup_logging


class Settings(LoggingSettings, BaseSettings):
    """
    Centralized configuration for Koda.
    Loads values from environment variables with sensible defaults.
    """

    model_config = SettingsConfigDict(extra="ignore")

    # Client Configuration
    timeout: int = 30000
    browser: Optional[Literal["invisible_playwright", "cloakbrowser"]] = "invisible_playwright"
    browser_type: Optional[Literal["firefox", "chromium"]] = "firefox"

    @model_validator(mode="after")
    def validate_browser(self) -> "Settings":
        # If neither is set, default to firefox + invisible_playwright
        if self.browser is None and self.browser_type is None:
            self.browser_type = "firefox"
            self.browser = "invisible_playwright"
        # If only browser_type is set, infer browser
        elif self.browser is None and self.browser_type is not None:
            if self.browser_type == "firefox":
                self.browser = "invisible_playwright"
            elif self.browser_type == "chromium":
                self.browser = "cloakbrowser"
        # If only browser is set, infer browser_type
        elif self.browser is not None and self.browser_type is None:
            if self.browser == "invisible_playwright":
                self.browser_type = "firefox"
            elif self.browser == "cloakbrowser":
                self.browser_type = "chromium"
        
        # Validate combinations
        if self.browser == "invisible_playwright" and self.browser_type != "firefox":
            raise ValueError("browser 'invisible_playwright' must be used with browser_type 'firefox'")
        if self.browser == "cloakbrowser" and self.browser_type != "chromium":
            raise ValueError("browser 'cloakbrowser' must be used with browser_type 'chromium'")
            
        return self

    # Storage Configuration
    storage_repository: str = "windmill"
    
    # Cache Configuration
    cache_repository: str = "windmill"
    cache_prefix: str = "koda.modules.cache:"

    # Windmill Configuration
    windmill_token: Optional[str] = None
    windmill_base_url: str = "https://app.windmill.dev"
    windmill_workspace: Optional[str] = None
    windmill_state_path: Optional[str] = Field(default=None, validation_alias="WM_STATE_PATH")
    windmill_state_path_file: Optional[str] = Field(default=None, validation_alias="WM_STATE_PATH_FILE")

    # Lock Configuration
    lock_repository: str = "consul"
    lock_ttl_seconds: int = 30
    lock_timeout_seconds: int = 10
    
    # Consul Configuration
    consul_base_url: str = "http://localhost:8500"

    # Redis Configuration (Upstash)
    upstash_redis_rest_url: Optional[str] = None
    upstash_redis_rest_token: Optional[str] = None

    # S3 Configuration
    s3_endpoint_url: Optional[str] = None
    s3_region_name: str = "us-east-1"
    s3_access_key_id: Optional[str] = None
    s3_secret_access_key: Optional[str] = None
    s3_bucket_name: Optional[str] = None
    s3_addressing_style: Literal["auto", "virtual", "path"] = "auto"

    # Security Configuration
    encryption_key: Optional[str] = Field(default=None, validation_alias="KODA_ENCRYPTION_KEY")

    # Email Configuration
    jmap_url: Optional[str] = None
    jmap_token: Optional[str] = None
    imap_host: Optional[str] = None
    imap_port: int = 993
    imap_user: Optional[str] = None
    imap_password: Optional[str] = None

    # PostHog Configuration
    posthog_api_key: Optional[str] = None
    posthog_host: str = "https://eu.i.posthog.com"

    # Sentry Configuration
    sentry_dsn: Optional[str] = None


# Global settings instance
settings = Settings()

# Initialize global logging state
setup_logging(settings)
