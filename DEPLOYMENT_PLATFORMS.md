# 🚀 Multi-Platform Deployment Guide with Ports & Links

Complete deployment options for Cybersecurity Fraud Detection System across multiple platforms with configured ports and access links.

---

## 📋 Deployment Platforms Overview

| Platform | Port | Link Format | Cost | Difficulty |
|----------|------|------------|------|-----------|
| **Vercel** | 443 (HTTPS) | `https://project.vercel.app` | $0-20/mo | ⭐ Easy |
| **Railway** | 443 (HTTPS) | `https://project.railway.app` | $5-50/mo | ⭐⭐ Medium |
| **Render** | 443 (HTTPS) | `https://project.onrender.com` | $7-50/mo | ⭐⭐ Medium |
| **Heroku** | 443 (HTTPS) | `https://project.herokuapp.com` | $50+/mo | ⭐⭐ Medium |
| **PythonAnywhere** | 443 (HTTPS) | `https://username.pythonanywhere.com` | $5-50/mo | ⭐⭐ Medium |
| **AWS Elastic Beanstalk** | 80/443 | `project.elasticbeanstalk.com` | $5-50+/mo | ⭐⭐⭐ Hard |
| **Google Cloud Run** | 8080 | `project.run.app` | $0-50/mo | ⭐⭐⭐ Hard |
| **Azure App Service** | 443 | `project.azurewebsites.net` | $10-50+/mo | ⭐⭐⭐ Hard |
| **Docker Locally** | 8000 | `http://localhost:8000` | $0 | ⭐ Easy |
| **Ports.io** | 3000+ | `https://ports-project.id.direct` | Free | ⭐⭐ Medium |

---

## 🐳 Local Docker (Development)

### Port Configuration
- **API**: `http://localhost:8000`
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000`

### Deploy Locally
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api

# Access endpoints
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/docs
```

### Custom Port Configuration
Edit `docker-compose.yml`:
```yaml
api:
  ports:
    - "9000:8000"  # External:Internal
  environment:
    - API_PORT=8000

prometheus:
  ports:
    - "9091:9090"

grafana:
  ports:
    - "3001:3000"
```

---

## ✨ Vercel (Recommended - Easiest)

### Access Links
```
API:          https://your-project.vercel.app
Docs:         https://your-project.vercel.app/docs
ReDoc:        https://your-project.vercel.app/redoc
Health:       https://your-project.vercel.app/api/v1/health
```

### Deploy
```bash
# 1. Setup services (PostgreSQL + Redis)
# 2. GitHub integration or CLI
vercel --prod

# 3. Add environment variables
vercel env add DATABASE_URL
vercel env add REDIS_URL
```

### Auto-Deploy from GitHub
1. Go to https://vercel.com/new
2. Import repository
3. Add environment variables
4. Deploy
5. Auto-redeploys on every push

---

## 🚂 Railway.app (Great Alternative)

### Access Links
```
https://your-project-name-XXXXX.railway.app
Port: 443 (auto-managed)
```

### Deploy Steps
```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Link to repo
railway link

# 4. Add services
railway service add postgresql
railway service add redis

# 5. Deploy
railway up
```

### Configuration
Edit `railway.toml`:
```toml
[build]
builder = "dockerfile"

[deploy]
startCommand = "uvicorn src.main:app --host 0.0.0.0 --port 8080"
pollTimeout = 3m
```

### GitHub Integration
```bash
# Connect repo for auto-deploy
railway connect github
railway service new
```

---

## 🎨 Render.com (Easy & Reliable)

### Access Links
```
https://your-project-name.onrender.com
Port: 443 (auto-managed)
```

### Deploy Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **Create `render.yaml`**:
   ```yaml
   services:
     - type: web
       name: fraud-detection-api
       env: python
       plan: free
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn src.main:app --host 0.0.0.0 --port 8080
       envVars:
         - key: DATABASE_URL
           fromDatabase:
             name: postgres
             property: connectionString
         - key: REDIS_URL
           fromService:
             name: redis
             property: connectionString
     
     - type: pserv
       name: postgres
       env: docker
       plan: free
       image: postgres:15
       
     - type: redis
       name: redis
       plan: free
   ```

3. **Go to https://dashboard.render.com**
4. **Click "New+"** → "Blueprint"
5. **Connect GitHub repo**
6. **Deploy**

---

## 🟣 Ports.io (Quick Free Hosting)

### Access Links
```
https://ports-[project-hash].id.direct
Port: 443 (auto-managed)
```

### Deploy Steps

```bash
# 1. Install Ports CLI
npm install @ports.dev/cli -g

# 2. Create ports.yml
cat > ports.yml << EOF
version: 1
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - 8000
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
EOF

# 3. Deploy
ports deploy

# 4. Get your link
ports info
```

