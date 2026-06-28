import httpx
from typing import Optional
from koda.config.main import settings
from koda.exceptions import Error


async def get_latest_email(address: str) -> Optional[str]:
    """
    Fetches the raw text of the most recent email for a given address using JMAP.
    """
    if not settings.jmap_url or not settings.jmap_token:
        raise Error("JMAP configuration is missing.")

    headers = {
        "Authorization": f"Bearer {settings.jmap_token}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        # 1. Get Session to find accountId
        session_res = await client.get(settings.jmap_url, headers=headers)
        session_res.raise_for_status()
        session_data = session_res.json()
        account_id = session_data["primaryAccounts"]["urn:ietf:params:jmap:mail"]

        # 2. Query for the latest email to the given address
        query_body = {
            "using": ["urn:ietf:params:jmap:core", "urn:ietf:params:jmap:mail"],
            "methodCalls": [
                [
                    "Email/query",
                    {
                        "accountId": account_id,
                        "filter": {"to": address},
                        "sort": [{"property": "receivedAt", "isAscending": False}],
                        "limit": 1,
                    },
                    "a",
                ],
                [
                    "Email/get",
                    {
                        "accountId": account_id,
                        "#ids": {
                            "resultOf": "a",
                            "name": "Email/query",
                            "path": "/ids",
                        },
                        "properties": ["bodyValues", "textBody"],
                    },
                    "b",
                ],
            ],
        }

        api_url = session_data["apiUrl"]
        res = await client.post(api_url, headers=headers, json=query_body)
        res.raise_for_status()
        data = res.json()

        # Parse results
        email_get_res = next(
            (call[1] for call in data["methodResponses"] if call[0] == "Email/get"), None
        )

        if not email_get_res or not email_get_res.get("list"):
            return None

        latest_email = email_get_res["list"][0]
        text_body_info = latest_email.get("textBody", [])
        if not text_body_info:
            return None

        part_id = text_body_info[0]["partId"]
        return latest_email["bodyValues"][part_id]["value"]
