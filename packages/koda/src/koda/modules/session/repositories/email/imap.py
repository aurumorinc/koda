import aioimaplib
import email
from typing import Optional
from koda.config.main import settings
from koda.exceptions import KodaError


async def get_latest_email(address: str) -> Optional[str]:
    """
    Fetches the raw text of the most recent email for a given address using IMAP.
    """
    if not settings.imap_host or not settings.imap_user or not settings.imap_password:
        raise KodaError("IMAP configuration is missing.")

    client = aioimaplib.IMAP4_SSL(host=settings.imap_host, port=settings.imap_port)
    await client.wait_hello_from_server()
    
    try:
        await client.login(settings.imap_user, settings.imap_password)
        await client.select("INBOX")

        # Search for emails to the given address
        # Note: IMAP search syntax can be tricky. "TO {address}" is standard.
        status, messages = await client.search(f'TO "{address}"')
        if status != "OK" or not messages[0]:
            return None

        # Get the last message ID
        msg_ids = messages[0].split()
        if not msg_ids:
            return None
        
        latest_msg_id = msg_ids[-1].decode()

        # Fetch the email body
        status, data = await client.fetch(latest_msg_id, "RFC822")
        if status != "OK":
            return None

        # Parse the email content
        raw_email = data[1].decode("utf-8")
        msg = email.message_from_string(raw_email)

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if isinstance(payload, bytes):
                        return payload.decode("utf-8")
                    return str(payload)
        else:
            payload = msg.get_payload(decode=True)
            if isinstance(payload, bytes):
                return payload.decode("utf-8")
            return str(payload)

        return None

    finally:
        if client.has_capability("LOGOUT"):
            await client.logout()
