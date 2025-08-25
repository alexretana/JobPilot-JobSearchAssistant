from fastapi import APIRouter

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("/")
async def list_applications():
    """List all job applications"""
    return {"message": "List all applications"}


@router.get("/{application_id}")
async def get_application(application_id: str):
    """Get a specific job application by ID"""
    return {"application_id": application_id, "status": "applied"}


@router.post("/")
async def create_application():
    """Create a new job application"""
    return {"message": "Application created"}


@router.put("/{application_id}")
async def update_application(application_id: str):
    """Update a job application"""
    return {"message": f"Application {application_id} updated"}


@router.delete("/{application_id}")
async def delete_application(application_id: str):
    """Delete a job application"""
    return {"message": f"Application {application_id} deleted"}
