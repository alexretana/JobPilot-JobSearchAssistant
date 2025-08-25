from typing import Generator

from backend.data.database import DatabaseManager, get_database_manager


def get_db() -> Generator[DatabaseManager, None, None]:
    """Dependency for database manager"""
    db = get_database_manager()
    try:
        yield db
    finally:
        # Database sessions are handled by the manager, so no need to close here
        pass
