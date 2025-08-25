import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_complete_project_structure():
    """Test that the complete API project structure is properly set up"""
    try:
        # Test 1: Main application import
        from backend.api.main import app
        assert isinstance(app, FastAPI)
        assert app.title == "JobPilot API"
        assert app.version == "0.1.0"
        
        # Test 2: Configuration import and values
        from backend.api.config import settings
        assert settings.API_TITLE == "JobPilot API"
        assert settings.API_VERSION == "0.1.0"
        
        # Test 3: Dependencies import
        from backend.api.dependencies import get_db
        db_gen = get_db()
        next(db_gen)  # Should work without errors
        try:
            next(db_gen)
        except StopIteration:
            pass  # Expected when generator is exhausted
        
        # Test 4: CORS middleware
        middleware_strings = [str(middleware) for middleware in app.user_middleware]
        cors_middleware_found = any("CORSMiddleware" in middleware_str for middleware_str in middleware_strings)
        assert cors_middleware_found, f"CORSMiddleware not found in {middleware_strings}"
        
        # Test 5: API endpoints
        client = TestClient(app)
        
        # Root endpoint
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the JobPilot API"}
        
        # Health check endpoint
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
        
        # Documentation endpoints
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        print("All project structure tests passed!")
        
    except ImportError as e:
        pytest.fail(f"Project structure incomplete: {e}")
    except Exception as e:
        pytest.fail(f"Project structure test failed: {e}")