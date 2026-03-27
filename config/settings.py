import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration settings."""
    
    # API Settings
    API_TITLE: str = "Cybersecurity & Fraud Detection System"
    API_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://fraud_user:fraud_pass@localhost:5432/fraud_detection_db"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # ML Models Path
    MODELS_PATH: str = "models/"
    
    # Thresholds
    ANOMALY_THRESHOLD: float = 0.7
    PHISHING_THRESHOLD: float = 0.75
    FRAUD_THRESHOLD: float = 0.8
    
    # NLP Settings
    PHISHING_KEYWORDS_FILE: str = "config/phishing_keywords.txt"
    SPAM_KEYWORDS_FILE: str = "config/spam_keywords.txt"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/fraud_detection.log"
    
    # Security
    API_KEY: Optional[str] = os.getenv("API_KEY", "your-secure-api-key-here")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-jwt-secret-key")
    
    # Feature Settings
    ENABLE_ANOMALY_DETECTION: bool = True
    ENABLE_PHISHING_DETECTION: bool = True
    ENABLE_FRAUD_DETECTION: bool = True
    ENABLE_BEHAVIORAL_ANALYSIS: bool = True
    
    # Model Configuration
    MODEL_UPDATE_INTERVAL: int = 3600  # seconds
    BATCH_PROCESSING_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
