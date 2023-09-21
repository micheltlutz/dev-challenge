import pytest
from pydantic import ValidationError
from app.user.user_schema import UserCreate

def test_valid_user_create():
    data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "test@example.com",
        "nickname": "testnick"
    }

    user = UserCreate(**data)
    for field, value in data.items():
        assert getattr(user, field) == value

def test_invalid_email_in_user_create():
    data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "invalidemail",  # This is an invalid email format
        "nickname": "testnick"
    }

    with pytest.raises(ValidationError):
        UserCreate(**data)

def test_missing_field_in_user_create():
    data = {
        "username": "testuser",
        "password": "testpassword",
        # Missing email field
        "nickname": "testnick"
    }

    with pytest.raises(ValidationError):
        UserCreate(**data)
