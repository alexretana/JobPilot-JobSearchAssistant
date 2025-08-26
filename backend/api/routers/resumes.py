from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.api.auth import get_current_user
from backend.api.dependencies import get_db
from backend.api.models.resumes.models import (
    ResumeCreate,
    ResumeListResponse,
    ResumeResponse,
    ResumeUpdate,
)
from backend.data.database import get_resume_repository
from backend.data.resume_models import ResumeStatus, ResumeType
from backend.logger import logger

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.get("/", response_model=ResumeListResponse)
async def list_resumes(
    status: Optional[ResumeStatus] = Query(None, description="Filter by resume status"),
    resume_type: Optional[ResumeType] = Query(
        None, description="Filter by resume type"
    ),
    limit: int = Query(50, description="Number of resumes to return", le=100),
    offset: int = Query(0, description="Number of resumes to skip"),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all resumes for the current user with optional filtering and pagination"""
    try:
        resume_repo = get_resume_repository()

        # Get user's resumes with filtering
        resumes = await resume_repo.get_user_resumes(
            user_id=current_user, status=status
        )

        # Apply pagination
        total_resumes = len(resumes)
        paginated_resumes = resumes[offset : offset + limit]

        # Convert to response models
        resume_responses = []
        for resume in paginated_resumes:
            # Get target job details if resume is tailored
            target_job = None
            if resume.job_id:
                from backend.data.database import get_job_repository

                job_repo = get_job_repository()
                job = job_repo.get_job(str(resume.job_id))
                if job:
                    target_job = job

            resume_response = ResumeResponse(
                id=UUID(resume.id) if not isinstance(resume.id, UUID) else resume.id,
                user_id=(
                    UUID(resume.user_id)
                    if not isinstance(resume.user_id, UUID)
                    else resume.user_id
                ),
                title=resume.title,
                resume_type=resume.resume_type,
                status=resume.status,
                contact_info=resume.contact_info,
                summary=resume.summary,
                work_experience=resume.work_experience,
                education=resume.education,
                skills=resume.skills,
                projects=resume.projects,
                certifications=resume.certifications,
                template_id=(
                    UUID(resume.template_id)
                    if resume.template_id and not isinstance(resume.template_id, UUID)
                    else resume.template_id
                ),
                parent_resume_id=(
                    UUID(resume.based_on_resume_id)
                    if resume.based_on_resume_id
                    and not isinstance(resume.based_on_resume_id, UUID)
                    else resume.based_on_resume_id
                ),
                target_job=target_job,
                version=resume.version,
                created_at=resume.created_at or datetime.utcnow(),
                updated_at=resume.updated_at or datetime.utcnow(),
                last_generated_at=resume.last_generated_at,
            )
            resume_responses.append(resume_response)

        return ResumeListResponse(
            resumes=resume_responses,
            total=total_resumes,
            page=offset // limit + 1 if limit > 0 else 1,
            page_size=limit,
        )
    except Exception as e:
        logger.error(f"Error listing resumes for user {current_user}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list resumes",
        )


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific resume by ID"""
    try:
        resume_repo = get_resume_repository()
        resume = await resume_repo.get_resume(resume_id, current_user)

        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found",
            )

        # Get target job details if resume is tailored
        target_job = None
        if resume.job_id:
            from backend.data.database import get_job_repository

            job_repo = get_job_repository()
            job = job_repo.get_job(str(resume.job_id))
            if job:
                target_job = job

        return ResumeResponse(
            id=UUID(resume.id) if not isinstance(resume.id, UUID) else resume.id,
            user_id=(
                UUID(resume.user_id)
                if not isinstance(resume.user_id, UUID)
                else resume.user_id
            ),
            title=resume.title,
            resume_type=resume.resume_type,
            status=resume.status,
            contact_info=resume.contact_info,
            summary=resume.summary,
            work_experience=resume.work_experience,
            education=resume.education,
            skills=resume.skills,
            projects=resume.projects,
            certifications=resume.certifications,
            template_id=(
                UUID(resume.template_id)
                if resume.template_id and not isinstance(resume.template_id, UUID)
                else resume.template_id
            ),
            parent_resume_id=(
                UUID(resume.based_on_resume_id)
                if resume.based_on_resume_id
                and not isinstance(resume.based_on_resume_id, UUID)
                else resume.based_on_resume_id
            ),
            target_job=target_job,
            version=resume.version,
            created_at=resume.created_at or datetime.utcnow(),
            updated_at=resume.updated_at or datetime.utcnow(),
            last_generated_at=resume.last_generated_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting resume {resume_id} for user {current_user}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get resume",
        )


