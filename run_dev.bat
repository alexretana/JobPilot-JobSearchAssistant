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
echo Servers started:
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo.
echo Press any key to stop servers...
pause >nul

REM Kill all started processes
echo Stopping servers...
taskkill /f /fi "windowtitle eq Backend Server*" >nul 2>&1
taskkill /f /fi "windowtitle eq Frontend Server*" >nul 2>&1

echo All servers stopped.