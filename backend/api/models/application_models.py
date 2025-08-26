from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from backend.data.models import ApplicationStatus


class JobApplicationCreate(BaseModel):
    """Model for creating a new job application"""
    job_id: UUID = Field(..., description="ID of the job being applied to")
    user_profile_id: UUID = Field(..., description="ID of the user applying")
    resume_version: Optional[str] = Field(None, description="Version/name of resume used")
    cover_letter: Optional[str] = Field(None, description="Cover letter text")
    notes: Optional[str] = Field(None, description="Additional notes about the application")


class JobApplicationUpdate(BaseModel):
    """Model for updating an existing job application"""
    status: Optional[ApplicationStatus] = Field(None, description="Application status")
    response_date: Optional[datetime] = Field(None, description="Date of employer response")
    notes: Optional[str] = Field(None, description="Additional notes about the application")
    resume_version: Optional[str] = Field(None, description="Version/name of resume used")
    cover_letter: Optional[str] = Field(None, description="Cover letter text")
    follow_up_date: Optional[datetime] = Field(None, description="Date for follow-up")
    interview_scheduled: Optional[datetime] = Field(None, description="Scheduled interview date")


class JobApplicationResponse(BaseModel):
    """Model for returning job application data"""
    id: UUID = Field(..., description="Unique identifier for the application")
    job_id: UUID = Field(..., description="ID of the job being applied to")
    user_profile_id: UUID = Field(..., description="ID of the user applying")
    status: ApplicationStatus = Field(..., description="Application status")
    applied_date: Optional[datetime] = Field(None, description="Date application was submitted")
    response_date: Optional[datetime] = Field(None, description="Date of employer response")
    resume_version: Optional[str] = Field(None, description="Version/name of resume used")
    cover_letter: Optional[str] = Field(None, description="Cover letter text")
    notes: Optional[str] = Field(None, description="Additional notes about the application")
    follow_up_date: Optional[datetime] = Field(None, description="Date for follow-up")
    interview_scheduled: Optional[datetime] = Field(None, description="Scheduled interview date")
    created_at: datetime = Field(..., description="Timestamp when record was created")
    updated_at: datetime = Field(..., description="Timestamp when record was last updated")


class JobApplicationListResponse(BaseModel):
    """Model for returning a list of job applications"""
    applications: List[JobApplicationResponse] = Field(..., description="List of job applications")
    total: int = Field(..., description="Total number of applications")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")