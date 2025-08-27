"""
Test data fixtures for company integration tests.
"""

import pytest


@pytest.fixture
def test_company_data():
    """Provide test company data for integration tests."""
    return {
        "name": "TechCorp Inc",
        "industry": "Technology",
        "size": "201-500 employees",
        "location": "San Francisco, CA",
        "headquarters_location": "San Francisco, CA",
        "founded_year": 2010,
        "website": "https://techcorp.com",
        "description": "A leading technology company specializing in innovative solutions",
        "logo_url": "https://techcorp.com/logo.png",
        "culture": "Innovation, Excellence, Teamwork",
        "values": ["Innovation", "Excellence", "Teamwork"],
        "benefits": ["Health Insurance", "401k", "Stock Options", "Flexible PTO"],
        "domain": "techcorp.com"
    }


@pytest.fixture
def test_company_search_filters():
    """Provide test company search filters for integration tests."""
    return {
        "query": "tech",
        "location": "San Francisco, CA",
        "industry": "Technology"
    }


@pytest.fixture
def test_company_update_data():
    """Provide test company update data for integration tests."""
    return {
        "name": "TechCorp International",
        "description": "A global technology company specializing in innovative solutions",
        "website": "https://techcorp.com/international"
    }


@pytest.fixture
def test_company_job_filters():
    """Provide test company job filters for integration tests."""
    return {
        "job_type": "Full-time",
        "remote_type": "Hybrid",
        "experience_level": "Mid-level"
    }