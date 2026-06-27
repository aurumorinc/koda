import asyncio
from worldline import structlog
import uuid
from typing import Optional

from upstash_redis.asyncio import Redis

from koda.config.main import settings

logger = structlog.get_logger(__name__)


def _get_client() -> Redis:
    """Initialize the Upstash Redis client."""
    if not settings.upstash_redis_rest_url or not settings.upstash_redis_rest_token:
        raise ValueError(
            "UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN must be set "
            "to use the Redis lock repository."
        )
    return Redis(
        url=settings.upstash_redis_rest_url,
        token=settings.upstash_redis_rest_token
    )


async def acquire_lock(
    lock_name: str,
    ttl_seconds: int = 30,
    timeout_seconds: int = 10,
) -> Optional[str]:
    """
    Acquire a lock in Redis using SET NX PX.
    Returns a unique identifier (token) if successful, None otherwise.
    """
    client = _get_client()
    token = str(uuid.uuid4())
    key = f"koda:lock:{lock_name}"
    
    # Convert TTL to milliseconds for PX
    ttl_ms = ttl_seconds * 1000
    
    start_time = asyncio.get_event_loop().time()
    try:
        while True:
            # Attempt to acquire the lock
            # NX: Only set the key if it does not already exist
            # PX: Set the specified expire time, in milliseconds
            if await client.set(key, token, nx=True, px=ttl_ms):
                return token
            
            # Check for timeout
            if asyncio.get_event_loop().time() - start_time > timeout_seconds:
                return None
            
            # Wait a bit before retrying
            await asyncio.sleep(0.1)
    except Exception as exc:
        logger.error(f"Failed to acquire Redis lock {lock_name!r}: {exc!r}")
        return None


async def release_lock(lock_name: str, token: str) -> bool:
    """
    Release a lock in Redis using a Lua script to ensure atomicity.
    Only releases the lock if the token matches.
    """
    client = _get_client()
    key = f"koda:lock:{lock_name}"
    
    # Lua script to release the lock safely
    script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    try:
        # upstash-redis eval signature: eval(script, keys, args)
        result = await client.eval(script, [key], [token])
        return bool(result)
    except Exception as exc:
        logger.error(f"Failed to release Redis lock {lock_name!r}: {exc!r}")
        return False


def start_heartbeat(lock_name: str, token: str, ttl_seconds: int = 30) -> asyncio.Task:
    """
    Start a background task to renew the Redis lock.
    """
    return asyncio.create_task(_renew_lock_loop(lock_name, token, ttl_seconds))


async def _renew_lock_loop(lock_name: str, token: str, ttl_seconds: int) -> None:
    """
    Internal loop for lock renewal.
    """
    client = _get_client()
    key = f"koda:lock:{lock_name}"
    ttl_ms = ttl_seconds * 1000
    interval = max(1, ttl_seconds // 2)
    
    # Lua script to renew the lock safely
    script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("pexpire", KEYS[1], ARGV[2])
    else
        return 0
    end
    """
    
    while True:
        try:
            result = await client.eval(script, [key], [str(token), str(ttl_ms)])
            if not result:
                logger.warning(f"Redis lock {lock_name!r} lost or token mismatch, stopping heartbeat.")
                break
            logger.debug(f"Renewed Redis lock {lock_name!r}")
        except Exception as exc:
            logger.error(f"Error renewing Redis lock {lock_name!r}: {exc!r}")
        
        await asyncio.sleep(interval)
