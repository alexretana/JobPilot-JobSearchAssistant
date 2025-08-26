import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_analytics_reporting_api_models():
    """Test that analytics & reporting API models work correctly"""
    try:
        # This test will fail initially since we haven't implemented the models yet
        from backend.api.models.analytics.models import (
            GeneralStatsResponse,
            JobStatsResponse,
            UserStatsResponse,
            ApplicationStatsResponse,
        )
        
        # Test creating a GeneralStatsResponse model
        from datetime import datetime
        general_stats = GeneralStatsResponse(
            total_jobs=1250,
            total_users=850,
            total_applications=2100,
            total_companies=150,
            total_resumes=950,
            total_skill_banks=420,
            total_job_sources=25,
            active_users_last_24h=125,
            new_jobs_last_24h=45,
            new_applications_last_24h=78,
            processed_at=datetime.utcnow()
        )
        
        assert general_stats.total_jobs == 1250
        assert general_stats.total_users == 850
        assert general_stats.total_applications == 2100
        assert general_stats.total_companies == 150
        
        print("Analytics & reporting API models work correctly!")
        
    except ImportError as e:
        pytest.fail(f"Failed to import analytics & reporting API models: {e}")
    except Exception as e:
        pytest.fail(f"Failed to test analytics & reporting API models: {e}")

def test_analytics_reporting_api_endpoints_exist():
    """Test that analytics & reporting API endpoints exist"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the analytics & reporting endpoints exist
        # GET /api/stats/general (general statistics)
        response = client.get("/stats/general")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # GET /api/stats/jobs (job statistics)
        response = client.get("/stats/jobs")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # GET /api/stats/users (user statistics)
        response = client.get("/stats/users")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # GET /api/stats/applications (application statistics)
        response = client.get("/stats/applications")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # GET /api/stats/resumes (resume statistics)
        response = client.get("/stats/resumes")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # GET /api/stats/skill-banks (skill bank statistics)
        response = client.get("/stats/skill-banks")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # GET /api/stats/job-sources (job source statistics)
        response = client.get("/stats/job-sources")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        print("All analytics & reporting API endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify analytics & reporting API endpoints: {e}")

def test_analytics_reporting_api_documentation():
    """Test that analytics & reporting API endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes analytics & reporting endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that analytics & reporting endpoints are documented
        assert "/stats/general" in paths
        assert "/stats/jobs" in paths
        assert "/stats/users" in paths
        assert "/stats/applications" in paths
        assert "/stats/resumes" in paths
        assert "/stats/skill-banks" in paths
        assert "/stats/job-sources" in paths
        
        # Check that the methods are documented
        general_stats_path = paths["/stats/general"]
        job_stats_path = paths["/stats/jobs"]
        user_stats_path = paths["/stats/users"]
        application_stats_path = paths["/stats/applications"]
        resume_stats_path = paths["/stats/resumes"]
        skill_bank_stats_path = paths["/stats/skill-banks"]
        job_source_stats_path = paths["/stats/job-sources"]
        
        assert "get" in general_stats_path
        assert "get" in job_stats_path
        assert "get" in user_stats_path
        assert "get" in application_stats_path
        assert "get" in resume_stats_path
        assert "get" in skill_bank_stats_path
        assert "get" in job_source_stats_path
        
        print("Analytics & reporting API endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify analytics & reporting API documentation: {e}")

def test_analytics_reporting_api_with_authentication():
    """Test analytics & reporting API endpoints with authentication"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-analytics-reporting-api"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test GET /stats/general (general statistics) with authentication
        response = client.get("/stats/general", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_jobs" in data
        assert "total_users" in data
        assert "total_applications" in data
        assert "total_companies" in data
        
        # Test GET /stats/jobs (job statistics) with authentication
        response = client.get("/stats/jobs", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_jobs" in data
        assert "jobs_by_type" in data
        assert "jobs_by_remote_type" in data
        assert "jobs_by_experience_level" in data
        
        # Test GET /stats/users (user statistics) with authentication
        response = client.get("/stats/users", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "users_by_role" in data
        assert "users_by_status" in data
        assert "recent_registrations" in data
        
        # Test GET /stats/applications (application statistics) with authentication
        response = client.get("/stats/applications", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_applications" in data
        assert "applications_by_status" in data
        assert "applications_by_job_type" in data
        assert "recent_applications" in data
        
        # Test GET /stats/resumes (resume statistics) with authentication
        response = client.get("/stats/resumes", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_resumes" in data
        assert "resumes_by_type" in data
        assert "resumes_by_status" in data
        assert "recent_resumes" in data
        
        # Test GET /stats/skill-banks (skill bank statistics) with authentication
        response = client.get("/stats/skill-banks", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_skill_banks" in data
        assert "average_skills_per_bank" in data
        assert "top_skills" in data
        assert "skill_categories" in data
        
        # Test GET /stats/job-sources (job source statistics) with authentication
        response = client.get("/stats/job-sources", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_job_sources" in data
        assert "active_job_sources" in data
        assert "sources_by_type" in data
        assert "jobs_per_source" in data
        
        print("All analytics & reporting API endpoints work with authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test analytics & reporting API with authentication: {e}")

def test_analytics_reporting_api_without_authentication():
    """Test that analytics & reporting API endpoints require authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test GET /stats/general (general statistics) without authentication
        response = client.get("/stats/general")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /stats/jobs (job statistics) without authentication
        response = client.get("/stats/jobs")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /stats/users (user statistics) without authentication
        response = client.get("/stats/users")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /stats/applications (application statistics) without authentication
        response = client.get("/stats/applications")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /stats/resumes (resume statistics) without authentication
        response = client.get("/stats/resumes")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /stats/skill-banks (skill bank statistics) without authentication
        response = client.get("/stats/skill-banks")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /stats/job-sources (job source statistics) without authentication
        response = client.get("/stats/job-sources")
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("All analytics & reporting API endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test analytics & reporting API without authentication: {e}")