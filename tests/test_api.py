import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestHealth:
    """Test health check endpoints."""

    def test_health_check(self):
        """Test API health check."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "api_title" in response.json() or "name" in response.json()


class TestTransactionAnalysis:
    """Test transaction analysis endpoint."""

    def test_analyze_transaction_valid(self):
        """Test transaction analysis with valid data."""
        payload = {
            "user_id": "user123",
            "amount": 100.0,
            "merchant": "Amazon",
            "transaction_type": "purchase",
            "device_id": "device456",
            "ip_address": "192.168.1.1",
            "location": "New York",
        }
        response = client.post("/api/v1/transactions/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "risk_level" in data
        assert data["amount"] == 100.0

    def test_analyze_transaction_negative_amount(self):
        """Test transaction with negative amount."""
        payload = {
            "user_id": "user123",
            "amount": -100.0,
            "merchant": "Amazon",
            "transaction_type": "purchase",
        }
        response = client.post("/api/v1/transactions/analyze", json=payload)
        assert response.status_code == 422  # Validation error


class TestPhishingDetection:
    """Test phishing detection endpoint."""

    def test_detect_phishing_legitimate(self):
        """Test detection of legitimate email."""
        payload = {
            "sender": "support@amazon.com",
            "display_name": "Amazon Support",
            "subject": "Your Order Confirmation",
            "body": "Thank you for your purchase. Your order #123 has been confirmed.",
        }
        response = client.post("/api/v1/phishing/detect", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "is_phishing" in data
        assert "phishing_score" in data

    def test_detect_phishing_suspicious(self):
        """Test detection of suspicious email."""
        payload = {
            "sender": "verify@secure.com",
            "subject": "URGENT: Verify Your Account Now",
            "body": "Click here immediately to verify your account or it will be closed",
        }
        response = client.post("/api/v1/phishing/detect", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "phishing_score" in data

    def test_detect_phishing_invalid_email(self):
        """Test phishing detection with invalid email."""
        payload = {"sender": "not-an-email", "subject": "Test", "body": "Test"}
        response = client.post("/api/v1/phishing/detect", json=payload)
        assert response.status_code == 400


class TestBehaviorAnalysis:
    """Test behavior analysis endpoint."""

    def test_analyze_behavior_login(self):
        """Test login behavior analysis."""
        payload = {
            "user_id": "user123",
            "behavior_type": "login",
            "metrics": {"hour": 14, "latitude": 40.7128, "longitude": -74.0060},
        }
        response = client.post("/api/v1/behavior/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "is_anomalous" in data
        assert "anomaly_score" in data

    def test_analyze_behavior_access_pattern(self):
        """Test access pattern behavior analysis."""
        payload = {
            "user_id": "user123",
            "behavior_type": "access_pattern",
            "metrics": {"count": 100, "unusual_files": 5, "failed_attempts": 2},
        }
        response = client.post("/api/v1/behavior/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "severity" in data


class TestModelsStatus:
    """Test model status endpoint."""

    def test_get_models_status(self):
        """Test getting models status."""
        response = client.get("/api/v1/models/status")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert "anomaly_detector" in data["models"]
        assert "fraud_detector" in data["models"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
