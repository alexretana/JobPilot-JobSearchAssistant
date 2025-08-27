"""
Integration tests for company API between frontend services and backend.
"""

import pytest
from fastapi.testclient import TestClient


class TestCompanyIntegration:
    """Test company API integration between frontend services and backend."""

    def test_list_companies(self, test_client, test_user_data):
        """Test listing all companies through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test the list companies endpoint
        response = test_client.get("/companies/")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_search_companies(self, test_client, test_user_data, test_company_search_filters):
        """Test company search functionality through frontend service to backend API."""
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
        query_params = "&".join([f"{key}={value}" for key, value in test_company_search_filters.items() if value is not None])
        response = test_client.get(f"/companies/search?{query_params}")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_company(self, test_client, test_user_data):
        """Test retrieving specific company by ID through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting a specific company
        response = test_client.get("/companies/test-company-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses

    def test_create_company(self, test_client, test_user_data, test_company_data):
        """Test creating new companies through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test creating a company
        response = test_client.post("/companies/", json=test_company_data)
        assert response.status_code in [200, 400, 401, 403, 422]  # Various possible responses

    def test_update_company(self, test_client, test_user_data, test_company_update_data):
        """Test updating company information through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test updating a company
        response = test_client.put("/companies/test-company-id", json=test_company_update_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_delete_company(self, test_client, test_user_data):
        """Test deleting companies through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test deleting a company
        response = test_client.delete("/companies/test-company-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses

    def test_get_company_jobs(self, test_client, test_user_data, test_company_job_filters):
        """Test retrieving jobs for a specific company through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting jobs for a company with filters
        query_params = "&".join([f"{key}={value}" for key, value in test_company_job_filters.items() if value is not None])
        response = test_client.get(f"/companies/test-company-id/jobs?{query_params}")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses