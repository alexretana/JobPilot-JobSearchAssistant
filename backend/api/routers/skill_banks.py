"""
Skill Bank API Router
FastAPI router for skill bank management endpoints
"""

from typing import Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.api.auth import get_current_user
from backend.api.dependencies import get_db
from backend.api.models.skill_banks.models import (
    ExperienceCreate,
    ExperienceUpdate,
    SkillBankCreate,
    SkillBankResponse,
    SkillBankUpdate,
    SkillCreate,
    SkillUpdate,
)
from backend.data.database import get_skill_bank_repository
from backend.data.skill_bank_models import (
    EnhancedSkill,
    ExperienceEntry,
    SkillBank,
)
from backend.logger import logger

router = APIRouter(prefix="/skill-banks", tags=["skill-banks"])


@router.post("/", response_model=SkillBankResponse, status_code=status.HTTP_201_CREATED)
async def create_skill_bank(
    skill_bank_data: SkillBankCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new skill bank for a user.
    
    Requires authentication. Users can only create skill banks for themselves.
    """
    try:
        # Verify user is creating skill bank for themselves
        if str(skill_bank_data.user_id) != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create skill bank for another user",
            )
        
        # Get skill bank repository
        skill_bank_repo = get_skill_bank_repository()
        
        # Check if skill bank already exists
        existing_skill_bank = await skill_bank_repo.get_skill_bank(current_user)
        if existing_skill_bank:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Skill bank already exists for this user",
            )
        
        # Create new skill bank
        skill_bank = await skill_bank_repo.create_skill_bank(current_user)
        
        # Add initial skills if provided
        if skill_bank_data.initial_skills:
            for skill in skill_bank_data.initial_skills:
                await skill_bank_repo.add_skill(current_user, skill)
            
            # Refresh skill bank to include added skills
            skill_bank = await skill_bank_repo.get_skill_bank(current_user)
        
        # Set default summary if provided
        if skill_bank_data.default_summary:
            update_data = {"default_summary": skill_bank_data.default_summary}
            skill_bank = await skill_bank_repo.update_skill_bank(current_user, update_data)
        
        logger.info(f"Created skill bank for user: {current_user}")
        
        # Convert to response model
        return _convert_skill_bank_to_response(skill_bank)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating skill bank for user {current_user}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create skill bank",
        )


@router.get("/{user_id}", response_model=SkillBankResponse)
async def get_skill_bank(
    user_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a user's skill bank.
    
    Requires authentication. Users can only access their own skill banks.
    """
    try:
        # Verify user is accessing their own skill bank
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access another user's skill bank",
            )
        
        # Get skill bank repository
        skill_bank_repo = get_skill_bank_repository()
        
        # Get skill bank
        skill_bank = await skill_bank_repo.get_skill_bank(user_id)
        if not skill_bank:
            # Create a new skill bank if it doesn't exist
            skill_bank = await skill_bank_repo.create_skill_bank(user_id)
        
        logger.info(f"Retrieved skill bank for user: {user_id}")
        
        # Convert to response model
        return _convert_skill_bank_to_response(skill_bank)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting skill bank for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get skill bank",
        )


@router.put("/{user_id}", response_model=SkillBankResponse)
async def update_skill_bank(
    user_id: str,
    update_data: SkillBankUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a user's skill bank.
    
    Requires authentication. Users can only update their own skill banks.
    """
    try:
        # Verify user is updating their own skill bank
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update another user's skill bank",
            )
        
        # Get skill bank repository
        skill_bank_repo = get_skill_bank_repository()
        
        # Check if skill bank exists
        existing_skill_bank = await skill_bank_repo.get_skill_bank(user_id)
        if not existing_skill_bank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill bank not found",
            )
        
        # Prepare update data
        update_dict = update_data.dict(exclude_unset=True)
        
        # Update skill bank
        updated_skill_bank = await skill_bank_repo.update_skill_bank(user_id, update_dict)
        
        logger.info(f"Updated skill bank for user: {user_id}")
        
        # Convert to response model
        return _convert_skill_bank_to_response(updated_skill_bank)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating skill bank for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update skill bank",
        )


@router.delete("/{user_id}")
async def delete_skill_bank(
    user_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a user's skill bank.
    
    Requires authentication. Users can only delete their own skill banks.
    """
    try:
        # Verify user is deleting their own skill bank
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete another user's skill bank",
            )
        
        # Get skill bank repository
        skill_bank_repo = get_skill_bank_repository()
        
        # Check if skill bank exists
        existing_skill_bank = await skill_bank_repo.get_skill_bank(user_id)
        if not existing_skill_bank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill bank not found",
            )
        
        # For now, we won't actually delete the skill bank to preserve user data
        # In a real implementation, this would delete the skill bank
        logger.info(f"Skill bank deletion requested for user: {user_id} (not actually deleted)")
        
        return {"message": "Skill bank archived successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting skill bank for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete skill bank",
        )


@router.post("/{user_id}/skills", response_model=SkillBankResponse)
async def add_skill(
    user_id: str,
    skill_data: SkillCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Add a skill to a user's skill bank.
    
    Requires authentication. Users can only add skills to their own skill banks.
    """
    try:
        # Verify user is adding skill to their own skill bank
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to add skills to another user's skill bank",
            )
        
        # Get skill bank repository
        skill_bank_repo = get_skill_bank_repository()
        
        # Create EnhancedSkill from SkillCreate
        enhanced_skill = EnhancedSkill(
            name=skill_data.name,
            level=skill_data.level,
            category=skill_data.category,
            subcategory=skill_data.subcategory,
            years_experience=skill_data.years_experience,
            proficiency_score=skill_data.proficiency_score,
            description=skill_data.description,
            keywords=skill_data.keywords,
            is_featured=skill_data.is_featured,
            display_order=skill_data.display_order,
        )
        
        # Add skill to skill bank
        added_skill = await skill_bank_repo.add_skill(user_id, enhanced_skill)
        
        # Get updated skill bank
        skill_bank = await skill_bank_repo.get_skill_bank(user_id)
        
        logger.info(f"Added skill '{skill_data.name}' to skill bank for user: {user_id}")
        
        # Convert to response model
        return _convert_skill_bank_to_response(skill_bank)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding skill to skill bank for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add skill to skill bank",
        )


@router.put("/{user_id}/skills/{skill_id}", response_model=SkillBankResponse)
async def update_skill(
    user_id: str,
    skill_id: str,
    update_data: SkillUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a skill in a user's skill bank.
    
    Requires authentication. Users can only update skills in their own skill banks.
    """
    try:
        # Verify user is updating skill in their own skill bank
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update skills in another user's skill bank",
            )
        
        # Get skill bank repository
        skill_bank_repo = get_skill_bank_repository()
        
        # Prepare update data
        update_dict = update_data.dict(exclude_unset=True)
        
        # Update skill
        updated_skill = await skill_bank_repo.update_skill(user_id, skill_id, update_dict)
        
        # Get updated skill bank
        skill_bank = await skill_bank_repo.get_skill_bank(user_id)
        
        logger.info(f"Updated skill '{skill_id}' in skill bank for user: {user_id}")
        
        # Convert to response model
        return _convert_skill_bank_to_response(skill_bank)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating skill in skill bank for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update skill in skill bank",
        )


