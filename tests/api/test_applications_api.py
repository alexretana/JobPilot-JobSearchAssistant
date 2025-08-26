import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid
from datetime import datetime

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_applications_api_endpoints_exist():
    """Test that applications API endpoints exist"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the applications endpoints exist
        # GET /applications/ (list applications)
        response = client.get("/applications/")
        assert response.status_code in [200, 403, 401]  # Should exist (403/401 if auth required)
        
        # GET /applications/{application_id} (get specific application)
        response = client.get(f"/applications/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist (404 if application not found)
        
        # POST /applications/ (create application)
        response = client.post("/applications/")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # PUT /applications/{application_id} (update application)
        response = client.put(f"/applications/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # DELETE /applications/{application_id} (delete application)
        response = client.delete(f"/applications/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        print("All applications API endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify applications API endpoints: {e}")

def test_applications_api_documentation():
    """Test that applications API endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes applications endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that applications endpoints are documented
        assert "/applications/" in paths
        assert "/applications/{application_id}" in paths
        
        # Check that the methods are documented
        applications_path = paths["/applications/"]
        application_id_path = paths["/applications/{application_id}"]
        
        assert "get" in applications_path
        assert "post" in applications_path
        assert "get" in application_id_path
        assert "put" in application_id_path
        assert "delete" in application_id_path
        
        print("Applications API endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify applications API documentation: {e}")

def test_applications_api_with_authentication():
    """Test applications API endpoints with authentication"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-applications-api"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test GET /applications/ (list applications) with authentication
        response = client.get("/applications/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "applications" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        
        # Test GET /applications/{application_id} (get specific application) with authentication
        application_id = str(uuid.uuid4())
        response = client.get(f"/applications/{application_id}", headers=auth_headers)
        assert response.status_code == 404  # Not found since it doesn't exist
        
        # Test POST /applications/ (create application) with authentication
        response = client.post("/applications/", headers=auth_headers)
        assert response.status_code == 422  # Validation error since no data provided
        
        # Test PUT /applications/{application_id} (update application) with authentication
        response = client.put(f"/applications/{application_id}", headers=auth_headers)
        assert response.status_code == 422  # Validation error since no data provided
        
        # Test DELETE /applications/{application_id} (delete application) with authentication
        response = client.delete(f"/applications/{application_id}", headers=auth_headers)
        assert response.status_code == 404  # Not found since it doesn't exist
        
        print("All applications API endpoints work with authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test applications API with authentication: {e}")

def test_applications_api_without_authentication():
    """Test that applications API endpoints require authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test GET /applications/ (list applications) without authentication
        response = client.get("/applications/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /applications/{application_id} (get specific application) without authentication
        application_id = str(uuid.uuid4())
        response = client.get(f"/applications/{application_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test POST /applications/ (create application) without authentication
        response = client.post("/applications/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test PUT /applications/{application_id} (update application) without authentication
        response = client.put(f"/applications/{application_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test DELETE /applications/{application_id} (delete application) without authentication
        response = client.delete(f"/applications/{application_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("All applications API endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test applications API authentication requirements: {e}")