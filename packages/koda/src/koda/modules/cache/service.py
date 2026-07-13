import structlog
from datetime import datetime, timezone
from typing import Any, Optional

from koda.config.main import settings
from koda.modules.cache.schema import CacheEntry

logger = structlog.get_logger("koda.modules.cache")


class CacheService:
    """Service for managing cache operations."""

    def __init__(self, cache_repo: Any):
        self.cache_repo = cache_repo

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache.
        """
        prefixed_key = f"{settings.cache_prefix}{key}"
        
        try:
            entry = await self.cache_repo.get(prefixed_key)
                
            if not entry:
                logger.info("Cache miss for key: %s", prefixed_key)
                return None
                
            if entry.expires_at and entry.expires_at < datetime.now(timezone.utc):
                logger.info("Cache entry expired for key: %s", prefixed_key)
                return None
                
            logger.info("Cache hit for key: %s", prefixed_key)
            return entry.value
            
        except Exception as e:
            logger.error("Failed to retrieve cache entry for key %s: %s", prefixed_key, e)
            return None

    async def set(self, key: str, value: Any) -> None:
        """
        Store a value in the cache.
        """
        prefixed_key = f"{settings.cache_prefix}{key}"
        
        try:
            entry = CacheEntry(key=prefixed_key, value=value)
            await self.cache_repo.set(entry)
            logger.info("Successfully cached value for key: %s", prefixed_key)
                
        except Exception as e:
            logger.error("Failed to set cache entry for key %s: %s", prefixed_key, e)
