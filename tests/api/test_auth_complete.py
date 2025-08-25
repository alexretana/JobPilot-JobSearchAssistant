import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_complete_auth_flow():
    """Test the complete authentication flow"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # 1. Test user registration
        register_response = client.post("/auth/register", json={
            "email": "newuser@example.com",
            "password": "new-password-123",
            "full_name": "New User"
        })
        assert register_response.status_code == 200
        assert "message" in register_response.json()
        
        # 2. Test user login
        login_response = client.post("/auth/login", json={
            "email": "newuser@example.com",
            "password": "new-password-123"
        })
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()
        assert "token_type" in login_response.json()
        assert login_response.json()["token_type"] == "bearer"
        
        # 3. Extract the access token
        access_token = login_response.json()["access_token"]
        
        # 4. Test logout
        logout_response = client.post("/auth/logout")
        assert logout_response.status_code == 200
        assert "message" in logout_response.json()
        
        print("Complete authentication flow test passed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test complete authentication flow: {e}")

def test_token_creation_and_validation():
    """Test token creation and validation independently"""
    try:
        from backend.api.auth import create_access_token, validate_token
        from datetime import timedelta
        
        # Test creating and validating a valid token
        data = {"sub": "test-user-456"}
        token = create_access_token(data)
        user_id = validate_token(token)
        assert user_id == "test-user-456"
        
        # Test creating and validating a token with custom expiration
        expires_delta = timedelta(minutes=15)
        token_with_exp = create_access_token(data, expires_delta)
        user_id_with_exp = validate_token(token_with_exp)
        assert user_id_with_exp == "test-user-456"
        
        print("Token creation and validation test passed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test token creation and validation: {e}")

def test_password_hashing_functions():
    """Test password hashing functions"""
    try:
        from backend.api.auth import get_password_hash, verify_password
        
        # Test hashing and verifying a password
        password = "secure-password-123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed)
        assert not verify_password("wrong-password", hashed)
        
        # Test with different passwords
        password2 = "another-password-456"
        hashed2 = get_password_hash(password2)
        assert verify_password(password2, hashed2)
        assert not verify_password(password, hashed2)
        
        print("Password hashing functions test passed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test password hashing functions: {e}")

def test_auth_endpoints_documentation():
    """Test that auth endpoints are properly documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes auth endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that auth endpoints are documented
        assert "/auth/login" in paths
        assert "/auth/register" in paths
        assert "/auth/logout" in paths
        assert "/auth/refresh" in paths
        
        print("Auth endpoints documentation test passed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test auth endpoints documentation: {e}")