import pytest
from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from backend.api.main import app
from backend.data.models import UserProfileDB
from backend.data.database import get_database_manager
from backend.api.auth import get_password_hash


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def db_manager():
    """Get the database manager"""
    return get_database_manager()


def test_register_user(client, db_manager):
    """Test that a new user can be registered"""
    # Test registering a new user
    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "password": "securepassword123",
        "first_name": "New",
        "last_name": "User"
    })
    
    # Check that the response is successful
    assert response.status_code == 200
    data = response.json()
    
    # Check that the response contains the expected fields
    assert "id" in data
    assert data["email"] == "newuser@example.com"
    assert data["first_name"] == "New"
    assert data["last_name"] == "User"
    assert data["is_active"] == True
    assert data["is_verified"] == False
    
    # Verify that the user was actually stored in the database
    with db_manager.get_session() as session:
        user_db = session.query(UserProfileDB).filter(UserProfileDB.email == "newuser@example.com").first()
        assert user_db is not None
        assert user_db.email == "newuser@example.com"
        assert user_db.first_name == "New"
        assert user_db.last_name == "User"
        assert user_db.is_active == True
        assert user_db.is_verified == False
        # Check that the password was hashed
        assert user_db.hashed_password is not None
        assert user_db.hashed_password != "securepassword123"


def test_register_duplicate_user(client, db_manager):
    """Test that registering a user with an existing email fails"""
    # First, register a user
    response1 = client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "securepassword123",
        "first_name": "First",
        "last_name": "User"
    })
    assert response1.status_code == 200
    
    # Try to register the same email again
    response2 = client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "differentpassword456",
        "first_name": "Second",
        "last_name": "User"
    })
    
    # Check that the response shows an error
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data
    assert "exists" in data["detail"]


def test_login_user(client, db_manager):
    """Test that a user can login with correct credentials"""
    # First, register a user
    client.post("/auth/register", json={
        "email": "loginuser@example.com",
        "password": "loginpassword123",
        "first_name": "Login",
        "last_name": "User"
    })
    
    # Test logging in with correct credentials
    response = client.post("/auth/login", json={
        "email": "loginuser@example.com",
        "password": "loginpassword123"
    })
    
    # Check that the response is successful
    assert response.status_code == 200
    data = response.json()
    
    # Check that the response contains the expected fields
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Verify that the token is a valid JWT
    token = data["access_token"]
    assert isinstance(token, str)
    assert len(token) > 0


def test_login_nonexistent_user(client):
    """Test that login fails with nonexistent user"""
    # Test logging in with nonexistent user
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "anypassword"
    })
    
    # Check that the response shows an error
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert "Incorrect email or password" in data["detail"]


def test_login_wrong_password(client, db_manager):
    """Test that login fails with wrong password"""
    # First, register a user
    client.post("/auth/register", json={
        "email": "wrongpass@example.com",
        "password": "correctpassword123",
        "first_name": "Wrong",
        "last_name": "Password"
    })
    
    # Test logging in with wrong password
    response = client.post("/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "incorrectpassword"
    })
    
    # Check that the response shows an error
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert "Incorrect email or password" in data["detail"]


def test_logout_user(client):
    """Test that a user can logout"""
    # Test logging out (should always succeed in JWT system)
    response = client.post("/auth/logout")
    
    # Check that the response is successful
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Logged out successfully"


def test_refresh_token(client):
    """Test that the refresh token endpoint exists"""
    # Test the refresh token endpoint
    response = client.post("/auth/refresh")
    
    # Check that the response is successful (even if not fully implemented)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data