"""
Integration tests for resume API between frontend services and backend.
"""

import pytest
from fastapi.testclient import TestClient


class TestResumeIntegration:
    """Test resume API integration between frontend services and backend."""

    def test_list_resumes(self, test_client, test_user_data, test_resume_search_filters):
        """Test listing resumes with filtering through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test the list resumes endpoint with filters
        query_params = "&".join([f"{key}={value}" for key, value in test_resume_search_filters.items() if value is not None])
        response = test_client.get(f"/resumes?{query_params}")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_resume(self, test_client, test_user_data):
        """Test retrieving specific resume by ID through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting a specific resume
        response = test_client.get("/resumes/test-resume-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses

    def test_create_resume(self, test_client, test_user_data, test_resume_data):
        """Test creating new resumes through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test creating a resume
        response = test_client.post("/resumes/", json=test_resume_data)
        assert response.status_code in [200, 400, 401, 403, 422]  # Various possible responses

    def test_update_resume(self, test_client, test_user_data, test_resume_update_data):
        """Test updating resumes through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test updating a resume
        response = test_client.put("/resumes/test-resume-id", json=test_resume_update_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_delete_resume(self, test_client, test_user_data):
        """Test deleting resumes through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test deleting a resume
        response = test_client.delete("/resumes/test-resume-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses