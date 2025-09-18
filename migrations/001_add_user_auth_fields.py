"""
Migration script to add authentication fields to UserProfileDB table.
"""

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker

def upgrade(engine):
    """Add authentication fields to UserProfileDB table."""
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Add columns to user_profiles table
        with engine.connect() as conn:
            # Add hashed_password column
            conn.execute(
                "ALTER TABLE user_profiles ADD COLUMN hashed_password VARCHAR(128)"
            )
            
            # Add is_active column with default value True
            conn.execute(
                "ALTER TABLE user_profiles ADD COLUMN is_active BOOLEAN DEFAULT 1"
            )
            
            # Add is_verified column with default value False
            conn.execute(
                "ALTER TABLE user_profiles ADD COLUMN is_verified BOOLEAN DEFAULT 0"
            )
            
            # Add last_login column
            conn.execute(
                "ALTER TABLE user_profiles ADD COLUMN last_login DATETIME"
            )
            
        session.commit()
        print("Successfully added authentication fields to UserProfileDB table")
        
    except Exception as e:
        session.rollback()
        print(f"Error during migration: {e}")
        raise
        
    finally:
        session.close()

def downgrade(engine):
    """Remove authentication fields from UserProfileDB table."""
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # SQLite doesn't support dropping columns directly, so we need to:
        # 1. Create a new table without the columns
        # 2. Copy data from the old table
        # 3. Drop the old table
        # 4. Rename the new table
        
        with engine.connect() as conn:
            # Create new table without auth columns
            conn.execute("""
                CREATE TABLE user_profiles_new (
                    id VARCHAR PRIMARY KEY,
                    first_name VARCHAR,
                    last_name VARCHAR,
                    email VARCHAR UNIQUE,
                    phone VARCHAR,
                    city VARCHAR,
                    state VARCHAR,
                    linkedin_url VARCHAR,
                    portfolio_url VARCHAR,
                    current_title VARCHAR,
                    experience_years INTEGER,
                    education VARCHAR,
                    bio TEXT,
                    preferred_locations JSON,
                    preferred_job_types JSON,
                    preferred_remote_types JSON,
                    desired_salary_min FLOAT,
                    desired_salary_max FLOAT,
                    created_at DATETIME,
                    updated_at DATETIME
                )
            """)
            
            # Copy data from old table (excluding new columns)
            conn.execute("""
                INSERT INTO user_profiles_new
                SELECT id, first_name, last_name, email, phone, city, state,
                       linkedin_url, portfolio_url, current_title, experience_years,
                       education, bio, preferred_locations, preferred_job_types,
                       preferred_remote_types, desired_salary_min, desired_salary_max,
                       created_at, updated_at
                FROM user_profiles
            """)
            
            # Drop old table
            conn.execute("DROP TABLE user_profiles")
            
            # Rename new table
            conn.execute("ALTER TABLE user_profiles_new RENAME TO user_profiles")
            
        session.commit()
        print("Successfully removed authentication fields from UserProfileDB table")
        
    except Exception as e:
        session.rollback()
        print(f"Error during downgrade: {e}")
        raise
        
    finally:
        session.close()

if __name__ == "__main__":
    from backend.data.models import create_database_engine
    
    # Run upgrade migration
    engine = create_database_engine()
    upgrade(engine)