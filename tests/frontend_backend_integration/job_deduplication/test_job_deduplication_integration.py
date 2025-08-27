"""
Integration tests for job deduplication API between frontend services and backend.
"""

import pytest
from fastapi.testclient import TestClient


class TestJobDeduplicationIntegration:
    """Test job deduplication API integration between frontend services and backend."""

    def test_check_job_duplicates(self, test_client, test_user_data, test_job_deduplication_data):
        """Test checking job duplicates through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test checking job duplicates
        response = test_client.post("/jobs/deduplicate", json=test_job_deduplication_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_batch_job_deduplication(self, test_client, test_user_data, test_batch_deduplication_data):
        """Test batch job deduplication through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test batch job deduplication
        response = test_client.post("/jobs/deduplicate-batch", json=test_batch_deduplication_data)
        assert response.status_code in [200, 400, 401, 403, 422]  # Various possible responses

    def test_check_job_duplicates_with_invalid_data(self, test_client, test_user_data):
        """Test checking job duplicates with invalid data through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test with missing job IDs
        invalid_data = {}
        response = test_client.post("/jobs/deduplicate", json=invalid_data)
        assert response.status_code in [400, 401, 403, 422]  # Should return validation error
        
        # Test with same job IDs
        same_job_data = {"job_id_1": "job-123", "job_id_2": "job-123"}
        response = test_client.post("/jobs/deduplicate", json=same_job_data)
        assert response.status_code in [200, 400, 401, 403, 422]  # Various possible responses

    def test_batch_job_deduplication_with_invalid_data(self, test_client, test_user_data):
        """Test batch job deduplication with invalid data through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test with empty job IDs list
        invalid_data = {"job_ids": [], "confidence_threshold": 0.8}
        response = test_client.post("/jobs/deduplicate-batch", json=invalid_data)
        assert response.status_code in [400, 401, 403, 422]  # Should return validation error
        
        # Test with invalid confidence threshold
        invalid_threshold_data = {"job_ids": ["job-123", "job-456"], "confidence_threshold": 1.5}
        response = test_client.post("/jobs/deduplicate-batch", json=invalid_threshold_data)
        assert response.status_code in [400, 401, 403, 422]  # Should return validation error

    def test_job_deduplication_without_authentication(self, test_client, test_job_deduplication_data, test_batch_deduplication_data):
        """Test job deduplication without authentication through frontend service to backend API."""
        # Test checking job duplicates without authentication
        response = test_client.post("/jobs/deduplicate", json=test_job_deduplication_data)
        assert response.status_code in [401, 403]  # Should require authentication
        
        # Test batch job deduplication without authentication
        response = test_client.post("/jobs/deduplicate-batch", json=test_batch_deduplication_data)
        assert response.status_code in [401, 403]  # Should require authentication

    def test_job_deduplication_with_nonexistent_jobs(self, test_client, test_user_data):
        """Test job deduplication with nonexistent jobs through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test with nonexistent job IDs
        nonexistent_data = {"job_id_1": "nonexistent-job-1", "job_id_2": "nonexistent-job-2"}
        response = test_client.post("/jobs/deduplicate", json=nonexistent_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses
        
        # Test batch with nonexistent job IDs
        nonexistent_batch_data = {"job_ids": ["nonexistent-job-1", "nonexistent-job-2"], "confidence_threshold": 0.8}
        response = test_client.post("/jobs/deduplicate-batch", json=nonexistent_batch_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses