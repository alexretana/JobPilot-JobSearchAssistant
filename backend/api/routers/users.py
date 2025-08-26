from fastapi import APIRouter, Depends, HTTPException, Query

from backend.api.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


# IMPORTANT: Specific endpoints must come BEFORE generic endpoints
# to avoid being caught by the /{user_id} route


@router.get("/search/by-email")
async def search_user_by_email(
    email: str = Query(..., description="Email address to search for"),
    current_user=Depends(get_current_user),
):
    """Search for a user by email address (requires authentication)"""
    # In a real implementation, this would:
    # 1. Search the database for a user with the given email
    # 2. Return the user if found, or 404 if not found

    # For now, we'll return a mock response
    # In a real implementation, you would validate the email format and search the database

    # Mock implementation - in reality this would look up the user in the database
    if email:
        return {
            "message": f"User found with email {email}",
            "user_id": "user-found-by-email",
            "email": email,
            "name": "Found User",
            "requester_id": current_user,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/default")
async def get_default_user(current_user=Depends(get_current_user)):
    """Get the default user profile for single-user mode (requires authentication)"""
    # In a real implementation, this would:
    # 1. Check if there's a designated default user in single-user mode
    # 2. Or create/get a default user profile for the requesting user
    # 3. Return that user profile

    # For now, we'll return a mock default user profile
    return {
        "message": "Default user profile for single-user mode",
        "user_id": "default-user",
        "email": "default@example.com",
        "name": "Default User",
        "current_title": "Job Seeker",
        "requester_id": current_user,
    }


# Generic endpoints (must come AFTER specific endpoints)
@router.get("/")
async def list_users(current_user=Depends(get_current_user)):
    """List all users"""
    return {"message": "List all users", "user_id": current_user}


@router.get("/{user_id}")
async def get_user(user_id: str, current_user=Depends(get_current_user)):
    """Get a specific user by ID"""
    return {"user_id": user_id, "name": "John Doe", "requester_id": current_user}


@router.post("/")
async def create_user(current_user=Depends(get_current_user)):
    """Create a new user"""
    return {"message": "User created", "user_id": current_user}


@router.put("/{user_id}")
async def update_user(user_id: str, current_user=Depends(get_current_user)):
    """Update a user"""
    return {"message": f"User {user_id} updated", "user_id": current_user}


@router.delete("/{user_id}")
async def delete_user(user_id: str, current_user=Depends(get_current_user)):
    """Delete a user"""
    return {"message": f"User {user_id} deleted", "user_id": current_user}
