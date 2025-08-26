"""
Skill Bank API Models
Pydantic models for skill bank request/response data
"""

from datetime import date, datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from backend.data.skill_bank_models import (
    Certification,
    EducationEntry,
    EnhancedSkill,
    ExperienceContentVariation,
    ExperienceEntry,
    ProjectEntry,
    SkillCategory,
    SkillLevel,
    SummaryVariation,
)


class SkillBankCreate(BaseModel):
    """Model for creating a new skill bank"""

    user_id: UUID = Field(..., description="ID of the user who owns this skill bank")
    default_summary: Optional[str] = Field(
        None, description="Default professional summary"
    )

    # Initial skills (optional - can be added later)
    initial_skills: Optional[List[EnhancedSkill]] = Field(
        None, description="Initial skills to add to the skill bank"
    )

    class Config:
        schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "default_summary": "Experienced software engineer with expertise in Python and JavaScript",
            }
        }


class SkillBankUpdate(BaseModel):
    """Model for updating an existing skill bank"""

    default_summary: Optional[str] = Field(
        None, description="Default professional summary"
    )
    skill_categories: Optional[List[str]] = Field(
        None, description="List of skill categories"
    )

    class Config:
        schema_extra = {
            "example": {
                "default_summary": "Updated professional summary with recent achievements"
            }
        }


class SkillBankResponse(BaseModel):
    """Model for returning skill bank data"""

    id: UUID = Field(..., description="Unique identifier for the skill bank")
    user_id: UUID = Field(..., description="ID of the user who owns this skill bank")

    # Skills organized by category
    skills: Dict[str, List[EnhancedSkill]] = Field(
        default_factory=dict, description="Skills organized by category"
    )
    skill_categories: List[str] = Field(
        default_factory=list, description="Available skill categories"
    )

    # Summary variations
    default_summary: Optional[str] = Field(
        None, description="Default professional summary"
    )
    summary_variations: List[SummaryVariation] = Field(
        default_factory=list, description="Professional summary variations"
    )

    # Work experiences
    work_experiences: List[ExperienceEntry] = Field(
        default_factory=list, description="Work experience entries"
    )

    # Education entries
    education_entries: List[EducationEntry] = Field(
        default_factory=list, description="Education entries"
    )

    # Projects
    projects: List[ProjectEntry] = Field(
        default_factory=list, description="Project entries"
    )

    # Certifications
    certifications: List[Certification] = Field(
        default_factory=list, description="Certification entries"
    )

    # Content variations
    experience_content_variations: Dict[str, List[ExperienceContentVariation]] = Field(
        default_factory=dict, description="Content variations for work experiences"
    )

    # Metadata
    created_at: datetime = Field(
        ..., description="Timestamp when skill bank was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when skill bank was last updated"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "skills": {
                    "Technical Skills": [
                        {
                            "id": "skill-1",
                            "name": "Python",
                            "level": "expert",
                            "category": "technical",
                            "subcategory": "Programming Languages",
                            "years_experience": 5,
                            "proficiency_score": 0.9,
                            "description": "Expert in Python development",
                            "keywords": ["Django", "FastAPI", "Flask"],
                            "is_featured": True,
                        }
                    ]
                },
                "skill_categories": ["Technical Skills", "Soft Skills"],
                "default_summary": "Experienced software engineer",
                "summary_variations": [],
                "work_experiences": [],
                "education_entries": [],
                "projects": [],
                "certifications": [],
                "experience_content_variations": {},
                "created_at": "2023-01-15T10:30:00Z",
                "updated_at": "2023-01-20T14:45:00Z",
            }
        }


class SkillBankListResponse(BaseModel):
    """Model for returning a list of skill banks"""

    skill_banks: List[SkillBankResponse] = Field(..., description="List of skill banks")
    total: int = Field(..., description="Total number of skill banks")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")


