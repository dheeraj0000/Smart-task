@echo off
echo ========================================
echo Fixing Django Installation
echo ========================================
echo.

cd backend

echo Step 1: Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not found!
    pause
    exit /b 1
)

echo.
echo Step 2: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 3: Installing Django (this may take a few minutes)...
echo Please wait, do not close this window...
python -m pip install Django
if errorlevel 1 (
    echo.
    echo Installation failed. Trying with --user flag...
    python -m pip install --user Django
)

echo.
echo Step 4: Installing Django REST Framework...
python -m pip install djangorestframework
if errorlevel 1 (
    python -m pip install --user djangorestframework
)

echo.
echo Step 5: Installing python-dateutil...
python -m pip install python-dateutil
if errorlevel 1 (
    python -m pip install --user python-dateutil
)

echo.
echo Step 6: Verifying installation...
python -c "import django; print('Django version:', django.get_version())" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Django installation verification failed!
    echo.
    echo Trying to continue anyway...
) else (
    echo Django installed successfully!
)

echo.
echo Step 7: Running migrations...
python manage.py migrate

echo.
echo Step 8: Starting server...
echo.
echo ========================================
echo Server will start at http://127.0.0.1:8000/
echo Press Ctrl+C to stop
echo ========================================
echo.

python manage.py runserver

pause

