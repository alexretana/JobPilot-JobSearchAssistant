"""
Migration runner script to apply database migrations.
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

def run_migrations():
    """Run all pending migrations."""
    from backend.data.models import create_database_engine
    
    # Create database engine
    engine = create_database_engine()
    
    # Get all migration files
    migrations_dir = Path(__file__).parent / "migrations"
    migration_files = sorted(migrations_dir.glob("*.py"))
    
    print(f"Found {len(migration_files)} migration files")
    
    # Run each migration
    for migration_file in migration_files:
        if migration_file.name == "run_migrations.py":
            continue
            
        print(f"Running migration: {migration_file.name}")
        
        # Import and run migration
        import importlib.util
        spec = importlib.util.spec_from_file_location("migration", migration_file)
        migration_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration_module)
        
        # Run upgrade function
        if hasattr(migration_module, "upgrade"):
            try:
                migration_module.upgrade(engine)
                print(f"Successfully applied migration: {migration_file.name}")
            except Exception as e:
                print(f"Error applying migration {migration_file.name}: {e}")
                raise
        else:
            print(f"No upgrade function found in {migration_file.name}")

if __name__ == "__main__":
    run_migrations()