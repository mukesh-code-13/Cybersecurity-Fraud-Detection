# Quick Start Guide

Get the Cybersecurity Fraud Detection System running in minutes!

## Option 1: Docker (Recommended - Fastest)

### Prerequisites
- Docker & Docker Compose installed
- ~15 minutes of setup time
- 8GB RAM available

### Quick Start Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/mukesh-code-13/Cybersecurity-Fraud-Detection.git
   cd Cybersecurity-Fraud-Detection
   ```

2. **Run Setup Script**
   ```bash
   chmod +x deploy/setup.sh
   ./deploy/setup.sh
   ```
   
   This script will:
   - Create `.env` file
   - Build Docker images
   - Start all services
   - Display service URLs

3. **Verify Services**
   ```bash
   # Check all services are running
   docker-compose ps
   
   # Check API health
   curl http://localhost:8000/api/v1/health
   ```

4. **Access Services**
   - **API Documentation**: http://localhost:8000/docs
   - **API ReDoc**: http://localhost:8000/redoc
   - **Prometheus**: http://localhost:9090
   - **Grafana**: http://localhost:3000 (admin/admin)

## Option 2: Local Development

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- Redis 5+
- Git

### Quick Start Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/mukesh-code-13/Cybersecurity-Fraud-Detection.git
   cd Cybersecurity-Fraud-Detection
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database and Redis URLs
   ```

5. **Initialize Database**
   ```bash
   psql fraud_detection_db -U fraud_user -f deploy/init.sql
   ```

6. **Start Development Server**
   ```bash
   python -m uvicorn src.main:app --reload --port 8000
   ```

7. **Access API**
   - API Documentation: http://localhost:8000/docs

## First Steps - Test the API

### 1. Check API Health
```bash
curl http://localhost:8000/api/v1/health
```

### 2. Test Transaction Analysis
```bash
curl -X POST http://localhost:8000/api/v1/transactions/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "amount": 100.0,
    "merchant": "Amazon",
    "transaction_type": "purchase"
  }'
```

### 3. Test Phishing Detection
```bash
curl -X POST http://localhost:8000/api/v1/phishing/detect \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "verify@bank.com",
    "subject": "Verify Your Account",
    "body": "Click here to verify your account immediately"
  }'
```

### 4. Interactive Testing
Visit **http://localhost:8000/docs** for interactive API documentation where you can:
- Test all endpoints
- See request/response examples
- View parameter descriptions

## Using the Python Client

```python
from scripts.client_example import FraudDetectionClient

# Initialize client
client = FraudDetectionClient()

# Analyze a transaction
result = client.analyze_transaction(
    user_id="user123",
    amount=50.00,
    merchant="Amazon",
    transaction_type="purchase"
)
print(f"Risk Level: {result['risk_level']}")
print(f"Fraud Score: {result['fraud_score']}")
```

Run example:
```bash
python scripts/client_example.py
```

## Using Make Commands

```bash
# Install dependencies
make install

# Setup development environment
make dev-setup

# Start all services
make up

# View logs
make logs

# Run tests
make test

# Run example client
make client

# See all available commands
make help
```

## Project Structure Overview

```
Cybersecurity-Fraud-Detection/
├── src/                    # Main application code
│   ├── main.py            # FastAPI app
│   ├── routes.py          # API endpoints
│   ├── detectors.py       # ML detection engines
│   └── phishing_detector.py
├── config/                # Configuration files
├── models/                # ML models (created after training)
├── data/                  # Training data
├── tests/                 # Test suite
├── scripts/               # Utility scripts
├── deploy/                # Docker & deployment configs
├── docker-compose.yml     # Docker orchestration
├── requirements.txt       # Python dependencies
└── Makefile              # Convenient commands
```

## Troubleshooting

### Error: Port 8000 Already in Use
```bash
lsof -i :8000
kill -9 <PID>
```

### Error: Database Connection Failed
```bash
# Ensure database is running
docker-compose ps db

# Restart database
docker-compose restart db
```

### Error: Redis Connection Failed
```bash
# Ensure Redis is running
docker-compose ps redis

# Restart Redis
docker-compose restart redis
```

### Want to See More Details?
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for advanced deployment options
- Review [README.md](README.md) for comprehensive documentation
- Run tests: `pytest tests/ -v`

## Next Steps

1. **Explore API Documentation**: Visit http://localhost:8000/docs
2. **Configure Thresholds**: Edit `config/settings.py`
3. **Train Models**: Run `python scripts/train_models.py --data your_data.csv`
4. **Setup Monitoring**: Configure Grafana dashboards
5. **Deploy to Production**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## Getting Help

- 📖 Read the [README.md](README.md)
- 📦 Check [DEPLOYMENT.md](DEPLOYMENT.md)
- 🧪 Run tests: `pytest tests/ -v`
- 🐛 Check logs: `make logs`
- 💻 Use interactive docs: http://localhost:8000/docs

## Common Tasks

### Train ML Models
```bash
python scripts/train_models.py --data data/training_data/transactions.csv
```

### View API Documentation
```
http://localhost:8000/docs
```

### Monitor System Performance
```
http://localhost:9090  # Prometheus
http://localhost:3000  # Grafana
```

### Run All Tests
```bash
make test
```

### Check Code Quality
```bash
make lint
make format
```

---

**You're now ready to use the Fraud Detection System!** 🎉

For more information, see the [README.md](README.md) and [DEPLOYMENT.md](DEPLOYMENT.md).
