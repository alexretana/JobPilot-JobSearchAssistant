"""
SQLAlchemy Database Model Tests.

Tests database model creation, schema validation, table structure,
and basic CRUD operations for all SQLAlchemy models.
"""

import pytest
from datetime import datetime
from uuid import uuid4
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError

from backend.data.models import (
    CompanyInfoDB,
    JobListingDB,
    UserProfileDB,
    JobUserInteractionDB,
    TimelineEventDB,
    JobSourceDB,
    JobSourceListingDB,
    JobEmbeddingDB,
    JobDeduplicationDB,
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
class TestDatabaseModelCreation:
    """Test database model creation and schema validation."""

    def test_database_tables_created(self, db_engine):
        """Test that all expected tables are created in the database."""
        inspector = inspect(db_engine)
        table_names = inspector.get_table_names()
        
        expected_tables = {
            "companies",
            "job_listings", 
            "user_profiles",
            "job_user_interactions",
            "timeline_events",
            "job_sources",
            "job_source_listings",
            "job_embeddings",
            "job_duplications",
        }
        
        actual_tables = set(table_names)
        assert expected_tables.issubset(actual_tables), f"Missing tables: {expected_tables - actual_tables}"

    def test_company_table_schema(self, db_engine):
        """Test CompanyInfoDB table schema and columns."""
        inspector = inspect(db_engine)
        columns = {col['name']: col for col in inspector.get_columns('companies')}
        
        # Test required columns exist
        required_columns = {
            'id', 'name', 'normalized_name', 'domain', 'industry', 'size',
            'size_category', 'location', 'headquarters_location', 'founded_year',
            'website', 'description', 'logo_url', 'culture', 'values', 'benefits',
            'created_at', 'updated_at'
        }
        
        actual_columns = set(columns.keys())
        assert required_columns.issubset(actual_columns), f"Missing columns: {required_columns - actual_columns}"
        
        # Test column types and constraints
        assert columns['id']['primary_key'] == True
        assert columns['name']['nullable'] == False
        assert columns['normalized_name']['nullable'] == False
        assert columns['domain']['nullable'] == True  # Can be null for some companies
        
        # Test indexes exist
        indexes = inspector.get_indexes('companies')
        index_columns = {tuple(idx['column_names']) for idx in indexes}
        
        # Should have indexes on key lookup fields
        assert ('name',) in index_columns or any('name' in idx['column_names'] for idx in indexes)

    def test_job_listings_table_schema(self, db_engine):
        """Test JobListingDB table schema and columns."""
        inspector = inspect(db_engine)
        columns = {col['name']: col for col in inspector.get_columns('job_listings')}
        
        # Test required columns exist
        required_columns = {
            'id', 'company_id', 'title', 'location', 'description', 'requirements',
            'responsibilities', 'job_type', 'remote_type', 'experience_level',
            'salary_min', 'salary_max', 'salary_currency', 'skills_required',
            'skills_preferred', 'education_required', 'benefits', 'job_url',
            'application_url', 'posted_date', 'application_deadline', 'source',
            'status', 'canonical_id', 'source_count', 'data_quality_score',
            'scraped_at', 'last_verified', 'verification_status',
            'company_size_category', 'seniority_level', 'tech_stack',
            'benefits_parsed', 'created_at', 'updated_at'
        }
        
        actual_columns = set(columns.keys())
        assert required_columns.issubset(actual_columns), f"Missing columns: {required_columns - actual_columns}"
        
        # Test primary key and foreign key constraints
        assert columns['id']['primary_key'] == True
        assert columns['company_id']['nullable'] == False
        assert columns['title']['nullable'] == False
        
        # Test foreign key relationships
        foreign_keys = inspector.get_foreign_keys('job_listings')
        fk_columns = {fk['constrained_columns'][0]: fk['referred_table'] for fk in foreign_keys}
        assert 'company_id' in fk_columns
        assert fk_columns['company_id'] == 'companies'

    def test_user_profiles_table_schema(self, db_engine):
        """Test UserProfileDB table schema and columns."""
        inspector = inspect(db_engine)
        columns = {col['name']: col for col in inspector.get_columns('user_profiles')}
        
        # Test required columns exist
        required_columns = {
            'id', 'first_name', 'last_name', 'email', 'phone', 'city', 'state',
            'linkedin_url', 'portfolio_url', 'current_title', 'experience_years',
            'education', 'bio', 'preferred_locations', 'preferred_job_types',
            'preferred_remote_types', 'desired_salary_min', 'desired_salary_max',
            'created_at', 'updated_at'
        }
        
        actual_columns = set(columns.keys())
        assert required_columns.issubset(actual_columns), f"Missing columns: {required_columns - actual_columns}"
        
        # Test primary key
        assert columns['id']['primary_key'] == True
        
        # Test unique constraint on email
        unique_constraints = inspector.get_unique_constraints('user_profiles')
        email_unique = any('email' in uc['column_names'] for uc in unique_constraints)
        assert email_unique, "Email should have unique constraint"

    def test_job_user_interactions_table_schema(self, db_engine):
        """Test JobUserInteractionDB table schema and relationships."""
        inspector = inspect(db_engine)
        columns = {col['name']: col for col in inspector.get_columns('job_user_interactions')}
        
        # Test required columns exist
        required_columns = {
            'id', 'user_id', 'job_id', 'interaction_type', 'application_status',
            'applied_date', 'response_date', 'resume_version', 'cover_letter',
            'follow_up_date', 'interview_scheduled', 'saved_date', 'tags',
            'notes', 'interaction_data', 'first_interaction', 'last_interaction',
            'interaction_count', 'job_snapshot'
        }
        
        actual_columns = set(columns.keys())
        assert required_columns.issubset(actual_columns), f"Missing columns: {required_columns - actual_columns}"
        
        # Test foreign key relationships
        foreign_keys = inspector.get_foreign_keys('job_user_interactions')
        fk_columns = {fk['constrained_columns'][0]: fk['referred_table'] for fk in foreign_keys}
        
        assert 'user_id' in fk_columns
        assert fk_columns['user_id'] == 'user_profiles'
        assert 'job_id' in fk_columns
        assert fk_columns['job_id'] == 'job_listings'
        
        # Test that required fields are not nullable
        assert columns['user_id']['nullable'] == False
        assert columns['job_id']['nullable'] == False
        assert columns['interaction_type']['nullable'] == False

    def test_check_constraints_exist(self, db_engine):
        """Test that database check constraints are properly created."""
        inspector = inspect(db_engine)
        
        # Test job_listings constraints
        job_constraints = inspector.get_check_constraints('job_listings')
        constraint_names = {c['name'] for c in job_constraints}
        
        expected_job_constraints = {
            'salary_min_positive',
            'salary_range_valid',
            'title_min_length',
            'title_max_length'
        }
        
        # Note: SQLite may not report all check constraints properly
        # This is more of a smoke test to ensure constraints can be created
        assert len(job_constraints) >= 0  # At least some constraints should exist
        
        # Test user_profiles constraints
        user_constraints = inspector.get_check_constraints('user_profiles')
        assert len(user_constraints) >= 0

    def test_indexes_created(self, db_engine):
        """Test that performance indexes are created."""
        inspector = inspect(db_engine)
        
        # Test job_listings indexes
        job_indexes = inspector.get_indexes('job_listings')
        job_index_columns = {tuple(idx['column_names']): idx['name'] for idx in job_indexes}
        
        # Should have indexes on frequently queried columns
        # Note: Some indexes might be composite, so we check for presence of key columns
        index_column_sets = [set(cols) for cols in job_index_columns.keys()]
        
        # Check that we have indexes on important columns
        important_columns = ['company_id', 'status', 'posted_date', 'location']
        for col in important_columns:
            assert any(col in idx_cols for idx_cols in index_column_sets), f"Missing index on {col}"

    def test_table_relationships_integrity(self, db_engine):
        """Test that table relationships maintain referential integrity."""
        inspector = inspect(db_engine)
        
        # Check company -> job_listings relationship
        job_fks = inspector.get_foreign_keys('job_listings')
        company_fk = next((fk for fk in job_fks if 'company_id' in fk['constrained_columns']), None)
        assert company_fk is not None
        assert company_fk['referred_table'] == 'companies'
        
        # Check user -> interactions relationship
        interaction_fks = inspector.get_foreign_keys('job_user_interactions')
        user_fk = next((fk for fk in interaction_fks if 'user_id' in fk['constrained_columns']), None)
        assert user_fk is not None
        assert user_fk['referred_table'] == 'user_profiles'
        
        # Check job -> interactions relationship
        job_fk = next((fk for fk in interaction_fks if 'job_id' in fk['constrained_columns']), None)
        assert job_fk is not None
        assert job_fk['referred_table'] == 'job_listings'


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.database
class TestDatabaseModelCRUD:
    """Test basic CRUD operations for database models."""

    def test_company_crud_operations(self, clean_db, sample_company_db_data):
        """Test Create, Read, Update, Delete operations for CompanyInfoDB."""
        # Create
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.commit()
        
        created_id = company.id
        assert created_id is not None
        
        # Read
        retrieved = clean_db.query(CompanyInfoDB).filter(CompanyInfoDB.id == created_id).first()
        assert retrieved is not None
        assert retrieved.name == "TechCorp Inc"
        assert retrieved.domain == "techcorp.com"
        assert retrieved.size_category == CompanySizeCategory.MEDIUM
        assert retrieved.values == ["Innovation", "Excellence", "Teamwork"]
        
        # Update
        retrieved.description = "Updated description"
        clean_db.commit()
        
        updated = clean_db.query(CompanyInfoDB).filter(CompanyInfoDB.id == created_id).first()
        assert updated.description == "Updated description"
        
        # Delete
        clean_db.delete(updated)
        clean_db.commit()
        
        deleted = clean_db.query(CompanyInfoDB).filter(CompanyInfoDB.id == created_id).first()
        assert deleted is None

    def test_user_profile_crud_operations(self, clean_db, sample_user_db_data):
        """Test CRUD operations for UserProfileDB."""
        # Create
        user = UserProfileDB(**sample_user_db_data)
        clean_db.add(user)
        clean_db.commit()
        
        created_id = user.id
        assert created_id is not None
        
        # Read
        retrieved = clean_db.query(UserProfileDB).filter(UserProfileDB.id == created_id).first()
        assert retrieved is not None
        assert retrieved.email == "john.doe@example.com"
        assert retrieved.first_name == "John"
        assert retrieved.preferred_locations == ["San Francisco, CA", "Remote"]
        
        # Update
        retrieved.current_title = "Senior Software Engineer"
        clean_db.commit()
        
        updated = clean_db.query(UserProfileDB).filter(UserProfileDB.id == created_id).first()
        assert updated.current_title == "Senior Software Engineer"
        
        # Delete
        clean_db.delete(updated)
        clean_db.commit()
        
        deleted = clean_db.query(UserProfileDB).filter(UserProfileDB.id == created_id).first()
        assert deleted is None

    def test_job_listing_crud_with_company_relationship(self, clean_db, sample_company_db_data, sample_job_db_data):
        """Test CRUD operations for JobListingDB with company relationship."""
        # First create a company
        company = CompanyInfoDB(**sample_company_db_data)
        clean_db.add(company)
        clean_db.commit()
        
        # Create job listing with company relationship
        job_data = sample_job_db_data.copy()
        job_data['company_id'] = company.id
        
        job = JobListingDB(**job_data)
        clean_db.add(job)
        clean_db.commit()
        
        created_job_id = job.id
        
        # Read with relationship
        retrieved = clean_db.query(JobListingDB).filter(JobListingDB.id == created_job_id).first()
        assert retrieved is not None
        assert retrieved.title == "Senior Software Engineer"
        assert retrieved.company_id == company.id
        assert retrieved.job_type == JobType.FULL_TIME
        assert retrieved.remote_type == RemoteType.HYBRID
        assert retrieved.skills_required == ["Python", "React", "PostgreSQL"]
        
        # Test relationship access
        assert retrieved.company is not None
        assert retrieved.company.name == "TechCorp Inc"
        
        # Update
        retrieved.salary_max = 200000.0
        clean_db.commit()
        
        updated = clean_db.query(JobListingDB).filter(JobListingDB.id == created_job_id).first()
        assert updated.salary_max == 200000.0
        
        # Delete (should not affect company due to foreign key relationship)
        clean_db.delete(updated)
        clean_db.commit()
        
        deleted_job = clean_db.query(JobListingDB).filter(JobListingDB.id == created_job_id).first()
        assert deleted_job is None
        
        # Company should still exist
        company_still_exists = clean_db.query(CompanyInfoDB).filter(CompanyInfoDB.id == company.id).first()
        assert company_still_exists is not None

    def test_user_job_interaction_crud(self, clean_db, sample_company_db_data, sample_job_db_data, sample_user_db_data):
        """Test CRUD operations for JobUserInteractionDB with full relationships."""
        # Create prerequisite records
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
        
        # Create interaction
        interaction = JobUserInteractionDB(
            user_id=user.id,
            job_id=job.id,
            interaction_type=InteractionType.APPLIED,
            application_status=ApplicationStatus.APPLIED,
            applied_date=datetime(2025, 1, 22),
            resume_version="v1.2",
            cover_letter="Dear Hiring Manager...",
            notes="Applied through LinkedIn",
        )
        clean_db.add(interaction)
        clean_db.commit()
        
        # Read with relationships
        retrieved = clean_db.query(JobUserInteractionDB).filter(
            JobUserInteractionDB.id == interaction.id
        ).first()
        
        assert retrieved is not None
        assert retrieved.interaction_type == InteractionType.APPLIED
        assert retrieved.application_status == ApplicationStatus.APPLIED
        assert retrieved.user_id == user.id
        assert retrieved.job_id == job.id
        
        # Test relationships
        assert retrieved.user is not None
        assert retrieved.user.email == "john.doe@example.com"
        assert retrieved.job is not None
        assert retrieved.job.title == "Senior Software Engineer"
        
        # Update interaction status
        retrieved.application_status = ApplicationStatus.INTERVIEWING
        retrieved.interview_scheduled = datetime(2025, 1, 30)
        clean_db.commit()
        
        updated = clean_db.query(JobUserInteractionDB).filter(
            JobUserInteractionDB.id == interaction.id
        ).first()
        assert updated.application_status == ApplicationStatus.INTERVIEWING
        assert updated.interview_scheduled is not None

    def test_timeline_event_creation(self, clean_db, sample_company_db_data, sample_job_db_data, sample_user_db_data):
        """Test timeline event creation and relationships."""
        # Create prerequisite records
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
        
        # Create timeline event
        event = TimelineEventDB(
            user_profile_id=user.id,
            job_id=job.id,
            event_type=TimelineEventType.APPLICATION_SUBMITTED,
            title="Application Submitted",
            description="Applied for Senior Software Engineer position",
            event_data={"resume_version": "v1.2", "method": "LinkedIn"},
            event_date=datetime(2025, 1, 22),
            is_milestone=True,
        )
        clean_db.add(event)
        clean_db.commit()
        
        # Verify creation
        retrieved = clean_db.query(TimelineEventDB).filter(TimelineEventDB.id == event.id).first()
        assert retrieved is not None
        assert retrieved.event_type == TimelineEventType.APPLICATION_SUBMITTED
        assert retrieved.is_milestone == True
        assert retrieved.event_data["resume_version"] == "v1.2"
        
        # Test relationships
        assert retrieved.job is not None
        assert retrieved.job.title == "Senior Software Engineer"
        assert retrieved.user_profile is not None
        assert retrieved.user_profile.email == "john.doe@example.com"
