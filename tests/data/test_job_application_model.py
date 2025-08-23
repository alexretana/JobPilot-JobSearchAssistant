"""
Unit tests for JobApplication Pydantic model validation.

Tests field constraints, enum validation, date validation, and status transitions
for the JobApplication model.
"""

import pytest
from datetime import datetime
from uuid import uuid4, UUID
from pydantic import ValidationError

from backend.data.models import (
    JobApplication,
    ApplicationStatus,
)


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestJobApplication:
    """Test JobApplication model validation."""

    def test_minimal_valid_job_application(self):
        """Test creating JobApplication with minimal required fields."""
        job_id = uuid4()
        user_id = uuid4()
        
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
        )
        
        # Test that auto-generated fields exist
        assert isinstance(app.id, UUID)
        assert isinstance(app.created_at, datetime)
        assert isinstance(app.updated_at, datetime)
        
        # Test required fields
        assert app.job_id == job_id
        assert app.user_profile_id == user_id
        
        # Test default values
        assert app.status == ApplicationStatus.NOT_APPLIED
        assert app.applied_date is None
        assert app.response_date is None
        assert app.resume_version is None
        assert app.cover_letter is None
        assert app.notes is None
        assert app.follow_up_date is None
        assert app.interview_scheduled is None

    def test_job_application_with_all_fields(self, sample_datetime, sample_job_application_data):
        """Test creating JobApplication with all fields populated."""
        job_id = uuid4()
        user_id = uuid4()
        
        app_data = {
            "job_id": job_id,
            "user_profile_id": user_id,
            **sample_job_application_data
        }
        
        app = JobApplication(**app_data)
        
        # Verify all fields are set correctly
        assert app.job_id == job_id
        assert app.user_profile_id == user_id
        assert app.status == ApplicationStatus.APPLIED
        assert app.applied_date == sample_job_application_data["applied_date"]
        assert app.resume_version == "v1.2"
        assert app.cover_letter == "Dear Hiring Manager, I am very interested..."
        assert app.notes == "Applied through company website"

    def test_required_fields_validation(self):
        """Test that required fields are properly validated."""
        # Missing job_id should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            JobApplication(user_profile_id=uuid4())
        
        assert "job_id" in str(exc_info.value)
        assert "field required" in str(exc_info.value).lower()
        
        # Missing user_profile_id should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            JobApplication(job_id=uuid4())
        
        assert "user_profile_id" in str(exc_info.value)
        assert "field required" in str(exc_info.value).lower()

    def test_status_enum_validation(self):
        """Test application status enum validation."""
        job_id = uuid4()
        user_id = uuid4()
        
        # Test all valid status values
        for status in ApplicationStatus:
            app = JobApplication(
                job_id=job_id,
                user_profile_id=user_id,
                status=status
            )
            assert app.status == status
        
        # Invalid status should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            JobApplication(
                job_id=job_id,
                user_profile_id=user_id,
                status="invalid_status"
            )
        
        assert "status" in str(exc_info.value)

    def test_uuid_field_validation(self):
        """Test UUID field validation."""
        # Valid UUIDs
        job_id = uuid4()
        user_id = uuid4()
        app_id = uuid4()
        
        app = JobApplication(
            id=app_id,
            job_id=job_id,
            user_profile_id=user_id,
        )
        
        assert app.id == app_id
        assert app.job_id == job_id
        assert app.user_profile_id == user_id
        
        # Test UUID string conversion
        app = JobApplication(
            job_id=str(job_id),
            user_profile_id=str(user_id),
        )
        
        assert app.job_id == job_id
        assert app.user_profile_id == user_id
        assert isinstance(app.job_id, UUID)
        assert isinstance(app.user_profile_id, UUID)

    def test_datetime_field_validation(self, sample_datetime):
        """Test datetime field validation."""
        job_id = uuid4()
        user_id = uuid4()
        
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            applied_date=sample_datetime,
            response_date=sample_datetime,
            follow_up_date=sample_datetime,
            interview_scheduled=sample_datetime,
        )
        
        assert isinstance(app.applied_date, datetime)
        assert isinstance(app.response_date, datetime)
        assert isinstance(app.follow_up_date, datetime)
        assert isinstance(app.interview_scheduled, datetime)
        
        assert app.applied_date == sample_datetime
        assert app.response_date == sample_datetime
        assert app.follow_up_date == sample_datetime
        assert app.interview_scheduled == sample_datetime

    def test_string_field_validation(self):
        """Test string field validation."""
        job_id = uuid4()
        user_id = uuid4()
        
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            resume_version="v2.1",
            cover_letter="This is my cover letter...",
            notes="Some application notes here",
        )
        
        assert app.resume_version == "v2.1"
        assert app.cover_letter == "This is my cover letter..."
        assert app.notes == "Some application notes here"
        
        # Empty strings should be allowed
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            resume_version="",
            cover_letter="",
            notes="",
        )
        
        assert app.resume_version == ""
        assert app.cover_letter == ""
        assert app.notes == ""

    def test_datetime_defaults(self):
        """Test that datetime fields have proper default values."""
        job_id1 = uuid4()
        user_id1 = uuid4()
        job_id2 = uuid4()
        user_id2 = uuid4()
        
        app1 = JobApplication(job_id=job_id1, user_profile_id=user_id1)
        app2 = JobApplication(job_id=job_id2, user_profile_id=user_id2)
        
        # Both should have datetime values
        assert isinstance(app1.created_at, datetime)
        assert isinstance(app1.updated_at, datetime)
        assert isinstance(app2.created_at, datetime)
        assert isinstance(app2.updated_at, datetime)
        
        # They should be different (created at different times)
        assert app1.id != app2.id  # At minimum, IDs should be different

    def test_job_application_config(self):
        """Test that the Config class is properly set."""
        app = JobApplication(job_id=uuid4(), user_profile_id=uuid4())
        
        # Test model config is properly set (Pydantic v2 style)
        model_config = getattr(app.__class__, 'model_config', None)
        if model_config:
            # Pydantic v2 style - model_config is a dictionary
            if isinstance(model_config, dict):
                assert model_config.get('from_attributes', False) is True
            else:
                # If it's an object
                assert getattr(model_config, 'from_attributes', False) is True
        else:
            # Fallback: test that the model can be created from dict (basic functionality)
            test_dict = {
                "job_id": uuid4(),
                "user_profile_id": uuid4(),
                "status": ApplicationStatus.APPLIED
            }
            test_app = JobApplication(**test_dict)
            assert test_app.status == ApplicationStatus.APPLIED


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestJobApplicationStatusTransitions:
    """Test JobApplication status transition logic and patterns."""

    def test_typical_application_flow(self, sample_datetime):
        """Test a typical application status progression."""
        job_id = uuid4()
        user_id = uuid4()
        
        # Start with not applied
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            status=ApplicationStatus.NOT_APPLIED
        )
        assert app.status == ApplicationStatus.NOT_APPLIED
        assert app.applied_date is None
        
        # Update to applied
        app.status = ApplicationStatus.APPLIED
        app.applied_date = sample_datetime
        assert app.status == ApplicationStatus.APPLIED
        assert app.applied_date == sample_datetime
        
        # Update to interviewing
        app.status = ApplicationStatus.INTERVIEWING
        app.interview_scheduled = sample_datetime
        assert app.status == ApplicationStatus.INTERVIEWING
        assert app.interview_scheduled == sample_datetime
        
        # Could end as accepted
        app.status = ApplicationStatus.ACCEPTED
        app.response_date = sample_datetime
        assert app.status == ApplicationStatus.ACCEPTED
        assert app.response_date == sample_datetime

    def test_application_rejection_flow(self, sample_datetime):
        """Test application rejection flow."""
        job_id = uuid4()
        user_id = uuid4()
        
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            status=ApplicationStatus.APPLIED,
            applied_date=sample_datetime
        )
        
        # Direct rejection after application
        app.status = ApplicationStatus.REJECTED
        app.response_date = sample_datetime
        app.notes = "Position filled by another candidate"
        
        assert app.status == ApplicationStatus.REJECTED
        assert app.response_date == sample_datetime
        assert app.notes == "Position filled by another candidate"

    def test_withdrawn_application_flow(self, sample_datetime):
        """Test withdrawn application flow."""
        job_id = uuid4()
        user_id = uuid4()
        
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            status=ApplicationStatus.INTERVIEWING,
            applied_date=sample_datetime,
            interview_scheduled=sample_datetime
        )
        
        # User withdraws application
        app.status = ApplicationStatus.WITHDRAWN
        app.notes = "Accepted another offer"
        
        assert app.status == ApplicationStatus.WITHDRAWN
        assert app.notes == "Accepted another offer"

    def test_status_validation_with_dates(self, sample_datetime):
        """Test status and date field combinations."""
        job_id = uuid4()
        user_id = uuid4()
        
        # Applied status with applied_date
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            status=ApplicationStatus.APPLIED,
            applied_date=sample_datetime
        )
        assert app.status == ApplicationStatus.APPLIED
        assert app.applied_date == sample_datetime
        
        # Interviewing status with interview scheduled
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            status=ApplicationStatus.INTERVIEWING,
            applied_date=sample_datetime,
            interview_scheduled=sample_datetime
        )
        assert app.status == ApplicationStatus.INTERVIEWING
        assert app.interview_scheduled == sample_datetime
        
        # Rejected status with response date
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            status=ApplicationStatus.REJECTED,
            applied_date=sample_datetime,
            response_date=sample_datetime
        )
        assert app.status == ApplicationStatus.REJECTED
        assert app.response_date == sample_datetime


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestJobApplicationEdgeCases:
    """Test edge cases and error conditions for JobApplication model."""

    def test_extremely_long_strings(self):
        """Test handling of extremely long string values."""
        long_string = "x" * 10000
        
        job_id = uuid4()
        user_id = uuid4()
        
        # Should not raise validation errors (length constraints at business logic level)
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            resume_version=long_string,
            cover_letter=long_string,
            notes=long_string,
        )
        
        assert len(app.resume_version) == 10000
        assert len(app.cover_letter) == 10000
        assert len(app.notes) == 10000

    def test_unicode_and_special_characters(self):
        """Test handling of Unicode and special characters."""
        job_id = uuid4()
        user_id = uuid4()
        
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            resume_version="résumé_v1.0_🚀",
            cover_letter="Dear Señor García, I'm très interested in this position! 💼",
            notes="Applied via LinkedIn - très promising company 🌟",
        )
        
        assert "résumé_v1.0_🚀" == app.resume_version
        assert "Señor García" in app.cover_letter
        assert "💼" in app.cover_letter
        assert "très promising" in app.notes
        assert "🌟" in app.notes

    def test_future_and_past_dates(self):
        """Test handling of future and past dates."""
        job_id = uuid4()
        user_id = uuid4()
        
        # Past dates (should be allowed)
        past_date = datetime(2020, 1, 1, 12, 0, 0)
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            applied_date=past_date,
            response_date=past_date,
        )
        assert app.applied_date == past_date
        assert app.response_date == past_date
        
        # Future dates (should be allowed - business logic can handle validation)
        future_date = datetime(2030, 12, 31, 23, 59, 59)
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            follow_up_date=future_date,
            interview_scheduled=future_date,
        )
        assert app.follow_up_date == future_date
        assert app.interview_scheduled == future_date

    def test_duplicate_job_user_combinations(self):
        """Test that duplicate job-user combinations can be created (business logic handles uniqueness)."""
        job_id = uuid4()
        user_id = uuid4()
        
        # Create two applications for same job-user combination
        app1 = JobApplication(job_id=job_id, user_profile_id=user_id)
        app2 = JobApplication(job_id=job_id, user_profile_id=user_id)
        
        # Should be allowed at model level (database constraints handle uniqueness)
        assert app1.job_id == app2.job_id
        assert app1.user_profile_id == app2.user_profile_id
        assert app1.id != app2.id  # But should have different IDs

    def test_empty_string_handling(self):
        """Test handling of empty strings."""
        job_id = uuid4()
        user_id = uuid4()
        
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            resume_version="",
            cover_letter="",
            notes="",
        )
        
        # Empty strings should be preserved
        assert app.resume_version == ""
        assert app.cover_letter == ""
        assert app.notes == ""

    def test_none_vs_empty_string_handling(self):
        """Test difference between None and empty string values."""
        job_id = uuid4()
        user_id = uuid4()
        
        # Test with None values
        app_none = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            resume_version=None,
            cover_letter=None,
            notes=None,
        )
        assert app_none.resume_version is None
        assert app_none.cover_letter is None
        assert app_none.notes is None
        
        # Test with empty strings
        app_empty = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            resume_version="",
            cover_letter="",
            notes="",
        )
        assert app_empty.resume_version == ""
        assert app_empty.cover_letter == ""
        assert app_empty.notes == ""


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestJobApplicationSerialization:
    """Test JobApplication model serialization and deserialization."""

    def test_job_application_to_dict(self, sample_datetime, sample_job_application_data):
        """Test converting JobApplication to dictionary."""
        job_id = uuid4()
        user_id = uuid4()
        
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            **sample_job_application_data
        )
        
        # Use model_dump for Pydantic v2
        app_dict = app.model_dump() if hasattr(app, 'model_dump') else app.dict()
        
        assert isinstance(app_dict, dict)
        assert app_dict["job_id"] == job_id
        assert app_dict["user_profile_id"] == user_id
        assert app_dict["status"] == ApplicationStatus.APPLIED
        assert app_dict["resume_version"] == "v1.2"
        assert "id" in app_dict
        assert "created_at" in app_dict

    def test_job_application_from_dict(self):
        """Test creating JobApplication from dictionary."""
        job_id = uuid4()
        user_id = uuid4()
        
        app_data = {
            "job_id": job_id,
            "user_profile_id": user_id,
            "status": "applied",
            "resume_version": "v1.5",
            "notes": "Applied via company website"
        }
        
        app = JobApplication(**app_data)
        
        assert app.job_id == job_id
        assert app.user_profile_id == user_id
        assert app.status == ApplicationStatus.APPLIED
        assert app.resume_version == "v1.5"
        assert app.notes == "Applied via company website"

    def test_job_application_json_serialization(self, sample_job_application_data):
        """Test JSON serialization compatibility."""
        job_id = uuid4()
        user_id = uuid4()
        
        app = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            **sample_job_application_data
        )
        
        # Test that we can get dictionary representation
        app_dict = app.model_dump() if hasattr(app, 'model_dump') else app.dict()
        
        # UUIDs remain as UUID objects in dict(), datetimes remain as datetime objects
        assert isinstance(app_dict["id"], (str, UUID))
        assert isinstance(app_dict["job_id"], (str, UUID))
        assert isinstance(app_dict["user_profile_id"], (str, UUID))
        assert isinstance(app_dict["created_at"], datetime)
        
        # Test JSON export (should work regardless of UUID/datetime handling)
        if hasattr(app, 'model_dump_json'):
            json_str = app.model_dump_json()  # Pydantic v2
        else:
            json_str = app.json()  # Pydantic v1
        
        assert isinstance(json_str, str)
        assert "applied" in json_str
        assert "v1.2" in json_str

    def test_job_application_copy_and_update(self, sample_datetime):
        """Test copying and updating JobApplication instances."""
        job_id = uuid4()
        user_id = uuid4()
        
        original = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            status=ApplicationStatus.APPLIED,
            applied_date=sample_datetime,
        )
        
        # Test copy with updates (use model_copy for Pydantic v2)
        if hasattr(original, 'model_copy'):
            # Pydantic v2 - copy preserves all fields including ID by default
            updated = original.model_copy(update={
                "status": ApplicationStatus.INTERVIEWING,
                "interview_scheduled": sample_datetime
            })
            
            assert updated.status == ApplicationStatus.INTERVIEWING
            assert updated.interview_scheduled == sample_datetime
            assert updated.applied_date == sample_datetime  # Unchanged fields preserved
            assert updated.id == original.id  # ID is preserved in model_copy
            
            # To get a new ID, we need to explicitly update it
            updated_with_new_id = original.model_copy(update={
                "status": ApplicationStatus.REJECTED,
                "id": uuid4()
            })
            assert updated_with_new_id.id != original.id
        else:
            # Pydantic v1 behavior
            updated = original.copy(update={
                "status": ApplicationStatus.INTERVIEWING,
                "interview_scheduled": sample_datetime
            })
            
            assert updated.status == ApplicationStatus.INTERVIEWING
            assert updated.interview_scheduled == sample_datetime
            assert updated.applied_date == sample_datetime  # Unchanged fields preserved
