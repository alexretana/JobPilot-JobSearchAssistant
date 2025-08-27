# Test Scripts

This directory contains scripts to run tests for both the backend and frontend components of the application.

## Available Scripts

### Root Directory Scripts

- `run-frontend-tests.bat` / `run-frontend-tests.sh` - Run frontend tests only
- These scripts are located in the project root directory

### Tests Directory Scripts

- `run_all_tests.bat` / `run_all_tests.sh` - Run both backend and frontend tests
- These scripts are located in the `tests/` directory

## Usage

### Running All Tests

From the project root directory:
```bash
# Windows
tests\run_all_tests.bat

# Unix/Linux/MacOS
./tests/run_all_tests.sh
```

### Running Backend Tests Only

From the project root directory:
```bash
# Windows
tests\run_all_tests.bat --backend-only

# Unix/Linux/MacOS
./tests/run_all_tests.sh --backend-only
```

### Running Frontend Tests Only

From the project root directory:
```bash
# Windows
tests\run_all_tests.bat --frontend-only

# Unix/Linux/MacOS
./tests/run_all_tests.sh --frontend-only
```

Or directly using the frontend test script:
```bash
# Windows
run-frontend-tests.bat

# Unix/Linux/MacOS
./run-frontend-tests.sh
```

## Features

- **Cross-platform compatibility**: Scripts work on both Windows (.bat) and Unix/Linux/MacOS (.sh)
- **Automatic dependency management**: 
  - Backend tests use `uv` for fast Python package management
  - Frontend tests automatically install npm dependencies if needed
- **Flexible execution**: Run all tests, backend only, or frontend only
- **Error handling**: Proper exit codes for CI/CD integration
- **GitHub Actions ready**: Designed to work seamlessly with GitHub Actions workflows

## GitHub Actions Integration

These scripts are designed to be easily integrated into GitHub Actions workflows. The scripts provide proper exit codes and error handling for CI/CD environments.