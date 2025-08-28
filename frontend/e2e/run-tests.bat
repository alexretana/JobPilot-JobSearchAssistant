@echo off
REM Test runner script that shows progress and prevents hanging

echo Starting Playwright tests...
echo ============================

REM Run tests with timeout and capture output
npx playwright test --reporter=list %* 2>&1 | more > test-output.log

REM Check the exit code
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ All tests passed!
    echo.
) else (
    echo.
    echo ❌ Some tests failed
    echo Check test-output.log for details
    echo.
)

exit /b %ERRORLEVEL%