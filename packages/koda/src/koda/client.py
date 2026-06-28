"""Core client for the Koda extraction engine."""

from __future__ import annotations

from typing import Any

from koda.config.main import Settings, settings, S3
from koda.modules.cache import service as cache

__all__ = ["KodaClient"]

class KodaClient:
    """Primary interface for the Koda extraction infrastructure."""
    
    def __init__(self, s3_resource: dict | Any | None = None, **kwargs: Any) -> None:
        """Initialize the KodaClient."""
        
        # Hydrate S3 resource if passed
        if s3_resource:
            if isinstance(s3_resource, dict):
                kwargs["s3"] = S3.from_dict(s3_resource)
            elif isinstance(s3_resource, S3):
                kwargs["s3"] = s3_resource

        if kwargs:
            settings_dump = settings.model_dump()
            settings_dump.update(kwargs)
            settings_valid = Settings.model_validate(settings_dump)
            settings.__dict__.update(settings_valid.__dict__)

        # Expose the unified cache adapter
        self.cache = cache
        
    async def __aenter__(self) -> KodaClient:
        return self
        
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass
