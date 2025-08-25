import pytest
import sys
import os
from datetime import datetime
from typing import List, Optional

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_user_profile_models_import():
    """Test that user profile models can be imported"""
    try:
        # This test should initially fail because we need to verify the models exist
        from backend.data.models import UserProfile, JobType, RemoteType
        # If we get here, the models exist
    except ImportError:
        pytest.fail("User profile models not found. Need to verify backend/data/models.py")

def test_user_profile_model():
    """Test UserProfile model creation"""
    try:
        from backend.data.models import UserProfile, JobType, RemoteType
        import uuid
        
        # Test creating a user profile
        user_id = str(uuid.uuid4())
        user_data = {
            "id": user_id,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-123-4567",
            "city": "San Francisco",
            "state": "CA",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "portfolio_url": "https://johndoe.com",
            "current_title": "Senior Software Engineer",
            "experience_years": 5,
            "education": "Master's in Computer Science",
            "bio": "Experienced software engineer passionate about building scalable applications",
            "preferred_locations": ["San Francisco, CA", "Remote"],
            "preferred_job_types": [JobType.FULL_TIME, JobType.CONTRACT],
            "preferred_remote_types": [RemoteType.REMOTE, RemoteType.HYBRID],
            "desired_salary_min": 120000,
            "desired_salary_max": 160000,
        }
        
        user = UserProfile(**user_data)
        assert str(user.id) == user_id
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.phone == "+1-555-123-4567"
        assert user.city == "San Francisco"
        assert user.state == "CA"
        assert user.linkedin_url == "https://linkedin.com/in/johndoe"
        assert user.portfolio_url == "https://johndoe.com"
        assert user.current_title == "Senior Software Engineer"
        assert user.experience_years == 5
        assert user.education == "Master's in Computer Science"
        assert user.bio == "Experienced software engineer passionate about building scalable applications"
        assert "San Francisco, CA" in user.preferred_locations
        assert JobType.FULL_TIME in user.preferred_job_types
        assert RemoteType.REMOTE in user.preferred_remote_types
        assert user.desired_salary_min == 120000
        assert user.desired_salary_max == 160000
        
    except ImportError:
        pytest.fail("User profile models not found. Need to verify backend/data/models.py")
    except Exception as e:
        pytest.fail(f"Failed to create UserProfile model: {e}")

def test_user_profile_defaults():
    """Test user profile model default values"""
    try:
        from backend.data.models import UserProfile
        import uuid
        
        # Test creating a user profile with minimal data
        user_id = str(uuid.uuid4())
        user_data = {
            "id": user_id,
            "email": "minimal@example.com",
        }
        
        user = UserProfile(**user_data)
        assert str(user.id) == user_id
        assert user.email == "minimal@example.com"
        assert user.preferred_locations == []  # Default empty list
        assert user.preferred_job_types == []  # Default empty list
        assert user.preferred_remote_types == []  # Default empty list
        
    except ImportError:
        pytest.fail("User profile models not found. Need to verify backend/data/models.py")
    except Exception as e:
        pytest.fail(f"Failed to test user profile defaults: {e}")

def test_user_profile_enums():
    """Test user profile enumeration values"""
    try:
        from backend.data.models import JobType, RemoteType
        
        # Test JobType enum
        assert JobType.FULL_TIME.value == "Full-time"
        assert JobType.PART_TIME.value == "Part-time"
        assert JobType.CONTRACT.value == "Contract"
        
        # Test RemoteType enum
        assert RemoteType.ON_SITE.value == "On-site"
        assert RemoteType.REMOTE.value == "Remote"
        assert RemoteType.HYBRID.value == "Hybrid"
        
    except ImportError:
        pytest.fail("User profile enums not found. Need to verify backend/data/models.py")
    except Exception as e:
        pytest.fail(f"Failed to test user profile enums: {e}")