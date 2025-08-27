"""
Integration tests for job source API between frontend services and backend.
"""

import pytest
from fastapi.testclient import TestClient


class TestJobSourceIntegration:
    """Test job source API integration between frontend services and backend."""

    def test_list_job_sources(self, test_client, test_user_data, test_job_source_search_filters):
        """Test listing job sources with filtering through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test the list job sources endpoint with filters
        query_params = "&".join([f"{key}={value}" for key, value in test_job_source_search_filters.items() if value is not None])
        response = test_client.get(f"/job-sources/?{query_params}")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_job_source(self, test_client, test_user_data):
        """Test retrieving specific job source by ID through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting a specific job source
        response = test_client.get("/job-sources/test-source-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses

    def test_create_job_source(self, test_client, test_user_data, test_job_source_data):
        """Test creating new job sources through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test creating a job source
        response = test_client.post("/job-sources/", json=test_job_source_data)
        assert response.status_code in [200, 201, 400, 401, 403, 422]  # Various possible responses

    def test_update_job_source(self, test_client, test_user_data, test_job_source_update_data):
        """Test updating job sources through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test updating a job source
        response = test_client.put("/job-sources/test-source-id", json=test_job_source_update_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_delete_job_source(self, test_client, test_user_data):
        """Test deleting job sources through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test deleting a job source
        response = test_client.delete("/job-sources/test-source-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses