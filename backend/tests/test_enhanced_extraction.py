"""
Tests for Enhanced Extraction Pipeline

Tests the detailed endpoint extraction, documentation generation,
and report generation functionality.
"""

import pytest
from pathlib import Path
from typing import Dict, Any, List

from backend.api_doc_generator.extractors.detailed_endpoint_extractor import DetailedEndpointExtractor
from backend.api_doc_generator.extractors.enhanced_extraction_pipeline import EnhancedExtractionPipeline
from backend.api_doc_generator.generators.documentation_generator import DocumentationGenerator


class TestDetailedEndpointExtractor:
    """Test DetailedEndpointExtractor functionality."""

    def test_extract_path_parameters(self):
        """Test extraction of path parameters from route path."""
        extractor = DetailedEndpointExtractor()
        
        # Test single parameter
        params = extractor._extract_path_parameters("/api/users/{id}")
        assert len(params) == 1
        assert params[0]["name"] == "id"
        assert params[0]["in"] == "path"
        assert params[0]["required"] is True
        
        # Test multiple parameters
        params = extractor._extract_path_parameters("/api/users/{userId}/posts/{postId}")
        assert len(params) == 2
        assert params[0]["name"] == "userId"
        assert params[1]["name"] == "postId"
        
        # Test no parameters
        params = extractor._extract_path_parameters("/api/users")
        assert params is None

    def test_parse_validation_rules(self):
        """Test parsing of Laravel validation rules."""
        extractor = DetailedEndpointExtractor()
        
        # Test required rule
        schema = extractor._parse_validation_rules("required|string|max:255")
        assert schema["required"] is True
        assert schema["type"] == "string"
        assert schema["maximum"] == 255
        
        # Test email rule
        schema = extractor._parse_validation_rules("required|email")
        assert schema["format"] == "email"
        
        # Test integer rule
        schema = extractor._parse_validation_rules("required|integer|min:1|max:100")
        assert schema["type"] == "integer"
        assert schema["minimum"] == 1
        assert schema["maximum"] == 100
        
        # Test enum rule
        schema = extractor._parse_validation_rules("required|in:active,inactive,pending")
        assert schema["enum"] == ["active", "inactive", "pending"]

    def test_extract_form_request_class(self):
        """Test extraction of FormRequest class from method parameters."""
        extractor = DetailedEndpointExtractor()
        
        # Test with FormRequest
        class_name = extractor._extract_form_request_class("StoreUserRequest $request")
        assert class_name == "StoreUserRequest"
        
        # Test with multiple parameters
        class_name = extractor._extract_form_request_class("UpdateUserRequest $request, $id")
        assert class_name == "UpdateUserRequest"
        
        # Test without FormRequest
        class_name = extractor._extract_form_request_class("Request $request")
        assert class_name is None


class TestEnhancedExtractionPipeline:
    """Test EnhancedExtractionPipeline functionality."""

    def test_deduplicate_endpoints(self):
        """Test deduplication of endpoints."""
        pipeline = EnhancedExtractionPipeline()
        
        endpoints = [
            {
                "method": "GET",
                "path": "/api/users",
                "confidence": 0.85,
                "handler": {"class": "UserController", "method": "index"}
            },
            {
                "method": "GET",
                "path": "/api/users",
                "confidence": 0.95,  # Higher confidence
                "handler": {"class": "UserController", "method": "index"}
            },
            {
                "method": "POST",
                "path": "/api/users",
                "confidence": 0.90,
                "handler": {"class": "UserController", "method": "store"}
            }
        ]
        
        deduplicated = pipeline._deduplicate_endpoints(endpoints)
        
        # Should have 2 endpoints (GET and POST)
        assert len(deduplicated) == 2
        
        # GET endpoint should have higher confidence
        get_endpoint = [e for e in deduplicated if e["method"] == "GET"][0]
        assert get_endpoint["confidence"] == 0.95

    def test_extract_summary_from_endpoint(self):
        """Test summary generation from endpoint."""
        pipeline = EnhancedExtractionPipeline()
        
        # Test GET
        summary = pipeline.extract_summary_from_endpoint({
            "method": "GET",
            "path": "/api/users"
        })
        assert "Retrieve" in summary
        
        # Test POST
        summary = pipeline.extract_summary_from_endpoint({
            "method": "POST",
            "path": "/api/users"
        })
        assert "Create" in summary
        
        # Test PUT
        summary = pipeline.extract_summary_from_endpoint({
            "method": "PUT",
            "path": "/api/users/{id}"
        })
        assert "Update" in summary
        
        # Test DELETE
        summary = pipeline.extract_summary_from_endpoint({
            "method": "DELETE",
            "path": "/api/users/{id}"
        })
        assert "Delete" in summary

    def test_generate_endpoint_report(self):
        """Test generation of endpoint report."""
        pipeline = EnhancedExtractionPipeline()
        
        endpoints = [
            {
                "method": "GET",
                "path": "/api/users",
                "framework": "laravel",
                "confidence": 0.95,
                "requestBody": None,
                "responses": {"200": {}},
                "security": ["auth:api"],
                "pathParameters": []
            },
            {
                "method": "POST",
                "path": "/api/users",
                "framework": "laravel",
                "confidence": 0.90,
                "requestBody": {"type": "object"},
                "responses": {"201": {}},
                "security": ["auth:api"],
                "pathParameters": []
            },
            {
                "method": "GET",
                "path": "/api/users/{id}",
                "framework": "laravel",
                "confidence": 0.85,
                "requestBody": None,
                "responses": {"200": {}},
                "security": [],
                "pathParameters": [{"name": "id"}]
            }
        ]
        
        report = pipeline.generate_endpoint_report(endpoints)
        
        assert report["total_endpoints"] == 3
        assert report["by_method"]["GET"] == 2
        assert report["by_method"]["POST"] == 1
        assert report["by_framework"]["laravel"] == 3
        assert report["with_request_body"] == 1
        assert report["with_response_schema"] == 3
        assert report["with_authentication"] == 2
        assert report["with_path_parameters"] == 1
        assert report["average_confidence"] == pytest.approx(0.9, abs=0.01)

    def test_export_to_openapi(self):
        """Test export to OpenAPI 3.0 format."""
        pipeline = EnhancedExtractionPipeline()
        
        endpoints = [
            {
                "method": "GET",
                "path": "/api/users",
                "summary": "List users",
                "description": "Get all users",
                "tags": ["users"],
                "requestBody": None,
                "responses": {"200": {}},
                "security": ["auth:api"],
                "pathParameters": [],
                "statusCodes": [200]
            }
        ]
        
        openapi_spec = pipeline.export_to_openapi(endpoints, title="Test API", version="1.0.0")
        
        assert openapi_spec["openapi"] == "3.0.0"
        assert openapi_spec["info"]["title"] == "Test API"
        assert openapi_spec["info"]["version"] == "1.0.0"
        assert "/api/users" in openapi_spec["paths"]
        assert "get" in openapi_spec["paths"]["/api/users"]


