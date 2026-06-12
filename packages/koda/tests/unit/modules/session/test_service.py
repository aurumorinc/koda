import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime, timedelta, timezone

from koda.modules.session.schema import SessionModel, Session, UserDataParam, MFAParam, BrowserParam
from koda.exceptions import SessionExhaustedError, KodaError
from koda.modules.session.service import SessionService


def create_mock_session_model(
    id: str, 
    provider: str = "test_provider", 
    usage_count: int = 0, 
    error_score: float = 0.0,
    is_blocked: bool = False,
    mfa: MFAParam = None,
    browser: BrowserParam = None
) -> SessionModel:
    """Helper to create a mock SessionModel."""
    if browser is None:
        browser = BrowserParam()
    return SessionModel(
        id=id,
        metadata={"provider": provider},
        userData=UserDataParam(username="test", password="password", mfa=mfa),
        usageCount=usage_count,
        errorScore=error_score,
        maxErrorScore=3.0 if not is_blocked else 0.0, # Force blocked if needed
        createdAt=datetime.now(timezone.utc),
        browser=browser
    )

@pytest.fixture
def mock_repos():
    return {
        "storage_repo": AsyncMock(),
        "lock_repo": AsyncMock(),
        "email_repo_imap": AsyncMock(),
        "email_repo_jmap": AsyncMock(),
        "s3_repo": AsyncMock(),
    }

@pytest.fixture
def session_service(mock_repos):
    return SessionService(**mock_repos)


@pytest.mark.asyncio
async def test_get_session_success(session_service, mock_repos):
    # Arrange
    model1 = create_mock_session_model(id="1", usage_count=10)
    model2 = create_mock_session_model(id="2", usage_count=2) # Should be picked first
    
    mock_repos["storage_repo"].list_sessions.return_value = [model1, model2]
    mock_repos["lock_repo"].acquire_lock.return_value = "token-123"
    
    # Act
    session, token = await session_service.get_session({"provider": "test_provider"})
    
    # Assert
    assert session.id == "2"
    assert token == "token-123"
    mock_repos["storage_repo"].list_sessions.assert_called_once_with({"provider": "test_provider"})
    mock_repos["lock_repo"].acquire_lock.assert_called_once_with("session:2", ttl_seconds=300, timeout_seconds=1)


@pytest.mark.asyncio
async def test_get_session_skips_locked(session_service, mock_repos):
    # Arrange
    model1 = create_mock_session_model(id="1", usage_count=1)
    model2 = create_mock_session_model(id="2", usage_count=2)
    
    mock_repos["storage_repo"].list_sessions.return_value = [model1, model2]
    # First lock fails (None), second succeeds
    mock_repos["lock_repo"].acquire_lock.side_effect = [None, "token-456"]
    
    # Act
    session, token = await session_service.get_session({"provider": "test_provider"})
    
    # Assert
    assert session.id == "2"
    assert token == "token-456"
    assert mock_repos["lock_repo"].acquire_lock.call_count == 2


@pytest.mark.asyncio
async def test_get_session_exhausted(session_service, mock_repos):
    # Arrange
    model1 = create_mock_session_model(id="1", usage_count=1)
    
    mock_repos["storage_repo"].list_sessions.return_value = [model1]
    mock_repos["lock_repo"].acquire_lock.return_value = None # Lock fails
    
    # Act & Assert
    with pytest.raises(SessionExhaustedError, match="No usable sessions available for metadata: {'provider': 'test_provider'}"):
        await session_service.get_session({"provider": "test_provider"})


@pytest.mark.asyncio
async def test_release_session(session_service, mock_repos):
    # Arrange
    model = create_mock_session_model(id="1")
    session = Session.from_model(model)
    token = "token-123"
    
    # Act
    await session_service.release_session(session, token)
    
    # Assert
    mock_repos["storage_repo"].update_session.assert_called_once_with("1", model)
    mock_repos["lock_repo"].release_lock.assert_called_once_with("session:1", "token-123")


@pytest.mark.asyncio
@patch("koda.modules.session.service.shutil.rmtree")
@patch("koda.modules.session.service.os.path.exists", return_value=True)
@patch("koda.modules.session.service.os.makedirs")
@patch("koda.modules.session.service.launch_browser")
async def test_browser_session_scope_success(
    mock_launch_browser, mock_makedirs, mock_exists, mock_rmtree, session_service, mock_repos
):
    # Arrange
    browser_param = BrowserParam(type="invisible_playwright", userDataDir="s3_key_123")
    model = create_mock_session_model(id="1", usage_count=0, error_score=1.0, browser=browser_param)
    session = Session.from_model(model)
    
    session_service.get_session = AsyncMock(return_value=(session, "token-123"))
    session_service.release_session = AsyncMock()
    
    mock_context = MagicMock()
    mock_launch_browser.return_value.__aenter__.return_value = mock_context
    mock_repos["s3_repo"].upload_profile.return_value = "new_s3_key_123"
    
    # Act
    async with session_service.browser_session_scope({"provider": "test_provider"}) as (s, ctx):
        assert s.id == "1"
        assert ctx == mock_context
        
    # Assert
    assert session.usage_count == 1 # mark_good increments usage
    assert session.error_score == 0.5 # mark_good decrements error score
    assert session.model.browser.user_data_dir == "new_s3_key_123"
    
    mock_repos["s3_repo"].download_profile.assert_called_once_with("s3_key_123", "/tmp/koda_profiles/1")
    mock_launch_browser.assert_called_once_with("invisible_playwright", "/tmp/koda_profiles/1", {})
    mock_repos["s3_repo"].upload_profile.assert_called_once_with("/tmp/koda_profiles/1", "1")
    mock_rmtree.assert_called_once_with("/tmp/koda_profiles/1", ignore_errors=True)
    session_service.release_session.assert_called_once_with(session, "token-123")


