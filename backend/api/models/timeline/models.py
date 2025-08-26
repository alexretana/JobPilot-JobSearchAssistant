from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from backend.data.models import TimelineEventType


class TimelineEventCreate(BaseModel):
    """Model for creating a new timeline event"""

    user_profile_id: str = Field(
        ..., description="ID of the user who owns this timeline event"
    )
    event_type: TimelineEventType = Field(..., description="Type of timeline event")
    title: str = Field(..., description="Title of the timeline event")
    description: Optional[str] = Field(
        None, description="Description of the timeline event"
    )
    job_id: Optional[str] = Field(
        None, description="ID of the job related to this event"
    )
    application_id: Optional[str] = Field(
        None, description="ID of the application related to this event"
    )
    event_data: Optional[Dict[str, Any]] = Field(
        None, description="Additional event-specific data"
    )
    event_date: Optional[datetime] = Field(
        None, description="Date and time of the event"
    )
    is_milestone: bool = Field(False, description="Whether this is a milestone event")


class TimelineEventUpdate(BaseModel):
    """Model for updating an existing timeline event"""

    title: Optional[str] = Field(None, description="Title of the timeline event")
    description: Optional[str] = Field(
        None, description="Description of the timeline event"
    )
    event_data: Optional[Dict[str, Any]] = Field(
        None, description="Additional event-specific data"
    )
    event_date: Optional[datetime] = Field(
        None, description="Date and time of the event"
    )
    is_milestone: Optional[bool] = Field(
        None, description="Whether this is a milestone event"
    )


class TimelineEventResponse(BaseModel):
    """Model for returning timeline event data"""

    id: str = Field(..., description="Unique identifier for the timeline event")
    user_profile_id: str = Field(
        ..., description="ID of the user who owns this timeline event"
    )
    event_type: TimelineEventType = Field(..., description="Type of timeline event")
    title: str = Field(..., description="Title of the timeline event")
    description: Optional[str] = Field(
        None, description="Description of the timeline event"
    )
    job_id: Optional[str] = Field(
        None, description="ID of the job related to this event"
    )
    application_id: Optional[str] = Field(
        None, description="ID of the application related to this event"
    )
    event_data: Dict[str, Any] = Field(
        default_factory=dict, description="Additional event-specific data"
    )
    event_date: datetime = Field(..., description="Date and time of the event")
    is_milestone: bool = Field(False, description="Whether this is a milestone event")

    # Metadata
    created_at: datetime = Field(..., description="Timestamp when event was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when event was last updated"
    )


class TimelineEventListResponse(BaseModel):
    """Model for returning a list of timeline events"""

    events: List[TimelineEventResponse] = Field(
        ..., description="List of timeline events"
    )
    total: int = Field(..., description="Total number of timeline events")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
