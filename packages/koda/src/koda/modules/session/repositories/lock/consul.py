import asyncio
import logging
from typing import Optional

import httpx

from koda.config.main import settings

logger = logging.getLogger(__name__)


async def acquire_lock(
    lock_name: str,
    ttl_seconds: int = 30,
    timeout_seconds: int = 10,
) -> Optional[str]:
    """
    Acquire a lock in Consul using a session.
    Returns the session ID if successful, None otherwise.
    """
    async with httpx.AsyncClient(base_url=settings.consul_base_url) as client:
        # 1. Create a session with a TTL
        session_payload = {
            "Name": f"koda-lock-{lock_name}",
            "TTL": f"{ttl_seconds}s",
            "Behavior": "release",
        }
        try:
            resp = await client.put("/v1/session/create", json=session_payload)
            resp.raise_for_status()
            session_id = resp.json()["ID"]
        except (httpx.HTTPError, KeyError) as exc:
            logger.error(f"Failed to create Consul session: {exc!r}")
            return None

        # 2. Attempt to acquire the lock (KV PUT with ?acquire=session_id)
        # We poll until the lock is acquired or timeout_seconds elapses.
        kv_path = f"/v1/kv/koda/locks/{lock_name}"
        start_time = asyncio.get_event_loop().time()
        
        try:
            while True:
                resp = await client.put(
                    kv_path,
                    params={"acquire": session_id},
                )
                resp.raise_for_status()
                
                if resp.json() is True:
                    return session_id
                
                # Check for timeout
                if asyncio.get_event_loop().time() - start_time > timeout_seconds:
                    logger.warning(f"Timed out waiting for Consul lock {lock_name!r}")
                    await client.put(f"/v1/session/destroy/{session_id}")
                    return None
                
                # Wait a bit before retrying
                await asyncio.sleep(0.5)
                
        except httpx.HTTPError as exc:
            logger.error(f"Failed to acquire Consul lock {lock_name!r}: {exc!r}")
            await client.put(f"/v1/session/destroy/{session_id}")
            return None


async def release_lock(lock_name: str, session_id: str) -> bool:
    """
    Release a lock by destroying the Consul session.
    """
    async with httpx.AsyncClient(base_url=settings.consul_base_url) as client:
        try:
            resp = await client.put(f"/v1/session/destroy/{session_id}")
            resp.raise_for_status()
            return True
        except httpx.HTTPError as exc:
            logger.error(f"Failed to release Consul lock {lock_name!r}: {exc!r}")
            return False


def start_heartbeat(session_id: str, interval_seconds: int = 15) -> asyncio.Task:
    """
    Start a background task to renew the Consul session.
    """
    return asyncio.create_task(_renew_session_loop(session_id, interval_seconds))


async def _renew_session_loop(session_id: str, interval_seconds: int) -> None:
    """
    Internal loop for session renewal.
    """
    async with httpx.AsyncClient(base_url=settings.consul_base_url) as client:
        while True:
            try:
                resp = await client.put(f"/v1/session/renew/{session_id}")
                if resp.status_code == 404:
                    logger.warning(f"Consul session {session_id!r} not found, stopping heartbeat.")
                    break
                resp.raise_for_status()
                logger.debug(f"Renewed Consul session {session_id!r}")
            except httpx.HTTPError as exc:
                logger.error(f"Error renewing Consul session {session_id!r}: {exc!r}")
            
            await asyncio.sleep(interval_seconds)
