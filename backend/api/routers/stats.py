from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, Depends

from backend.api.auth import get_current_user
from backend.api.models.analytics.models import (
    ApplicationStatsResponse,
    GeneralStatsResponse,
    JobSourceStatsResponse,
    JobStatsResponse,
    ResumeStatsResponse,
    SkillBankStatsResponse,
    UserStatsResponse,
    TopCompany,
    TopLocation,
    TopSkill,
    TopCompanyApplied,
    TopSkillResume,
    TopSkillBankSkill,
)

router = APIRouter(prefix="/stats", tags=["statistics"])

router = APIRouter(prefix="/stats", tags=["statistics"])


@router.get("/general", response_model=GeneralStatsResponse)
async def get_general_statistics(current_user=Depends(get_current_user)):
    """Get general system statistics (requires authentication)"""
    try:
        # In a real implementation, this would:
        # 1. Query the database for counts of various entities
        # 2. Calculate active users in the last 24 hours
        # 3. Count new entities added recently
        # 4. Return aggregated statistics
        
        # Mock implementation for now
        return GeneralStatsResponse(
            total_jobs=1250,
            total_users=850,
            total_applications=2100,
            total_companies=150,
            total_resumes=950,
            total_skill_banks=420,
            total_job_sources=25,
            active_users_last_24h=125,
            new_jobs_last_24h=45,
            new_applications_last_24h=78,
            processed_at=datetime.utcnow()
        )
    except Exception as e:
        raise Exception(f"Error fetching general statistics: {str(e)}")


@router.get("/jobs", response_model=JobStatsResponse)
async def get_job_statistics(current_user=Depends(get_current_user)):
    """Get job-related statistics (requires authentication)"""
    try:
        # In a real implementation, this would:
        # 1. Query the database for job statistics
        # 2. Aggregate data by job type, remote type, experience level, etc.
        # 3. Calculate salary averages
        # 4. Identify top companies and locations
        # 5. Count recent job additions
        
        # Mock implementation for now
        return JobStatsResponse(
            total_jobs=1250,
            jobs_by_type={
                "full_time": 850,
                "part_time": 120,
                "contract": 280
            },
            jobs_by_remote_type={
                "remote": 450,
                "hybrid": 520,
                "on_site": 280
            },
            jobs_by_experience_level={
                "entry_level": 300,
                "mid_level": 600,
                "senior_level": 350
            },
            jobs_by_industry={
                "technology": 750,
                "finance": 200,
                "healthcare": 150,
                "education": 100,
                "other": 50
            },
            jobs_by_location={
                "san_francisco_ca": 180,
                "new_york_ny": 150,
                "remote": 140,
                "austin_tx": 95,
                "seattle_wa": 85
            },
            average_salary_min=95000.0,
            average_salary_max=165000.0,
            top_companies=[
                TopCompany(company="Tech Corp", count=45),
                TopCompany(company="Innovate Inc", count=38),
                TopCompany(company="Digital Solutions", count=32),
                TopCompany(company="Future Systems", count=28),
                TopCompany(company="Global Enterprises", count=25)
            ],
            top_locations=[
                TopLocation(location="San Francisco, CA", count=180),
                TopLocation(location="New York, NY", count=150),
                TopLocation(location="Remote", count=140),
                TopLocation(location="Austin, TX", count=95),
                TopLocation(location="Seattle, WA", count=85)
            ],
            new_jobs_last_7_days=85,
            new_jobs_last_30_days=320,
            processed_at=datetime.utcnow()
        )
    except Exception as e:
        raise Exception(f"Error fetching job statistics: {str(e)}")


@router.get("/users", response_model=UserStatsResponse)
async def get_user_statistics(current_user=Depends(get_current_user)):
    """Get user-related statistics (requires authentication)"""
    try:
        # In a real implementation, this would:
        # 1. Query the database for user statistics
        # 2. Aggregate data by role, status, location
        # 3. Count recent registrations
        # 4. Calculate active users over time periods
        # 5. Compute average profile completion
        
        # Mock implementation for now
        return UserStatsResponse(
            total_users=850,
            users_by_role={
                "job_seeker": 750,
                "recruiter": 80,
                "admin": 20
            },
            users_by_status={
                "active": 720,
                "pending": 80,
                "suspended": 50
            },
            recent_registrations=45,
            active_users_last_7_days=680,
            active_users_last_30_days=780,
            users_by_location={
                "san_francisco_ca": 120,
                "new_york_ny": 110,
                "london_uk": 95,
                "remote": 85,
                "austin_tx": 75
            },
            average_profile_completion=75.5,
            processed_at=datetime.utcnow()
        )
    except Exception as e:
        raise Exception(f"Error fetching user statistics: {str(e)}")


