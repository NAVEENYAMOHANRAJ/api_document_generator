"""
Provenance validator to ensure only source-detected metadata is included.

This module enforces the principle: "source-grounded deterministic documentation"
- NO synthetic error responses
- NO fabricated validation errors
- NO generic success payloads
- NO invented authentication assumptions
- NO synthetic headers
- NO generated testing flows
- NO fabricated AI notes

Only include metadata that was explicitly detected from source code.
"""

from typing import Dict, List, Any, Optional


class ProvenanceValidator:
    """Validate that endpoint metadata comes from source code, not fabrication."""

    # Metadata that should NEVER be fabricated
    FORBIDDEN_SYNTHETIC_FIELDS = {
        "ai_notes",  # Generated interpretations
        "testing_flow",  # Generic guidance
        "changelog",  # Invented metadata
        "generic_headers",  # Synthetic recommendations
    }

    # Response codes that should ONLY be included if explicitly detected
    DANGEROUS_RESPONSE_CODES = {
        401: "Unauthorized",  # Only if auth middleware/decorator detected
        403: "Forbidden",  # Only if permission check detected
        422: "Unprocessable Entity",  # Only if validation detected
        500: "Internal Server Error",  # Only if error handling detected
    }

    @classmethod
    def validate_endpoint(cls, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean endpoint metadata.
        
        Removes all synthetic/fabricated fields and ensures only
        source-detected metadata remains.
        """
        # Remove forbidden synthetic fields
        for field in cls.FORBIDDEN_SYNTHETIC_FIELDS:
            endpoint.pop(field, None)

        # Validate responses - remove fabricated error codes
        endpoint["responses"] = cls._validate_responses(endpoint.get("responses", []))

        # Validate request body - ensure it's source-detected
        endpoint["request_body"] = cls._validate_request_body(endpoint.get("request_body"))

        # Validate headers - remove synthetic recommendations
        endpoint["headers"] = cls._validate_headers(endpoint.get("headers", []))

        # Validate authentication - ensure it has provenance
        endpoint["security"] = cls._validate_security(endpoint.get("security", []))

        # Remove generic descriptions
        if cls._is_generic_description(endpoint.get("description", "")):
            endpoint.pop("description", None)

        return endpoint

    @classmethod
    def _validate_responses(cls, responses: List[Dict]) -> List[Dict]:
        """
        Validate response codes.
        
        Rules:
        - Keep 2xx success codes (these are defaults)
        - Remove 401/403/422/500 unless they have provenance
        - Keep only responses with explicit detection
        """
        validated = []

        for response in responses:
            status_code = response.get("status_code")

            # Keep success responses (2xx)
            if 200 <= status_code < 300:
                validated.append(response)
                continue

            # Check if dangerous code has provenance
            if status_code in cls.DANGEROUS_RESPONSE_CODES:
                # Only keep if it has detection source
                if cls._has_provenance(response):
                    validated.append(response)
                # Otherwise skip - it's fabricated
                continue

            # Keep other error codes if they have provenance
            if cls._has_provenance(response):
                validated.append(response)

        return validated

    @classmethod
    def _validate_request_body(cls, request_body: Optional[Dict]) -> Optional[Dict]:
        """
        Validate request body.
        
        Rules:
        - If not detected, return None (not "not_detected" string)
        - If detected, must have provenance
        - Remove synthetic schema examples
        """
        if not request_body:
            return None

        # If it's a string like "not_detected", return None
        if isinstance(request_body, str):
            return None

        # If it has provenance, keep it
        if cls._has_provenance(request_body):
            return request_body

        # Otherwise it's synthetic, remove it
        return None

    @classmethod
    def _validate_headers(cls, headers: List[Dict]) -> List[Dict]:
        """
        Validate headers.
        
        Rules:
        - Remove Content-Type (synthetic recommendation)
        - Keep only headers with explicit detection
        - Remove generic headers
        """
        validated = []

        for header in headers:
            name = header.get("name", "").lower()

            # Remove synthetic headers
            if name in {"content-type", "accept", "user-agent"}:
                continue

            # Keep only if has provenance
            if cls._has_provenance(header):
                validated.append(header)

        return validated

    @classmethod
    def _validate_security(cls, security: List[Dict]) -> List[Dict]:
        """
        Validate security/authentication.
        
        Rules:
        - Remove if no provenance
        - Must show detection source
        - No invented auth assumptions
        """
        validated = []

        for auth in security:
            # Only keep if has provenance
            if cls._has_provenance(auth):
                validated.append(auth)

        return validated

    @classmethod
    def _has_provenance(cls, metadata: Dict) -> bool:
        """
        Check if metadata has provenance information.
        
        Provenance fields:
        - detection_type: How it was detected
        - source_file: Where it came from
        - line_number: Specific location
        - detected_from: What code pattern
        """
        provenance_fields = {
            "detection_type",
            "source_file",
            "line_number",
            "detected_from",
            "provenance",
        }

        return any(field in metadata for field in provenance_fields)

    @classmethod
    def _is_generic_description(cls, description: str) -> bool:
        """
        Check if description is generic/synthetic.
        
        Generic patterns:
        - "is handled by"
        - "was extracted from"
        - Generic success messages
        """
        if not description:
            return False

        generic_patterns = [
            "is handled by",
            "was extracted from",
            "Success",
            "Generic",
            "Unknown",
        ]

        return any(pattern in description for pattern in generic_patterns)

    @classmethod
    def remove_synthetic_ai_notes(cls, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove AI-generated notes section entirely.
        
        The ai_notes section contains:
        - Generated interpretations
        - Inferred patterns
        - Semi-hallucinatory content
        
        This should not exist in source-grounded documentation.
        """
        endpoint.pop("ai_notes", None)
        endpoint.pop("ai_enhanced", None)
        return endpoint

    @classmethod
    def remove_generic_sections(cls, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove generic/fabricated sections.
        
        Sections to remove:
        - testing_flow: Generic guidance
        - changelog: Invented metadata
        - generic_headers: Synthetic recommendations
        """
        sections_to_remove = [
            "testing_flow",
            "changelog",
            "generic_headers",
            "generic_notes",
            "generated_examples",
        ]

        for section in sections_to_remove:
            endpoint.pop(section, None)

        return endpoint

    @classmethod
    def ensure_detection_metadata(cls, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure endpoint has detection metadata.
        
        Required fields:
        - detection_type: How the endpoint was detected
        - source_file: Where it came from
        - confidence: How confident we are
        """
        if "detection_type" not in endpoint:
            endpoint["detection_type"] = "unknown"

        if "source_file" not in endpoint:
            endpoint["source_file"] = "unknown"

        if "confidence" not in endpoint:
            endpoint["confidence"] = 0.0

        return endpoint

    @classmethod
    def add_not_detected_markers(cls, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add explicit "not_detected" markers for missing metadata.
        
        Instead of fabricating or omitting, explicitly mark what wasn't detected.
        """
        # If no request body detected, mark it
        if not endpoint.get("request_body"):
            endpoint["request_body_detected"] = False

        # If no authentication detected, mark it
        if not endpoint.get("security"):
            endpoint["authentication_detected"] = False

        # If no query params detected, mark it
        if not endpoint.get("query_params"):
            endpoint["query_params_detected"] = False

        return endpoint

    @classmethod
    def validate_and_clean(cls, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete validation and cleaning pipeline.
        
        1. Remove synthetic fields
        2. Validate responses
        3. Validate request body
        4. Validate headers
        5. Validate security
        6. Remove generic sections
        7. Add detection metadata
        8. Add not_detected markers
        """
        # Step 1: Remove synthetic fields
        endpoint = cls.validate_endpoint(endpoint)

        # Step 2: Remove AI notes
        endpoint = cls.remove_synthetic_ai_notes(endpoint)

        # Step 3: Remove generic sections
        endpoint = cls.remove_generic_sections(endpoint)

        # Step 4: Ensure detection metadata
        endpoint = cls.ensure_detection_metadata(endpoint)

        # Step 5: Add not_detected markers
        endpoint = cls.add_not_detected_markers(endpoint)

        return endpoint
