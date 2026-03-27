# ⚡ React Frontend - Quick Start (5 Minutes)

Get the fraud detection dashboard running in 5 minutes!

## 🚀 Ultra-Quick Setup

### Step 1: Navigate to Frontend (30 seconds)
```bash
cd frontend
```

### Step 2: Install Dependencies (2 minutes)
```bash
npm install
```

### Step 3: Start Development Server (30 seconds)
```bash
npm run dev
```

**Expected output:**
```
  VITE v5.0.8  ready in 245 ms

  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

### Step 4: Open in Browser (1 minute)

Navigate to: **http://localhost:3000**

### Step 5: Login with Demo Account (30 seconds)

**Demo Credentials:**
- Username: `demo_analyst`
- Password: `demo123`

Or click **"Demo Login"** button

---

## ✨ That's It! You're Done! 🎉

Your fraud detection dashboard is now running with:
- ✅ Real-time system monitoring
- ✅ Transaction fraud analysis
- ✅ Phishing email detection
- ✅ Behavioral anomaly detection
- ✅ Analytics dashboard

---

## 📖 Features Quick Tour

### 🏠 Dashboard
See system health, model status, and quick stats

### 💳 Transactions
Analyze any transaction for fraud:
1. Enter user ID and amount
2. Click "Analyze Transaction"
3. Get instant fraud scores

**Example:**
```
User ID: user123
Amount: $150.00
Merchant: Amazon
Type: Purchase
```

### 📧 Phishing Detection
Check emails for phishing:
1. Paste sender email
2. Enter subject and body
3. Click "Analyze Email"
4. See phishing score and indicators

### 👥 Behavior Analysis
Detect unusual user behavior:
1. Enter user ID
2. Select behavior type (login or access pattern)
3. Enter metrics
4. Get anomaly score

### 📈 Analytics
View reports, stats, and alerts

---

## 🔧 Environment Setup (Optional)

To change backend API URL:

### 1. Copy environment file
```bash
cp .env.example .env.local
```

### 2. Edit `.env.local`
```env
VITE_API_URL=http://localhost:8000
```

### 3. Restart dev server
```
Press Ctrl+C to stop
npm run dev
```

---

## 🏗️ Build for Production

When ready to deploy:

```bash
# Build
npm run build

# Test build locally
npm run preview
```

Result: Optimized `dist/` folder ready for deployment

---

## 🌐 Deploy (Choose One)

### ⚡ Vercel (Easiest - 2 minutes)
```bash
npm install -g vercel
vercel
```

### 🚂 Railway (Full Stack - 5 minutes)
```bash
npm install -g @railway/cli
railway up
```

### 🎨 Render (Simple - 5 minutes)
1. Go to: https://render.com
2. New Static Site
3. Connect GitHub repo
4. Done!

### 🐳 Docker (Containerized)
```bash
docker build -f frontend/Dockerfile -t fraud-detection-frontend .
docker run -p 3000:3000 fraud-detection-frontend
```

---

## 🐛 Troubleshooting

### Can't connect to backend?
- ✅ Backend running on port 8000? Run: `docker-compose up -d`
- ✅ VITE_API_URL correct? Check `.env.local`
- ✅ CORS enabled? Check backend settings

### Port 3000 already in use?
```bash
# Use different port
npm run dev -- --port 3001
```

### Dependencies error?
```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## 📚 Full Documentation

- **README.md** - Complete feature documentation
- **FRONTEND_DEPLOYMENT.md** - Advanced deployment guide
- **FRONTEND_SUMMARY.md** - Full build summary

---

## 🎯 Common Tasks

### Change Backend URL
Edit `.env.local`:
```env
VITE_API_URL=https://your-api.com
```

### Add Custom Branding
Edit:
- `vite.config.ts` - App name
- `tailwind.config.js` - Colors
- `src/components/Sidebar.tsx` - Logo

### Enable Dark Mode
Already built in! Browser respects `prefers-color-scheme`

### Add New Page
1. Create `src/pages/MyPage.tsx`
2. Add to `src/App.tsx` routes
3. Add to sidebar in `src/components/Sidebar.tsx`

---

## 💡 Pro Tips

### Development
- Use `npm run dev` for hot reload
- Open DevTools with F12
- Check Network tab for API calls
- Use Console for debugging

### Building
- Run `npm run build` to check build size
- Use `npm run preview` to test production build
- Check `dist/` folder size (should be ~85KB gzipped)

### Performance
- Use Chrome DevTools Lighthouse
- Check Network tab for slow requests
- Enable SourceMaps in `vite.config.ts` for debugging

---

## ✅ Quick Checklist

- [ ] Navigated to `frontend/` folder
- [ ] Ran `npm install`
- [ ] Started `npm run dev`
- [ ] Opened http://localhost:3000
- [ ] Logged in with demo credentials
- [ ] Tried analyzing a transaction
- [ ] Checked phishing detection
- [ ] Viewed behavior analysis

**All done?** 🎉 You're ready to use the dashboard!

---

## 🚀 Next Steps

1. **Customize Dashboard** - Edit pages to match your needs
2. **Connect Real Data** - Update backend API
3. **Deploy** - Use one of the deployment methods
4. **Monitor** - Set up alerts and logging
5. **Scale** - Add more features as needed

---

## 📞 Quick Links

- **Frontend Docs**: [README.md](./README.md)
- **Deployment Guide**: [FRONTEND_DEPLOYMENT.md](./FRONTEND_DEPLOYMENT.md)
- **Build Summary**: [FRONTEND_SUMMARY.md](../FRONTEND_SUMMARY.md)
- **Backend Docs**: [../DEPLOYMENT_PLATFORMS.md](../DEPLOYMENT_PLATFORMS.md)
- **React Docs**: https://react.dev
- **TypeScript Docs**: https://www.typescriptlang.org/docs/

---

## 🎓 Learn More

### Inside the Frontend
- **API Integration**: `src/services/api.ts`
- **Authentication**: `src/services/auth.ts`
- **State Management**: `src/store/index.ts`
- **Components**: `src/components/`
- **Pages**: `src/pages/`

### Extending Features
- Add new API endpoints in `src/services/api.ts`
- Create new pages in `src/pages/`
- Add new components in `src/components/`
- Customize colors in `tailwind.config.js`

---

**Ready?** Run `npm run dev` and start building! 🚀

---

Created: January 2024  
React Dashboard v1.0.0 ✨
