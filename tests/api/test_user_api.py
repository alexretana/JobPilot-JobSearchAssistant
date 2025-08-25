import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_user_api_endpoints_exist():
    """Test that user API endpoints exist"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the user endpoints exist
        # GET /users/ (list users)
        response = client.get("/users/")
        assert response.status_code in [200, 403, 401]  # Should exist (403/401 if auth required)
        
        # GET /users/{user_id} (get specific user)
        response = client.get(f"/users/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist (404 if user not found)
        
        # POST /users/ (create user)
        response = client.post("/users/")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # PUT /users/{user_id} (update user)
        response = client.put(f"/users/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # DELETE /users/{user_id} (delete user)
        response = client.delete(f"/users/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        print("All user API endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify user API endpoints: {e}")

def test_user_api_documentation():
    """Test that user API endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes user endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that user endpoints are documented
        assert "/users/" in paths
        assert "/users/{user_id}" in paths
        
        # Check that the methods are documented
        users_path = paths["/users/"]
        user_id_path = paths["/users/{user_id}"]
        
        assert "get" in users_path
        assert "post" in users_path
        assert "get" in user_id_path
        assert "put" in user_id_path
        assert "delete" in user_id_path
        
        print("User API endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify user API documentation: {e}")

def test_user_models_integration():
    """Test that user models work with the API"""
    try:
        from backend.data.models import UserProfile, JobType, RemoteType
        import uuid
        
        # Test creating a user profile model
        user_id = str(uuid.uuid4())
        user_data = {
            "id": user_id,
            "first_name": "API",
            "last_name": "Tester",
            "email": "api.tester@example.com",
            "current_title": "API Test Engineer",
            "preferred_job_types": [JobType.FULL_TIME],
            "preferred_remote_types": [RemoteType.REMOTE],
        }
        
        user = UserProfile(**user_data)
        assert str(user.id) == user_id
        assert user.first_name == "API"
        assert user.last_name == "Tester"
        assert user.email == "api.tester@example.com"
        
        print("User models integrate correctly with the API!")
        
    except Exception as e:
        pytest.fail(f"Failed to test user models integration: {e}")