### Link Format
```
https://ports-[random-hash].id.direct
```

---

## 📦 Heroku (Larger Projects)

### Access Links
```
https://project-name.herokuapp.com
Port: 443 (auto-managed)
```

### Deploy Steps

```bash
# 1. Install Heroku CLI
npm install -g heroku

# 2. Login
heroku login

# 3. Create app
heroku create your-app-name

# 4. Create `Procfile`
echo "web: uvicorn src.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 5. Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 6. Add Redis
heroku addons:create heroku-redis:premium-0

# 7. Deploy
git push heroku main

# 8. View logs
heroku logs --tail
```

### Environment Variables
```bash
heroku config:set DATABASE_URL="postgresql://..."
heroku config:set REDIS_URL="redis://..."
heroku config:set API_KEY="your-key"
```

---

## ☁️ AWS Elastic Beanstalk

### Access Links
```
http://fraud-detection-api.us-east-1.elasticbeanstalk.com
Port: 80/443
```

### Deploy Steps

```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Initialize
eb init -p "python-3.11" fraud-detection --region us-east-1

# 3. Create environment
eb create fraud-detection-env

# 4. Deploy
eb deploy

# 5. Open
eb open
```

### Configuration (``.ebextensions/python.config``)
```yaml
option_settings:
  aws:autoscaling:launchconfiguration:
    InstanceType: t3.small
  aws:elasticbeanstalk:application:environment:
    PYTHONUNBUFFERED: 1
    DATABASE_URL: <your-db-url>
    REDIS_URL: <your-redis-url>
```

---

## 🔵 Google Cloud Run

### Access Links
```
https://fraud-detection-XXXXX-REGION.a.run.app
Port: 8080
```

### Deploy Steps

```bash
# 1. Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# 2. Initialize
gcloud init
gcloud config set project YOUR_PROJECT_ID

# 3. Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/fraud-detection

# 4. Deploy
gcloud run deploy fraud-detection \
  --image gcr.io/YOUR_PROJECT_ID/fraud-detection \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=<url>,REDIS_URL=<url>

# 5. Get URL
gcloud run services describe fraud-detection --platform managed --region us-central1
```

### Update `src/main.py` for Cloud Run
```python
import os
port = int(os.environ.get("PORT", 8080))
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## 🔷 Azure App Service

### Access Links
```
https://fraud-detection-api.azurewebsites.net
Port: 443
```

### Deploy Steps

```bash
# 1. Install Azure CLI
curl https://aka.ms/install-azure-cli | bash

# 2. Login
az login

# 3. Create resource group
az group create --name fraud-detection-rg --location eastus

# 4. Create app service plan
az appservice plan create \
  --name fraud-detection-plan \
  --resource-group fraud-detection-rg \
  --sku B1

# 5. Create web app
az webapp create \
  --resource-group fraud-detection-rg \
  --plan fraud-detection-plan \
  --name fraud-detection-api \
  --runtime "PYTHON:3.11"

# 6. Deploy
az webapp deployment source config-zip \
  --resource-group fraud-detection-rg \
  --name fraud-detection-api \
  --src app.zip
