@echo off
echo Starting servers and running Playwright tests...

REM Start servers in subprocess mode
echo Starting servers...
start /b run_all.bat --subprocess

REM Wait for servers to start
echo Waiting for servers to start...
timeout /t 15 /nobreak >nul

REM Check if servers are running
echo Checking if servers are responding...
powershell -Command "& {try {Invoke-WebRequest -Uri 'http://localhost:8000/health' -Method GET | Out-Null; Write-Host '✓ Backend server is running'} catch {Write-Host '✗ Backend server is not responding'}}" 2>nul
powershell -Command "& {try {Invoke-WebRequest -Uri 'http://localhost:3000' -Method GET | Out-Null; Write-Host '✓ Frontend server is running'} catch {Write-Host '✗ Frontend server is not responding'}}" 2>nul

REM Run Playwright tests
echo Running Playwright tests...
cd frontend
npx playwright test
if %errorlevel% neq 0 (
    echo Playwright tests failed!
    cd ..
    goto :cleanup
)
echo Playwright tests completed successfully!
cd ..

:cleanup
REM Kill the servers
echo Stopping servers...
taskkill /f /fi "windowtitle eq Backend Server*" >nul 2>&1
taskkill /f /fi "windowtitle eq Frontend Server*" >nul 2>&1

echo All servers stopped.