from worldline import structlog
import os
import re
import shutil
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Tuple

import pyotp

from koda.exceptions import KodaError, SessionExhaustedError
from koda.modules.browser.service import BrowserSession
from koda.modules.session.schema import Session

logger = structlog.get_logger(__name__)


class SessionService:
    """Service for managing browser sessions, including locking, storage, and MFA resolution."""

    def __init__(
        self,
        storage_repo: Any,
        lock_repo: Any,
        email_repo_imap: Any,
        email_repo_jmap: Any,
        s3_repo: Any,
    ):
        self.storage_repo = storage_repo
        self.lock_repo = lock_repo
        self.email_repo_imap = email_repo_imap
        self.email_repo_jmap = email_repo_jmap
        self.s3_repo = s3_repo

    async def get_session(self, metadata: dict[str, Any]) -> Tuple[Session, str]:
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
        session_models = await self.storage_repo.list_sessions(metadata)
        
        # 2. Map to Session objects
        sessions = [Session.from_model(model) for model in session_models]
        
        # 3. Filter usable sessions
        usable_sessions = [s for s in sessions if s.is_usable]
        
        # 4. Sort by usage_count (ascending) and error_score (ascending)
        usable_sessions.sort(key=lambda s: (s.usage_count, s.error_score))
        
        # 5. Iterate and attempt to lock
        for session in usable_sessions:
            lock_key = f"session:{session.id}"
            token = await self.lock_repo.acquire_lock(lock_key, ttl_seconds=300, timeout_seconds=1)
            
            if token:
                logger.debug(f"Acquired lock for session {session.id}")
                return session, token
                
        # 6. If we get here, no sessions could be locked or none were usable
        raise SessionExhaustedError(f"No usable sessions available for metadata: {metadata}")

    async def release_session(self, session: Session, lock_token: str) -> None:
        """
        Update the session state in storage and release its lock.
        
        Args:
            session: The Session object to update.
            lock_token: The token used to acquire the lock.
        """
        # 1. Update session in storage
        await self.storage_repo.update_session(session.id, session.model)
        
        # 2. Release the lock
        lock_key = f"session:{session.id}"
        await self.lock_repo.release_lock(lock_key, lock_token)
        logger.debug(f"Released lock for session {session.id}")

    @asynccontextmanager
    async def browser_session_scope(self, metadata: dict[str, Any]) -> AsyncGenerator[Tuple[Session, Any], None]:
        """
        Async context manager for safely using a browser session.
        Automatically handles locking, S3 profile sync, browser launch, state updates, and releasing.
        
        Args:
            metadata: A dictionary of metadata key-value pairs to filter sessions by.
            
        Yields:
            A tuple containing the locked Session object and the browser context.
        """
        session, token = await self.get_session(metadata)
        local_profile_dir = f"/tmp/koda_profiles/{session.id}"
        
        try:
            if session.model.browser.user_data_dir:
                await self.s3_repo.download_profile(session.model.browser.user_data_dir, local_profile_dir)
            else:
                os.makedirs(local_profile_dir, exist_ok=True)
                
            async with BrowserSession(
                config=session.model.browser.config,
                user_data_dir=local_profile_dir
            ) as browser_context:
                yield session, browser_context
                session.mark_good()
        except Exception:
            session.mark_bad()
            raise
        finally:
            try:
                s3_key = await self.s3_repo.upload_profile(local_profile_dir, session.id)
                session.model.browser.user_data_dir = s3_key
            except Exception:
                logger.error(f"Failed to upload profile for session {session.id}", exc_info=True)
                
            if os.path.exists(local_profile_dir):
                shutil.rmtree(local_profile_dir, ignore_errors=True)
                
            await self.release_session(session, token)

    async def resolve_mfa(self, session: Session) -> str:
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
            return await self._resolve_totp(config)
        elif strategy in ("imap", "jmap"):
            return await self._resolve_email_otp(strategy, config)
        else:
            raise KodaError(f"Unknown MFA strategy: {strategy}")

    async def _resolve_totp(self, config: dict[str, Any]) -> str:
        """Resolve a TOTP MFA challenge."""
        secret = config.get("secret")
        if not secret:
            raise KodaError("TOTP secret is missing in MFA config.")
        return pyotp.TOTP(secret).now()

    async def _resolve_email_otp(self, strategy: str, config: dict[str, Any]) -> str:
        """Resolve an email-based OTP MFA challenge using IMAP or JMAP."""
        address = config.get("address")
        if not address:
            raise KodaError(f"Email address is missing in {strategy} MFA config.")
            
        # Fetch the latest email
        if strategy == "imap":
            raw_text = await self.email_repo_imap.get_latest_email(address)
        else:
            raw_text = await self.email_repo_jmap.get_latest_email(address)
            
        if not raw_text:
            raise KodaError(f"Failed to fetch email for {address} via {strategy} or email is empty.")
            
        # Extract the code using regex
        pattern = config.get("pattern", r"\b\d{6}\b")
        match = re.search(pattern, raw_text)
        
        if match:
            return match.group(0)
            
        raise KodaError(f"Failed to extract MFA code from {strategy} email using pattern {pattern}.")
