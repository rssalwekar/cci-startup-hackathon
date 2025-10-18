# 🚀 Railway Deployment Guide

## Why Railway?
- **Easiest deployment**: Just connect GitHub repo
- **Automatic HTTPS**: Gets you a secure domain immediately
- **Free tier**: $5 credit monthly (usually enough for small apps)
- **No complex config**: Works with Django out of the box
- **Fixes microphone issues**: HTTPS domain resolves browser permission problems

## Quick Setup (5 minutes)

### 1. Push to GitHub
```bash
# If not already in git
git init
git add .
git commit -m "Initial commit"

# Push to GitHub (create repo first on github.com)
git remote add origin https://github.com/yourusername/ai-interview-platform.git
git push -u origin main
```

### 2. Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Django and deploys!

### 3. Set Environment Variables
In Railway dashboard:
- Go to your project → Variables tab
- Add:
  - `KRONOS_API_KEY` = your kronos key
  - `ELEVEN_LABS_API_KEY` = your elevenlabs key
  - `SECRET_KEY` = generate a new Django secret key

### 4. Get Your URL
Railway gives you a URL like: `https://your-app-name.railway.app`

## Expected Results
- ✅ HTTPS domain for microphone access
- ✅ Automatic deployments on git push
- ✅ Easy environment variable management
- ✅ Free tier should be sufficient for testing

## Alternative: Render.com
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. "New Web Service" → Connect your repo
4. Set environment variables
5. Deploy!

## Alternative: Vercel (with Django adapter)
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`
3. Follow prompts
4. Set environment variables in Vercel dashboard

## Cost Comparison
- **Railway**: $5/month credit (usually free for small apps)
- **Render**: Free tier available
- **Vercel**: Generous free tier
- **Heroku**: $7/month minimum

## Why These Work Better Than Modal
- **Simpler setup**: No complex configuration files
- **GitHub integration**: Auto-deploy on push
- **Better Django support**: Designed for web apps
- **Easier debugging**: Better logging and monitoring
