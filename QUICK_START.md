# Quick Start Guide - Get the App Running

## Option 1: Using Batch Script (Easiest - Windows)

1. **Double-click** `backend/setup_and_run.bat`
   - This will automatically:
     - Create a virtual environment
     - Install all dependencies
     - Run database migrations
     - Start the server

2. **Open your browser** and go to: `http://127.0.0.1:8000/`

3. **To stop the server**: Press `Ctrl+C` in the command window

---

## Option 2: Manual Setup (Step by Step)

### Step 1: Open Command Prompt or PowerShell
Navigate to the project folder:
```bash
cd "C:\Users\Dheeraj\OneDrive\Desktop\Smart task\backend"
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**For Command Prompt (CMD):**
```bash
venv\Scripts\activate
```

**For PowerShell:**
```bash
venv\Scripts\Activate.ps1
```

If you get an execution policy error in PowerShell, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run Database Migrations
```bash
python manage.py migrate
```

### Step 6: Start the Server
```bash
python manage.py runserver
```

### Step 7: Open in Browser
Go to: `http://127.0.0.1:8000/`

---

## Option 3: Using PowerShell Script

1. **Open PowerShell** in the `backend` folder
2. **Run the script:**
   ```powershell
   .\setup_and_run.ps1
   ```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then run the script again.

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"

**Solution:** Make sure you've activated the virtual environment:
```bash
# In backend folder
venv\Scripts\activate
```

Then install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Execution Policy" error in PowerShell

**Solution:** Run this command:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Port 8000 already in use

**Solution:** Use a different port:
```bash
python manage.py runserver 8001
```
Then access at: `http://127.0.0.1:8001/`

### Issue: Database errors

**Solution:** Delete the database and re-run migrations:
```bash
del db.sqlite3
python manage.py migrate
```

---

## Testing the Application

Once the server is running:

1. **Add Tasks**: Use the form to add individual tasks or paste JSON in bulk
2. **Select Strategy**: Choose from 4 sorting strategies
3. **Analyze**: Click "Analyze Tasks" to see prioritized results
4. **View Results**: See top 3 recommendations and all tasks sorted by priority

### Sample JSON for Testing

You can use the sample tasks from `frontend/sample_tasks.json`:
- Copy the JSON content
- Go to "Bulk Import (JSON)" tab
- Paste and click "Load Tasks"
- Click "Analyze Tasks"

---

## Next Steps After Running

1. ✅ Test adding tasks via form
2. ✅ Test bulk JSON import
3. ✅ Try all 4 sorting strategies
4. ✅ Verify priority scores make sense
5. ✅ Check that circular dependencies are detected

---

## Need Help?

If you encounter any issues:
1. Make sure Python 3.8+ is installed
2. Ensure you're in the `backend` directory
3. Verify virtual environment is activated
4. Check that all dependencies installed correctly

**Happy coding! 🚀**

