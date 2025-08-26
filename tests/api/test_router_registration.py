import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_all_routers_registered():
    """Test that all routers are properly registered with the main app"""
    try:
        from backend.api.main import app
        
        # Get all registered routes
        routes = app.routes
        
        # Check that we have routes with the expected prefixes
        route_paths = [route.path for route in routes]
        
        # Check for job routes
        assert any(path.startswith("/jobs") for path in route_paths)
        
        # Check for user routes
        assert any(path.startswith("/users") for path in route_paths)
        
        # Check for company routes
        assert any(path.startswith("/companies") for path in route_paths)
        
        # Check for application routes
        assert any(path.startswith("/applications") for path in route_paths)
        
        # Check for resume routes
        assert any(path.startswith("/resumes") for path in route_paths)
        
        print("All routers are properly registered!")
        
    except ImportError as e:
        pytest.fail(f"Failed to import main app: {e}")
    except Exception as e:
        pytest.fail(f"Failed to verify router registration: {e}")

def test_job_routes_functionality():
    """Test that job routes are functional"""
    try:
        from backend.api.main import app
        client = TestClient(app)
        
        # Test list jobs endpoint
        response = client.get("/jobs/")
        assert response.status_code == 403  # Requires authentication
        
        # Test get job endpoint
        response = client.get("/jobs/123")
        assert response.status_code == 403  # Requires authentication
        
        # Test create job endpoint
        response = client.post("/jobs/")
        assert response.status_code == 403  # Requires authentication
        
        # Test update job endpoint
        response = client.put("/jobs/123")
        assert response.status_code == 403  # Requires authentication
        
        # Test delete job endpoint
        response = client.delete("/jobs/123")
        assert response.status_code == 403  # Requires authentication
        
        print("All job routes properly require authentication!")
        
    except ImportError as e:
        pytest.fail(f"Failed to import main app: {e}")
    except Exception as e:
        pytest.fail(f"Failed to test job routes: {e}")

def test_user_routes_functionality():
    """Test that user routes are functional"""
    try:
        from backend.api.main import app
        client = TestClient(app)
        
        # Test list users endpoint
        response = client.get("/users/")
        assert response.status_code == 403  # Requires authentication
        
        # Test get user endpoint
        response = client.get("/users/123")
        assert response.status_code == 403  # Requires authentication
        
        # Test create user endpoint
        response = client.post("/users/")
        assert response.status_code == 403  # Requires authentication
        
        # Test update user endpoint
        response = client.put("/users/123")
        assert response.status_code == 403  # Requires authentication
        
        # Test delete user endpoint
        response = client.delete("/users/123")
        assert response.status_code == 403  # Requires authentication
        
        print("All user routes properly require authentication!")
        
    except ImportError as e:
        pytest.fail(f"Failed to import main app: {e}")
    except Exception as e:
        pytest.fail(f"Failed to test user routes: {e}")

def test_company_routes_functionality():
    """Test that company routes are functional"""
    try:
        from backend.api.main import app
        client = TestClient(app)
        
        # Test list companies endpoint
        response = client.get("/companies/")
        assert response.status_code == 403  # Requires authentication
        
        # Test get company endpoint
        response = client.get("/companies/123")
        assert response.status_code == 403  # Requires authentication
        
        # Test create company endpoint
        response = client.post("/companies/")
        assert response.status_code == 403  # Requires authentication
        
        # Test update company endpoint
        response = client.put("/companies/123")
        assert response.status_code == 403  # Requires authentication
        
        # Test delete company endpoint
        response = client.delete("/companies/123")
        assert response.status_code == 403  # Requires authentication
        
        print("All company routes properly require authentication!")
        
    except ImportError as e:
        pytest.fail(f"Failed to import main app: {e}")
    except Exception as e:
        pytest.fail(f"Failed to test company routes: {e}")

def test_application_routes_functionality():
    """Test that application routes are functional"""
    try:
        from backend.api.main import app
        client = TestClient(app)
        
        # Test list applications endpoint
        response = client.get("/applications/")
        assert response.status_code == 403  # Requires authentication
        
        # Test get application endpoint
        response = client.get("/applications/123")
        assert response.status_code == 403  # Requires authentication
        
        # Test create application endpoint
        response = client.post("/applications/")
        assert response.status_code == 403  # Requires authentication
        
        # Test update application endpoint
        response = client.put("/applications/123")
        assert response.status_code == 403  # Requires authentication
        
        # Test delete application endpoint
        response = client.delete("/applications/123")
        assert response.status_code == 403  # Requires authentication
        
        print("All application routes properly require authentication!")
        
    except ImportError as e:
        pytest.fail(f"Failed to import main app: {e}")
    except Exception as e:
        pytest.fail(f"Failed to test application routes: {e}")

def test_resume_routes_functionality():
    """Test that resume routes are functional"""
    try:
        from backend.api.main import app
        client = TestClient(app)
        
        # Test list resumes endpoint
        response = client.get("/resumes/")
        assert response.status_code == 403  # Requires authentication
        
        # Test get resume endpoint
        response = client.get("/resumes/123")
        assert response.status_code == 403  # Requires authentication
        
        # Test create resume endpoint
        response = client.post("/resumes/")
        assert response.status_code == 403  # Requires authentication
        
        # Test update resume endpoint
        response = client.put("/resumes/123")
        assert response.status_code == 403  # Requires authentication
        
        # Test delete resume endpoint
        response = client.delete("/resumes/123")
        assert response.status_code == 403  # Requires authentication
        
        print("All resume routes properly require authentication!")
        
    except ImportError as e:
        pytest.fail(f"Failed to import main app: {e}")
    except Exception as e:
        pytest.fail(f"Failed to test resume routes: {e}")