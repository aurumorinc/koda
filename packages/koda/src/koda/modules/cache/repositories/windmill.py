from worldline import structlog
from pathlib import Path
from typing import Any, Dict, Optional

import httpx

from koda.config.main import settings
from koda.modules.cache.schema import CacheEntry

logger = structlog.get_logger("koda.modules.cache.windmill")


def _get_state_path() -> str:
    """
    Determine the Windmill state path from settings.
    """
    if settings.windmill_state_path:
        return settings.windmill_state_path
    if settings.windmill_state_path_file:
        try:
            return Path(settings.windmill_state_path_file).read_text().strip()
        except Exception as e:
            logger.warning("Failed to read windmill_state_path_file: %s", e)
    return "u/local/koda_state"


async def _fetch_state() -> Dict[str, Any]:
    """
    Fetch the current state dictionary from Windmill.
    """
    if not settings.windmill_workspace or not settings.windmill_token:
        logger.warning("Windmill workspace or token not configured. Cannot fetch state.")
        return {}

    path = _get_state_path()
    url = f"{settings.windmill_base_url}/api/w/{settings.windmill_workspace}/resources/get_value_interpolated/{path}"
    headers = {"Authorization": f"Bearer {settings.windmill_token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 404:
                return {}
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Failed to fetch state from Windmill: %s", e)
            return {}


async def get(key: str) -> Optional[CacheEntry]:
    """
    Retrieve a cache entry from Windmill state.
    """
    state = await _fetch_state()
    if key not in state:
        return None

    try:
        return CacheEntry.model_validate(state[key])
    except Exception as e:
        logger.error("Failed to validate cache entry for key %s: %s", key, e)
        return None


async def set(entry: CacheEntry) -> None:
    """
    Update a cache entry in Windmill state.
    """
    if not settings.windmill_workspace or not settings.windmill_token:
        logger.warning("Windmill workspace or token not configured. Cannot update state.")
        return

    state = await _fetch_state()
    state[entry.key] = entry.model_dump(mode="json")

    path = _get_state_path()
    url = f"{settings.windmill_base_url}/api/w/{settings.windmill_workspace}/resources/update_value/{path}"
    headers = {"Authorization": f"Bearer {settings.windmill_token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json={"value": state})
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.error("Failed to update state in Windmill: %s", e)
