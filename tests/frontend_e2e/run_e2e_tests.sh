#!/bin/bash

# Frontend E2E Test Runner Script for Unix/Linux/MacOS
# This script runs frontend end-to-end tests using Playwright

echo "========================================"
echo "Running Frontend E2E Tests"
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

# Check if Playwright is installed
if [ ! -d "node_modules/@playwright/test" ]; then
    echo "Installing Playwright..."
    npm install @playwright/test
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install Playwright"
        cd ..
        exit 1
    fi
fi

# Install browsers if not already installed
echo "Installing Playwright browsers..."
npx playwright install --with-deps
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Playwright browsers"
    cd ..
    exit 1
fi

# Run frontend e2e tests
echo "Running frontend e2e tests..."
npm run test:e2e
if [ $? -ne 0 ]; then
    echo "ERROR: Frontend e2e tests failed"
    cd ..
    exit 1
fi

echo "Frontend e2e tests completed successfully!"
cd ..
exit 0