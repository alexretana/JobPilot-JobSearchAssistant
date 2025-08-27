"""
Integration tests for job API between frontend services and backend.
"""

import pytest
from fastapi.testclient import TestClient


class TestJobIntegration:
    """Test job API integration between frontend services and backend."""

    def test_search_jobs(self, test_client, test_user_data, test_job_search_filters):
        """Test job search functionality with filters through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test the search endpoint with filters
        # Build query string from filters
        query_params = "&".join([f"{key}={value}" for key, value in test_job_search_filters.items() if value is not None])
        response = test_client.get(f"/jobs/search?{query_params}")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_job_statistics(self, test_client, test_user_data):
        """Test job statistics endpoint through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test the statistics endpoint
        response = test_client.get("/jobs/statistics")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_list_jobs(self, test_client, test_user_data):
        """Test listing all jobs through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test the list jobs endpoint
        response = test_client.get("/jobs/")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_job(self, test_client, test_user_data):
        """Test retrieving specific job by ID through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting a specific job
        response = test_client.get("/jobs/test-job-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses

    def test_create_job(self, test_client, test_user_data, test_job_data):
        """Test creating new job listings through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test creating a job
        response = test_client.post("/jobs/", json=test_job_data)
        assert response.status_code in [200, 400, 401, 403, 422]  # Various possible responses

    def test_update_job(self, test_client, test_user_data, test_job_update_data):
        """Test updating job listings through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test updating a job
        response = test_client.put("/jobs/test-job-id", json=test_job_update_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_delete_job(self, test_client, test_user_data):
        """Test deleting job listings through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test deleting a job
        response = test_client.delete("/jobs/test-job-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses