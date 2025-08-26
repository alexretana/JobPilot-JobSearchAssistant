import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_job_deduplication_api_models():
    """Test that job deduplication API models work correctly"""
    try:
        # This test will fail initially since we haven't implemented the models yet
        from backend.api.models.job_deduplication.models import (
            JobDeduplicationRequest,
            JobDeduplicationResponse,
            BatchDeduplicationRequest,
            BatchDeduplicationResponse,
        )
        
        # Test creating a JobDeduplicationRequest model
        request_data = JobDeduplicationRequest(
            job_id_1="job-123",
            job_id_2="job-456",
        )
        
        assert request_data.job_id_1 == "job-123"
        assert request_data.job_id_2 == "job-456"
        
        print("Job deduplication API models work correctly!")
        
    except ImportError as e:
        pytest.fail(f"Failed to import job deduplication API models: {e}")
    except Exception as e:
        pytest.fail(f"Failed to test job deduplication API models: {e}")

def test_job_deduplication_api_endpoints_exist():
    """Test that job deduplication API endpoints exist"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the job deduplication endpoints exist
        # POST /api/jobs/deduplicate (check if two jobs are duplicates)
        response = client.post("/jobs/deduplicate")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # POST /api/jobs/deduplicate-batch (find duplicates in a batch of jobs)
        response = client.post("/jobs/deduplicate-batch")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        print("All job deduplication API endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify job deduplication API endpoints: {e}")

def test_job_deduplication_api_documentation():
    """Test that job deduplication API endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes job deduplication endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that job deduplication endpoints are documented
        assert "/jobs/deduplicate" in paths
        assert "/jobs/deduplicate-batch" in paths
        
        # Check that the methods are documented
        deduplicate_path = paths["/jobs/deduplicate"]
        deduplicate_batch_path = paths["/jobs/deduplicate-batch"]
        
        assert "post" in deduplicate_path
        assert "post" in deduplicate_batch_path
        
        print("Job deduplication API endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify job deduplication API documentation: {e}")

def test_job_deduplication_api_with_authentication():
    """Test job deduplication API endpoints with authentication"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-job-deduplication-api"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test POST /jobs/deduplicate (check if two jobs are duplicates) with authentication
        response = client.post("/jobs/deduplicate", headers=auth_headers, json={
            "job_id_1": "job-123",
            "job_id_2": "job-456"
        })
        assert response.status_code == 200
        data = response.json()
        assert "is_duplicate" in data
        assert "confidence_score" in data
        assert "matching_fields" in data
        
        # Test POST /jobs/deduplicate-batch (find duplicates in a batch of jobs) with authentication
        response = client.post("/jobs/deduplicate-batch", headers=auth_headers, json={
            "job_ids": ["job-123", "job-456", "job-789"]
        })
        assert response.status_code == 200
        data = response.json()
        assert "duplicates" in data
        assert "total_checked" in data
        assert "total_duplicates_found" in data
        
        print("All job deduplication API endpoints work with authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job deduplication API with authentication: {e}")

def test_job_deduplication_api_without_authentication():
    """Test that job deduplication API endpoints require authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test POST /jobs/deduplicate (check if two jobs are duplicates) without authentication
        response = client.post("/jobs/deduplicate", json={
            "job_id_1": "job-123",
            "job_id_2": "job-456"
        })
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test POST /jobs/deduplicate-batch (find duplicates in a batch of jobs) without authentication
        response = client.post("/jobs/deduplicate-batch", json={
            "job_ids": ["job-123", "job-456", "job-789"]
        })
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("All job deduplication API endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job deduplication API without authentication: {e}")