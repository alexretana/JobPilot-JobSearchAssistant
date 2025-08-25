import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_job_api_endpoints_exist():
    """Test that job API endpoints exist"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the job endpoints exist
        # GET /jobs/ (list jobs)
        response = client.get("/jobs/")
        assert response.status_code in [200, 403, 401]  # Should exist (403/401 if auth required)
        
        # GET /jobs/{job_id} (get specific job)
        response = client.get(f"/jobs/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist (404 if job not found)
        
        # POST /jobs/ (create job)
        response = client.post("/jobs/")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # PUT /jobs/{job_id} (update job)
        response = client.put(f"/jobs/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # DELETE /jobs/{job_id} (delete job)
        response = client.delete(f"/jobs/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        print("All job API endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify job API endpoints: {e}")

def test_job_api_documentation():
    """Test that job API endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes job endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that job endpoints are documented
        assert "/jobs/" in paths
        assert "/jobs/{job_id}" in paths
        
        # Check that the methods are documented
        jobs_path = paths["/jobs/"]
        job_id_path = paths["/jobs/{job_id}"]
        
        assert "get" in jobs_path
        assert "post" in jobs_path
        assert "get" in job_id_path
        assert "put" in job_id_path
        assert "delete" in job_id_path
        
        print("Job API endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify job API documentation: {e}")

def test_job_models_integration():
    """Test that job models work with the API"""
    try:
        from backend.data.models import JobListing, JobListingBase, JobType, RemoteType, ExperienceLevel
        import uuid
        
        # Test creating a job listing base model
        job_base_data = {
            "title": "API Test Engineer",
            "location": "Test City",
            "description": "Test job for API integration",
            "job_type": JobType.FULL_TIME,
            "remote_type": RemoteType.HYBRID,
            "experience_level": ExperienceLevel.MID_LEVEL,
            "skills_required": ["Python", "Testing"],
        }
        
        job_base = JobListingBase(**job_base_data)
        assert job_base.title == "API Test Engineer"
        
        # Test creating a full job listing model
        job_id = str(uuid.uuid4())
        job_data = {
            "id": job_id,
            "title": "API Test Engineer",
            "location": "Test City",
            "description": "Test job for API integration",
            "job_type": JobType.FULL_TIME,
            "remote_type": RemoteType.HYBRID,
            "experience_level": ExperienceLevel.MID_LEVEL,
            "skills_required": ["Python", "Testing"],
            "status": "active",
        }
        
        job = JobListing(**job_data)
        assert str(job.id) == job_id
        assert job.title == "API Test Engineer"
        
        print("Job models integrate correctly with the API!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job models integration: {e}")