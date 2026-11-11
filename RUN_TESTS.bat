@echo off
title OS Sync Lab - Run Tests
color 0E

cd /d "%~dp0"

echo.
echo  ========================================================
echo   Running OS Synchronization Test Suite
echo  ========================================================
echo.

node tests/run-tests.js

echo.
echo  ========================================================
echo.
echo  Press any key to run stress test, or close to exit...
pause >nul

node tests/concurrency-stress-test.js

echo.
pause
