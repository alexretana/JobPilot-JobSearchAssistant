from fastapi import APIRouter, Depends

from backend.api.auth import get_current_user

router = APIRouter(prefix="/jobs", tags=["jobs"])


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
