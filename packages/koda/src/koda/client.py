"""Core client for the Koda extraction engine."""

from __future__ import annotations

from typing import Any

from koda.modules.cache import service as cache

__all__ = ["KodaClient"]

class KodaClient:
    """Primary interface for the Koda extraction infrastructure."""
    
    def __init__(self) -> None:
        """Initialize the KodaClient."""
        # Expose the unified cache adapter
        self.cache = cache
        
    async def __aenter__(self) -> KodaClient:
        return self
        
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass
