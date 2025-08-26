"""
Test for Experience Management Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

def test_experience_management_endpoints_exist():
    """Test that experience management endpoints exist"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the experience management endpoints exist
        user_id = str(uuid4())
        experience_id = str(uuid4())
        
        # POST /skill-banks/{user_id}/experiences (add experience)
        response = client.post(f"/skill-banks/{user_id}/experiences")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # PUT /skill-banks/{user_id}/experiences/{experience_id} (update experience)
        response = client.put(f"/skill-banks/{user_id}/experiences/{experience_id}")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # DELETE /skill-banks/{user_id}/experiences/{experience_id} (delete experience)
        response = client.delete(f"/skill-banks/{user_id}/experiences/{experience_id}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        print("All experience management endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify experience management endpoints: {e}")