"""
Test data fixtures for job deduplication integration tests.
"""

import pytest


@pytest.fixture
def test_job_deduplication_data():
    """Provide test job deduplication data for integration tests."""
    return {
        "job_id_1": "job-123",
        "job_id_2": "job-456"
    }


@pytest.fixture
def test_batch_deduplication_data():
    """Provide test batch deduplication data for integration tests."""
    return {
        "job_ids": ["job-123", "job-456", "job-789", "job-101"],
        "confidence_threshold": 0.8
    }


@pytest.fixture
def test_job_for_deduplication():
    """Provide test job data for deduplication for integration tests."""
    return {
        "title": "Senior Python Developer",
        "company": "Tech Corp",
        "description": "Looking for an experienced Python developer with Django and FastAPI experience",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "remote_type": "Hybrid",
        "experience_level": "Senior-level",
        "salary_min": 120000,
        "salary_max": 160000
    }


@pytest.fixture
def test_batch_jobs_for_deduplication():
    """Provide test batch jobs data for deduplication for integration tests."""
    return [
        {
            "id": "job-123",
            "title": "Senior Python Developer",
            "company": "Tech Corp",
            "description": "Looking for an experienced Python developer with Django and FastAPI experience",
            "location": "San Francisco, CA",
            "job_type": "Full-time",
            "remote_type": "Hybrid",
            "experience_level": "Senior-level",
            "salary_min": 120000,
            "salary_max": 160000
        },
        {
            "id": "job-456",
            "title": "Senior Python Engineer",
            "company": "Tech Corp",
            "description": "Seeking experienced Python engineer with Django and FastAPI expertise",
            "location": "San Francisco, CA",
            "job_type": "Full-time",
            "remote_type": "Hybrid",
            "experience_level": "Senior-level",
            "salary_min": 125000,
            "salary_max": 165000
        }
    ]