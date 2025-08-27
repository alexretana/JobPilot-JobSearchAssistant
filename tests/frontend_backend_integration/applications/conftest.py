"""
Test data fixtures for job application integration tests.
"""

import pytest
from datetime import datetime, timedelta


@pytest.fixture
def test_job_application_data():
    """Provide test job application data for integration tests."""
    now = datetime.now()
    return {
        "user_profile_id": "test-user-id",
        "job_id": "test-job-id",
        "status": "applied",
        "applied_date": now.isoformat(),
        "resume_version": "v1.0",
        "cover_letter": "Dear Hiring Manager, I am excited to apply for this position...",
        "notes": "Submitted through company website on 2023-01-15",
        "follow_up_date": (now + timedelta(days=7)).isoformat(),
        "interview_scheduled": False
    }


@pytest.fixture
def test_job_application_update_data():
    """Provide test job application update data for integration tests."""
    return {
        "status": "interviewing",
        "response_date": datetime.now().isoformat(),
        "interview_scheduled": True,
        "notes": "Phone interview scheduled for next week"
    }


@pytest.fixture
def test_job_application_search_filters():
    """Provide test job application search filters for integration tests."""
    return {
        "status": "applied",
        "limit": 10,
        "offset": 0
    }