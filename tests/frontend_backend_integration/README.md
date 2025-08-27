# Frontend-Backend Integration Tests

This directory contains integration tests that verify the communication between frontend services and backend APIs.

## Directory Structure

```
frontend_backend_integration/
├── auth/                 # Authentication API integration tests
├── user_profiles/        # User profile API integration tests
├── jobs/                 # Job API integration tests
├── companies/            # Company API integration tests
├── applications/         # Job application API integration tests
├── resumes/              # Resume API integration tests
├── skill_banks/          # Skill bank API integration tests
├── timeline/             # Timeline API integration tests
├── job_sources/          # Job source API integration tests
├── search/               # Search API integration tests
├── job_deduplication/    # Job deduplication API integration tests
├── analytics/            # Analytics API integration tests
├── fixtures/             # Shared test fixtures and utilities
└── conftest.py           # Shared pytest configuration
```

## Running Integration Tests

### Using pytest directly

```bash
# Run all integration tests
pytest tests/frontend_backend_integration/

# Run specific test category
pytest tests/frontend_backend_integration/auth/

# Run specific test file
pytest tests/frontend_backend_integration/auth/test_auth_integration.py

# Run with verbose output
pytest tests/frontend_backend_integration/ -v

# Run with coverage
pytest tests/frontend_backend_integration/ --cov=backend --cov-report=html
```

### Using project test scripts

```bash
# Run integration tests using the master test script
tests/run_all_tests.bat --integration-only
tests/run_all_tests.sh --integration-only
```

## Test Structure Guidelines

1. **Test Organization**: Each API category has its own subdirectory with dedicated test files
2. **Naming Convention**: Test files follow the pattern `test_[feature]_integration.py`
3. **Fixture Usage**: Shared fixtures are defined in `conftest.py` and category-specific fixtures in respective directories
4. **Test Isolation**: Each test should be independent and not rely on state from other tests
5. **Resource Cleanup**: Tests should clean up any resources they create

## Writing New Integration Tests

1. Create a new test file in the appropriate category directory
2. Import required modules and fixtures
3. Create a test class with descriptive name
4. Write test methods following the AAA pattern (Arrange, Act, Assert)
5. Use appropriate fixtures for test data and setup
6. Ensure proper cleanup of resources

## Environment and Configuration

Integration tests use:
- In-memory SQLite database for test isolation
- FastAPI TestClient for making HTTP requests
- Environment variables to enable test mode
- Shared fixtures for common test data and setup

## Debugging Integration Tests

- Use `pytest --log-cli-level=INFO` to see detailed logging
- Add breakpoints using `import pdb; pdb.set_trace()` for interactive debugging
- Check the HTML coverage report to ensure adequate test coverage