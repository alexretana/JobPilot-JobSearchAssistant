from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.api.auth import get_current_user
from backend.api.dependencies import get_db
from backend.api.models.application_models import (
    JobApplicationCreate,
    JobApplicationListResponse,
    JobApplicationResponse,
    JobApplicationUpdate,
)
from backend.data.database import get_interaction_repository
from backend.data.models import ApplicationStatus
from backend.logger import logger

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("/", response_model=JobApplicationListResponse)
async def list_applications(
    status: Optional[ApplicationStatus] = Query(
        None, description="Filter by application status"
    ),
    limit: int = Query(50, description="Number of applications to return", le=100),
    offset: int = Query(0, description="Number of applications to skip"),
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """List all job applications for the current user (requires authentication)"""
    try:
        interaction_repo = get_interaction_repository()
        applications, total = interaction_repo.get_applications(
            user_profile_id=current_user,
            status=status,
            limit=limit,
            offset=offset,
        )

        # Convert to response models
        app_responses = []
        for app in applications:
            app_responses.append(
                JobApplicationResponse(
                    id=app.id,
                    job_id=app.job_id,
                    user_profile_id=app.user_profile_id,
                    status=app.status,
                    applied_date=app.applied_date,
                    response_date=app.response_date,
                    resume_version=app.resume_version,
                    cover_letter=app.cover_letter,
                    notes=app.notes,
                    follow_up_date=app.follow_up_date,
                    interview_scheduled=app.interview_scheduled,
                    created_at=app.created_at,
                    updated_at=app.updated_at,
                )
            )

        return JobApplicationListResponse(
            applications=app_responses,
            total=total,
            page=offset // limit + 1 if limit > 0 else 1,
            page_size=limit,
        )
    except Exception as e:
        logger.error(f"Error listing applications for user {current_user}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list applications",
        )


@router.get("/{application_id}", response_model=JobApplicationResponse)
async def get_application(
    application_id: str,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Get a specific job application by ID (requires authentication)"""
    try:
        interaction_repo = get_interaction_repository()
        application = interaction_repo.get_application(application_id)

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        # Check if the application belongs to the current user
        if str(application.user_profile_id) != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this application",
            )

        return JobApplicationResponse(
            id=application.id,
            job_id=application.job_id,
            user_profile_id=application.user_profile_id,
            status=application.status,
            applied_date=application.applied_date,
            response_date=application.response_date,
            resume_version=application.resume_version,
            cover_letter=application.cover_letter,
            notes=application.notes,
            follow_up_date=application.follow_up_date,
            interview_scheduled=application.interview_scheduled,
            created_at=application.created_at,
            updated_at=application.updated_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error getting application {application_id} for user {current_user}: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get application",
        )


@router.post("/", response_model=JobApplicationResponse)
async def create_application(
    application_data: JobApplicationCreate,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Create a new job application (requires authentication)"""
    try:
        # Verify that the user is creating an application for themselves
        if str(application_data.user_profile_id) != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create application for another user",
            )

        interaction_repo = get_interaction_repository()
        interaction = interaction_repo.apply_to_job(
            user_id=str(application_data.user_profile_id),
            job_id=str(application_data.job_id),
            resume_version=application_data.resume_version,
            cover_letter=application_data.cover_letter,
            interaction_data=(
                {"notes": application_data.notes} if application_data.notes else None
            ),
        )

        # If notes were provided, we need to update the interaction to store them in the notes field
        if application_data.notes:
            # Update the interaction to store notes in the proper field
            update_dict = {"notes": application_data.notes}
            updated_interaction = interaction_repo.update_application(
                interaction.id, update_dict
            )
            if updated_interaction:
                interaction = updated_interaction

        # Convert interaction to application response
        return JobApplicationResponse(
            id=(
                UUID(str(interaction.id))
                if not isinstance(interaction.id, UUID)
                else interaction.id
            ),
            job_id=(
                UUID(str(interaction.job_id))
                if not isinstance(interaction.job_id, UUID)
                else interaction.job_id
            ),
            user_profile_id=(
                UUID(str(interaction.user_profile_id))
                if not isinstance(interaction.user_profile_id, UUID)
                else interaction.user_profile_id
            ),
            status=interaction.status,
            applied_date=interaction.applied_date,
            response_date=interaction.response_date,
            resume_version=interaction.resume_version,
            cover_letter=interaction.cover_letter,
            notes=interaction.notes,
            follow_up_date=interaction.follow_up_date,
            interview_scheduled=interaction.interview_scheduled,
            created_at=interaction.created_at,
            updated_at=interaction.updated_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating application for user {current_user}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create application",
        )


@router.put("/{application_id}", response_model=JobApplicationResponse)
async def update_application(
    application_id: str,
    update_data: JobApplicationUpdate,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Update a job application (requires authentication)"""
    try:
        interaction_repo = get_interaction_repository()
        application = interaction_repo.get_application(application_id)

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        # Check if the application belongs to the current user
        if str(application.user_profile_id) != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this application",
            )

        # Update the application
        update_dict = update_data.dict(exclude_unset=True)
        updated_application = interaction_repo.update_application(
            application_id, update_dict
        )

        if not updated_application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found after update",
            )

        # Refresh the application data to ensure we have the latest values
        # This is a workaround for potential caching issues
        refreshed_application = interaction_repo.get_application(application_id)
        if refreshed_application:
            updated_application = refreshed_application

        return JobApplicationResponse(
            id=updated_application.id,
            job_id=updated_application.job_id,
            user_profile_id=updated_application.user_profile_id,
            status=updated_application.status,
            applied_date=updated_application.applied_date,
            response_date=updated_application.response_date,
            resume_version=updated_application.resume_version,
            cover_letter=updated_application.cover_letter,
            notes=updated_application.notes,
            follow_up_date=updated_application.follow_up_date,
            interview_scheduled=updated_application.interview_scheduled,
            created_at=updated_application.created_at,
            updated_at=updated_application.updated_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error updating application {application_id} for user {current_user}: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update application",
        )


@router.delete("/{application_id}")
async def delete_application(
    application_id: str,
    current_user=Depends(get_current_user),
    db=Depends(get_db),
):
    """Delete a job application (requires authentication)"""
    try:
        interaction_repo = get_interaction_repository()
        application = interaction_repo.get_application(application_id)

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        # Check if the application belongs to the current user
        if str(application.user_profile_id) != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this application",
            )

        success = interaction_repo.delete_application(application_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete application",
            )

        return {"message": "Application deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error deleting application {application_id} for user {current_user}: {e}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete application",
        )