@router.get("/applications", response_model=ApplicationStatsResponse)
async def get_application_statistics(current_user=Depends(get_current_user)):
    """Get application-related statistics (requires authentication)"""
    try:
        # In a real implementation, this would:
        # 1. Query the database for application statistics
        # 2. Aggregate data by status, job type, experience level
        # 3. Count recent applications
        # 4. Calculate average time to apply
        # 5. Identify top companies by application count
        
        # Mock implementation for now
        return ApplicationStatsResponse(
            total_applications=2100,
            applications_by_status={
                "not_applied": 500,
                "applied": 1200,
                "interviewing": 250,
                "rejected": 100,
                "accepted": 50
            },
            applications_by_job_type={
                "full_time": 1600,
                "part_time": 200,
                "contract": 300
            },
            applications_by_experience_level={
                "entry_level": 600,
                "mid_level": 1000,
                "senior_level": 500
            },
            recent_applications=180,
            applications_last_7_days=420,
            applications_last_30_days=950,
            average_time_to_apply=24,
            top_companies_applied=[
                TopCompanyApplied(company="tech_corp", count=120),
                TopCompanyApplied(company="innovate_inc", count=95),
                TopCompanyApplied(company="digital_solutions", count=80),
                TopCompanyApplied(company="future_systems", count=70),
                TopCompanyApplied(company="global_enterprises", count=65)
            ],
            processed_at=datetime.utcnow()
        )
    except Exception as e:
        raise Exception(f"Error fetching application statistics: {str(e)}")


@router.get("/resumes", response_model=ResumeStatsResponse)
async def get_resume_statistics(current_user=Depends(get_current_user)):
    """Get resume-related statistics (requires authentication)"""
    try:
        # In a real implementation, this would:
        # 1. Query the database for resume statistics
        # 2. Aggregate data by type, status
        # 3. Count recent resumes
        # 4. Identify top skills
        # 5. Calculate average resume length
        
        # Mock implementation for now
        return ResumeStatsResponse(
            total_resumes=950,
            resumes_by_type={
                "professional": 650,
                "creative": 200,
                "academic": 100
            },
            resumes_by_status={
                "draft": 150,
                "published": 700,
                "archived": 100
            },
            recent_resumes=75,
            top_skills=[
                TopSkillResume(skill="python", count=250),
                TopSkillResume(skill="javascript", count=220),
                TopSkillResume(skill="react", count=180),
                TopSkillResume(skill="aws", count=150),
                TopSkillResume(skill="docker", count=120)
            ],
            average_resume_length=450,
            processed_at=datetime.utcnow()
        )
    except Exception as e:
        raise Exception(f"Error fetching resume statistics: {str(e)}")


@router.get("/skill-banks", response_model=SkillBankStatsResponse)
async def get_skill_bank_statistics(current_user=Depends(get_current_user)):
    """Get skill bank-related statistics (requires authentication)"""
    try:
        # In a real implementation, this would:
        # 1. Query the database for skill bank statistics
        # 2. Calculate average skills per bank
        # 3. Identify top skills
        # 4. Aggregate by skill categories
        # 5. Count recent skill additions
        
        # Mock implementation for now
        return SkillBankStatsResponse(
            total_skill_banks=420,
            average_skills_per_bank=25.5,
            top_skills=[
                TopSkillBankSkill(skill="python", count=180),
                TopSkillBankSkill(skill="javascript", count=160),
                TopSkillBankSkill(skill="aws", count=140),
                TopSkillBankSkill(skill="react", count=120),
                TopSkillBankSkill(skill="docker", count=95)
            ],
            skill_categories={
                "programming_languages": 350,
                "frameworks": 280,
                "cloud_platforms": 180,
                "databases": 150,
                "devops": 120
            },
            recent_skill_additions=45,
            processed_at=datetime.utcnow()
        )
    except Exception as e:
        raise Exception(f"Error fetching skill bank statistics: {str(e)}")


@router.get("/job-sources", response_model=JobSourceStatsResponse)
async def get_job_source_statistics(current_user=Depends(get_current_user)):
    """Get job source-related statistics (requires authentication)"""
    try:
        # In a real implementation, this would:
        # 1. Query the database for job source statistics
        # 2. Count total and active job sources
        # 3. Aggregate by source type
        # 4. Calculate jobs per source
        # 5. Count recently scraped sources
        
        # Mock implementation for now
        return JobSourceStatsResponse(
            total_job_sources=25,
            active_job_sources=22,
            sources_by_type={
                "api": 10,
                "scraping": 12,
                "manual": 3
            },
            jobs_per_source={
                "linkedin": 450,
                "indeed": 320,
                "glassdoor": 280,
                "company_websites": 150,
                "other": 100
            },
            recently_scraped=8,
            processed_at=datetime.utcnow()
        )
    except Exception as e:
        raise Exception(f"Error fetching job source statistics: {str(e)}")