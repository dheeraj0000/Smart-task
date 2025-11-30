# Fix Static Files (CSS/JS) Not Loading in Production

## The Problem

CSS and JavaScript files aren't loading on your live site because Django needs to collect and serve static files properly in production.

## Solution: Update Build Command

### Step 1: Update Render Build Command

1. Go to: https://dashboard.render.com
2. Click on your **Web Service**
3. Click **"Settings"** tab
4. Find **"Build Command"** section
5. **Replace** the current build command with:

```
cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Important:** The new part is `python manage.py collectstatic --noinput` - this collects all static files.

6. Click **"Save Changes"**
7. Render will automatically redeploy

---

## What Changed

### 1. Updated HTML to Use Django Static Tags

The HTML now uses `{% static %}` tags which Django will convert to proper URLs:
- `{% static 'styles.css' %}` → `/static/styles.css`
- `{% static 'script.js' %}` → `/static/script.js`

### 2. Updated Build Command

Added `collectstatic` to collect all static files into the `staticfiles` folder during build.

### 3. WhiteNoise Middleware

WhiteNoise (already configured) will serve these static files in production.

---

## After Redeployment

1. **Wait 5-10 minutes** for redeployment to complete
2. **Hard refresh** your browser (Ctrl+F5 or Cmd+Shift+R)
3. **Check** if CSS and JS are loading

---

## Verify It's Working

1. Open your live site
2. Right-click → "Inspect" or press F12
3. Go to **"Network"** tab
4. Refresh the page
5. Look for:
   - `styles.css` - should show status 200 (success)
   - `script.js` - should show status 200 (success)

If they show 404, the deployment might still be in progress. Wait a bit longer.

---

## Alternative: If Still Not Working

If after redeployment it still doesn't work, try this:

### Option 1: Check WhiteNoise is Working

Make sure WhiteNoise middleware is in your settings (it should be). Check `backend/task_analyzer/settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Should be here
    # ... rest of middleware
]
```

### Option 2: Manual Static File Collection

If needed, you can manually collect static files:

1. In Render dashboard → **"Shell"** tab
2. Run:
   ```bash
   cd backend
   python manage.py collectstatic --noinput
   ```

### Option 3: Check STATIC_ROOT

Make sure `STATIC_ROOT` is set correctly in settings:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

---

## Quick Checklist

- [ ] Updated Build Command to include `collectstatic`
- [ ] Saved changes in Render
- [ ] Waited for redeployment to complete
- [ ] Hard refreshed browser (Ctrl+F5)
- [ ] Checked Network tab - files should show 200 status

---

## Files Changed

1. ✅ `frontend/index.html` - Now uses `{% static %}` tags
2. ✅ `backend/render.yaml` - Build command updated
3. ✅ `backend/task_analyzer/settings.py` - STATIC_URL fixed (added leading slash)

---

**After updating the build command and redeploying, your CSS and JS should load! 🎨**

