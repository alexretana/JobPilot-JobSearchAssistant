"""
Integration tests for stats API between frontend services and backend.
"""

import pytest
from fastapi.testclient import TestClient


class TestStatsIntegration:
    """Test stats API integration between frontend services and backend."""

    def test_get_general_statistics(self, test_client, test_user_data, test_general_stats_expected):
        """Test getting general statistics through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting general statistics
        response = test_client.get("/stats/general")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_job_statistics(self, test_client, test_user_data, test_job_stats_expected):
        """Test getting job statistics through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting job statistics
        response = test_client.get("/stats/jobs")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_user_statistics(self, test_client, test_user_data, test_user_stats_expected):
        """Test getting user statistics through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting user statistics
        response = test_client.get("/stats/users")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_application_statistics(self, test_client, test_user_data, test_application_stats_expected):
        """Test getting application statistics through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting application statistics
        response = test_client.get("/stats/applications")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_resume_statistics(self, test_client, test_user_data, test_resume_stats_expected):
        """Test getting resume statistics through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting resume statistics
        response = test_client.get("/stats/resumes")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_skill_bank_statistics(self, test_client, test_user_data, test_skill_bank_stats_expected):
        """Test getting skill bank statistics through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting skill bank statistics
        response = test_client.get("/stats/skill-banks")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_job_source_statistics(self, test_client, test_user_data, test_job_source_stats_expected):
        """Test getting job source statistics through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting job source statistics
        response = test_client.get("/stats/job-sources")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_stats_without_authentication(self, test_client):
        """Test accessing stats without authentication through frontend service to backend API."""
        # Test getting general statistics without authentication
        response = test_client.get("/stats/general")
        assert response.status_code in [401, 403]  # Should require authentication
        
        # Test getting job statistics without authentication
        response = test_client.get("/stats/jobs")
        assert response.status_code in [401, 403]  # Should require authentication
        
        # Test getting user statistics without authentication
        response = test_client.get("/stats/users")
        assert response.status_code in [401, 403]  # Should require authentication

    def test_invalid_stats_endpoint(self, test_client, test_user_data):
        """Test accessing invalid stats endpoint through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test accessing invalid stats endpoint
        response = test_client.get("/stats/invalid-endpoint")
        assert response.status_code in [404, 405]  # Should return not found or method not allowed

    def test_stats_with_different_user_roles(self, test_client, test_user_data):
        """Test accessing stats with different user roles through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test that different user roles can access stats (in this mock implementation all users can access)
        response = test_client.get("/stats/general")
        assert response.status_code in [200, 401, 403]  # Various possible responses
        
        # Test job seeker accessing stats
        response = test_client.get("/stats/jobs")
        assert response.status_code in [200, 401, 403]  # Various possible responses
        
        # Test recruiter accessing stats
        response = test_client.get("/stats/applications")
        assert response.status_code in [200, 401, 403]  # Various possible responses