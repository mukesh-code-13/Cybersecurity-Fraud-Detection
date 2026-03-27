# 🔗 Deployment Links & Ports - Quick Reference

**All ports and links for deploying your Fraud Detection System**

---

## 🏠 Local Development (Docker)

```
API:          http://localhost:8000
Docs:         http://localhost:8000/docs
ReDoc:        http://localhost:8000/redoc
Prometheus:   http://localhost:9090
Grafana:      http://localhost:3000 (admin/admin)
Database:     localhost:5432
Redis:        localhost:6379
```

**Start:**
```bash
docker-compose up -d
```

---

## ☁️ Cloud Deployment Platforms

### **Vercel** (⭐ Recommended - Easiest)
```
🌐 https://your-project.vercel.app
📖 https://your-project.vercel.app/docs
🔗 https://vercel.com/new
💰 Free to $20/month
⏱️ Setup: 10 minutes
```

### **Railway** (Great Alternative)
```
🌐 https://your-project-XXXXX.railway.app
📖 https://your-project-XXXXX.railway.app/docs
🔗 https://railway.app
💰 $5-50/month
⏱️ Setup: 15 minutes
```

### **Render** (Easy & Reliable)
```
🌐 https://your-project-name.onrender.com
📖 https://your-project-name.onrender.com/docs
🔗 https://render.com
💰 $7-50/month
⏱️ Setup: 15 minutes
```

### **Ports.io** (Quick Free Hosting)
```
🌐 https://ports-[hash].id.direct
📖 https://ports-[hash].id.direct/docs
🔗 https://ports.dev
💰 Free
⏱️ Setup: 5 minutes
```

### **Heroku** (Legacy - Paid)
```
🌐 https://your-app.herokuapp.com
📖 https://your-app.herokuapp.com/docs
🔗 https://heroku.com
💰 $50+/month
⏱️ Setup: 20 minutes
```

### **PythonAnywhere** (Easy Python Hosting)
```
🌐 https://username.pythonanywhere.com
📖 https://username.pythonanywhere.com/docs
🔗 https://pythonanywhere.com
💰 $5-50/month
⏱️ Setup: 15 minutes
```

### **Google Cloud Run** (Scalable)
```
🌐 https://fraud-detection-XXXXX-[REGION].a.run.app
📖 https://fraud-detection-XXXXX-[REGION].a.run.app/docs
🔗 https://cloud.google.com/run
💰 $0-50/month
⏱️ Setup: 30 minutes
Port: 8080
```

### **AWS Elastic Beanstalk** (Enterprise)
```
🌐 http://app-name.[REGION].elasticbeanstalk.com
📖 http://app-name.[REGION].elasticbeanstalk.com/docs
🔗 https://aws.amazon.com/elasticbeanstalk/
💰 $5-50+/month
⏱️ Setup: 30 minutes
Port: 80/443
```

### **Azure App Service** (Enterprise)
```
🌐 https://app-name.azurewebsites.net
📖 https://app-name.azurewebsites.net/docs
🔗 https://azure.microsoft.com/
💰 $10-50+/month
⏱️ Setup: 30 minutes
Port: 443
```

---

## 🎯 Port Mapping by Platform

| Platform | Port | Internal | Notes |
|----------|------|----------|-------|
| Local Docker | 8000 | 8000 | Development |
| Vercel | 443 | Auto | HTTPS only |
| Railway | 443 | Auto | HTTPS only |
| Render | 443 | Auto | HTTPS only |
| Ports.io | 443 | Auto | HTTPS only |
| Heroku | 443 | Auto | HTTPS only |
| PythonAnywhere | 443 | Auto | HTTPS only |
| Google Cloud Run | 8080 | 8080 | Custom port |
| AWS EB | 80/443 | 80/443 | Configurable |
| Azure | 443 | 443 | HTTPS only |

---

## 📊 Platform Comparison Matrix

| Feature | Vercel | Railway | Render | Heroku | GCP Run | AWS EB |
|---------|--------|---------|--------|--------|---------|--------|
| Ease | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Cost | Free | $5+ | $7+ | $50+ | Free | $5+ |
| Setup | 10 min | 15 min | 15 min | 20 min | 30 min | 30 min |
| Free Tier | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| GitHub Auto | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Custom Domain | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Database | External | Managed | Managed | Add-on | External | RDS |
| Cache | External | Managed | Managed | Add-on | External | ElastiCache |

---

## 🚀 3-Step Deploy Guide for Each Platform

### **Vercel (Easiest)**
```bash
# 1. Push to GitHub
git add . && git commit -m "Deploy" && git push

# 2. Go to https://vercel.com/new
# 3. Import repository and deploy

# Access: https://your-project.vercel.app
```

### **Railway**
```bash
# 1. Go to https://railway.app
# 2. Connect GitHub repository
# 3. Add PostgreSQL and Redis services

# Access: https://your-project.railway.app
```

### **Render**
```bash
# 1. Go to https://dashboard.render.com
# 2. New Web Service → Connect GitHub
# 3. Configure and deploy

# Access: https://your-project.onrender.com
```

### **Ports.io**
```bash
# 1. npm install @ports.dev/cli -g
# 2. ports deploy
# 3. Copy link from ports info

# Access: https://ports-[hash].id.direct
```

---

## 🔌 API Endpoints by Platform

