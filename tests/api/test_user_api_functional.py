import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_user_api_with_authentication():
    """Test user API endpoints with authentication"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-api-user"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test GET /users/ (list users) with authentication
        response = client.get("/users/", headers=auth_headers)
        assert response.status_code == 200
        assert "user_id" in response.json()
        
        # Test GET /users/{user_id} (get specific user) with authentication
        user_id = str(uuid.uuid4())
        response = client.get(f"/users/{user_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "user_id" in response.json()
        
        # Test POST /users/ (create user) with authentication
        response = client.post("/users/", headers=auth_headers)
        assert response.status_code == 200
        assert "user_id" in response.json()
        
        # Test PUT /users/{user_id} (update user) with authentication
        response = client.put(f"/users/{user_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "user_id" in response.json()
        
        # Test DELETE /users/{user_id} (delete user) with authentication
        response = client.delete(f"/users/{user_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "user_id" in response.json()
        
        print("All user API endpoints work with authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test user API with authentication: {e}")

def test_user_api_without_authentication():
    """Test that user API endpoints now require authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test GET /users/ (list users) without authentication
        response = client.get("/users/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /users/{user_id} (get specific user) without authentication
        user_id = str(uuid.uuid4())
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test POST /users/ (create user) without authentication
        response = client.post("/users/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test PUT /users/{user_id} (update user) without authentication
        response = client.put(f"/users/{user_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test DELETE /users/{user_id} (delete user) without authentication
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("All user API endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test user API authentication requirements: {e}")

def test_user_api_request_response_models():
    """Test user API request and response models"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        from backend.data.models import JobType, RemoteType
        import json
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-models"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test creating a user with proper data structure
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "current_title": "API Test Engineer",
            "preferred_job_types": [JobType.FULL_TIME.value],
            "preferred_remote_types": [RemoteType.REMOTE.value],
        }
        
        # Test POST /users/ with user data
        response = client.post("/users/", json=user_data, headers=auth_headers)
        assert response.status_code == 200
        
        # Test that response contains expected fields
        response_data = response.json()
        assert "message" in response_data
        assert "user_id" in response_data
        
        print("User API request/response models work correctly!")
        
    except Exception as e:
        pytest.fail(f"Failed to test user API request/response models: {e}")

def test_user_api_end_to_end_flow():
    """Test complete user API end-to-end flow"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        from backend.data.models import JobType, RemoteType
        import json
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-end-to-end"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Create a user
        user_data = {
            "first_name": "End-to-End",
            "last_name": "Tester",
            "email": "e2e.tester@example.com",
            "current_title": "End-to-End Test Engineer",
            "preferred_job_types": [JobType.FULL_TIME.value],
            "preferred_remote_types": [RemoteType.HYBRID.value],
        }
        
        create_response = client.post("/users/", json=user_data, headers=auth_headers)
        assert create_response.status_code == 200
        print("[PASS] User creation successful")
        
        # 2. List users
        list_response = client.get("/users/", headers=auth_headers)
        assert list_response.status_code == 200
        print("[PASS] User listing successful")
        
        # 3. Get specific user (using a known user ID)
        # For this test, we'll just verify the endpoint exists and works
        user_id = str(uuid.uuid4())
        get_response = client.get(f"/users/{user_id}", headers=auth_headers)
        assert get_response.status_code == 200
        print("[PASS] Get specific user successful")
        
        # 4. Update user
        update_data = {
            "first_name": "Updated End-to-End",
            "last_name": "Tester",
            "current_title": "Updated End-to-End Test Engineer",
        }
        
        update_response = client.put(f"/users/{user_id}", json=update_data, headers=auth_headers)
        assert update_response.status_code == 200
        print("[PASS] User update successful")
        
        # 5. Delete user
        delete_response = client.delete(f"/users/{user_id}", headers=auth_headers)
        assert delete_response.status_code == 200
        print("[PASS] User deletion successful")
        
        print("Complete user API end-to-end flow test passed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test user API end-to-end flow: {e}")