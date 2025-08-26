from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, Field


class GeneralStatsResponse(BaseModel):
    """Response model for general statistics"""

    total_jobs: int = Field(..., description="Total number of jobs in the system")
    total_users: int = Field(..., description="Total number of users in the system")
    total_applications: int = Field(..., description="Total number of job applications")
    total_companies: int = Field(..., description="Total number of companies")
    total_resumes: int = Field(..., description="Total number of resumes")
    total_skill_banks: int = Field(..., description="Total number of skill banks")
    total_job_sources: int = Field(..., description="Total number of job sources")
    active_users_last_24h: int = Field(
        ..., description="Number of active users in the last 24 hours"
    )
    new_jobs_last_24h: int = Field(
        ..., description="Number of new jobs added in the last 24 hours"
    )
    new_applications_last_24h: int = Field(
        ..., description="Number of new applications in the last 24 hours"
    )
    processed_at: datetime = Field(
        ..., description="Timestamp when statistics were processed"
    )


class TopCompany(BaseModel):
    """Model for a top company entry"""

    company: str = Field(..., description="Company name")
    count: int = Field(..., description="Number of jobs at this company")


class TopLocation(BaseModel):
    """Model for a top location entry"""

    location: str = Field(..., description="Location name")
    count: int = Field(..., description="Number of jobs in this location")


class TopSkill(BaseModel):
    """Model for a top skill entry"""

    skill: str = Field(..., description="Skill name")
    count: int = Field(..., description="Number of times this skill appears")


class JobStatsResponse(BaseModel):
    """Response model for job statistics"""

    total_jobs: int = Field(..., description="Total number of jobs")
    jobs_by_type: Dict[str, int] = Field(..., description="Count of jobs by job type")
    jobs_by_remote_type: Dict[str, int] = Field(
        ..., description="Count of jobs by remote type"
    )
    jobs_by_experience_level: Dict[str, int] = Field(
        ..., description="Count of jobs by experience level"
    )
    jobs_by_industry: Dict[str, int] = Field(
        ..., description="Count of jobs by industry"
    )
    jobs_by_location: Dict[str, int] = Field(
        ..., description="Count of jobs by location"
    )
    average_salary_min: float = Field(
        ..., description="Average minimum salary across all jobs"
    )
    average_salary_max: float = Field(
        ..., description="Average maximum salary across all jobs"
    )
    top_companies: List[TopCompany] = Field(
        ..., description="Top companies by job count"
    )
    top_locations: List[TopLocation] = Field(
        ..., description="Top locations by job count"
    )
    new_jobs_last_7_days: int = Field(
        ..., description="Number of new jobs in the last 7 days"
    )
    new_jobs_last_30_days: int = Field(
        ..., description="Number of new jobs in the last 30 days"
    )
    processed_at: datetime = Field(
        ..., description="Timestamp when statistics were processed"
    )


class UserStatsResponse(BaseModel):
    """Response model for user statistics"""

    total_users: int = Field(..., description="Total number of users")
    users_by_role: Dict[str, int] = Field(..., description="Count of users by role")
    users_by_status: Dict[str, int] = Field(..., description="Count of users by status")
    recent_registrations: int = Field(
        ..., description="Number of new user registrations in the last 30 days"
    )
    active_users_last_7_days: int = Field(
        ..., description="Number of active users in the last 7 days"
    )
    active_users_last_30_days: int = Field(
        ..., description="Number of active users in the last 30 days"
    )
    users_by_location: Dict[str, int] = Field(
        ..., description="Count of users by location"
    )
    average_profile_completion: float = Field(
        ..., description="Average profile completion percentage"
    )
    processed_at: datetime = Field(
        ..., description="Timestamp when statistics were processed"
    )


class TopCompanyApplied(BaseModel):
    """Model for a top company applied entry"""

    company: str = Field(..., description="Company name")
    count: int = Field(..., description="Number of applications to this company")


class ApplicationStatsResponse(BaseModel):
    """Response model for application statistics"""

    total_applications: int = Field(..., description="Total number of job applications")
    applications_by_status: Dict[str, int] = Field(
        ..., description="Count of applications by status"
    )
    applications_by_job_type: Dict[str, int] = Field(
        ..., description="Count of applications by job type"
    )
    applications_by_experience_level: Dict[str, int] = Field(
        ..., description="Count of applications by experience level"
    )
    recent_applications: int = Field(
        ..., description="Number of new applications in the last 30 days"
    )
    applications_last_7_days: int = Field(
        ..., description="Number of applications in the last 7 days"
    )
    applications_last_30_days: int = Field(
        ..., description="Number of applications in the last 30 days"
    )
    average_time_to_apply: int = Field(
        ..., description="Average time (in hours) from job posting to application"
    )
    top_companies_applied: List[TopCompanyApplied] = Field(
        ..., description="Top companies by application count"
    )
    processed_at: datetime = Field(
        ..., description="Timestamp when statistics were processed"
    )


class TopSkillResume(BaseModel):
    """Model for a top skill in resume entry"""

    skill: str = Field(..., description="Skill name")
    count: int = Field(..., description="Number of times this skill appears")


class ResumeStatsResponse(BaseModel):
    """Response model for resume statistics"""

    total_resumes: int = Field(..., description="Total number of resumes")
    resumes_by_type: Dict[str, int] = Field(..., description="Count of resumes by type")
    resumes_by_status: Dict[str, int] = Field(
        ..., description="Count of resumes by status"
    )
    recent_resumes: int = Field(
        ..., description="Number of new resumes in the last 30 days"
    )
    top_skills: List[TopSkillResume] = Field(
        ..., description="Most commonly mentioned skills"
    )
    average_resume_length: int = Field(
        ..., description="Average resume length in words"
    )
    processed_at: datetime = Field(
        ..., description="Timestamp when statistics were processed"
    )


class TopSkillBankSkill(BaseModel):
    """Model for a top skill in skill bank entry"""

    skill: str = Field(..., description="Skill name")
    count: int = Field(..., description="Number of times this skill appears")


class SkillBankStatsResponse(BaseModel):
    """Response model for skill bank statistics"""

    total_skill_banks: int = Field(..., description="Total number of skill banks")
    average_skills_per_bank: float = Field(
        ..., description="Average number of skills per skill bank"
    )
    top_skills: List[TopSkillBankSkill] = Field(
        ..., description="Most commonly added skills"
    )
    skill_categories: Dict[str, int] = Field(
        ..., description="Count of skills by category"
    )
    recent_skill_additions: int = Field(
        ..., description="Number of new skill additions in the last 30 days"
    )
    processed_at: datetime = Field(
        ..., description="Timestamp when statistics were processed"
    )


class JobSourceStatsResponse(BaseModel):
    """Response model for job source statistics"""

    total_job_sources: int = Field(..., description="Total number of job sources")
    active_job_sources: int = Field(..., description="Number of active job sources")
    sources_by_type: Dict[str, int] = Field(
        ..., description="Count of sources by type (API, Scraping, Manual)"
    )
    jobs_per_source: Dict[str, int] = Field(
        ..., description="Average number of jobs per source"
    )
    recently_scraped: int = Field(
        ..., description="Number of sources scraped in the last 24 hours"
    )
    processed_at: datetime = Field(
        ..., description="Timestamp when statistics were processed"
    )
