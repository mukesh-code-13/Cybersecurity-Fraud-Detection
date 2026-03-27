import re
from typing import Dict, List, Tuple
import logging
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class PhishingDetector:
    """Detect phishing emails using NLP and pattern matching."""

    def __init__(self):
        """Initialize phishing detector."""
        self.phishing_keywords = self._load_keywords("config/phishing_keywords.txt")
        self.spam_keywords = self._load_keywords("config/spam_keywords.txt")
        self.suspicious_urls = set()
        self.trusted_domains = set()

    def _load_keywords(self, filepath: str) -> List[str]:
        """Load keywords from file."""
        try:
            if Path(filepath).exists():
                with open(filepath, "r") as f:
                    return [line.strip().lower() for line in f if line.strip()]
        except Exception as e:
            logger.warning(f"Could not load keywords from {filepath}: {e}")
        return []

    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text."""
        url_pattern = r"https?://[^\s]+"
        return re.findall(url_pattern, text)

    def check_domain_reputation(self, url: str) -> float:
        """
        Check reputation of domain in URL.

        Returns:
            Risk score from 0 (safe) to 1 (malicious)
        """
        try:
            domain = url.split("/")[2].lower()

            # Check against trusted domains
            if domain in self.trusted_domains:
                return 0.0

            # Check for suspicious patterns
            suspicious_patterns = [
                r"verify",
                r"confirm",
                r"update",
                r"login",
                r"secure",
                r"click",
            ]

            risk_score = 0.0
            for pattern in suspicious_patterns:
                if re.search(pattern, domain):
                    risk_score += 0.15

            # Check for homograph attacks (unicode lookalikes)
            if any(ord(c) > 127 for c in domain):
                risk_score += 0.3

            # Check for IP addresses
            ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
            if re.search(ip_pattern, domain):
                risk_score += 0.25

            return min(risk_score, 1.0)
        except Exception as e:
            logger.error(f"Error checking domain reputation: {e}")
            return 0.5

    def analyze_sender(
        self, sender_email: str, display_name: str = ""
    ) -> Tuple[bool, float]:
        """
        Analyze sender email for phishing indicators.

        Returns:
            Tuple of (is_suspicious, risk_score)
        """
        risk_score = 0.0

        # Check for spoofed domains
        if display_name and sender_email:
            display_domain = display_name.split("@")[-1] if "@" in display_name else ""
            sender_domain = sender_email.split("@")[-1]

            if display_domain and display_domain != sender_domain:
                risk_score += 0.3

        # Check for suspicious characters
        if re.search(r"[0-9]{3,}", sender_email):
            risk_score += 0.1

        # Check against known phishing patterns
        if any(
            keyword in sender_email.lower()
            for keyword in ["noreply", "no-reply", "notification"]
        ):
            risk_score += 0.15

        is_suspicious = risk_score > 0.3
        return is_suspicious, min(risk_score, 1.0)

    def analyze_content(self, subject: str, body: str) -> Tuple[bool, float]:
        """
        Analyze email content for phishing indicators.

        Returns:
            Tuple of (is_suspicious, risk_score)
        """
        content = f"{subject} {body}".lower()
        risk_score = 0.0

        # Check for urgency indicators
        urgency_indicators = [
            "urgent",
            "immediate",
            "act now",
            "verify immediately",
            "confirm now",
        ]
        for indicator in urgency_indicators:
            if indicator in content:
                risk_score += 0.1

        # Check for phishing keywords
        keyword_matches = sum(
            1 for keyword in self.phishing_keywords if keyword in content
        )
        risk_score += min(keyword_matches * 0.05, 0.3)

        # Check for requests for sensitive information
        sensitive_requests = [
            "password",
            "credit card",
            "ssn",
            "bank account",
            "verify identity",
        ]
        for request in sensitive_requests:
            if request in content:
                risk_score += 0.15

        # Check for grammatical errors
        typos = len(re.findall(r"\b[a-z]{1}\b", content))
        if typos > 3:
            risk_score += 0.1

        # Check for excessive capitalization
        caps_count = sum(1 for c in body if c.isupper())
        if caps_count > len(body) / 3:
            risk_score += 0.05

        is_suspicious = risk_score > 0.35
        return is_suspicious, min(risk_score, 1.0)

    def detect(self, email_data: Dict) -> Dict[str, any]:
        """
        Perform comprehensive phishing detection.

        Args:
            email_data: Dict with keys: subject, body, sender, display_name (optional)

        Returns:
            Dict with detection results
        """
        try:
            sender = email_data.get("sender", "")
            display_name = email_data.get("display_name", "")
            subject = email_data.get("subject", "")
            body = email_data.get("body", "")

            # Analyze different aspects
            sender_suspicious, sender_score = self.analyze_sender(sender, display_name)
            content_suspicious, content_score = self.analyze_content(subject, body)

            # Extract and check URLs
            urls = self.extract_urls(body)
            url_scores = [self.check_domain_reputation(url) for url in urls]
            url_risk = max(url_scores) if url_scores else 0.0

            # Calculate overall score
            overall_score = sender_score * 0.2 + content_score * 0.5 + url_risk * 0.3

            return {
                "is_phishing": overall_score > 0.5,
                "phishing_score": min(overall_score, 1.0),
                "confidence": min(overall_score, 1.0),
                "sender_risk": sender_score,
                "content_risk": content_score,
                "url_risk": url_risk,
                "suspicious_urls": [u for u, s in zip(urls, url_scores) if s > 0.5],
                "indicators": self._get_indicators(
                    sender_suspicious, content_suspicious, urls
                ),
            }
        except Exception as e:
            logger.error(f"Error in phishing detection: {e}")
            return {"is_phishing": False, "phishing_score": 0.0, "error": str(e)}

    def _get_indicators(
        self, sender_suspicious: bool, content_suspicious: bool, urls: List[str]
    ) -> List[str]:
        """Get list of detected phishing indicators."""
        indicators = []
        if sender_suspicious:
            indicators.append("Suspicious sender")
        if content_suspicious:
            indicators.append("Suspicious content")
        if urls:
            indicators.append(f"Contains {len(urls)} URLs")
        return indicators

    def add_trusted_domain(self, domain: str):
        """Add domain to trusted list."""
        self.trusted_domains.add(domain.lower())

    def add_suspicious_url(self, url: str):
        """Add URL to suspicious list."""
        self.suspicious_urls.add(url.lower())


class EmailValidator:
    """Validate and analyze email addresses."""

    @staticmethod
    def is_valid_format(email: str) -> bool:
        """Check if email has valid format."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def extract_domain(email: str) -> str:
        """Extract domain from email."""
        if "@" in email:
            return email.split("@")[1].lower()
        return ""

    @staticmethod
    def detect_homograph_attack(email: str) -> bool:
        """Detect homograph attacks using unicode lookalikes."""
        return any(ord(c) > 127 for c in email)

    @staticmethod
    def is_temporary_email(email: str) -> bool:
        """Check if email is from temporary email service."""
        temp_domains = [
            "tempmail",
            "throwaway",
            "10minutemail",
            "guerrillamail",
            "mailinator",
            "yopmail",
            "protonmail",
            "maildrop",
        ]
        domain = EmailValidator.extract_domain(email)
        return any(temp in domain.lower() for temp in temp_domains)

    @staticmethod
    def check_domain_age(domain: str) -> str:
        """
        Estimate domain age (would integrate with WHOIS API in production).

        Returns:
            'new', 'moderate', 'old'
        """
        # This is a placeholder - in production, use WHOIS API
        return "moderate"
