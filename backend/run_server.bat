@echo off
echo ========================================
echo Starting Smart Task Analyzer Server
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

echo Starting Django development server...
echo The application will be available at: http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

pause

