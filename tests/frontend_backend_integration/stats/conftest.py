"""
Test data fixtures for stats integration tests.
"""

import pytest


@pytest.fixture
def test_general_stats_expected():
    """Provide expected general stats response for integration tests."""
    return {
        "total_jobs": 1250,
        "total_users": 850,
        "total_applications": 2100,
        "total_companies": 150,
        "total_resumes": 950,
        "total_skill_banks": 420,
        "total_job_sources": 25,
        "active_users_last_24h": 125,
        "new_jobs_last_24h": 45,
        "new_applications_last_24h": 78
    }


@pytest.fixture
def test_job_stats_expected():
    """Provide expected job stats response for integration tests."""
    return {
        "total_jobs": 1250,
        "jobs_by_type": {"full_time": 850, "part_time": 120, "contract": 280},
        "jobs_by_remote_type": {"remote": 450, "hybrid": 520, "on_site": 280},
        "jobs_by_experience_level": {
            "entry_level": 300,
            "mid_level": 600,
            "senior_level": 350,
        },
        "jobs_by_industry": {
            "technology": 750,
            "finance": 200,
            "healthcare": 150,
            "education": 100,
            "other": 50,
        },
        "average_salary_min": 95000.0,
        "average_salary_max": 165000.0
    }


@pytest.fixture
def test_user_stats_expected():
    """Provide expected user stats response for integration tests."""
    return {
        "total_users": 850,
        "users_by_role": {"job_seeker": 750, "recruiter": 80, "admin": 20},
        "users_by_status": {"active": 720, "pending": 80, "suspended": 50},
        "recent_registrations": 45,
        "active_users_last_7_days": 680,
        "active_users_last_30_days": 780,
        "average_profile_completion": 75.5
    }


@pytest.fixture
def test_application_stats_expected():
    """Provide expected application stats response for integration tests."""
    return {
        "total_applications": 2100,
        "applications_by_status": {
            "not_applied": 500,
            "applied": 1200,
            "interviewing": 250,
            "rejected": 100,
            "accepted": 50,
        },
        "applications_by_job_type": {
            "full_time": 1600,
            "part_time": 200,
            "contract": 300,
        },
        "recent_applications": 180,
        "applications_last_7_days": 420,
        "applications_last_30_days": 950,
        "average_time_to_apply": 24
    }


@pytest.fixture
def test_resume_stats_expected():
    """Provide expected resume stats response for integration tests."""
    return {
        "total_resumes": 950,
        "resumes_by_type": {"professional": 650, "creative": 200, "academic": 100},
        "resumes_by_status": {"draft": 150, "published": 700, "archived": 100},
        "recent_resumes": 75,
        "average_resume_length": 450
    }


@pytest.fixture
def test_skill_bank_stats_expected():
    """Provide expected skill bank stats response for integration tests."""
    return {
        "total_skill_banks": 420,
        "average_skills_per_bank": 25.5,
        "recent_skill_additions": 45
    }


@pytest.fixture
def test_job_source_stats_expected():
    """Provide expected job source stats response for integration tests."""
    return {
        "total_job_sources": 25,
        "active_job_sources": 22,
        "sources_by_type": {"api": 10, "scraping": 12, "manual": 3},
        "recently_scraped": 8
    }