"""
Database Foreign Key Relationships and Constraint Tests.

Tests foreign key relationships, enum storage/retrieval, database constraints,
and referential integrity for all SQLAlchemy models.
"""

import pytest
from datetime import datetime
from uuid import uuid4
from sqlalchemy.exc import IntegrityError, StatementError

from backend.data.models import (
    CompanyInfoDB,
    JobListingDB,
    UserProfileDB,
    JobUserInteractionDB,
    TimelineEventDB,
    JobType,
    RemoteType,
    JobStatus,
    ExperienceLevel,
    ApplicationStatus,
    InteractionType,
    TimelineEventType,
    CompanySizeCategory,
    VerificationStatus,
    SeniorityLevel,
)


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.database
class TestForeignKeyRelationships:
    """Test foreign key relationships and referential integrity."""

    def test_company_to_job_listings_relationship(self, clean_db, sample_company_db_data, sample_job_db_data):
        """Test Company → JobListing one-to-many relationship."""
        # Create company
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.commit()
        
        # Create multiple job listings for the company
        job1_data = sample_job_db_data.copy()
        job1_data.update({
            'company_id': company.id,
            'title': 'Senior Software Engineer'
        })
        
        job2_data = sample_job_db_data.copy()
        job2_data.update({
            'company_id': company.id,
            'title': 'Junior Developer'
        })
        
        job1 = JobListingDB(**job1_data)
        job2 = JobListingDB(**job2_data)
        
        clean_db.add(job1)
        clean_db.add(job2)
        clean_db.commit()
        
        # Test forward relationship (company -> jobs)
        retrieved_company = clean_db.query(CompanyInfoDB).filter(CompanyInfoDB.id == company.id).first()
        assert retrieved_company is not None
        assert len(retrieved_company.job_listings) == 2
        
        job_titles = {job.title for job in retrieved_company.job_listings}
        assert job_titles == {'Senior Software Engineer', 'Junior Developer'}
        
        # Test reverse relationship (job -> company)
        retrieved_job1 = clean_db.query(JobListingDB).filter(JobListingDB.id == job1.id).first()
        assert retrieved_job1.company is not None
        assert retrieved_job1.company.name == "TechCorp Inc"
        assert retrieved_job1.company.id == company.id

    def test_user_to_interactions_relationship(self, clean_db, sample_company_db_data, sample_job_db_data, sample_user_db_data):
        """Test UserProfile → JobUserInteraction one-to-many relationship."""
        # Create prerequisites
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.flush()
        
        job_data = sample_job_db_data.copy()
        job_data['company_id'] = company.id
        job = JobListingDB(**job_data)
        clean_db.add(job)
        clean_db.flush()
        
        user = UserProfileDB(**sample_user_db_data)
        clean_db.add(user)
        clean_db.flush()
        clean_db.commit()
        
        # Create multiple interactions for the user
        interaction1 = JobUserInteractionDB(
            user_id=user.id,
            job_id=job.id,
            interaction_type=InteractionType.VIEWED,
            notes="Viewed this job posting"
        )
        
        interaction2 = JobUserInteractionDB(
            user_id=user.id,
            job_id=job.id,
            interaction_type=InteractionType.SAVED,
            saved_date=datetime(2025, 1, 22),
            notes="Saved for later application"
        )
        
        clean_db.add(interaction1)
        clean_db.add(interaction2)
        clean_db.commit()
        
        # Test forward relationship (user -> interactions)
        retrieved_user = clean_db.query(UserProfileDB).filter(UserProfileDB.id == user.id).first()
        assert retrieved_user is not None
        assert len(retrieved_user.job_interactions) == 2
        
        interaction_types = {interaction.interaction_type for interaction in retrieved_user.job_interactions}
        assert interaction_types == {InteractionType.VIEWED, InteractionType.SAVED}
        
        # Test reverse relationship (interaction -> user)
        retrieved_interaction1 = clean_db.query(JobUserInteractionDB).filter(JobUserInteractionDB.id == interaction1.id).first()
        assert retrieved_interaction1.user is not None
        assert retrieved_interaction1.user.email == "john.doe@example.com"
        assert retrieved_interaction1.user.id == user.id

    def test_job_to_interactions_relationship(self, clean_db, sample_company_db_data, sample_job_db_data, sample_user_db_data):
        """Test JobListing → JobUserInteraction one-to-many relationship."""
        # Create prerequisites
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.flush()
        
        job_data = sample_job_db_data.copy()
        job_data['company_id'] = company.id
        job = JobListingDB(**job_data)
        clean_db.add(job)
        clean_db.flush()
        
        # Create multiple users
        user1_data = sample_user_db_data.copy()
        user1_data['email'] = 'user1@example.com'
        user1 = UserProfileDB(**user1_data)
        clean_db.add(user1)
        clean_db.flush()
        
        user2_data = sample_user_db_data.copy()
        user2_data['email'] = 'user2@example.com'
        user2 = UserProfileDB(**user2_data)
        clean_db.add(user2)
        clean_db.flush()
        clean_db.commit()
        
        # Create interactions from different users to the same job
        interaction1 = JobUserInteractionDB(
            user_id=user1.id,
            job_id=job.id,
            interaction_type=InteractionType.APPLIED,
            application_status=ApplicationStatus.APPLIED
        )
        
        interaction2 = JobUserInteractionDB(
            user_id=user2.id,
            job_id=job.id,
            interaction_type=InteractionType.SAVED,
            saved_date=datetime(2025, 1, 22)
        )
        
        clean_db.add(interaction1)
        clean_db.add(interaction2)
        clean_db.commit()
        
        # Test forward relationship (job -> interactions)
        retrieved_job = clean_db.query(JobListingDB).filter(JobListingDB.id == job.id).first()
        assert retrieved_job is not None
        assert len(retrieved_job.user_interactions) == 2
        
        # Test that interactions come from different users
        user_emails = {interaction.user.email for interaction in retrieved_job.user_interactions}
        assert user_emails == {'user1@example.com', 'user2@example.com'}

    def test_cascade_delete_relationships(self, clean_db, sample_company_db_data, sample_job_db_data, sample_user_db_data):
        """Test cascade delete behavior for foreign key relationships."""
        # Create full relationship chain
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.flush()
        
        job_data = sample_job_db_data.copy()
        job_data['company_id'] = company.id
        job = JobListingDB(**job_data)
        clean_db.add(job)
        clean_db.flush()
        
        user = UserProfileDB(**sample_user_db_data)
        clean_db.add(user)
        clean_db.flush()
        
        interaction = JobUserInteractionDB(
            user_id=user.id,
            job_id=job.id,
            interaction_type=InteractionType.APPLIED,
            application_status=ApplicationStatus.APPLIED
        )
        clean_db.add(interaction)
        clean_db.commit()
        
        # Store IDs for later checking
        company_id = company.id
        job_id = job.id
        user_id = user.id
        interaction_id = interaction.id
        
        # Delete user - should cascade to interactions
        clean_db.delete(user)
        clean_db.commit()
        
        # Interaction should be deleted due to cascade
        deleted_interaction = clean_db.query(JobUserInteractionDB).filter(JobUserInteractionDB.id == interaction_id).first()
        assert deleted_interaction is None
        
        # Job and company should still exist
        remaining_job = clean_db.query(JobListingDB).filter(JobListingDB.id == job_id).first()
        assert remaining_job is not None
        
        remaining_company = clean_db.query(CompanyInfoDB).filter(CompanyInfoDB.id == company_id).first()
        assert remaining_company is not None

    def test_foreign_key_constraint_violation(self, clean_db):
        """Test that foreign key constraints prevent invalid references."""
        # Try to create job with non-existent company
        with pytest.raises(IntegrityError):
            job = JobListingDB(
                company_id=str(uuid4()),  # Non-existent company
                title="Test Job"
            )
            clean_db.add(job)
            clean_db.commit()
        
        clean_db.rollback()
        
        # Try to create interaction with non-existent user
        with pytest.raises(IntegrityError):
            interaction = JobUserInteractionDB(
                user_id=str(uuid4()),  # Non-existent user
                job_id=str(uuid4()),   # Non-existent job
                interaction_type=InteractionType.VIEWED
            )
            clean_db.add(interaction)
            clean_db.commit()


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.database
class TestEnumFieldStorage:
    """Test enum field storage and retrieval in database."""

    def test_job_type_enum_storage(self, clean_db, sample_company_db_data, sample_job_db_data):
        """Test JobType enum storage and retrieval."""
        # Create company first
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.commit()
        
        # Test all JobType enum values
        test_cases = [
            (JobType.FULL_TIME, "Full-time"),
            (JobType.PART_TIME, "Part-time"),
            (JobType.CONTRACT, "Contract"),
            (JobType.FREELANCE, "Freelance"),
            (JobType.INTERNSHIP, "Internship"),
            (JobType.TEMPORARY, "Temporary"),
        ]
        
        job_ids = []
        for job_type_enum, expected_value in test_cases:
            job_data = sample_job_db_data.copy()
            job_data.update({
                'company_id': company.id,
                'title': f'Test {job_type_enum.value} Job',
                'job_type': job_type_enum
            })
            
            job = JobListingDB(**job_data)
            clean_db.add(job)
            clean_db.flush()
            job_ids.append((job.id, job_type_enum, expected_value))
        
        clean_db.commit()
        
        # Verify enum values are stored and retrieved correctly
        for job_id, expected_enum, expected_value in job_ids:
            retrieved_job = clean_db.query(JobListingDB).filter(JobListingDB.id == job_id).first()
            assert retrieved_job is not None
            assert retrieved_job.job_type == expected_enum
            assert retrieved_job.job_type.value == expected_value

    def test_remote_type_enum_storage(self, clean_db, sample_company_db_data, sample_job_db_data):
        """Test RemoteType enum storage and retrieval."""
        # Create company first
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.commit()
        
        # Test all RemoteType enum values
        test_cases = [
            (RemoteType.ON_SITE, "On-site"),
            (RemoteType.REMOTE, "Remote"),
            (RemoteType.HYBRID, "Hybrid"),
        ]
        
        job_ids = []
        for remote_type_enum, expected_value in test_cases:
            job_data = sample_job_db_data.copy()
            job_data.update({
                'company_id': company.id,
                'title': f'Test {remote_type_enum.value} Job',
                'remote_type': remote_type_enum
            })
            
            job = JobListingDB(**job_data)
            clean_db.add(job)
            clean_db.flush()
            job_ids.append((job.id, remote_type_enum, expected_value))
        
        clean_db.commit()
        
        # Verify enum values are stored and retrieved correctly
        for job_id, expected_enum, expected_value in job_ids:
            retrieved_job = clean_db.query(JobListingDB).filter(JobListingDB.id == job_id).first()
            assert retrieved_job is not None
            assert retrieved_job.remote_type == expected_enum
            assert retrieved_job.remote_type.value == expected_value

    def test_application_status_enum_storage(self, clean_db, sample_company_db_data, sample_job_db_data, sample_user_db_data):
        """Test ApplicationStatus enum storage and retrieval."""
        # Create prerequisites
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.flush()
        
        job_data = sample_job_db_data.copy()
        job_data['company_id'] = company.id
        job = JobListingDB(**job_data)
        clean_db.add(job)
        clean_db.flush()
        
        user = UserProfileDB(**sample_user_db_data)
        clean_db.add(user)
        clean_db.flush()
        clean_db.commit()
        
        # Test all ApplicationStatus enum values
        # Create different jobs for each status to avoid unique constraint violations
        test_cases = [
            (ApplicationStatus.NOT_APPLIED, "not_applied"),
            (ApplicationStatus.APPLIED, "applied"),
            (ApplicationStatus.INTERVIEWING, "interviewing"),
            (ApplicationStatus.REJECTED, "rejected"),
            (ApplicationStatus.ACCEPTED, "accepted"),
            (ApplicationStatus.WITHDRAWN, "withdrawn"),
        ]
        
        interaction_ids = []
        for i, (status_enum, expected_value) in enumerate(test_cases):
            # Create a unique job for each status
            unique_job_data = sample_job_db_data.copy()
            unique_job_data.update({
                'company_id': company.id,
                'title': f'Job {i} - {status_enum.value}'
            })
            unique_job = JobListingDB(**unique_job_data)
            clean_db.add(unique_job)
            clean_db.flush()
            
            interaction = JobUserInteractionDB(
                user_id=user.id,
                job_id=unique_job.id,
                interaction_type=InteractionType.APPLIED,
                application_status=status_enum,
                notes=f'Test {status_enum.value} status'
            )
            clean_db.add(interaction)
            clean_db.flush()
            interaction_ids.append((interaction.id, status_enum, expected_value))
        
        clean_db.commit()
        
        # Verify enum values are stored and retrieved correctly
        for interaction_id, expected_enum, expected_value in interaction_ids:
            retrieved_interaction = clean_db.query(JobUserInteractionDB).filter(JobUserInteractionDB.id == interaction_id).first()
            assert retrieved_interaction is not None
            assert retrieved_interaction.application_status == expected_enum
            assert retrieved_interaction.application_status.value == expected_value

    def test_company_size_category_enum_storage(self, clean_db, sample_company_db_data):
        """Test CompanySizeCategory enum storage and retrieval."""
        # Test all CompanySizeCategory enum values
        test_cases = [
            (CompanySizeCategory.STARTUP, "startup"),
            (CompanySizeCategory.SMALL, "small"),
            (CompanySizeCategory.MEDIUM, "medium"),
            (CompanySizeCategory.LARGE, "large"),
            (CompanySizeCategory.ENTERPRISE, "enterprise"),
        ]
        
        company_ids = []
        for size_category_enum, expected_value in test_cases:
            company_data = sample_company_db_data.copy()
            company_data.update({
                'name': f'Test {size_category_enum.value.title()} Company',
                'domain': f'{size_category_enum.value}-test.com',
                'size_category': size_category_enum
            })
            
            company = CompanyInfoDB(**company_data)
            clean_db.add(company)
            clean_db.flush()
            company_ids.append((company.id, size_category_enum, expected_value))
        
        clean_db.commit()
        
        # Verify enum values are stored and retrieved correctly
        for company_id, expected_enum, expected_value in company_ids:
            retrieved_company = clean_db.query(CompanyInfoDB).filter(CompanyInfoDB.id == company_id).first()
            assert retrieved_company is not None
            assert retrieved_company.size_category == expected_enum
            assert retrieved_company.size_category.value == expected_value

    def test_invalid_enum_value_handling(self, clean_db, sample_company_db_data):
        """Test handling of invalid enum values."""
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.commit()
        
        # Try to create job with invalid enum value
        # SQLAlchemy will accept string values during object creation
        job = JobListingDB(
            company_id=company.id,
            title="Test Job",
            job_type="invalid_job_type"  # Invalid enum value - stored as string
        )
        clean_db.add(job)
        
        # The validation might happen at different times
        try:
            clean_db.commit()
            # If we get here, the database stored the string value
            # But SQLAlchemy will raise LookupError when trying to read it back
            with pytest.raises(LookupError):
                retrieved_job = clean_db.query(JobListingDB).filter(JobListingDB.id == job.id).first()
                
        except (IntegrityError, StatementError, LookupError):
            # Some databases might enforce enum constraints at different levels
            clean_db.rollback()
            # This is also acceptable behavior - validation failed at commit or read


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.database
class TestDatabaseConstraints:
    """Test database constraints and validation rules."""

    def test_unique_constraint_violations(self, clean_db, sample_user_db_data, sample_company_db_data):
        """Test unique constraint violations."""
        # Test email uniqueness in user profiles
        user1 = UserProfileDB(**sample_user_db_data)
        clean_db.add(user1)
        clean_db.commit()
        
        # Try to create another user with same email
        user2_data = sample_user_db_data.copy()
        user2_data['first_name'] = 'Jane'
        user2 = UserProfileDB(**user2_data)  # Same email as user1
        
        with pytest.raises(IntegrityError):
            clean_db.add(user2)
            clean_db.commit()
        
        clean_db.rollback()
        
        # Test company domain uniqueness
        company1 = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company1)
        clean_db.commit()
        
        # Try to create another company with same domain
        company2_data = sample_company_db_data.copy()
        company2_data['name'] = 'Different Name Corp'
        company2_data['normalized_name'] = 'different name corp'
        company2 = CompanyInfoDB(**company2_data)  # Same domain as company1
        
        with pytest.raises(IntegrityError):
            clean_db.add(company2)
            clean_db.commit()

    def test_check_constraint_validations(self, clean_db, sample_company_db_data):
        """Test database check constraints."""
        # Create company first
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.commit()
        
        # Test salary range constraint: salary_max >= salary_min
        with pytest.raises(IntegrityError):
            job = JobListingDB(
                company_id=company.id,
                title="Invalid Salary Job",
                salary_min=100000.0,
                salary_max=80000.0  # Max less than min - should violate constraint
            )
            clean_db.add(job)
            clean_db.commit()
        
        clean_db.rollback()
        
        # Test positive salary constraint: salary_min >= 0
        with pytest.raises(IntegrityError):
            job = JobListingDB(
                company_id=company.id,
                title="Negative Salary Job",
                salary_min=-50000.0  # Negative salary - should violate constraint
            )
            clean_db.add(job)
            clean_db.commit()
        
        clean_db.rollback()
        
        # Test title length constraints
        with pytest.raises(IntegrityError):
            job = JobListingDB(
                company_id=company.id,
                title="AB"  # Too short - should violate minimum length constraint
            )
            clean_db.add(job)
            clean_db.commit()
        
        clean_db.rollback()
        
        # Test title maximum length
        with pytest.raises(IntegrityError):
            job = JobListingDB(
                company_id=company.id,
                title="A" * 201  # Too long - should violate maximum length constraint
            )
            clean_db.add(job)
            clean_db.commit()

    def test_not_null_constraints(self, clean_db, sample_company_db_data):
        """Test NOT NULL constraints on required fields."""
        # Try to create company without required name field
        with pytest.raises(IntegrityError):
            company = CompanyInfoDB(
                domain='test.com',
                industry='Technology'
                # Missing required 'name' field
            )
            clean_db.add(company)
            clean_db.commit()
        
        clean_db.rollback()
        
        # Try to create job without required company_id
        with pytest.raises(IntegrityError):
            job = JobListingDB(
                title="Test Job"
                # Missing required 'company_id' field
            )
            clean_db.add(job)
            clean_db.commit()
        
        clean_db.rollback()
        
        # Try to create interaction without required fields
        with pytest.raises(IntegrityError):
            interaction = JobUserInteractionDB(
                # Missing required user_id, job_id, interaction_type
                notes="Test interaction"
            )
            clean_db.add(interaction)
            clean_db.commit()

    def test_unique_constraint_combinations(self, clean_db, sample_company_db_data, sample_job_db_data, sample_user_db_data):
        """Test unique constraint combinations (composite unique constraints)."""
        # Create prerequisites
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.flush()
        
        job_data = sample_job_db_data.copy()
        job_data['company_id'] = company.id
        job = JobListingDB(**job_data)
        clean_db.add(job)
        clean_db.flush()
        
        user = UserProfileDB(**sample_user_db_data)
        clean_db.add(user)
        clean_db.flush()
        clean_db.commit()
        
        # Create first interaction
        interaction1 = JobUserInteractionDB(
            user_id=user.id,
            job_id=job.id,
            interaction_type=InteractionType.VIEWED
        )
        clean_db.add(interaction1)
        clean_db.commit()
        
        # Try to create duplicate interaction (same user, job, interaction_type)
        with pytest.raises(IntegrityError):
            interaction2 = JobUserInteractionDB(
                user_id=user.id,
                job_id=job.id,
                interaction_type=InteractionType.VIEWED  # Same combination should violate unique constraint
            )
            clean_db.add(interaction2)
            clean_db.commit()
        
        clean_db.rollback()
        
        # Different interaction type should work
        interaction3 = JobUserInteractionDB(
            user_id=user.id,
            job_id=job.id,
            interaction_type=InteractionType.SAVED  # Different interaction type
        )
        clean_db.add(interaction3)
        clean_db.commit()
        
        # Verify both interactions exist
        interactions = clean_db.query(JobUserInteractionDB).filter(
            JobUserInteractionDB.user_id == user.id,
            JobUserInteractionDB.job_id == job.id
        ).all()
        
        assert len(interactions) == 2
        interaction_types = {i.interaction_type for i in interactions}
        assert interaction_types == {InteractionType.VIEWED, InteractionType.SAVED}
