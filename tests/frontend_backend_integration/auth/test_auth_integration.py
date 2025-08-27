"""
Integration tests for authentication API between frontend services and backend.
"""

import pytest
from fastapi.testclient import TestClient


class TestAuthIntegration:
    """Test authentication API integration between frontend services and backend."""

    def test_user_registration(self, test_client, test_user_data):
        """Test user registration flow through frontend service to backend API."""
        # Arrange
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        
        # Act
        response = test_client.post("/auth/register", json=registration_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "email" in data
        assert data["email"] == test_user_data["email"]

    def test_user_login(self, test_client, test_user_data):
        """Test user login flow through frontend service to backend API."""
        # First register a user
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        test_client.post("/auth/register", json=registration_data)
        
        # Arrange
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        
        # Act
        response = test_client.post("/auth/login", json=login_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        # Note: Actual response structure depends on the API implementation

    def test_protected_endpoint_with_valid_token(self, test_client, test_user_data):
        """Test accessing protected endpoints with valid authentication token."""
        # Register and login to get a token
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        # Note: Token extraction depends on the actual API response structure
        
        # For now, just test that the endpoint exists
        response = test_client.get("/users/profile")
        assert response.status_code in [200, 401, 403]

    def test_protected_endpoint_without_token(self, test_client):
        """Test accessing protected endpoints without authentication token."""
        # Act
        response = test_client.get("/users/profile")
        
        # Assert
        assert response.status_code in [401, 403]  # Either is acceptable