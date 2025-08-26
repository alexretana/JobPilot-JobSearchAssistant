from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional, Dict, Any
from datetime import datetime
from backend.api.auth import get_current_user
from backend.data.models import JobType, RemoteType, ExperienceLevel

router = APIRouter(prefix="/jobs", tags=["jobs"])


# IMPORTANT: Search and statistics endpoints must come BEFORE the generic endpoints
# to avoid being caught by the /{job_id} route


@router.get("/search")
async def search_jobs(
    query: Optional[str] = Query(None, description="Text search query"),
    job_type: Optional[JobType] = Query(None, description="Filter by job type"),
    remote_type: Optional[RemoteType] = Query(None, description="Filter by remote type"),
    experience_level: Optional[ExperienceLevel] = Query(None, description="Filter by experience level"),
    salary_min: Optional[int] = Query(None, description="Minimum salary filter"),
    salary_max: Optional[int] = Query(None, description="Maximum salary filter"),
    location: Optional[str] = Query(None, description="Location filter"),
    company: Optional[str] = Query(None, description="Company filter"),
    posted_after: Optional[datetime] = Query(None, description="Posted after date"),
    posted_before: Optional[datetime] = Query(None, description="Posted before date"),
    current_user=Depends(get_current_user)
):
    """Search jobs with advanced filtering (requires authentication)"""
    # In a real implementation, this would:
    # 1. Search jobs in the database with the provided filters
    # 2. Apply text search across title, company, description
    # 3. Apply all the provided filters
    # 4. Return paginated results
    
    # For now, we'll return a mock response showing what filters were applied
    filters_applied = {}
    if query:
        filters_applied["query"] = query
    if job_type:
        filters_applied["job_type"] = job_type.value
    if remote_type:
        filters_applied["remote_type"] = remote_type.value
    if experience_level:
        filters_applied["experience_level"] = experience_level.value
    if salary_min:
        filters_applied["salary_min"] = salary_min
    if salary_max:
        filters_applied["salary_max"] = salary_max
    if location:
        filters_applied["location"] = location
    if company:
        filters_applied["company"] = company
    if posted_after:
        filters_applied["posted_after"] = posted_after.isoformat()
    if posted_before:
        filters_applied["posted_before"] = posted_before.isoformat()
    
    return {
        "message": "Job search results",
        "user_id": current_user,
        "filters_applied": filters_applied,
        "results": [
            {
                "job_id": "job-123",
                "title": "Software Engineer",
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "job_type": "Full-time",
                "remote_type": "Hybrid",
                "experience_level": "Mid-level",
                "salary_min": 100000,
                "salary_max": 150000,
                "posted_date": "2023-01-15T10:30:00Z"
            }
        ],
        "total_results": 1,
        "page": 1,
        "page_size": 20
    }


@router.get("/statistics")
async def get_job_statistics(
    current_user=Depends(get_current_user)
):
    """Get job listing statistics (requires authentication)"""
    # In a real implementation, this would:
    # 1. Query the database for job statistics
    # 2. Aggregate data by various dimensions
    # 3. Return comprehensive statistics
    
    # For now, we'll return mock statistics
    return {
        "message": "Job statistics",
        "user_id": current_user,
        "total_jobs": 1250,
        "jobs_by_type": {
            "Full-time": 850,
            "Part-time": 120,
            "Contract": 280
        },
        "jobs_by_remote_type": {
            "Remote": 450,
            "Hybrid": 520,
            "On-site": 280
        },
        "jobs_by_experience_level": {
            "Entry-level": 300,
            "Mid-level": 600,
            "Senior-level": 350
        },
        "average_salary_by_type": {
            "Full-time": {"min": 95000, "max": 165000},
            "Part-time": {"min": 45000, "max": 85000},
            "Contract": {"min": 75000, "max": 145000}
        },
        "top_locations": [
            {"location": "San Francisco, CA", "count": 180},
            {"location": "New York, NY", "count": 150},
            {"location": "Remote", "count": 140},
            {"location": "Austin, TX", "count": 95},
            {"location": "Seattle, WA", "count": 85}
        ],
        "top_companies": [
            {"company": "Tech Corp", "count": 45},
            {"company": "Innovate Inc", "count": 38},
            {"company": "Digital Solutions", "count": 32},
            {"company": "Future Systems", "count": 28},
            {"company": "Global Enterprises", "count": 25}
        ],
        "recent_trend": {
            "last_7_days": 85,
            "last_30_days": 320,
            "last_90_days": 750
        }
    }


# Generic endpoints (must come AFTER specific endpoints)
@router.get("/")
async def list_jobs(current_user=Depends(get_current_user)):
    """List all jobs (requires authentication)"""
    return {"message": "List all jobs", "user_id": current_user}


@router.get("/{job_id}")
async def get_job(job_id: str, current_user=Depends(get_current_user)):
    """Get a specific job by ID (requires authentication)"""
    return {"job_id": job_id, "title": "Software Engineer", "user_id": current_user}


@router.post("/")
async def create_job(current_user=Depends(get_current_user)):
    """Create a new job (requires authentication)"""
    return {"message": "Job created", "user_id": current_user}


@router.put("/{job_id}")
async def update_job(job_id: str, current_user=Depends(get_current_user)):
    """Update a job (requires authentication)"""
    return {"message": f"Job {job_id} updated", "user_id": current_user}


@router.delete("/{job_id}")
async def delete_job(job_id: str, current_user=Depends(get_current_user)):
    """Delete a job (requires authentication)"""
    return {"message": f"Job {job_id} deleted", "user_id": current_user}
