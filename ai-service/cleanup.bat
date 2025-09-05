@echo off
echo Cleaning up AI service processes...

REM Kill all Python processes (be careful - this kills ALL Python processes!)
wmic process where "name='python.exe'" delete 2>nul

REM Alternative: Kill processes by port (more targeted)
REM for /f "tokens=5" %%i in ('netstat -ano ^| findstr :8080') do taskkill /PID %%i /F 2>nul

echo Cleanup complete.
timeout /t 2 >nul