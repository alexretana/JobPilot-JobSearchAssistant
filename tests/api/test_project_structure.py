import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_project_structure_setup():
    """Test that the API project structure is properly set up"""
    try:
        from backend.api.main import app
        assert isinstance(app, FastAPI)
        assert app.title == "JobPilot API"
        assert app.version == "0.1.0"
    except ImportError:
        pytest.fail("API main module not found. Need to create backend/api/main.py")

def test_api_root_endpoint():
    """Test that the API root endpoint is working"""
    try:
        from backend.api.main import app
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the JobPilot API"}
    except ImportError:
        pytest.fail("API main module not found. Need to create backend/api/main.py")

def test_health_check_endpoint():
    """Test that the health check endpoint is working"""
    try:
        from backend.api.main import app
        client = TestClient(app)
        
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    except ImportError:
        pytest.fail("API main module not found. Need to create backend/api/main.py")

def test_api_documentation_available():
    """Test that API documentation endpoints are available"""
    try:
        from backend.api.main import app
        client = TestClient(app)
        
        # Test Swagger UI endpoint
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Test OpenAPI JSON endpoint
        response = client.get("/openapi.json")
        assert response.status_code == 200
    except ImportError:
        pytest.fail("API main module not found. Need to create backend/api/main.py")

def test_cors_middleware():
    """Test that CORS middleware is properly configured"""
    try:
        from backend.api.main import app
        # Check that CORS middleware is in the middleware stack
        middleware_strings = [str(middleware) for middleware in app.user_middleware]
        cors_middleware_found = any("CORSMiddleware" in middleware_str for middleware_str in middleware_strings)
        assert cors_middleware_found, f"CORSMiddleware not found in {middleware_strings}"
    except ImportError:
        pytest.fail("API main module not found. Need to create backend/api/main.py")