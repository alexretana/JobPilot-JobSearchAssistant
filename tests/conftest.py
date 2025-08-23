"""
Common test fixtures and configuration for JobPilot tests.
"""

import os
import tempfile
from datetime import datetime, date
from pathlib import Path
from typing import Generator
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test environment variables
os.environ["TEST_MODE"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Provide a test database URL for SQLite in-memory database."""
    return "sqlite:///:memory:"


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_datetime() -> datetime:
    """Provide a consistent datetime for testing."""
    return datetime(2025, 1, 23, 12, 0, 0)


@pytest.fixture
def sample_date() -> date:
    """Provide a consistent date for testing."""
    return date(2025, 1, 23)


@pytest.fixture
def sample_uuid() -> str:
    """Provide a consistent UUID for testing."""
    return str(uuid4())


# Common test data factories
@pytest.fixture
def valid_email() -> str:
    """Provide a valid email for testing."""
    return "test@example.com"


@pytest.fixture
def invalid_email() -> str:
    """Provide an invalid email for testing."""
    return "not-an-email"


@pytest.fixture
def sample_job_data() -> dict:
    """Provide sample job listing data for testing."""
    return {
        "title": "Senior Software Engineer",
        "description": "We are looking for an experienced software engineer...",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "remote_type": "Hybrid",
        "experience_level": "senior_level",
        "salary_min": 120000.0,
        "salary_max": 180000.0,
        "salary_currency": "USD",
        "skills_required": ["Python", "JavaScript", "React"],
        "skills_preferred": ["AWS", "Docker", "Kubernetes"],
        "benefits": ["Health Insurance", "401k", "Flexible PTO"],
        "requirements": "5+ years of software development experience",
        "responsibilities": "Develop and maintain web applications",
        "job_url": "https://example.com/jobs/123",
        "application_url": "https://example.com/apply/123",
        "posted_date": datetime(2025, 1, 20),
    }


@pytest.fixture
def sample_user_data() -> dict:
    """Provide sample user profile data for testing."""
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
        "education": "BS Computer Science",
        "bio": "Experienced software engineer passionate about building great products",
        "preferred_locations": ["San Francisco, CA", "Remote"],
        "preferred_job_types": ["Full-time"],
        "preferred_remote_types": ["Hybrid", "Remote"],
        "desired_salary_min": 100000.0,
        "desired_salary_max": 150000.0,
    }


@pytest.fixture
def sample_company_data() -> dict:
    """Provide sample company data for testing."""
    return {
        "name": "TechCorp Inc",
        "industry": "Technology",
        "size": "201-500 employees",
        "location": "San Francisco, CA",
        "website": "https://techcorp.com",
        "description": "A leading technology company specializing in innovative solutions",
    }


@pytest.fixture
def sample_job_application_data() -> dict:
    """Provide sample job application data for testing."""
    return {
        "status": "applied",
        "applied_date": datetime(2025, 1, 22),
        "resume_version": "v1.2",
        "cover_letter": "Dear Hiring Manager, I am very interested...",
        "notes": "Applied through company website",
    }


# Database fixtures will be added later when we implement database testing
@pytest.fixture
def db_session():
    """Database session fixture - will be implemented in database tests."""
    # This will be implemented when we get to database testing
    pass


# Custom markers for test organization
pytestmark = pytest.mark.unit
