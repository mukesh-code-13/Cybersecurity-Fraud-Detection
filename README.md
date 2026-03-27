# Cybersecurity-Fraud-Detection

<div align="center">

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Real-time AI-driven Cybersecurity & Fraud Detection System**

[Features](#features) • [Quick Start](#quick-start) • [Architecture](#architecture) • [API](#api) • [Deployment](#deployment)

</div>

---

## Overview

This project develops a comprehensive **AI-driven cybersecurity and fraud detection system** that monitors network traffic, user behavior, and transactions in real-time. Using advanced machine learning algorithms and natural language processing, it detects anomalies, phishing attempts, and fraudulent transactions while maintaining data integrity and reducing cyber risks.

### Key Capabilities
- 🔍 **Real-time threat detection** across multiple vectors
- 🤖 **ML-powered anomaly detection** using Isolation Forest
- 🎯 **Fraud detection** with Random Forest classification
- 📧 **Phishing email detection** with NLP analysis
- 👥 **Behavioral analysis** for user patterns
- 📊 **Network traffic monitoring** and analysis
- 📈 **Comprehensive monitoring** with Prometheus & Grafana
- 🐳 **Containerized deployment** with Docker & Kubernetes support

## Features

### Detection Engines

| Engine | Technology | Threshold | Purpose |
|--------|-----------|-----------|---------|
| **Anomaly Detection** | Isolation Forest | 0.70 | Detects unusual transactions and behaviors |
| **Fraud Detection** | Random Forest | 0.80 | Classifies transactions as fraudulent or legitimate |
| **Phishing Detection** | Rule-based + NLP | 0.75 | Identifies phishing emails with multiple indicators |
| **Behavioral Analysis** | Statistical | 0.65 | Recognizes deviations from user baselines |

### Data Monitoring

- **Network Traffic**: IP addresses, protocols, packet analysis
- **User Behavior**: Login patterns, access attempts, resource usage
- **Transactions**: Amount, merchant, location, device, velocity
- **Email Security**: Sender analysis, content inspection, URL reputation

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- 8GB RAM, 4 CPU cores minimum
- PostgreSQL 12+ (for persistent storage)

### Using Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/mukesh-code-13/Cybersecurity-Fraud-Detection.git
cd Cybersecurity-Fraud-Detection

# Run setup script
chmod +x deploy/setup.sh
./deploy/setup.sh
```

### Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python -m uvicorn src.main:app --reload --port 8000
```

Access the API at: **http://localhost:8000/docs**

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Fraud Detection System                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Anomaly     │  │  Fraud       │  │  Phishing    │      │
│  │  Detector    │  │  Detector    │  │  Detector    │      │
│  │(ISO Forest)  │  │(RF Classifier)│  │(NLP + Rules) │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│  ┌──────────────────────────────────────────────┐           │
│  │      Behavioral Analyzer                     │           │
│  │      & Pattern Recognition                   │           │
│  └──────────────────────────────────────────────┘           │
│         │                   │                   │            │
│  ┌──────v────────┐  ┌──────v────────┐  ┌──────v────────┐  │
│  │  PostgreSQL   │  │   Redis       │  │  Network      │  │
│  │  Database     │  │   Cache       │  │  Monitoring   │  │
│  └───────────────┘  └───────────────┘  └───────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Component Details

**Backend**: FastAPI with async support  
**ML Models**: scikit-learn (Isolation Forest, Random Forest)  
**NLP**: NLTK, spaCy, regex patterns  
**Database**: PostgreSQL for persistence  
**Cache**: Redis for performance  
**Monitoring**: Prometheus + Grafana  

## API Endpoints

### Health & Status
- `GET /` - API information
- `GET /api/v1/health` - Health check
- `GET /api/v1/models/status` - Model status

### Detection Endpoints
- `POST /api/v1/transactions/analyze` - Analyze transaction for fraud
- `POST /api/v1/phishing/detect` - Detect phishing in email
- `POST /api/v1/behavior/analyze` - Analyze user behavior
- `GET /api/v1/alerts/risk-summary` - Get system risk summary

### Management
- `POST /api/v1/models/update-baseline` - Update user behavior baseline

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Usage

### Analyze Transaction
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/transactions/analyze",
    json={
        "user_id": "user123",
        "amount": 150.00,
        "merchant": "Amazon",
        "transaction_type": "purchase",
        "device_id": "device456",
        "ip_address": "192.168.1.1",
        "location": "New York"
    }
)

