"""
Test data fixtures for user profile integration tests.
"""

import pytest


@pytest.fixture
def test_user_profile_data():
    """Provide test user profile data for integration tests."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-123-4567",
        "city": "San Francisco",
        "state": "CA",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "portfolio_url": "https://johndoe.dev",
        "current_title": "Software Engineer",
        "experience_years": 5,
        "skills": ["Python", "JavaScript", "React", "SQL"],
        "education": "BS Computer Science",
        "bio": "Experienced software engineer passionate about building great products",
        "preferred_locations": ["San Francisco, CA", "Remote"],
        "preferred_job_types": ["Full-time"],
        "preferred_remote_types": ["Hybrid", "Remote"],
        "desired_salary_min": 100000.0,
        "desired_salary_max": 150000.0
    }


@pytest.fixture
def test_user_profile_update_data():
    """Provide test user profile update data for integration tests."""
    return {
        "first_name": "Jane",
        "current_title": "Senior Software Engineer",
        "experience_years": 7
    }