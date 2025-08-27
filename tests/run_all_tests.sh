#!/bin/bash

# Master Test Runner Script for Unix/Linux/MacOS
# This script orchestrates backend, frontend, and integration tests

echo "========================================"
echo "Running Tests"
echo "========================================"

# Parse command line arguments
RUN_BACKEND=1
RUN_FRONTEND=1
RUN_INTEGRATION=0

if [ "$1" == "--backend-only" ]; then
    RUN_FRONTEND=0
elif [ "$1" == "--frontend-only" ]; then
    RUN_BACKEND=0
elif [ "$1" == "--integration-only" ]; then
    RUN_BACKEND=0
    RUN_FRONTEND=0
    RUN_INTEGRATION=1
fi

# Run integration tests if requested
if [ $RUN_INTEGRATION -eq 1 ]; then
    echo "Running integration tests..."
    echo "Checking if Python dependencies are installed..."
    if ! uv pip install -r ../backend/requirements.txt >/dev/null 2>&1; then
        echo "Installing Python dependencies with uv..."
        uv pip install -r ../backend/requirements.txt
        if [ $? -ne 0 ]; then
            echo "ERROR: Failed to install Python dependencies"
            exit 1
        fi
    fi
    pytest frontend_backend_integration/
    if [ $? -ne 0 ]; then
        echo "ERROR: Integration tests failed"
        exit 1
    fi
    echo "Integration tests completed successfully!"
    echo
    exit 0
fi

# Run backend tests if requested
if [ $RUN_BACKEND -eq 1 ]; then
    echo "Running backend tests..."
    echo "Checking if Python dependencies are installed..."
    if ! uv pip install -r ../backend/requirements.txt >/dev/null 2>&1; then
        echo "Installing Python dependencies with uv..."
        uv pip install -r ../backend/requirements.txt
        if [ $? -ne 0 ]; then
            echo "ERROR: Failed to install Python dependencies"
            exit 1
        fi
    fi
    pytest .. --ignore=frontend_backend_integration
    if [ $? -ne 0 ]; then
        echo "ERROR: Backend tests failed"
        exit 1
    fi
    echo "Backend tests completed successfully!"
    echo
fi

# Run frontend tests if requested
if [ $RUN_FRONTEND -eq 1 ]; then
    echo "Running frontend tests..."
    cd ..
    ./run-frontend-tests.sh
    if [ $? -ne 0 ]; then
        echo "ERROR: Frontend tests failed"
        exit 1
    fi
    cd tests
    echo "Frontend tests completed successfully!"
    echo
fi

echo "========================================"
echo "All tests completed successfully!"
echo "========================================"
exit 0