# 🚀 Perfect Deployment Steps (After GitHub Connection)

## Step-by-Step Guide

### Step 1: Generate Secret Key

Open PowerShell/Command Prompt and run:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copy the output** - you'll need it in Step 3.

---

### Step 2: Update ALLOWED_HOSTS

Before deploying, update your settings file:

1. Open: `backend/task_analyzer/settings.py`
2. Find the line: `ALLOWED_HOSTS = ['*']`
3. Replace it with:

```python
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'your-app-name.onrender.com',  # Will update after deployment
    'your-app-name.railway.app',    # If using Railway
]
```

**For now, you can use:**
```python
ALLOWED_HOSTS = ['*']  # We'll update after getting the actual URL
```

4. **Commit and push this change:**
```bash
git add backend/task_analyzer/settings.py
git commit -m "Update settings for deployment"
git push
```

---

### Step 3: Deploy on Render (Recommended)

#### A. Go to Render Dashboard

1. Visit: https://dashboard.render.com
2. Click **"New +"** button (top right)
3. Select **"Web Service"**

#### B. Connect Repository

1. If not connected, click **"Connect account"** → Connect GitHub
2. Select your repository from the list
3. Click **"Connect"**

#### C. Configure Service

Fill in these settings:

**Basic Settings:**
- **Name**: `smart-task-analyzer` (or your choice)
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `main` (or `master`)

**Build & Deploy:**
- **Environment**: `Python 3`
- **Build Command**: 
  ```
  cd backend && pip install -r requirements.txt && python manage.py migrate
  ```
- **Start Command**: 
  ```
  cd backend && gunicorn task_analyzer.wsgi:application
  ```

**Advanced Settings (Optional):**
- **Root Directory**: Leave empty (or set to project root if needed)

#### D. Add Environment Variables

Click **"Add Environment Variable"** and add:

1. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Value: (Paste the secret key from Step 1)

2. **DEBUG**
   - Key: `DEBUG`
   - Value: `False`

3. **PYTHON_VERSION** (Optional)
   - Key: `PYTHON_VERSION`
   - Value: `3.12.2`

#### E. Create Service

1. Scroll down and click **"Create Web Service"**
2. Wait 5-10 minutes for deployment

---

### Step 4: Update ALLOWED_HOSTS with Your URL

Once deployment starts, you'll see your app URL (e.g., `smart-task-analyzer.onrender.com`)

1. **Copy your app URL** from Render dashboard
2. **Update `backend/task_analyzer/settings.py`**:
   ```python
   ALLOWED_HOSTS = [
       '127.0.0.1',
       'localhost',
       'smart-task-analyzer.onrender.com',  # Your actual URL
   ]
   ```
3. **Commit and push**:
   ```bash
   git add backend/task_analyzer/settings.py
   git commit -m "Add Render URL to ALLOWED_HOSTS"
   git push
   ```
4. Render will **automatically redeploy** with the new settings

---

### Step 5: Verify Deployment

1. **Wait for deployment to complete** (green checkmark ✅)
2. **Click on your service name** in Render dashboard
3. **Click "Open Live URL"** or visit: `https://your-app-name.onrender.com`
4. **Test your app**:
   - Add a task
   - Test JSON import
   - Verify API works

---

## Alternative: Deploy on Railway

If you prefer Railway:

### Step 1: Go to Railway

1. Visit: https://railway.app
2. Sign up/login with GitHub

### Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository

### Step 3: Configure

Railway auto-detects Django! But verify:

1. **Settings** → **Variables**:
   - Add `SECRET_KEY`: (from Step 1 above)
   - Add `DEBUG`: `False`

2. **Settings** → **Deploy**:
   - Build Command: `cd backend && pip install -r requirements.txt && python manage.py migrate`
   - Start Command: `cd backend && gunicorn task_analyzer.wsgi:application`

### Step 4: Deploy

Railway will automatically:
- Install dependencies
- Run migrations
- Start the server

### Step 5: Get Your URL

1. Click on your service
2. Go to **"Settings"** → **"Domains"**
3. Copy your Railway URL (e.g., `smart-task-analyzer.railway.app`)
4. Update `ALLOWED_HOSTS` as in Step 4 above

---

## Troubleshooting

### Issue: Build Fails

**Check:**
- Build logs in Render/Railway dashboard
- Make sure `requirements.txt` is in `backend/` folder
- Verify Python version matches `runtime.txt`

### Issue: App Crashes After Deployment

**Check:**
- Environment variables are set correctly
- `ALLOWED_HOSTS` includes your domain
- Logs in dashboard for error messages

### Issue: Static Files Not Loading

**Solution:** Already handled with WhiteNoise, but if issues persist:
- Check that `STATIC_ROOT` is set in settings
- Verify WhiteNoise middleware is in MIDDLEWARE list

### Issue: Database Errors

**Solution:**
- Most platforms auto-create database
- Make sure migrations run in build command
- Check database URL in environment variables

---

## Success Checklist

After deployment, verify:

- [ ] App loads at your URL
- [ ] CSS and JavaScript load correctly
- [ ] Can add tasks via form
- [ ] Can import JSON tasks
- [ ] API endpoints work (`/api/tasks/analyze/`)
- [ ] Priority scoring works
- [ ] Results display correctly

---

## Final Steps

1. ✅ **Test your live app thoroughly**
2. ✅ **Update README.md** with your deployment URL
3. ✅ **Share the URL** with recruiters
4. ✅ **Celebrate!** 🎉

---

## Quick Reference Commands

```bash
# Generate Secret Key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Update and push changes
git add .
git commit -m "Your message"
git push
```

---

**You're almost there! Follow these steps and your app will be live! 🚀**

