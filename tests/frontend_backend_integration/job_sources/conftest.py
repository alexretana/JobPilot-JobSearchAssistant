"""
Test data fixtures for job source integration tests.
"""

import pytest
from datetime import datetime


@pytest.fixture
def test_job_source_data():
    """Provide test job source data for integration tests."""
    return {
        "name": "linkedin-jobs",
        "display_name": "LinkedIn Jobs",
        "base_url": "https://linkedin.com/jobs",
        "api_available": True,
        "scraping_rules": {
            "job_posting_selector": ".job-card-container",
            "title_selector": ".job-card-title",
            "company_selector": ".job-card-company",
            "location_selector": ".job-card-location"
        },
        "rate_limit_config": {
            "requests_per_minute": 10,
            "burst_limit": 5
        },
        "is_active": True
    }


@pytest.fixture
def test_job_source_update_data():
    """Provide test job source update data for integration tests."""
    return {
        "display_name": "LinkedIn Career Portal",
        "base_url": "https://linkedin.com/careers",
        "is_active": False,
        "rate_limit_config": {
            "requests_per_minute": 5,
            "burst_limit": 3
        }
    }


@pytest.fixture
def test_job_source_search_filters():
    """Provide test job source search filters for integration tests."""
    return {
        "is_active": True,
        "api_available": True,
        "limit": 10,
        "offset": 0
    }