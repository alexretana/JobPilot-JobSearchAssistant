import pytest
import bcrypt
import jwt
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from backend.api.auth import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    validate_token,
    get_user_by_email
)
from backend.api.config import settings


def test_password_hashing():
    """Test that passwords can be hashed and verified using bcrypt"""
    password = "test-password-123"
    
    # Test hashing a password
    hashed_password = get_password_hash(password)
    
    # Verify that the password was hashed
    assert isinstance(hashed_password, str)
    assert len(hashed_password) > 0
    assert hashed_password != password
    
    # Test verifying the password
    assert verify_password(password, hashed_password)
    assert not verify_password("wrong-password", hashed_password)


def test_jwt_token_creation():
    """Test that JWT tokens can be created using PyJWT"""
    # Test creating a token with a user ID
    data = {"sub": "test-user-id"}
    token = create_access_token(data)
    
    # Verify that a token was created
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Verify that the token can be decoded
    decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    assert decoded_payload["sub"] == "test-user-id"


def test_jwt_token_with_expiration():
    """Test that JWT tokens have proper expiration using PyJWT"""
    # Test creating a token with expiration
    data = {"sub": "test-user-id"}
    expires_delta = timedelta(minutes=30)
    token = create_access_token(data, expires_delta)
    
    # Verify that the token was created
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Verify that the token has an expiration claim
    decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    assert "exp" in decoded_payload
    assert decoded_payload["sub"] == "test-user-id"
    
    # Verify that expiration is in the future
    expiration = decoded_payload["exp"]
    now = datetime.utcnow().timestamp()
    assert expiration > now


def test_token_validation():
    """Test that tokens can be validated"""
    # Create a token
    data = {"sub": "test-user-id"}
    token = create_access_token(data)
    
    # Validate the token
    user_id = validate_token(token)
    assert user_id == "test-user-id"


def test_expired_token():
    """Test that expired tokens are rejected"""
    # Create a token that expires immediately
    data = {"sub": "test-user-id"}
    expires_delta = timedelta(seconds=-1)  # Expired 1 second ago
    token = create_access_token(data, expires_delta)
    
    # Try to validate the expired token - should raise HTTPException
    with pytest.raises(Exception):
        validate_token(token)


@patch('backend.data.database.get_user_repository')
def test_get_user_by_email(mock_get_user_repo):
    """Test that get_user_by_email calls the user repository correctly"""
    # Mock the user repository and its method
    mock_user_repo = MagicMock()
    mock_get_user_repo.return_value = mock_user_repo
    mock_user_repo.get_user_by_email.return_value = {"id": "123", "email": "test@example.com"}
    
    # Call the function
    user = get_user_by_email("test@example.com")
    
    # Verify the repository method was called correctly
    mock_get_user_repo.assert_called_once()
    mock_user_repo.get_user_by_email.assert_called_once_with("test@example.com")
    assert user == {"id": "123", "email": "test@example.com"}