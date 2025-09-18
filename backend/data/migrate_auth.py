#!/usr/bin/env python3
"""
Script to migrate the database and add authentication columns to user_profiles table
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, Column, String, Boolean, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import the database manager
from backend.data.database import get_database_manager

def migrate_database():
    """Add authentication columns to user_profiles table"""
    print("Migrating database to add authentication columns...")
    
    # Get the database manager
    db_manager = get_database_manager()
    engine = db_manager.engine
    
    # Connect to the database
    connection = engine.connect()
    
    try:
        # Check if the columns already exist
        result = connection.execute(text("PRAGMA table_info(user_profiles)"))
        columns = [row[1] for row in result.fetchall()]
        
        # Add columns if they don't exist
        if 'hashed_password' not in columns:
            print("Adding hashed_password column...")
            connection.execute(text("ALTER TABLE user_profiles ADD COLUMN hashed_password VARCHAR(128)"))
        
        if 'is_active' not in columns:
            print("Adding is_active column...")
            connection.execute(text("ALTER TABLE user_profiles ADD COLUMN is_active BOOLEAN DEFAULT 1"))
        
        if 'is_verified' not in columns:
            print("Adding is_verified column...")
            connection.execute(text("ALTER TABLE user_profiles ADD COLUMN is_verified BOOLEAN DEFAULT 0"))
        
        if 'last_login' not in columns:
            print("Adding last_login column...")
            connection.execute(text("ALTER TABLE user_profiles ADD COLUMN last_login DATETIME"))
        
        print("Database migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    migrate_database()