"""
Tests for provenance validator to ensure only source-detected metadata is included.

This test suite validates that the system does NOT fabricate:
- Synthetic error responses (401, 422, etc.)
- Fake validation errors
- Generic success payloads
- Invented authentication assumptions
- Synthetic headers
- Generated testing flows
- Fabricated AI notes
"""

import pytest
from api_doc_generator.utils.provenance_validator import ProvenanceValidator


class TestProvenanceValidator:
    """Test provenance validation and synthetic content removal."""

    def test_removes_ai_notes_section(self):
        """AI notes section should be completely removed."""
        endpoint = {
            "method": "GET",
            "path": "/jobs",
            "ai_notes": {
                "request": "Uses path parameters",
                "response": "Success responses detected: 200",
                "errors": "No explicit error responses were detected",
            },
        }

        cleaned = ProvenanceValidator.remove_synthetic_ai_notes(endpoint)
        assert "ai_notes" not in cleaned
        assert "ai_enhanced" not in cleaned

    def test_removes_fabricated_401_response(self):
        """401 Unauthorized should be removed if not explicitly detected."""
        endpoint = {
            "method": "GET",
            "path": "/jobs",
            "responses": [
                {"status_code": 200, "description": "Success"},
                {"status_code": 401, "description": "Unauthorized"},  # Fabricated
            ],
        }

        cleaned = ProvenanceValidator._validate_responses(endpoint["responses"])
        assert len(cleaned) == 1
        assert cleaned[0]["status_code"] == 200

    def test_keeps_401_response_with_provenance(self):
        """401 should be kept if it has provenance."""
        endpoint = {
            "method": "GET",
            "path": "/jobs",
            "responses": [
                {"status_code": 200, "description": "Success"},
                {
                    "status_code": 401,
                    "description": "Unauthorized",
                    "detection_type": "middleware_detected",
                    "detected_from": "auth middleware",
                },
            ],
        }

        cleaned = ProvenanceValidator._validate_responses(endpoint["responses"])
        assert len(cleaned) == 2
        assert any(r["status_code"] == 401 for r in cleaned)

    def test_removes_fabricated_422_response(self):
        """422 Validation Error should be removed if not explicitly detected."""
        endpoint = {
            "method": "POST",
            "path": "/jobs",
            "responses": [
                {"status_code": 201, "description": "Created"},
                {"status_code": 422, "description": "Validation Error"},  # Fabricated
            ],
        }

        cleaned = ProvenanceValidator._validate_responses(endpoint["responses"])
        assert len(cleaned) == 1
        assert cleaned[0]["status_code"] == 201

    def test_keeps_422_response_with_provenance(self):
        """422 should be kept if it has provenance."""
        endpoint = {
            "method": "POST",
            "path": "/jobs",
            "responses": [
                {"status_code": 201, "description": "Created"},
                {
                    "status_code": 422,
                    "description": "Validation Error",
                    "detection_type": "form_request_detected",
                    "detected_from": "StoreJobRequest",
                },
            ],
        }

        cleaned = ProvenanceValidator._validate_responses(endpoint["responses"])
        assert len(cleaned) == 2
        assert any(r["status_code"] == 422 for r in cleaned)

    def test_removes_synthetic_content_type_header(self):
        """Content-Type header should be removed (synthetic recommendation)."""
        endpoint = {
            "method": "POST",
            "path": "/jobs",
            "headers": [
                {"name": "Content-Type", "value": "application/json"},
                {"name": "Authorization", "value": "Bearer token", "detection_type": "middleware"},
            ],
        }

        cleaned = ProvenanceValidator._validate_headers(endpoint["headers"])
        assert len(cleaned) == 1
        assert cleaned[0]["name"] == "Authorization"

    def test_removes_headers_without_provenance(self):
        """Headers without provenance should be removed."""
        endpoint = {
            "method": "GET",
            "path": "/jobs",
            "headers": [
                {"name": "X-Custom-Header"},  # No provenance
                {"name": "X-Detected", "detection_type": "middleware"},  # Has provenance
            ],
        }

        cleaned = ProvenanceValidator._validate_headers(endpoint["headers"])
        assert len(cleaned) == 1
        assert cleaned[0]["name"] == "X-Detected"

    def test_removes_generic_description(self):
        """Generic descriptions should be removed."""
        endpoint = {
            "method": "GET",
            "path": "/jobs",
            "description": "GET /jobs is handled by JobController@index and was extracted from routes/api.php",
        }

        cleaned = ProvenanceValidator.validate_endpoint(endpoint)
        # Generic description should be removed
        assert "description" not in cleaned or cleaned.get("description") == ""

    def test_removes_testing_flow_section(self):
        """Testing flow section should be completely removed."""
        endpoint = {
            "method": "GET",
            "path": "/jobs",
            "testing_flow": "Start with a detected read endpoint...",
        }

        cleaned = ProvenanceValidator.remove_generic_sections(endpoint)
        assert "testing_flow" not in cleaned

    def test_removes_changelog_section(self):
        """Changelog section should be completely removed."""
        endpoint = {
            "method": "GET",
            "path": "/jobs",
            "changelog": "Initial generated documentation",
        }

        cleaned = ProvenanceValidator.remove_generic_sections(endpoint)
        assert "changelog" not in cleaned

    def test_removes_request_body_without_provenance(self):
        """Request body without provenance should be removed."""
        endpoint = {
            "method": "POST",
            "path": "/jobs",
            "request_body": {
                "schema": {"type": "object", "properties": {}},
                # No provenance
            },
        }

        cleaned = ProvenanceValidator._validate_request_body(endpoint["request_body"])
        assert cleaned is None

    def test_keeps_request_body_with_provenance(self):
        """Request body with provenance should be kept."""
        endpoint = {
            "method": "POST",
            "path": "/jobs",
            "request_body": {
                "schema": {"type": "object", "properties": {}},
                "detection_type": "form_request",
                "detected_from": "StoreJobRequest",
            },
        }

        cleaned = ProvenanceValidator._validate_request_body(endpoint["request_body"])
        assert cleaned is not None
        assert cleaned["detection_type"] == "form_request"

    def test_removes_security_without_provenance(self):
        """Security/auth without provenance should be removed."""
        endpoint = {
            "method": "GET",
            "path": "/jobs",
            "security": [
                {"tokenAuth": []},  # No provenance
            ],
        }

        cleaned = ProvenanceValidator._validate_security(endpoint["security"])
        assert len(cleaned) == 0

    def test_keeps_security_with_provenance(self):
        """Security/auth with provenance should be kept."""
        endpoint = {
            "method": "GET",
            "path": "/jobs",
            "security": [
                {
                    "tokenAuth": [],
                    "detection_type": "middleware",
                    "detected_from": "auth middleware",
                },
            ],
        }

        cleaned = ProvenanceValidator._validate_security(endpoint["security"])
        assert len(cleaned) == 1

    def test_adds_detection_metadata(self):
        """Detection metadata should be added if missing."""
        endpoint = {
            "method": "GET",
            "path": "/jobs",
        }

        cleaned = ProvenanceValidator.ensure_detection_metadata(endpoint)
        assert "detection_type" in cleaned
        assert "source_file" in cleaned
        assert "confidence" in cleaned

    def test_adds_not_detected_markers(self):
        """Not detected markers should be added for missing metadata."""
        endpoint = {
            "method": "POST",
            "path": "/jobs",
            "request_body": None,
            "security": None,
            "query_params": None,
        }

        cleaned = ProvenanceValidator.add_not_detected_markers(endpoint)
        assert cleaned.get("request_body_detected") is False
        assert cleaned.get("authentication_detected") is False
        assert cleaned.get("query_params_detected") is False

    def test_complete_validation_pipeline(self):
        """Test complete validation and cleaning pipeline."""
        endpoint = {
            "method": "POST",
            "path": "/jobs",
            "summary": "Create jobs",
            "responses": [
                {"status_code": 201, "description": "Created"},
                {"status_code": 401, "description": "Unauthorized"},  # Fabricated
                {"status_code": 422, "description": "Validation Error"},  # Fabricated
            ],
            "headers": [
                {"name": "Content-Type"},  # Synthetic
            ],
            "ai_notes": {
                "request": "Synthetic",
                "response": "Synthetic",
            },
            "testing_flow": "Generic guidance",
            "changelog": "Invented",
        }

        cleaned = ProvenanceValidator.validate_and_clean(endpoint)

        # Verify synthetic content is removed
        assert "ai_notes" not in cleaned
        assert "testing_flow" not in cleaned
        assert "changelog" not in cleaned

        # Verify fabricated responses are removed
        assert len(cleaned["responses"]) == 1
        assert cleaned["responses"][0]["status_code"] == 201

        # Verify synthetic headers are removed
        assert len(cleaned.get("headers", [])) == 0

        # Verify detection metadata is added
        assert "detection_type" in cleaned
        assert "source_file" in cleaned

    def test_critical_issue_no_synthetic_401(self):
        """
        CRITICAL TEST: 401 Unauthorized should NOT be fabricated.
        
        This was a major issue where every endpoint with auth
        got a synthetic 401 response without evidence.
        """
        endpoint = {
            "method": "GET",
            "path": "/v1/ips",
            "x-authentication": ["jwt"],  # Auth detected
            "responses": [
                {"status_code": 200, "description": "Success"},
                # System was adding this fabricated 401
                {"status_code": 401, "description": "Unauthorized"},
            ],
        }

        # Validate responses - should remove the fabricated 401
        cleaned_responses = ProvenanceValidator._validate_responses(endpoint["responses"])

        # Should only have the 200 response
        assert len(cleaned_responses) == 1
        assert cleaned_responses[0]["status_code"] == 200

    def test_critical_issue_no_synthetic_422(self):
        """
        CRITICAL TEST: 422 Validation Error should NOT be fabricated.
        
        This was a major issue where POST/PUT/PATCH endpoints
        got synthetic 422 responses without evidence.
        """
        endpoint = {
            "method": "POST",
            "path": "/jobs",
            "responses": [
                {"status_code": 201, "description": "Created"},
                # System was adding this fabricated 422
                {"status_code": 422, "description": "Validation Error"},
            ],
        }

        # Validate responses - should remove the fabricated 422
        cleaned_responses = ProvenanceValidator._validate_responses(endpoint["responses"])

        # Should only have the 201 response
        assert len(cleaned_responses) == 1
        assert cleaned_responses[0]["status_code"] == 201

    def test_critical_issue_no_synthetic_ai_notes(self):
        """
        CRITICAL TEST: AI notes section should be completely removed.
        
        This section contains:
        - Generated interpretations
        - Inferred patterns
        - Semi-hallucinatory content
        """
        endpoint = {
            "method": "GET",
            "path": "/jobs",
            "ai_notes": {
                "request": "Uses path parameters",
                "response": "Success responses detected: 200",
                "errors": "No explicit error responses were detected",
            },
        }

        cleaned = ProvenanceValidator.remove_synthetic_ai_notes(endpoint)

        # AI notes should be completely gone
        assert "ai_notes" not in cleaned
        assert "ai_enhanced" not in cleaned


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
