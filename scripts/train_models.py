#!/usr/bin/env python3
"""
Model training script for fraud detection system.
Trains ML models with historical data.
"""

import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import logging
from pathlib import Path

from src.detectors import AnomalyDetector, FraudDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(filepath):
    """Load training data from CSV."""
    logger.info(f"Loading data from {filepath}")
    return pd.read_csv(filepath)


def prepare_anomaly_data(df):
    """Prepare data for anomaly detection."""
    features = df[
        [
            "amount",
            "hour_of_day",
            "days_since_last_transaction",
            "transaction_count_today",
            "avg_transaction_amount",
        ]
    ].values
    return features


def prepare_fraud_data(df):
    """Prepare data for fraud detection."""
    X = df[
        [
            "amount",
            "is_foreign",
            "is_weekend",
            "time_since_last_transaction",
            "merchant_risk_score",
            "velocity_score",
            "device_is_new",
            "location_change_km",
        ]
    ].values
    y = df["is_fraudulent"].values
    return X, y


def train_anomaly_detector(X):
    """Train anomaly detection model."""
    logger.info("Training anomaly detection model...")
    detector = AnomalyDetector()
    detector.train(X)
    logger.info("Anomaly detection model trained successfully")
    return detector


def train_fraud_detector(X, y):
    """Train fraud detection model."""
    logger.info("Training fraud detection model...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    detector = FraudDetector()
    detector.train(X_train, y_train)

    # Evaluate
    y_pred = detector.model.predict(detector.scaler.fit_transform(X_test))
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    logger.info(f"Fraud Detection Model Performance:")
    logger.info(f"  Accuracy: {accuracy:.4f}")
    logger.info(f"  Precision: {precision:.4f}")
    logger.info(f"  Recall: {recall:.4f}")
    logger.info(f"  F1 Score: {f1:.4f}")

    return detector


def main():
    parser = argparse.ArgumentParser(description="Train fraud detection models")
    parser.add_argument(
        "--data", type=str, required=True, help="Path to training data CSV"
    )
    parser.add_argument(
        "--anomaly-model",
        type=str,
        default="models/isolation_forest.pkl",
        help="Path to save anomaly detection model",
    )
    parser.add_argument(
        "--fraud-model",
        type=str,
        default="models/fraud_detector.pkl",
        help="Path to save fraud detection model",
    )

    args = parser.parse_args()

    # Load data
    df = load_data(args.data)
    logger.info(f"Loaded {len(df)} records")

    # Train anomaly detector
    X_anomaly = prepare_anomaly_data(df)
    anomaly_detector = train_anomaly_detector(X_anomaly)

    # Train fraud detector
    X_fraud, y_fraud = prepare_fraud_data(df)
    fraud_detector = train_fraud_detector(X_fraud, y_fraud)

    logger.info("Model training completed successfully!")
    logger.info(f"Models saved to {args.anomaly_model} and {args.fraud_model}")


if __name__ == "__main__":
    main()
