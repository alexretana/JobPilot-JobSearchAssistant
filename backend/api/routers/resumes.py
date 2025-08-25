from fastapi import APIRouter

router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.get("/")
async def list_resumes():
    """List all resumes"""
    return {"message": "List all resumes"}

@router.get("/{resume_id}")
async def get_resume(resume_id: str):
    """Get a specific resume by ID"""
    return {"resume_id": resume_id, "title": "John's Resume"}

@router.post("/")
async def create_resume():
    """Create a new resume"""
    return {"message": "Resume created"}

@router.put("/{resume_id}")
async def update_resume(resume_id: str):
    """Update a resume"""
    return {"message": f"Resume {resume_id} updated"}

@router.delete("/{resume_id}")
async def delete_resume(resume_id: str):
    """Delete a resume"""
    return {"message": f"Resume {resume_id} deleted"}