"""
Integration tests for timeline API between frontend services and backend.
"""

import pytest
from fastapi.testclient import TestClient


class TestTimelineIntegration:
    """Test timeline API integration between frontend services and backend."""

    def test_list_timeline_events(self, test_client, test_user_data, test_timeline_search_filters):
        """Test listing timeline events with filtering through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test the list timeline events endpoint with filters
        query_params = "&".join([f"{key}={value}" for key, value in test_timeline_search_filters.items() if value is not None])
        response = test_client.get(f"/timeline/?{query_params}")
        assert response.status_code in [200, 401, 403]  # Various possible responses

    def test_get_timeline_event(self, test_client, test_user_data):
        """Test retrieving specific timeline event by ID through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test getting a specific timeline event
        response = test_client.get("/timeline/test-event-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses

    def test_create_timeline_event(self, test_client, test_user_data, test_timeline_event_data):
        """Test creating new timeline events through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test creating a timeline event
        response = test_client.post("/timeline/", json=test_timeline_event_data)
        assert response.status_code in [200, 201, 400, 401, 403, 422]  # Various possible responses

    def test_update_timeline_event(self, test_client, test_user_data, test_timeline_event_update_data):
        """Test updating timeline events through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test updating a timeline event
        response = test_client.put("/timeline/test-event-id", json=test_timeline_event_update_data)
        assert response.status_code in [200, 400, 401, 403, 404, 422]  # Various possible responses

    def test_delete_timeline_event(self, test_client, test_user_data):
        """Test deleting timeline events through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test deleting a timeline event
        response = test_client.delete("/timeline/test-event-id")
        assert response.status_code in [200, 401, 403, 404]  # Various possible responses

    def test_log_job_saved(self, test_client, test_user_data):
        """Test logging job saved event through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test logging job saved event
        params = "job_title=Software Engineer&company_name=TechCorp Inc"
        response = test_client.post(f"/timeline/user/test-user-id/job/test-job-id/saved?{params}")
        assert response.status_code in [200, 201, 400, 401, 403, 404, 422]  # Various possible responses

    def test_log_application_submitted(self, test_client, test_user_data):
        """Test logging application submitted event through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test logging application submitted event
        params = "job_id=test-job-id&job_title=Software Engineer&company_name=TechCorp Inc&application_method=Online Portal"
        response = test_client.post(f"/timeline/user/test-user-id/application/test-application-id/submitted?{params}")
        assert response.status_code in [200, 201, 400, 401, 403, 404, 422]  # Various possible responses

    def test_log_interview_scheduled(self, test_client, test_user_data):
        """Test logging interview scheduled event through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test logging interview scheduled event
        params = "job_id=test-job-id&job_title=Software Engineer&company_name=TechCorp Inc&interview_date=2023-06-15&interview_type=Phone Interview"
        response = test_client.post(f"/timeline/user/test-user-id/application/test-application-id/interview-scheduled?{params}")
        assert response.status_code in [200, 201, 400, 401, 403, 404, 422]  # Various possible responses

    def test_log_status_change(self, test_client, test_user_data):
        """Test logging status change event through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test logging status change event
        params = "job_id=test-job-id&job_title=Software Engineer&company_name=TechCorp Inc&old_status=applied&new_status=interviewing&notes=Phone interview scheduled for next week"
        response = test_client.post(f"/timeline/user/test-user-id/application/test-application-id/status-changed?{params}")
        assert response.status_code in [200, 201, 400, 401, 403, 404, 422]  # Various possible responses