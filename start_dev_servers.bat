@echo off
setlocal

echo Starting JobPilot development servers...

REM Start backend server in a new minimized window
echo Starting backend server...
start "Backend Server" /min cmd /c "cd backend && python -m api.main && pause"

REM Start frontend server in a new minimized window
echo Starting frontend server...
start "Frontend Server" /min cmd /c "cd frontend && npm run dev && pause"

echo.
echo Servers are starting in separate windows:
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo.
echo To stop the servers, close the windows titled "Backend Server" and "Frontend Server"
echo or use Task Manager to end the processes.
echo.

REM Wait a bit for servers to start
timeout 15 >nul

echo Checking if servers are responding...

REM Check if backend is running
powershell -Command "& {try {Invoke-WebRequest -Uri 'http://localhost:8000/health' -Method GET | Out-Null; Write-Host '✓ Backend server is running'} catch {Write-Host '✗ Backend server is not responding'}}" 2>nul

REM Check if frontend is running
powershell -Command "& {try {Invoke-WebRequest -Uri 'http://localhost:3000' -Method GET | Out-Null; Write-Host '✓ Frontend server is running'} catch {Write-Host '✗ Frontend server is not responding'}}" 2>nul

echo.
echo Setup complete! Servers should be running now.
echo.