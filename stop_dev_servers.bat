@echo off
echo Stopping JobPilot development servers...

REM Kill backend server
echo Stopping backend server...
taskkill /f /fi "windowtitle eq Backend Server*" >nul 2>&1

REM Kill frontend server
echo Stopping frontend server...
taskkill /f /fi "windowtitle eq Frontend Server*" >nul 2>&1

echo All servers stopped.