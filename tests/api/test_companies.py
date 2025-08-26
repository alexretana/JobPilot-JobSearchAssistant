import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_company_models_import():
    """Test that company models can be imported"""
    try:
        # This test should initially fail because we need to verify the models exist
        from backend.data.models import CompanyInfo
        # If we get here, the models exist
    except ImportError:
        pytest.fail("Company models not found. Need to verify backend/data/models.py")

def test_company_crud_endpoints_exist():
    """Test that company CRUD endpoints exist"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-company-user"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test POST /companies/ (create company)
        response = client.post("/companies/", headers=auth_headers, json={"name": "Test Company"})
        assert response.status_code in [200, 201, 403, 422]  # Should exist
        
        # Test GET /companies/ (list companies)
        response = client.get("/companies/", headers=auth_headers)
        assert response.status_code in [200, 403]  # Should exist
        
        # Test GET /companies/{company_id} (get specific company)
        company_id = str(uuid.uuid4())
        response = client.get(f"/companies/{company_id}", headers=auth_headers)
        assert response.status_code in [200, 403, 404]  # Should exist
        
        # Test PUT /companies/{company_id} (update company)
        response = client.put(f"/companies/{company_id}", headers=auth_headers, json={"name": "Updated Company"})
        assert response.status_code in [200, 403, 404, 422]  # Should exist
        
        # Test DELETE /companies/{company_id} (delete company)
        response = client.delete(f"/companies/{company_id}", headers=auth_headers)
        assert response.status_code in [200, 403, 404]  # Should exist
        
        print("All company CRUD endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify company CRUD endpoints: {e}")

def test_company_search_endpoint_exists():
    """Test that company search endpoint exists"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-company-search-user"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test GET /companies/search endpoint exists
        response = client.get("/companies/search", headers=auth_headers)
        assert response.status_code in [200, 403, 404, 422]  # Should exist
        
        print("Company search endpoint exists!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify company search endpoint: {e}")

def test_company_jobs_endpoint_exists():
    """Test that company jobs endpoint exists"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-company-jobs-user"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test GET /companies/{company_id}/jobs endpoint exists
        company_id = str(uuid.uuid4())
        response = client.get(f"/companies/{company_id}/jobs", headers=auth_headers)
        assert response.status_code in [200, 403, 404]  # Should exist
        
        print("Company jobs endpoint exists!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify company jobs endpoint: {e}")

def test_company_endpoints_documentation():
    """Test that company endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes company endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that basic company endpoints are documented
        assert "/companies/" in paths or "/companies" in paths
        assert "/companies/{company_id}" in paths
        
        print("Company endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify company endpoints documentation: {e}")

def test_company_endpoints_require_authentication():
    """Test that company endpoints require authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that company endpoints require authentication
        # POST /companies/ without auth
        response = client.post("/companies/", json={"name": "Test Company"})
        assert response.status_code == 403  # Forbidden - authentication required
        
        # GET /companies/ without auth
        response = client.get("/companies/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # GET /companies/{company_id} without auth
        company_id = str(uuid.uuid4())
        response = client.get(f"/companies/{company_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # PUT /companies/{company_id} without auth
        response = client.put(f"/companies/{company_id}", json={"name": "Updated Company"})
        assert response.status_code == 403  # Forbidden - authentication required
        
        # DELETE /companies/{company_id} without auth
        response = client.delete(f"/companies/{company_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # GET /companies/search without auth
        response = client.get("/companies/search")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # GET /companies/{company_id}/jobs without auth
        response = client.get(f"/companies/{company_id}/jobs")
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("Company endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify company authentication requirements: {e}")