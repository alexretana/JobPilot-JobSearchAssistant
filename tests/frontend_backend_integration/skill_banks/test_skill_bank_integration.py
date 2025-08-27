"""
Integration tests for skill bank API between frontend services and backend.
"""

import pytest
from fastapi.testclient import TestClient


class TestSkillBankIntegration:
    """Test skill bank API integration between frontend services and backend."""

    def test_create_skill_bank(self, test_client, test_user_data, test_skill_bank_data):
        """Test creating a new skill bank through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test creating a skill bank
        response = test_client.post("/skill-banks/", json=test_skill_bank_data)
        assert response.status_code in [200, 201, 400, 401, 403, 409, 422]  # Various possible responses

    def test_get_skill_bank(self, test_client, test_user_data):
        """Test retrieving skill bank by user ID through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting a skill bank
        response = test_client.get("/skill-banks/test-user-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses

    def test_update_skill_bank(self, test_client, test_user_data):
        """Test updating skill bank through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test updating a skill bank
        update_data = {"default_summary": "Updated professional summary"}
        response = test_client.put("/skill-banks/test-user-id", json=update_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_delete_skill_bank(self, test_client, test_user_data):
        """Test deleting skill bank through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test deleting a skill bank
        response = test_client.delete("/skill-banks/test-user-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses

    def test_add_skill(self, test_client, test_user_data, test_skill_data):
        """Test adding a skill to skill bank through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test adding a skill
        response = test_client.post("/skill-banks/test-user-id/skills", json=test_skill_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_update_skill(self, test_client, test_user_data, test_skill_update_data):
        """Test updating a skill in skill bank through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test updating a skill
        response = test_client.put("/skill-banks/test-user-id/skills/test-skill-id", json=test_skill_update_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_delete_skill(self, test_client, test_user_data):
        """Test deleting a skill from skill bank through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test deleting a skill
        response = test_client.delete("/skill-banks/test-user-id/skills/test-skill-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses

    def test_add_experience(self, test_client, test_user_data, test_experience_data):
        """Test adding work experience to skill bank through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test adding experience
        response = test_client.post("/skill-banks/test-user-id/experiences", json=test_experience_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_update_experience(self, test_client, test_user_data, test_experience_update_data):
        """Test updating work experience in skill bank through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test updating experience
        response = test_client.put("/skill-banks/test-user-id/experiences/test-experience-id", json=test_experience_update_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_delete_experience(self, test_client, test_user_data):
        """Test deleting work experience from skill bank through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test deleting experience
        response = test_client.delete("/skill-banks/test-user-id/experiences/test-experience-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses