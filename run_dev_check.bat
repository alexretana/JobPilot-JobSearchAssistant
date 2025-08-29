@echo off
setlocal

echo Starting JobPilot development servers...

REM Start backend server
echo Starting backend server...
cd backend
start "Backend Server" /min cmd /c "python -m api.main"
cd ..

REM Start frontend server
echo Starting frontend server...
cd frontend
start "Frontend Server" /min cmd /c "npm run dev"
cd ..

echo.
echo Servers starting up...
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo.

REM Wait a bit for servers to start
timeout /t 10 /nobreak >nul

echo Checking if servers are running...

REM Check if backend is running
powershell -Command "& {try {Invoke-WebRequest -Uri 'http://localhost:8000/health' -Method GET | Out-Null; Write-Host '✓ Backend server is running'} catch {Write-Host '✗ Backend server is not responding'}}" 2>nul

REM Check if frontend is running
powershell -Command "& {try {Invoke-WebRequest -Uri 'http://localhost:3000' -Method GET | Out-Null; Write-Host '✓ Frontend server is running'} catch {Write-Host '✗ Frontend server is not responding'}}" 2>nul

echo.
echo Press Ctrl+C to stop servers, or close this window to keep them running.
echo.

REM Keep the script running
:loop
timeout /t 1 /nobreak >nul
goto loop