from datetime import datetime
from backend.api.models.analytics.models import JobStatsResponse

# Test creating a JobStatsResponse
try:
    response = JobStatsResponse(
        total_jobs=1250,
        jobs_by_type={
            "full_time": 850,
            "part_time": 120,
            "contract": 280
        },
        jobs_by_remote_type={
            "remote": 450,
            "hybrid": 520,
            "on_site": 280
        },
        jobs_by_experience_level={
            "entry_level": 300,
            "mid_level": 600,
            "senior_level": 350
        },
        jobs_by_industry={
            "technology": 750,
            "finance": 200,
            "healthcare": 150,
            "education": 100,
            "other": 50
        },
        jobs_by_location={
            "san_francisco_ca": 180,
            "new_york_ny": 150,
            "remote": 140,
            "austin_tx": 95,
            "seattle_wa": 85
        },
        average_salary_min=95000.0,
        average_salary_max=165000.0,
        top_companies=[
            {"company": "Tech Corp", "count": 45},
            {"company": "Innovate Inc", "count": 38},
            {"company": "Digital Solutions", "count": 32},
            {"company": "Future Systems", "count": 28},
            {"company": "Global Enterprises", "count": 25}
        ],
        top_locations=[
            {"location": "San Francisco, CA", "count": 180},
            {"location": "New York, NY", "count": 150},
            {"location": "Remote", "count": 140},
            {"location": "Austin, TX", "count": 95},
            {"location": "Seattle, WA", "count": 85}
        ],
        new_jobs_last_7_days=85,
        new_jobs_last_30_days=320,
        processed_at=datetime.utcnow()
    )
    print("JobStatsResponse created successfully!")
    print(response)
except Exception as e:
    print(f"Error creating JobStatsResponse: {e}")
    import traceback
    traceback.print_exc()