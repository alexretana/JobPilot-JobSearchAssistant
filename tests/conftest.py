"""
Common test fixtures and configuration for JobPilot tests.
"""

import os
import sys
import tempfile
from datetime import datetime, date
from pathlib import Path
from typing import Generator
from uuid import uuid4

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

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


# =====================================
# Database Testing Fixtures
# =====================================

@pytest.fixture(scope="session")
def db_engine():
    """Create an in-memory SQLite database engine for testing."""
    from sqlalchemy import create_engine, event
    from backend.data.base import Base
    
    # Use in-memory SQLite database for fast testing
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,  # Set to True for SQL debugging
        connect_args={"check_same_thread": False},  # Allow multiple threads
    )
    
    # Enable foreign key constraints for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    yield engine
    
    # Cleanup
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a database session for each test."""
    from sqlalchemy.orm import sessionmaker
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def clean_db(db_session):
    """Ensure database is clean before each test."""
    from backend.data.base import Base
    
    # Clear all tables
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
    
    yield db_session


@pytest.fixture
def sample_company_db_data():
    """Sample company data optimized for database testing."""
    from backend.data.models import CompanySizeCategory
    
    return {
        "name": "TechCorp Inc",
        "normalized_name": "techcorp inc",
        "domain": "techcorp.com",
        "industry": "Technology",
        "size": "201-500 employees",
        "size_category": CompanySizeCategory.MEDIUM,
        "location": "San Francisco, CA",
        "headquarters_location": "San Francisco, CA",
        "founded_year": 2010,
        "website": "https://techcorp.com",
        "description": "A leading technology company specializing in innovative solutions",
        "values": ["Innovation", "Excellence", "Teamwork"],
        "benefits": ["Health Insurance", "401k", "Stock Options"],
    }


@pytest.fixture
def sample_job_db_data():
    """Sample job listing data optimized for database testing."""
    from backend.data.models import JobType, RemoteType, JobStatus, ExperienceLevel
    from datetime import datetime
    
    return {
        "title": "Senior Software Engineer",
        "location": "San Francisco, CA",
        "description": "Great opportunity for a senior engineer",
        "requirements": "5+ years experience with Python",
        "responsibilities": "Develop and maintain applications",
        "job_type": JobType.FULL_TIME,
        "remote_type": RemoteType.HYBRID,
        "experience_level": ExperienceLevel.SENIOR_LEVEL,
        "salary_min": 120000.0,
        "salary_max": 180000.0,
        "salary_currency": "USD",
        "skills_required": ["Python", "React", "PostgreSQL"],
        "skills_preferred": ["AWS", "Docker"],
        "education_required": "Bachelor's degree",
        "benefits": ["Health Insurance", "401k"],
        "job_url": "https://techcorp.com/jobs/123",
        "application_url": "https://techcorp.com/apply/123",
        "posted_date": datetime(2025, 1, 20, 9, 0, 0),
        "source": "company_website",
        "status": JobStatus.ACTIVE,
        "tech_stack": ["Python", "React", "PostgreSQL"],
    }


@pytest.fixture
def sample_user_db_data():
    """Sample user profile data optimized for database testing."""
    from backend.data.models import JobType, RemoteType
    
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
        "bio": "Experienced software engineer",
        "preferred_locations": ["San Francisco, CA", "Remote"],
        "preferred_job_types": ["Full-time"],
        "preferred_remote_types": ["Hybrid", "Remote"],
        "desired_salary_min": 100000.0,
        "desired_salary_max": 150000.0,
    }


@pytest.fixture(scope="session")
def database_engine():
    """Alias for db_engine to match test expectations."""
    from sqlalchemy import create_engine, event
    from backend.data.base import Base
    
    # Use in-memory SQLite database for fast testing
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,  # Set to True for SQL debugging
        connect_args={"check_same_thread": False},  # Allow multiple threads
    )
    
    # Enable foreign key constraints for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    yield engine
    
    # Cleanup
    engine.dispose()


# Custom markers for test organization
pytestmark = pytest.mark.unit
