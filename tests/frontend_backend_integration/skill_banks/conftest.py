"""
Test data fixtures for skill bank integration tests.
"""

import pytest
from datetime import datetime


@pytest.fixture
def test_skill_bank_data():
    """Provide test skill bank data for integration tests."""
    return {
        "user_id": "test-user-id",
        "initial_skills": [
            {
                "name": "Python",
                "level": "Expert",
                "category": "Programming",
                "subcategory": "Backend",
                "years_experience": 5,
                "proficiency_score": 95,
                "description": "Full-stack development with Python frameworks",
                "keywords": ["Django", "FastAPI", "Flask"],
                "is_featured": True,
                "display_order": 1
            },
            {
                "name": "JavaScript",
                "level": "Advanced",
                "category": "Programming",
                "subcategory": "Frontend",
                "years_experience": 4,
                "proficiency_score": 85,
                "description": "Modern JavaScript development",
                "keywords": ["React", "Vue.js", "Node.js"],
                "is_featured": True,
                "display_order": 2
            }
        ],
        "default_summary": "Experienced full-stack developer with expertise in Python and JavaScript technologies."
    }


@pytest.fixture
def test_skill_data():
    """Provide test skill data for integration tests."""
    return {
        "name": "TypeScript",
        "level": "Intermediate",
        "category": "Programming",
        "subcategory": "Frontend",
        "years_experience": 2,
        "proficiency_score": 75,
        "description": "Strong typing for JavaScript applications",
        "keywords": ["Angular", "React", "Node.js"],
        "is_featured": False,
        "display_order": 3
    }


@pytest.fixture
def test_skill_update_data():
    """Provide test skill update data for integration tests."""
    return {
        "level": "Advanced",
        "years_experience": 3,
        "proficiency_score": 85,
        "is_featured": True
    }


@pytest.fixture
def test_experience_data():
    """Provide test experience data for integration tests."""
    return {
        "company": "TechCorp Inc",
        "position": "Senior Software Engineer",
        "location": "San Francisco, CA",
        "start_date": "2020-01-01",
        "end_date": None,
        "is_current": True,
        "default_description": "Lead development of cloud-based applications",
        "default_achievements": [
            "Increased system performance by 40%",
            "Led team of 5 developers"
        ],
        "skills_used": ["Python", "JavaScript", "AWS"],
        "technologies": ["Django", "React", "Docker", "Kubernetes"]
    }


@pytest.fixture
def test_experience_update_data():
    """Provide test experience update data for integration tests."""
    return {
        "position": "Lead Software Engineer",
        "end_date": datetime.now().strftime("%Y-%m-%d"),
        "is_current": False,
        "default_achievements": [
            "Increased system performance by 40%",
            "Led team of 5 developers",
            "Implemented microservices architecture"
        ]
    }