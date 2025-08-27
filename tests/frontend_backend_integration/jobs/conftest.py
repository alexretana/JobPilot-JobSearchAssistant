"""
Test data fixtures for job integration tests.
"""

import pytest
from datetime import datetime, timedelta


@pytest.fixture
def test_job_data():
    """Provide test job data for integration tests."""
    return {
        "title": "Senior Software Engineer",
        "company": "TechCorp Inc",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "remote_type": "Hybrid",
        "experience_level": "Senior-level",
        "salary_min": 120000,
        "salary_max": 180000,
        "description": "We are looking for an experienced software engineer to join our team...",
        "requirements": "5+ years of Python experience, 3+ years of React experience",
        "responsibilities": "Develop and maintain web applications, collaborate with cross-functional teams",
        "benefits": ["Health Insurance", "401k", "Stock Options", "Flexible PTO"],
        "skills_required": ["Python", "React", "PostgreSQL", "Docker"],
        "skills_preferred": ["AWS", "Kubernetes", "Machine Learning"],
        "education_required": "Bachelor's degree in Computer Science or related field",
        "job_url": "https://techcorp.com/jobs/123",
        "application_url": "https://techcorp.com/apply/123",
        "posted_date": datetime.now().isoformat(),
        "source": "company_website",
        "status": "active"
    }


@pytest.fixture
def test_job_search_filters():
    """Provide test job search filters for integration tests."""
    return {
        "query": "software engineer",
        "job_type": "Full-time",
        "remote_type": "Remote",
        "experience_level": "Mid-level",
        "salary_min": 100000,
        "salary_max": 150000,
        "location": "San Francisco, CA",
        "company": "Tech Corp",
        "posted_after": (datetime.now() - timedelta(days=30)).isoformat(),
        "posted_before": datetime.now().isoformat()
    }


@pytest.fixture
def test_job_update_data():
    """Provide test job update data for integration tests."""
    return {
        "title": "Lead Software Engineer",
        "salary_min": 130000,
        "salary_max": 190000,
        "status": "inactive"
    }