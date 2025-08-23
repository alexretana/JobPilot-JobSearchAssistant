"""
Cross-model serialization and integration tests.

Tests serialization/deserialization across multiple models, relationship handling,
and complex data flow scenarios for all Pydantic models.
"""

import pytest
from datetime import datetime
from uuid import uuid4, UUID
from typing import Dict, Any

from backend.data.models import (
    JobListing,
    UserProfile,
    JobApplication,
    CompanyInfo,
    ApplicationStatus,
    JobType,
    RemoteType,
    ExperienceLevel,
    JobStatus,
)


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestCrossModelSerialization:
    """Test serialization across multiple models."""

    def test_complete_job_application_workflow_serialization(self):
        """Test serialization of a complete job application workflow."""
        # Create related entities
        company_id = uuid4()
        job_id = uuid4()
        user_id = uuid4()
        
        # 1. Company Info
        company = CompanyInfo(
            id=company_id,
            name="TechCorp Inc",
            industry="Technology",
            size="100-500 employees",
            location="San Francisco, CA",
            benefits=["Health Insurance", "401k", "Stock Options"],
        )
        
        # 2. Job Listing
        job = JobListing(
            id=job_id,
            title="Senior Software Engineer",
            company_id=company_id,
            company_name=company.name,
            description="Great opportunity for a senior engineer",
            job_type=JobType.FULL_TIME,
            remote_type=RemoteType.HYBRID,
            salary_min=120000.0,
            salary_max=180000.0,
            skills_required=["Python", "React", "PostgreSQL"],
            status=JobStatus.ACTIVE,
        )
        
        # 3. User Profile
        user = UserProfile(
            id=user_id,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            current_title="Software Engineer",
            experience_years=5,
            preferred_job_types=[JobType.FULL_TIME],
            preferred_remote_types=[RemoteType.HYBRID, RemoteType.REMOTE],
            desired_salary_min=110000.0,
            desired_salary_max=160000.0,
        )
        
        # 4. Job Application
        application = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            status=ApplicationStatus.APPLIED,
            applied_date=datetime(2025, 1, 20),
            resume_version="v1.2",
            cover_letter="Dear Hiring Manager, I'm very interested...",
            notes="Applied through LinkedIn",
        )
        
        # Test serialization of all models
        company_dict = company.model_dump() if hasattr(company, 'model_dump') else company.dict()
        job_dict = job.model_dump() if hasattr(job, 'model_dump') else job.dict()
        user_dict = user.model_dump() if hasattr(user, 'model_dump') else user.dict()
        app_dict = application.model_dump() if hasattr(application, 'model_dump') else application.dict()
        
        # Verify relationships are preserved
        assert company_dict["id"] == company_id
        assert job_dict["company_id"] == company_id
        assert job_dict["company_name"] == company.name
        assert app_dict["job_id"] == job_id
        assert app_dict["user_profile_id"] == user_id
        
        # Test that we can reconstruct the models
        reconstructed_company = CompanyInfo(**company_dict)
        reconstructed_job = JobListing(**job_dict)
        reconstructed_user = UserProfile(**user_dict)
        reconstructed_app = JobApplication(**app_dict)
        
        # Verify reconstructed models match originals
        assert reconstructed_company.name == company.name
        assert reconstructed_job.title == job.title
        assert reconstructed_user.email == user.email
        assert reconstructed_app.status == application.status

    def test_bulk_model_serialization(self):
        """Test serialization of multiple instances of each model type."""
        companies = []
        jobs = []
        users = []
        applications = []
        
        # Create multiple instances of each model
        for i in range(3):
            company_id = uuid4()
            job_id = uuid4()
            user_id = uuid4()
            
            company = CompanyInfo(
                id=company_id,
                name=f"Company {i}",
                industry=f"Industry {i}",
                size=f"{i*100}-{(i+1)*100} employees"
            )
            companies.append(company)
            
            job = JobListing(
                id=job_id,
                title=f"Job {i}",
                company_id=company_id,
                salary_min=50000.0 + (i * 10000),
                salary_max=100000.0 + (i * 10000),
            )
            jobs.append(job)
            
            user = UserProfile(
                id=user_id,
                first_name=f"User{i}",
                last_name="Doe",
                email=f"user{i}@example.com",
                experience_years=i + 1,
            )
            users.append(user)
            
            application = JobApplication(
                job_id=job_id,
                user_profile_id=user_id,
                status=ApplicationStatus.APPLIED,
                notes=f"Application {i}",
            )
            applications.append(application)
        
        # Test bulk serialization
        companies_data = [c.model_dump() if hasattr(c, 'model_dump') else c.dict() for c in companies]
        jobs_data = [j.model_dump() if hasattr(j, 'model_dump') else j.dict() for j in jobs]
        users_data = [u.model_dump() if hasattr(u, 'model_dump') else u.dict() for u in users]
        apps_data = [a.model_dump() if hasattr(a, 'model_dump') else a.dict() for a in applications]
        
        # Verify all data is serialized
        assert len(companies_data) == 3
        assert len(jobs_data) == 3
        assert len(users_data) == 3
        assert len(apps_data) == 3
        
        # Verify specific data
        assert companies_data[0]["name"] == "Company 0"
        assert jobs_data[1]["title"] == "Job 1"
        assert users_data[2]["email"] == "user2@example.com"
        assert apps_data[0]["notes"] == "Application 0"
        
        # Test bulk deserialization
        reconstructed_companies = [CompanyInfo(**data) for data in companies_data]
        reconstructed_jobs = [JobListing(**data) for data in jobs_data]
        reconstructed_users = [UserProfile(**data) for data in users_data]
        reconstructed_apps = [JobApplication(**data) for data in apps_data]
        
        # Verify reconstruction
        assert len(reconstructed_companies) == 3
        assert reconstructed_companies[1].name == "Company 1"
        assert reconstructed_jobs[2].title == "Job 2"
        assert reconstructed_users[0].email == "user0@example.com"
        assert reconstructed_apps[1].notes == "Application 1"

    def test_nested_model_data_structure(self):
        """Test creating complex nested data structures with multiple models."""
        company_id = uuid4()
        
        # Create a company
        company = CompanyInfo(
            id=company_id,
            name="MegaTech Corp",
            industry="Software Development",
            size="500-1000 employees",
            values=["Innovation", "Excellence", "Teamwork"],
            benefits=["Health Insurance", "401k", "Stock Options", "Flexible PTO"],
        )
        
        # Create multiple jobs for the company
        job_ids = [uuid4() for _ in range(3)]
        jobs = [
            JobListing(
                id=job_ids[0],
                title="Senior Frontend Developer",
                company_id=company_id,
                company_name=company.name,
                job_type=JobType.FULL_TIME,
                remote_type=RemoteType.REMOTE,
                salary_min=100000.0,
                skills_required=["React", "TypeScript", "CSS"],
            ),
            JobListing(
                id=job_ids[1],
                title="Backend Engineer",
                company_id=company_id,
                company_name=company.name,
                job_type=JobType.FULL_TIME,
                remote_type=RemoteType.HYBRID,
                salary_min=110000.0,
                skills_required=["Python", "Django", "PostgreSQL"],
            ),
            JobListing(
                id=job_ids[2],
                title="DevOps Specialist",
                company_id=company_id,
                company_name=company.name,
                job_type=JobType.CONTRACT,
                remote_type=RemoteType.REMOTE,
                salary_min=120000.0,
                skills_required=["AWS", "Docker", "Kubernetes"],
            ),
        ]
        
        # Create multiple users
        user_ids = [uuid4() for _ in range(2)]
        users = [
            UserProfile(
                id=user_ids[0],
                first_name="Alice",
                last_name="Johnson",
                email="alice@example.com",
                current_title="Frontend Developer",
                experience_years=4,
                preferred_job_types=[JobType.FULL_TIME],
                preferred_remote_types=[RemoteType.REMOTE],
            ),
            UserProfile(
                id=user_ids[1],
                first_name="Bob",
                last_name="Smith",
                email="bob@example.com",
                current_title="DevOps Engineer",
                experience_years=6,
                preferred_job_types=[JobType.FULL_TIME, JobType.CONTRACT],
                preferred_remote_types=[RemoteType.REMOTE, RemoteType.HYBRID],
            ),
        ]
        
        # Create applications (multiple users applying to multiple jobs)
        applications = [
            JobApplication(
                job_id=job_ids[0],  # Frontend job
                user_profile_id=user_ids[0],  # Alice
                status=ApplicationStatus.APPLIED,
                notes="Perfect match for frontend skills",
            ),
            JobApplication(
                job_id=job_ids[2],  # DevOps job
                user_profile_id=user_ids[1],  # Bob
                status=ApplicationStatus.INTERVIEWING,
                notes="Strong DevOps background",
            ),
            JobApplication(
                job_id=job_ids[1],  # Backend job
                user_profile_id=user_ids[0],  # Alice (applying to multiple jobs)
                status=ApplicationStatus.NOT_APPLIED,
                notes="Considering backend transition",
            ),
        ]
        
        # Create nested data structure
        company_data = {
            "company": company.model_dump() if hasattr(company, 'model_dump') else company.dict(),
            "jobs": [j.model_dump() if hasattr(j, 'model_dump') else j.dict() for j in jobs],
            "users": [u.model_dump() if hasattr(u, 'model_dump') else u.dict() for u in users],
            "applications": [a.model_dump() if hasattr(a, 'model_dump') else a.dict() for a in applications],
            "metadata": {
                "total_jobs": len(jobs),
                "total_users": len(users),
                "total_applications": len(applications),
                "created_at": datetime.utcnow(),
            }
        }
        
        # Verify nested structure
        assert company_data["company"]["name"] == "MegaTech Corp"
        assert len(company_data["jobs"]) == 3
        assert len(company_data["users"]) == 2
        assert len(company_data["applications"]) == 3
        assert company_data["metadata"]["total_jobs"] == 3
        
        # Verify relationships are preserved
        frontend_job = company_data["jobs"][0]
        alice_user = company_data["users"][0]
        alice_frontend_app = company_data["applications"][0]
        
        assert frontend_job["title"] == "Senior Frontend Developer"
        assert alice_user["first_name"] == "Alice"
        assert alice_frontend_app["job_id"] == frontend_job["id"]
        assert alice_frontend_app["user_profile_id"] == alice_user["id"]
        
        # Test reconstruction from nested structure
        reconstructed_company = CompanyInfo(**company_data["company"])
        reconstructed_jobs = [JobListing(**job_data) for job_data in company_data["jobs"]]
        reconstructed_users = [UserProfile(**user_data) for user_data in company_data["users"]]
        reconstructed_apps = [JobApplication(**app_data) for app_data in company_data["applications"]]
        
        # Verify reconstruction maintains relationships
        assert reconstructed_company.id == company_id
        assert len(reconstructed_jobs) == 3
        assert all(job.company_id == company_id for job in reconstructed_jobs)
        assert reconstructed_apps[0].job_id in job_ids
        assert reconstructed_apps[0].user_profile_id in user_ids

    def test_json_serialization_compatibility(self):
        """Test JSON serialization compatibility across all models."""
        import json
        
        # Create instances of all models
        company = CompanyInfo(name="JsonTest Corp")
        
        job = JobListing(
            title="Test Job",
            company_id=company.id,
            job_type=JobType.FULL_TIME,
        )
        
        user = UserProfile(
            first_name="Test",
            last_name="User",
            email="test@example.com",
        )
        
        application = JobApplication(
            job_id=job.id,
            user_profile_id=user.id,
        )
        
        models = {
            "company": company,
            "job": job,
            "user": user,
            "application": application,
        }
        
        # Test JSON serialization for each model
        for model_name, model_instance in models.items():
            # Test model's built-in JSON method
            if hasattr(model_instance, 'model_dump_json'):
                json_str = model_instance.model_dump_json()  # Pydantic v2
            else:
                json_str = model_instance.json()  # Pydantic v1
            
            assert isinstance(json_str, str)
            
            # Verify JSON is valid
            parsed_data = json.loads(json_str)
            assert isinstance(parsed_data, dict)
            
            # Test manual JSON serialization of dict
            model_dict = model_instance.model_dump() if hasattr(model_instance, 'model_dump') else model_instance.dict()
            
            # Handle UUID and datetime serialization for manual JSON
            def serialize_special_types(obj):
                if isinstance(obj, UUID):
                    return str(obj)
                elif isinstance(obj, datetime):
                    return obj.isoformat()
                raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
            
            manual_json_str = json.dumps(model_dict, default=serialize_special_types)
            manual_parsed_data = json.loads(manual_json_str)
            
            assert isinstance(manual_parsed_data, dict)
            assert "id" in manual_parsed_data


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestModelInteractionPatterns:
    """Test common interaction patterns between models."""

    def test_job_matching_scenario(self):
        """Test serialization for a job matching scenario."""
        # Create a user looking for jobs
        user = UserProfile(
            first_name="Sarah",
            last_name="Connor",
            email="sarah.connor@example.com",
            current_title="Software Engineer",
            experience_years=3,
            preferred_job_types=[JobType.FULL_TIME],
            preferred_remote_types=[RemoteType.REMOTE, RemoteType.HYBRID],
            desired_salary_min=80000.0,
            desired_salary_max=120000.0,
            preferred_locations=["Remote", "San Francisco, CA"],
        )
        
        # Create companies and jobs
        companies_and_jobs = []
        
        for i, (company_name, job_title, salary, remote_type) in enumerate([
            ("TechStartup", "Frontend Developer", 85000.0, RemoteType.REMOTE),
            ("BigCorp", "Full Stack Engineer", 110000.0, RemoteType.HYBRID),
            ("ConsultingFirm", "Senior Developer", 95000.0, RemoteType.ON_SITE),
        ]):
            company = CompanyInfo(
                name=company_name,
                industry="Technology",
                size=f"{(i+1)*100}-{(i+2)*100} employees",
            )
            
            job = JobListing(
                title=job_title,
                company_id=company.id,
                company_name=company.name,
                job_type=JobType.FULL_TIME,
                remote_type=remote_type,
                salary_min=salary,
                salary_max=salary + 20000.0,
                location="San Francisco, CA" if remote_type != RemoteType.REMOTE else "Remote",
                skills_required=["JavaScript", "React", "Node.js"],
            )
            
            companies_and_jobs.append((company, job))
        
        # Serialize matching data
        matching_data = {
            "user": user.model_dump() if hasattr(user, 'model_dump') else user.dict(),
            "opportunities": []
        }
        
        for company, job in companies_and_jobs:
            # Simple matching logic based on salary and remote type
            salary_match = (
                job.salary_min <= user.desired_salary_max and
                job.salary_max >= user.desired_salary_min
            )
            remote_match = job.remote_type in user.preferred_remote_types
            
            opportunity = {
                "company": company.model_dump() if hasattr(company, 'model_dump') else company.dict(),
                "job": job.model_dump() if hasattr(job, 'model_dump') else job.dict(),
                "match_score": {
                    "salary_match": salary_match,
                    "remote_match": remote_match,
                    "overall_score": (salary_match + remote_match) / 2,
                },
            }
            
            matching_data["opportunities"].append(opportunity)
        
        # Verify matching data structure
        assert len(matching_data["opportunities"]) == 3
        assert matching_data["user"]["email"] == "sarah.connor@example.com"
        
        # Check specific matches
        remote_job = matching_data["opportunities"][0]  # TechStartup remote job
        hybrid_job = matching_data["opportunities"][1]   # BigCorp hybrid job
        onsite_job = matching_data["opportunities"][2]   # ConsultingFirm on-site job
        
        assert remote_job["match_score"]["remote_match"] is True
        assert hybrid_job["match_score"]["remote_match"] is True
        assert onsite_job["match_score"]["remote_match"] is False
        
        assert remote_job["match_score"]["salary_match"] is True
        assert hybrid_job["match_score"]["salary_match"] is True
        assert onsite_job["match_score"]["salary_match"] is True

    def test_application_tracking_serialization(self):
        """Test serialization for application tracking across time."""
        job_id = uuid4()
        user_id = uuid4()
        
        # Create initial application
        initial_application = JobApplication(
            job_id=job_id,
            user_profile_id=user_id,
            status=ApplicationStatus.NOT_APPLIED,
            notes="Initial interest in position",
        )
        
        # Simulate application status changes over time
        application_timeline = []
        
        statuses_and_updates = [
            (ApplicationStatus.APPLIED, "Applied with resume v1.2", datetime(2025, 1, 15)),
            (ApplicationStatus.INTERVIEWING, "Phone screening scheduled", datetime(2025, 1, 22)),
            (ApplicationStatus.INTERVIEWING, "Technical interview completed", datetime(2025, 1, 28)),
            (ApplicationStatus.ACCEPTED, "Offer received!", datetime(2025, 2, 5)),
        ]
        
        current_app = initial_application
        for status, note, date in statuses_and_updates:
            # Create updated application
            if hasattr(current_app, 'model_copy'):
                updated_app = current_app.model_copy(update={
                    "status": status,
                    "notes": note,
                    "applied_date": date if status == ApplicationStatus.APPLIED else current_app.applied_date,
                    "interview_scheduled": date if status == ApplicationStatus.INTERVIEWING and "scheduled" in note else current_app.interview_scheduled,
                    "response_date": date if status == ApplicationStatus.ACCEPTED else current_app.response_date,
                })
            else:
                updated_app = current_app.copy(update={
                    "status": status,
                    "notes": note,
                    "applied_date": date if status == ApplicationStatus.APPLIED else current_app.applied_date,
                    "interview_scheduled": date if status == ApplicationStatus.INTERVIEWING and "scheduled" in note else current_app.interview_scheduled,
                    "response_date": date if status == ApplicationStatus.ACCEPTED else current_app.response_date,
                })
            
            # Add to timeline
            timeline_entry = {
                "timestamp": date,
                "application": updated_app.model_dump() if hasattr(updated_app, 'model_dump') else updated_app.dict(),
                "change": f"Status changed to {status.value}",
            }
            
            application_timeline.append(timeline_entry)
            current_app = updated_app
        
        # Verify timeline serialization
        assert len(application_timeline) == 4
        assert application_timeline[0]["application"]["status"] == ApplicationStatus.APPLIED
        assert application_timeline[1]["application"]["status"] == ApplicationStatus.INTERVIEWING
        assert application_timeline[3]["application"]["status"] == ApplicationStatus.ACCEPTED
        
        # Verify dates are preserved
        assert application_timeline[0]["timestamp"] == datetime(2025, 1, 15)
        assert application_timeline[3]["timestamp"] == datetime(2025, 2, 5)
        
        # Test reconstruction of timeline
        reconstructed_timeline = []
        for entry in application_timeline:
            reconstructed_app = JobApplication(**entry["application"])
            reconstructed_entry = {
                "timestamp": entry["timestamp"],
                "application": reconstructed_app,
                "change": entry["change"],
            }
            reconstructed_timeline.append(reconstructed_entry)
        
        # Verify reconstruction
        assert len(reconstructed_timeline) == 4
        assert reconstructed_timeline[0]["application"].status == ApplicationStatus.APPLIED
        assert reconstructed_timeline[3]["application"].status == ApplicationStatus.ACCEPTED


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.data
class TestSerializationPerformance:
    """Test serialization performance and edge cases."""

    def test_large_scale_serialization(self):
        """Test serialization performance with larger datasets."""
        # Create a moderate number of models for testing
        num_companies = 10
        jobs_per_company = 5
        num_users = 20
        applications_per_user = 3
        
        companies = []
        all_jobs = []
        users = []
        all_applications = []
        
        # Create companies and jobs
        for i in range(num_companies):
            company = CompanyInfo(
                name=f"Company {i}",
                industry=f"Industry {i % 3}",  # Rotate through 3 industries
                size=f"{i*50}-{(i+1)*50} employees",
                benefits=[f"Benefit {j}" for j in range(5)],  # 5 benefits each
            )
            companies.append(company)
            
            # Create jobs for this company
            for j in range(jobs_per_company):
                job = JobListing(
                    title=f"Job {i}-{j}",
                    company_id=company.id,
                    company_name=company.name,
                    salary_min=50000.0 + (j * 10000),
                    salary_max=80000.0 + (j * 10000),
                    skills_required=[f"Skill_{k}" for k in range(j + 1)],  # Variable number of skills
                )
                all_jobs.append(job)
        
        # Create users
        for i in range(num_users):
            user = UserProfile(
                first_name=f"User{i}",
                last_name="LastName",
                email=f"user{i}@example.com",
                experience_years=i % 10,  # 0-9 years
                preferred_locations=[f"Location {j}" for j in range(i % 3 + 1)],  # Variable locations
            )
            users.append(user)
        
        # Create applications
        import random
        for i, user in enumerate(users):
            # Each user applies to a random subset of jobs
            sample_size = min(applications_per_user, len(all_jobs))
            selected_jobs = random.sample(all_jobs, sample_size)
            
            for job in selected_jobs:
                application = JobApplication(
                    job_id=job.id,
                    user_profile_id=user.id,
                    status=random.choice(list(ApplicationStatus)),
                    notes=f"Application from user {i}",
                )
                all_applications.append(application)
        
        # Test bulk serialization
        companies_data = [c.model_dump() if hasattr(c, 'model_dump') else c.dict() for c in companies]
        jobs_data = [j.model_dump() if hasattr(j, 'model_dump') else j.dict() for j in all_jobs]
        users_data = [u.model_dump() if hasattr(u, 'model_dump') else u.dict() for u in users]
        applications_data = [a.model_dump() if hasattr(a, 'model_dump') else a.dict() for a in all_applications]
        
        # Verify serialization completed
        assert len(companies_data) == num_companies
        assert len(jobs_data) == num_companies * jobs_per_company
        assert len(users_data) == num_users
        assert len(applications_data) == num_users * applications_per_user
        
        # Test bulk deserialization
        reconstructed_companies = [CompanyInfo(**data) for data in companies_data]
        reconstructed_jobs = [JobListing(**data) for data in jobs_data]
        reconstructed_users = [UserProfile(**data) for data in users_data]
        reconstructed_applications = [JobApplication(**data) for data in applications_data]
        
        # Verify reconstruction
        assert len(reconstructed_companies) == num_companies
        assert len(reconstructed_jobs) == num_companies * jobs_per_company
        assert len(reconstructed_users) == num_users
        assert len(reconstructed_applications) == num_users * applications_per_user
        
        # Spot check some data integrity
        assert reconstructed_companies[0].name == "Company 0"
        assert reconstructed_jobs[5].title == "Job 1-0"  # Second company, first job
        assert reconstructed_users[10].email == "user10@example.com"
        assert len([app for app in reconstructed_applications if app.status == ApplicationStatus.APPLIED]) >= 0