@pytest.mark.asyncio
@patch("koda.modules.session.service.shutil.rmtree")
@patch("koda.modules.session.service.os.path.exists", return_value=True)
@patch("koda.modules.session.service.os.makedirs")
@patch("koda.modules.session.service.launch_browser")
async def test_browser_session_scope_exception(
    mock_launch_browser, mock_makedirs, mock_exists, mock_rmtree, session_service, mock_repos
):
    # Arrange
    browser_param = BrowserParam(type="invisible_playwright", user_data_dir=None)
    model = create_mock_session_model(id="1", usage_count=0, error_score=0.0, browser=browser_param)
    session = Session.from_model(model)
    
    session_service.get_session = AsyncMock(return_value=(session, "token-123"))
    session_service.release_session = AsyncMock()
    
    mock_context = MagicMock()
    mock_launch_browser.return_value.__aenter__.return_value = mock_context
    mock_repos["s3_repo"].upload_profile.return_value = "new_s3_key_123"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Test error"):
        async with session_service.browser_session_scope({"provider": "test_provider"}) as (s, ctx):
            raise ValueError("Test error")
            
    # Assert
    assert session.usage_count == 1 # mark_bad increments usage
    assert session.error_score == 1.0 # mark_bad increments error score
    assert session.model.browser.user_data_dir == "new_s3_key_123"
    
    mock_makedirs.assert_called_once_with("/tmp/koda_profiles/1", exist_ok=True)
    mock_launch_browser.assert_called_once_with("invisible_playwright", "/tmp/koda_profiles/1", {})
    mock_repos["s3_repo"].upload_profile.assert_called_once_with("/tmp/koda_profiles/1", "1")
    mock_rmtree.assert_called_once_with("/tmp/koda_profiles/1", ignore_errors=True)
    session_service.release_session.assert_called_once_with(session, "token-123")


@pytest.mark.asyncio
async def test_resolve_mfa_no_mfa(session_service):
    # Arrange
    model = create_mock_session_model(id="1")
    session = Session.from_model(model)
    
    # Act
    result = await session_service.resolve_mfa(session)
    
    # Assert
    assert result == ""


@pytest.mark.asyncio
@patch("koda.modules.session.service.pyotp.TOTP")
async def test_resolve_mfa_totp(mock_totp, session_service):
    # Arrange
    mock_totp_instance = MagicMock()
    mock_totp_instance.now.return_value = "123456"
    mock_totp.return_value = mock_totp_instance
    
    mfa = MFAParam(strategy="totp", config={"secret": "base32secret"})
    model = create_mock_session_model(id="1", mfa=mfa)
    session = Session.from_model(model)
    
    # Act
    result = await session_service.resolve_mfa(session)
    
    # Assert
    assert result == "123456"
    mock_totp.assert_called_once_with("base32secret")


@pytest.mark.asyncio
async def test_resolve_mfa_imap(session_service, mock_repos):
    # Arrange
    mock_repos["email_repo_imap"].get_latest_email.return_value = "Your code is 654321."
    
    mfa = MFAParam(strategy="imap", config={"address": "test@example.com"})
    model = create_mock_session_model(id="1", mfa=mfa)
    session = Session.from_model(model)
    
    # Act
    result = await session_service.resolve_mfa(session)
    
    # Assert
    assert result == "654321"
    mock_repos["email_repo_imap"].get_latest_email.assert_called_once_with("test@example.com")


@pytest.mark.asyncio
async def test_resolve_mfa_jmap_custom_pattern(session_service, mock_repos):
    # Arrange
    mock_repos["email_repo_jmap"].get_latest_email.return_value = "Code: 9876"
    
    mfa = MFAParam(strategy="jmap", config={"address": "test@example.com", "pattern": r"\b\d{4}\b"})
    model = create_mock_session_model(id="1", mfa=mfa)
    session = Session.from_model(model)
    
    # Act
    result = await session_service.resolve_mfa(session)
    
    # Assert
    assert result == "9876"
    mock_repos["email_repo_jmap"].get_latest_email.assert_called_once_with("test@example.com")


@pytest.mark.asyncio
async def test_resolve_mfa_unknown_strategy(session_service):
    # Arrange
    mfa = MFAParam(strategy="unknown", config={})
    model = create_mock_session_model(id="1", mfa=mfa)
    session = Session.from_model(model)
    
    # Act & Assert
    with pytest.raises(KodaError, match="Unknown MFA strategy: unknown"):
        await session_service.resolve_mfa(session)
