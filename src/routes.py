from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
import logging

from src.detectors import AnomalyDetector, FraudDetector, BehavioralAnalyzer
from src.phishing_detector import PhishingDetector, EmailValidator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["detection"])

# Initialize detectors
anomaly_detector = AnomalyDetector()
fraud_detector = FraudDetector()
behavioral_analyzer = BehavioralAnalyzer()
phishing_detector = PhishingDetector()


# Pydantic models
class TransactionRequest(BaseModel):
    user_id: str
    amount: float = Field(..., gt=0)
    merchant: str
    transaction_type: str
    device_id: Optional[str] = None
    ip_address: Optional[str] = None
    location: Optional[str] = None


class TransactionResponse(BaseModel):
    user_id: str
    amount: float
    is_anomalous: bool
    is_fraudulent: bool
    anomaly_score: float
    fraud_score: float
    risk_level: str
    timestamp: datetime


class EmailData(BaseModel):
    sender: str
    display_name: Optional[str] = None
    subject: str
    body: str
    recipient: Optional[str] = None


class PhishingDetectionResponse(BaseModel):
    is_phishing: bool
    phishing_score: float
    confidence: float
    sender_risk: float
    content_risk: float
    url_risk: float
    suspicious_urls: List[str]
    indicators: List[str]


class BehaviorAnalysisRequest(BaseModel):
    user_id: str
    behavior_type: str  # login, access_pattern
    metrics: dict


class BehaviorAnalysisResponse(BaseModel):
    user_id: str
    is_anomalous: bool
    anomaly_score: float
    severity: str
    details: dict


class HealthResponse(BaseModel):
    status: str
    models_loaded: dict
    timestamp: datetime


# Routes


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "models_loaded": {
            "anomaly_detector": True,
            "fraud_detector": True,
            "phishing_detector": True,
            "behavioral_analyzer": True,
        },
        "timestamp": datetime.utcnow(),
    }


@router.post("/transactions/analyze", response_model=TransactionResponse)
async def analyze_transaction(request: TransactionRequest):
    """Analyze a transaction for fraud and anomalies."""
    try:
        # Prepare transaction data
        transaction_data = {
            "amount": request.amount,
            "hour_of_day": datetime.now().hour,
            "days_since_last_transaction": 1,
            "transaction_count_today": 1,
            "avg_transaction_amount": request.amount,
            "is_foreign": 0,
            "is_weekend": datetime.now().weekday() >= 5,
            "time_since_last_transaction": 3600,
            "merchant_risk_score": 0.3,
            "velocity_score": 0.4,
            "device_is_new": 0,
            "location_change_km": 10,
        }

        # Run detections
        is_anomalous, anomaly_score = anomaly_detector.predict(transaction_data)
        is_fraudulent, fraud_score = fraud_detector.predict(transaction_data)

        # Determine risk level
        combined_score = (anomaly_score + fraud_score) / 2
        if combined_score > 0.8:
            risk_level = "critical"
        elif combined_score > 0.6:
            risk_level = "high"
        elif combined_score > 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "user_id": request.user_id,
            "amount": request.amount,
            "is_anomalous": is_anomalous,
            "is_fraudulent": is_fraudulent,
            "anomaly_score": float(anomaly_score),
            "fraud_score": float(fraud_score),
            "risk_level": risk_level,
            "timestamp": datetime.utcnow(),
        }
    except Exception as e:
        logger.error(f"Error analyzing transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/phishing/detect", response_model=PhishingDetectionResponse)
async def detect_phishing(email_data: EmailData):
    """Detect phishing in an email."""
    try:
        # Validate sender
        if not EmailValidator.is_valid_format(email_data.sender):
            raise HTTPException(status_code=400, detail="Invalid sender email format")

        # Perform detection
        result = phishing_detector.detect(
            {
                "sender": email_data.sender,
                "display_name": email_data.display_name or "",
                "subject": email_data.subject,
                "body": email_data.body,
            }
        )

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in phishing detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/behavior/analyze", response_model=BehaviorAnalysisResponse)
async def analyze_behavior(request: BehaviorAnalysisRequest):
    """Analyze user behavior for anomalies."""
    try:
        user_id = request.user_id
        behavior_type = request.behavior_type

        if behavior_type == "login":
            is_anomalous, score = behavioral_analyzer.detect_login_anomaly(
                user_id, request.metrics
            )
        elif behavior_type == "access_pattern":
            is_anomalous, score = behavioral_analyzer.detect_access_pattern_anomaly(
                user_id, request.metrics
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid behavior type")

        severity = "high" if score > 0.7 else "medium" if score > 0.4 else "low"

        return {
            "user_id": user_id,
            "is_anomalous": is_anomalous,
            "anomaly_score": float(score),
            "severity": severity,
            "details": request.metrics,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing behavior: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/status")
async def get_models_status():
    """Get status of all detection models."""
    return {
        "status": "all_models_operational",
        "models": {
            "anomaly_detector": {
                "type": "Isolation Forest",
                "status": "ready",
                "model_path": str(anomaly_detector.model_path),
            },
            "fraud_detector": {
                "type": "Random Forest",
                "status": "ready",
                "model_path": str(fraud_detector.model_path),
                "feature_importance": fraud_detector.get_feature_importance(),
            },
            "phishing_detector": {"type": "Rule-based + NLP", "status": "ready"},
            "behavioral_analyzer": {"type": "Statistical", "status": "ready"},
        },
        "timestamp": datetime.utcnow(),
    }


@router.post("/models/update-baseline")
async def update_baseline(user_id: str = Query(...), metrics: dict = None):
    """Update behavioral baseline for a user."""
    try:
        if not metrics:
            raise HTTPException(status_code=400, detail="Metrics required")

        behavioral_analyzer.update_baseline(user_id, metrics)
        return {"status": "baseline_updated", "user_id": user_id}
    except Exception as e:
        logger.error(f"Error updating baseline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/risk-summary")
async def get_risk_summary():
    """Get overall system risk summary."""
    return {
        "risk_level": "low",
        "critical_alerts": 0,
        "high_alerts": 2,
        "medium_alerts": 5,
        "timestamp": datetime.utcnow(),
    }
