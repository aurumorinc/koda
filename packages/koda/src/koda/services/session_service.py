import logging
import re
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Tuple

import pyotp

from koda.exceptions import KodaError, SessionExhaustedError
from koda.repositories.email import imap, jmap
from koda.repositories.lock import redis
from koda.repositories.storage import windmill
from koda.schemas.session_schema import Session

logger = logging.getLogger(__name__)


async def get_session(metadata: dict[str, Any]) -> Tuple[Session, str]:
    """
    Retrieve a usable session matching the given metadata and acquire a lock on it.
    
    Args:
        metadata: A dictionary of metadata key-value pairs to filter sessions by.
        
    Returns:
        A tuple containing the Session object and the lock token.
        
    Raises:
        SessionExhaustedError: If no usable sessions are available or can be locked.
    """
    # 1. Fetch sessions from storage
    session_models = await windmill.list_sessions(metadata)
    
    # 2. Map to Session objects
    sessions = [Session.from_model(model) for model in session_models]
    
    # 3. Filter usable sessions
    usable_sessions = [s for s in sessions if s.is_usable]
    
    # 4. Sort by usage_count (ascending) and error_score (ascending)
    usable_sessions.sort(key=lambda s: (s.usage_count, s.error_score))
    
    # 5. Iterate and attempt to lock
    for session in usable_sessions:
        lock_key = f"session:{session.id}"
        token = await redis.acquire_lock(lock_key, ttl_seconds=300, timeout_seconds=1)
        
        if token:
            logger.debug(f"Acquired lock for session {session.id}")
            return session, token
            
    # 6. If we get here, no sessions could be locked or none were usable
    raise SessionExhaustedError(f"No usable sessions available for metadata: {metadata}")


async def release_session(session: Session, lock_token: str) -> None:
    """
    Update the session state in storage and release its lock.
    
    Args:
        session: The Session object to update.
        lock_token: The token used to acquire the lock.
    """
    # 1. Update session in storage
    await windmill.update_session(session.id, session.model)
    
    # 2. Release the lock
    lock_key = f"session:{session.id}"
    await redis.release_lock(lock_key, lock_token)
    logger.debug(f"Released lock for session {session.id}")


@asynccontextmanager
async def session_scope(metadata: dict[str, Any]) -> AsyncGenerator[Session, None]:
    """
    Async context manager for safely using a session.
    Automatically handles locking, state updates (mark_good/mark_bad), and releasing.
    
    Args:
        metadata: A dictionary of metadata key-value pairs to filter sessions by.
        
    Yields:
        A locked, usable Session object.
    """
    session, token = await get_session(metadata)
    
    try:
        yield session
    except Exception:
        session.mark_bad()
        raise
    else:
        session.mark_good()
    finally:
        await release_session(session, token)


async def resolve_mfa(session: Session) -> str:
    """
    Resolve the MFA challenge for a given session.
    
    Args:
        session: The Session object containing MFA configuration.
        
    Returns:
        The resolved MFA code as a string.
        
    Raises:
        KodaError: If MFA configuration is missing, invalid, or resolution fails.
    """
    if not session.model.user_data.mfa:
        return ""
        
    strategy = session.model.user_data.mfa.strategy
    config = session.model.user_data.mfa.config
    
    if strategy == "totp":
        return await _resolve_totp(config)
    elif strategy in ("imap", "jmap"):
        return await _resolve_email_otp(strategy, config)
    else:
        raise KodaError(f"Unknown MFA strategy: {strategy}")


async def _resolve_totp(config: dict[str, Any]) -> str:
    """Resolve a TOTP MFA challenge."""
    secret = config.get("secret")
    if not secret:
        raise KodaError("TOTP secret is missing in MFA config.")
    return pyotp.TOTP(secret).now()


async def _resolve_email_otp(strategy: str, config: dict[str, Any]) -> str:
    """Resolve an email-based OTP MFA challenge using IMAP or JMAP."""
    address = config.get("address")
    if not address:
        raise KodaError(f"Email address is missing in {strategy} MFA config.")
        
    # Fetch the latest email
    if strategy == "imap":
        raw_text = await imap.get_latest_email(address)
    else:
        raw_text = await jmap.get_latest_email(address)
        
    if not raw_text:
        raise KodaError(f"Failed to fetch email for {address} via {strategy} or email is empty.")
        
    # Extract the code using regex
    pattern = config.get("pattern", r"\b\d{6}\b")
    match = re.search(pattern, raw_text)
    
    if match:
        return match.group(0)
        
    raise KodaError(f"Failed to extract MFA code from {strategy} email using pattern {pattern}.")
