# Architecture Documentation

## System Overview

The Cybersecurity Fraud Detection System is built on a microservices architecture with real-time processing capabilities.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Applications                      │
│                  (Web, Mobile, Third-party APIs)                │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    ┌──────────v───────────┐
                    │  API Gateway / LB    │
                    │    (Load Balancer)   │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        v                      v                      v
    ┌─────────┐           ┌─────────┐          ┌─────────┐
    │ API     │           │ API     │          │ API     │
    │Instance │           │Instance │    ...   │Instance │
    │    1    │           │    2    │          │    N    │
    └────┬────┘           └────┬────┘          └────┬────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
        ┌──────────────┬────────┴────────┬──────────────┐
        │              │                 │              │
        v              v                 v              v
    ┌────────┐  ┌──────────┐        ┌──────────┐   ┌────────┐
    │ Cache  │  │Database  │        │Message   │   │Files   │
    │(Redis) │  │(PostgreSQL)       │Queue    │   │Storage │
    └────────┘  │                   │(Optional)    │        │
               └──────────┘        └──────────┘    └────────┘
```

## Component Architecture

### 1. API Layer (FastAPI)

**Location**: `src/main.py`, `src/routes.py`

**Responsibilities**:
- REST API endpoints
- Request validation
- Response formatting
- Authentication & authorization
- Rate limiting

**Key Features**:
- Async operations with asyncio
- CORS support
- Request/response logging
- Error handling

### 2. Detection Engines

#### Anomaly Detector
**Location**: `src/detectors.py`
**Algorithm**: Isolation Forest
**Input**: Transaction features
**Output**: Anomaly score (0-1)

```
Transaction Data
    ↓
Feature Extraction
    ↓
Scaling & Preprocessing
    ↓
Isolation Forest Model
    ↓
Anomaly Score & Prediction
```

#### Fraud Detector
**Location**: `src/detectors.py`
**Algorithm**: Random Forest Classifier
**Input**: Transaction & behavior features
**Output**: Fraud probability (0-1)

```
Transaction + Context Data
    ↓
Feature Engineering
    ↓
Random Forest Classifier
    ↓
Fraud Score & Classification
```

#### Phishing Detector
**Location**: `src/phishing_detector.py`
**Algorithm**: Rule-based + NLP
**Input**: Email fields (sender, subject, body, URLs)
**Output**: Phishing score (0-1)

```
Email Data
    ↓
├─ Sender Analysis
├─ Content Analysis
├─ URL Reputation Check
└─ Keyword Matching
    ↓
Aggregate Score & Classification
```

#### Behavioral Analyzer
**Location**: `src/detectors.py`
**Algorithm**: Statistical deviation analysis
**Input**: User action history
**Output**: Anomaly score & severity

```
User Behavior History
    ↓
Establish Baseline
    ↓
Compare Current vs Baseline
    ↓
Calculate Deviation
    ↓
Severity Classification
```

### 3. Data Layer

#### Database (PostgreSQL)
**Location**: `src/database.py`

**Tables**:
- `users` - User profiles
- `transactions` - Transaction records
- `anomaly_detections` - Detected anomalies
- `phishing_detections` - Phishing emails
- `behavioral_patterns` - User behaviors
- `network_traffic` - Network activity
- `model_metrics` - ML performance

**Indexing Strategy**:
- Primary keys for all tables
- Foreign key relationships
- Composite indices for common queries
- Time-based partitioning for large tables

#### Cache (Redis)
**Purposes**:
- Session caching
- Model predictions cache
- Rate limiting
- Temporary data storage

**TTL Strategy**:
- User sessions: 24 hours
- Predictions: 1 hour
- Rate limits: 1 minute

### 4. Configuration Management

**Location**: `config/settings.py`

**Configuration Levels**:
1. Environment variables (highest priority)
2. .env file
3. Default values in settings.py

**Key Settings**:
- Detection thresholds
- Model paths
- Feature flags
- Database connections
- Logging configuration

## Data Flow Diagrams

### Transaction Analysis Flow

```
User Submits
Transaction
    │
    ├─→ [PreProcessing]
    │    ├─ Validate input
    │    ├─ Extract features
    │    └─ Query user history
    │
    ├─→ [Anomaly Detection]
    │    └─ Compare vs baseline
    │
    ├─→ [Fraud Detection]
    │    └─ Run ML model
    │
    ├─→ [Risk Scoring]
    │    └─ Combine scores
    │
    ├─→ [Storage]
    │    └─ Save to database
    │
    └─→ API Response
        ├─ Risk level
        ├─ Scores
        └─ Timestamp
```

### Phishing Email Analysis Flow

```
Email Received
    │
    ├─ Parse Email
    │    ├─ Sender
    │    ├─ Subject
    │    ├─ Body
    │    └─ URLs
    │
    ├─ Sender Analysis
    │    ├─ Domain validation
    │    └─ Spoofing check
    │
    ├─ Content Analysis
    │    ├─ NLP processing
    │    ├─ Keyword matching
    │    └─ Urgency detection
    │
    ├─ URL Analysis
    │    ├─ Domain reputation
    │    ├─ IP address check
    │    └─ Homograph detection
    │
    ├─ Scoring
    │    └─ Weighted scoring
    │
    └─ Classification
        ├─ Store record
        └─ Return result
