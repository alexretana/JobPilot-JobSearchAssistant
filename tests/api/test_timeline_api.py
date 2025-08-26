import pytest
from fastapi.testclient import TestClient
import sys
import os
import uuid
from datetime import datetime

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_timeline_api_models():
    """Test that timeline API models work correctly"""
    try:
        # This test will fail initially since we haven't implemented the models yet
        from backend.api.models.timeline.models import (
            TimelineEventCreate,
            TimelineEventUpdate,
            TimelineEventResponse,
            TimelineEventListResponse
        )
        from backend.data.models import TimelineEventType
        
        # Test creating a TimelineEventCreate model
        user_id = str(uuid.uuid4())
        job_id = str(uuid.uuid4())
        application_id = str(uuid.uuid4())
        
        create_data = TimelineEventCreate(
            user_profile_id=user_id,
            event_type=TimelineEventType.JOB_SAVED,
            title="Test Event",
            description="Test description",
            job_id=job_id,
            application_id=application_id,
            event_data={"test": "data"},
            event_date=datetime.utcnow(),
            is_milestone=True
        )
        
        assert create_data.user_profile_id == user_id
        assert create_data.event_type == TimelineEventType.JOB_SAVED
        assert create_data.title == "Test Event"
        assert create_data.description == "Test description"
        assert create_data.job_id == job_id
        assert create_data.application_id == application_id
        assert create_data.event_data == {"test": "data"}
        assert create_data.is_milestone == True
        
        print("Timeline API models work correctly!")
        
    except ImportError as e:
        pytest.fail(f"Failed to import timeline API models: {e}")
    except Exception as e:
        pytest.fail(f"Failed to test timeline API models: {e}")

def test_timeline_api_endpoints_exist():
    """Test that timeline API endpoints exist"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the timeline endpoints exist
        # POST /api/timeline (create timeline event)
        response = client.post("/timeline/")
        assert response.status_code in [200, 403, 401, 422]  # Should exist (422 if validation fails)
        
        # GET /api/timeline (list timeline events)
        response = client.get("/timeline/")
        assert response.status_code in [200, 403, 401]  # Should exist
        
        # GET /api/timeline/{event_id} (get specific timeline event)
        response = client.get(f"/timeline/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        # PUT /api/timeline/{event_id} (update timeline event)
        response = client.put(f"/timeline/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404, 422]  # Should exist
        
        # DELETE /api/timeline/{event_id} (delete timeline event)
        response = client.delete(f"/timeline/{uuid.uuid4()}")
        assert response.status_code in [200, 403, 401, 404]  # Should exist
        
        print("All timeline API endpoints exist!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify timeline API endpoints: {e}")

def test_timeline_api_documentation():
    """Test that timeline API endpoints are documented"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test that the OpenAPI documentation includes timeline endpoints
        docs_response = client.get("/openapi.json")
        assert docs_response.status_code == 200
        
        openapi_spec = docs_response.json()
        paths = openapi_spec.get("paths", {})
        
        # Check that timeline endpoints are documented
        assert "/timeline/" in paths
        assert "/timeline/{event_id}" in paths
        
        # Check that the methods are documented
        timeline_path = paths["/timeline/"]
        timeline_id_path = paths["/timeline/{event_id}"]
        
        assert "post" in timeline_path
        assert "get" in timeline_path
        assert "get" in timeline_id_path
        assert "put" in timeline_id_path
        assert "delete" in timeline_id_path
        
        print("Timeline API endpoints are properly documented!")
        
    except Exception as e:
        pytest.fail(f"Failed to verify timeline API documentation: {e}")

def test_timeline_api_with_authentication():
    """Test timeline API endpoints with authentication"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token
        
        client = TestClient(app)
        
        # Create a valid token for testing
        token = create_access_token(data={"sub": "test-user-timeline-api"})
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Test POST /timeline/ (create timeline event) with authentication
        response = client.post("/timeline/", headers=auth_headers)
        assert response.status_code == 422  # Validation error since no data provided
        
        # Test GET /timeline/ (list timeline events) with authentication
        response = client.get("/timeline/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "events" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        
        # Test GET /timeline/{event_id} (get specific timeline event) with authentication
        event_id = str(uuid.uuid4())
        response = client.get(f"/timeline/{event_id}", headers=auth_headers)
        assert response.status_code == 404  # Not found since it doesn't exist
        
        # Test PUT /timeline/{event_id} (update timeline event) with authentication
        response = client.put(f"/timeline/{event_id}", headers=auth_headers)
        assert response.status_code == 422  # Validation error since no data provided
        
        # Test DELETE /timeline/{event_id} (delete timeline event) with authentication
        response = client.delete(f"/timeline/{event_id}", headers=auth_headers)
        assert response.status_code == 404  # Not found since it doesn't exist
        
        print("All timeline API endpoints work with authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test timeline API with authentication: {e}")

def test_timeline_api_without_authentication():
    """Test that timeline API endpoints require authentication"""
    try:
        from backend.api.main import app
        
        client = TestClient(app)
        
        # Test POST /timeline/ (create timeline event) without authentication
        response = client.post("/timeline/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /timeline/ (list timeline events) without authentication
        response = client.get("/timeline/")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test GET /timeline/{event_id} (get specific timeline event) without authentication
        event_id = str(uuid.uuid4())
        response = client.get(f"/timeline/{event_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test PUT /timeline/{event_id} (update timeline event) without authentication
        response = client.put(f"/timeline/{event_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        # Test DELETE /timeline/{event_id} (delete timeline event) without authentication
        response = client.delete(f"/timeline/{event_id}")
        assert response.status_code == 403  # Forbidden - authentication required
        
        print("All timeline API endpoints properly require authentication!")
        
    except Exception as e:
        pytest.fail(f"Failed to test timeline API without authentication: {e}")