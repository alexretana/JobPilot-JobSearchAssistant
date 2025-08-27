"""
Common fixtures and configuration for frontend-backend integration tests.
"""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def test_client():
    """Create a FastAPI TestClient for integration tests."""
    # Set test environment variables
    os.environ["TEST_MODE"] = "true"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    
    # Import the app after setting environment variables
    from backend.api.main import app
    
    with TestClient(app) as client:
        yield client


@pytest.fixture
def auth_headers():
    """Provide authentication headers for protected endpoints."""
    # This would typically involve calling the login endpoint
    # and returning the appropriate Authorization header
    return {"Authorization": "Bearer test-token"}


@pytest.fixture
def test_user_data():
    """Provide test user data for integration tests."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }


@pytest.fixture
def test_job_data():
    """Provide test job data for integration tests."""
    return {
        "title": "Software Engineer",
        "description": "Test job description",
        "location": "Test City, TC",
        "job_type": "Full-time",
        "remote_type": "Remote"
    }


@pytest.fixture
def test_company_data():
    """Provide test company data for integration tests."""
    return {
        "name": "Test Company",
        "industry": "Technology",
        "size": "100-200 employees",
        "location": "Test City, TC",
        "website": "https://testcompany.com"
    }