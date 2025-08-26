from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.api.auth import get_current_user

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/")
async def list_companies(current_user=Depends(get_current_user)):
    """List all companies (requires authentication)"""
    return {"message": "List all companies", "user_id": current_user}


@router.get("/search")
async def search_companies(
    query: Optional[str] = Query(None, description="Search query"),
    location: Optional[str] = Query(None, description="Filter by location"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    current_user=Depends(get_current_user),
):
    """Search companies with filtering (requires authentication)"""
    # In a real implementation, this would:
    # 1. Search companies in the database with the provided filters
    # 2. Return paginated results

    filters_applied = {}
    if query:
        filters_applied["query"] = query
    if location:
        filters_applied["location"] = location
    if industry:
        filters_applied["industry"] = industry

    return {
        "message": "Company search results",
        "user_id": current_user,
        "filters_applied": filters_applied,
        "results": [
            {
                "company_id": "company-123",
                "name": "Tech Corp",
                "location": "San Francisco, CA",
                "industry": "Technology",
                "description": "Leading technology company",
                "website": "https://techcorp.com",
            }
        ],
        "total_results": 1,
        "page": 1,
        "page_size": 20,
    }


@router.get("/{company_id}")
async def get_company(company_id: str, current_user=Depends(get_current_user)):
    """Get a specific company by ID (requires authentication)"""
    return {
        "company_id": company_id,
        "name": "Tech Corp",
        "location": "San Francisco, CA",
        "industry": "Technology",
        "description": "Leading technology company",
        "website": "https://techcorp.com",
        "user_id": current_user,
    }


@router.post("/")
async def create_company(current_user=Depends(get_current_user)):
    """Create a new company (requires authentication)"""
    return {"message": "Company created", "user_id": current_user}


@router.put("/{company_id}")
async def update_company(company_id: str, current_user=Depends(get_current_user)):
    """Update a company (requires authentication)"""
    return {"message": f"Company {company_id} updated", "user_id": current_user}


@router.delete("/{company_id}")
async def delete_company(company_id: str, current_user=Depends(get_current_user)):
    """Delete a company (requires authentication)"""
    return {"message": f"Company {company_id} deleted", "user_id": current_user}


@router.get("/{company_id}/jobs")
async def get_company_jobs(
    company_id: str,
    job_type: Optional[str] = Query(None, description="Filter by job type"),
    remote_type: Optional[str] = Query(None, description="Filter by remote type"),
    experience_level: Optional[str] = Query(
        None, description="Filter by experience level"
    ),
    current_user=Depends(get_current_user),
):
    """Get jobs for a specific company (requires authentication)"""
    # In a real implementation, this would:
    # 1. Query the database for jobs associated with the company
    # 2. Apply filters if provided
    # 3. Return paginated results

    filters_applied = {}
    if job_type:
        filters_applied["job_type"] = job_type
    if remote_type:
        filters_applied["remote_type"] = remote_type
    if experience_level:
        filters_applied["experience_level"] = experience_level

    return {
        "message": f"Jobs for company {company_id}",
        "company_id": company_id,
        "user_id": current_user,
        "filters_applied": filters_applied,
        "jobs": [
            {
                "job_id": "job-123",
                "title": "Software Engineer",
                "company_id": company_id,
                "location": "San Francisco, CA",
                "job_type": "Full-time",
                "remote_type": "Hybrid",
                "experience_level": "Mid-level",
                "salary_min": 100000,
                "salary_max": 150000,
                "posted_date": "2023-01-15T10:30:00Z",
            }
        ],
        "total_jobs": 1,
    }
