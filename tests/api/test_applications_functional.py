import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid
from datetime import datetime

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_job_application_api_functional():
    """Test the functional implementation of the job application API"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        from backend.api.models.applications.models import (
            JobApplicationCreate,
            JobApplicationUpdate,
            JobApplicationResponse,
            JobApplicationListResponse
        )
        from backend.data.models import ApplicationStatus
        
        client = TestClient(app)
        
        # Create a valid token for testing
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test POST /applications/ (create application) with proper data
        job_id = str(uuid.uuid4())
        create_data = {
            "job_id": job_id,
            "user_profile_id": user_id,
            "resume_version": "v1.2",
            "cover_letter": "Dear Hiring Manager...",
            "notes": "Applied through company website"
        }
        
        response = client.post("/applications/", json=create_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # Verify the response structure
        assert "id" in data
        assert data["job_id"] == job_id
        assert data["user_profile_id"] == user_id
        assert data["status"] == "applied"  # When applying to a job, status is "applied"
        assert data["resume_version"] == "v1.2"
        assert data["cover_letter"] == "Dear Hiring Manager..."
        
        application_id = data["id"]
        
        # Test GET /applications/{application_id} (get specific application)
        response = client.get(f"/applications/{application_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # Verify the response structure
        assert data["id"] == application_id
        assert data["job_id"] == job_id
        assert data["user_profile_id"] == user_id
        assert data["status"] == "applied"  # Status should be "applied" after creation
        assert data["resume_version"] == "v1.2"
        assert data["cover_letter"] == "Dear Hiring Manager..."
        
        # Test PUT /applications/{application_id} (update application)
        update_data = {
            "notes": "Got a response from employer"
        }
        
        response = client.put(f"/applications/{application_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # Verify the response structure
        assert data["id"] == application_id
        assert data["job_id"] == job_id
        assert data["user_profile_id"] == user_id
        assert data["status"] == "applied"  # Status should remain "applied"
        assert data["resume_version"] == "v1.2"  # Should remain unchanged
        assert data["cover_letter"] == "Dear Hiring Manager..."  # Should remain unchanged
        assert data["notes"] == "Got a response from employer"
        
        # Test GET /applications/ (list applications)
        response = client.get("/applications/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        # Verify the response structure
        assert "applications" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert len(data["applications"]) >= 1
        assert data["total"] >= 1
        
        # Find our application in the list
        app_found = False
        for app in data["applications"]:
            if app["id"] == application_id:
                app_found = True
                assert app["job_id"] == job_id
                assert app["user_profile_id"] == user_id
                assert app["status"] == "applied"
                break
        assert app_found, "Created application not found in list"
        
        # Test DELETE /applications/{application_id} (delete application)
        response = client.delete(f"/applications/{application_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "successfully" in data["message"]
        
        # Verify the application is deleted
        response = client.get(f"/applications/{application_id}", headers=auth_headers)
        assert response.status_code == 404
        
        print("Job application API functional tests passed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job application API functionality: {e}")

def test_job_application_api_unauthorized_access():
    """Test that users cannot access applications belonging to other users"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create tokens for two different users
        user1_id = str(uuid.uuid4())
        user2_id = str(uuid.uuid4())
        
        token1 = create_access_token(data={"sub": user1_id})
        token2 = create_access_token(data={"sub": user2_id})
        
        auth_headers1 = {"Authorization": f"Bearer {token1}"}
        auth_headers2 = {"Authorization": f"Bearer {token2}"}
        
        # User 1 creates an application
        job_id = str(uuid.uuid4())
        create_data = {
            "job_id": job_id,
            "user_profile_id": user1_id,
            "resume_version": "v1.2",
            "cover_letter": "Dear Hiring Manager...",
            "notes": "Applied through company website"
        }
        
        response = client.post("/applications/", json=create_data, headers=auth_headers1)
        assert response.status_code == 200
        application_id = response.json()["id"]
        
        # User 2 tries to access User 1's application (should fail)
        response = client.get(f"/applications/{application_id}", headers=auth_headers2)
        assert response.status_code == 403
        
        # User 2 tries to update User 1's application (should fail)
        update_data = {"status": "applied"}
        response = client.put(f"/applications/{application_id}", json=update_data, headers=auth_headers2)
        assert response.status_code == 403
        
        # User 2 tries to delete User 1's application (should fail)
        response = client.delete(f"/applications/{application_id}", headers=auth_headers2)
        assert response.status_code == 403
        
        # User 1 can still access their own application
        response = client.get(f"/applications/{application_id}", headers=auth_headers1)
        assert response.status_code == 200
        
        # Clean up: User 1 deletes their application
        response = client.delete(f"/applications/{application_id}", headers=auth_headers1)
        assert response.status_code == 200
        
        print("Job application API unauthorized access tests passed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job application API unauthorized access: {e}")

def test_job_application_api_invalid_data():
    """Test that the API handles invalid data correctly"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test creating application with invalid user ID (should fail)
        job_id = str(uuid.uuid4())
        create_data = {
            "job_id": job_id,
            "user_profile_id": str(uuid.uuid4()),  # Different user ID
            "resume_version": "v1.2",
            "cover_letter": "Dear Hiring Manager...",
            "notes": "Applied through company website"
        }
        
        response = client.post("/applications/", json=create_data, headers=auth_headers)
        assert response.status_code == 403  # Forbidden
        
        # Test creating application with missing required fields (should fail)
        invalid_data = {
            "resume_version": "v1.2"
        }
        
        response = client.post("/applications/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422  # Unprocessable Entity
        
        print("Job application API invalid data tests passed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job application API invalid data handling: {e}")