@echo off
title Global Civic AI - Start Dev Environment

:: ==== START SERVERS ====
echo Starting Backend...
start "Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload"

timeout /t 5

echo Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo Done! Wait a few seconds, then open browser:
echo http://127.0.0.1:3000

:: ==== STOP OPTION ====
echo.
echo Press S to stop all dev servers, or any other key to exit this window.
choice /c SY /n /m "S=Stop, Y=Exit"
if errorlevel 2 exit
if errorlevel 1 goto STOP_SERVERS

:STOP_SERVERS
echo Stopping backend and frontend...
taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T
echo All dev servers terminated.
pause
exit