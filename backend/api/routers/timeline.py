from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.api.auth import get_current_user
from backend.data.database import get_database_manager
from backend.api.models.timeline.models import (
    TimelineEventCreate,
    TimelineEventListResponse,
    TimelineEventResponse,
    TimelineEventUpdate,
)
from backend.data.models import TimelineEventType
from backend.logger import logger
from backend.services.timeline_service import TimelineService

router = APIRouter(prefix="/timeline", tags=["timeline"])


# Database session dependency
def get_database_session():
    """Get database session for timeline operations."""
    db_manager = get_database_manager()
    with db_manager.get_session() as session:
        yield session


@router.get("/", response_model=TimelineEventListResponse)
async def list_timeline_events(
    user_profile_id: Optional[str] = Query(None, description="Filter by user profile ID"),
    job_id: Optional[str] = Query(None, description="Filter by job ID"),
    application_id: Optional[str] = Query(None, description="Filter by application ID"),
    event_types: Optional[List[TimelineEventType]] = Query(None, description="Filter by event types"),
    limit: int = Query(50, description="Number of timeline events to return", le=100),
    offset: int = Query(0, description="Number of timeline events to skip"),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_database_session),
):
    """List timeline events with optional filtering and pagination"""
    try:
        timeline_service = TimelineService(db)
        
        # If no user_profile_id is specified, use the current user
        if user_profile_id is None:
            user_profile_id = current_user
        
        # Get timeline events with filtering
        events = timeline_service.get_user_timeline(
            user_profile_id=user_profile_id,
            limit=limit,
            offset=offset,
            job_id=job_id,
            event_types=event_types,
        )
        
        # Convert to response models
        event_responses = []
        for event in events:
            event_response = TimelineEventResponse(
                id=event.id,
                user_profile_id=event.user_profile_id,
                event_type=event.event_type,
                title=event.title,
                description=event.description,
                job_id=event.job_id,
                application_id=event.application_id,
                event_data=event.event_data,
                event_date=event.event_date,
                is_milestone=event.is_milestone,
                created_at=event.created_at,
                updated_at=event.updated_at,
            )
            event_responses.append(event_response)
        
        # Get total count (simplified for now)
        total_events = len(event_responses)
        
        return TimelineEventListResponse(
            events=event_responses,
            total=total_events,
            page=offset // limit + 1 if limit > 0 else 1,
            page_size=limit,
        )
    except Exception as e:
        logger.error(f"Error listing timeline events: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list timeline events",
        )


@router.get("/{event_id}", response_model=TimelineEventResponse)
async def get_timeline_event(
    event_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_database_session),
):
    """Get a specific timeline event by ID"""
    try:
        timeline_service = TimelineService(db)
        
        # Get all events for the user and find the specific one
        # This is a simplified approach - in a real implementation, we would query directly by ID
        events = timeline_service.get_user_timeline(user_profile_id=current_user)
        event = next((e for e in events if e.id == event_id), None)
        
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Timeline event not found",
            )
        
        return TimelineEventResponse(
            id=event.id,
            user_profile_id=event.user_profile_id,
            event_type=event.event_type,
            title=event.title,
            description=event.description,
            job_id=event.job_id,
            application_id=event.application_id,
            event_data=event.event_data,
            event_date=event.event_date,
            is_milestone=event.is_milestone,
            created_at=event.created_at,
            updated_at=event.updated_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting timeline event {event_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get timeline event",
        )


@router.post("/", response_model=TimelineEventResponse, status_code=status.HTTP_201_CREATED)
async def create_timeline_event(
    event_data: TimelineEventCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_database_session),
):
    """Create a new timeline event"""
    try:
        # Verify user is creating event for themselves (unless they have special permissions)
        if event_data.user_profile_id != current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create timeline event for another user",
            )
        
        timeline_service = TimelineService(db)
        event = timeline_service.create_event(
            user_profile_id=event_data.user_profile_id,
            event_type=event_data.event_type,
            title=event_data.title,
            description=event_data.description,
            job_id=event_data.job_id,
            application_id=event_data.application_id,
            event_data=event_data.event_data,
            event_date=event_data.event_date,
            is_milestone=event_data.is_milestone,
        )
        
        return TimelineEventResponse(
            id=event.id,
            user_profile_id=event.user_profile_id,
            event_type=event.event_type,
            title=event.title,
            description=event.description,
            job_id=event.job_id,
            application_id=event.application_id,
            event_data=event.event_data,
            event_date=event.event_date,
            is_milestone=event.is_milestone,
            created_at=event.created_at,
            updated_at=event.updated_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating timeline event: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create timeline event",
        )


@router.put("/{event_id}", response_model=TimelineEventResponse)
async def update_timeline_event(
    event_id: str,
    update_data: TimelineEventUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_database_session),
):
    """Update an existing timeline event"""
    try:
        timeline_service = TimelineService(db)
        
        # Check if event exists and belongs to user (simplified check)
        events = timeline_service.get_user_timeline(user_profile_id=current_user)
        existing_event = next((e for e in events if e.id == event_id), None)
        
        if not existing_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Timeline event not found",
            )
        
        # Update the event
        update_dict = update_data.dict(exclude_unset=True)
        updated_event = timeline_service.update_event(event_id, **update_dict)
        
        if not updated_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Timeline event not found after update",
            )
        
        return TimelineEventResponse(
            id=updated_event.id,
            user_profile_id=updated_event.user_profile_id,
            event_type=updated_event.event_type,
            title=updated_event.title,
            description=updated_event.description,
            job_id=updated_event.job_id,
            application_id=updated_event.application_id,
            event_data=updated_event.event_data,
            event_date=updated_event.event_date,
            is_milestone=updated_event.is_milestone,
            created_at=updated_event.created_at,
            updated_at=updated_event.updated_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating timeline event {event_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update timeline event",
        )


@router.delete("/{event_id}")
async def delete_timeline_event(
    event_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_database_session),
):
    """Delete a timeline event"""
    try:
        timeline_service = TimelineService(db)
        
        # Check if event exists and belongs to user (simplified check)
        events = timeline_service.get_user_timeline(user_profile_id=current_user)
        existing_event = next((e for e in events if e.id == event_id), None)
        
        if not existing_event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Timeline event not found",
            )
        
        # Delete the event
        success = timeline_service.delete_event(event_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete timeline event",
            )
        
        return {"message": "Timeline event deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting timeline event {event_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete timeline event",
        )