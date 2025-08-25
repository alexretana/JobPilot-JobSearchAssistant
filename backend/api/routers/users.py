from fastapi import APIRouter, Depends
from backend.api.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def list_users(current_user = Depends(get_current_user)):
    """List all users"""
    return {"message": "List all users", "user_id": current_user}


@router.get("/{user_id}")
async def get_user(user_id: str, current_user = Depends(get_current_user)):
    """Get a specific user by ID"""
    return {"user_id": user_id, "name": "John Doe", "requester_id": current_user}


@router.post("/")
async def create_user(current_user = Depends(get_current_user)):
    """Create a new user"""
    return {"message": "User created", "user_id": current_user}


@router.put("/{user_id}")
async def update_user(user_id: str, current_user = Depends(get_current_user)):
    """Update a user"""
    return {"message": f"User {user_id} updated", "user_id": current_user}


@router.delete("/{user_id}")
async def delete_user(user_id: str, current_user = Depends(get_current_user)):
    """Delete a user"""
    return {"message": f"User {user_id} deleted", "user_id": current_user}