result = response.json()
print(f"Risk Level: {result['risk_level']}")
print(f"Fraud Score: {result['fraud_score']}")
print(f"Anomaly Score: {result['anomaly_score']}")
```

### Detect Phishing Email
```python
response = requests.post(
    "http://localhost:8000/api/v1/phishing/detect",
    json={
        "sender": "verify@secure-bank.com",
        "subject": "URGENT: Verify Your Account Now",
        "body": "Click here immediately to confirm your password..."
    }
)

result = response.json()
print(f"Is Phishing: {result['is_phishing']}")
print(f"Phishing Score: {result['phishing_score']}")
print(f"Indicators: {result['indicators']}")
```

### Analyze User Behavior
```python
response = requests.post(
    "http://localhost:8000/api/v1/behavior/analyze",
    json={
        "user_id": "user123",
        "behavior_type": "login",
        "metrics": {
            "hour": 14,
            "latitude": 40.7128,
            "longitude": -74.0060
        }
    }
)

result = response.json()
print(f"Is Anomalous: {result['is_anomalous']}")
print(f"Severity: {result['severity']}")
```

## ML Models

### Anomaly Detection
- **Algorithm**: Isolation Forest
- **Input Features**: Amount, Time, Frequency, Velocity
- **Output**: Is Anomalous (Boolean), Anomaly Score (0-1)
- **Threshold**: 0.70

### Fraud Detection
- **Algorithm**: Random Forest Classifier
- **Input Features**: Transaction details, behavior patterns, device info
- **Output**: Is Fraud (Boolean), Fraud Score (0-1)
- **Threshold**: 0.80

### Phishing Detection
- **Algorithm**: Rule-based + NLP
- **Input**: Email sender, subject, body, URLs
- **Output**: Is Phishing (Boolean), Confidence (0-1)
- **Checks**: 
  - Sender spoofing
  - Urgency indicators
  - Suspicious URLs
  - Sensitive information requests

### Behavioral Analysis
- **Algorithm**: Statistical deviation from baseline
- **Input**: User action patterns
- **Output**: Is Anomalous (Boolean), Severity (Low/Medium/High)

## Deployment

### Docker Compose (Recommended)
```bash
docker-compose up -d
```

Services:
- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Kubernetes
See [DEPLOYMENT.md](DEPLOYMENT.md) for complete Kubernetes deployment guide.

### Cloud Deployment
- **AWS**: ECS/Fargate with RDS PostgreSQL
- **Google Cloud**: Cloud Run with Cloud SQL
- **Azure**: Container Instances with Azure Database

## Configuration

### Environment Variables
Create `.env` file:
```env
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=postgresql://fraud_user:fraud_pass@db:5432/fraud_detection_db
REDIS_URL=redis://redis:6379/0
ANOMALY_THRESHOLD=0.7
PHISHING_THRESHOLD=0.75
FRAUD_THRESHOLD=0.8
DEBUG=False
```

### Model Thresholds
Edit `config/settings.py`:
```python
ANOMALY_THRESHOLD = 0.7      # Anomaly detection sensitivity
PHISHING_THRESHOLD = 0.75    # Phishing detection sensitivity
FRAUD_THRESHOLD = 0.8        # Fraud detection sensitivity
```

## Monitoring

### Prometheus Metrics
- Request latency and error rates
- Model prediction times
- Database query performance
- Cache hit rates

### Grafana Dashboards
- System overview
- Detection metrics
- Model performance
- User activity analysis

Access Grafana: http://localhost:3000 (admin/admin)

## Testing

### Run Tests
```bash
pytest tests/ -v
```

### Test Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

### API Integration Testing
```bash
# Test transaction analysis
curl -X POST http://localhost:8000/api/v1/transactions/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "amount": 100.0,
    "merchant": "TestStore",
    "transaction_type": "purchase"
  }'
```

## Model Training

Train ML models with your data:

```bash
python scripts/train_models.py \
  --data data/training_data/transactions.csv \
  --anomaly-model models/isolation_forest.pkl \
  --fraud-model models/fraud_detector.pkl
