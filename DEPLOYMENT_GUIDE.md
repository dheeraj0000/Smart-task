# Deployment Guide - Smart Task Analyzer

This guide covers deploying your Smart Task Analyzer to various platforms.

## 🚀 Quick Deploy Options

### Option 1: Render (Recommended - Easiest) ⭐

**Free tier available, easy setup**

#### Steps:

1. **Create a GitHub Repository**
   - Go to https://github.com
   - Create a new repository
   - Push your code:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin https://github.com/yourusername/your-repo-name.git
     git push -u origin main
     ```

2. **Deploy on Render**
   - Go to https://render.com
   - Sign up/login (free)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: smart-task-analyzer (or your choice)
     - **Environment**: Python 3
     - **Build Command**: `cd backend && pip install -r requirements.txt && python manage.py migrate`
     - **Start Command**: `cd backend && gunicorn task_analyzer.wsgi:application`
     - **Root Directory**: Leave empty (or set to project root)
   - Add Environment Variables:
     - `SECRET_KEY`: Generate one (see below)
     - `DEBUG`: `False`
   - Click "Create Web Service"

3. **Generate Secret Key**:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. **Update ALLOWED_HOSTS**:
   - In `backend/task_analyzer/settings.py`, add your Render URL:
     ```python
     ALLOWED_HOSTS = ['your-app-name.onrender.com', '127.0.0.1', 'localhost']
     ```

5. **Wait for deployment** (5-10 minutes)

6. **Access your app**: `https://your-app-name.onrender.com`

---

### Option 2: Railway (Also Easy)

**Free tier with $5 credit**

#### Steps:

1. **Push to GitHub** (same as Render step 1)

2. **Deploy on Railway**
   - Go to https://railway.app
   - Sign up/login
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Django
   - Add Environment Variables:
     - `SECRET_KEY`: (generate one)
     - `DEBUG`: `False`
   - Railway will automatically:
     - Install dependencies
     - Run migrations
     - Start the server

3. **Update ALLOWED_HOSTS**:
   ```python
   ALLOWED_HOSTS = ['your-app-name.railway.app', '127.0.0.1', 'localhost']
   ```

4. **Access your app**: `https://your-app-name.railway.app`

---

### Option 3: PythonAnywhere (Beginner-Friendly)

**Free tier available**

#### Steps:

1. **Sign up** at https://www.pythonanywhere.com

2. **Upload your code**:
   - Go to "Files" tab
   - Upload your project files
   - Or use Git: `git clone https://github.com/yourusername/your-repo.git`

3. **Set up virtual environment**:
   - Open "Consoles" → "Bash"
   - Navigate to your project:
     ```bash
     cd ~/your-project-name/backend
     ```
   - Create venv:
     ```bash
     python3.10 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

4. **Configure Web App**:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - Set:
     - **Source code**: `/home/yourusername/your-project-name/backend`
     - **Working directory**: `/home/yourusername/your-project-name/backend`
   - In WSGI configuration file, add:
     ```python
     import os
     import sys
     
     path = '/home/yourusername/your-project-name/backend'
     if path not in sys.path:
         sys.path.append(path)
     
     os.environ['DJANGO_SETTINGS_MODULE'] = 'task_analyzer.settings'
     
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```

5. **Run migrations**:
   - In Bash console:
     ```bash
     source venv/bin/activate
     cd ~/your-project-name/backend
     python manage.py migrate
     ```

6. **Reload web app** (click reload button)

7. **Access**: `https://yourusername.pythonanywhere.com`

---

### Option 4: Heroku (Classic, but requires credit card for free tier)

#### Steps:

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Login**:
   ```bash
   heroku login
   ```

3. **Create app**:
   ```bash
   cd backend
   heroku create your-app-name
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```

5. **Deploy**:
   ```bash
   git init
   git add .
   git commit -m "Deploy to Heroku"
   heroku git:remote -a your-app-name
   git push heroku main
   ```

6. **Run migrations**:
   ```bash
   heroku run python manage.py migrate
   ```

7. **Open**: `https://your-app-name.herokuapp.com`

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [ ] **Update ALLOWED_HOSTS** in `settings.py`:
  ```python
  ALLOWED_HOSTS = ['your-domain.com', '127.0.0.1', 'localhost']
  ```

- [ ] **Set DEBUG = False** for production (or use environment variable)

- [ ] **Generate a new SECRET_KEY** for production:
  ```python
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```

- [ ] **Collect static files** (if needed):
  ```bash
  python manage.py collectstatic --noinput
  ```

- [ ] **Test locally** with production settings:
  ```bash
  python manage.py runserver --settings=task_analyzer.settings_production
  ```

- [ ] **Update requirements.txt** (already done - includes gunicorn, whitenoise)

- [ ] **Commit all changes to Git**

---

## 🔧 Platform-Specific Configuration

### For Render/Railway:

1. **Create `render.yaml`** (optional, for Render):
   ```yaml
   services:
     - type: web
       name: smart-task-analyzer
       env: python
       buildCommand: cd backend && pip install -r requirements.txt && python manage.py migrate
       startCommand: cd backend && gunicorn task_analyzer.wsgi:application
       envVars:
         - key: SECRET_KEY
           generateValue: true
         - key: DEBUG
           value: False
   ```

### For Railway:

Railway auto-detects Django. Just make sure:
- `Procfile` exists (already created)
- `requirements.txt` is in backend folder (already done)

---

## 🌐 Domain Configuration

After deployment, you'll get a URL like:
- Render: `https://your-app.onrender.com`
- Railway: `https://your-app.railway.app`
- PythonAnywhere: `https://yourusername.pythonanywhere.com`

Update `ALLOWED_HOSTS` with your actual domain.

---

## 🐛 Troubleshooting

### Issue: Static files not loading

**Solution**: Add WhiteNoise middleware (already in requirements):
```python
# In settings.py, add to MIDDLEWARE:
MIDDLEWARE = [
    # ... other middleware ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
```

### Issue: Database errors

**Solution**: Most platforms provide DATABASE_URL. Make sure migrations run:
```bash
python manage.py migrate
```

### Issue: 500 Internal Server Error

**Solution**: 
1. Check logs on your platform
2. Verify SECRET_KEY is set
3. Check ALLOWED_HOSTS includes your domain
4. Ensure DEBUG=False in production

### Issue: CSRF errors

**Solution**: Already handled with `@csrf_exempt` in views, but for production you might want to configure CSRF properly.

---

## 📝 Recommended: Render Deployment

**Why Render?**
- ✅ Free tier (no credit card needed)
- ✅ Easy GitHub integration
- ✅ Automatic deployments
- ✅ Good documentation
- ✅ Free SSL certificate

**Quick Start:**
1. Push code to GitHub
2. Connect to Render
3. Deploy!
4. Done in 10 minutes

---

## 🎯 Next Steps After Deployment

1. **Test the deployed app**:
   - Visit your URL
   - Try adding tasks
   - Test the API endpoints

2. **Update your README**:
   - Add deployment link
   - Update setup instructions

3. **Share with recruiters**:
   - Include the live URL in your submission
   - Mention deployment in your README

---

## 💡 Pro Tips

1. **Use environment variables** for sensitive data (SECRET_KEY, database URLs)
2. **Enable logging** to debug production issues
3. **Set up monitoring** (optional, but impressive)
4. **Use a custom domain** (optional, for professional look)

---

**Good luck with your deployment! 🚀**

