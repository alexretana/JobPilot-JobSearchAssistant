from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, validator

from backend.api.auth import (
    create_access_token,
    get_password_hash,
    get_user_by_email,
    verify_password,
)
from backend.data.database import get_user_repository
from backend.data.models import UserProfile, UserProfileDB

router = APIRouter(prefix="/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @validator("password")
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # Add more password strength validation as needed
        return v


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    is_verified: bool


@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    """Authenticate user and return access token"""
    # Look up user by email in database
    user_repo = get_user_repository()

    # Get user from database
    with user_repo.db_manager.get_session() as session:
        db_user = (
            session.query(UserProfileDB)
            .filter(UserProfileDB.email == login_request.email)
            .first()
        )

        # Check if user exists
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if user is active
        if not db_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password against hashed password in database
        if not verify_password(login_request.password, db_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Update last login time
        db_user.last_login = datetime.utcnow()
        session.flush()

        # Get user ID while still in session
        user_id = str(db_user.id)

    # Create access token
    access_token = create_access_token(data={"sub": user_id})

    return LoginResponse(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    # Check if user with this email already exists
    existing_user = get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create user profile data
    user_profile = UserProfile(
        id=str(uuid4()),
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        # Set default values for authentication fields
        is_active=True,
        is_verified=False,
        # Other fields will use defaults from the model
    )

    # Store user in database
    user_repo = get_user_repository()
    # Use pydantic_to_sqlalchemy to convert the user_profile to UserProfileDB
    from datetime import datetime

    from backend.data.models import UserProfileDB, pydantic_to_sqlalchemy

    user_db = pydantic_to_sqlalchemy(user_profile, UserProfileDB)
    # Set the hashed_password and timestamps
    user_db.hashed_password = hashed_password
    user_db.created_at = datetime.utcnow()
    user_db.updated_at = datetime.utcnow()

    with user_repo.db_manager.get_session() as session:
        session.add(user_db)
        session.flush()

    # Return user data
    return UserResponse(
        id=user_profile.id,
        email=user_profile.email,
        first_name=user_profile.first_name,
        last_name=user_profile.last_name,
        is_active=True,
        is_verified=False,
    )


@router.post("/logout")
async def logout():
    """Logout user (typically handled client-side by deleting token)"""
    # In a stateless JWT system, logout is typically handled client-side
    # by deleting the token. In a stateful system, you might invalidate
    # the token on the server.
    return {"message": "Logged out successfully"}


@router.post("/refresh")
async def refresh_token():
    """Refresh access token"""
    # In a real implementation, you would:
    # 1. Verify refresh token
    # 2. Generate new access token
    # 3. Return new access token

    # For now, we'll just return a placeholder
    return {"message": "Token refresh endpoint - not implemented yet"}
