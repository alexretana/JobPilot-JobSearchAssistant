from datetime import datetime, timedelta
from typing import Optional, Union
import base64
import json
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Secret key for JWT token signing (in production, this should be stored securely)
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security scheme for Swagger UI
security = HTTPBearer()

# TODO: Implement AWS Cognito integration
# Future enhancement: Add configuration to switch between local auth and AWS Cognito
# This would involve:
# 1. Adding AWS Cognito client configuration
# 2. Implementing OAuth 2.0 flows for Cognito
# 3. Creating user mappings between Cognito and local user system
# 4. Adding config file to choose between local auth or Cognito auth


def get_password_hash(password: str) -> str:
    """Hash a password (simplified for testing)"""
    # In a real implementation, we would use bcrypt or similar
    # For now, we'll just base64 encode it as a placeholder
    return base64.b64encode(password.encode()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    # In a real implementation, we would use bcrypt or similar
    # For now, we'll just compare with base64 encoded version
    try:
        return base64.b64encode(plain_password.encode()).decode() == hashed_password
    except:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT-like access token (simplified for testing)"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire.timestamp()})

    # Simple base64 encoding for testing purposes
    # In a real implementation, we would use proper JWT encoding
    token_data = json.dumps(to_encode)
    encoded_token = base64.b64encode(token_data.encode()).decode()
    return encoded_token


def validate_token(token: str) -> str:
    """Validate a token and return the user ID"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Decode the base64 token
        decoded_data = base64.b64decode(token.encode()).decode()
        payload = json.loads(decoded_data)

        # Check if token has expired
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Get current user from token (for use as FastAPI dependency)"""
    token = credentials.credentials
    return validate_token(token)
