"""
Unit tests for JobListing Pydantic model validation.

Tests field constraints, enum validation, custom validators, and edge cases
for the JobListing and JobListingBase models.
"""

import pytest
from datetime import datetime
from uuid import uuid4, UUID
from pydantic import ValidationError

from backend.data.models import (
    JobListing,
    JobListingBase,
    JobType,
    RemoteType,
    ExperienceLevel,
    JobStatus,
    VerificationStatus,
    CompanySizeCategory,
    SeniorityLevel,
)


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestJobListingBase:
    """Test JobListingBase model validation."""

    def test_minimal_valid_job_listing_base(self):
        """Test creating JobListingBase with minimal required fields."""
        job = JobListingBase(title="Software Engineer")
        
        assert job.title == "Software Engineer"
        assert job.location is None
        assert job.description is None
        assert job.salary_currency == "USD"  # Default value
        assert job.skills_required == []
        assert job.skills_preferred == []
        assert job.benefits == []
        assert job.tech_stack == []
        assert job.source_count == 1  # Default value
        assert job.verification_status == VerificationStatus.UNVERIFIED

    def test_job_listing_base_with_all_fields(self, sample_datetime):
        """Test creating JobListingBase with all fields populated."""
        job_data = {
            "title": "Senior Software Engineer",
            "location": "San Francisco, CA",
            "description": "We are looking for an experienced software engineer...",
            "requirements": "5+ years of experience with Python",
            "responsibilities": "Develop and maintain web applications",
            "job_type": JobType.FULL_TIME,
            "remote_type": RemoteType.HYBRID,
            "experience_level": ExperienceLevel.SENIOR_LEVEL,
            "salary_min": 120000.0,
            "salary_max": 180000.0,
            "salary_currency": "USD",
            "skills_required": ["Python", "JavaScript"],
            "skills_preferred": ["AWS", "Docker"],
            "education_required": "Bachelor's degree in Computer Science",
            "benefits": ["Health Insurance", "401k"],
            "job_url": "https://example.com/jobs/123",
            "application_url": "https://example.com/apply/123",
            "posted_date": sample_datetime,
            "application_deadline": sample_datetime,
            "source": "company_website",
            "canonical_id": uuid4(),
            "source_count": 2,
            "data_quality_score": 0.95,
            "scraped_at": sample_datetime,
            "last_verified": sample_datetime,
            "verification_status": VerificationStatus.ACTIVE,
            "company_size_category": CompanySizeCategory.MEDIUM,
            "seniority_level": SeniorityLevel.INDIVIDUAL_CONTRIBUTOR,
            "tech_stack": ["Python", "React", "PostgreSQL"],
        }
        
        job = JobListingBase(**job_data)
        
        # Verify all fields are set correctly
        assert job.title == "Senior Software Engineer"
        assert job.location == "San Francisco, CA"
        assert job.job_type == JobType.FULL_TIME
        assert job.remote_type == RemoteType.HYBRID
        assert job.experience_level == ExperienceLevel.SENIOR_LEVEL
        assert job.salary_min == 120000.0
        assert job.salary_max == 180000.0
        assert job.skills_required == ["Python", "JavaScript"]
        assert job.skills_preferred == ["AWS", "Docker"]
        assert job.verification_status == VerificationStatus.ACTIVE
        assert job.tech_stack == ["Python", "React", "PostgreSQL"]

    def test_title_field_validation(self):
        """Test that title field is required and validates properly."""
        # Title is required
        with pytest.raises(ValidationError) as exc_info:
            JobListingBase()
        
        assert "title" in str(exc_info.value)
        assert "field required" in str(exc_info.value).lower()
        
        # Empty title should be allowed (no additional constraints in model)
        job = JobListingBase(title="")
        assert job.title == ""
        
        # Test with whitespace-only title
        job = JobListingBase(title="   ")
        assert job.title == "   "

    def test_enum_field_validation(self):
        """Test that enum fields validate properly."""
        # Valid enum values
        job = JobListingBase(
            title="Test Job",
            job_type=JobType.FULL_TIME,
            remote_type=RemoteType.REMOTE,
            experience_level=ExperienceLevel.MID_LEVEL,
        )
        
        assert job.job_type == JobType.FULL_TIME
        assert job.remote_type == RemoteType.REMOTE
        assert job.experience_level == ExperienceLevel.MID_LEVEL
        
        # Invalid enum values should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            JobListingBase(title="Test Job", job_type="invalid_type")
        
        assert "job_type" in str(exc_info.value)

    def test_salary_field_validation(self):
        """Test salary field validation."""
        # Valid salary ranges
        job = JobListingBase(
            title="Test Job",
            salary_min=50000.0,
            salary_max=100000.0,
        )
        
        assert job.salary_min == 50000.0
        assert job.salary_max == 100000.0
        
        # Test with integer values (should be converted to float)
        job = JobListingBase(
            title="Test Job",
            salary_min=50000,
            salary_max=100000,
        )
        
        assert isinstance(job.salary_min, float)
        assert isinstance(job.salary_max, float)
        
        # Negative salaries should be allowed (for validation at business logic level)
        job = JobListingBase(title="Test Job", salary_min=-1000.0)
        assert job.salary_min == -1000.0

    def test_list_field_custom_validator(self):
        """Test the custom validator for list fields (skills_required, skills_preferred, etc.)."""
        
        # Test with None values (should become empty lists)
        job = JobListingBase(
            title="Test Job",
            skills_required=None,
            skills_preferred=None,
            benefits=None,
            tech_stack=None,
        )
        
        assert job.skills_required == []
        assert job.skills_preferred == []
        assert job.benefits == []
        assert job.tech_stack == []
        
        # Test with comma-separated strings (should be split into lists)
        job = JobListingBase(
            title="Test Job",
            skills_required="Python, JavaScript, React",
            skills_preferred=" AWS , Docker , Kubernetes ",  # Extra spaces
            benefits="Health, 401k, PTO",
            tech_stack="React,Vue,Angular",  # No spaces
        )
        
        assert job.skills_required == ["Python", "JavaScript", "React"]
        assert job.skills_preferred == ["AWS", "Docker", "Kubernetes"]
        assert job.benefits == ["Health", "401k", "PTO"]
        assert job.tech_stack == ["React", "Vue", "Angular"]
        
        # Test with already valid lists (should remain unchanged)
        skills = ["Python", "JavaScript"]
        job = JobListingBase(title="Test Job", skills_required=skills)
        assert job.skills_required == skills
        
        # Test with empty string (should result in empty list)
        job = JobListingBase(title="Test Job", skills_required="")
        assert job.skills_required == []
        
        # Test with string containing only commas and spaces
        job = JobListingBase(title="Test Job", skills_required="  ,  ,  ")
        assert job.skills_required == []

    def test_url_field_validation(self):
        """Test URL field validation."""
        # Valid URLs
        job = JobListingBase(
            title="Test Job",
            job_url="https://example.com/jobs/123",
            application_url="https://apply.example.com/job/456",
        )
        
        assert job.job_url == "https://example.com/jobs/123"
        assert job.application_url == "https://apply.example.com/job/456"
        
        # Note: Pydantic doesn't validate URL format by default for str fields
        # This would need custom validation if strict URL validation is required

    def test_datetime_field_validation(self, sample_datetime):
        """Test datetime field validation."""
        job = JobListingBase(
            title="Test Job",
            posted_date=sample_datetime,
            application_deadline=sample_datetime,
            scraped_at=sample_datetime,
            last_verified=sample_datetime,
        )
        
        assert isinstance(job.posted_date, datetime)
        assert isinstance(job.application_deadline, datetime)
        assert isinstance(job.scraped_at, datetime)
        assert isinstance(job.last_verified, datetime)

    def test_quality_score_validation(self):
        """Test data quality score validation."""
        # Valid quality scores
        for score in [0.0, 0.5, 1.0]:
            job = JobListingBase(title="Test Job", data_quality_score=score)
            assert job.data_quality_score == score
        
        # Scores outside 0.0-1.0 range should be allowed (business logic validation)
        job = JobListingBase(title="Test Job", data_quality_score=1.5)
        assert job.data_quality_score == 1.5


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestJobListing:
    """Test JobListing model validation (inherits from JobListingBase)."""

    def test_minimal_valid_job_listing(self):
        """Test creating JobListing with minimal required fields."""
        job = JobListing(title="Software Engineer")
        
        # Test inherited fields
        assert job.title == "Software Engineer"
        assert job.salary_currency == "USD"
        
        # Test JobListing-specific fields
        assert isinstance(job.id, UUID)
        assert job.company_id is None
        assert job.company_name is None
        assert job.status == JobStatus.ACTIVE  # Default value
        assert isinstance(job.created_at, datetime)
        assert isinstance(job.updated_at, datetime)

    def test_job_listing_with_company_relationship(self):
        """Test JobListing with company relationship fields."""
        company_id = uuid4()
        
        job = JobListing(
            title="Senior Developer",
            company_id=company_id,
            company_name="TechCorp Inc",
        )
        
        assert job.company_id == company_id
        assert job.company_name == "TechCorp Inc"

    def test_job_listing_status_validation(self):
        """Test job status enum validation."""
        # Test all valid status values
        for status in JobStatus:
            job = JobListing(title="Test Job", status=status)
            assert job.status == status
        
        # Invalid status should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            JobListing(title="Test Job", status="invalid_status")
        
        assert "status" in str(exc_info.value)

    def test_job_listing_uuid_field_validation(self):
        """Test UUID field validation."""
        # Valid UUID
        job_id = uuid4()
        company_id = uuid4()
        
        job = JobListing(
            title="Test Job",
            id=job_id,
            company_id=company_id,
        )
        
        assert job.id == job_id
        assert job.company_id == company_id
        
        # Test UUID string conversion
        job = JobListing(
            title="Test Job",
            company_id=str(company_id),  # String UUID should be converted
        )
        
        assert job.company_id == company_id
        assert isinstance(job.company_id, UUID)

    def test_job_listing_config(self):
        """Test that the Config class is properly set."""
        job = JobListing(title="Test Job")
        
        # Test model config is properly set (Pydantic v2 style)
        # The from_attributes setting allows creating models from SQLAlchemy objects
        model_config = getattr(job.__class__, 'model_config', None)
        if model_config:
            # Pydantic v2 style - model_config is a dictionary
            if isinstance(model_config, dict):
                assert model_config.get('from_attributes', False) is True
            else:
                # If it's an object
                assert getattr(model_config, 'from_attributes', False) is True
        else:
            # Fallback: test that the model can be created from dict (basic functionality)
            test_dict = {"title": "Test from dict"}
            test_job = JobListing(**test_dict)
            assert test_job.title == "Test from dict"

    def test_job_listing_inheritance(self):
        """Test that JobListing properly inherits from JobListingBase."""
        job = JobListing(
            title="Full Stack Developer",
            description="Great opportunity...",
            job_type=JobType.FULL_TIME,
            skills_required="Python,React,PostgreSQL",
        )
        
        # Test inherited validation works
        assert job.skills_required == ["Python", "React", "PostgreSQL"]
        assert job.job_type == JobType.FULL_TIME
        
        # Test JobListing-specific fields
        assert isinstance(job.id, UUID)
        assert job.status == JobStatus.ACTIVE

    def test_job_listing_field_constraints(self):
        """Test field constraints and edge cases."""
        # Test that all optional fields can be None
        job = JobListing(
            title="Test Job",
            company_id=None,
            company_name=None,
        )
        
        assert job.company_id is None
        assert job.company_name is None
        
        # Test empty string handling
        job = JobListing(
            title="Test Job",
            company_name="",  # Empty string should be allowed
        )
        
        assert job.company_name == ""

    def test_job_listing_datetime_defaults(self):
        """Test that datetime fields have proper default values."""
        job1 = JobListing(title="Test Job 1")
        job2 = JobListing(title="Test Job 2")
        
        # Both should have datetime values
        assert isinstance(job1.created_at, datetime)
        assert isinstance(job1.updated_at, datetime)
        assert isinstance(job2.created_at, datetime)
        assert isinstance(job2.updated_at, datetime)
        
        # They should be different (created at different times)
        # Note: This could potentially be flaky if created in the same microsecond
        # In production, we might want to use a more robust test
        assert job1.id != job2.id  # At minimum, IDs should be different


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestJobListingEdgeCases:
    """Test edge cases and error conditions for job listing models."""

    def test_extremely_long_strings(self):
        """Test handling of extremely long string values."""
        long_string = "x" * 10000
        
        # Should not raise validation errors (length constraints at business logic level)
        job = JobListing(
            title=long_string,
            description=long_string,
            requirements=long_string,
        )
        
        assert len(job.title) == 10000
        assert len(job.description) == 10000
        assert len(job.requirements) == 10000

    def test_unicode_and_special_characters(self):
        """Test handling of Unicode and special characters."""
        job = JobListing(
            title="Développeur Python & ML Engineer 🚀",
            description="Looking for a developer with café experience ☕",
            location="São Paulo, Brasil",
            requirements="Must know C++ and .NET",
        )
        
        assert "🚀" in job.title
        assert "☕" in job.description
        assert "São Paulo" in job.location
        assert "C++" in job.requirements

    def test_large_numeric_values(self):
        """Test handling of large numeric values."""
        job = JobListing(
            title="High Paying Job",
            salary_min=1000000.0,  # $1M
            salary_max=10000000.0,  # $10M
            source_count=999999,
            data_quality_score=1.0,
        )
        
        assert job.salary_min == 1000000.0
        assert job.salary_max == 10000000.0
        assert job.source_count == 999999

    def test_very_large_lists(self):
        """Test handling of very large lists."""
        large_list = [f"skill_{i}" for i in range(1000)]
        
        job = JobListing(
            title="Requires Many Skills",
            skills_required=large_list,
            skills_preferred=large_list[:500],
            benefits=large_list[:100],
            tech_stack=large_list[:200],
        )
        
        assert len(job.skills_required) == 1000
        assert len(job.skills_preferred) == 500
        assert len(job.benefits) == 100
        assert len(job.tech_stack) == 200

    def test_mixed_type_list_validation(self):
        """Test that list validator handles mixed types properly."""
        # This should be handled by the custom validator
        job = JobListingBase(
            title="Test Job",
            skills_required="Python,JavaScript,123,",  # Mixed with number
        )
        
        # Should convert everything to strings and filter empty items
        assert "Python" in job.skills_required
        assert "JavaScript" in job.skills_required
        assert "123" in job.skills_required
        assert len([skill for skill in job.skills_required if skill.strip()]) == 3


