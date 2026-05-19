import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime, timedelta, timezone

from koda.schemas.session_schema import SessionModel, Session, UserDataParam, MFAParam
from koda.exceptions import SessionExhaustedError, KodaError
from koda.services.session_service import get_session, release_session, session_scope, resolve_mfa


def create_mock_session_model(
    id: str, 
    provider: str = "test_provider", 
    usage_count: int = 0, 
    error_score: float = 0.0,
    is_blocked: bool = False,
    mfa: MFAParam = None
) -> SessionModel:
    """Helper to create a mock SessionModel."""
    return SessionModel(
        id=id,
        metadata={"provider": provider},
        userData=UserDataParam(username="test", password="password", mfa=mfa),
        usageCount=usage_count,
        errorScore=error_score,
        maxErrorScore=3.0 if not is_blocked else 0.0, # Force blocked if needed
        createdAt=datetime.now(timezone.utc)
    )


@pytest.mark.asyncio
@patch("koda.services.session_service.redis.acquire_lock", new_callable=AsyncMock)
@patch("koda.services.session_service.windmill.list_sessions", new_callable=AsyncMock)
async def test_get_session_success(mock_list_sessions, mock_acquire_lock):
    # Arrange
    model1 = create_mock_session_model(id="1", usage_count=10)
    model2 = create_mock_session_model(id="2", usage_count=2) # Should be picked first
    
    mock_list_sessions.return_value = [model1, model2]
    mock_acquire_lock.return_value = "token-123"
    
    # Act
    session, token = await get_session({"provider": "test_provider"})
    
    # Assert
    assert session.id == "2"
    assert token == "token-123"
    mock_list_sessions.assert_called_once_with({"provider": "test_provider"})
    mock_acquire_lock.assert_called_once_with("session:2", ttl_seconds=300, timeout_seconds=1)


@pytest.mark.asyncio
@patch("koda.services.session_service.redis.acquire_lock", new_callable=AsyncMock)
@patch("koda.services.session_service.windmill.list_sessions", new_callable=AsyncMock)
async def test_get_session_skips_locked(mock_list_sessions, mock_acquire_lock):
    # Arrange
    model1 = create_mock_session_model(id="1", usage_count=1)
    model2 = create_mock_session_model(id="2", usage_count=2)
    
    mock_list_sessions.return_value = [model1, model2]
    # First lock fails (None), second succeeds
    mock_acquire_lock.side_effect = [None, "token-456"]
    
    # Act
    session, token = await get_session({"provider": "test_provider"})
    
    # Assert
    assert session.id == "2"
    assert token == "token-456"
    assert mock_acquire_lock.call_count == 2


@pytest.mark.asyncio
@patch("koda.services.session_service.redis.acquire_lock", new_callable=AsyncMock)
@patch("koda.services.session_service.windmill.list_sessions", new_callable=AsyncMock)
async def test_get_session_exhausted(mock_list_sessions, mock_acquire_lock):
    # Arrange
    model1 = create_mock_session_model(id="1", usage_count=1)
    
    mock_list_sessions.return_value = [model1]
    mock_acquire_lock.return_value = None # Lock fails
    
    # Act & Assert
    with pytest.raises(SessionExhaustedError, match="No usable sessions available for metadata: {'provider': 'test_provider'}"):
        await get_session({"provider": "test_provider"})


@pytest.mark.asyncio
@patch("koda.services.session_service.redis.release_lock", new_callable=AsyncMock)
@patch("koda.services.session_service.windmill.update_session", new_callable=AsyncMock)
async def test_release_session(mock_update_session, mock_release_lock):
    # Arrange
    model = create_mock_session_model(id="1")
    session = Session.from_model(model)
    token = "token-123"
    
    # Act
    await release_session(session, token)
    
    # Assert
    mock_update_session.assert_called_once_with("1", model)
    mock_release_lock.assert_called_once_with("session:1", "token-123")


