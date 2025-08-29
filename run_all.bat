@echo off
setlocal

REM Check if --subprocess flag is provided
set SUBPROCESS_MODE=0
if "%1"== "--subprocess" (
    set SUBPROCESS_MODE=1
)

echo Starting JobPilot servers...

REM Start backend server
if %SUBPROCESS_MODE%==1 (
    echo Starting backend server in subprocess mode...
    start "Backend Server" /min cmd /c "cd backend && uv run python -m api.main"
) else (
    echo Starting backend server in subprocess mode...
    cd backend
    start "Backend Server" /min cmd /c "uv run python -m api.main"
    cd ..
)

REM Start frontend server as subprocess using PowerShell
echo Starting frontend server in subprocess mode...
cd frontend
powershell -Command "$proc = Start-Process npm -ArgumentList 'run','dev' -PassThru -WindowStyle Minimized; Write-Output $proc.Id" > ..\frontend_pid.txt
for /f "delims=" %%a in (..\frontend_pid.txt) do set FRONTEND_PID=%%a
del ..\frontend_pid.txt
cd ..

echo Frontend server started with PID: %FRONTEND_PID%

REM Wait for user to press Ctrl+C
echo Press Ctrl+C to stop servers...
if %SUBPROCESS_MODE%==0 (
    pause
)

REM Kill frontend server
if defined FRONTEND_PID (
    echo Killing frontend server...
    taskkill /f /pid %FRONTEND_PID% >nul 2>&1
)

REM Kill backend server if in subprocess mode
if %SUBPROCESS_MODE%==1 (
    echo Killing backend server...
    taskkill /f /fi "windowtitle eq Backend Server*" >nul 2>&1
)

echo All servers stopped.
