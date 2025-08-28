@echo off
REM Master Test Runner Script for Windows
REM This script orchestrates backend, frontend, and integration tests

echo ========================================
echo Running Tests
echo ========================================

REM Parse command line arguments
set RUN_BACKEND=1
set RUN_FRONTEND=1
set RUN_E2E=1
set RUN_INTEGRATION=0

if "%1"=="--backend-only" (
    set RUN_FRONTEND=0
    set RUN_E2E=0
)
if "%1"=="--frontend-only" (
    set RUN_BACKEND=0
    set RUN_E2E=0
)
if "%1"=="--e2e-only" (
    set RUN_BACKEND=0
    set RUN_FRONTEND=0
    set RUN_E2E=1
)
if "%1"=="--integration-only" (
    set RUN_BACKEND=0
    set RUN_FRONTEND=0
    set RUN_E2E=0
    set RUN_INTEGRATION=1
)

REM Run integration tests if requested
if %RUN_INTEGRATION%==1 (
    echo Running integration tests...
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
    pytest frontend_backend_integration/
    if errorlevel 1 (
        echo ERROR: Integration tests failed
        exit /b 1
    )
    echo Integration tests completed successfully!
    echo.
    goto :end
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
    pytest .. --ignore=frontend_backend_integration
    if errorlevel 1 (
        echo ERROR: Backend tests failed
        exit /b 1
    )
    echo Backend tests completed successfully!
    echo.
)

REM Run frontend unit tests if requested
if %RUN_FRONTEND%==1 (
    echo Running frontend unit tests...
    cd ..
    call run-frontend-tests.bat
    if errorlevel 1 (
        echo ERROR: Frontend unit tests failed
        exit /b 1
    )
    cd tests
    echo Frontend unit tests completed successfully!
    echo.
)

REM Run frontend e2e tests if requested
if %RUN_E2E%==1 (
    echo Running frontend e2e tests...
    cd ..
    call tests\frontend_e2e\run_e2e_tests.bat
    if errorlevel 1 (
        echo ERROR: Frontend e2e tests failed
        exit /b 1
    )
    cd tests
    echo Frontend e2e tests completed successfully!
    echo.
)

:end
echo ========================================
echo All tests completed successfully!
echo ========================================
exit /b 0