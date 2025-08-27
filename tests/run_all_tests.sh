#!/bin/bash

# Master Test Runner Script for Unix/Linux/MacOS
# This script orchestrates both backend and frontend tests

echo "========================================"
echo "Running All Tests"
echo "========================================"

# Parse command line arguments
RUN_BACKEND=1
RUN_FRONTEND=1

if [ "$1" == "--backend-only" ]; then
    RUN_FRONTEND=0
elif [ "$1" == "--frontend-only" ]; then
    RUN_BACKEND=0
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
    pytest ..
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