```

## Security Architecture

### Authentication & Authorization
- API Key validation
- JWT token support
- Role-based access control (RBAC)
- Request signing

### Data Protection
- Input validation & sanitization
- SQL injection prevention (via ORM)
- CORS security
- HTTPS/TLS encryption
- Data encryption at rest (optional)

### Audit & Monitoring
- Request logging
- Error tracking
- Anomaly detection on system level
- Comprehensive audit trail

## Scalability Architecture

### Horizontal Scaling

#### Docker Swarm
```
Docker Swarm
    │
    ├─ API Service (3+ replicas)
    ├─ PostgreSQL (1 primary, N replicas)
    ├─ Redis (clustered mode)
    └─ Load Balancer
```

#### Kubernetes
```
Kubernetes Cluster
    │
    ├─ API Deployment (replicas: 2-10)
    ├─ Database StatefulSet
    ├─ Cache DaemonSet
    ├─ Horizontal Pod Autoscaling
    └─ Ingress Controller
```

### Vertical Scaling
- Increase container resources
- Optimize database indices
- Enable query caching
- Model optimization

### Database Scaling

#### Read Replicas
```
Primary DB
    ├─ Replica 1 (read-only)
    ├─ Replica 2 (read-only)
    └─ Replica N (read-only)
```

#### Partitioning Strategy
- Time-based partitioning for transactions
- User-based sharding for behavioral data
- Archive old data to separate storage

## Performance Optimization

### Caching Strategy
1. **Query Results Cache** - Redis
2. **Model Predictions Cache** - Redis
3. **Database Query Cache** - PostgreSQL
4. **HTTP Caching** - Browser/CDN

### Batch Processing
- Batch anomaly detection
- Bulk model training
- Bulk imports

### Query Optimization
- Indexed columns
- Query result filtering
- Connection pooling
- Statement preparation

## Deployment Architecture

### Development
```
Developer Machine
    ├─ Code Editor
    ├─ Virtual Environment
    ├─ Local PostgreSQL
    ├─ Local Redis
    └─ Development Server
```

### Staging
```
Container Registry
    ├─ Docker Images
    └─ Model Artifacts

Staging Environment
    ├─ Docker Compose
    ├─ Staging Database
    ├─ Staging Cache
    └─ Staging API
```

### Production
```
Cloud Provider
    (AWS/GCP/Azure/On-Premise)
    ├─ Kubernetes Cluster
    ├─ Managed Database
    ├─ Managed Cache
    ├─ Load Balancer
    ├─ Monitoring
    └─ Backup Systems
```

## Monitoring & Observability

### Metrics Collection
**Prometheus**:
- API request latency
- Error rates
- Model prediction time
- Database query time
- Cache hit rates

### Log Aggregation
**ELK Stack** (optional):
- API logs
- Application errors
- Audit logs
- Security events

### Visualization
**Grafana**:
- System health dashboard
- Detection metrics dashboard
- Model performance dashboard
- Alert management

### Alerting
**Alert Conditions**:
- High fraud score (> 0.9)
- Service down
- Database connection failure
- High error rate
- Unusual pattern detection

## CI/CD Architecture

### Development Pipeline
```
Git Commit
    ↓
Pre-commit Hooks
    ├─ Code formatting
    ├─ Linting
    └─ Type checking
    ↓
GitHub Actions / GitLab CI
    ├─ Unit Tests
    ├─ Integration Tests
    ├─ Code Coverage
    └─ Security Scanning
    ↓
Build Docker Image
    ↓
Push to Registry
    ↓
Deploy to Staging
```

### Deployment Pipeline
```
Merge to Main
    ↓
Tag Release
    ↓
Build Release Image
    ↓
Run Full Test Suite
    ↓
Security Scanning
    ↓
Deploy to Production
    ├─ Blue-Green Deployment
    ├─ Health Checks
    └─ Rollback Capability
```

## Model Management

### Model Training Pipeline
```
Historical Data
    ↓
Feature Engineering
    ↓
Data Splitting
    ├─ Training (70%)
    ├─ Validation (15%)
    └─ Test (15%)
    ↓
Model Training
    ├─ Isolation Forest
    ├─ Random Forest
    └─ Hyperparameter Tuning
    ↓
Model Evaluation
    ├─ Accuracy
    ├─ Precision/Recall
    ├─ F1 Score
    └─ ROC-AUC
    ↓
Model Versioning
    └─ Save & Register
    ↓
Model Serving
    └─ Load in API
```

### Model Versioning
```
models/
├── isolation_forest_v1.pkl
├── isolation_forest_v2.pkl
├── fraud_detector_v1.pkl
├── fraud_detector_v2.pkl
├── fraud_detector_v3.pkl (current)
└── fraud_detector_v3.metadata
    ├─ accuracy: 0.95
    ├─ precision: 0.93
    ├─ recall: 0.91
    └─ training_date: 2024-03-27
```

## Error Handling & Recovery

### Error Categories and Handling

| Error Type | Handling | Recovery |
|-----------|----------|----------|
| Validation Error | Return 400 | User correction |
| Not Found | Return 404 | Check input |
| Service Error | Return 500 | Auto-retry |
| DB Connection | Return 503 | Connection pool retry |
| Timeout | Return 504 | Async retry |

### Circuit Breaker Pattern
```
Healthy
    ↓
   (Failure Threshold Exceeded)
    ↓
Open (Reject Requests)
    ↓
   (Timeout Duration)
    ↓
Half-Open (Test Request)
    ↓
   Success / Failure
    ↓
Healthy / Open
```

## Conclusion

This architecture provides:
- ✅ **Scalability** - Horizontal and vertical scaling
- ✅ **Reliability** - Failover and recovery mechanisms
- ✅ **Performance** - Caching and optimization
- ✅ **Maintainability** - Clear separation of concerns
- ✅ **Observability** - Comprehensive monitoring
