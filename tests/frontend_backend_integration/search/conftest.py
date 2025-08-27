"""
Test data fixtures for search integration tests.
"""

import pytest


@pytest.fixture
def test_semantic_search_query():
    """Provide test semantic search query for integration tests."""
    return "python developer remote work"


@pytest.fixture
def test_hybrid_search_query():
    """Provide test hybrid search query for integration tests."""
    return "senior software engineer san francisco"


@pytest.fixture
def test_search_filters():
    """Provide test search filters for integration tests."""
    return {
        "job_types": ["Full-time", "Contract"],
        "remote_types": ["Remote", "Hybrid"],
        "experience_levels": ["Mid-level", "Senior-level"],
        "min_salary": 100000,
        "max_salary": 150000,
        "location": "San Francisco, CA",
        "company": "TechCorp",
        "limit": 10
    }


@pytest.fixture
def test_search_weights():
    """Provide test search weights for integration tests."""
    return {
        "keyword_weight": 0.6,
        "semantic_weight": 0.4
    }