@echo off
echo Setting up AI Art Game Service Environment...
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% neq 0 (
    echo Error creating virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Error activating virtual environment
    pause
    exit /b 1
)

REM Install requirements
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error installing requirements
    pause
    exit /b 1
)

REM Install CUDA-enabled PyTorch specifically
echo Installing CUDA-enabled PyTorch...
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
if %ERRORLEVEL% neq 0 (
    echo Error installing CUDA PyTorch
    pause
    exit /b 1
)

echo.
echo Environment setup complete!
echo To start the server, run: python test_web.py
echo.
pause