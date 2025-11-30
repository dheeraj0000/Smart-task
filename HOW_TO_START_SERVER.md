# How to Start the Server - Step by Step Guide

## The Problem
You're getting "server cannot be reached" because the Django server is not running.

## Solution: Choose One Method Below

---

## Method 1: Use the Batch Script (Easiest) ⭐

1. **Double-click** `INSTALL_AND_RUN.bat` in the project root folder
   - This will automatically:
     - Install Django and all dependencies
     - Run database migrations
     - Start the server

2. **Wait for this message**:
   ```
   Starting development server at http://127.0.0.1:8000/
   ```

3. **Open your browser** and go to: `http://127.0.0.1:8000/`

---

## Method 2: Manual Setup (If Method 1 doesn't work)

### Step 1: Open Command Prompt or PowerShell
- Press `Win + R`
- Type `cmd` and press Enter
- OR search for "PowerShell" in Start menu

### Step 2: Navigate to the backend folder
```bash
cd "C:\Users\Dheeraj\OneDrive\Desktop\Smart task\backend"
```

### Step 3: Install Django and dependencies
```bash
pip install Django djangorestframework python-dateutil
```

**If you get permission errors**, try:
```bash
python -m pip install --user Django djangorestframework python-dateutil
```

### Step 4: Run database migrations
```bash
python manage.py migrate
```

### Step 5: Start the server
```bash
python manage.py runserver
```

### Step 6: Open in browser
Go to: `http://127.0.0.1:8000/`

---

## Method 3: Using Virtual Environment (Recommended for production)

### Step 1: Create virtual environment
```bash
cd backend
python -m venv venv
```

### Step 2: Activate it

**For Command Prompt (CMD):**
```bash
venv\Scripts\activate
```

**For PowerShell:**
```bash
venv\Scripts\Activate.ps1
```

If PowerShell gives an error, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run migrations
```bash
python manage.py migrate
```

### Step 5: Start server
```bash
python manage.py runserver
```

---

## Verify Server is Running

You should see output like this:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November XX, 2025 - XX:XX:XX
Django version X.X.X, using settings 'task_analyzer.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**If you see this, the server is running! ✅**

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"

**Solution**: Install Django:
```bash
pip install Django djangorestframework python-dateutil
```

### Issue: "python is not recognized"

**Solution**: 
- Python is not installed, OR
- Python is not in your PATH

Install Python from https://www.python.org/downloads/
Make sure to check "Add Python to PATH" during installation.

### Issue: Permission denied errors

**Solution**: Use `--user` flag:
```bash
python -m pip install --user Django djangorestframework python-dateutil
```

### Issue: Port 8000 already in use

**Solution**: Use a different port:
```bash
python manage.py runserver 8001
```
Then access at: `http://127.0.0.1:8001/`

---

## Quick Test

Once the server is running:

1. Open browser: `http://127.0.0.1:8000/`
2. You should see the Smart Task Analyzer interface
3. Try adding a task or pasting JSON
4. Click "Analyze Tasks"

---

## Important Notes

- **Keep the terminal window open** while the server is running
- **Don't close it** - closing it will stop the server
- **To stop the server**: Press `Ctrl+C` in the terminal
- **To restart**: Run `python manage.py runserver` again

---

**Need help?** Make sure:
1. ✅ Python is installed (`python --version`)
2. ✅ You're in the `backend` folder
3. ✅ Django is installed (`pip list | findstr Django`)
4. ✅ Server is running (see the "Starting development server" message)

