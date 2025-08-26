from typing import List, Optional

from pydantic import BaseModel, Field


class JobDeduplicationRequest(BaseModel):
    """Request model for checking if two jobs are duplicates"""

    job_id_1: str = Field(..., description="First job ID to compare")
    job_id_2: str = Field(..., description="Second job ID to compare")


class JobDeduplicationResponse(BaseModel):
    """Response model for job deduplication result"""

    is_duplicate: bool = Field(..., description="Whether the two jobs are duplicates")
    confidence_score: float = Field(
        ..., description="Confidence score (0.0 to 1.0)", ge=0.0, le=1.0
    )
    matching_fields: List[str] = Field(
        ..., description="Which fields matched (title, company, etc.)"
    )
    canonical_job_id: Optional[str] = Field(
        None, description="Canonical job ID if duplicates found"
    )
    duplicate_job_id: Optional[str] = Field(
        None, description="Duplicate job ID if duplicates found"
    )
    merge_strategy: str = Field(
        "keep_canonical", description="Suggested merge strategy"
    )
    processed_at: str = Field(
        ..., description="Timestamp when the deduplication was processed"
    )


class BatchDeduplicationRequest(BaseModel):
    """Request model for finding duplicates in a batch of jobs"""

    job_ids: List[str] = Field(
        ..., description="List of job IDs to check for duplicates", min_items=2
    )
    confidence_threshold: float = Field(
        0.8,
        description="Minimum confidence score to consider duplicates",
        ge=0.0,
        le=1.0,
    )


class BatchDeduplicationResult(BaseModel):
    """Model for a single duplicate pair in batch deduplication"""

    job_id_1: str = Field(..., description="First job ID")
    job_id_2: str = Field(..., description="Second job ID")
    confidence_score: float = Field(
        ..., description="Confidence score (0.0 to 1.0)", ge=0.0, le=1.0
    )
    matching_fields: List[str] = Field(
        ..., description="Which fields matched (title, company, etc.)"
    )
    canonical_job_id: str = Field(..., description="Canonical job ID")
    duplicate_job_id: str = Field(..., description="Duplicate job ID")
    merge_strategy: str = Field(
        "keep_canonical", description="Suggested merge strategy"
    )


class BatchDeduplicationResponse(BaseModel):
    """Response model for batch deduplication results"""

    duplicates: List[BatchDeduplicationResult] = Field(
        ..., description="List of duplicate pairs found"
    )
    total_checked: int = Field(..., description="Total number of job pairs checked")
    total_duplicates_found: int = Field(
        ..., description="Total number of duplicates found"
    )
    confidence_threshold: float = Field(..., description="Confidence threshold used")
    processed_at: str = Field(
        ..., description="Timestamp when the deduplication was processed"
    )
