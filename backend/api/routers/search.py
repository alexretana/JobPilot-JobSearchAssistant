from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from backend.api.auth import get_current_user
from backend.api.models.semantic_search.models import (
    HybridSearchRequest,
    HybridSearchResponse,
    HybridSearchResult,
    SemanticSearchRequest,
    SemanticSearchResponse,
    SemanticSearchResult,
)

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/semantic", response_model=SemanticSearchResponse)
async def semantic_search(
    query: str = Query(..., description="Semantic search query"),
    limit: int = Query(20, description="Maximum number of results to return", ge=1, le=100),
    job_types: Optional[List[str]] = Query(None, description="Filter by job types"),
    remote_types: Optional[List[str]] = Query(None, description="Filter by remote types"),
    experience_levels: Optional[List[str]] = Query(None, description="Filter by experience levels"),
    min_salary: Optional[int] = Query(None, description="Minimum salary filter"),
    max_salary: Optional[int] = Query(None, description="Maximum salary filter"),
    location: Optional[str] = Query(None, description="Location filter"),
    company: Optional[str] = Query(None, description="Company filter"),
    current_user=Depends(get_current_user),
):
    """Perform semantic search on job listings (requires authentication)"""
    try:
        # In a real implementation, this would:
        # 1. Convert the query to embeddings using a sentence transformer model
        # 2. Search the job embeddings in the database
        # 3. Calculate semantic similarity scores
        # 4. Apply filters if provided
        # 5. Return results sorted by semantic similarity
        
        # Mock implementation for now
        mock_results = [
            SemanticSearchResult(
                job_id="job-123",
                title="Senior Python Developer",
                company="Tech Corp",
                location="San Francisco, CA",
                job_type="Full-time",
                remote_type="Hybrid",
                experience_level="Senior-level",
                salary_min=120000,
                salary_max=160000,
                description="Looking for an experienced Python developer with Django and FastAPI experience",
                score=0.95
            ),
            SemanticSearchResult(
                job_id="job-456",
                title="Backend Engineer",
                company="Innovate Inc",
                location="Remote",
                job_type="Full-time",
                remote_type="Remote",
                experience_level="Mid-level",
                salary_min=100000,
                salary_max=140000,
                description="Build scalable backend services using Python and cloud technologies",
                score=0.87
            )
        ]
        
        # Apply limit to mock results
        limited_results = mock_results[:limit]
        
        return SemanticSearchResponse(
            query=query,
            results=limited_results,
            total=len(mock_results),
            limit=limit,
            processed_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise Exception(f"Error performing semantic search: {str(e)}")


@router.get("/hybrid", response_model=HybridSearchResponse)
async def hybrid_search(
    query: str = Query(..., description="Hybrid search query"),
    limit: int = Query(20, description="Maximum number of results to return", ge=1, le=100),
    job_types: Optional[List[str]] = Query(None, description="Filter by job types"),
    remote_types: Optional[List[str]] = Query(None, description="Filter by remote types"),
    experience_levels: Optional[List[str]] = Query(None, description="Filter by experience levels"),
    min_salary: Optional[int] = Query(None, description="Minimum salary filter"),
    max_salary: Optional[int] = Query(None, description="Maximum salary filter"),
    location: Optional[str] = Query(None, description="Location filter"),
    company: Optional[str] = Query(None, description="Company filter"),
    keyword_weight: float = Query(0.5, description="Weight for keyword matching (0.0 to 1.0)", ge=0.0, le=1.0),
    semantic_weight: float = Query(0.5, description="Weight for semantic matching (0.0 to 1.0)", ge=0.0, le=1.0),
    current_user=Depends(get_current_user),
):
    """Perform hybrid search on job listings (semantic + keyword) (requires authentication)"""
    try:
        # In a real implementation, this would:
        # 1. Perform keyword search on job listings
        # 2. Convert the query to embeddings and perform semantic search
        # 3. Combine the scores using the provided weights
        # 4. Apply filters if provided
        # 5. Return results sorted by combined score
        
        # Mock implementation for now
        mock_results = [
            HybridSearchResult(
                job_id="job-123",
                title="Senior Python Developer",
                company="Tech Corp",
                location="San Francisco, CA",
                job_type="Full-time",
                remote_type="Hybrid",
                experience_level="Senior-level",
                salary_min=120000,
                salary_max=160000,
                description="Looking for an experienced Python developer with Django and FastAPI experience",
                keyword_score=0.85,
                semantic_score=0.95,
                combined_score=0.90
            ),
            HybridSearchResult(
                job_id="job-456",
                title="Backend Engineer",
                company="Innovate Inc",
                location="Remote",
                job_type="Full-time",
                remote_type="Remote",
                experience_level="Mid-level",
                salary_min=100000,
                salary_max=140000,
                description="Build scalable backend services using Python and cloud technologies",
                keyword_score=0.75,
                semantic_score=0.87,
                combined_score=0.81
            )
        ]
        
        # Apply limit to mock results
        limited_results = mock_results[:limit]
        
        return HybridSearchResponse(
            query=query,
            results=limited_results,
            total=len(mock_results),
            limit=limit,
            keyword_weight=keyword_weight,
            semantic_weight=semantic_weight,
            processed_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise Exception(f"Error performing hybrid search: {str(e)}")