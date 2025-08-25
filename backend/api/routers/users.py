from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def list_users():
    """List all users"""
    return {"message": "List all users"}


@router.get("/{user_id}")
async def get_user(user_id: str):
    """Get a specific user by ID"""
    return {"user_id": user_id, "name": "John Doe"}


@router.post("/")
async def create_user():
    """Create a new user"""
    return {"message": "User created"}


@router.put("/{user_id}")
async def update_user(user_id: str):
    """Update a user"""
    return {"message": f"User {user_id} updated"}


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Delete a user"""
    return {"message": f"User {user_id} deleted"}
