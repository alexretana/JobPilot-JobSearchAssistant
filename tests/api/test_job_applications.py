import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid
from datetime import datetime

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_job_application_models():
    """Test that job application models work correctly"""
    try:
        from backend.api.models.applications.models import (
            JobApplicationCreate,
            JobApplicationUpdate,
            JobApplicationResponse,
            JobApplicationListResponse
        )
        from backend.data.models import ApplicationStatus
        
        # Test creating a JobApplicationCreate model
        job_id = uuid.uuid4()
        user_id = uuid.uuid4()
        
        create_data = {
            "job_id": job_id,
            "user_profile_id": user_id,
            "resume_version": "v1.2",
            "cover_letter": "Dear Hiring Manager...",
            "notes": "Applied through company website"
        }
        
        app_create = JobApplicationCreate(**create_data)
        assert app_create.job_id == job_id
        assert app_create.user_profile_id == user_id
        assert app_create.resume_version == "v1.2"
        assert app_create.cover_letter == "Dear Hiring Manager..."
        assert app_create.notes == "Applied through company website"
        
        # Test creating a JobApplicationUpdate model
        update_data = {
            "status": ApplicationStatus.INTERVIEWING,
            "response_date": datetime(2023, 1, 15),
            "notes": "Got a response from employer",
            "follow_up_date": datetime(2023, 1, 20)
        }
        
        app_update = JobApplicationUpdate(**update_data)
        assert app_update.status == ApplicationStatus.INTERVIEWING
        assert app_update.response_date == datetime(2023, 1, 15)
        assert app_update.notes == "Got a response from employer"
        assert app_update.follow_up_date == datetime(2023, 1, 20)
        
        # Test creating a JobApplicationResponse model
        app_id = uuid.uuid4()
        created_at = datetime(2023, 1, 10)
        updated_at = datetime(2023, 1, 12)
        
        response_data = {
            "id": app_id,
            "job_id": job_id,
            "user_profile_id": user_id,
            "status": ApplicationStatus.APPLIED,
            "applied_date": datetime(2023, 1, 10),
            "response_date": None,
            "resume_version": "v1.2",
            "cover_letter": "Dear Hiring Manager...",
            "notes": "Applied through company website",
            "follow_up_date": None,
            "interview_scheduled": None,
            "created_at": created_at,
            "updated_at": updated_at
        }
        
        app_response = JobApplicationResponse(**response_data)
        assert app_response.id == app_id
        assert app_response.job_id == job_id
        assert app_response.user_profile_id == user_id
        assert app_response.status == ApplicationStatus.APPLIED
        assert app_response.applied_date == datetime(2023, 1, 10)
        assert app_response.created_at == created_at
        assert app_response.updated_at == updated_at
        
        print("All job application models work correctly!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job application models: {e}")

def test_job_application_api_integration():
    """Test job application API integration with authentication"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        user_id = "test-user-123"
        token = create_access_token(data={"sub": user_id})
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
        app_id = str(uuid.uuid4())
        response = client.get(f"/applications/{app_id}", headers=auth_headers)
        assert response.status_code == 404  # Not found since it doesn't exist
        
        # Test POST /applications/ (create application) with authentication
        response = client.post("/applications/", headers=auth_headers)
        assert response.status_code == 422  # Validation error since no data provided
        
        # Test PUT /applications/{application_id} (update application) with authentication
        response = client.put(f"/applications/{app_id}", headers=auth_headers)
        assert response.status_code == 422  # Validation error since no data provided
        
        # Test DELETE /applications/{application_id} (delete application) with authentication
        response = client.delete(f"/applications/{app_id}", headers=auth_headers)
        assert response.status_code == 404  # Not found since it doesn't exist
        
        print("Job application API integration works correctly!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job application API integration: {e}")

def test_job_application_api_documentation():
    """Test that job application API endpoints are properly documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes job application endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that job application endpoints are documented
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
        
        print("Job application API endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job application API documentation: {e}")

def test_job_application_api_without_authentication():
    """Test that job application API endpoints require authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test GET /applications/ (list applications) without authentication
        response = client.get("/applications/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /applications/{application_id} (get specific application) without authentication
        app_id = str(uuid.uuid4())
        response = client.get(f"/applications/{app_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test POST /applications/ (create application) without authentication
        response = client.post("/applications/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test PUT /applications/{application_id} (update application) without authentication
        response = client.put(f"/applications/{app_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test DELETE /applications/{application_id} (delete application) without authentication
        response = client.delete(f"/applications/{app_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("All job application API endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job application API authentication requirements: {e}")