@echo off
REM Master Test Runner Script for Windows
REM This script orchestrates both backend and frontend tests

echo ========================================
echo Running All Tests
echo ========================================

REM Parse command line arguments
set RUN_BACKEND=1
set RUN_FRONTEND=1

if "%1"=="--backend-only" (
    set RUN_FRONTEND=0
)
if "%1"=="--frontend-only" (
    set RUN_BACKEND=0
)

REM Run backend tests if requested
if %RUN_BACKEND%==1 (
    echo Running backend tests...
    echo Checking if Python dependencies are installed...
    uv pip install -r ../backend/requirements.txt >nul 2>&1
    if errorlevel 1 (
        echo Installing Python dependencies with uv...
        uv pip install -r ../backend/requirements.txt
        if errorlevel 1 (
            echo ERROR: Failed to install Python dependencies
            exit /b 1
        )
    )
    pytest ..
    if errorlevel 1 (
        echo ERROR: Backend tests failed
        exit /b 1
    )
    echo Backend tests completed successfully!
    echo.
)

REM Run frontend tests if requested
if %RUN_FRONTEND%==1 (
    echo Running frontend tests...
    cd ..
    call run-frontend-tests.bat
    if errorlevel 1 (
        echo ERROR: Frontend tests failed
        exit /b 1
    )
    cd tests
    echo Frontend tests completed successfully!
    echo.
)

echo ========================================
echo All tests completed successfully!
echo ========================================
exit /b 0