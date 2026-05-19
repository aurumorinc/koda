from typing import List, Optional, Any, Dict

import httpx

from koda.config.main import settings
from koda.schemas.session_schema import SessionModel


async def list_sessions(metadata: Optional[Dict[str, Any]] = None) -> List[SessionModel]:
    """
    List all sessions from Windmill resources.
    Uses the resource_type filter for efficiency and filters by metadata in-memory.
    """
    if not settings.windmill_workspace:
        return []

    url = (
        f"{settings.windmill_base_url}/api/w/"
        f"{settings.windmill_workspace}/resources/list"
    )
    headers = {"Authorization": f"Bearer {settings.windmill_token}"}
    params = {
        "resource_type": "koda_session",
        "per_page": 100,  # Fetch up to 100 sessions at once
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        resources = response.json()

    # Map to SessionModel
    sessions: List[SessionModel] = [SessionModel.model_validate(res["value"]) for res in resources]

    if metadata:
        # Filter sessions where all key-value pairs in the requested metadata match the session's metadata
        return [
            s for s in sessions 
            if all(s.metadata.get(k) == v for k, v in metadata.items())
        ]

    return sessions


async def update_session(session_id: str, model: SessionModel) -> None:
    """
    Update a session resource value in Windmill.
    Uses the update_value endpoint which expects {"value": ...}
    """
    if not settings.windmill_workspace:
        return

    # Use update_value endpoint for cleaner value-only updates
    url = (
        f"{settings.windmill_base_url}/api/w/"
        f"{settings.windmill_workspace}/resources/update_value/{session_id}"
    )
    headers = {"Authorization": f"Bearer {settings.windmill_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json={"value": model.model_dump(by_alias=True)})
        response.raise_for_status()
