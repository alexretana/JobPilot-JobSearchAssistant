"""
Unit tests for UserProfile Pydantic model validation.

Tests field constraints, enum validation, email validation, and edge cases
for the UserProfile model.
"""

import pytest
from datetime import datetime
from uuid import uuid4, UUID
from pydantic import ValidationError

from backend.data.models import (
    UserProfile,
    JobType,
    RemoteType,
)


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestUserProfile:
    """Test UserProfile model validation."""

    def test_minimal_valid_user_profile(self):
        """Test creating UserProfile with no required fields."""
        user = UserProfile()
        
        # Test that auto-generated fields exist
        assert isinstance(user.id, UUID)
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
        
        # Test default values
        assert user.first_name is None
        assert user.last_name is None
        assert user.email is None
        assert user.phone is None
        assert user.city is None
        assert user.state is None
        assert user.linkedin_url is None
        assert user.portfolio_url is None
        assert user.current_title is None
        assert user.experience_years is None
        assert user.education is None
        assert user.bio is None
        assert user.preferred_locations == []
        assert user.preferred_job_types == []
        assert user.preferred_remote_types == []
        assert user.desired_salary_min is None
        assert user.desired_salary_max is None

    def test_user_profile_with_all_fields(self, sample_user_data):
        """Test creating UserProfile with all fields populated."""
        user = UserProfile(**sample_user_data)
        
        # Verify all fields are set correctly
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.phone == "+1-555-123-4567"
        assert user.city == "San Francisco"
        assert user.state == "CA"
        assert user.linkedin_url == "https://linkedin.com/in/johndoe"
        assert user.portfolio_url == "https://johndoe.dev"
        assert user.current_title == "Software Engineer"
        assert user.experience_years == 5
        assert user.education == "BS Computer Science"
        assert user.bio == "Experienced software engineer passionate about building great products"
        assert user.preferred_locations == ["San Francisco, CA", "Remote"]
        assert user.preferred_job_types == ["Full-time"]
        assert user.preferred_remote_types == ["Hybrid", "Remote"]
        assert user.desired_salary_min == 100000.0
        assert user.desired_salary_max == 150000.0

    def test_email_validation(self, valid_email, invalid_email):
        """Test email field validation."""
        # Valid email
        user = UserProfile(email=valid_email)
        assert user.email == valid_email
        
        # Invalid email should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            UserProfile(email=invalid_email)
        
        assert "email" in str(exc_info.value)
        
        # None email should be allowed
        user = UserProfile(email=None)
        assert user.email is None
        
        # Empty string should raise ValidationError for email
        with pytest.raises(ValidationError) as exc_info:
            UserProfile(email="")
        assert "email" in str(exc_info.value)

    def test_name_field_validation(self):
        """Test name field validation."""
        # Valid names
        user = UserProfile(
            first_name="John",
            last_name="Doe"
        )
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        
        # Empty strings should be allowed
        user = UserProfile(
            first_name="",
            last_name=""
        )
        assert user.first_name == ""
        assert user.last_name == ""
        
        # Unicode names
        user = UserProfile(
            first_name="José",
            last_name="García-López"
        )
        assert user.first_name == "José"
        assert user.last_name == "García-López"

    def test_experience_years_validation(self):
        """Test experience years validation."""
        # Valid positive integers
        for years in [0, 1, 5, 10, 25, 50]:
            user = UserProfile(experience_years=years)
            assert user.experience_years == years
        
        # Negative years should be allowed (validation at business logic level)
        user = UserProfile(experience_years=-1)
        assert user.experience_years == -1
        
        # Large numbers should be allowed
        user = UserProfile(experience_years=100)
        assert user.experience_years == 100
        
        # Non-integer should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            UserProfile(experience_years=5.5)
        assert "experience_years" in str(exc_info.value)

    def test_salary_field_validation(self):
        """Test salary field validation."""
        # Valid salary ranges
        user = UserProfile(
            desired_salary_min=50000.0,
            desired_salary_max=100000.0,
        )
        
        assert user.desired_salary_min == 50000.0
        assert user.desired_salary_max == 100000.0
        
        # Test with integer values (should be converted to float)
        user = UserProfile(
            desired_salary_min=50000,
            desired_salary_max=100000,
        )
        
        assert isinstance(user.desired_salary_min, float)
        assert isinstance(user.desired_salary_max, float)
        
        # Negative salaries should be allowed (for validation at business logic level)
        user = UserProfile(desired_salary_min=-1000.0)
        assert user.desired_salary_min == -1000.0
        
        # Very large salaries
        user = UserProfile(desired_salary_max=10000000.0)
        assert user.desired_salary_max == 10000000.0

    def test_job_preference_enum_validation(self):
        """Test job preference enum fields validation."""
        # Valid enum values
        user = UserProfile(
            preferred_job_types=[JobType.FULL_TIME, JobType.PART_TIME],
            preferred_remote_types=[RemoteType.REMOTE, RemoteType.HYBRID],
        )
        
        assert user.preferred_job_types == [JobType.FULL_TIME, JobType.PART_TIME]
        assert user.preferred_remote_types == [RemoteType.REMOTE, RemoteType.HYBRID]
        
        # Empty lists should work
        user = UserProfile(
            preferred_job_types=[],
            preferred_remote_types=[],
        )
        assert user.preferred_job_types == []
        assert user.preferred_remote_types == []
        
        # Invalid enum values should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            UserProfile(preferred_job_types=["invalid_type"])
        
        assert "preferred_job_types" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            UserProfile(preferred_remote_types=["invalid_remote"])
        
        assert "preferred_remote_types" in str(exc_info.value)

    def test_preferred_locations_validation(self):
        """Test preferred locations list validation."""
        # Valid location lists
        locations = ["San Francisco, CA", "New York, NY", "Remote", "Austin, TX"]
        user = UserProfile(preferred_locations=locations)
        assert user.preferred_locations == locations
        
        # Empty list
        user = UserProfile(preferred_locations=[])
        assert user.preferred_locations == []
        
        # Single location
        user = UserProfile(preferred_locations=["Remote"])
        assert user.preferred_locations == ["Remote"]
        
        # Unicode locations
        user = UserProfile(preferred_locations=["São Paulo, Brasil", "München, Germany"])
        assert "São Paulo, Brasil" in user.preferred_locations
        assert "München, Germany" in user.preferred_locations

    def test_url_field_validation(self):
        """Test URL field validation."""
        # Valid URLs
        user = UserProfile(
            linkedin_url="https://linkedin.com/in/johndoe",
            portfolio_url="https://johndoe.dev",
        )
        
        assert user.linkedin_url == "https://linkedin.com/in/johndoe"
        assert user.portfolio_url == "https://johndoe.dev"
        
        # Different URL formats
        user = UserProfile(
            linkedin_url="http://www.linkedin.com/in/johndoe/",
            portfolio_url="https://github.com/johndoe",
        )
        
        assert user.linkedin_url == "http://www.linkedin.com/in/johndoe/"
        assert user.portfolio_url == "https://github.com/johndoe"
        
        # Note: Pydantic doesn't validate URL format by default for str fields
        # This would need custom validation if strict URL validation is required

    def test_phone_field_validation(self):
        """Test phone field validation."""
        # Various phone formats
        phone_formats = [
            "+1-555-123-4567",
            "+1 (555) 123-4567",
            "555-123-4567",
            "(555) 123-4567",
            "5551234567",
            "+44 20 7123 4567",  # International
        ]
        
        for phone in phone_formats:
            user = UserProfile(phone=phone)
            assert user.phone == phone

    def test_uuid_field_validation(self):
        """Test UUID field validation."""
        # Valid UUID
        user_id = uuid4()
        user = UserProfile(id=user_id)
        assert user.id == user_id
        
        # Test UUID string conversion
        user = UserProfile(id=str(user_id))
        assert user.id == user_id
        assert isinstance(user.id, UUID)

    def test_datetime_defaults(self):
        """Test that datetime fields have proper default values."""
        user1 = UserProfile()
        user2 = UserProfile()
        
        # Both should have datetime values
        assert isinstance(user1.created_at, datetime)
        assert isinstance(user1.updated_at, datetime)
        assert isinstance(user2.created_at, datetime)
        assert isinstance(user2.updated_at, datetime)
        
        # They should be different (created at different times)
        assert user1.id != user2.id  # At minimum, IDs should be different

    def test_user_profile_config(self):
        """Test that the Config class is properly set."""
        user = UserProfile()
        
        # Test model config is properly set (Pydantic v2 style)
        model_config = getattr(user.__class__, 'model_config', None)
        if model_config:
            # Pydantic v2 style - model_config is a dictionary
            if isinstance(model_config, dict):
                assert model_config.get('from_attributes', False) is True
            else:
                # If it's an object
                assert getattr(model_config, 'from_attributes', False) is True
        else:
            # Fallback: test that the model can be created from dict (basic functionality)
            test_dict = {"first_name": "Test", "last_name": "User"}
            test_user = UserProfile(**test_dict)
            assert test_user.first_name == "Test"


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestUserProfileEdgeCases:
    """Test edge cases and error conditions for UserProfile model."""

    def test_extremely_long_strings(self):
        """Test handling of extremely long string values."""
        long_string = "x" * 10000
        
        # Should not raise validation errors (length constraints at business logic level)
        user = UserProfile(
            first_name=long_string,
            last_name=long_string,
            bio=long_string,
            education=long_string,
            current_title=long_string,
        )
        
        assert len(user.first_name) == 10000
        assert len(user.last_name) == 10000
        assert len(user.bio) == 10000
        assert len(user.education) == 10000
        assert len(user.current_title) == 10000

    def test_unicode_and_special_characters(self):
        """Test handling of Unicode and special characters."""
        user = UserProfile(
            first_name="José María",
            last_name="García-López O'Connor",
            bio="Software engineer with café ☕ experience in São Paulo 🇧🇷",
            city="München",
            state="Bayern",
            education="Master's in Informática & AI 🤖",
        )
        
        assert "José María" == user.first_name
        assert "García-López O'Connor" == user.last_name
        assert "☕" in user.bio
        assert "🇧🇷" in user.bio
        assert "München" == user.city
        assert "🤖" in user.education

    def test_large_numeric_values(self):
        """Test handling of large numeric values."""
        user = UserProfile(
            experience_years=999999,
            desired_salary_min=1.0,  # Very small
            desired_salary_max=999999999.99,  # Very large
        )
        
        assert user.experience_years == 999999
        assert user.desired_salary_min == 1.0
        assert user.desired_salary_max == 999999999.99

    def test_very_large_preference_lists(self):
        """Test handling of very large preference lists."""
        large_locations_list = [f"City_{i}, State_{i}" for i in range(1000)]
        all_job_types = list(JobType)
        all_remote_types = list(RemoteType)
        
        user = UserProfile(
            preferred_locations=large_locations_list,
            preferred_job_types=all_job_types * 100,  # Duplicates allowed
            preferred_remote_types=all_remote_types * 50,
        )
        
        assert len(user.preferred_locations) == 1000
        assert len(user.preferred_job_types) == len(JobType) * 100
        assert len(user.preferred_remote_types) == len(RemoteType) * 50

    def test_boundary_experience_years(self):
        """Test boundary values for experience years."""
        # Test zero experience
        user = UserProfile(experience_years=0)
        assert user.experience_years == 0
        
        # Test very high experience
        user = UserProfile(experience_years=70)  # 70 years of experience
        assert user.experience_years == 70
        
        # Test negative experience (should be allowed, validation at business logic)
        user = UserProfile(experience_years=-5)
        assert user.experience_years == -5

    def test_boundary_salary_values(self):
        """Test boundary values for salary fields."""
        # Test zero salaries
        user = UserProfile(
            desired_salary_min=0.0,
            desired_salary_max=0.0,
        )
        assert user.desired_salary_min == 0.0
        assert user.desired_salary_max == 0.0
        
        # Test very small values
        user = UserProfile(
            desired_salary_min=0.01,
            desired_salary_max=0.99,
        )
        assert user.desired_salary_min == 0.01
        assert user.desired_salary_max == 0.99
        
        # Test very large values
        user = UserProfile(
            desired_salary_min=1000000000.0,  # 1 billion
            desired_salary_max=9999999999.99,  # Almost 10 billion
        )
        assert user.desired_salary_min == 1000000000.0
        assert user.desired_salary_max == 9999999999.99

    def test_empty_string_handling(self):
        """Test handling of empty strings."""
        user = UserProfile(
            first_name="",
            last_name="",
            phone="",
            city="",
            state="",
            linkedin_url="",
            portfolio_url="",
            current_title="",
            education="",
            bio="",
            preferred_locations=[""],  # Empty string in list
        )
        
        # Empty strings should be preserved
        assert user.first_name == ""
        assert user.last_name == ""
        assert user.phone == ""
        assert user.city == ""
        assert user.state == ""
        assert user.linkedin_url == ""
        assert user.portfolio_url == ""
        assert user.current_title == ""
        assert user.education == ""
        assert user.bio == ""
        assert user.preferred_locations == [""]


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestUserProfileSerialization:
    """Test UserProfile model serialization and deserialization."""

    def test_user_profile_to_dict(self, sample_user_data):
        """Test converting UserProfile to dictionary."""
        user = UserProfile(**sample_user_data)
        
        # Use model_dump for Pydantic v2
        user_dict = user.model_dump() if hasattr(user, 'model_dump') else user.dict()
        
        assert isinstance(user_dict, dict)
        assert user_dict["first_name"] == "John"
        assert user_dict["last_name"] == "Doe"
        assert user_dict["email"] == "john.doe@example.com"
        assert user_dict["experience_years"] == 5
        assert "id" in user_dict
        assert "created_at" in user_dict

    def test_user_profile_from_dict(self, sample_user_data):
        """Test creating UserProfile from dictionary."""
        user = UserProfile(**sample_user_data)
        
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.preferred_job_types == ["Full-time"]
        assert user.preferred_remote_types == ["Hybrid", "Remote"]

    def test_user_profile_json_serialization(self, sample_user_data):
        """Test JSON serialization compatibility."""
        user = UserProfile(**sample_user_data)
        
        # Test that we can get dictionary representation
        user_dict = user.model_dump() if hasattr(user, 'model_dump') else user.dict()
        
        # UUIDs remain as UUID objects in dict(), datetimes remain as datetime objects
        assert isinstance(user_dict["id"], (str, UUID))
        assert isinstance(user_dict["created_at"], datetime)
        
        # Test JSON export (should work regardless of UUID/datetime handling)
        if hasattr(user, 'model_dump_json'):
            json_str = user.model_dump_json()  # Pydantic v2
        else:
            json_str = user.json()  # Pydantic v1
        
        assert isinstance(json_str, str)
        assert "John" in json_str
        assert "Doe" in json_str

    def test_user_profile_copy_and_update(self):
        """Test copying and updating UserProfile instances."""
        original = UserProfile(
            first_name="John",
            last_name="Doe",
            experience_years=5,
        )
        
        # Test copy with updates (use model_copy for Pydantic v2)
        if hasattr(original, 'model_copy'):
            # Pydantic v2 - copy preserves all fields including ID by default
            updated = original.model_copy(update={"first_name": "Jane", "experience_years": 7})
            
            assert updated.first_name == "Jane"
            assert updated.last_name == "Doe"  # Unchanged fields preserved
            assert updated.experience_years == 7
            assert updated.id == original.id  # ID is preserved in model_copy
            
            # To get a new ID, we need to explicitly update it
            updated_with_new_id = original.model_copy(update={
                "first_name": "Jane",
                "id": uuid4()
            })
            assert updated_with_new_id.id != original.id
        else:
            # Pydantic v1 behavior
            updated = original.copy(update={"first_name": "Jane", "experience_years": 7})
            
            assert updated.first_name == "Jane"
            assert updated.last_name == "Doe"  # Unchanged fields preserved
            assert updated.experience_years == 7
