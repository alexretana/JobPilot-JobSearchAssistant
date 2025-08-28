@echo off

REM Test script to verify that both frontend and backend servers start correctly

echo Testing JobPilot server startup...

REM Start both servers in subprocess mode
echo Starting servers in subprocess mode...
start /b run_all.bat --subprocess

REM Wait for 10 seconds
timeout /t 10 /nobreak >nul

REM Check if servers are running
tasklist /fi "imagename eq npm.exe" | find /i "npm.exe" >nul
set npm_running=%errorlevel%

tasklist /fi "imagename eq python.exe" | find /i "python.exe" >nul
set python_running=%errorlevel%

if %npm_running%==0 if %python_running%==0 (
    echo Servers are running correctly
    
    REM Kill the processes
    taskkill /f /im npm.exe >nul 2>&1
    taskkill /f /fi "windowtitle eq Backend Server*" >nul 2>&1
    
    echo Test completed successfully
) else (
    echo Error: Servers failed to start
    exit /b 1
)