#!/bin/bash

# Frontend Test Runner Script for Unix/Linux/MacOS
# This script runs frontend tests using npm/vitest

echo "========================================"
echo "Running Frontend Tests"
echo "========================================"

# Check if we're in the correct directory structure
if [ ! -f "frontend/package.json" ]; then
    echo "ERROR: frontend/package.json not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Check if node_modules exists, if not install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install frontend dependencies"
        cd ..
        exit 1
    fi
fi

# Run frontend tests
echo "Running frontend tests..."
npm run test:run
if [ $? -ne 0 ]; then
    echo "ERROR: Frontend tests failed"
    cd ..
    exit 1
fi

echo "Frontend tests completed successfully!"
cd ..
exit 0