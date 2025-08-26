from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from backend.data.resume_models import (
    ContactInfo,
    Education,
    ExperienceType,
    Project,
    ResumeStatus,
    ResumeType,
    SectionType,
    Skill,
    SkillLevel,
    WorkExperience,
    Certification,
)
from backend.data.models import JobListing


class ResumeCreate(BaseModel):
    """Model for creating a new resume"""
    user_id: UUID = Field(..., description="ID of the user who owns this resume")
    title: str = Field(..., description="Title of the resume")
    resume_type: ResumeType = Field(ResumeType.BASE, description="Type of resume")
    status: ResumeStatus = Field(ResumeStatus.DRAFT, description="Status of the resume")
    
    # Resume content
    contact_info: ContactInfo = Field(..., description="Contact information")
    summary: Optional[str] = Field(None, description="Professional summary")
    work_experience: List[WorkExperience] = Field(default_factory=list, description="Work experience entries")
    education: List[Education] = Field(default_factory=list, description="Education entries")
    skills: List[Skill] = Field(default_factory=list, description="Skills")
    projects: List[Project] = Field(default_factory=list, description="Projects")
    certifications: List[Certification] = Field(default_factory=list, description="Certifications")
    
    # References
    template_id: Optional[UUID] = Field(None, description="ID of the template used")
    parent_resume_id: Optional[UUID] = Field(None, description="ID of the parent resume (for versions/tailoring)")
    target_job_id: Optional[UUID] = Field(None, description="ID of the target job (for tailored resumes)")


class ResumeUpdate(BaseModel):
    """Model for updating an existing resume"""
    title: Optional[str] = Field(None, description="Title of the resume")
    status: Optional[ResumeStatus] = Field(None, description="Status of the resume")
    resume_type: Optional[ResumeType] = Field(None, description="Type of resume")
    
    # Resume content
    contact_info: Optional[ContactInfo] = Field(None, description="Contact information")
    summary: Optional[str] = Field(None, description="Professional summary")
    work_experience: Optional[List[WorkExperience]] = Field(None, description="Work experience entries")
    education: Optional[List[Education]] = Field(None, description="Education entries")
    skills: Optional[List[Skill]] = Field(None, description="Skills")
    projects: Optional[List[Project]] = Field(None, description="Projects")
    certifications: Optional[List[Certification]] = Field(None, description="Certifications")
    
    # References
    template_id: Optional[UUID] = Field(None, description="ID of the template used")
    parent_resume_id: Optional[UUID] = Field(None, description="ID of the parent resume (for versions/tailoring)")
    target_job_id: Optional[UUID] = Field(None, description="ID of the target job (for tailored resumes)")


class ResumeResponse(BaseModel):
    """Model for returning resume data"""
    id: UUID = Field(..., description="Unique identifier for the resume")
    user_id: UUID = Field(..., description="ID of the user who owns this resume")
    title: str = Field(..., description="Title of the resume")
    resume_type: ResumeType = Field(..., description="Type of resume")
    status: ResumeStatus = Field(..., description="Status of the resume")
    
    # Resume content
    contact_info: ContactInfo = Field(..., description="Contact information")
    summary: Optional[str] = Field(None, description="Professional summary")
    work_experience: List[WorkExperience] = Field(default_factory=list, description="Work experience entries")
    education: List[Education] = Field(default_factory=list, description="Education entries")
    skills: List[Skill] = Field(default_factory=list, description="Skills")
    projects: List[Project] = Field(default_factory=list, description="Projects")
    certifications: List[Certification] = Field(default_factory=list, description="Certifications")
    
    # References
    template_id: Optional[UUID] = Field(None, description="ID of the template used")
    parent_resume_id: Optional[UUID] = Field(None, description="ID of the parent resume (for versions/tailoring)")
    target_job: Optional[JobListing] = Field(None, description="Target job details (for tailored resumes)")
    
    # Metadata
    version: int = Field(1, description="Version number")
    created_at: datetime = Field(..., description="Timestamp when resume was created")
    updated_at: datetime = Field(..., description="Timestamp when resume was last updated")
    last_generated_at: Optional[datetime] = Field(None, description="Timestamp when resume was last generated")


class ResumeListResponse(BaseModel):
    """Model for returning a list of resumes"""
    resumes: List[ResumeResponse] = Field(..., description="List of resumes")
    total: int = Field(..., description="Total number of resumes")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")