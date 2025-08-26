from typing import List, Optional

from pydantic import BaseModel, Field


class SemanticSearchRequest(BaseModel):
    """Request model for semantic search"""

    query: str = Field(..., description="Search query string")
    limit: int = Field(
        20, description="Maximum number of results to return", ge=1, le=100
    )
    job_types: Optional[List[str]] = Field(None, description="Filter by job types")
    remote_types: Optional[List[str]] = Field(
        None, description="Filter by remote types"
    )
    experience_levels: Optional[List[str]] = Field(
        None, description="Filter by experience levels"
    )
    min_salary: Optional[int] = Field(None, description="Minimum salary filter")
    max_salary: Optional[int] = Field(None, description="Maximum salary filter")
    location: Optional[str] = Field(None, description="Location filter")
    company: Optional[str] = Field(None, description="Company filter")


class SemanticSearchResult(BaseModel):
    """Model for a single semantic search result"""

    job_id: str = Field(..., description="Unique identifier for the job")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: Optional[str] = Field(None, description="Job location")
    job_type: Optional[str] = Field(None, description="Job type")
    remote_type: Optional[str] = Field(None, description="Remote type")
    experience_level: Optional[str] = Field(None, description="Experience level")
    salary_min: Optional[int] = Field(None, description="Minimum salary")
    salary_max: Optional[int] = Field(None, description="Maximum salary")
    description: Optional[str] = Field(None, description="Job description")
    score: float = Field(..., description="Semantic similarity score")


class SemanticSearchResponse(BaseModel):
    """Response model for semantic search"""

    query: str = Field(..., description="Original search query")
    results: List[SemanticSearchResult] = Field(
        ..., description="List of search results"
    )
    total: int = Field(..., description="Total number of results")
    limit: int = Field(..., description="Limit used for this search")
    processed_at: str = Field(
        ..., description="Timestamp when the search was processed"
    )


class HybridSearchRequest(BaseModel):
    """Request model for hybrid search (semantic + keyword)"""

    query: str = Field(..., description="Search query string")
    limit: int = Field(
        20, description="Maximum number of results to return", ge=1, le=100
    )
    job_types: Optional[List[str]] = Field(None, description="Filter by job types")
    remote_types: Optional[List[str]] = Field(
        None, description="Filter by remote types"
    )
    experience_levels: Optional[List[str]] = Field(
        None, description="Filter by experience levels"
    )
    min_salary: Optional[int] = Field(None, description="Minimum salary filter")
    max_salary: Optional[int] = Field(None, description="Maximum salary filter")
    location: Optional[str] = Field(None, description="Location filter")
    company: Optional[str] = Field(None, description="Company filter")
    keyword_weight: float = Field(
        0.5, description="Weight for keyword matching (0.0 to 1.0)", ge=0.0, le=1.0
    )
    semantic_weight: float = Field(
        0.5, description="Weight for semantic matching (0.0 to 1.0)", ge=0.0, le=1.0
    )


class HybridSearchResult(BaseModel):
    """Model for a single hybrid search result"""

    job_id: str = Field(..., description="Unique identifier for the job")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: Optional[str] = Field(None, description="Job location")
    job_type: Optional[str] = Field(None, description="Job type")
    remote_type: Optional[str] = Field(None, description="Remote type")
    experience_level: Optional[str] = Field(None, description="Experience level")
    salary_min: Optional[int] = Field(None, description="Minimum salary")
    salary_max: Optional[int] = Field(None, description="Maximum salary")
    description: Optional[str] = Field(None, description="Job description")
    keyword_score: float = Field(..., description="Keyword matching score")
    semantic_score: float = Field(..., description="Semantic similarity score")
    combined_score: float = Field(..., description="Combined score")


class HybridSearchResponse(BaseModel):
    """Response model for hybrid search"""

    query: str = Field(..., description="Original search query")
    results: List[HybridSearchResult] = Field(..., description="List of search results")
    total: int = Field(..., description="Total number of results")
    limit: int = Field(..., description="Limit used for this search")
    keyword_weight: float = Field(..., description="Weight used for keyword matching")
    semantic_weight: float = Field(..., description="Weight used for semantic matching")
    processed_at: str = Field(
        ..., description="Timestamp when the search was processed"
    )