```

---

## 🐍 PythonAnywhere

### Access Links
```
https://username.pythonanywhere.com
Port: 443
```

### Deploy Steps

1. **Create Account**: https://www.pythonanywhere.com
2. **Upload Code**:
   ```bash
   scp -r . username@ssh.pythonanywhere.com:mysite
   ```

3. **Configure WSGI**:
   ```python
   import os
   import sys
   
   path = os.path.expanduser('~/mysite')
   if path not in sys.path:
       sys.path.insert(0, path)
   
   from src.main import app as application
   ```

4. **Reload Web App**

---

## 📊 Port Mapping Summary

```
┌─────────────────────────────────────────────────┐
│           Service Port Mapping                  │
├────────────────────────┬────────────────────────┤
│ Local Docker           │ 8000 (API)             │
│                        │ 5432 (DB)              │
│                        │ 6379 (Redis)           │
│                        │ 9090 (Prometheus)      │
│                        │ 3000 (Grafana)         │
├────────────────────────┼────────────────────────┤
│ Vercel                 │ 443 (auto)             │
│ Railway                │ 443 (auto)             │
│ Render                 │ 443 (auto)             │
│ Heroku                 │ 443 (auto)             │
│ PythonAnywhere         │ 443 (auto)             │
├────────────────────────┼────────────────────────┤
│ Google Cloud Run       │ 8080 (configured)      │
│ AWS EB                 │ 80/443 (configurable)  │
│ Azure App Service      │ 443 (auto)             │
├────────────────────────┼────────────────────────┤
│ Ports.io               │ 443 (auto)             │
└────────────────────────┴────────────────────────┘
```

---

## 🔗 Complete Access Link Examples

### Development (Local)
```
API:          http://localhost:8000
Docs:         http://localhost:8000/docs
Prometheus:   http://localhost:9090
Grafana:      http://localhost:3000
Database:     localhost:5432
Cache:        localhost:6379
```

### Production (Vercel)
```
API:          https://fraud-detection-api.vercel.app
Docs:         https://fraud-detection-api.vercel.app/docs
ReDoc:        https://fraud-detection-api.vercel.app/redoc
Custom:       https://fraud-detection.yourdomain.com (optional)
```

### Production (Railway)
```
API:          https://fraud-detection-production.railway.app
Docs:         https://fraud-detection-production.railway.app/docs
Database:     Managed by Railway
Redis:        Managed by Railway
```

### Production (Render)
```
API:          https://fraud-detection-api.onrender.com
Docs:         https://fraud-detection-api.onrender.com/docs
Database:     Managed by Render
Redis:        Managed by Render
```

### Production (Google Cloud Run)
```
API:          https://fraud-detection-xyz.us-central1.a.run.app
Docs:         https://fraud-detection-xyz.us-central1.a.run.app/docs
Port:         8080 (internal)
```

---

## 🎯 Quick Deploy Comparison

| Platform | Setup Time | Cost/Month | Ease | Best For |
|----------|-----------|-----------|------|----------|
| **Docker Local** | 5 min | $0 | ⭐⭐⭐⭐⭐ | Development |
| **Vercel** | 10 min | $0-20 | ⭐⭐⭐⭐⭐ | Serverless |
| **Railway** | 15 min | $5-50 | ⭐⭐⭐⭐ | Full Stack |
| **Render** | 15 min | $7-50 | ⭐⭐⭐⭐ | Full Stack |
| **Heroku** | 20 min | $50+ | ⭐⭐⭐ | Legacy |
| **Google Cloud** | 30 min | $0-50 | ⭐⭐⭐ | Enterprise |
| **AWS EB** | 30 min | $5-50+ | ⭐⭐ | Enterprise |
| **Azure** | 30 min | $10-50+ | ⭐⭐ | Enterprise |

---

## 📝 Custom Port Configuration

### Change Local Ports

Edit `docker-compose.yml`:
```yaml
api:
  ports:
    - "9000:8000"        # Access on 9000

db:
  ports:
    - "5433:5432"        # Access on 5433

redis:
  ports:
    - "6380:6379"        # Access on 6380

prometheus:
  ports:
    - "9091:9090"

grafana:
  ports:
    - "3001:3000"
```

Access:
```
API:       http://localhost:9000
DB:        localhost:5433
Redis:     localhost:6380
Prometheus: http://localhost:9091
Grafana:   http://localhost:3001
```

### Change API Port

Edit `src/main.py`:
```python
if __name__ == "__main__":
    import os
    port = int(os.environ.get("API_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

Or via environment:
```bash
export API_PORT=9000
python -m uvicorn src.main:app --port 9000
```

---

## 🌐 Domain Configuration

### Vercel Custom Domain
1. Project Settings → Domains
2. Add domain
3. Update DNS records
4. Access: `https://yourdomain.com`

### Railway Custom Domain
```bash
railway domain add yourdomain.com
```

### Render Custom Domain
1. Dashboard → Service
2. Settings → Custom Domain
3. Add domain
4. Update DNS CNAME

### Others
Similar process - add DNS CNAME pointing to platform

---

## 🚀 Recommended Deploy Path

### For Development
```bash
docker-compose up -d
# Access: http://localhost:8000
```

### For Quick MVP
```bash
# Use Vercel + GitHub
git push && deploy via vercel.com/new
# Access: https://project.vercel.app
```

### For Production
```bash
# Use Railway or Render
# Full-managed database/cache
# Better control than Vercel
# Access: https://project.railway.app
```

### For Large Scale
```bash
# Use Google Cloud Run or AWS EB
# More scalability
# Enterprise features
# Access: https://project.a.run.app
```

---

## 📞 Where to Deploy

**Choose Based on:**
- 🎯 **Speed**: Vercel (fastest setup)
- 💰 **Cost**: Docker local (free) or Vercel (free tier)
- 🛠️ **Control**: Railway or Render (best balance)
- 📈 **Scale**: Google Cloud Run or AWS
- 🆓 **Free**: Vercel, Docker local, Render (limited free tier)

---

## ✅ Deployment Checklist

- [ ] Choose platform
- [ ] Setup external services (DB + Cache)
- [ ] Configure environment variables
- [ ] Test locally: `docker-compose up`
- [ ] Push to GitHub
- [ ] Deploy to platform
- [ ] Test endpoints
- [ ] Configure custom domain (optional)
- [ ] Setup monitoring
- [ ] Configure backups

---

**Ready to deploy!** Choose your platform above and follow the deploy steps. 🚀
