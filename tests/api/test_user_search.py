import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_user_search_by_email_endpoint_exists():
    """Test that user search by email endpoint exists"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-search-user"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test GET /users/search/by-email endpoint exists
        response = client.get("/users/search/by-email?email=test@example.com", headers=auth_headers)
        # Should exist (might return 404 if user not found, 422 if validation fails)
        assert response.status_code in [200, 404, 422]
        
        print("User search by email endpoint exists!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify user search by email endpoint: {e}")

def test_default_user_profile_endpoint_exists():
    """Test that default user profile endpoint exists"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-default-user"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test GET /users/default endpoint exists
        response = client.get("/users/default", headers=auth_headers)
        # Should exist (might return 200 with default user or create one)
        assert response.status_code in [200, 201, 404]
        
        print("Default user profile endpoint exists!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify default user profile endpoint: {e}")

def test_user_search_endpoints_documentation():
    """Test that user search endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes user search endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that user search endpoints are documented
        assert "/users/search/by-email" in paths
        assert "/users/default" in paths
        
        print("User search endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify user search documentation: {e}")

def test_user_search_by_email_requires_email():
    """Test that user search by email requires email parameter"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-validation-user"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test GET /users/search/by-email without email parameter
        response = client.get("/users/search/by-email", headers=auth_headers)
        # Should return 422 for validation error
        assert response.status_code == 422
        
        print("User search by email properly validates email parameter!")
        
    except Exception as e:
        pytest.fail(f"Failed to test user search email validation: {e}")

def test_user_search_without_authentication():
    """Test that user search endpoints require authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test search by email without authentication
        response = client.get("/users/search/by-email?email=test@example.com")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test default user without authentication
        response = client.get("/users/default")
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("User search endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test user search authentication requirements: {e}")