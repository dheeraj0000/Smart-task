# Quick Setup Guide

## Prerequisites Check

Before starting, ensure you have:
- Python 3.8 or higher installed
- pip (Python package manager)

Check Python version:
```bash
python --version
# or
python3 --version
```

## Step-by-Step Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Start the Server
```bash
python manage.py runserver
```

### 6. Open in Browser
Navigate to: `http://127.0.0.1:8000/`

## Testing

Run the test suite:
```bash
python manage.py test tasks.tests
```

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Make sure you're in the `backend` directory and have activated your virtual environment.

### Issue: Port already in use
**Solution**: Use a different port:
```bash
python manage.py runserver 8001
```

### Issue: Database errors
**Solution**: Delete `db.sqlite3` and run migrations again:
```bash
rm db.sqlite3  # Linux/Mac
del db.sqlite3  # Windows
python manage.py migrate
```

## Project Structure Reminder

```
task-analyzer/
├── backend/          # Django project (run commands from here)
│   ├── manage.py
│   ├── task_analyzer/
│   └── tasks/
└── frontend/         # HTML/CSS/JS files
```

## Next Steps

1. Open the application in your browser
2. Add some tasks using the form or bulk JSON import
3. Select a sorting strategy
4. Click "Analyze Tasks" to see prioritized results

For detailed information, see the main [README.md](README.md).

