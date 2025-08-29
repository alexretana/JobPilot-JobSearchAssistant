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

REM Run frontend e2e tests directly with Playwright
echo Running frontend e2e tests...
npx playwright test
if errorlevel 1 (
    echo ERROR: Frontend e2e tests failed
    cd ..
    exit /b 1
)

echo Frontend e2e tests completed successfully!
cd ..
exit /b 0