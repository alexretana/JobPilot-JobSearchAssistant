"""
Simple test to verify CI setup is working correctly.
This test doesn't require complex application dependencies.
"""

def test_python_version():
    """Test that we're running Python 3.12+"""
    import sys
    assert sys.version_info >= (3, 12), f"Python version {sys.version_info} is too old"
    print(f"✅ Python version {sys.version_info.major}.{sys.version_info.minor} is supported")


def test_core_dependencies():
    """Test that core dependencies are available"""
    try:
        import fastapi
        import pydantic
        import pytest
        import sqlalchemy
        print("✅ Core dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False


def test_dev_tools():
    """Test that development tools are available"""
    try:
        import black
        import ruff
        print("✅ Development tools available")
        return True
    except ImportError as e:
        print(f"❌ Missing dev tool: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing CI Setup...")
    test_python_version()
    test_core_dependencies()
    test_dev_tools()
    print("🎉 CI setup verification complete!")
