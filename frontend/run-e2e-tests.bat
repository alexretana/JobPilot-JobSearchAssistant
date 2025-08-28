@echo off
REM Script to run Playwright tests with a timeout

REM Run the tests with a 5-minute timeout (300 seconds)
timeout /t 300 /nobreak >nul
npx playwright test %*

REM Check the exit code
if %ERRORLEVEL% EQU 124 (
    echo Test execution timed out after 5 minutes
    exit /b 1
) else (
    echo Tests completed
)