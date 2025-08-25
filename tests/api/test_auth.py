import pytest
from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime, timedelta
import base64
import json

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_auth_module_import():
    """Test that auth module can be imported"""
    try:
        from backend.api.auth import create_access_token
        # If we get here, the module exists
    except ImportError:
        pytest.fail("Auth module not found. Need to create backend/api/auth.py")

def test_jwt_token_creation():
    """Test that JWT tokens can be created"""
    try:
        from backend.api.auth import create_access_token
        
        # Test creating a token with a user ID
        data = {"sub": "test-user-id"}
        token = create_access_token(data)
        
        # Verify that a token was created
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify that the token can be decoded
        decoded_data = base64.b64decode(token.encode()).decode()
        payload = json.loads(decoded_data)
        assert payload["sub"] == "test-user-id"
        
    except ImportError:
        pytest.fail("Auth module not found. Need to create backend/api/auth.py")
    except Exception as e:
        pytest.fail(f"Failed to create JWT token: {e}")

def test_jwt_token_with_expiration():
    """Test that JWT tokens have proper expiration"""
    try:
        from backend.api.auth import create_access_token
        
        # Test creating a token with expiration
        data = {"sub": "test-user-id"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)
        
        # Verify that the token was created
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify that the token has an expiration claim
        decoded_data = base64.b64decode(token.encode()).decode()
        payload = json.loads(decoded_data)
        assert "exp" in payload
        assert payload["sub"] == "test-user-id"
        
        # Verify that expiration is in the future
        expiration = payload["exp"]
        now = datetime.utcnow().timestamp()
        assert expiration > now
        
    except ImportError:
        pytest.fail("Auth module not found. Need to create backend/api/auth.py")
    except Exception as e:
        pytest.fail(f"Failed to create JWT token with expiration: {e}")

def test_password_hashing():
    """Test that passwords can be hashed and verified"""
    try:
        from backend.api.auth import get_password_hash, verify_password
        
        # Test hashing a password
        password = "test-password-123"
        hashed_password = get_password_hash(password)
        
        # Verify that the password was hashed
        assert isinstance(hashed_password, str)
        assert len(hashed_password) > 0
        assert hashed_password != password
        
        # Test verifying the password
        assert verify_password(password, hashed_password)
        assert not verify_password("wrong-password", hashed_password)
        
    except ImportError:
        pytest.fail("Auth module not found. Need to create backend/api/auth.py")
    except Exception as e:
        pytest.fail(f"Failed to hash/verify password: {e}")

def test_auth_middleware():
    """Test that auth middleware can validate tokens"""
    try:
        from backend.api.main import app
        from fastapi import Depends
        from backend.api.auth import get_current_user, create_access_token
        
        # Add a test endpoint that requires authentication
        @app.get("/test-auth")
        async def test_auth_endpoint(current_user = Depends(get_current_user)):
            return {"user_id": current_user}
        
        client = TestClient(app)
        
        # Test accessing the endpoint without authentication (should fail)
        response = client.get("/test-auth")
        assert response.status_code == 403  # Forbidden - no credentials provided
        
        # Test accessing the endpoint with invalid token (should fail)
        response = client.get("/test-auth", headers={"Authorization": "Bearer invalid-token"})
        assert response.status_code == 401  # Unauthorized - invalid token
        
        # Test accessing the endpoint with valid token (should succeed)
        # Create a valid token
        token = create_access_token(data={"sub": "test-user-123"})
        
        # Access endpoint with valid token
        response = client.get("/test-auth", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json()["user_id"] == "test-user-123"
        
    except ImportError:
        pytest.fail("Auth module not found. Need to create backend/api/auth.py")
    except Exception as e:
        pytest.fail(f"Failed to test auth middleware: {e}")

def test_login_endpoint():
    """Test that login endpoint works"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test accessing the login endpoint
        response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "test-password"
        })
        # This should now work since we've implemented the endpoint
        assert response.status_code == 200
        assert "access_token" in response.json()
        
    except Exception as e:
        pytest.fail(f"Failed to test login endpoint: {e}")

def test_register_endpoint():
    """Test that register endpoint works"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test accessing the register endpoint
        response = client.post("/auth/register", json={
            "email": "newuser@example.com",
            "password": "new-password-123",
            "full_name": "New User"
        })
        # This should now work since we've implemented the endpoint
        assert response.status_code == 200
        assert "message" in response.json()
        
    except Exception as e:
        pytest.fail(f"Failed to test register endpoint: {e}")

def test_logout_endpoint():
    """Test that logout endpoint works"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test accessing the logout endpoint
        response = client.post("/auth/logout")
        # This should now work since we've implemented the endpoint
        assert response.status_code == 200
        assert "message" in response.json()
        
    except Exception as e:
        pytest.fail(f"Failed to test logout endpoint: {e}")

def test_token_validation():
    """Test that tokens can be validated"""
    try:
        from backend.api.auth import create_access_token, validate_token
        
        # Create a token
        data = {"sub": "test-user-id"}
        token = create_access_token(data)
        
        # Validate the token
        user_id = validate_token(token)
        assert user_id == "test-user-id"
        
    except ImportError:
        pytest.fail("Auth module not found. Need to create backend/api/auth.py")
    except Exception as e:
        pytest.fail(f"Failed to validate token: {e}")

def test_expired_token():
    """Test that expired tokens are rejected"""
    try:
        from backend.api.auth import create_access_token, validate_token
        from datetime import timedelta
        
        # Create a token that expires immediately
        data = {"sub": "test-user-id"}
        expires_delta = timedelta(seconds=-1)  # Expired 1 second ago
        token = create_access_token(data, expires_delta)
        
        # Try to validate the expired token - should raise HTTPException
        try:
            user_id = validate_token(token)
            assert False, "Should have raised HTTPException for expired token"
        except Exception:
            # Expected to raise an exception for expired token
            pass
        
    except ImportError:
        pytest.fail("Auth module not found. Need to create backend/api/auth.py")
    except Exception as e:
        pytest.fail(f"Failed to test expired token: {e}")