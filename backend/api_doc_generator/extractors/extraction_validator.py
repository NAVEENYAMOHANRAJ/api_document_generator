"""
Extraction Validator - Ensures all required metadata is extracted.

Validates that the extraction system captures all details shown in the sample:
- Request headers (Authorization, Accept, etc.)
- Query parameters with types and descriptions
- Request body with field types and descriptions
- Response schemas with field types and descriptions
- Status codes with descriptions
- Authentication methods
- Middleware
- Tags and categories
- Rate limits
- Response examples
"""

from typing import Dict, List, Any, Optional, Tuple
import re


class ExtractionValidator:
    """Validate that all required metadata is extracted from endpoints."""

    # Required fields for complete endpoint documentation
    REQUIRED_FIELDS = {
        "method": "HTTP method (GET, POST, etc.)",
        "path": "Route path",
        "handler": "Controller and method",
        "summary": "Brief description",
        "description": "Detailed description",
    }

    # Optional but important fields
    IMPORTANT_FIELDS = {
        "requestBody": "Request body schema",
        "responses": "Response schemas",
        "statusCodes": "HTTP status codes",
        "security": "Authentication requirements",
        "pathParameters": "Path parameters",
        "queryParameters": "Query parameters",
        "headers": "Request headers",
        "tags": "Endpoint tags/categories",
        "middleware": "Applied middleware",
        "rateLimit": "Rate limiting info",
        "examples": "Request/response examples",
    }

    def __init__(self):
        self.validation_results = []
        self.missing_fields = []
        self.coverage_score = 0.0

    def validate_endpoint(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single endpoint for completeness.
        
        Returns:
            Validation report with coverage score and missing fields
        """
        report = {
            "endpoint": f"{endpoint.get('method')} {endpoint.get('path')}",
            "required_fields_present": [],
            "required_fields_missing": [],
            "important_fields_present": [],
            "important_fields_missing": [],
            "coverage_score": 0.0,
            "issues": [],
            "recommendations": []
        }

        # Check required fields
        for field, description in self.REQUIRED_FIELDS.items():
            if field in endpoint and endpoint[field]:
                report["required_fields_present"].append(field)
            else:
                report["required_fields_missing"].append(field)
                report["issues"].append(f"Missing required field: {field}")

        # Check important fields
        for field, description in self.IMPORTANT_FIELDS.items():
            if field in endpoint and endpoint[field]:
                report["important_fields_present"].append(field)
            else:
                report["important_fields_missing"].append(field)

        # Calculate coverage score
        required_present = len(report["required_fields_present"])
        required_total = len(self.REQUIRED_FIELDS)
        important_present = len(report["important_fields_present"])
        important_total = len(self.IMPORTANT_FIELDS)

        required_score = (required_present / required_total) * 100 if required_total > 0 else 0
        important_score = (important_present / important_total) * 100 if important_total > 0 else 0

        # Weighted: 70% required, 30% important
        report["coverage_score"] = (required_score * 0.7) + (important_score * 0.3)

        # Add recommendations
        if "requestBody" not in endpoint or not endpoint.get("requestBody"):
            if endpoint.get("method") in ["POST", "PUT", "PATCH"]:
                report["recommendations"].append(
                    "Add request body schema (FormRequest class or validation rules)"
                )

        if "responses" not in endpoint or not endpoint.get("responses"):
            report["recommendations"].append(
                "Add response schema (Resource class or response statement)"
            )

        if "statusCodes" not in endpoint or not endpoint.get("statusCodes"):
            report["recommendations"].append(
                "Add explicit status codes to response statements"
            )

        if "security" not in endpoint or not endpoint.get("security"):
            if endpoint.get("middleware") and "auth" in str(endpoint.get("middleware")):
                report["recommendations"].append(
                    "Authentication detected in middleware but not extracted"
                )

        return report

    def validate_request_body(self, request_body: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate request body schema completeness.
        
        Should include:
        - type (object, array, etc.)
        - properties (field definitions)
        - required (required fields)
        - Each property should have:
          - type
          - description
          - constraints (min, max, pattern, etc.)
        """
        report = {
            "has_type": False,
            "has_properties": False,
            "has_required": False,
            "property_count": 0,
            "properties_with_description": 0,
            "properties_with_constraints": 0,
            "issues": [],
            "score": 0.0
        }

        if not request_body:
            report["issues"].append("Request body not detected")
            return report

        # Check type
        if "type" in request_body:
            report["has_type"] = True
        else:
            report["issues"].append("Missing 'type' field")

        # Check properties
        properties = request_body.get("properties", {})
        if properties:
            report["has_properties"] = True
            report["property_count"] = len(properties)

            # Check each property
            for prop_name, prop_schema in properties.items():
                if "description" in prop_schema:
                    report["properties_with_description"] += 1

                # Check for constraints
                has_constraints = any(
                    key in prop_schema
                    for key in ["minimum", "maximum", "minLength", "maxLength", "pattern", "enum", "format"]
                )
                if has_constraints:
                    report["properties_with_constraints"] += 1

        # Check required
        if "required" in request_body:
            report["has_required"] = True

        # Calculate score
        score = 0
        if report["has_type"]:
            score += 25
        if report["has_properties"]:
            score += 25
        if report["has_required"]:
            score += 25
        if report["property_count"] > 0:
            desc_ratio = report["properties_with_description"] / report["property_count"]
            score += 25 * desc_ratio

        report["score"] = score

        return report

    def validate_response_schema(self, responses: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate response schema completeness.
        
        Should include:
        - Multiple status codes (200, 201, 400, 404, 422, 500, etc.)
        - Each response should have:
          - description
          - schema/type
          - example
        """
        report = {
            "has_responses": False,
            "status_code_count": 0,
            "status_codes": [],
            "responses_with_description": 0,
            "responses_with_schema": 0,
            "responses_with_example": 0,
            "issues": [],
            "score": 0.0
        }

        if not responses:
            report["issues"].append("Response schema not detected")
            return report

        report["has_responses"] = True
        report["status_code_count"] = len(responses)
        report["status_codes"] = list(responses.keys())

        # Check each response
        for status_code, response_schema in responses.items():
            if "description" in response_schema:
                report["responses_with_description"] += 1
            else:
                report["issues"].append(f"Status {status_code}: Missing description")

            if "schema" in response_schema or "type" in response_schema:
                report["responses_with_schema"] += 1
            else:
                report["issues"].append(f"Status {status_code}: Missing schema")

            if "example" in response_schema:
                report["responses_with_example"] += 1

        # Calculate score
        score = 0
        if report["has_responses"]:
            score += 25
        if report["status_code_count"] >= 2:
            score += 25
        if report["responses_with_description"] > 0:
            score += 25 * (report["responses_with_description"] / report["status_code_count"])
        if report["responses_with_schema"] > 0:
            score += 25 * (report["responses_with_schema"] / report["status_code_count"])

        report["score"] = score

        return report

    def validate_parameters(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate parameter extraction.
        
        Should include:
        - Path parameters with types and descriptions
        - Query parameters with types, descriptions, and required flag
        - Headers with descriptions
        """
        report = {
            "path_parameters": [],
            "query_parameters": [],
            "headers": [],
            "total_parameters": 0,
            "parameters_with_description": 0,
            "parameters_with_type": 0,
            "issues": [],
            "score": 0.0
        }

        # Check path parameters
        path_params = endpoint.get("pathParameters", [])
        if path_params:
            report["path_parameters"] = len(path_params)
            report["total_parameters"] += len(path_params)
            for param in path_params:
                if "description" in param:
                    report["parameters_with_description"] += 1
                if "type" in param:
                    report["parameters_with_type"] += 1

        # Check query parameters
        query_params = endpoint.get("queryParameters", [])
        if query_params:
            report["query_parameters"] = len(query_params)
            report["total_parameters"] += len(query_params)
            for param in query_params:
                if "description" in param:
                    report["parameters_with_description"] += 1
                if "type" in param:
                    report["parameters_with_type"] += 1

        # Check headers
        headers = endpoint.get("headers", [])
        if headers:
            report["headers"] = len(headers)
            report["total_parameters"] += len(headers)

        # Calculate score
        if report["total_parameters"] > 0:
            report["score"] = (report["parameters_with_description"] / report["total_parameters"]) * 50
            report["score"] += (report["parameters_with_type"] / report["total_parameters"]) * 50

        return report

    def validate_authentication(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate authentication extraction.
        
        Should include:
        - Security scheme (Bearer, Basic, API Key, etc.)
        - Required scopes
        - Example token
        """
        report = {
            "has_security": False,
            "security_methods": [],
            "has_example_token": False,
            "has_scopes": False,
            "issues": [],
            "score": 0.0
        }

        security = endpoint.get("security", [])
        if security:
            report["has_security"] = True
            report["security_methods"] = security
            report["score"] += 50

        # Check for example token
        if endpoint.get("exampleToken"):
            report["has_example_token"] = True
            report["score"] += 25

        # Check for scopes
        if endpoint.get("scopes"):
            report["has_scopes"] = True
            report["score"] += 25

        if not security:
            report["issues"].append("No authentication detected")

        return report

    def generate_validation_report(self, endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive validation report for all endpoints.
        """
        report = {
            "total_endpoints": len(endpoints),
            "endpoints": [],
            "overall_coverage": 0.0,
            "request_body_coverage": 0.0,
            "response_schema_coverage": 0.0,
            "parameter_coverage": 0.0,
            "authentication_coverage": 0.0,
            "issues": [],
            "recommendations": []
        }

        endpoint_scores = []
        request_body_scores = []
        response_schema_scores = []
        parameter_scores = []
        authentication_scores = []

        for endpoint in endpoints:
            # Validate endpoint
            endpoint_report = self.validate_endpoint(endpoint)
            report["endpoints"].append(endpoint_report)
            endpoint_scores.append(endpoint_report["coverage_score"])

            # Validate request body
            request_body_report = self.validate_request_body(endpoint.get("requestBody"))
            request_body_scores.append(request_body_report["score"])

            # Validate response schema
            response_schema_report = self.validate_response_schema(endpoint.get("responses"))
            response_schema_scores.append(response_schema_report["score"])

            # Validate parameters
            parameter_report = self.validate_parameters(endpoint)
            parameter_scores.append(parameter_report["score"])

            # Validate authentication
            authentication_report = self.validate_authentication(endpoint)
            authentication_scores.append(authentication_report["score"])

        # Calculate overall scores
        if endpoint_scores:
            report["overall_coverage"] = sum(endpoint_scores) / len(endpoint_scores)
        if request_body_scores:
            report["request_body_coverage"] = sum(request_body_scores) / len(request_body_scores)
        if response_schema_scores:
            report["response_schema_coverage"] = sum(response_schema_scores) / len(response_schema_scores)
        if parameter_scores:
            report["parameter_coverage"] = sum(parameter_scores) / len(parameter_scores)
        if authentication_scores:
            report["authentication_coverage"] = sum(authentication_scores) / len(authentication_scores)

        # Generate recommendations
        if report["request_body_coverage"] < 70:
            report["recommendations"].append(
                "Improve request body extraction: Use FormRequest classes with validation rules"
            )
        if report["response_schema_coverage"] < 70:
            report["recommendations"].append(
                "Improve response schema extraction: Use Resource classes for responses"
            )
        if report["parameter_coverage"] < 70:
            report["recommendations"].append(
                "Improve parameter extraction: Add explicit parameter documentation"
            )
        if report["authentication_coverage"] < 70:
            report["recommendations"].append(
                "Improve authentication extraction: Use middleware for auth requirements"
            )

        return report

    def print_validation_report(self, report: Dict[str, Any]) -> None:
        """Print validation report in human-readable format."""
        print("\n" + "=" * 80)
        print("EXTRACTION VALIDATION REPORT")
        print("=" * 80)

        print(f"\nTotal Endpoints: {report['total_endpoints']}")
        print(f"\nCoverage Scores:")
        print(f"  Overall Coverage: {report['overall_coverage']:.1f}%")
        print(f"  Request Body Coverage: {report['request_body_coverage']:.1f}%")
        print(f"  Response Schema Coverage: {report['response_schema_coverage']:.1f}%")
        print(f"  Parameter Coverage: {report['parameter_coverage']:.1f}%")
        print(f"  Authentication Coverage: {report['authentication_coverage']:.1f}%")

        if report["recommendations"]:
            print(f"\nRecommendations:")
            for rec in report["recommendations"]:
                print(f"  • {rec}")

        print("\n" + "=" * 80)
