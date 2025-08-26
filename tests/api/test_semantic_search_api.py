import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_semantic_search_api_models():
    """Test that semantic search API models work correctly"""
    try:
        # This test will fail initially since we haven't implemented the models yet
        from backend.api.models.semantic_search.models import (
            SemanticSearchRequest,
            SemanticSearchResponse,
            HybridSearchRequest,
            HybridSearchResponse,
        )
        
        # Test creating a SemanticSearchRequest model
        request_data = SemanticSearchRequest(
            query="python developer",
            limit=20,
        )
        
        assert request_data.query == "python developer"
        assert request_data.limit == 20
        
        print("Semantic search API models work correctly!")
        
    except ImportError as e:
        pytest.fail(f"Failed to import semantic search API models: {e}")
    except Exception as e:
        pytest.fail(f"Failed to test semantic search API models: {e}")

def test_semantic_search_api_endpoints_exist():
    """Test that semantic search API endpoints exist"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the semantic search endpoints exist
        # GET /api/search/semantic (semantic search)
        response = client.get("/search/semantic")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # GET /api/search/hybrid (hybrid search)
        response = client.get("/search/hybrid")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        print("All semantic search API endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify semantic search API endpoints: {e}")

def test_semantic_search_api_documentation():
    """Test that semantic search API endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes semantic search endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that semantic search endpoints are documented
        assert "/search/semantic" in paths
        assert "/search/hybrid" in paths
        
        # Check that the methods are documented
        semantic_path = paths["/search/semantic"]
        hybrid_path = paths["/search/hybrid"]
        
        assert "get" in semantic_path
        assert "get" in hybrid_path
        
        print("Semantic search API endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify semantic search API documentation: {e}")

def test_semantic_search_api_with_authentication():
    """Test semantic search API endpoints with authentication"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-semantic-search-api"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test GET /search/semantic (semantic search) with authentication
        response = client.get("/search/semantic?query=python+developer", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total" in data
        assert "query" in data
        
        # Test GET /search/hybrid (hybrid search) with authentication
        response = client.get("/search/hybrid?query=python+developer", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total" in data
        assert "query" in data
        
        print("All semantic search API endpoints work with authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test semantic search API with authentication: {e}")

def test_semantic_search_api_without_authentication():
    """Test that semantic search API endpoints require authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test GET /search/semantic (semantic search) without authentication
        response = client.get("/search/semantic?query=python+developer")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /search/hybrid (hybrid search) without authentication
        response = client.get("/search/hybrid?query=python+developer")
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("All semantic search API endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test semantic search API without authentication: {e}")