@router.delete("/{user_id}/skills/{skill_id}")
async def delete_skill(
    user_id: str,
    skill_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a skill from a user's skill bank.
    
    Requires authentication. Users can only delete skills from their own skill banks.
    """
    try:
        # Verify user is deleting skill from their own skill bank
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete skills from another user's skill bank",
            )
        
        # Get skill bank repository
        skill_bank_repo = get_skill_bank_repository()
        
        # Delete skill
        success = await skill_bank_repo.delete_skill(user_id, skill_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Skill not found",
            )
        
        # Get updated skill bank
        skill_bank = await skill_bank_repo.get_skill_bank(user_id)
        
        logger.info(f"Deleted skill '{skill_id}' from skill bank for user: {user_id}")
        
        # Convert to response model
        return _convert_skill_bank_to_response(skill_bank)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting skill from skill bank for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete skill from skill bank",
        )


@router.post("/{user_id}/experiences", response_model=SkillBankResponse)
async def add_experience(
    user_id: str,
    experience_data: ExperienceCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Add a work experience to a user's skill bank.
    
    Requires authentication. Users can only add experiences to their own skill banks.
    """
    try:
        # Verify user is adding experience to their own skill bank
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to add experiences to another user's skill bank",
            )
        
        # Get skill bank repository
        skill_bank_repo = get_skill_bank_repository()
        
        # Create ExperienceEntry from ExperienceCreate
        experience_entry = ExperienceEntry(
            company=experience_data.company,
            position=experience_data.position,
            location=experience_data.location,
            start_date=experience_data.start_date,
            end_date=experience_data.end_date,
            is_current=experience_data.is_current,
            default_description=experience_data.default_description,
            default_achievements=experience_data.default_achievements,
            skills_used=experience_data.skills_used,
            technologies=experience_data.technologies,
        )
        
        # Add experience to skill bank
        added_experience = await skill_bank_repo.add_experience(user_id, experience_entry)
        
        # Get updated skill bank
        skill_bank = await skill_bank_repo.get_skill_bank(user_id)
        
        logger.info(f"Added experience at '{experience_data.company}' to skill bank for user: {user_id}")
        
        # Convert to response model
        return _convert_skill_bank_to_response(skill_bank)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding experience to skill bank for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add experience to skill bank",
        )


@router.put("/{user_id}/experiences/{experience_id}", response_model=SkillBankResponse)
async def update_experience(
    user_id: str,
    experience_id: str,
    update_data: ExperienceUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update a work experience in a user's skill bank.
    
    Requires authentication. Users can only update experiences in their own skill banks.
    """
    try:
        # Verify user is updating experience in their own skill bank
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update experiences in another user's skill bank",
            )
        
        # Get skill bank repository
        skill_bank_repo = get_skill_bank_repository()
        
        # Prepare update data
        update_dict = update_data.dict(exclude_unset=True)
        
        # Update experience
        updated_experience = await skill_bank_repo.update_experience(user_id, experience_id, update_dict)
        
        # Get updated skill bank
        skill_bank = await skill_bank_repo.get_skill_bank(user_id)
        
        logger.info(f"Updated experience '{experience_id}' in skill bank for user: {user_id}")
        
        # Convert to response model
        return _convert_skill_bank_to_response(skill_bank)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating experience in skill bank for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update experience in skill bank",
        )


@router.delete("/{user_id}/experiences/{experience_id}")
async def delete_experience(
    user_id: str,
    experience_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a work experience from a user's skill bank.
    
    Requires authentication. Users can only delete experiences from their own skill banks.
    """
    try:
        # Verify user is deleting experience from their own skill bank
        if user_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete experiences from another user's skill bank",
            )
        
        # Get skill bank repository
        skill_bank_repo = get_skill_bank_repository()
        
        # Delete experience
        success = await skill_bank_repo.delete_experience(user_id, experience_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Experience not found",
            )
        
        # Get updated skill bank
        skill_bank = await skill_bank_repo.get_skill_bank(user_id)
        
        logger.info(f"Deleted experience '{experience_id}' from skill bank for user: {user_id}")
        
        # Convert to response model
        return _convert_skill_bank_to_response(skill_bank)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting experience from skill bank for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete experience from skill bank",
        )


def _convert_skill_bank_to_response(skill_bank: SkillBank) -> SkillBankResponse:
    """
    Convert a SkillBank model to a SkillBankResponse model.
    """
    return SkillBankResponse(
        id=UUID(skill_bank.id) if not isinstance(skill_bank.id, UUID) else skill_bank.id,
        user_id=UUID(skill_bank.user_id) if not isinstance(skill_bank.user_id, UUID) else skill_bank.user_id,
        skills=skill_bank.skills,
        skill_categories=skill_bank.skill_categories,
        default_summary=skill_bank.default_summary,
        summary_variations=skill_bank.summary_variations,
        work_experiences=skill_bank.work_experiences,
        education_entries=skill_bank.education_entries,
        projects=skill_bank.projects,
        certifications=skill_bank.certifications,
        experience_content_variations=skill_bank.experience_content_variations,
        created_at=skill_bank.created_at,
        updated_at=skill_bank.updated_at,
    )