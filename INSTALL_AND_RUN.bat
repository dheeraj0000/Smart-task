@echo off
echo ========================================
echo Smart Task Analyzer - Complete Setup
echo ========================================
echo.

cd backend

echo Step 1: Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Step 2: Installing Django and dependencies...
echo This may take a few minutes...
echo.

python -m pip install --user Django djangorestframework python-dateutil

if errorlevel 1 (
    echo.
    echo Installation failed. Trying alternative method...
    pip install Django djangorestframework python-dateutil
    if errorlevel 1 (
        echo.
        echo ERROR: Could not install dependencies.
        echo Please install manually:
        echo   pip install Django djangorestframework python-dateutil
        pause
        exit /b 1
    )
)

echo.
echo Step 3: Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo.
    echo Migration failed. This might be okay if it's the first run.
)

echo.
echo ========================================
echo Setup Complete! Starting server...
echo ========================================
echo.
echo The application will be available at:
echo   http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

python manage.py runserver

pause

