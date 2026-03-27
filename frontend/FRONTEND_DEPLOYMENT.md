# React Frontend - Deployment & Setup Guide

Complete guide for setting up and deploying the Fraud Detection React frontend with the FastAPI backend.

## 📋 Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Project Structure](#project-structure)
3. [Running Frontend](#running-frontend)
4. [Building for Production](#building-for-production)
5. [Deployment Platforms](#deployment-platforms)
6. [Environment Configuration](#environment-configuration)
7. [Troubleshooting](#troubleshooting)
8. [Docker Integration](#docker-integration)

---

## 🏠 Local Development Setup

### Prerequisites

- **Node.js**: v16.x or higher
- **npm**: v8.x or yarn v3.x
- **Backend**: FastAPI server running on port 8000

### Step-by-Step Setup

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

**Alternative with yarn:**
```bash
yarn install
```

#### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env.local

# Edit .env.local with your settings
nano .env.local
```

#### 3. Start Development Server

```bash
npm run dev
# or
yarn dev
```

**Output:**
```
  VITE v5.0.8  ready in 245 ms

  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

#### 4. Access the Dashboard

Open your browser: http://localhost:3000

**Demo Credentials:**
```
Username: demo_analyst
Password: demo123
```

---

## 📁 Project Structure

### Directory Organization

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── common/         # Reusable UI components
│   │   │   └── Card.tsx    # Button, Card, Alert, Badge
│   │   ├── Header.tsx      # Navigation bar
│   │   ├── Sidebar.tsx     # Left navigation
│   │   ├── ProtectedRoute.tsx
│   │   └── index.ts        # Barrel export
│   │
│   ├── pages/              # Page components
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Transactions.tsx
│   │   ├── Phishing.tsx
│   │   ├── Behavior.tsx
│   │   ├── Analytics.tsx
│   │   └── index.ts
│   │
│   ├── services/           # Business logic
│   │   ├── api.ts         # Axios instance & API calls
│   │   ├── auth.ts        # Authentication service
│   │   └── index.ts
│   │
│   ├── store/              # State management (Zustand)
│   │   └── index.ts
│   │
│   ├── types/              # TypeScript definitions
│   │   └── index.ts
│   │
│   ├── utils/              # Utility functions
│   │   └── helpers.ts
│   │
│   ├── App.tsx             # Main app with routing
│   ├── main.tsx            # React entry point
│   └── index.css           # Global styles
│
├── public/                 # Static assets
├── index.html             # HTML template
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript config
├── vite.config.ts         # Vite configuration
├── tailwind.config.js     # Tailwind CSS config
├── postcss.config.js      # PostCSS config
└── README.md
```

---

## 🚀 Running Frontend

### Development Mode

```bash
npm run dev
```

- Hot module replacement (HMM)
- File watching
- Browser auto-refresh
- Source maps for debugging
- Unminified code

**Access**: http://localhost:3000

### Production Build

```bash
npm run build
```

**Output:**
```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   ├── index-[hash].css
│   └── vendor-[hash].js
```

### Preview Production Build

```bash
npm run preview
```

Starts local server on http://localhost:4173 serving `dist/` folder

---

## 🏗️ Building for Production

### Build Process

```bash
# Install dependencies
npm install

# Build optimized production bundle
npm run build

# Output to dist/ directory
# - All code minified
# - CSS bundled
# - Assets optimized
# - Source maps (optional)
```

### Build Features

- **Code Splitting**: Automatic route-based splitting
- **Tree Shaking**: Unused code removed
- **CSS Minification**: Tailwind CSS optimized
- **Asset Minification**: JavaScript compressed
- **SourceMaps**: Disabled by default (enable in vite.config.ts)

### Build Optimization

```javascript
// vite.config.ts
export default defineConfig({
  build: {
    outDir: 'dist',
    sourcemap: false,      // Disable for smaller build
    minify: 'terser',      // JavaScript minification
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['react', 'react-dom', 'react-router-dom'],
        }
      }
    }
  },
})
```

---

## ☁️ Deployment Platforms

### Vercel (Recommended)

**Easiest deployment with GitHub integration**

#### Deploy with Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from frontend directory
cd frontend
vercel
```

#### Automatic GitHub Deployment

1. Push code to GitHub
2. Go to https://vercel.com/new
3. Select GitHub repository
4. Configure:
   - **Framework**: Vite
   - **Root Directory**: frontend
   - **Build Command**: `npm run build`
   - **Output Directory**: dist
5. Add environment variables:
   ```
   VITE_API_URL=https://your-backend.com
   ```
6. Deploy

**Result**: https://your-project.vercel.app

### Railway.app

**Full-stack deployments with database support**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd frontend
railway up
```

**Configuration on Railway Dashboard:**
- Build Command: `npm run build`
- Start Command: `npm run preview`
- Environment Variables: `VITE_API_URL`

### Render.com

**Simple deployment with good free tier**

1. Push code to GitHub
2. Go to https://dashboard.render.com
3. New → Static Site
4. Connect GitHub repository
5. Configure:
   - **Build Command**: `npm run build`
   - **Publish Directory**: dist
   - **Environment**: Add `VITE_API_URL`
6. Deploy

### Docker

**For containerized deployment**

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

**Build & Run:**
```bash
docker build -f frontend/Dockerfile -t fraud-detection-frontend .
docker run -p 3000:3000 -e VITE_API_URL=http://backend:8000 fraud-detection-frontend
```

### Docker Compose (Full Stack)

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://backend:8000
    depends_on:
      - backend

  backend:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/fraud_db
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: fraud_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

**Start all services:**
```bash
docker-compose up -d
```

---

## 🔧 Environment Configuration

### Development Environment

**`.env.local`**:
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Fraud Detection Dashboard
```

### Production Environment

**Vercel (via Dashboard)**:
- Go to Settings → Environment Variables
- Add:
  ```
  VITE_API_URL=https://api.yourdomain.com
  VITE_APP_NAME=Fraud Detection Dashboard
  ```

**Railway**:
- Go to Variables → Add Variable
- Key: `VITE_API_URL`
- Value: `https://api.yourdomain.com`

**Docker**:
```bash
docker run -p 3000:3000 \
  -e VITE_API_URL=https://api.yourdomain.com \
  fraud-detection-frontend
```

### Build-Time vs Runtime

Variables prefixed with `VITE_` are baked into the build. To change them without rebuilding, use a runtime config file approach.

---

## 🔌 API Integration

### Configuring Backend URL

The frontend expects backend at `VITE_API_URL`:

```typescript
// src/services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

### API Endpoints

```
GET    /api/v1/health                 ← Keep-alive check
GET    /api/v1/models/status          ← Model status
GET    /api/v1/alerts/risk-summary    ← Overall risk
POST   /api/v1/transactions/analyze   ← Fraud analysis
POST   /api/v1/phishing/detect        ← Email analysis
POST   /api/v1/behavior/analyze       ← Behavior detection
POST   /api/v1/models/update-baseline ← Update user baseline
```

### Testing API Connection

```bash
curl -X GET http://your-backend.com/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "models_loaded": {
    "anomaly_detector": true,
    "fraud_detector": true,
    "phishing_detector": true,
    "behavioral_analyzer": true
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## 📊 Performance Optimization

### Build Size Optimization

Original: ~250KB
After optimization:
- Critical CSS: Extracted
- Unused CSS: Removed
- Code split: 3 main chunks
- Gzip: ~85KB

### Lazy Loading Routes

Already implemented in `App.tsx`:
```typescript
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Transactions = lazy(() => import('./pages/Transactions'))
```

### Caching Strategy

- **HTML**: Cache-Control: max-age=0
- **JS/CSS**: Cache-Control: max-age=31536000 (1 year)
- **Assets**: Cache-Control: max-age=31536000

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: "Cannot find module errors"

**Solution:**
```bash
# Clear node_modules
rm -rf node_modules
rm package-lock.json

# Reinstall
npm install
```

#### Issue: "API not responding"

**Checklist:**
- ✅ Backend running on correct port?
- ✅ VITE_API_URL correct?
- ✅ CORS enabled on backend?
- ✅ No firewall blocking?

**Debug:**
```bash
curl -I http://localhost:8000/api/v1/health
```

#### Issue: "Build fails with CSS error"

**Solution:**
```bash
npm run build -- --debug
```

Check for Tailwind config issues in `tailwind.config.js`

#### Issue: "Page goes blank after deploy"

**Causes:**
- Wrong API URL
- Missing environment variables
- Router misconfiguration

**Verify:**
```javascript
// Check in browser console
console.log('API URL:', import.meta.env.VITE_API_URL)
```

---

## 🧪 Testing

### Run Tests

```bash
npm run test
```

### Test with Different Backends

```bash
# Against local backend
VITE_API_URL=http://localhost:8000 npm run dev

# Against staging backend
VITE_API_URL=https://staging-api.com npm run dev

# Against production backend
VITE_API_URL=https://api.yourdomain.com npm run build
```

---

## 📈 Monitoring & Debugging

### Performance Monitoring

```bash
# Build analysis
npm run build -- --analyze
```

### Network Debugging

Use browser DevTools:
- Network tab: Check API response times
- Console: Check for errors
- Performance: Measure page load

### Error Tracking

Add error boundary:
```typescript
import ErrorBoundary from './components/ErrorBoundary'

<ErrorBoundary>
  <App />
</ErrorBoundary>
```

---

## 🚀 Deployment Checklist

- [ ] Dependencies installed: `npm install`
- [ ] Environment configured: `.env.local` created
- [ ] Backend running: Verify `/api/v1/health`
- [ ] Local test: `npm run dev` works
- [ ] Build succeeds: `npm run build`
- [ ] No console errors: Check DevTools
- [ ] API endpoints working: Test in Postman
- [ ] CORS configured: On backend
- [ ] SSL certificate: If HTTPS
- [ ] Domain configured: If custom domain
- [ ] Environment variables: Set in platform
- [ ] Build command configured: In platform
- [ ] Start command configured: In platform

---

## 📚 Additional Resources

- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [React Router](https://reactrouter.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

**Last Updated**: January 2024  
**Version**: 1.0.0
