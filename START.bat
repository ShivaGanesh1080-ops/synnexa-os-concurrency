@echo off
title OS Sync Lab - Server
color 0A

echo.
echo  ========================================================
echo   OS Sync Lab: Critical Section ^& Mutex System
echo  ========================================================
echo.

:: Kill any existing process on port 3000
echo  [*] Checking port 3000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING 2^>nul') do (
    echo  [!] Killing existing process on port 3000 (PID: %%a)
    taskkill /PID %%a /F >nul 2>&1
)

:: Navigate to project directory
cd /d "%~dp0"

echo  [*] Starting server...
echo.

:: Open browser after 2 second delay (in background)
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:3000"

:: Start the server (keeps terminal open for logs)
node server.js

:: If server crashes, don't close immediately
echo.
echo  [!] Server stopped. Press any key to exit.
pause >nul
