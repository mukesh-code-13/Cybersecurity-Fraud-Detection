# 🚀 Vercel Deployment Quick Reference

## One-Command Deploy

```bash
# Make setup executable
chmod +x deploy/vercel-deploy.sh

# Run deploy script (interactive)
./deploy/vercel-deploy.sh
```

## Manual Deploy (Step-by-Step)

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy
```bash
vercel              # Deploy preview
vercel --prod       # Deploy production
```

### 4. Set Environment Variables
```bash
vercel env add DATABASE_URL
vercel env add REDIS_URL
vercel env add API_KEY
vercel env add JWT_SECRET
```

### 5. Redeploy with Variables
```bash
vercel --prod
```

---

## Required External Services

### Database (Choose One)
- **Supabase** - Free tier available
- **Neon** - Free tier available
- **AWS RDS** - Managed PostgreSQL
- **Azure Database** - Managed PostgreSQL

Get connection string → Set as `DATABASE_URL`

### Redis Cache (Choose One)
- **Vercel KV** - Integrated with Vercel
- **Upstash** - Free tier available
- **Redis Cloud** - Managed Redis

Get connection string → Set as `REDIS_URL`

---

## Environment Variables Required

```bash
DATABASE_URL=postgresql://user:pass@host:5432/fraud_detection_db
REDIS_URL=redis://default:pass@host:port
API_KEY=your-secure-key
JWT_SECRET=your-jwt-secret
DEBUG=False
LOG_LEVEL=INFO
```

---

## GitHub Deployment (Recommended)

1. Push code to GitHub:
   ```bash
   git add .
   git commit -m "Add Vercel deployment"
   git push origin main
   ```

2. Go to https://vercel.com/new

3. Select GitHub repository

4. Add Environment Variables

5. Click Deploy

6. Auto-deploys on every push!

---

## Verify Deployment

```bash
# Health check
curl https://your-project.vercel.app/api/v1/health

# Test API
curl -X POST https://your-project.vercel.app/api/v1/transactions/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","amount":100,"merchant":"Test","transaction_type":"purchase"}'

# View docs
open https://your-project.vercel.app/docs
```

---

## View Logs

```bash
# View deployment logs
vercel logs <project-url> --follow

# View via dashboard
# Go to: Vercel Dashboard → Project → Deployments → Logs
```

---

## Important Limitations

⚠️ **Timeout**: 30-60 seconds max  
⚠️ **Memory**: 3GB max  
⚠️ **File System**: Read-only except `/tmp`  
⚠️ **Cold Start**: ~5-10 seconds  

**ML Training**: Do this separately (not in serverless)

---

## Rollback to Previous Version

```bash
# View deployments
vercel list

# Rollback
vercel rollback

# Or via dashboard: Deployments → Click previous → Redeploy
```

---

## Custom Domain

1. Go to Vercel Dashboard
2. Project Settings → Domains
3. Add custom domain
4. Update DNS records (instructions provided)
5. Verify domain

---

## Monitoring

- **Vercel Dashboard**: Project → Monitoring
- **Real-time logs**: `vercel logs <url> --follow`
- **Error tracking**: Dashboard → Functions
- **Performance**: Dashboard → Analytics

---

## Cost

- **Vercel**: Free or $20+/month
- **Database**: $0-50/month
- **Redis**: $0-50/month
- **Total**: ~$0-100/month

---

## Detailed Guides

📖 **Full Deployment Guide**: [VERCEL_DEPLOY.md](../VERCEL_DEPLOY.md)  
📖 **Main Documentation**: [README.md](../README.md)  
📖 **Architecture**: [ARCHITECTURE.md](../ARCHITECTURE.md)  

---

## Troubleshooting

### Build Fails
```bash
# Check logs
vercel logs <url> --follow

# Common issues:
# - Wrong Python version (should be 3.11)
# - Missing dependencies in requirements.txt
# - Wrong directory structure
```

### Database Connection Error
```bash
# Check:
1. DATABASE_URL environment variable is set
2. Connection string is correct
3. Database is accessible
4. IP whitelist configured (if needed)
```

### Redis Connection Error
```bash
# Check:
1. REDIS_URL environment variable is set
2. Redis service is running/accessible
3. Network connectivity from Vercel
```

### Timeouts
```bash
# Solutions:
- Optimize database queries
- Use caching more aggressively
- Upgrade to Pro plan (+60s timeout)
- Move heavy work to background jobs
```

---

## Performance Tips

1. **Cache Everything**: Use Redis aggressively
2. **Optimize Queries**: Use database indices
3. **Lazy Load Models**: Load ML models on demand
4. **Enable Compression**: Gzip responses
5. **Monitor Cold Starts**: Use Vercel analytics

---

## Useful Commands

```bash
# Status
vercel status

# List deployments
vercel list

# Current config
vercel env list

# Remove deployment
vercel remove <project>

# Update project
vercel env pull      # Pull config locally

# Debug locally
vercel dev           # Run locally like production
```

---

**Ready to deploy! 🚀**

For issues: Check [VERCEL_DEPLOY.md](../VERCEL_DEPLOY.md) for detailed instructions.
