from fastapi import APIRouter

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/")
async def list_jobs():
    """List all jobs"""
    return {"message": "List all jobs"}


@router.get("/{job_id}")
async def get_job(job_id: str):
    """Get a specific job by ID"""
    return {"job_id": job_id, "title": "Software Engineer"}


@router.post("/")
async def create_job():
    """Create a new job"""
    return {"message": "Job created"}


@router.put("/{job_id}")
async def update_job(job_id: str):
    """Update a job"""
    return {"message": f"Job {job_id} updated"}


@router.delete("/{job_id}")
async def delete_job(job_id: str):
    """Delete a job"""
    return {"message": f"Job {job_id} deleted"}
