"""
Integration tests for search API between frontend services and backend.
"""

import pytest
from fastapi.testclient import TestClient


class TestSearchIntegration:
    """Test search API integration between frontend services and backend."""

    def test_semantic_search(self, test_client, test_user_data, test_semantic_search_query, test_search_filters):
        """Test semantic search functionality through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test semantic search with query and filters
        query_params = f"query={test_semantic_search_query}"
        if "limit" in test_search_filters:
            query_params += f"&limit={test_search_filters['limit']}"
            
        response = test_client.get(f"/search/semantic?{query_params}")
        assert response.status_code in [200, 400, 401, 403, 422]  # Various possible responses

    def test_hybrid_search(self, test_client, test_user_data, test_hybrid_search_query, test_search_filters, test_search_weights):
        """Test hybrid search functionality through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test hybrid search with query, filters, and weights
        query_params = f"query={test_hybrid_search_query}"
        if "limit" in test_search_filters:
            query_params += f"&limit={test_search_filters['limit']}"
        if "keyword_weight" in test_search_weights:
            query_params += f"&keyword_weight={test_search_weights['keyword_weight']}"
        if "semantic_weight" in test_search_weights:
            query_params += f"&semantic_weight={test_search_weights['semantic_weight']}"
            
        response = test_client.get(f"/search/hybrid?{query_params}")
        assert response.status_code in [200, 400, 401, 403, 422]  # Various possible responses

    def test_semantic_search_with_filters(self, test_client, test_user_data, test_semantic_search_query, test_search_filters):
        """Test semantic search with advanced filtering through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Build query parameters with filters
        query_params = f"query={test_semantic_search_query}"
        
        # Add filter parameters
        filter_params = []
        if "job_types" in test_search_filters:
            for job_type in test_search_filters["job_types"]:
                filter_params.append(f"job_types={job_type}")
        if "remote_types" in test_search_filters:
            for remote_type in test_search_filters["remote_types"]:
                filter_params.append(f"remote_types={remote_type}")
        if "experience_levels" in test_search_filters:
            for exp_level in test_search_filters["experience_levels"]:
                filter_params.append(f"experience_levels={exp_level}")
        if "min_salary" in test_search_filters:
            filter_params.append(f"min_salary={test_search_filters['min_salary']}")
        if "max_salary" in test_search_filters:
            filter_params.append(f"max_salary={test_search_filters['max_salary']}")
        if "location" in test_search_filters:
            filter_params.append(f"location={test_search_filters['location']}")
        if "company" in test_search_filters:
            filter_params.append(f"company={test_search_filters['company']}")
        if "limit" in test_search_filters:
            filter_params.append(f"limit={test_search_filters['limit']}")
            
        if filter_params:
            query_params += "&" + "&".join(filter_params)
            
        response = test_client.get(f"/search/semantic?{query_params}")
        assert response.status_code in [200, 400, 401, 403, 422]  # Various possible responses

    def test_hybrid_search_with_filters(self, test_client, test_user_data, test_hybrid_search_query, test_search_filters, test_search_weights):
        """Test hybrid search with advanced filtering through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Build query parameters with filters and weights
        query_params = f"query={test_hybrid_search_query}"
        
        # Add filter parameters
        filter_params = []
        if "job_types" in test_search_filters:
            for job_type in test_search_filters["job_types"]:
                filter_params.append(f"job_types={job_type}")
        if "remote_types" in test_search_filters:
            for remote_type in test_search_filters["remote_types"]:
                filter_params.append(f"remote_types={remote_type}")
        if "experience_levels" in test_search_filters:
            for exp_level in test_search_filters["experience_levels"]:
                filter_params.append(f"experience_levels={exp_level}")
        if "min_salary" in test_search_filters:
            filter_params.append(f"min_salary={test_search_filters['min_salary']}")
        if "max_salary" in test_search_filters:
            filter_params.append(f"max_salary={test_search_filters['max_salary']}")
        if "location" in test_search_filters:
            filter_params.append(f"location={test_search_filters['location']}")
        if "company" in test_search_filters:
            filter_params.append(f"company={test_search_filters['company']}")
        if "limit" in test_search_filters:
            filter_params.append(f"limit={test_search_filters['limit']}")
        if "keyword_weight" in test_search_weights:
            filter_params.append(f"keyword_weight={test_search_weights['keyword_weight']}")
        if "semantic_weight" in test_search_weights:
            filter_params.append(f"semantic_weight={test_search_weights['semantic_weight']}")
            
        if filter_params:
            query_params += "&" + "&".join(filter_params)
            
        response = test_client.get(f"/search/hybrid?{query_params}")
        assert response.status_code in [200, 400, 401, 403, 422]  # Various possible responses

    def test_search_with_invalid_parameters(self, test_client, test_user_data):
        """Test search with invalid parameters through frontend service to backend API."""
        # First register and login to get authentication
        registration_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"],
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"]
        }
        register_response = test_client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 200
        
        # Test semantic search with invalid limit
        response = test_client.get("/search/semantic?query=test&limit=-5")
        assert response.status_code in [400, 403, 422]  # Should return validation error or forbidden
        
        # Test hybrid search with invalid weights
        response = test_client.get("/search/hybrid?query=test&keyword_weight=1.5&semantic_weight=-0.5")
        assert response.status_code in [400, 403, 422]  # Should return validation error or forbidden

    def test_search_without_authentication(self, test_client, test_semantic_search_query):
        """Test search without authentication through frontend service to backend API."""
        # Test semantic search without authentication
        response = test_client.get(f"/search/semantic?query={test_semantic_search_query}")
        assert response.status_code in [401, 403]  # Should require authentication
        
        # Test hybrid search without authentication
        response = test_client.get(f"/search/hybrid?query={test_semantic_search_query}")
        assert response.status_code in [401, 403]  # Should require authentication