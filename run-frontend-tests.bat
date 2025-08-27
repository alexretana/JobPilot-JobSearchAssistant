@echo off
REM Frontend Test Runner Script for Windows
REM This script runs frontend tests using npm/vitest

echo ========================================
echo Running Frontend Tests
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

REM Run frontend tests
echo Running frontend tests...
npm run test:run
if errorlevel 1 (
    echo ERROR: Frontend tests failed
    cd ..
    exit /b 1
)

echo Frontend tests completed successfully!
cd ..
exit /b 0