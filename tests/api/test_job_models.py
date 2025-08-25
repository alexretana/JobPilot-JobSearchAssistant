import pytest
import sys
import os
from datetime import datetime
from typing import List, Optional

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_job_listing_models_import():
    """Test that job listing models can be imported"""
    try:
        # This test should initially fail because we haven't created the job models yet
        from backend.data.models import JobListing, JobListingBase, JobType, RemoteType, ExperienceLevel
        # If we get here, the models exist
    except ImportError:
        pytest.fail("Job listing models not found. Need to verify backend/data/models.py")

def test_job_listing_base_model():
    """Test JobListingBase model creation"""
    try:
        from backend.data.models import JobListingBase, JobType, RemoteType, ExperienceLevel
        
        # Test creating a basic job listing
        job_data = {
            "title": "Software Engineer",
            "location": "San Francisco, CA",
            "description": "Exciting opportunity for a software engineer",
            "requirements": "Python, FastAPI, SQL",
            "responsibilities": "Develop and maintain web applications",
            "job_type": JobType.FULL_TIME,
            "remote_type": RemoteType.HYBRID,
            "experience_level": ExperienceLevel.MID_LEVEL,
            "salary_min": 100000,
            "salary_max": 150000,
            "salary_currency": "USD",
            "skills_required": ["Python", "FastAPI", "SQL"],
            "skills_preferred": ["Docker", "AWS"],
            "education_required": "Bachelor's degree in Computer Science",
            "benefits": ["Health insurance", "401k", "PTO"],
            "job_url": "https://example.com/jobs/123",
            "application_url": "https://example.com/apply/123",
        }
        
        job = JobListingBase(**job_data)
        assert job.title == "Software Engineer"
        assert job.location == "San Francisco, CA"
        assert job.job_type == JobType.FULL_TIME
        assert job.remote_type == RemoteType.HYBRID
        assert job.experience_level == ExperienceLevel.MID_LEVEL
        assert job.salary_min == 100000
        assert job.salary_max == 150000
        assert job.salary_currency == "USD"
        assert "Python" in job.skills_required
        assert "Docker" in job.skills_preferred
        assert "Health insurance" in job.benefits
        
    except ImportError:
        pytest.fail("Job listing models not found. Need to verify backend/data/models.py")
    except Exception as e:
        pytest.fail(f"Failed to create JobListingBase model: {e}")

def test_job_listing_model():
    """Test JobListing model creation"""
    try:
        from backend.data.models import JobListing, JobType, RemoteType, ExperienceLevel
        import uuid
        
        # Test creating a job listing with ID
        job_id = str(uuid.uuid4())
        job_data = {
            "id": job_id,
            "title": "Senior Software Engineer",
            "location": "Remote",
            "description": "Lead development of our platform",
            "requirements": "10+ years Python, Leadership experience",
            "responsibilities": "Lead team, architect solutions",
            "job_type": JobType.FULL_TIME,
            "remote_type": RemoteType.REMOTE,
            "experience_level": ExperienceLevel.SENIOR_LEVEL,
            "salary_min": 150000,
            "salary_max": 200000,
            "salary_currency": "USD",
            "skills_required": ["Python", "Leadership", "System Design"],
            "skills_preferred": ["Machine Learning", "Cloud Architecture"],
            "education_required": "Master's degree preferred",
            "benefits": ["Unlimited PTO", "Stock options", "Health insurance"],
            "job_url": "https://example.com/jobs/456",
            "application_url": "https://example.com/apply/456",
            "status": "active",
        }
        
        job = JobListing(**job_data)
        print(f"Created job with ID: {job.id}")
        print(f"Expected ID: {job_id}")
        assert str(job.id) == job_id  # Convert UUID to string for comparison
        assert job.title == "Senior Software Engineer"
        assert job.location == "Remote"
        assert job.job_type == JobType.FULL_TIME
        assert job.remote_type == RemoteType.REMOTE
        assert job.experience_level == ExperienceLevel.SENIOR_LEVEL
        assert job.salary_min == 150000
        assert job.salary_max == 200000
        assert job.salary_currency == "USD"
        assert "Python" in job.skills_required
        assert "Machine Learning" in job.skills_preferred
        assert "Unlimited PTO" in job.benefits
        assert job.status == "active"
        
    except ImportError:
        pytest.fail("Job listing models not found. Need to verify backend/data/models.py")
    except Exception as e:
        pytest.fail(f"Failed to create JobListing model: {e}")

def test_job_enums():
    """Test job enumeration values"""
    try:
        from backend.data.models import JobType, RemoteType, ExperienceLevel, JobStatus
        
        # Test JobType enum
        assert JobType.FULL_TIME.value == "Full-time"
        assert JobType.PART_TIME.value == "Part-time"
        assert JobType.CONTRACT.value == "Contract"
        
        # Test RemoteType enum
        assert RemoteType.ON_SITE.value == "On-site"
        assert RemoteType.REMOTE.value == "Remote"
        assert RemoteType.HYBRID.value == "Hybrid"
        
        # Test ExperienceLevel enum
        assert ExperienceLevel.ENTRY_LEVEL.value == "entry_level"
        assert ExperienceLevel.MID_LEVEL.value == "mid_level"
        assert ExperienceLevel.SENIOR_LEVEL.value == "senior_level"
        
        # Test JobStatus enum
        assert JobStatus.ACTIVE.value == "active"
        assert JobStatus.INACTIVE.value == "inactive"
        assert JobStatus.FILLED.value == "filled"
        
    except ImportError:
        pytest.fail("Job enums not found. Need to verify backend/data/models.py")
    except Exception as e:
        pytest.fail(f"Failed to test job enums: {e}")

def test_job_model_defaults():
    """Test job model default values"""
    try:
        from backend.data.models import JobListingBase
        
        # Test creating a job with minimal data
        job_data = {
            "title": "Junior Developer",
        }
        
        job = JobListingBase(**job_data)
        assert job.title == "Junior Developer"
        assert job.skills_required == []  # Default empty list
        assert job.skills_preferred == []  # Default empty list
        assert job.benefits == []  # Default empty list
        assert job.salary_currency == "USD"  # Default currency
        
    except ImportError:
        pytest.fail("Job listing models not found. Need to verify backend/data/models.py")
    except Exception as e:
        pytest.fail(f"Failed to test job model defaults: {e}")