import os
import sys

# Prevent VSCode or OS BROWSER leak during tests
if "pytest" in sys.argv[0]:
    os.environ.pop("BROWSER", None)

from typing import Optional, Literal, Any
from pydantic import BaseModel, Field, model_validator, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict
from worldline import LoggingSettings


class S3(BaseModel):
    endpoint_url: Optional[str] = Field(default=None, validation_alias=AliasChoices("endpoint_url", "endPoint"))
    region_name: str = Field(default="us-east-1", validation_alias=AliasChoices("region_name", "region"))
    access_key_id: Optional[str] = Field(default=None, validation_alias=AliasChoices("access_key_id", "accessKey", "access_key"))
    secret_access_key: Optional[str] = Field(default=None, validation_alias=AliasChoices("secret_access_key", "secretKey", "secret_key"))
    bucket_name: Optional[str] = Field(default=None, validation_alias=AliasChoices("bucket_name", "bucket"))
    addressing_style: Literal["auto", "virtual", "path"] = Field(default="auto", validation_alias=AliasChoices("addressing_style", "pathStyle", "path_style"))

    @classmethod
    def from_dict(cls, data: dict) -> Optional["S3"]:
        if not data:
            return None
            
        # Handle the Windmill specific boolean to literal cast for pathStyle
        if "pathStyle" in data or "path_style" in data:
            val = data.get("pathStyle", data.get("path_style"))
            data["addressing_style"] = "path" if val is True else "auto"
            
        try:
            return cls(**data)
        except Exception:
            return None


class Settings(LoggingSettings, BaseSettings):
    """
    Centralized configuration for Koda.
    Loads values from environment variables with sensible defaults.
    """

    model_config = SettingsConfigDict(extra="ignore")

    # Client Configuration
    timeout: int = 30000
    browser: Optional[Literal["invisible_playwright", "cloakbrowser"]] = Field(default="invisible_playwright", validation_alias=AliasChoices("koda_browser", "browser"))
    browser_type: Optional[Literal["firefox", "chromium"]] = Field(default="firefox", validation_alias=AliasChoices("koda_browser_type", "browser_type"))

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
    windmill_base_url: Optional[str] = "https://app.windmill.dev"
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
    s3: Optional[S3] = None

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

# Global settings instance
settings = Settings()
