import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid
from datetime import datetime

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_job_sources_api_models():
    """Test that job sources API models work correctly"""
    try:
        # This test will fail initially since we haven't implemented the models yet
        from backend.api.models.job_sources.models import (
            JobSourceCreate,
            JobSourceUpdate,
            JobSourceResponse,
        )
        
        # Test creating a JobSourceCreate model
        create_data = JobSourceCreate(
            name="linkedin",
            display_name="LinkedIn Jobs",
            base_url="https://linkedin.com/jobs",
            api_available=True,
            scraping_rules={"test": "rule"},
            rate_limit_config={"requests_per_minute": 10},
            is_active=True
        )
        
        assert create_data.name == "linkedin"
        assert create_data.display_name == "LinkedIn Jobs"
        assert create_data.base_url == "https://linkedin.com/jobs"
        assert create_data.api_available == True
        assert create_data.scraping_rules == {"test": "rule"}
        assert create_data.rate_limit_config == {"requests_per_minute": 10}
        assert create_data.is_active == True
        
        # Test creating a JobSourceUpdate model
        update_data = JobSourceUpdate(
            name="indeed",
            display_name="Indeed Jobs",
            base_url="https://indeed.com/jobs",
            api_available=False,
            scraping_rules={"test": "updated_rule"},
            rate_limit_config={"requests_per_minute": 20},
            is_active=False,
            last_scraped=datetime.utcnow()
        )
        
        assert update_data.name == "indeed"
        assert update_data.display_name == "Indeed Jobs"
        assert update_data.base_url == "https://indeed.com/jobs"
        assert update_data.api_available == False
        assert update_data.scraping_rules == {"test": "updated_rule"}
        assert update_data.rate_limit_config == {"requests_per_minute": 20}
        assert update_data.is_active == False
        assert update_data.last_scraped is not None
        
        # Test creating a JobSourceResponse model
        response_data = JobSourceResponse(
            id=uuid.uuid4(),
            name="glassdoor",
            display_name="Glassdoor Jobs",
            base_url="https://glassdoor.com/jobs",
            api_available=False,
            scraping_rules={"test": "response_rule"},
            rate_limit_config={"requests_per_minute": 15},
            last_scraped=datetime.utcnow(),
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        assert response_data.name == "glassdoor"
        assert response_data.display_name == "Glassdoor Jobs"
        assert response_data.base_url == "https://glassdoor.com/jobs"
        assert response_data.api_available == False
        assert response_data.scraping_rules == {"test": "response_rule"}
        assert response_data.rate_limit_config == {"requests_per_minute": 15}
        assert response_data.is_active == True
        assert response_data.created_at is not None
        assert response_data.updated_at is not None
        
        print("Job sources API models work correctly!")
        
    except ImportError as e:
        pytest.fail(f"Failed to import job sources API models: {e}")
    except Exception as e:
        pytest.fail(f"Failed to test job sources API models: {e}")

def test_job_sources_api_endpoints_exist():
    """Test that job sources API endpoints exist"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the job sources endpoints exist
        # POST /api/job-sources (create job source)
        response = client.post("/job-sources/")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # GET /api/job-sources (list job sources)
        response = client.get("/job-sources/")
        assert response.status_code in [200, 403, 401]  # Should exist
        
        # GET /api/job-sources/{source_id} (get specific job source)
        source_id = str(uuid.uuid4())
        response = client.get(f"/job-sources/{source_id}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        # PUT /api/job-sources/{source_id} (update job source)
        response = client.put(f"/job-sources/{source_id}")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # DELETE /api/job-sources/{source_id} (delete job source)
        response = client.delete(f"/job-sources/{source_id}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        print("All job sources API endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify job sources API endpoints: {e}")

def test_job_sources_api_documentation():
    """Test that job sources API endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes job sources endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that job sources endpoints are documented
        assert "/job-sources/" in paths
        assert "/job-sources/{source_id}" in paths
        
        # Check that the methods are documented
        job_sources_path = paths["/job-sources/"]
        job_sources_id_path = paths["/job-sources/{source_id}"]
        
        assert "post" in job_sources_path
        assert "get" in job_sources_path
        assert "get" in job_sources_id_path
        assert "put" in job_sources_id_path
        assert "delete" in job_sources_id_path
        
        print("Job sources API endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify job sources API documentation: {e}")

def test_job_sources_api_with_authentication():
    """Test job sources API endpoints with authentication"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-job-sources-api"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test POST /job-sources/ (create job source) with authentication
        response = client.post("/job-sources/", headers=auth_headers)
        assert response.status_code == 422  # Validation error since no data provided
        
        # Test GET /job-sources/ (list job sources) with authentication
        response = client.get("/job-sources/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "sources" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        
        # Test GET /job-sources/{source_id} (get specific job source) with authentication
        source_id = str(uuid.uuid4())
        response = client.get(f"/job-sources/{source_id}", headers=auth_headers)
        assert response.status_code in [200, 403, 401, 404]  # Should exist or not found
        
        # Test PUT /job-sources/{source_id} (update job source) with authentication
        response = client.put(f"/job-sources/{source_id}", headers=auth_headers)
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # Test DELETE /job-sources/{source_id} (delete job source) with authentication
        response = client.delete(f"/job-sources/{source_id}", headers=auth_headers)
        assert response.status_code in [200, 403, 401, 404]  # Should exist or not found
        
        print("All job sources API endpoints work with authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job sources API with authentication: {e}")

def test_job_sources_api_without_authentication():
    """Test that job sources API endpoints require authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test POST /job-sources/ (create job source) without authentication
        response = client.post("/job-sources/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /job-sources/ (list job sources) without authentication
        response = client.get("/job-sources/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /job-sources/{source_id} (get specific job source) without authentication
        source_id = str(uuid.uuid4())
        response = client.get(f"/job-sources/{source_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test PUT /job-sources/{source_id} (update job source) without authentication
        response = client.put(f"/job-sources/{source_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test DELETE /job-sources/{source_id} (delete job source) without authentication
        response = client.delete(f"/job-sources/{source_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("All job sources API endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job sources API without authentication: {e}")