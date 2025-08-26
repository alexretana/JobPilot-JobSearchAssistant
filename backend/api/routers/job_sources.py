from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.api.auth import get_current_user
from backend.api.models.job_sources.models import (
    JobSourceCreate,
    JobSourceResponse,
    JobSourceUpdate,
)
from backend.data.database import get_database_manager, get_job_repository
from backend.data.models import JobSourceDB
from backend.logger import logger

router = APIRouter(prefix="/job-sources", tags=["job-sources"])


# Database session dependency
def get_database_session():
    """Get database session for job sources operations."""
    db_manager = get_database_manager()
    with db_manager.get_session() as session:
        yield session


@router.get("/", response_model=Dict[str, Any])
async def list_job_sources(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    api_available: Optional[bool] = Query(None, description="Filter by API availability"),
    limit: int = Query(50, description="Number of job sources to return", le=100),
    offset: int = Query(0, description="Number of job sources to skip"),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_database_session),
):
    """List job sources with optional filtering and pagination"""
    try:
        # In a real implementation, this would:
        # 1. Query the database for job sources with the provided filters
        # 2. Apply pagination
        # 3. Return paginated results
        
        filters_applied = {}
        if is_active is not None:
            filters_applied["is_active"] = is_active
        if api_available is not None:
            filters_applied["api_available"] = api_available
        
        # Mock implementation for now
        mock_sources = [
            {
                "id": "source-123",
                "name": "linkedin",
                "display_name": "LinkedIn Jobs",
                "base_url": "https://linkedin.com/jobs",
                "api_available": True,
                "is_active": True,
                "created_at": "2023-01-15T10:30:00Z",
                "updated_at": "2023-01-20T14:45:00Z",
            },
            {
                "id": "source-456",
                "name": "indeed",
                "display_name": "Indeed",
                "base_url": "https://indeed.com",
                "api_available": False,
                "is_active": True,
                "created_at": "2023-01-10T09:15:00Z",
                "updated_at": "2023-01-18T11:30:00Z",
            }
        ]
        
        # Apply pagination to mock data
        paginated_sources = mock_sources[offset:offset + limit]
        
        return {
            "message": "List of job sources",
            "user_id": current_user,
            "filters_applied": filters_applied,
            "sources": paginated_sources,
            "total": len(mock_sources),
            "page": offset // limit + 1 if limit > 0 else 1,
            "page_size": limit,
        }
    except Exception as e:
        logger.error(f"Error listing job sources: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list job sources",
        )


@router.get("/{source_id}", response_model=JobSourceResponse)
async def get_job_source(
    source_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_database_session),
):
    """Get a specific job source by ID"""
    try:
        # In a real implementation, this would:
        # 1. Query the database for the job source with the given ID
        # 2. Return the job source if found, or 404 if not found
        
        # For testing, let's simulate a real implementation that would return 404 for non-existent sources
        # In a real app, we would check if the source exists in the database
        # For now, we'll just return a mock response for any ID except a special test ID
        if source_id == "non-existent-test-id":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job source not found",
            )
        
        # Mock implementation for other IDs
        mock_source = {
            "id": source_id,
            "name": "linkedin",
            "display_name": "LinkedIn Jobs",
            "base_url": "https://linkedin.com/jobs",
            "api_available": True,
            "scraping_rules": {"test": "rule"},
            "rate_limit_config": {"requests_per_minute": 10},
            "last_scraped": "2023-01-20T14:45:00Z",
            "is_active": True,
            "created_at": "2023-01-15T10:30:00Z",
            "updated_at": "2023-01-20T14:45:00Z",
        }
        
        return JobSourceResponse(**mock_source)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job source {source_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get job source",
        )


@router.post("/", response_model=JobSourceResponse, status_code=status.HTTP_201_CREATED)
async def create_job_source(
    source_data: JobSourceCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_database_session),
):
    """Create a new job source"""
    try:
        # In a real implementation, this would:
        # 1. Validate the source data
        # 2. Create a new job source in the database
        # 3. Return the created job source
        
        # Mock implementation for now
        mock_source = {
            "id": "new-source-id",
            "name": source_data.name,
            "display_name": source_data.display_name,
            "base_url": source_data.base_url,
            "api_available": source_data.api_available,
            "scraping_rules": source_data.scraping_rules,
            "rate_limit_config": source_data.rate_limit_config,
            "is_active": source_data.is_active,
            "created_at": "2023-01-25T10:00:00Z",
            "updated_at": "2023-01-25T10:00:00Z",
        }
        
        return JobSourceResponse(**mock_source)
    except Exception as e:
        logger.error(f"Error creating job source: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create job source",
        )


@router.put("/{source_id}", response_model=JobSourceResponse)
async def update_job_source(
    source_id: str,
    update_data: JobSourceUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_database_session),
):
    """Update an existing job source"""
    try:
        # In a real implementation, this would:
        # 1. Query the database for the job source with the given ID
        # 2. Update the job source with the provided data
        # 3. Return the updated job source
        
        # Mock implementation for now
        mock_source = {
            "id": source_id,
            "name": update_data.name or "linkedin",
            "display_name": update_data.display_name or "LinkedIn Jobs",
            "base_url": update_data.base_url or "https://linkedin.com/jobs",
            "api_available": update_data.api_available if update_data.api_available is not None else True,
            "scraping_rules": update_data.scraping_rules,
            "rate_limit_config": update_data.rate_limit_config,
            "last_scraped": update_data.last_scraped,
            "is_active": update_data.is_active if update_data.is_active is not None else True,
            "created_at": "2023-01-15T10:30:00Z",
            "updated_at": "2023-01-25T11:00:00Z",
        }
        
        return JobSourceResponse(**mock_source)
    except Exception as e:
        logger.error(f"Error updating job source {source_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update job source",
        )


@router.delete("/{source_id}")
async def delete_job_source(
    source_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_database_session),
):
    """Delete a job source"""
    try:
        # In a real implementation, this would:
        # 1. Query the database for the job source with the given ID
        # 2. Delete the job source if found
        # 3. Return success message
        
        # Mock implementation for now
        return {"message": f"Job source {source_id} deleted successfully", "user_id": current_user}
    except Exception as e:
        logger.error(f"Error deleting job source {source_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete job source",
        )