class SkillCreate(BaseModel):
    """Model for adding a new skill to a skill bank"""

    name: str = Field(..., description="Name of the skill")
    level: SkillLevel = Field(SkillLevel.INTERMEDIATE, description="Proficiency level")
    category: SkillCategory = Field(
        SkillCategory.TECHNICAL, description="Skill category"
    )
    subcategory: Optional[str] = Field(None, description="Skill subcategory")
    years_experience: Optional[int] = Field(
        None, description="Years of experience with this skill"
    )
    proficiency_score: Optional[float] = Field(
        None, description="Proficiency score (0.0-1.0)"
    )
    description: Optional[str] = Field(None, description="Description of the skill")
    keywords: List[str] = Field(default_factory=list, description="Related keywords")
    is_featured: bool = Field(
        False, description="Whether this skill should be featured"
    )
    display_order: int = Field(0, description="Display order for sorting")

    class Config:
        schema_extra = {
            "example": {
                "name": "Python",
                "level": "expert",
                "category": "technical",
                "subcategory": "Programming Languages",
                "years_experience": 5,
                "proficiency_score": 0.9,
                "description": "Expert in Python development with focus on web applications",
                "keywords": ["Django", "FastAPI", "Flask"],
                "is_featured": True,
                "display_order": 1,
            }
        }


class SkillUpdate(BaseModel):
    """Model for updating an existing skill"""

    name: Optional[str] = Field(None, description="Name of the skill")
    level: Optional[SkillLevel] = Field(None, description="Proficiency level")
    category: Optional[SkillCategory] = Field(None, description="Skill category")
    subcategory: Optional[str] = Field(None, description="Skill subcategory")
    years_experience: Optional[int] = Field(
        None, description="Years of experience with this skill"
    )
    proficiency_score: Optional[float] = Field(
        None, description="Proficiency score (0.0-1.0)"
    )
    description: Optional[str] = Field(None, description="Description of the skill")
    keywords: Optional[List[str]] = Field(None, description="Related keywords")
    is_featured: Optional[bool] = Field(
        None, description="Whether this skill should be featured"
    )
    display_order: Optional[int] = Field(None, description="Display order for sorting")

    class Config:
        schema_extra = {"example": {"proficiency_score": 0.95, "is_featured": True}}


class ExperienceCreate(BaseModel):
    """Model for adding a new work experience to a skill bank"""

    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Position title")
    location: Optional[str] = Field(None, description="Location")
    start_date: date = Field(..., description="Start date")
    end_date: Optional[date] = Field(None, description="End date")
    is_current: bool = Field(False, description="Whether this is the current position")
    default_description: Optional[str] = Field(None, description="Default description")
    default_achievements: List[str] = Field(
        default_factory=list, description="Default achievements"
    )
    skills_used: List[str] = Field(
        default_factory=list, description="Skills used in this role"
    )
    technologies: List[str] = Field(
        default_factory=list, description="Technologies used"
    )

    class Config:
        schema_extra = {
            "example": {
                "company": "Tech Corp",
                "position": "Senior Software Engineer",
                "location": "San Francisco, CA",
                "start_date": "2020-01-15",
                "end_date": "2023-12-31",
                "is_current": False,
                "default_description": "Led development of cloud-based applications",
                "default_achievements": [
                    "Increased system performance by 40%",
                    "Mentored junior developers",
                ],
                "skills_used": ["Python", "AWS", "Docker"],
                "technologies": ["FastAPI", "PostgreSQL", "Redis"],
            }
        }


class ExperienceUpdate(BaseModel):
    """Model for updating an existing work experience"""

    company: Optional[str] = Field(None, description="Company name")
    position: Optional[str] = Field(None, description="Position title")
    location: Optional[str] = Field(None, description="Location")
    start_date: Optional[date] = Field(None, description="Start date")
    end_date: Optional[date] = Field(None, description="End date")
    is_current: Optional[bool] = Field(
        None, description="Whether this is the current position"
    )
    default_description: Optional[str] = Field(None, description="Default description")
    default_achievements: Optional[List[str]] = Field(
        None, description="Default achievements"
    )
    skills_used: Optional[List[str]] = Field(
        None, description="Skills used in this role"
    )
    technologies: Optional[List[str]] = Field(None, description="Technologies used")
