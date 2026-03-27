#!/usr/bin/env python3
"""
Example client script for Fraud Detection API.
Demonstrates how to use the detection endpoints.
"""

import requests
import json
from typing import Dict
from datetime import datetime


class FraudDetectionClient:
    """Client for Fraud Detection API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize client."""
        self.base_url = base_url
        self.session = requests.Session()

    def health_check(self) -> Dict:
        """Check API health."""
        response = self.session.get(f"{self.base_url}/api/v1/health")
        return response.json()

    def analyze_transaction(
        self,
        user_id: str,
        amount: float,
        merchant: str,
        transaction_type: str = "purchase",
        device_id: str = None,
        ip_address: str = None,
        location: str = None,
    ) -> Dict:
        """Analyze a transaction for fraud."""
        payload = {
            "user_id": user_id,
            "amount": amount,
            "merchant": merchant,
            "transaction_type": transaction_type,
        }

        if device_id:
            payload["device_id"] = device_id
        if ip_address:
            payload["ip_address"] = ip_address
        if location:
            payload["location"] = location

        response = self.session.post(
            f"{self.base_url}/api/v1/transactions/analyze", json=payload
        )
        return response.json()

    def detect_phishing(
        self,
        sender: str,
        subject: str,
        body: str,
        display_name: str = None,
        recipient: str = None,
    ) -> Dict:
        """Analyze email for phishing."""
        payload = {
            "sender": sender,
            "subject": subject,
            "body": body,
        }

        if display_name:
            payload["display_name"] = display_name
        if recipient:
            payload["recipient"] = recipient

        response = self.session.post(
            f"{self.base_url}/api/v1/phishing/detect", json=payload
        )
        return response.json()

    def analyze_behavior(self, user_id: str, behavior_type: str, metrics: Dict) -> Dict:
        """Analyze user behavior."""
        payload = {
            "user_id": user_id,
            "behavior_type": behavior_type,
            "metrics": metrics,
        }

        response = self.session.post(
            f"{self.base_url}/api/v1/behavior/analyze", json=payload
        )
        return response.json()

    def get_models_status(self) -> Dict:
        """Get status of all models."""
        response = self.session.get(f"{self.base_url}/api/v1/models/status")
        return response.json()

    def get_api_info(self) -> Dict:
        """Get API information."""
        response = self.session.get(f"{self.base_url}/api/v1/info")
        return response.json()


def main():
    """Run example usage."""

    # Initialize client
    client = FraudDetectionClient()

    print("=" * 60)
    print("Fraud Detection System - API Client Examples")
    print("=" * 60)
    print()

    # 1. Health Check
    print("1. Health Check")
    print("-" * 60)
    try:
        health = client.health_check()
        print(f"Status: {health.get('status')}")
        print(f"Available Models: {list(health.get('models_loaded', {}).keys())}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # 2. API Information
    print("2. API Information")
    print("-" * 60)
    try:
        info = client.get_api_info()
        print(json.dumps(info, indent=2))
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # 3. Analyze Normal Transaction
    print("3. Analyze Normal Transaction")
    print("-" * 60)
    try:
        result = client.analyze_transaction(
            user_id="user_123",
            amount=50.99,
            merchant="Amazon",
            transaction_type="purchase",
            device_id="device_001",
            ip_address="192.168.1.100",
            location="New York, NY",
        )
        print(f"User ID: {result['user_id']}")
        print(f"Amount: ${result['amount']}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Fraud Score: {result['fraud_score']:.4f}")
        print(f"Anomaly Score: {result['anomaly_score']:.4f}")
        print(f"Is Fraudulent: {result['is_fraudulent']}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # 4. Analyze Suspicious Transaction
    print("4. Analyze Suspicious Transaction")
    print("-" * 60)
    try:
        result = client.analyze_transaction(
            user_id="user_456",
            amount=5000.00,
            merchant="WireTransfer",
            transaction_type="wire_transfer",
            device_id="device_unknown",
            ip_address="192.168.1.200",
            location="Unknown Location",
        )
        print(f"User ID: {result['user_id']}")
        print(f"Amount: ${result['amount']}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Fraud Score: {result['fraud_score']:.4f}")
        print(f"Anomaly Score: {result['anomaly_score']:.4f}")
        print(f"Is Fraudulent: {result['is_fraudulent']}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # 5. Detect Legitimate Email
    print("5. Detect Legitimate Email")
    print("-" * 60)
    try:
        result = client.detect_phishing(
            sender="support@amazon.com",
            display_name="Amazon Customer Service",
            subject="Your Order Confirmation #123456",
            body="Thank you for your purchase. Your order has been confirmed and will be shipped soon.",
        )
        print(f"Is Phishing: {result['is_phishing']}")
        print(f"Phishing Score: {result['phishing_score']:.4f}")
        print(f"Confidence: {result['confidence']:.4f}")
        print(f"Sender Risk: {result['sender_risk']:.4f}")
        print(f"Content Risk: {result['content_risk']:.4f}")
        print(f"URL Risk: {result['url_risk']:.4f}")
        print(f"Indicators: {result['indicators']}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # 6. Detect Phishing Email
    print("6. Detect Phishing Email")
    print("-" * 60)
    try:
        result = client.detect_phishing(
            sender="verify@secure-bank-confirm.com",
            display_name="Bank Support",
            subject="URGENT: Verify Your Account Immediately",
            body="""
            Dear Customer,
            
            Your account has been flagged for suspicious activity.
            Click here immediately to verify your account and password.
            
            https://fake-bank-verify.com/login
            
            Act now or your account will be closed!
            """,
        )
        print(f"Is Phishing: {result['is_phishing']}")
        print(f"Phishing Score: {result['phishing_score']:.4f}")
        print(f"Confidence: {result['confidence']:.4f}")
        print(f"Sender Risk: {result['sender_risk']:.4f}")
        print(f"Content Risk: {result['content_risk']:.4f}")
        print(f"URL Risk: {result['url_risk']:.4f}")
        print(f"Suspicious URLs: {result['suspicious_urls']}")
        print(f"Indicators: {result['indicators']}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # 7. Analyze User Login
    print("7. Analyze User Login Behavior")
    print("-" * 60)
    try:
        result = client.analyze_behavior(
            user_id="user_123",
            behavior_type="login",
            metrics={"hour": 14, "latitude": 40.7128, "longitude": -74.0060},
        )
        print(f"User ID: {result['user_id']}")
        print(f"Is Anomalous: {result['is_anomalous']}")
        print(f"Anomaly Score: {result['anomaly_score']:.4f}")
        print(f"Severity: {result['severity']}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # 8. Analyze Access Pattern
    print("8. Analyze Access Pattern")
    print("-" * 60)
    try:
        result = client.analyze_behavior(
            user_id="user_789",
            behavior_type="access_pattern",
            metrics={"count": 150, "unusual_files": 20, "failed_attempts": 10},
        )
        print(f"User ID: {result['user_id']}")
        print(f"Is Anomalous: {result['is_anomalous']}")
        print(f"Anomaly Score: {result['anomaly_score']:.4f}")
        print(f"Severity: {result['severity']}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    # 9. Get Models Status
    print("9. Get Models Status")
    print("-" * 60)
    try:
        result = client.get_models_status()
        print(json.dumps(result, indent=2, default=str))
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()

    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
