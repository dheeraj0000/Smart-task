@echo off
echo ========================================
echo Smart Task Analyzer - Setup and Run
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 4: Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo Failed to run migrations
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup complete! Starting server...
echo ========================================
echo.
echo The application will be available at: http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

pause