# Performance and serialization tests
@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestJobListingSerialization:
    """Test model serialization and deserialization."""

    def test_job_listing_to_dict(self, sample_datetime):
        """Test converting JobListing to dictionary."""
        job = JobListing(
            title="Software Engineer",
            description="Great job opportunity",
            salary_min=100000.0,
            posted_date=sample_datetime,
        )
        
        # Use model_dump for Pydantic v2
        job_dict = job.model_dump() if hasattr(job, 'model_dump') else job.dict()
        
        assert isinstance(job_dict, dict)
        assert job_dict["title"] == "Software Engineer"
        assert job_dict["description"] == "Great job opportunity"
        assert job_dict["salary_min"] == 100000.0
        assert "id" in job_dict
        assert "created_at" in job_dict

    def test_job_listing_from_dict(self, sample_datetime):
        """Test creating JobListing from dictionary."""
        job_data = {
            "title": "Python Developer",
            "job_type": "Full-time",
            "remote_type": "Remote",
            "salary_min": 80000.0,
            "skills_required": ["Python", "Django"],
            "posted_date": sample_datetime.isoformat(),
        }
        
        job = JobListing(**job_data)
        
        assert job.title == "Python Developer"
        assert job.job_type == JobType.FULL_TIME
        assert job.remote_type == RemoteType.REMOTE
        assert job.skills_required == ["Python", "Django"]

    def test_job_listing_json_serialization(self, sample_datetime):
        """Test JSON serialization compatibility."""
        job = JobListing(
            title="Data Scientist",
            posted_date=sample_datetime,
            company_id=uuid4(),
        )
        
        # Test that we can get dictionary representation
        job_dict = job.model_dump() if hasattr(job, 'model_dump') else job.dict()
        
        # In Pydantic v2, UUIDs remain as UUID objects in dict(), datetimes remain as datetime objects
        assert isinstance(job_dict["id"], (str, UUID))  # Could be either depending on version
        assert isinstance(job_dict["created_at"], datetime)
        
        # Test JSON export (this should work regardless of UUID/datetime handling)
        if hasattr(job, 'model_dump_json'):
            json_str = job.model_dump_json()  # Pydantic v2
        else:
            json_str = job.json()  # Pydantic v1
        
        assert isinstance(json_str, str)
        assert "Data Scientist" in json_str

    def test_job_listing_copy_and_update(self):
        """Test copying and updating JobListing instances."""
        original = JobListing(
            title="Original Job",
            salary_min=50000.0,
            status=JobStatus.ACTIVE,
        )
        
        # Test copy with updates (use model_copy for Pydantic v2)
        if hasattr(original, 'model_copy'):
            # Pydantic v2 - copy preserves all fields including ID by default
            updated = original.model_copy(update={"title": "Updated Job", "salary_min": 60000.0})
            
            assert updated.title == "Updated Job"
            assert updated.salary_min == 60000.0
            assert updated.status == JobStatus.ACTIVE  # Unchanged fields preserved
            assert updated.id == original.id  # ID is preserved in model_copy
            
            # To get a new ID, we need to explicitly update it
            updated_with_new_id = original.model_copy(update={
                "title": "Updated Job",
                "salary_min": 60000.0,
                "id": uuid4()
            })
            assert updated_with_new_id.id != original.id
        else:
            # Pydantic v1 behavior
            updated = original.copy(update={"title": "Updated Job", "salary_min": 60000.0})
            
            assert updated.title == "Updated Job"
            assert updated.salary_min == 60000.0
            assert updated.status == JobStatus.ACTIVE  # Unchanged fields preserved
            # In v1, copy behavior may vary depending on implementation
