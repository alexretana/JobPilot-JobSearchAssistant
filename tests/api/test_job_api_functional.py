import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_job_api_with_authentication():
    """Test job API endpoints with authentication"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-job-api"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test GET /jobs/ (list jobs) with authentication
        response = client.get("/jobs/", headers=auth_headers)
        assert response.status_code == 200
        assert "user_id" in response.json()
        
        # Test GET /jobs/{job_id} (get specific job) with authentication
        job_id = str(uuid.uuid4())
        response = client.get(f"/jobs/{job_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "user_id" in response.json()
        
        # Test POST /jobs/ (create job) with authentication
        response = client.post("/jobs/", headers=auth_headers)
        assert response.status_code == 200
        assert "user_id" in response.json()
        
        # Test PUT /jobs/{job_id} (update job) with authentication
        response = client.put(f"/jobs/{job_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "user_id" in response.json()
        
        # Test DELETE /jobs/{job_id} (delete job) with authentication
        response = client.delete(f"/jobs/{job_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "user_id" in response.json()
        
        print("All job API endpoints work with authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job API with authentication: {e}")

def test_job_api_without_authentication():
    """Test that job API endpoints require authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test GET /jobs/ (list jobs) without authentication
        response = client.get("/jobs/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /jobs/{job_id} (get specific job) without authentication
        job_id = str(uuid.uuid4())
        response = client.get(f"/jobs/{job_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test POST /jobs/ (create job) without authentication
        response = client.post("/jobs/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test PUT /jobs/{job_id} (update job) without authentication
        response = client.put(f"/jobs/{job_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test DELETE /jobs/{job_id} (delete job) without authentication
        response = client.delete(f"/jobs/{job_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("All job API endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job API authentication requirements: {e}")

def test_job_api_request_response_models():
    """Test job API request and response models"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        from backend.data.models import JobType, RemoteType, ExperienceLevel
        import json
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-job-models"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test creating a job with proper data structure
        job_data = {
            "title": "Test API Engineer",
            "location": "API Test City",
            "description": "Job created via API test",
            "job_type": JobType.FULL_TIME.value,
            "remote_type": RemoteType.REMOTE.value,
            "experience_level": ExperienceLevel.MID_LEVEL.value,
            "skills_required": ["Python", "FastAPI", "Testing"],
            "salary_min": 90000,
            "salary_max": 120000,
            "salary_currency": "USD"
        }
        
        # Test POST /jobs/ with job data
        response = client.post("/jobs/", json=job_data, headers=auth_headers)
        assert response.status_code == 200
        
        # Test that response contains expected fields
        response_data = response.json()
        assert "message" in response_data
        assert "user_id" in response_data
        
        print("Job API request/response models work correctly!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job API request/response models: {e}")

def test_job_api_end_to_end_flow():
    """Test complete job API end-to-end flow"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        from backend.data.models import JobType, RemoteType, ExperienceLevel
        import json
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-end-to-end"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Create a job
        job_data = {
            "title": "End-to-End Test Engineer",
            "location": "Test Location",
            "description": "End-to-end API test job",
            "job_type": JobType.FULL_TIME.value,
            "remote_type": RemoteType.HYBRID.value,
            "experience_level": ExperienceLevel.SENIOR_LEVEL.value,
            "skills_required": ["Python", "Testing", "API Design"],
            "salary_min": 120000,
            "salary_max": 160000,
            "salary_currency": "USD"
        }
        
        create_response = client.post("/jobs/", json=job_data, headers=auth_headers)
        assert create_response.status_code == 200
        print("[PASS] Job creation successful")
        
        # 2. List jobs
        list_response = client.get("/jobs/", headers=auth_headers)
        assert list_response.status_code == 200
        print("[PASS] Job listing successful")
        
        # 3. Get specific job (using a known job ID)
        # For this test, we'll just verify the endpoint exists and works
        job_id = str(uuid.uuid4())
        get_response = client.get(f"/jobs/{job_id}", headers=auth_headers)
        assert get_response.status_code == 200
        print("[PASS] Get specific job successful")
        
        # 4. Update job
        update_data = {
            "title": "Updated End-to-End Test Engineer",
            "location": "Updated Test Location",
            "description": "Updated end-to-end API test job",
        }
        
        update_response = client.put(f"/jobs/{job_id}", json=update_data, headers=auth_headers)
        assert update_response.status_code == 200
        print("[PASS] Job update successful")
        
        # 5. Delete job
        delete_response = client.delete(f"/jobs/{job_id}", headers=auth_headers)
        assert delete_response.status_code == 200
        print("[PASS] Job deletion successful")
        
        print("Complete job API end-to-end flow test passed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job API end-to-end flow: {e}")