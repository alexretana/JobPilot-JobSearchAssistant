import pytest
import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def test_api_settings_creation():
    """Test that API settings can be created with default values"""
    try:
        from backend.api.config import APISettings
        
        # Test that we can create settings with default values
        settings = APISettings()
        assert settings.API_TITLE == "JobPilot API"
        assert settings.API_VERSION == "0.1.0"
        assert settings.API_DESCRIPTION == "API for JobPilot Career Assistant"
        assert settings.CORS_ORIGINS == ["*"]
        assert settings.CORS_CREDENTIALS == True
        assert settings.CORS_METHODS == ["*"]
        assert settings.CORS_HEADERS == ["*"]
        assert settings.DATABASE_URL == "sqlite:///../data/jobpilot.db"
    except ImportError as e:
        pytest.fail(f"Config module not found: {e}")

def test_api_settings_singleton():
    """Test that settings is a singleton instance"""
    try:
        from backend.api.config import settings as settings1
        from backend.api.config import APISettings
        
        # Import again to check if it's the same instance
        from backend.api.config import settings as settings2
        
        # They should be the same instance
        assert settings1 is settings2
        
        # But different from a new instance
        new_settings = APISettings()
        assert settings1 is not new_settings
    except ImportError as e:
        pytest.fail(f"Config module not found: {e}")

def test_api_settings_override_via_env():
    """Test that API settings can be overridden via environment variables"""
    try:
        import os
        from backend.api.config import APISettings
        
        # Set an environment variable
        os.environ["API_TITLE"] = "Test API"
        
        # Create settings and check that the environment variable is used
        settings = APISettings()
        assert settings.API_TITLE == "Test API"
        
        # Clean up
        del os.environ["API_TITLE"]
    except ImportError as e:
        pytest.fail(f"Config module not found: {e}")