"""
Test data fixtures for timeline integration tests.
"""

import pytest
from datetime import datetime


@pytest.fixture
def test_timeline_event_data():
    """Provide test timeline event data for integration tests."""
    return {
        "user_profile_id": "test-user-id",
        "event_type": "job_saved",
        "title": "Software Engineer Position Saved",
        "description": "Saved a Software Engineer position at TechCorp Inc",
        "timestamp": datetime.now().isoformat(),
        "related_job_id": "test-job-id",
        "related_application_id": "test-application-id",
        "metadata": {
            "job_title": "Software Engineer",
            "company_name": "TechCorp Inc",
            "location": "San Francisco, CA",
            "salary_range": "$100k - $150k"
        }
    }


@pytest.fixture
def test_timeline_event_update_data():
    """Provide test timeline event update data for integration tests."""
    return {
        "title": "Senior Software Engineer Position Saved",
        "description": "Saved a Senior Software Engineer position at TechCorp Inc",
        "metadata": {
            "job_title": "Senior Software Engineer",
            "company_name": "TechCorp Inc",
            "location": "San Francisco, CA",
            "salary_range": "$120k - $180k"
        }
    }


@pytest.fixture
def test_custom_event_data():
    """Provide test custom event data for integration tests."""
    return {
        "title": "Networking Event Attendance",
        "description": "Attended Tech Networking Meetup",
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "event_name": "Tech Networking Meetup",
            "location": "San Francisco, CA",
            "attendees": 50,
            "connections_made": 5
        }
    }


@pytest.fixture
def test_timeline_search_filters():
    """Provide test timeline search filters for integration tests."""
    return {
        "event_types": ["job_saved", "application_submitted"],
        "limit": 20,
        "offset": 0,
        "job_id": "test-job-id"
    }