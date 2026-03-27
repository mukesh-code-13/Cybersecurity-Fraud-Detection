from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    Text,
    JSON,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class User(Base):
    """User entity for fraud detection tracking."""

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    risk_score = Column(Float, default=0.0)

    transactions = relationship("Transaction", back_populates="user")
    behaviors = relationship("BehavioralPattern", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


class Transaction(Base):
    """Transaction entity for fraud detection."""

    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    merchant = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    location = Column(String)
    device_id = Column(String)
    ip_address = Column(String)

    is_fraudulent = Column(Boolean, default=False)
    fraud_score = Column(Float, default=0.0)
    detection_method = Column(String)

    raw_features = Column(JSON)

    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.id} - Amount: {self.amount}>"


class AnomalyDetection(Base):
    """Anomaly detection records."""

    __tablename__ = "anomaly_detections"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    anomaly_type = Column(String, nullable=False)  # network, behavioral, transaction
    anomaly_score = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    description = Column(Text)
    is_confirmed = Column(Boolean, default=False)
    features = Column(JSON)

    def __repr__(self):
        return f"<AnomalyDetection {self.id}>"


class PhishingDetection(Base):
    """Phishing detection records."""

    __tablename__ = "phishing_detections"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email_subject = Column(String)
    email_body = Column(Text)
    sender_email = Column(String, index=True)
    recipient_email = Column(String, index=True)
    phishing_score = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    is_phishing = Column(Boolean, default=False)
    indicators = Column(JSON)
    action_taken = Column(String)  # quarantined, deleted, flagged

    def __repr__(self):
        return f"<PhishingDetection {self.id}>"


class BehavioralPattern(Base):
    """User behavioral patterns for analysis."""

    __tablename__ = "behavioral_patterns"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    pattern_type = Column(String, nullable=False)  # login, transaction, network
    metric = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    baseline = Column(Float)
    deviation = Column(Float)

    user = relationship("User", back_populates="behaviors")

    def __repr__(self):
        return f"<BehavioralPattern {self.id}>"


class NetworkTraffic(Base):
    """Network traffic monitoring records."""

    __tablename__ = "network_traffic"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_ip = Column(String, index=True)
    destination_ip = Column(String, index=True)
    port = Column(Integer)
    protocol = Column(String)
    packet_count = Column(Integer)
    byte_count = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    anomaly_score = Column(Float, default=0.0)
    is_suspicious = Column(Boolean, default=False)
    metadata = Column(JSON)

    def __repr__(self):
        return f"<NetworkTraffic {self.source_ip} -> {self.destination_ip}>"


class ModelMetrics(Base):
    """ML model performance metrics."""

    __tablename__ = "model_metrics"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model_name = Column(String, nullable=False, index=True)
    model_version = Column(String)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    training_samples = Column(Integer)

    def __repr__(self):
        return f"<ModelMetrics {self.model_name}>"
