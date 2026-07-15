"""Core client for the Koda extraction engine."""

from __future__ import annotations

from typing import Any

from koda.config.main import Settings, settings
from koda.modules.cache import service as cache

__all__ = ["KodaClient"]

class KodaClient:
    """Primary interface for the Koda extraction infrastructure."""
    
    def __init__(self, **kwargs: Any) -> None:
        """Initialize the KodaClient."""

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
