@echo off
echo Starting AI Art Game Service...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run setup_env.bat first to set up the environment.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the server
echo Starting server at http://localhost:8081
echo Press Ctrl+C to stop the server
echo.
python test_web.py