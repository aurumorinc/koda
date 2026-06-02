from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field


class CacheEntry(BaseModel):
    """
    Pydantic model representing a cache entry.
    Ensures strict type safety and validation for cached payloads.
    """
    key: str = Field(..., description="The fully prefixed cache key")
    value: Any = Field(..., description="The cached value (e.g., XPath string, JSON dictionary)")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of when the entry was created")
    expires_at: Optional[datetime] = Field(default=None, description="Optional expiration timestamp")
