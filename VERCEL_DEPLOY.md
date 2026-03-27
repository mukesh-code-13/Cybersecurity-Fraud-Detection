# Vercel Deployment Guide - Cybersecurity Fraud Detection

## Prerequisites

1. **Vercel Account**: https://vercel.com
2. **GitHub Account**: Already set up (for git integration)
3. **External Services**:
   - PostgreSQL database (e.g., Supabase, AWS RDS, Neon)
   - Redis (e.g., Vercel KV, Redis Cloud, Upstash)

## Step 1: Prepare Repository for Vercel

Your repository already has `vercel.json` configured. The FastAPI app in `src/main.py` is set up to work with Vercel's Python runtime.

## Step 2: Set Up External Services

### Option A: Use Vercel KV (Recommended for Redis)
```bash
vercel env add REDIS_URL
# Enter your Vercel KV connection string
```

### Option B: Use Third-Party Services

#### PostgreSQL Database
Choose one:
- **Supabase** (https://supabase.com)
- **Neon** (https://neon.tech)
- **AWS RDS** (https://aws.amazon.com/rds/)
- **Azure Database** (https://azure.microsoft.com/services/postgresql/)

#### Redis Cache
Choose one:
- **Vercel KV** (https://vercel.com/storage/kv)
- **Upstash** (https://upstash.com)
- **Redis Cloud** (https://redis.com/cloud/)

## Step 3: Deploy to Vercel

### Method 1: Deploy from GitHub (Recommended)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com/new
   - Click "Import Git Repository"
   - Select your GitHub repository
   - Click "Import"

3. **Configure Environment Variables**
   - Click "Environment Variables"
   - Add the following:
     ```
     DATABASE_URL=postgresql://user:password@host:5432/fraud_detection_db
     REDIS_URL=redis://default:password@host:port
     API_KEY=your-secure-api-key
     JWT_SECRET=your-jwt-secret
     DEBUG=False
     LOG_LEVEL=INFO
     ```

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete

### Method 2: Deploy from CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Set environment variables
vercel env add DATABASE_URL
vercel env add REDIS_URL
vercel env add API_KEY
vercel env add JWT_SECRET

# Redeploy with environment variables
vercel --prod
```

## Step 4: Verify Deployment

Once deployed:

```bash
# Test health endpoint
curl https://your-project.vercel.app/api/v1/health

# Test transaction analysis
curl -X POST https://your-project.vercel.app/api/v1/transactions/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "amount": 100.0,
    "merchant": "TestMerchant",
    "transaction_type": "purchase"
  }'
```

## Important Considerations

### Limitations of Vercel Serverless

⚠️ **Function Timeout**: 30 seconds max for hobby plan, 60 seconds for pro
- ML model training should be done separately
- Long-running operations not suitable
- Use Vercel Cron Jobs for periodic tasks

⚠️ **Memory**: Limited to 3GB
- Models are loaded on each request
- Consider caching strategy

⚠️ **File System**: Read-only except `/tmp`
- Cannot persist models locally
- Use external storage for model files

### Recommended Architecture for Vercel

```
Vercel Functions (API)
    ↓
PostgreSQL (Supabase/Neon/RDS)
    ↓
Redis (Vercel KV/Upstash/Redis Cloud)
    ↓
External ML Training (Lambda/Cloud Functions)
```

## Database Setup for Vercel

### Using Supabase (Recommended)

1. **Create Account**: https://app.supabase.com
2. **Create Project**: Choose region
3. **Run SQL Script**:
   - Go to SQL Editor
   - Copy content from `deploy/init.sql`
   - Execute

4. **Get Connection String**:
   - Go to Settings → Database
   - Copy "URI" under Connection pooling (recommended)
   - Set as `DATABASE_URL` environment variable

### Using Neon

1. **Create Account**: https://neon.tech
2. **Create Project**
3. **Run Migrations**:
   ```bash
   psql $DATABASE_URL -f deploy/init.sql
   ```

## Redis Setup for Vercel

### Using Vercel KV (Easiest)

```bash
# Install Vercel Storage
vercel env add REDIS_URL

# This automatically creates a Vercel KV database
# Copy the connection string provided
```

### Using Upstash

1. **Create Account**: https://console.upstash.com
2. **Create Database**: Choose region
3. **Get Connection String**:
   - Copy Redis URL (Upstash Redis)
   - Set as `REDIS_URL` environment variable

## Setting Environment Variables

### Via Vercel Dashboard

1. Project Settings → Environment Variables
2. Add each variable
3. Redeploy for changes to take effect

### Via CLI

```bash
vercel env add DATABASE_URL
vercel env add REDIS_URL
vercel env add API_KEY
vercel env add JWT_SECRET
vercel env add DEBUG false
```

## Monitoring Deployment

### View Logs
```bash
vercel logs https://your-project.vercel.app
# or
vercel logs your-project --follow
```

### Monitor Performance
- Vercel Dashboard → Monitoring
- Check function execution times
- Monitor error rates
- View logs in real-time

## Enable Auto-Deploy

1. **Go to Project Settings** → Git
2. **Select "Deploy on push"**
3. **Choose Branch** (main)
4. **Deploy** automatically on each push

## Custom Domain (Optional)

1. **Go to Settings** → Domains
2. **Add Domain**
3. **Update DNS Records** (instructions provided)
4. **Verify Domain**

## Scaling Configuration

### For Production Use

```
Hobby Plan (Free):
- 5 deployments/day
- 100 Concurrent Invocations
- Not recommended for production

Pro Plan ($20/month):
- Unlimited deployments
- Better cold start performance
- Priority support

Enterprise Plan:
- Custom scaling
- Dedicated support
```

## Cost Estimation

### Vercel (API)
- **Hobby**: Free ($0)
- **Pro**: $20/month

### External Services
- **PostgreSQL**: $7-50/month (Supabase Starter)
- **Redis**: $0-50/month (Upstash free tier available)
- **Total**: ~$30-100/month for production setup

## Troubleshooting

### Deployment Failed
```bash
# Check build logs
vercel logs <project-url> --follow

# Common issues:
# 1. Python version mismatch - check runtime.txt
# 2. Missing dependencies - update requirements.txt
# 3. Environment variables not set
```

### Database Connection Error
```
Check:
1. DATABASE_URL environment variable is set
2. IP whitelist includes Vercel IPs (optional for Supabase)
3. Connection string format is correct
```

### Redis Connection Error
```
Check:
1. REDIS_URL environment variable is set
2. Redis service is running
3. Connection string includes correct port
```

### Timeout Errors
```
Solutions:
1. Optimize database queries
2. Add caching with Redis
3. Consider paid plan for longer timeouts
4. Move heavy operations to background tasks
```

## Advanced Configuration

### Using Runtime.txt
Create `runtime.txt`:
```
python-3.11
```

### Using .vercelignore
Create `.vercelignore`:
```
.git
.gitignore
*.md
tests/
scripts/
logs/
models/
data/
```

### Cron Jobs (Pro Plan)

Create `vercel.json` with cron:
```json
{
  "crons": [
    {
      "path": "/api/v1/models/retrain",
      "schedule": "0 2 * * *"
    }
  ]
}
```

## Next Steps

1. **Setup External Services**
   - PostgreSQL database
   - Redis cache

2. **Set Environment Variables**
   - Add all required vars to Vercel

3. **Deploy**
   ```bash
   vercel --prod
   ```

4. **Test Endpoints**
   - Use curl or Postman
   - Monitor logs

5. **Configure Custom Domain** (optional)

## Support & Resources

- **Vercel Docs**: https://vercel.com/docs
- **FastAPI on Vercel**: https://vercel.com/guides/fastapi
- **Database Options**: https://vercel.com/storage
- **Python Runtime**: https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python

## Production Checklist

- [ ] PostgreSQL database configured
- [ ] Redis cache configured
- [ ] Environment variables set
- [ ] Database schema initialized
- [ ] HTTPS/SSL enabled
- [ ] Custom domain configured
- [ ] Monitoring enabled
- [ ] Backup strategy configured
- [ ] Logging configured
- [ ] Rate limiting enabled

---

**Your Vercel deployment is now ready!** 🚀

Access your API at: `https://your-project.vercel.app`
