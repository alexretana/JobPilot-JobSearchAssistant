from fastapi import APIRouter

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/")
async def list_companies():
    """List all companies"""
    return {"message": "List all companies"}


@router.get("/{company_id}")
async def get_company(company_id: str):
    """Get a specific company by ID"""
    return {"company_id": company_id, "name": "Tech Corp"}


@router.post("/")
async def create_company():
    """Create a new company"""
    return {"message": "Company created"}


@router.put("/{company_id}")
async def update_company(company_id: str):
    """Update a company"""
    return {"message": f"Company {company_id} updated"}


@router.delete("/{company_id}")
async def delete_company(company_id: str):
    """Delete a company"""
    return {"message": f"Company {company_id} deleted"}
