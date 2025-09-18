#!/usr/bin/env python3
"""
Script to test the settings loading
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.api.config import settings

print("REQUIRE_AUTHENTICATION setting:", getattr(settings, 'REQUIRE_AUTHENTICATION', 'Not found'))
print("All settings:", settings.dict())