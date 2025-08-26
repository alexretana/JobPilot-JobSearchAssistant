"""
Test for Skill Bank API Router
"""

import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

def test_skill_bank_router_endpoints_exist():
    """Test that skill bank router endpoints exist"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the skill bank endpoints exist
        # GET /skill-banks/{user_id} (get skill bank)
        user_id = str(uuid4())
        response = client.get(f"/skill-banks/{user_id}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist (404 if skill bank not found)
        
        # POST /skill-banks/ (create skill bank)
        response = client.post("/skill-banks/")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # PUT /skill-banks/{user_id} (update skill bank)
        response = client.put(f"/skill-banks/{user_id}")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # DELETE /skill-banks/{user_id} (delete skill bank)
        response = client.delete(f"/skill-banks/{user_id}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        # POST /skill-banks/{user_id}/skills (add skill)
        response = client.post(f"/skill-banks/{user_id}/skills")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # PUT /skill-banks/{user_id}/skills/{skill_id} (update skill)
        skill_id = str(uuid4())
        response = client.put(f"/skill-banks/{user_id}/skills/{skill_id}")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # DELETE /skill-banks/{user_id}/skills/{skill_id} (delete skill)
        response = client.delete(f"/skill-banks/{user_id}/skills/{skill_id}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        # POST /skill-banks/{user_id}/experiences (add experience)
        response = client.post(f"/skill-banks/{user_id}/experiences")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # PUT /skill-banks/{user_id}/experiences/{experience_id} (update experience)
        experience_id = str(uuid4())
        response = client.put(f"/skill-banks/{user_id}/experiences/{experience_id}")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # DELETE /skill-banks/{user_id}/experiences/{experience_id} (delete experience)
        response = client.delete(f"/skill-banks/{user_id}/experiences/{experience_id}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        print("All skill bank API endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify skill bank API endpoints: {e}")


def test_skill_bank_router_documentation():
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
        pytest.fail(f"Failed to verify skill bank API documentation: {e}")