class TestDocumentationGenerator:
    """Test DocumentationGenerator enhancements."""

    def test_html_status_codes(self):
        """Test HTML generation for status codes."""
        endpoint = {
            "statusCodes": [200, 201, 422]
        }
        
        html = DocumentationGenerator._html_status_codes(endpoint)
        
        assert "200" in html
        assert "201" in html
        assert "422" in html
        assert "detail-section" in html

    def test_html_path_parameters(self):
        """Test HTML generation for path parameters."""
        endpoint = {
            "pathParameters": [
                {
                    "name": "id",
                    "type": "string",
                    "description": "User ID"
                },
                {
                    "name": "postId",
                    "type": "integer",
                    "description": "Post ID"
                }
            ]
        }
        
        html = DocumentationGenerator._html_path_parameters(endpoint)
        
        assert "id" in html
        assert "postId" in html
        assert "User ID" in html
        assert "Post ID" in html

    def test_html_security(self):
        """Test HTML generation for security/authentication."""
        endpoint = {
            "security": ["auth:api", "auth:sanctum"]
        }
        
        html = DocumentationGenerator._html_security(endpoint)
        
        assert "auth:api" in html
        assert "auth:sanctum" in html
        assert "Authentication" in html

    def test_status_code_description(self):
        """Test status code description mapping."""
        assert "OK" in DocumentationGenerator._status_code_description(200)
        assert "Created" in DocumentationGenerator._status_code_description(201)
        assert "Not Found" in DocumentationGenerator._status_code_description(404)
        assert "Unauthorized" in DocumentationGenerator._status_code_description(401)
        assert "Unprocessable Entity" in DocumentationGenerator._status_code_description(422)


class TestIntegration:
    """Integration tests for the complete pipeline."""

    def test_complete_extraction_flow(self):
        """Test complete extraction flow."""
        pipeline = EnhancedExtractionPipeline()
        
        # Create sample endpoint
        endpoint = {
            "method": "POST",
            "path": "/api/users",
            "handler": {
                "class": "App\\Http\\Controllers\\UserController",
                "method": "store"
            },
            "framework": "laravel",
            "confidence": 0.95,
            "requestBody": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "required": True},
                    "email": {"type": "string", "format": "email", "required": True}
                },
                "required": ["name", "email"]
            },
            "responses": {
                200: {"type": "object", "resource": "UserResource"}
            },
            "statusCodes": [200, 422],
            "security": ["auth:api"],
            "pathParameters": []
        }
        
        # Generate report
        report = pipeline.generate_endpoint_report([endpoint])
        assert report["total_endpoints"] == 1
        assert report["with_request_body"] == 1
        
        # Export to OpenAPI
        openapi_spec = pipeline.export_to_openapi([endpoint])
        assert "/api/users" in openapi_spec["paths"]
        assert "post" in openapi_spec["paths"]["/api/users"]
        
        # Generate documentation
        html = DocumentationGenerator.generate_html([endpoint], title="Test API")
        assert "POST" in html
        assert "/api/users" in html
        
        markdown = DocumentationGenerator.generate_markdown([endpoint], title="Test API")
        assert "POST" in markdown
        assert "/api/users" in markdown


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
