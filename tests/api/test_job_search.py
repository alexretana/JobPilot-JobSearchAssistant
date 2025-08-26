import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid
from datetime import datetime, timedelta

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_job_search_endpoint_functionality():
    """Test that job search endpoint works with filters"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-search-user"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test basic search endpoint
        response = client.get("/jobs/search", headers=auth_headers)
        assert response.status_code == 200
        
        # Test search with filters
        response = client.get("/jobs/search?query=python&job_type=Full-time&remote_type=Remote&salary_min=100000", headers=auth_headers)
        assert response.status_code == 200
        
        # Check response structure
        data = response.json()
        assert "message" in data
        assert "user_id" in data
        assert "filters_applied" in data
        assert "results" in data
        assert "total_results" in data
        
        # Check that filters were applied correctly
        filters = data["filters_applied"]
        assert filters["query"] == "python"
        assert filters["job_type"] == "Full-time"
        assert filters["remote_type"] == "Remote"
        assert filters["salary_min"] == 100000
        
        print("Job search endpoint works with filters!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job search endpoint functionality: {e}")

def test_job_statistics_endpoint_functionality():
    """Test that job statistics endpoint works"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-stats-user"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test statistics endpoint
        response = client.get("/jobs/statistics", headers=auth_headers)
        assert response.status_code == 200
        
        # Check response structure
        data = response.json()
        assert "message" in data
        assert "user_id" in data
        assert "total_jobs" in data
        assert "jobs_by_type" in data
        assert "jobs_by_remote_type" in data
        assert "jobs_by_experience_level" in data
        assert "average_salary_by_type" in data
        assert "top_locations" in data
        assert "top_companies" in data
        assert "recent_trend" in data
        
        # Check that statistics data is present
        assert isinstance(data["total_jobs"], int)
        assert isinstance(data["jobs_by_type"], dict)
        assert isinstance(data["jobs_by_remote_type"], dict)
        assert isinstance(data["jobs_by_experience_level"], dict)
        assert isinstance(data["average_salary_by_type"], dict)
        assert isinstance(data["top_locations"], list)
        assert isinstance(data["top_companies"], list)
        assert isinstance(data["recent_trend"], dict)
        
        print("Job statistics endpoint works correctly!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job statistics endpoint functionality: {e}")

def test_job_search_documentation():
    """Test that job search endpoints are properly documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes job search endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that job search endpoints are documented
        assert "/jobs/search" in paths
        assert "/jobs/statistics" in paths
        
        # Check that search endpoint has proper query parameters
        search_endpoint = paths["/jobs/search"]["get"]
        parameters = search_endpoint.get("parameters", [])
        
        # Check for key parameters
        param_names = [param["name"] for param in parameters]
        assert "query" in param_names
        assert "job_type" in param_names
        assert "remote_type" in param_names
        assert "experience_level" in param_names
        assert "salary_min" in param_names
        assert "salary_max" in param_names
        assert "location" in param_names
        assert "company" in param_names
        
        # Check that statistics endpoint is documented
        stats_endpoint = paths["/jobs/statistics"]["get"]
        assert stats_endpoint is not None
        
        print("Job search endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify job search documentation: {e}")

def test_job_search_with_various_filters():
    """Test job search with various combinations of filters"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        from datetime import datetime, timezone
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-filter-user"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test search with location filter
        response = client.get("/jobs/search?location=San+Francisco", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["filters_applied"]["location"] == "San Francisco"
        
        # Test search with company filter
        response = client.get("/jobs/search?company=Tech+Corp", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["filters_applied"]["company"] == "Tech Corp"
        
        # Test search with experience level filter
        response = client.get("/jobs/search?experience_level=mid_level", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["filters_applied"]["experience_level"] == "mid_level"
        
        # Test search with salary range
        response = client.get("/jobs/search?salary_min=80000&salary_max=120000", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["filters_applied"]["salary_min"] == 80000
        assert data["filters_applied"]["salary_max"] == 120000
        
        print("Job search works with various filter combinations!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job search with various filters: {e}")

def test_job_search_without_authentication():
    """Test that job search requires authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test search without authentication
        response = client.get("/jobs/search")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test statistics without authentication
        response = client.get("/jobs/statistics")
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("Job search endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test job search authentication requirements: {e}")