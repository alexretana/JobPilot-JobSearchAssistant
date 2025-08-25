from typing import List

from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    """
    API configuration settings
    """

    # API settings
    API_TITLE: str = "JobPilot API"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "API for JobPilot Career Assistant"

    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    # Database settings
    DATABASE_URL: str = "sqlite:///../data/jobpilot.db"

    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a single instance of settings to be used throughout the application
settings = APISettings()
