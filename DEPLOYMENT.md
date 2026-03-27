# Deployment Guide - Cybersecurity Fraud Detection System

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Configuration](#configuration)
6. [Monitoring & Logging](#monitoring--logging)
7. [Model Training](#model-training)
8. [Scaling](#scaling)

## Prerequisites

### Required Software
- Python 3.11+
- Docker 20.10+
- Docker Compose 1.29+
- PostgreSQL 12+ (for local development)
- Redis 5+ (for caching)
- Git

### System Requirements
- **CPU**: 4 cores minimum
- **RAM**: 8GB minimum
- **Storage**: 20GB minimum
- **Network**: Outbound HTTPS access for model updates

### Port Requirements
- **8000**: Main API
- **5432**: PostgreSQL
- **6379**: Redis
- **9090**: Prometheus
- **3000**: Grafana

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/mukesh-code-13/Cybersecurity-Fraud-Detection.git
cd Cybersecurity-Fraud-Detection
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Setup PostgreSQL (Local Development)
```bash
# Create database
createdb fraud_detection_db
createuser fraud_user --encrypted -P

# Run migrations
psql fraud_detection_db -U fraud_user -f deploy/init.sql
```

### 6. Setup Redis (Local Development)
```bash
# Using Docker
docker run -d -p 6379:6379 redis:7-alpine

# Or using package manager
# macOS: brew install redis
# Ubuntu: sudo apt-get install redis-server
```

### 7. Start Development Server
```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API documentation at: http://localhost:8000/docs

## Docker Deployment

### Quick Start
```bash
# Make setup script executable
chmod +x deploy/setup.sh

# Run setup
./deploy/setup.sh
```

### Manual Docker Setup

#### Build Images
```bash
docker-compose build
```

#### Start Services
```bash
docker-compose up -d
```

#### Check Status
```bash
docker-compose ps
docker-compose logs -f api
```

#### Stop Services
```bash
docker-compose down
```

#### Stop and Remove Data
```bash
docker-compose down -v
```

### Access Services
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432
- **Redis**: localhost:6379
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

### Docker Troubleshooting
```bash
# View logs
docker-compose logs api

# Rebuild specific service
docker-compose build --no-cache api

# Reset everything
docker-compose down -v
docker-compose up -d

# Check resource usage
docker stats
```

## Kubernetes Deployment

### Prerequisites
```bash
kubectl version --client
kubectl cluster-info
```

### Deploy to Kubernetes

#### 1. Create Namespace
```bash
kubectl create namespace fraud-detection
```

#### 2. Create Secrets
```bash
kubectl create secret generic fraud-detection-secrets \
  --from-literal=db-password=fraud_pass \
  --from-literal=api-key=your-secure-key \
  -n fraud-detection
```

#### 3. Create ConfigMap
```bash
kubectl create configmap fraud-detection-config \
  --from-file=config/phishing_keywords.txt \
  --from-file=config/spam_keywords.txt \
  -n fraud-detection
```

#### 4. Deploy Services
```bash
kubectl apply -f deploy/k8s/postgres-deployment.yaml
kubectl apply -f deploy/k8s/redis-deployment.yaml
kubectl apply -f deploy/k8s/api-deployment.yaml
kubectl apply -f deploy/k8s/ingress.yaml
```

#### 5. Verify Deployment
```bash
kubectl get all -n fraud-detection
kubectl logs -f deployment/api -n fraud-detection
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_HOST` | 0.0.0.0 | API listening address |
| `API_PORT` | 8000 | API listening port |
| `DATABASE_URL` | PostgreSQL URL | Database connection string |
| `REDIS_URL` | redis://localhost | Redis connection URL |
| `ANOMALY_THRESHOLD` | 0.7 | Anomaly detection threshold |
| `PHISHING_THRESHOLD` | 0.75 | Phishing detection threshold |
| `FRAUD_THRESHOLD` | 0.8 | Fraud detection threshold |
| `DEBUG` | False | Debug mode |
| `LOG_LEVEL` | INFO | Logging level |

### Model Configuration

Edit `config/settings.py`:
```python
# Thresholds
ANOMALY_THRESHOLD = 0.7
PHISHING_THRESHOLD = 0.75
FRAUD_THRESHOLD = 0.8

# Model paths
MODELS_PATH = "models/"

# Features
ENABLE_ANOMALY_DETECTION = True
ENABLE_PHISHING_DETECTION = True
ENABLE_FRAUD_DETECTION = True
ENABLE_BEHAVIORAL_ANALYSIS = True
```

## Monitoring & Logging

### View Logs

#### Docker
```bash
docker-compose logs api
docker-compose logs -f --tail=100 api
```

#### Kubernetes
```bash
kubectl logs -f deployment/api -n fraud-detection
```

#### Local
```bash
tail -f logs/fraud_detection.log
```

### Prometheus Metrics

Access at: http://localhost:9090

#### Common Metrics
```
# API Response Time
histogram_quantile(0.95, request_duration_seconds)

# Error Rate
rate(http_requests_total{status=~"5.."}[5m])

# Active Connections
connections_active
```

### Grafana Dashboards

1. Access Grafana: http://localhost:3000
2. Default login: admin/admin
3. Add Prometheus data source
4. Import dashboard templates:
   - Fraud Detection Overview
   - ML Model Performance
   - System Health

## Model Training

### Update Models with Production Data

```bash
# Using training script
python scripts/train_models.py \
  --data data/training_data/transactions.csv \
  --anomaly-model models/isolation_forest.pkl \
  --fraud-model models/fraud_detector.pkl
```

### Model Evaluation

```bash
python scripts/evaluate_models.py \
  --test-data data/test_data/transactions.csv \
  --model models/fraud_detector.pkl
```

### Retrain with New Data

```bash
# Set to production
export MODEL_UPDATE_INTERVAL=86400  # 24 hours

# Models will auto-update based on schedule
```

## Scaling

### Horizontal Scaling (Docker Swarm)

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml fraud-detection

# Scale API service
docker service scale fraud-detection_api=3
```

### Horizontal Scaling (Kubernetes)

```bash
# Scale API deployment
kubectl scale deployment/api --replicas=3 -n fraud-detection

# Auto-scaling
kubectl autoscale deployment api \
  --min=2 --max=10 \
  --cpu-percent=70 \
  -n fraud-detection
```

### Load Balancing

Configure load balancer in `deploy/k8s/ingress.yaml`:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fraud-detection-ingress
spec:
  rules:
  - host: fraud-detection.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api
            port:
              number: 8000
```

## Backup & Recovery

### Database Backup
```bash
# Backup
docker-compose exec db pg_dump -U fraud_user fraud_detection_db > backup.sql

# Restore
docker-compose exec -T db psql -U fraud_user fraud_detection_db < backup.sql
```

### Model Backup
```bash
# Backup models
tar -czf models_backup.tar.gz models/

# Restore models
tar -xzf models_backup.tar.gz
```

## Health Checks

### API Health
```bash
curl http://localhost:8000/api/v1/health
```

### Database Health
```bash
docker-compose exec db pg_isready -U fraud_user
```

### Redis Health
```bash
docker-compose exec redis redis-cli ping
```

## Performance Optimization

### Database Optimization
- Enable query caching
- Create indices (done in init.sql)
- Regular VACUUM and ANALYZE

### API Optimization
- Enable Redis caching
- Implement rate limiting
- Use connection pooling

### Model Optimization
- Pre-load models at startup
- Cache predictions
- Batch processing

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Database Connection Issues
```bash
# Check PostgreSQL
docker-compose ps db

# View logs
docker-compose logs db

# Recreate
docker-compose down -v db
docker-compose up -d db
```

### Memory Issues
```bash
# Monitor memory
docker stats

# Increase limits in docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 2G
```

## Security Best Practices

1. **Change Default Passwords**: Update Grafana and database passwords
2. **Use HTTPS**: Deploy with SSL/TLS certificates
3. **API Key Rotation**: Regularly rotate API keys
4. **Network Security**: Use VPN/Firewall
5. **Data Encryption**: Enable encrypted connections
6. **Access Control**: Implement RBAC
7. **Audit Logging**: Enable comprehensive logging

## Support and Troubleshooting

For issues and support:
1. Check logs: `docker-compose logs -f`
2. Review configuration: `.env` and `config/settings.py`
3. Test endpoints: Use Swagger docs at `/docs`
4. Check resource usage: `docker stats`
5. Run tests: `pytest tests/`

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
