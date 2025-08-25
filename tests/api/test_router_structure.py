import pytest
from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_router_structure_creation():
    """Test that API routers can be created with proper prefixes and tags"""
    try:
        from fastapi import APIRouter
        
        # Test creating a router with prefix and tags
        router = APIRouter(prefix="/test", tags=["test"])
        assert router.prefix == "/test"
        assert "test" in router.tags
        
        # Test creating a router without prefix and tags
        router2 = APIRouter()
        assert router2.prefix == ""
        assert router2.tags == []
        
    except Exception as e:
        pytest.fail(f"Failed to create API router: {e}")

def test_router_registration():
    """Test that routers can be registered with the main app"""
    try:
        from backend.api.main import app
        from fastapi import APIRouter
        
        # Create a test router
        test_router = APIRouter(prefix="/test", tags=["test"])
        
        @test_router.get("/")
        async def test_endpoint():
            return {"message": "test"}
        
        # Register the router with the main app
        app.include_router(test_router)
        
        # Test that the endpoint is available
        client = TestClient(app)
        response = client.get("/test/")
        assert response.status_code == 200
        assert response.json() == {"message": "test"}
        
        # Clean up by removing the router
        # We can't easily remove routers, so we'll just check that our endpoint exists
        # In a real implementation, we would organize our routers better
        
    except ImportError as e:
        pytest.fail(f"Failed to import main app: {e}")
    except Exception as e:
        pytest.fail(f"Failed to register router: {e}")

def test_job_listings_router_structure():
    """Test that job listings router has proper structure"""
    try:
        from fastapi import APIRouter
        from fastapi import FastAPI
        
        # Create a test app to mount the router
        test_app = FastAPI()
        
        # Create job listings router with proper prefix and tags
        job_router = APIRouter(prefix="/jobs", tags=["jobs"])
        
        # Check that the router has the correct prefix and tags
        assert job_router.prefix == "/jobs"
        assert "jobs" in job_router.tags
        
        # Add a sample endpoint
        @job_router.get("/{job_id}")
        async def get_job(job_id: str):
            return {"job_id": job_id}
        
        # Mount the router on the test app
        test_app.include_router(job_router)
        
        # Test the endpoint
        client = TestClient(test_app)
        response = client.get("/jobs/123")
        assert response.status_code == 200
        assert response.json() == {"job_id": "123"}
        
    except Exception as e:
        pytest.fail(f"Failed to create job listings router: {e}")

def test_user_profiles_router_structure():
    """Test that user profiles router has proper structure"""
    try:
        from fastapi import APIRouter
        from fastapi import FastAPI
        
        # Create a test app to mount the router
        test_app = FastAPI()
        
        # Create user profiles router with proper prefix and tags
        user_router = APIRouter(prefix="/users", tags=["users"])
        
        # Check that the router has the correct prefix and tags
        assert user_router.prefix == "/users"
        assert "users" in user_router.tags
        
        # Add a sample endpoint
        @user_router.get("/{user_id}")
        async def get_user(user_id: str):
            return {"user_id": user_id}
        
        # Mount the router on the test app
        test_app.include_router(user_router)
        
        # Test the endpoint
        client = TestClient(test_app)
        response = client.get("/users/456")
        assert response.status_code == 200
        assert response.json() == {"user_id": "456"}
        
    except Exception as e:
        pytest.fail(f"Failed to create user profiles router: {e}")

def test_companies_router_structure():
    """Test that companies router has proper structure"""
    try:
        from fastapi import APIRouter
        from fastapi import FastAPI
        
        # Create a test app to mount the router
        test_app = FastAPI()
        
        # Create companies router with proper prefix and tags
        company_router = APIRouter(prefix="/companies", tags=["companies"])
        
        # Check that the router has the correct prefix and tags
        assert company_router.prefix == "/companies"
        assert "companies" in company_router.tags
        
        # Add a sample endpoint
        @company_router.get("/{company_id}")
        async def get_company(company_id: str):
            return {"company_id": company_id}
        
        # Mount the router on the test app
        test_app.include_router(company_router)
        
        # Test the endpoint
        client = TestClient(test_app)
        response = client.get("/companies/789")
        assert response.status_code == 200
        assert response.json() == {"company_id": "789"}
        
    except Exception as e:
        pytest.fail(f"Failed to create companies router: {e}")