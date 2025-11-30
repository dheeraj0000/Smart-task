# Step-by-Step: Install Django and Fix "ModuleNotFoundError"

## The Problem
You're getting `ModuleNotFoundError: No module named 'django'` which means Django isn't installed or Python can't find it.

## Solution: Follow These Steps Exactly

### Step 1: Verify Python is Working

Open PowerShell or Command Prompt and run:
```bash
python --version
```

You should see something like: `Python 3.12.2`

If you get an error, Python isn't installed or not in PATH.

---

### Step 2: Check Which Python You're Using

```bash
where python
```

This shows the path to Python. Note this path.

---

### Step 3: Install Django (Try These Methods in Order)

#### Method A: Standard Installation (Try This First)
```bash
python -m pip install Django djangorestframework python-dateutil
```

**Wait for it to complete!** It may take 2-5 minutes.

#### Method B: If Method A Fails - Use --user Flag
```bash
python -m pip install --user Django djangorestframework python-dateutil
```

This installs to your user directory (no admin rights needed).

#### Method C: If Still Fails - Upgrade pip First
```bash
python -m pip install --upgrade pip
python -m pip install Django djangorestframework python-dateutil
```

---

### Step 4: Verify Django is Installed

```bash
python -c "import django; print('Django version:', django.get_version())"
```

**If this works**, you'll see: `Django version: 4.2.x`

**If you get an error**, Django isn't installed correctly. Try Method B or C above.

---

### Step 5: Navigate to Backend Folder

```bash
cd "C:\Users\Dheeraj\OneDrive\Desktop\Smart task\backend"
```

---

### Step 6: Run Migrations

```bash
python manage.py migrate
```

---

### Step 7: Start the Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

---

## Common Issues and Fixes

### Issue 1: "pip is not recognized"

**Fix**: Use `python -m pip` instead of just `pip`

### Issue 2: Permission Denied

**Fix**: Use `--user` flag:
```bash
python -m pip install --user Django djangorestframework python-dateutil
```

### Issue 3: Installation Takes Forever

**Fix**: 
- Check your internet connection
- Try installing one package at a time:
  ```bash
  python -m pip install Django
  python -m pip install djangorestframework
  python -m pip install python-dateutil
  ```

### Issue 4: "Requirement already satisfied" but Django still not found

**Fix**: You might have multiple Python installations. Check:
```bash
python -c "import sys; print(sys.executable)"
```

This shows which Python is being used. Make sure you're using the same Python for installation and running.

### Issue 5: Virtual Environment Confusion

If you created a virtual environment but didn't activate it:
- **Activate it first**:
  ```bash
  venv\Scripts\activate
  ```
- Then install Django:
  ```bash
  pip install Django djangorestframework python-dateutil
  ```

---

## Quick Test Script

Copy and paste this entire block into PowerShell:

```powershell
# Step 1: Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
python --version

# Step 2: Install Django
Write-Host "`nInstalling Django..." -ForegroundColor Yellow
python -m pip install --user Django djangorestframework python-dateutil

# Step 3: Verify Installation
Write-Host "`nVerifying Django installation..." -ForegroundColor Yellow
python -c "import django; print('Django version:', django.get_version())"

# Step 4: Navigate to backend
Write-Host "`nNavigating to backend folder..." -ForegroundColor Yellow
cd backend

# Step 5: Run migrations
Write-Host "`nRunning migrations..." -ForegroundColor Yellow
python manage.py migrate

# Step 6: Start server
Write-Host "`nStarting server..." -ForegroundColor Green
Write-Host "Server will be at: http://127.0.0.1:8000/" -ForegroundColor Cyan
python manage.py runserver
```

---

## Still Having Issues?

1. **Check Python Installation**:
   - Go to: https://www.python.org/downloads/
   - Download and install Python 3.8 or higher
   - **IMPORTANT**: Check "Add Python to PATH" during installation

2. **Try Using py Launcher** (Windows):
   ```bash
   py -3 -m pip install Django djangorestframework python-dateutil
   py -3 manage.py migrate
   py -3 manage.py runserver
   ```

3. **Check if Django is in a different location**:
   ```bash
   python -c "import sys; print('\n'.join(sys.path))"
   ```

---

## Success Checklist

After installation, verify:
- [ ] `python --version` works
- [ ] `python -c "import django"` works (no error)
- [ ] `python manage.py migrate` runs successfully
- [ ] `python manage.py runserver` starts the server
- [ ] You can access `http://127.0.0.1:8000/` in browser

If all checkboxes are ✅, you're good to go!

