"""
Test for Skill Bank API Models
"""

import pytest
from datetime import date, datetime
from uuid import uuid4

def test_skill_bank_models():
    """Test that skill bank API models work correctly"""
    try:
        from backend.api.models.skill_banks.models import (
            SkillBankCreate,
            SkillBankUpdate,
            SkillBankResponse,
            SkillBankListResponse,
            SkillCreate,
            SkillUpdate,
            ExperienceCreate,
            ExperienceUpdate
        )
        from backend.data.skill_bank_models import (
            EnhancedSkill,
            SkillLevel,
            SkillCategory,
            ExperienceEntry
        )
        
        # Test creating a SkillBankCreate model
        user_id = uuid4()
        create_data = {
            "user_id": user_id,
            "default_summary": "Experienced software engineer"
        }
        
        skill_bank_create = SkillBankCreate(**create_data)
        assert skill_bank_create.user_id == user_id
        assert skill_bank_create.default_summary == "Experienced software engineer"
        
        # Test creating a SkillBankUpdate model
        update_data = {
            "default_summary": "Updated professional summary"
        }
        
        skill_bank_update = SkillBankUpdate(**update_data)
        assert skill_bank_update.default_summary == "Updated professional summary"
        
        # Test creating a SkillCreate model
        skill_create_data = {
            "name": "Python",
            "level": SkillLevel.EXPERT,
            "category": SkillCategory.TECHNICAL,
            "subcategory": "Programming Languages",
            "years_experience": 5,
            "proficiency_score": 0.9,
            "description": "Expert in Python development",
            "keywords": ["Django", "FastAPI", "Flask"],
            "is_featured": True,
            "display_order": 1
        }
        
        skill_create = SkillCreate(**skill_create_data)
        assert skill_create.name == "Python"
        assert skill_create.level == SkillLevel.EXPERT
        assert skill_create.category == SkillCategory.TECHNICAL
        assert skill_create.subcategory == "Programming Languages"
        assert skill_create.years_experience == 5
        assert skill_create.proficiency_score == 0.9
        assert skill_create.description == "Expert in Python development"
        assert "Django" in skill_create.keywords
        assert skill_create.is_featured == True
        assert skill_create.display_order == 1
        
        # Test creating a SkillUpdate model
        skill_update_data = {
            "proficiency_score": 0.95,
            "is_featured": True
        }
        
        skill_update = SkillUpdate(**skill_update_data)
        assert skill_update.proficiency_score == 0.95
        assert skill_update.is_featured == True
        
        # Test creating an ExperienceCreate model
        experience_create_data = {
            "company": "Tech Corp",
            "position": "Senior Software Engineer",
            "location": "San Francisco, CA",
            "start_date": date(2020, 1, 15),
            "end_date": date(2023, 12, 31),
            "is_current": False,
            "default_description": "Led development of cloud-based applications",
            "default_achievements": [
                "Increased system performance by 40%",
                "Mentored junior developers"
            ],
            "skills_used": ["Python", "AWS", "Docker"],
            "technologies": ["FastAPI", "PostgreSQL", "Redis"]
        }
        
        experience_create = ExperienceCreate(**experience_create_data)
        assert experience_create.company == "Tech Corp"
        assert experience_create.position == "Senior Software Engineer"
        assert experience_create.location == "San Francisco, CA"
        assert experience_create.start_date == date(2020, 1, 15)
        assert experience_create.end_date == date(2023, 12, 31)
        assert experience_create.is_current == False
        assert experience_create.default_description == "Led development of cloud-based applications"
        assert "Increased system performance by 40%" in experience_create.default_achievements
        assert "Python" in experience_create.skills_used
        assert "FastAPI" in experience_create.technologies
        
        print("All skill bank API models work correctly!")
        
    except Exception as e:
        pytest.fail(f"Failed to test skill bank API models: {e}")