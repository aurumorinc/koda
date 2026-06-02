import pytest
from datetime import datetime, timedelta, timezone
from koda.modules.session.schema import SessionModel, Session, UserDataParam, MFAParam

def test_session_model_validation():
    """Test that SessionModel correctly validates and handles aliases."""
    data = {
        "id": "test-session",
        "maxAge": 3000,  # 50 minutes in seconds
        "userData": {
            "username": "user",
            "password": "pass",
            "mfa": {
                "strategy": "totp",
                "config": {"secret": "base32secret"}
            }
        },
        "maxErrorScore": 5.0,
        "errorScoreDecrement": 1.0,
        "createdAt": "2024-01-01T00:00:00Z",
        "usageCount": 10,
        "maxUsageCount": 100,
        "errorScore": 2.5,
        "blockedStatusCodes": [401, 403],
        "metadata": {"provider": "windmill", "key": "value"}
    }
    
    model = SessionModel.model_validate(data)
    
    assert model.id == "test-session"
    assert model.max_age == timedelta(seconds=3000)
    assert model.user_data.username == "user"
    assert model.user_data.mfa.strategy == "totp"
    assert model.error_score == 2.5
    assert model.metadata.get("provider") == "windmill"

def test_session_wrapper_methods():
    """Test the methods and properties of the Session wrapper."""
    model = SessionModel(
        id="test",
        user_data=UserDataParam(username="u", password="p"),
        metadata={"provider": "test"},
        max_error_score=3.0,
        error_score_decrement=0.5,
        max_usage_count=5,
        created_at=datetime.now(timezone.utc) - timedelta(minutes=10),
        max_age=timedelta(minutes=20)
    )
    
    session = Session(model=model)
    
    assert session.id == "test"
    assert session.is_usable is True
    assert not session.is_blocked
    assert not session.is_expired
    
    # Test mark_good
    session.mark_good()
    assert session.usage_count == 1
    assert session.error_score == 0.0
    
    # Test mark_bad
    session.mark_bad()
    assert session.usage_count == 2
    assert session.error_score == 1.0
    
    # Test retire
    session.retire()
    assert session.is_blocked is True
    assert session.is_usable is False

def test_session_expiration():
    """Test session expiration logic."""
    model = SessionModel(
        id="test",
        user_data=UserDataParam(username="u", password="p"),
        metadata={"provider": "test"},
        created_at=datetime.now(timezone.utc) - timedelta(minutes=30),
        max_age=timedelta(minutes=20)
    )
    session = Session(model=model)
    assert session.is_expired is True
    assert session.is_usable is False

def test_session_max_usage():
    """Test session max usage logic."""
    model = SessionModel(
        id="test",
        user_data=UserDataParam(username="u", password="p"),
        metadata={"provider": "test"},
        usage_count=5,
        max_usage_count=5
    )
    session = Session(model=model)
    assert session.is_max_usage_count_reached is True
    assert session.is_usable is False

def test_get_state():
    """Test get_state method."""
    model = SessionModel(
        id="test",
        user_data=UserDataParam(username="u", password="p"),
        metadata={"provider": "test"}
    )
    session = Session(model=model)
    
    state_dict = session.get_state(as_dict=True)
    assert isinstance(state_dict, dict)
    assert state_dict["id"] == "test"
    assert "userData" in state_dict  # Check alias
    
    state_model = session.get_state(as_dict=False)
    assert isinstance(state_model, SessionModel)
    assert state_model.id == "test"
