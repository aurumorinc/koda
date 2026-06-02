import logging
from datetime import datetime, timezone
from typing import Any, Optional

from koda.config.main import settings
from koda.modules.cache.repositories import windmill
from koda.modules.cache.schema import CacheEntry

logger = logging.getLogger("koda.modules.cache")


async def get(key: str) -> Optional[Any]:
    """
    Retrieve a value from the cache.
    """
    prefixed_key = f"{settings.cache_prefix}{key}"
    
    try:
        if settings.cache_repository == "windmill":
            entry = await windmill.get(prefixed_key)
        else:
            logger.warning("Unsupported cache repository: %s", settings.cache_repository)
            return None
            
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


async def set(key: str, value: Any) -> None:
    """
    Store a value in the cache.
    """
    prefixed_key = f"{settings.cache_prefix}{key}"
    
    try:
        entry = CacheEntry(key=prefixed_key, value=value)
        
        if settings.cache_repository == "windmill":
            await windmill.set(entry)
            logger.info("Successfully cached value for key: %s", prefixed_key)
        else:
            logger.warning("Unsupported cache repository: %s", settings.cache_repository)
            
    except Exception as e:
        logger.error("Failed to set cache entry for key %s: %s", prefixed_key, e)
