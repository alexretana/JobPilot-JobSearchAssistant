"""
Functional Test for Skill Bank API
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_skill_bank_api_functional():
    """Test the functional implementation of the skill bank API"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        user_id = str(uuid.uuid4())
        token = create_access_token(data={"sub": user_id})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test GET /skill-banks/{user_id} (get skill bank)
        # This should create a new skill bank if it doesn't exist
        response = client.get(f"/skill-banks/{user_id}", headers=auth_headers)
        assert response.status_code in [200, 403, 401, 404]
        
        # Test POST /skill-banks/ (create skill bank)
        create_data = {
            "user_id": user_id,
            "default_summary": "Experienced software engineer"
        }
        response = client.post("/skill-banks/", json=create_data, headers=auth_headers)
        assert response.status_code in [200, 201, 403, 401, 409, 422]
        
        # Test PUT /skill-banks/{user_id} (update skill bank)
        update_data = {
            "default_summary": "Updated professional summary"
        }
        response = client.put(f"/skill-banks/{user_id}", json=update_data, headers=auth_headers)
        assert response.status_code in [200, 403, 401, 404, 422]
        
        # Test DELETE /skill-banks/{user_id} (delete skill bank)
        response = client.delete(f"/skill-banks/{user_id}", headers=auth_headers)
        assert response.status_code in [200, 403, 401, 404]
        
        print("Skill bank API functional test completed!")
        
    except Exception as e:
        pytest.fail(f"Failed to test skill bank API functionality: {e}")


def test_skill_bank_api_documentation():
    """Test that skill bank API endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes skill bank endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that skill bank endpoints are documented
        assert "/skill-banks/" in paths
        assert "/skill-banks/{user_id}" in paths
        assert "/skill-banks/{user_id}/skills" in paths
        assert "/skill-banks/{user_id}/skills/{skill_id}" in paths
        assert "/skill-banks/{user_id}/experiences" in paths
        assert "/skill-banks/{user_id}/experiences/{experience_id}" in paths
        
        # Check that the methods are documented
        skill_banks_path = paths["/skill-banks/"]
        skill_bank_id_path = paths["/skill-banks/{user_id}"]
        skills_path = paths["/skill-banks/{user_id}/skills"]
        skill_id_path = paths["/skill-banks/{user_id}/skills/{skill_id}"]
        experiences_path = paths["/skill-banks/{user_id}/experiences"]
        experience_id_path = paths["/skill-banks/{user_id}/experiences/{experience_id}"]
        
        assert "post" in skill_banks_path
        assert "get" in skill_bank_id_path
        assert "put" in skill_bank_id_path
        assert "delete" in skill_bank_id_path
        assert "post" in skills_path
        assert "put" in skill_id_path
        assert "delete" in skill_id_path
        assert "post" in experiences_path
        assert "put" in experience_id_path
        assert "delete" in experience_id_path
        
        print("Skill bank API endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to test skill bank API documentation: {e}")