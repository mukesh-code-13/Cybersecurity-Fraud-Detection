import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib
from typing import Dict, List, Tuple, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Detect anomalies in user transactions and network behavior."""

    def __init__(self, contamination: float = 0.1, model_path: str = None):
        """Initialize anomaly detector with Isolation Forest."""
        self.contamination = contamination
        self.model_path = model_path or "models/isolation_forest.pkl"
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=5)
        self.model = IsolationForest(
            contamination=contamination, random_state=42, n_jobs=-1
        )
        self.feature_names = None
        self._load_model()

    def _load_model(self):
        """Load pre-trained model if exists."""
        try:
            if Path(self.model_path).exists():
                saved = joblib.load(self.model_path)
                self.model = saved.get("model", self.model)
                self.scaler = saved.get("scaler", self.scaler)
                logger.info(f"Loaded anomaly detection model from {self.model_path}")
        except Exception as e:
            logger.warning(f"Could not load model: {e}")

    def extract_features(self, transaction_data: Dict) -> np.ndarray:
        """Extract numerical features from transaction data."""
        features = np.array(
            [
                transaction_data.get("amount", 0),
                transaction_data.get("hour_of_day", 0),
                transaction_data.get("days_since_last_transaction", 0),
                transaction_data.get("transaction_count_today", 0),
                transaction_data.get("avg_transaction_amount", 0),
            ]
        )
        return features.reshape(1, -1)

    def predict(self, transaction_data: Dict) -> Tuple[bool, float]:
        """
        Detect if a transaction is anomalous.

        Returns:
            Tuple of (is_anomaly, anomaly_score)
        """
        try:
            features = self.extract_features(transaction_data)
            features_scaled = self.scaler.fit_transform(features)

            # Get anomaly score (-1 for outliers, 1 for inliers)
            prediction = self.model.predict(features_scaled)[0]
            score = abs(self.model.score_samples(features_scaled)[0])

            is_anomaly = prediction == -1
            return is_anomaly, min(score, 1.0)
        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
            return False, 0.0

    def train(self, X: np.ndarray):
        """Train the anomaly detection model."""
        try:
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled)
            self.save_model()
            logger.info("Anomaly detection model trained successfully")
        except Exception as e:
            logger.error(f"Error training anomaly detector: {e}")

    def save_model(self):
        """Save model to disk."""
        try:
            Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)
            joblib.dump({"model": self.model, "scaler": self.scaler}, self.model_path)
            logger.info(f"Anomaly detection model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")


class FraudDetector:
    """Detect fraudulent transactions using Random Forest classifier."""

    def __init__(self, model_path: str = None):
        """Initialize fraud detector."""
        self.model_path = model_path or "models/fraud_detector.pkl"
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced",
        )
        self._load_model()

    def _load_model(self):
        """Load pre-trained model if exists."""
        try:
            if Path(self.model_path).exists():
                saved = joblib.load(self.model_path)
                self.model = saved.get("model", self.model)
                self.scaler = saved.get("scaler", self.scaler)
                logger.info(f"Loaded fraud detection model from {self.model_path}")
        except Exception as e:
            logger.warning(f"Could not load model: {e}")

    def extract_features(self, transaction_data: Dict) -> np.ndarray:
        """Extract features for fraud detection."""
        features = np.array(
            [
                transaction_data.get("amount", 0),
                transaction_data.get("is_foreign", 0),
                transaction_data.get("is_weekend", 0),
                transaction_data.get("time_since_last_transaction", 0),
                transaction_data.get("merchant_risk_score", 0),
                transaction_data.get("velocity_score", 0),
                transaction_data.get("device_is_new", 0),
                transaction_data.get("location_change_km", 0),
            ]
        )
        return features.reshape(1, -1)

    def predict(self, transaction_data: Dict) -> Tuple[bool, float]:
        """
        Detect if a transaction is fraudulent.

        Returns:
            Tuple of (is_fraud, fraud_score)
        """
        try:
            features = self.extract_features(transaction_data)
            features_scaled = self.scaler.fit_transform(features)

            prediction = self.model.predict(features_scaled)[0]
            proba = self.model.predict_proba(features_scaled)[0]
            fraud_score = proba[1]  # Probability of fraud class

            is_fraud = prediction == 1
            return is_fraud, fraud_score
        except Exception as e:
            logger.error(f"Error in fraud detection: {e}")
            return False, 0.0

    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the fraud detection model."""
        try:
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled, y)
            self.save_model()
            logger.info("Fraud detection model trained successfully")
        except Exception as e:
            logger.error(f"Error training fraud detector: {e}")

    def save_model(self):
        """Save model to disk."""
        try:
            Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)
            joblib.dump({"model": self.model, "scaler": self.scaler}, self.model_path)
            logger.info(f"Fraud detection model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")

    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores."""
        feature_names = [
            "amount",
            "is_foreign",
            "is_weekend",
            "time_since_last_transaction",
            "merchant_risk_score",
            "velocity_score",
            "device_is_new",
            "location_change_km",
        ]
        importance = dict(zip(feature_names, self.model.feature_importances_))
        return {
            k: v
            for k, v in sorted(importance.items(), key=lambda x: x[1], reverse=True)
        }


class BehavioralAnalyzer:
    """Analyze user behavioral patterns for anomalies."""

    def __init__(self):
        """Initialize behavioral analyzer."""
        self.user_baselines = {}

    def update_baseline(self, user_id: str, metrics: Dict[str, float]):
        """Update baseline metrics for a user."""
        if user_id not in self.user_baselines:
            self.user_baselines[user_id] = {}

        self.user_baselines[user_id].update(metrics)

    def analyze_behavior(
        self, user_id: str, current_metrics: Dict[str, float]
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Analyze current behavior against baseline.

        Returns:
            Tuple of (behavior_score, analysis_details)
        """
        if user_id not in self.user_baselines:
            return 0.0, {"status": "no_baseline"}

        baseline = self.user_baselines[user_id]
        deviations = {}
        anomaly_score = 0.0

        for metric, current_value in current_metrics.items():
            if metric in baseline:
                baseline_value = baseline[metric]
                if baseline_value > 0:
                    deviation = abs(current_value - baseline_value) / baseline_value
                    deviations[metric] = deviation
                    anomaly_score += deviation

        anomaly_score = min(anomaly_score / len(deviations) if deviations else 0, 1.0)

        return anomaly_score, {
            "deviations": deviations,
            "severity": (
                "high"
                if anomaly_score > 0.7
                else "medium" if anomaly_score > 0.4 else "low"
            ),
        }

    def detect_login_anomaly(
        self, user_id: str, login_data: Dict
    ) -> Tuple[bool, float]:
        """Detect anomalous login attempts."""
        metrics = {
            "login_hour": login_data.get("hour", 0),
            "login_location_lat": login_data.get("latitude", 0),
            "login_location_lon": login_data.get("longitude", 0),
        }

        score, _ = self.analyze_behavior(user_id, metrics)
        is_anomalous = score > 0.6

        return is_anomalous, score

    def detect_access_pattern_anomaly(
        self, user_id: str, access_data: Dict
    ) -> Tuple[bool, float]:
        """Detect anomalies in resource access patterns."""
        metrics = {
            "resource_access_count": access_data.get("count", 0),
            "unusual_file_access": access_data.get("unusual_files", 0),
            "failed_attempts": access_data.get("failed_attempts", 0),
        }

        score, _ = self.analyze_behavior(user_id, metrics)
        is_anomalous = score > 0.65

        return is_anomalous, score
