# Testing the API - Troubleshooting "Failed to fetch" Error

## Step 1: Verify Server is Running

Make sure the Django server is running. You should see output like:
```
Starting development server at http://127.0.0.1:8000/
```

If not running, start it:
```bash
cd backend
python manage.py runserver
```

## Step 2: Test API Endpoint Directly

Open your browser and go to:
```
http://127.0.0.1:8000/api/tasks/suggest/
```

You should see JSON response (even if it's sample data).

## Step 3: Test with Browser Console

1. Open the app: `http://127.0.0.1:8000/`
2. Open browser Developer Tools (F12)
3. Go to Console tab
4. Try this command:
```javascript
fetch('/api/tasks/suggest/')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

This will show you the exact error.

## Step 4: Check Network Tab

1. Open Developer Tools (F12)
2. Go to Network tab
3. Try to analyze tasks
4. Look for the `/api/tasks/analyze/` request
5. Click on it to see:
   - Request URL
   - Status code
   - Response
   - Error message

## Common Issues:

### Issue 1: Server Not Running
**Solution**: Start the server with `python manage.py runserver`

### Issue 2: Wrong Port
**Solution**: Make sure you're accessing `http://127.0.0.1:8000/` (not 8001 or other port)

### Issue 3: CSRF Error
**Solution**: The code has been updated to exempt CSRF. Restart the server after the update.

### Issue 4: CORS Error
**Solution**: Should be fixed with the settings update. Restart server.

## Quick Fix:

1. **Restart the Django server** (stop with Ctrl+C, then run again):
   ```bash
   cd backend
   python manage.py runserver
   ```

2. **Clear browser cache** (Ctrl+Shift+Delete) or use Incognito mode

3. **Try again** with the JSON import

If still not working, check the browser console (F12) for the exact error message.

