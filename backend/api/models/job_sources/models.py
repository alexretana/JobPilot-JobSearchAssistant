from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class JobSourceCreate(BaseModel):
    """Model for creating a new job source"""

    name: str = Field(..., description="Unique identifier for the job source (e.g., 'linkedin', 'indeed')")
    display_name: str = Field(..., description="Human-readable name for the job source (e.g., 'LinkedIn Jobs', 'Indeed')")
    base_url: str = Field(..., description="Base URL for the job source")
    api_available: bool = Field(False, description="Whether the job source has an API available")
    scraping_rules: Optional[Dict[str, Any]] = Field(None, description="Rules for scraping jobs from this source")
    rate_limit_config: Optional[Dict[str, Any]] = Field(None, description="Rate limiting configuration for this source")
    is_active: bool = Field(True, description="Whether this job source is active")


class JobSourceUpdate(BaseModel):
    """Model for updating an existing job source"""

    name: Optional[str] = Field(None, description="Unique identifier for the job source")
    display_name: Optional[str] = Field(None, description="Human-readable name for the job source")
    base_url: Optional[str] = Field(None, description="Base URL for the job source")
    api_available: Optional[bool] = Field(None, description="Whether the job source has an API available")
    scraping_rules: Optional[Dict[str, Any]] = Field(None, description="Rules for scraping jobs from this source")
    rate_limit_config: Optional[Dict[str, Any]] = Field(None, description="Rate limiting configuration for this source")
    is_active: Optional[bool] = Field(None, description="Whether this job source is active")
    last_scraped: Optional[datetime] = Field(None, description="Timestamp of when this source was last scraped")


class JobSourceResponse(BaseModel):
    """Model for returning job source data"""

    id: UUID = Field(..., description="Unique identifier for the job source")
    name: str = Field(..., description="Unique identifier for the job source (e.g., 'linkedin', 'indeed')")
    display_name: str = Field(..., description="Human-readable name for the job source (e.g., 'LinkedIn Jobs', 'Indeed')")
    base_url: str = Field(..., description="Base URL for the job source")
    api_available: bool = Field(False, description="Whether the job source has an API available")
    scraping_rules: Optional[Dict[str, Any]] = Field(None, description="Rules for scraping jobs from this source")
    rate_limit_config: Optional[Dict[str, Any]] = Field(None, description="Rate limiting configuration for this source")
    last_scraped: Optional[datetime] = Field(None, description="Timestamp of when this source was last scraped")
    is_active: bool = Field(True, description="Whether this job source is active")
    created_at: datetime = Field(..., description="Timestamp when the job source was created")
    updated_at: datetime = Field(..., description="Timestamp when the job source was last updated")