```

## Database Schema

### Key Tables
- **users**: User profiles and risk scores
- **transactions**: Transaction records with fraud labels
- **anomaly_detections**: Detected anomalies with scores
- **phishing_detections**: Phishing email records
- **behavioral_patterns**: User behavioral metrics
- **network_traffic**: Network activity logs
- **model_metrics**: ML model performance metrics

See [deploy/init.sql](deploy/init.sql) for complete schema.

## Performance

### Latency
- Transaction analysis: < 100ms
- Phishing detection: < 50ms
- Behavior analysis: < 75ms

### Throughput
- Transactions: 1000+ req/sec (single instance)
- Phishing detection: 500+ req/sec
- Parallel scalability: Linear with additional replicas

### Resource Usage
- Base memory: 500MB
- Per model: 50-200MB
- Cold start time: < 10 seconds

## Security

- ✅ API key authentication
- ✅ HTTPS/TLS support
- ✅ Database encryption
- ✅ Input validation
- ✅ Rate limiting
- ✅ CORS enabled
- ✅ Comprehensive logging

## Logging

View logs:
```bash
# Docker
docker-compose logs -f api

# Local
tail -f logs/fraud_detection.log

# Kubernetes
kubectl logs -f deployment/api
```

## File Structure

```
Cybersecurity-Fraud-Detection/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── routes.py            # API endpoints
│   ├── database.py          # SQLAlchemy models
│   ├── detectors.py         # ML detection engines
│   └── phishing_detector.py # Phishing detection
├── config/
│   ├── settings.py          # Application settings
│   ├── phishing_keywords.txt# Phishing indicators
│   └── spam_keywords.txt    # Spam indicators
├── models/                  # Trained ML models
├── data/                    # Training data
├── deploy/
│   ├── docker-compose.yml   # Docker orchestration
│   ├── Dockerfile           # Container definition
│   ├── init.sql             # Database schema
│   └── prometheus.yml       # Monitoring config
├── tests/
│   ├── test_api.py          # API tests
│   └── test_detectors.py    # Model tests
├── scripts/
│   └── train_models.py      # Model training script
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── README.md                # This file
└── DEPLOYMENT.md            # Deployment guide
```

## Troubleshooting

### Port Already in Use
```bash
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error
```bash
docker-compose down -v
docker-compose up -d
```

### Memory Issues
```bash
docker stats
# Increase memory limits in docker-compose.yml
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [ ] Mobile app for alerts
- [ ] Advanced NLP for email analysis
- [ ] Real-time network packet analysis
- [ ] Graph neural networks for pattern detection
- [ ] Integration with SIEM systems
- [ ] Custom model training API
- [ ] Multi-language support
- [ ] Advanced visualization dashboard

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- 📧 Email: support@fraud-detection-system.com
- 🐛 Issues: [GitHub Issues](https://github.com/mukesh-code-13/Cybersecurity-Fraud-Detection/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/mukesh-code-13/Cybersecurity-Fraud-Detection/discussions)

## Acknowledgments

- FastAPI community for excellent framework
- scikit-learn for ML algorithms
- Docker for containerization
- PostgreSQL community for reliable database

---

<div align="center">

**Built with ❤️ for cybersecurity professionals**

[⬆ back to top](#cybersecurity-fraud-detection)

</div>
=======
# Cybersecurity Fraud Detection

## Project Overview
This project aims to detect fraudulent activities in cybersecurity. By utilizing various algorithms and machine learning techniques, the project identifies anomalies in user behavior.

## Features
- Real-time fraud detection
- Machine learning algorithms for anomaly detection
- Comprehensive reporting and analytics
- User-friendly interface

## Installation
To install the project, follow these steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/mukesh-code-13/Cybersecurity-Fraud-Detection.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Cybersecurity-Fraud-Detection
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the project, use the command:
```bash
python main.py
```

## Architecture
The architecture consists of a data collection layer, machine learning layer, and presentation layer. The data is processed to detect patterns that indicate fraud.

## Contribution Guidelines
1. Fork the repository.
2. Create a new branch (`feature-branch`) for your feature:
   ```bash
   git checkout -b feature-branch
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your message"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a pull request.
>>>>>>> 8a4d3d51a979055d08ed1c4301cc009ec7f4c8e2
