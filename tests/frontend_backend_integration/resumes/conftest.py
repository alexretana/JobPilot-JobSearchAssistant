"""
Test data fixtures for resume integration tests.
"""

import pytest
from datetime import datetime


@pytest.fixture
def test_resume_data():
    """Provide test resume data for integration tests."""
    return {
        "user_id": "test-user-id",
        "title": "Senior Software Engineer Resume",
        "resume_type": "professional",
        "status": "active",
        "contact_info": {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-123-4567",
            "location": "San Francisco, CA",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "github_url": "https://github.com/johndoe"
        },
        "summary": "Experienced software engineer with 5+ years of expertise in Python, JavaScript, and cloud technologies.",
        "work_experience": [
            {
                "company": "TechCorp Inc",
                "position": "Senior Software Engineer",
                "location": "San Francisco, CA",
                "start_date": "2020-01-01",
                "end_date": None,
                "is_current": True,
                "description": "Lead development of cloud-based applications",
                "achievements": [
                    "Increased system performance by 40%",
                    "Led team of 5 developers"
                ]
            }
        ],
        "education": [
            {
                "institution": "University of California",
                "degree": "BS Computer Science",
                "field_of_study": "Computer Science",
                "location": "Berkeley, CA",
                "graduation_date": "2018-05-01",
                "gpa": "3.8"
            }
        ],
        "skills": [
            {"name": "Python", "category": "Programming", "proficiency_level": "Expert"},
            {"name": "JavaScript", "category": "Programming", "proficiency_level": "Advanced"},
            {"name": "React", "category": "Frontend", "proficiency_level": "Advanced"}
        ],
        "projects": [
            {
                "name": "JobPilot Platform",
                "description": "AI-powered job search platform",
                "technologies": ["Python", "FastAPI", "React"],
                "url": "https://github.com/jobpilot",
                "start_date": "2022-01-01",
                "end_date": "2022-12-01"
            }
        ],
        "certifications": [
            {
                "name": "AWS Certified Developer",
                "issuer": "Amazon Web Services",
                "date_earned": "2021-06-01",
                "credential_id": "AWS-123456"
            }
        ],
        "version": 1
    }


@pytest.fixture
def test_resume_update_data():
    """Provide test resume update data for integration tests."""
    return {
        "title": "Lead Software Engineer Resume",
        "summary": "Lead software engineer with 7+ years of expertise in full-stack development and team leadership.",
        "status": "published"
    }


@pytest.fixture
def test_resume_search_filters():
    """Provide test resume search filters for integration tests."""
    return {
        "status": "active",
        "resume_type": "professional",
        "limit": 10,
        "offset": 0
    }