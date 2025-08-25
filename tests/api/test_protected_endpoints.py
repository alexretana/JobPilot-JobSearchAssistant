import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_protected_jobs_endpoint():
    """Test that jobs endpoint requires authentication"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Test accessing jobs endpoint without authentication (should fail)
        response = client.get("/jobs/")
        assert response.status_code == 403  # Forbidden - no credentials provided
        
        # Test accessing jobs endpoint with valid token (should succeed)
        # Create a valid token
        token = create_access_token(data={"sub": "test-user-789"})
        
        # Access endpoint with valid token
        response = client.get("/jobs/", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json()["user_id"] == "test-user-789"
        
        print("Protected jobs endpoint test passed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test protected jobs endpoint: {e}")

def test_all_jobs_endpoints_protected():
    """Test that all jobs endpoints require authentication"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token
        token = create_access_token(data={"sub": "test-user-abc"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test all jobs endpoints
        endpoints = [
            ("GET", "/jobs/"),
            ("GET", "/jobs/123"),
            ("POST", "/jobs/"),
            ("PUT", "/jobs/123"),
            ("DELETE", "/jobs/123"),
        ]
        
        for method, url in endpoints:
            # Test without authentication (should fail)
            if method == "GET":
                response = client.get(url)
            elif method == "POST":
                response = client.post(url)
            elif method == "PUT":
                response = client.put(url)
            elif method == "DELETE":
                response = client.delete(url)
                
            assert response.status_code == 403  # Forbidden - no credentials provided
            
            # Test with authentication (should succeed)
            if method == "GET":
                response = client.get(url, headers=auth_headers)
            elif method == "POST":
                response = client.post(url, headers=auth_headers)
            elif method == "PUT":
                response = client.put(url, headers=auth_headers)
            elif method == "DELETE":
                response = client.delete(url, headers=auth_headers)
                
            assert response.status_code == 200
            
        print("All jobs endpoints protection test passed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test all jobs endpoints protection: {e}")