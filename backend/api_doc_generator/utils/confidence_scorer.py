"""Stage 13: Confidence Scoring - Calculate confidence scores for endpoints."""

from typing import Dict


class ConfidenceScorer:
    """Calculate confidence scores for extracted endpoints."""

    # Confidence thresholds
    HIGH_CONFIDENCE_THRESHOLD = 0.90
    MEDIUM_CONFIDENCE_THRESHOLD = 0.60
    LOW_CONFIDENCE_THRESHOLD = 0.30
    REJECTION_THRESHOLD = 0.30

    @staticmethod
    def score_endpoint(endpoint: Dict) -> float:
        """Calculate confidence score for endpoint."""
        score = 0.0

        # Route found in official routing file (strong signal)
        if endpoint.get("detection_type") == "framework_route_definition":
            score += 0.4

        # Controller resolved
        if endpoint.get("controller_resolved"):
            score += 0.3

        # Method resolved
        if endpoint.get("method"):
            score += 0.1

        # AST parsed successfully (vs regex fallback)
        if endpoint.get("ast_parsed"):
            score += 0.2

        # Request schema extracted
        if endpoint.get("request_body") and endpoint.get("request_body") != "not_detected":
            score += 0.1

        # Response schema extracted
        if endpoint.get("response_body") and endpoint.get("response_body") != "not_detected":
            score += 0.1

        # Authentication detected
        if endpoint.get("authentication") and endpoint.get("authentication") != "not_detected":
            score += 0.05

        # Normalize to 0.0-1.0 range
        return min(score, 0.99)

    @staticmethod
    def score_metadata(metadata: Dict, detection_method: str) -> float:
        """Calculate confidence score for metadata field."""
        if detection_method == "detected":
            return 0.95
        elif detection_method == "inferred":
            return 0.70
        elif detection_method == "regex_fallback":
            return 0.50
        elif detection_method == "synthetic":
            return 0.0
        else:
            return 0.50

    @staticmethod
    def classify_confidence(score: float) -> str:
        """Classify confidence level."""
        if score >= ConfidenceScorer.HIGH_CONFIDENCE_THRESHOLD:
            return "high"
        elif score >= ConfidenceScorer.MEDIUM_CONFIDENCE_THRESHOLD:
            return "medium"
        elif score >= ConfidenceScorer.LOW_CONFIDENCE_THRESHOLD:
            return "low"
        else:
            return "rejected"

    @staticmethod
    def should_reject(score: float) -> bool:
        """Determine if endpoint should be rejected."""
        return score < ConfidenceScorer.REJECTION_THRESHOLD