@pytest.mark.asyncio
@patch("koda.services.session_service.release_session", new_callable=AsyncMock)
@patch("koda.services.session_service.get_session", new_callable=AsyncMock)
async def test_session_scope_success(mock_get_session, mock_release_session):
    # Arrange
    model = create_mock_session_model(id="1", usage_count=0, error_score=1.0)
    session = Session.from_model(model)
    mock_get_session.return_value = (session, "token-123")
    
    # Act
    async with session_scope({"provider": "test_provider"}) as s:
        assert s.id == "1"
        
    # Assert
    assert session.usage_count == 1 # mark_good increments usage
    assert session.error_score == 0.5 # mark_good decrements error score
    mock_release_session.assert_called_once_with(session, "token-123")


@pytest.mark.asyncio
@patch("koda.services.session_service.release_session", new_callable=AsyncMock)
@patch("koda.services.session_service.get_session", new_callable=AsyncMock)
async def test_session_scope_exception(mock_get_session, mock_release_session):
    # Arrange
    model = create_mock_session_model(id="1", usage_count=0, error_score=0.0)
    session = Session.from_model(model)
    mock_get_session.return_value = (session, "token-123")
    
    # Act & Assert
    with pytest.raises(ValueError, match="Test error"):
        async with session_scope({"provider": "test_provider"}) as s:
            raise ValueError("Test error")
            
    # Assert
    assert session.usage_count == 1 # mark_bad increments usage
    assert session.error_score == 1.0 # mark_bad increments error score
    mock_release_session.assert_called_once_with(session, "token-123")


@pytest.mark.asyncio
async def test_resolve_mfa_no_mfa():
    # Arrange
    model = create_mock_session_model(id="1")
    session = Session.from_model(model)
    
    # Act
    result = await resolve_mfa(session)
    
    # Assert
    assert result == ""


@pytest.mark.asyncio
@patch("koda.services.session_service.pyotp.TOTP")
async def test_resolve_mfa_totp(mock_totp):
    # Arrange
    mock_totp_instance = MagicMock()
    mock_totp_instance.now.return_value = "123456"
    mock_totp.return_value = mock_totp_instance
    
    mfa = MFAParam(strategy="totp", config={"secret": "base32secret"})
    model = create_mock_session_model(id="1", mfa=mfa)
    session = Session.from_model(model)
    
    # Act
    result = await resolve_mfa(session)
    
    # Assert
    assert result == "123456"
    mock_totp.assert_called_once_with("base32secret")


@pytest.mark.asyncio
@patch("koda.services.session_service.imap.get_latest_email", new_callable=AsyncMock)
async def test_resolve_mfa_imap(mock_get_latest_email):
    # Arrange
    mock_get_latest_email.return_value = "Your code is 654321."
    
    mfa = MFAParam(strategy="imap", config={"address": "test@example.com"})
    model = create_mock_session_model(id="1", mfa=mfa)
    session = Session.from_model(model)
    
    # Act
    result = await resolve_mfa(session)
    
    # Assert
    assert result == "654321"
    mock_get_latest_email.assert_called_once_with("test@example.com")


@pytest.mark.asyncio
@patch("koda.services.session_service.jmap.get_latest_email", new_callable=AsyncMock)
async def test_resolve_mfa_jmap_custom_pattern(mock_get_latest_email):
    # Arrange
    mock_get_latest_email.return_value = "Code: 9876"
    
    mfa = MFAParam(strategy="jmap", config={"address": "test@example.com", "pattern": r"\b\d{4}\b"})
    model = create_mock_session_model(id="1", mfa=mfa)
    session = Session.from_model(model)
    
    # Act
    result = await resolve_mfa(session)
    
    # Assert
    assert result == "9876"
    mock_get_latest_email.assert_called_once_with("test@example.com")


@pytest.mark.asyncio
async def test_resolve_mfa_unknown_strategy():
    # Arrange
    mfa = MFAParam(strategy="unknown", config={})
    model = create_mock_session_model(id="1", mfa=mfa)
    session = Session.from_model(model)
    
    # Act & Assert
    with pytest.raises(KodaError, match="Unknown MFA strategy: unknown"):
        await resolve_mfa(session)
