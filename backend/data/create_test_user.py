#!/usr/bin/env python3
"""
Script to create a test user in the database
"""
import sys
import os
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.api.auth import get_password_hash
from backend.data.database import get_database_manager
from backend.data.models import UserProfileDB

def create_test_user():
    """Create a test user in the database"""
    print("Creating test user...")
    
    # Get the database manager
    db_manager = get_database_manager()
    
    # Create a test user with hashed password
    email = "test@example.com"
    password = "testpassword123"
    hashed_password = get_password_hash(password)
    
    # Create user data
    user_data = {
        "id": "test-user-id",
        "email": email,
        "hashed_password": hashed_password,
        "is_active": True,
        "is_verified": False,
        "first_name": "Test",
        "last_name": "User",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    try:
        # Insert the user into the database
        with db_manager.get_session() as session:
            # Check if user already exists
            existing_user = session.query(UserProfileDB).filter(UserProfileDB.email == email).first()
            if existing_user:
                print(f"User {email} already exists")
                return
            
            # Create new user
            user = UserProfileDB(**user_data)
            session.add(user)
            session.flush()
            
            print(f"Created test user: {email}")
            print(f"User ID: {user.id}")
            
    except Exception as e:
        print(f"Error creating test user: {e}")
        raise

if __name__ == "__main__":
    create_test_user()