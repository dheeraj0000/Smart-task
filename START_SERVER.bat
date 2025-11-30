@echo off
echo ========================================
echo Starting Smart Task Analyzer Server
echo ========================================
echo.

cd backend

echo Checking if Django is installed...
python -c "import django" 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Django is not installed!
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Failed to install dependencies.
        echo Please install manually: pip install Django djangorestframework python-dateutil
        pause
        exit /b 1
    )
)

echo.
echo Running database migrations...
python manage.py migrate

echo.
echo ========================================
echo Starting Django development server...
echo ========================================
echo.
echo The application will be available at:
echo   http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

pause

