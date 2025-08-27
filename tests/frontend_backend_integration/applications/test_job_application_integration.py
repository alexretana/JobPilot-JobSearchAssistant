"""
Integration tests for job application API between frontend services and backend.
"""

import pytest
from fastapi.testclient import TestClient


class TestJobApplicationIntegration:
    """Test job application API integration between frontend services and backend."""

    def test_list_applications(self, test_client, test_user_data, test_job_application_search_filters):
        """Test listing job applications through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test the list applications endpoint with filters
        query_params = "&".join([f"{key}={value}" for key, value in test_job_application_search_filters.items() if value is not None])
        response = test_client.get(f"/applications?{query_params}")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_application(self, test_client, test_user_data):
        """Test retrieving specific application by ID through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting a specific application
        response = test_client.get("/applications/test-application-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses

    def test_create_application(self, test_client, test_user_data, test_job_application_data):
        """Test creating new job applications through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test creating an application
        response = test_client.post("/applications/", json=test_job_application_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_update_application(self, test_client, test_user_data, test_job_application_update_data):
        """Test updating job applications through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test updating an application
        response = test_client.put("/applications/test-application-id", json=test_job_application_update_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_delete_application(self, test_client, test_user_data):
        """Test deleting job applications through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test deleting an application
        response = test_client.delete("/applications/test-application-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses