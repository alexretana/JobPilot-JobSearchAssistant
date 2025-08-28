@echo off
REM Frontend E2E Test Runner Script for Windows
REM This script runs frontend end-to-end tests using Playwright

echo ========================================
echo Running Frontend E2E Tests
echo ========================================

REM Check if we're in the correct directory structure
if not exist "frontend\package.json" (
    echo ERROR: frontend/package.json not found!
    echo Please run this script from the project root directory.
    exit /b 1
)

REM Navigate to frontend directory
cd frontend

REM Check if node_modules exists, if not install dependencies
if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install frontend dependencies
        cd ..
        exit /b 1
    )
)

REM Check if Playwright is installed
if not exist "node_modules\@playwright\test" (
    echo Installing Playwright...
    npm install @playwright/test
    if errorlevel 1 (
        echo ERROR: Failed to install Playwright
        cd ..
        exit /b 1
    )
)

REM Install browsers if not already installed
echo Installing Playwright browsers...
npx playwright install --with-deps
if errorlevel 1 (
    echo ERROR: Failed to install Playwright browsers
    cd ..
    exit /b 1
)

REM Run frontend e2e tests
echo Running frontend e2e tests...
npm run test:e2e
if errorlevel 1 (
    echo ERROR: Frontend e2e tests failed
    cd ..
    exit /b 1
)

echo Frontend e2e tests completed successfully!
cd ..
exit /b 0