@router.post("/", response_model=ResumeResponse)
async def create_resume(
    resume_data: ResumeCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new resume"""
    try:
        # Verify user is creating resume for themselves
        if str(resume_data.user_id) != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create resume for another user",
            )

        resume_repo = get_resume_repository()
        resume_db = await resume_repo.create_resume(resume_data)

        if not resume_db:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create resume",
            )

        # Convert back to Pydantic model
        resume = resume_repo._db_to_pydantic(resume_db)

        # Get target job details if resume is tailored
        target_job = None
        if resume.job_id:
            from backend.data.database import get_job_repository

            job_repo = get_job_repository()
            job = job_repo.get_job(str(resume.job_id))
            if job:
                target_job = job

        return ResumeResponse(
            id=UUID(resume.id) if not isinstance(resume.id, UUID) else resume.id,
            user_id=(
                UUID(resume.user_id)
                if not isinstance(resume.user_id, UUID)
                else resume.user_id
            ),
            title=resume.title,
            resume_type=resume.resume_type,
            status=resume.status,
            contact_info=resume.contact_info,
            summary=resume.summary,
            work_experience=resume.work_experience,
            education=resume.education,
            skills=resume.skills,
            projects=resume.projects,
            certifications=resume.certifications,
            template_id=(
                UUID(resume.template_id)
                if resume.template_id and not isinstance(resume.template_id, UUID)
                else resume.template_id
            ),
            parent_resume_id=(
                UUID(resume.based_on_resume_id)
                if resume.based_on_resume_id
                and not isinstance(resume.based_on_resume_id, UUID)
                else resume.based_on_resume_id
            ),
            target_job=target_job,
            version=resume.version,
            created_at=resume.created_at or datetime.utcnow(),
            updated_at=resume.updated_at or datetime.utcnow(),
            last_generated_at=resume.last_generated_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating resume for user {current_user}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create resume",
        )


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: str,
    update_data: ResumeUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an existing resume"""
    try:
        resume_repo = get_resume_repository()

        # Check if resume exists and belongs to user
        existing_resume = await resume_repo.get_resume(resume_id, current_user)
        if not existing_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found",
            )

        # Prepare update data
        update_dict = update_data.dict(exclude_unset=True)

        # Update the resume
        updated_resume = await resume_repo.update_resume(
            resume_id, current_user, update_dict
        )

        if not updated_resume:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update resume",
            )

        # Get target job details if resume is tailored
        target_job = None
        if updated_resume.job_id:
            from backend.data.database import get_job_repository

            job_repo = get_job_repository()
            job = job_repo.get_job(str(updated_resume.job_id))
            if job:
                target_job = job

        return ResumeResponse(
            id=(
                UUID(updated_resume.id)
                if not isinstance(updated_resume.id, UUID)
                else updated_resume.id
            ),
            user_id=(
                UUID(updated_resume.user_id)
                if not isinstance(updated_resume.user_id, UUID)
                else updated_resume.user_id
            ),
            title=updated_resume.title,
            resume_type=updated_resume.resume_type,
            status=updated_resume.status,
            contact_info=updated_resume.contact_info,
            summary=updated_resume.summary,
            work_experience=updated_resume.work_experience,
            education=updated_resume.education,
            skills=updated_resume.skills,
            projects=updated_resume.projects,
            certifications=updated_resume.certifications,
            template_id=(
                UUID(updated_resume.template_id)
                if updated_resume.template_id
                and not isinstance(updated_resume.template_id, UUID)
                else updated_resume.template_id
            ),
            parent_resume_id=(
                UUID(updated_resume.based_on_resume_id)
                if updated_resume.based_on_resume_id
                and not isinstance(updated_resume.based_on_resume_id, UUID)
                else updated_resume.based_on_resume_id
            ),
            target_job=target_job,
            version=updated_resume.version,
            created_at=updated_resume.created_at or datetime.utcnow(),
            updated_at=updated_resume.updated_at or datetime.utcnow(),
            last_generated_at=updated_resume.last_generated_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating resume {resume_id} for user {current_user}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update resume",
        )


@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a resume"""
    try:
        resume_repo = get_resume_repository()

        # Check if resume exists and belongs to user
        existing_resume = await resume_repo.get_resume(resume_id, current_user)
        if not existing_resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found",
            )

        # Delete the resume
        success = await resume_repo.delete_resume(resume_id, current_user)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete resume",
            )

        return {"message": "Resume deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting resume {resume_id} for user {current_user}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete resume",
        )