All platforms provide these endpoints:

```
GET    /                              # Root info
GET    /api/v1/health                 # Health check
GET    /api/v1/info                   # API info
GET    /api/v1/models/status          # Model status
POST   /api/v1/transactions/analyze   # Analyze transaction
POST   /api/v1/phishing/detect        # Detect phishing
POST   /api/v1/behavior/analyze       # Analyze behavior
GET    /docs                          # Swagger UI
GET    /redoc                         # ReDoc
```

**Example calls:**
```bash
# Health check
curl https://your-platform.com/api/v1/health

# Analyze transaction
curl -X POST https://your-platform.com/api/v1/transactions/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user1","amount":100,"merchant":"Test","transaction_type":"purchase"}'

# View API docs
open https://your-platform.com/docs
```

---

## 💾 External Services Needed

Each platform needs external services (not built-in):

| Service | Platform |
|---------|----------|
| **PostgreSQL** | Vercel, Ports.io, GCP Run, AWS |
| **Redis** | Vercel, Ports.io, GCP Run, AWS |
| **Managed DB** | Railway, Render, Heroku, Azure |

**Recommended:**
- **Database**: Supabase (free) or Neon (free)
- **Cache**: Vercel KV (included) or Upstash (free)

---

## 🎯 Quick Decision Guide

**Choose based on:**

🟢 **Want easiest?** → **Vercel**
```
git push → vercel.com → Done ✅
Link: https://project.vercel.app
```

🟢 **Want best value?** → **Railway**
```
Connect repo → Deploy ✅
Link: https://project.railway.app
Includes DB + Cache
```

🟢 **Want free?** → **Ports.io or Docker Local**
```
ports deploy ✅
Link: https://ports-[hash].id.direct
```

🟢 **Want enterprise?** → **Google Cloud Run or AWS**
```
More complex setup but powerful
Link: https://project.a.run.app
```

---

## 🔐 Environment Variables

Every platform needs these variables set:

```env
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://default:pass@host:port
API_KEY=your-secure-key
JWT_SECRET=your-secret
DEBUG=False
LOG_LEVEL=INFO
```

---

## 📈 Scaling Options

| Platform | Auto-Scale | Max Instances | CPU/Memory |
|----------|-----------|---------------|-----------|
| Vercel | Yes | Unlimited | 3GB |
| Railway | Yes | 50+ | 2GB |
| Render | Yes | Unlimited | 4GB |
| Heroku | Manual | Unlimited | 1GB+ |
| Google Cloud | Yes | Unlimited | Custom |
| AWS EB | Yes | Unlimited | Custom |

---

## 💳 Cost Breakdown

### **Free Tier** (Best for MVP)
```
Vercel          : Free
PostgreSQL      : Supabase free (~5GB)
Redis           : Vercel KV free tier
Total           : $0/month
```

### **Budget** ($20-30/month)
```
Vercel          : $20
PostgreSQL      : Supabase free
Redis           : Free tier
Total           : $20/month
```

### **Production** ($50-100/month)
```
Railway/Render  : $30-50
PostgreSQL      : $15-20
Redis           : $10-20
Total           : $55-90/month
```

---

## 🛠️ Custom Domain Setup

After deploying, add custom domain:

1. **Get domain** (GoDaddy, Namecheap, CloudFlare)
2. **Update DNS CNAME** to platform URL
3. **Verify domain** in platform dashboard
4. **Access**: `https://yourdomain.com`

Example:
```
yourdomain.com → CNAME → your-project.vercel.app
```

---

## 📞 Platform Support & Docs

| Platform | Docs | Status Page | Support |
|----------|------|-------------|---------|
| Vercel | https://vercel.com/docs | status.vercel.com | Community |
| Railway | https://railway.app/docs | xn--7gq.app | Email |
| Render | https://render.com/docs | status.render.com | Chat/Email |
| Heroku | https://devcenter.heroku.com | status.heroku.com | Email |
| GCP Run | https://cloud.google.com/run/docs | status.cloud.google.com | Chat |
| AWS EB | https://docs.aws.amazon.com/elasticbeanstalk/ | health.aws.amazon.com | Phone/Chat |

---

## ✅ Pre-Deployment Checklist

- [ ] Code committed to GitHub
- [ ] `.env` variables documented
- [ ] Database service selected
- [ ] Redis service selected
- [ ] README updated
- [ ] Tests passing locally
- [ ] Docker builds successfully
- [ ] API health check working
- [ ] Environment variables ready
- [ ] Choose deployment platform

---

## 🎬 Next Steps

1. **Choose Platform** (Vercel recommended for ease)
2. **Setup External Services** (Database + Redis)
3. **Deploy** (click deploy or push to GitHub)
4. **Get Link** from platform dashboard
5. **Test** endpoints at your link
6. **Configure Domain** (optional)
7. **Monitor** with platform tools

---

## 🚀 Start Deploying

Pick your platform and follow the guide:

📘 **[DEPLOYMENT_PLATFORMS.md](DEPLOYMENT_PLATFORMS.md)** - Full detailed guide  
📘 **[VERCEL_DEPLOY.md](VERCEL_DEPLOY.md)** - Vercel specific  
📘 **[VERCEL_QUICK_START.md](VERCEL_QUICK_START.md)** - Quick Vercel reference  

**Your system is ready for any platform!** 🎉
