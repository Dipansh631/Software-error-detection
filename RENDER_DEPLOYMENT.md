# 🚀 Render Deployment Guide

## Complete Setup for Software Defects Detection Website

### 📋 Prerequisites

1. **GitHub Account** - Your code needs to be on GitHub
2. **Render Account** - Sign up at https://render.com (free tier available)
3. **Git Repository** - Your project pushed to GitHub

---

## 🔧 Step 1: Prepare Your Repository

### Files Already Created:
- ✅ `render.yaml` - Render configuration
- ✅ `Procfile` - Process file for web server
- ✅ `requirements.txt` - Python dependencies (updated with gunicorn)
- ✅ `runtime.txt` - Python version specification

### Make sure these files exist in your repo:
```
your-project/
├── app.py                 # Flask application
├── requirements.txt       # Dependencies
├── Procfile              # Process file
├── runtime.txt           # Python version
├── render.yaml           # Render config (optional)
├── model/
│   └── defect_model.pkl  # Your trained model
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

---

## 📤 Step 2: Push to GitHub

1. **Initialize Git** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Prepare for Render deployment"
   ```

2. **Create GitHub Repository:**
   - Go to https://github.com/new
   - Create a new repository
   - Don't initialize with README (if you already have files)

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

---

## 🌐 Step 3: Deploy on Render

### Option A: Using render.yaml (Recommended)

1. **Go to Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Sign in with GitHub

2. **Create New Web Service:**
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub account if not already connected
   - Select your repository

3. **Configure Service:**
   - **Name:** `software-defect-detection` (or your choice)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** Leave empty (or specify if needed)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

4. **Environment Variables:**
   - Click "Advanced" → "Add Environment Variable"
   - Add if needed:
     - `PYTHON_VERSION=3.11.0`
     - `PORT=10000` (Render sets this automatically)

5. **Click "Create Web Service"**

### Option B: Manual Configuration

If not using render.yaml:

1. **Create New Web Service** on Render
2. **Connect GitHub Repository**
3. **Settings:**
   - **Name:** Your app name
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free (or paid if needed)

---

## ⚙️ Step 4: Update app.py for Production

Your `app.py` should work, but make sure it uses the PORT environment variable:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False for production
```

**Note:** Render uses gunicorn, so the `if __name__ == '__main__'` block won't run. That's fine - gunicorn handles it.

---

## 🔍 Step 5: Verify Deployment

1. **Check Build Logs:**
   - Go to your service on Render
   - Click "Logs" tab
   - Watch for build progress
   - Should see: "Build successful"

2. **Check Your App:**
   - Render provides a URL like: `https://your-app-name.onrender.com`
   - Visit the URL
   - Your app should be live!

---

## 🐛 Troubleshooting

### Build Fails

**Problem:** Dependencies not installing
- **Solution:** Check `requirements.txt` has all packages
- Check build logs for specific errors

**Problem:** Module not found
- **Solution:** Add missing package to `requirements.txt`
- Make sure all imports are in requirements

### App Crashes

**Problem:** Port binding error
- **Solution:** Make sure using `0.0.0.0` and `$PORT` in Procfile
- Render sets PORT automatically

**Problem:** Model not found
- **Solution:** Make sure `model/defect_model.pkl` is in your repo
- Or the app will use fallback model

**Problem:** Template not found
- **Solution:** Verify `templates/` folder is in repo
- Check file paths are correct

### Static Files Not Loading

**Problem:** CSS/JS not showing
- **Solution:** Check `static/` folder structure
- Verify `url_for('static', ...)` paths in templates
- Hard refresh browser (Ctrl+F5)

---

## 📝 Important Notes

### Free Tier Limitations:
- ⚠️ **Spins down after 15 minutes** of inactivity
- ⚠️ **First request after spin-down takes ~30 seconds** (cold start)
- ⚠️ **512MB RAM limit**
- ✅ **Unlimited bandwidth**
- ✅ **Free SSL certificate**

### Production Recommendations:
- Use **Starter Plan ($7/month)** for:
  - No spin-downs
  - Faster response times
  - More resources

### Environment Variables:
You can add these in Render dashboard:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secret-key` (if using sessions)

---

## 🔄 Updating Your App

1. **Make changes locally**
2. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```
3. **Render auto-deploys** when you push to main branch
4. **Check deployment** in Render dashboard

---

## 📊 Monitoring

- **Logs:** View real-time logs in Render dashboard
- **Metrics:** Monitor CPU, memory, and response times
- **Alerts:** Set up email alerts for crashes

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `requirements.txt` includes all dependencies
- [ ] `Procfile` created with correct command
- [ ] `runtime.txt` specifies Python version
- [ ] `model/defect_model.pkl` exists (or fallback works)
- [ ] `templates/` and `static/` folders in repo
- [ ] Render service created
- [ ] Build successful
- [ ] App accessible at Render URL

---

## 🎉 Success!

Once deployed, your app will be available at:
```
https://your-app-name.onrender.com
```

Share this URL with anyone! 🚀

---

## 🔗 Useful Links

- **Render Dashboard:** https://dashboard.render.com
- **Render Docs:** https://render.com/docs
- **Render Status:** https://status.render.com

---

## 💡 Pro Tips

1. **Use render.yaml** for easier configuration
2. **Monitor logs** during first deployment
3. **Test locally** with gunicorn before deploying:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```
4. **Keep requirements.txt updated** with all dependencies
5. **Use environment variables** for sensitive data

Your Flask app is now ready for Render deployment! 🎊

