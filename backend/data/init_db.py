#!/usr/bin/env python3
"""
Script to initialize the database with proper tables
"""
import os
import sys

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.data.database import get_database_manager


def initialize_database():
    """Initialize the database with all required tables"""
    print("Initializing database...")

    # Get the database manager which will create tables automatically
    db_manager = get_database_manager()

    # Force table creation
    db_manager.create_tables()

    print("Database initialized successfully!")

    # Show table stats
    stats = db_manager.get_table_stats()
    print("Table statistics:")
    for table, count in stats.items():
        print(f"  {table}: {count} rows")


if __name__ == "__main__":
    initialize_database()
