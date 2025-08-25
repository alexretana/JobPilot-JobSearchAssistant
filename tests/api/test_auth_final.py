import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_final_auth_system_verification():
    """Final comprehensive test of the authentication system"""
    try:
        from backend.api.main import app
        from backend.api.auth import create_access_token, get_password_hash, verify_password
        
        client = TestClient(app)
        
        print("Starting final authentication system verification...")
        
        # 1. Test password hashing functionality
        password = "test-password-123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed)
        assert not verify_password("wrong-password", hashed)
        print("[PASS] Password hashing and verification working")
        
        # 2. Test token creation and validation
        token = create_access_token(data={"sub": "final-test-user"})
        # Note: We can't easily test validate_token directly in this context
        # because our tests don't have access to the HTTPAuthorizationCredentials
        print("[PASS] Token creation working")
        
        # 3. Test auth endpoints exist and function
        # Register endpoint
        register_resp = client.post("/auth/register", json={
            "email": "finaltest@example.com",
            "password": "final-password-123",
            "full_name": "Final Test User"
        })
        assert register_resp.status_code == 200
        print("[PASS] Registration endpoint working")
        
        # Login endpoint
        login_resp = client.post("/auth/login", json={
            "email": "finaltest@example.com",
            "password": "final-password-123"
        })
        assert login_resp.status_code == 200
        assert "access_token" in login_resp.json()
        token = login_resp.json()["access_token"]
        print("[PASS] Login endpoint working")
        
        # Logout endpoint
        logout_resp = client.post("/auth/logout")
        assert logout_resp.status_code == 200
        print("[PASS] Logout endpoint working")
        
        # Refresh endpoint
        refresh_resp = client.post("/auth/refresh")
        assert refresh_resp.status_code == 200
        print("[PASS] Token refresh endpoint working")
        
        # 4. Test protected endpoints
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Jobs endpoint (should be protected)
        jobs_resp = client.get("/jobs/", headers=auth_headers)
        assert jobs_resp.status_code == 200
        print("[PASS] Protected endpoints working with valid token")
        
        # Jobs endpoint without auth (should fail)
        jobs_no_auth_resp = client.get("/jobs/")
        assert jobs_no_auth_resp.status_code == 403
        print("[PASS] Protected endpoints properly reject requests without authentication")
        
        # 5. Test middleware behavior
        # Invalid token should be rejected
        invalid_token_resp = client.get("/jobs/", headers={"Authorization": "Bearer invalid-token"})
        assert invalid_token_resp.status_code == 401
        print("[PASS] Middleware properly rejects invalid tokens")
        
        print("All authentication system tests passed!")
        print("Authentication system is fully functional!")
        
    except Exception as e:
        pytest.fail(f"Failed final authentication system verification: {e}")

if __name__ == "__main__":
    test_final_auth_system_verification()
    print("Final authentication system verification completed successfully!")