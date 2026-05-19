from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Literal

from pydantic import BaseModel, Field, ConfigDict


class CookieParam(BaseModel):
    """Dictionary representation of cookies."""
    model_config = ConfigDict(populate_by_name=True)

    name: str
    value: str
    domain: Optional[str] = None
    path: Optional[str] = None
    secure: Optional[bool] = None
    http_only: Optional[bool] = Field(None, alias='httpOnly')
    expires: Optional[int] = None
    same_site: Optional[Literal['Lax', 'None', 'Strict']] = Field(None, alias='sameSite')


class MFAParam(BaseModel):
    """Configuration for MFA resolution."""
    strategy: str  # e.g., "jmap", "totp"
    config: Dict[str, Any]


class UserDataParam(BaseModel):
    """Merged authentication and MFA configuration stored in Crawlee's userData."""
    username: str
    password: str
    mfa: Optional[MFAParam] = None


class SessionModel(BaseModel):
    """
    Model for a Session object, extending Crawlee's SessionModel.
    Renamed from SessionPayload to align with Crawlee naming.
    """
    model_config = ConfigDict(populate_by_name=True)

    # Crawlee Fields (with aliases for compatibility)
    id: str
    max_age: timedelta = Field(timedelta(minutes=50), alias='maxAge')
    user_data: UserDataParam = Field(alias='userData')
    max_error_score: float = Field(3.0, alias='maxErrorScore')
    error_score_decrement: float = Field(0.5, alias='errorScoreDecrement')
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), alias='createdAt')
    usage_count: int = Field(0, alias='usageCount')
    max_usage_count: int = Field(50, alias='maxUsageCount')
    error_score: float = Field(0.0, alias='errorScore')
    cookies: List[CookieParam] = Field(default_factory=list)
    blocked_status_codes: List[int] = Field(default_factory=lambda: [401, 403, 429], alias='blockedStatusCodes')

    # Koda Specific Fields
    metadata: Dict[str, Any] = Field(default_factory=dict)


@dataclass
class Session:
    """
    A lightweight wrapper around SessionModel providing an Apify-style API.
    Delegates I/O and orchestration to service functions.
    """

    model: SessionModel

    @property
    def id(self) -> str:
        """Return the session ID."""
        return self.model.id

    @property
    def user_data(self) -> UserDataParam:
        """Return the user data."""
        return self.model.user_data

    @property
    def cookies(self) -> List[CookieParam]:
        """Return the cookies."""
        return self.model.cookies

    @property
    def error_score(self) -> float:
        """Return the current error score."""
        return self.model.error_score

    @property
    def usage_count(self) -> int:
        """Return the current usage count."""
        return self.model.usage_count

    @property
    def expires_at(self) -> datetime:
        """Get the expiration datetime of the session."""
        return self.model.created_at + self.model.max_age

    @property
    def is_blocked(self) -> bool:
        """Indicate whether the session is blocked based on the error score."""
        return self.model.error_score >= self.model.max_error_score

    @property
    def is_expired(self) -> bool:
        """Indicate whether the session is expired based on the current time."""
        return datetime.now(timezone.utc) >= self.expires_at

    @property
    def is_max_usage_count_reached(self) -> bool:
        """Indicate whether the session has reached its maximum usage limit."""
        return self.model.usage_count >= self.model.max_usage_count

    @property
    def is_usable(self) -> bool:
        """Determine if the session is usable for next requests."""
        return not (self.is_blocked or self.is_expired or self.is_max_usage_count_reached)

    def mark_good(self) -> None:
        """
        Mark the session as successful.
        Decrements error score and increments usage count.
        """
        self.model.usage_count += 1
        if self.model.error_score > 0:
            self.model.error_score = max(0.0, self.model.error_score - self.model.error_score_decrement)

        if not self.is_usable:
            self.retire()

    def mark_bad(self) -> None:
        """
        Mark the session as failed.
        Increments error score and usage count.
        """
        self.model.error_score += 1.0
        self.model.usage_count += 1

        if not self.is_usable:
            self.retire()

    def retire(self) -> None:
        """Retire the session by setting the error score to the maximum value."""
        self.model.error_score = self.model.max_error_score

    def is_blocked_status_code(self, status_code: int) -> bool:
        """Evaluate whether a session should be retired based on the received HTTP status code."""
        return status_code in self.model.blocked_status_codes

    def get_state(self, as_dict: bool = False) -> SessionModel | dict:
        """Retrieve the current state of the session either as a model or as a dictionary."""
        if as_dict:
            return self.model.model_dump(by_alias=True)
        return self.model

    @classmethod
    def from_model(cls, model: SessionModel) -> Session:
        """Initialize a new instance from a `SessionModel`."""
        return cls(model=model)
