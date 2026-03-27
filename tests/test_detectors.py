import pytest
import numpy as np
from src.detectors import AnomalyDetector, FraudDetector, BehavioralAnalyzer
from src.phishing_detector import PhishingDetector, EmailValidator


class TestAnomalyDetector:
    """Test anomaly detection module."""

    @pytest.fixture
    def detector(self):
        return AnomalyDetector(contamination=0.1)

    def test_predict_normal_transaction(self, detector):
        """Test prediction on normal transaction."""
        transaction = {
            "amount": 100.0,
            "hour_of_day": 14,
            "days_since_last_transaction": 1,
            "transaction_count_today": 2,
            "avg_transaction_amount": 95.0,
        }
        is_anomaly, score = detector.predict(transaction)
        assert isinstance(is_anomaly, bool)
        assert 0.0 <= score <= 1.0

    def test_predict_suspicious_transaction(self, detector):
        """Test prediction on suspicious transaction."""
        transaction = {
            "amount": 5000.0,
            "hour_of_day": 3,
            "days_since_last_transaction": 30,
            "transaction_count_today": 10,
            "avg_transaction_amount": 50.0,
        }
        is_anomaly, score = detector.predict(transaction)
        assert isinstance(is_anomaly, bool)
        assert 0.0 <= score <= 1.0


class TestFraudDetector:
    """Test fraud detection module."""

    @pytest.fixture
    def detector(self):
        return FraudDetector()

    def test_predict_legitimate_transaction(self, detector):
        """Test prediction on legitimate transaction."""
        transaction = {
            "amount": 50.0,
            "is_foreign": 0,
            "is_weekend": False,
            "time_since_last_transaction": 3600,
            "merchant_risk_score": 0.1,
            "velocity_score": 0.2,
            "device_is_new": 0,
            "location_change_km": 5,
        }
        is_fraud, score = detector.predict(transaction)
        assert isinstance(is_fraud, bool)
        assert 0.0 <= score <= 1.0

    def test_predict_fraudulent_transaction(self, detector):
        """Test prediction on fraudulent transaction."""
        transaction = {
            "amount": 10000.0,
            "is_foreign": 1,
            "is_weekend": True,
            "time_since_last_transaction": 60,
            "merchant_risk_score": 0.8,
            "velocity_score": 0.9,
            "device_is_new": 1,
            "location_change_km": 5000,
        }
        is_fraud, score = detector.predict(transaction)
        assert isinstance(is_fraud, bool)
        assert 0.0 <= score <= 1.0

    def test_feature_importance(self, detector):
        """Test feature importance extraction."""
        importance = detector.get_feature_importance()
        assert isinstance(importance, dict)
        assert len(importance) == 8


class TestBehavioralAnalyzer:
    """Test behavioral analysis module."""

    @pytest.fixture
    def analyzer(self):
        return BehavioralAnalyzer()

    def test_update_baseline(self, analyzer):
        """Test updating user baseline."""
        user_id = "user123"
        metrics = {"login_hour": 14, "login_count_daily": 2}
        analyzer.update_baseline(user_id, metrics)

        assert user_id in analyzer.user_baselines
        assert analyzer.user_baselines[user_id]["login_hour"] == 14

    def test_analyze_behavior_no_baseline(self, analyzer):
        """Test behavior analysis without baseline."""
        user_id = "new_user"
        metrics = {"login_hour": 10}
        score, details = analyzer.analyze_behavior(user_id, metrics)
        assert score == 0.0
        assert details["status"] == "no_baseline"

    def test_detect_login_anomaly(self, analyzer):
        """Test login anomaly detection."""
        user_id = "user123"
        analyzer.update_baseline(user_id, {"login_hour": 14})

        login_data = {"hour": 3, "latitude": 40.7, "longitude": -74.0}
        is_anomalous, score = analyzer.detect_login_anomaly(user_id, login_data)

        assert isinstance(is_anomalous, bool)
        assert 0.0 <= score <= 1.0


class TestPhishingDetector:
    """Test phishing detection module."""

    @pytest.fixture
    def detector(self):
        return PhishingDetector()

    def test_extract_urls(self, detector):
        """Test URL extraction from text."""
        text = "Visit https://example.com or http://test.org"
        urls = detector.extract_urls(text)
        assert len(urls) == 2
        assert "https://example.com" in urls

    def test_check_domain_reputation_suspicious(self, detector):
        """Test domain reputation check for suspicious domain."""
        url = "https://verify-account.com"
        score = detector.check_domain_reputation(url)
        assert 0.0 <= score <= 1.0

    def test_analyze_sender_legitimate(self, detector):
        """Test sender analysis for legitimate sender."""
        sender = "support@amazon.com"
        is_suspicious, score = detector.analyze_sender(sender)
        assert isinstance(is_suspicious, bool)
        assert 0.0 <= score <= 1.0

    def test_analyze_content_phishing(self, detector):
        """Test content analysis for phishing indicators."""
        subject = "Urgent: Verify Your Account"
        body = "Click here immediately to confirm your password"
        is_suspicious, score = detector.analyze_content(subject, body)
        assert isinstance(is_suspicious, bool)
        assert score > 0.3  # Should have moderate phishing score

    def test_detect_full_email(self, detector):
        """Test full email phishing detection."""
        email_data = {
            "sender": "verify@secure.com",
            "display_name": "Amazon",
            "subject": "Verify Your Account Now",
            "body": "Click here to verify your password immediately",
        }
        result = detector.detect(email_data)
        assert "is_phishing" in result
        assert "phishing_score" in result
        assert "confidence" in result


class TestEmailValidator:
    """Test email validation utilities."""

    def test_valid_email_format(self):
        """Test valid email format."""
        assert EmailValidator.is_valid_format("user@example.com") is True
        assert EmailValidator.is_valid_format("invalid.email") is False

    def test_extract_domain(self):
        """Test domain extraction."""
        domain = EmailValidator.extract_domain("user@example.com")
        assert domain == "example.com"

    def test_detect_homograph_attack(self):
        """Test homograph attack detection."""
        assert EmailValidator.detect_homograph_attack("user@exаmple.com") is True
        assert EmailValidator.detect_homograph_attack("user@example.com") is False

    def test_is_temporary_email(self):
        """Test temporary email detection."""
        assert EmailValidator.is_temporary_email("user@tempmail.com") is True
        assert EmailValidator.is_temporary_email("user@example.com") is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
