from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from backend.api.auth import get_current_user
from backend.api.models.job_deduplication.models import (
    BatchDeduplicationRequest,
    BatchDeduplicationResponse,
    BatchDeduplicationResult,
    JobDeduplicationRequest,
    JobDeduplicationResponse,
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/deduplicate", response_model=JobDeduplicationResponse)
async def check_job_duplicates(
    request: JobDeduplicationRequest,
    current_user=Depends(get_current_user),
):
    """Check if two jobs are duplicates (requires authentication)"""
    try:
        # In a real implementation, this would:
        # 1. Retrieve both jobs from the database
        # 2. Compare key fields (title, company, description, requirements, etc.)
        # 3. Calculate a similarity score using text similarity algorithms
        # 4. Return whether they're duplicates based on a threshold
        
        # Mock implementation for now
        # In a real implementation, we would compare the actual job data
        job1_id = request.job_id_1
        job2_id = request.job_id_2
        
        # Simple mock logic - in reality this would involve complex text comparison
        is_duplicate = job1_id != job2_id and (
            job1_id.startswith("job-") and job2_id.startswith("job-")
        )
        
        confidence_score = 0.9 if is_duplicate else 0.1
        matching_fields = ["title", "company"] if is_duplicate else []
        canonical_job_id = job1_id if is_duplicate else None
        duplicate_job_id = job2_id if is_duplicate else None
        
        return JobDeduplicationResponse(
            is_duplicate=is_duplicate,
            confidence_score=confidence_score,
            matching_fields=matching_fields,
            canonical_job_id=canonical_job_id,
            duplicate_job_id=duplicate_job_id,
            merge_strategy="keep_canonical" if is_duplicate else "no_action",
            processed_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking job duplicates: {str(e)}"
        )


@router.post("/deduplicate-batch", response_model=BatchDeduplicationResponse)
async def batch_job_deduplication(
    request: BatchDeduplicationRequest,
    current_user=Depends(get_current_user),
):
    """Find duplicates in a batch of jobs (requires authentication)"""
    try:
        # In a real implementation, this would:
        # 1. Retrieve all jobs from the database
        # 2. Compare each job with every other job
        # 3. Calculate similarity scores for each pair
        # 4. Identify duplicates based on the confidence threshold
        # 5. Return a list of duplicate pairs
        
        # Mock implementation for now
        job_ids = request.job_ids
        confidence_threshold = request.confidence_threshold
        
        # Simple mock logic - in reality this would involve complex text comparison
        mock_duplicates = []
        total_checked = 0
        
        # Compare each job with every other job (simplified)
        for i in range(len(job_ids)):
            for j in range(i + 1, len(job_ids)):
                total_checked += 1
                job1_id = job_ids[i]
                job2_id = job_ids[j]
                
                # Simple mock logic for determining duplicates
                is_duplicate = (
                    job1_id.startswith("job-") and 
                    job2_id.startswith("job-") and 
                    job1_id != job2_id and
                    # Mock condition for higher confidence
                    abs(hash(job1_id) - hash(job2_id)) % 10 < 3
                )
                
                if is_duplicate:
                    confidence_score = 0.95
                    matching_fields = ["title", "company", "description"]
                    canonical_job_id = job1_id
                    duplicate_job_id = job2_id
                    
                    mock_duplicates.append(BatchDeduplicationResult(
                        job_id_1=job1_id,
                        job_id_2=job2_id,
                        confidence_score=confidence_score,
                        matching_fields=matching_fields,
                        canonical_job_id=canonical_job_id,
                        duplicate_job_id=duplicate_job_id,
                        merge_strategy="keep_canonical"
                    ))
        
        return BatchDeduplicationResponse(
            duplicates=mock_duplicates,
            total_checked=total_checked,
            total_duplicates_found=len(mock_duplicates),
            confidence_threshold=confidence_threshold,
            processed_at=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error performing batch job deduplication: {str(e)}"
        )