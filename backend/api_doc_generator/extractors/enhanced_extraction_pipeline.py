"""
Enhanced Extraction Pipeline - Integrates detailed endpoint extraction.

This pipeline orchestrates:
1. Basic route extraction from framework files
2. Detailed metadata extraction (request/response schemas, auth, etc.)
3. Deduplication and normalization
4. Documentation generation
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import json

from .laravel_extractor import LaravelExtractor
from .detailed_endpoint_extractor import DetailedEndpointExtractor


class EnhancedExtractionPipeline:
    """Orchestrate enhanced endpoint extraction with detailed metadata."""

    def __init__(self, repo_path: str = ""):
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.detailed_extractor = DetailedEndpointExtractor(str(self.repo_path))

    def extract_from_laravel_routes(
        self,
        routes_file: str,
        repo_files: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Extract endpoints from Laravel routes file with detailed metadata.
        
        Args:
            routes_file: Path to routes file (e.g., routes/api.php)
            repo_files: List of all files in repository
            
        Returns:
            List of enhanced endpoints with detailed metadata
        """
        # Step 1: Extract basic routes
        routes_content = Path(routes_file).read_text(encoding='utf-8', errors='ignore')
        basic_endpoints = LaravelExtractor.extract(routes_file, routes_content, str(self.repo_path))
        
        # Step 2: Enhance each endpoint with detailed metadata
        enhanced_endpoints = []
        for endpoint in basic_endpoints:
            enhanced = self.detailed_extractor.extract_endpoint_details(endpoint, repo_files)
            enhanced_endpoints.append(enhanced)
        
        # Step 3: Deduplicate
        deduplicated = self._deduplicate_endpoints(enhanced_endpoints)
        
        return deduplicated

    def _deduplicate_endpoints(
        self,
        endpoints: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Deduplicate endpoints by (method, path).
        Keep endpoint with highest confidence.
        """
        seen = {}
        
        for endpoint in endpoints:
            key = (endpoint.get("method"), endpoint.get("path"))
            
            if key not in seen:
                seen[key] = endpoint
            else:
                # Keep endpoint with higher confidence
                existing_confidence = seen[key].get("confidence", 0.0)
                new_confidence = endpoint.get("confidence", 0.0)
                
                if new_confidence > existing_confidence:
                    seen[key] = endpoint
        
        return list(seen.values())

    def extract_summary_from_endpoint(
        self,
        endpoint: Dict[str, Any]
    ) -> str:
        """
        Generate a summary for an endpoint based on HTTP method and path.
        
        Args:
            endpoint: Endpoint dictionary
            
        Returns:
            Generated summary string
        """
        method = endpoint.get("method", "GET").upper()
        path = endpoint.get("path", "/")
        
        # Extract resource name from path
        parts = [p for p in path.split("/") if p and not p.startswith("{")]
        resource = parts[-1] if parts else "resource"
        
        # Generate summary based on method
        summaries = {
            "GET": f"Retrieve {resource}",
            "POST": f"Create {resource}",
            "PUT": f"Update {resource}",
            "PATCH": f"Partially update {resource}",
            "DELETE": f"Delete {resource}",
            "HEAD": f"Check {resource} existence",
            "OPTIONS": f"Get {resource} options",
        }
        
        return summaries.get(method, f"{method} {resource}")

    def generate_endpoint_report(
        self,
        endpoints: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive report of extracted endpoints.
        
        Args:
            endpoints: List of extracted endpoints
            
        Returns:
            Report dictionary with statistics and metadata
        """
        report = {
            "total_endpoints": len(endpoints),
            "by_method": {},
            "by_framework": {},
            "with_request_body": 0,
            "with_response_schema": 0,
            "with_authentication": 0,
            "with_path_parameters": 0,
            "average_confidence": 0.0,
            "endpoints": []
        }
        
        total_confidence = 0.0
        
        for endpoint in endpoints:
            method = endpoint.get("method", "GET")
            framework = endpoint.get("framework", "unknown")
            
            # Count by method
            report["by_method"][method] = report["by_method"].get(method, 0) + 1
            
            # Count by framework
            report["by_framework"][framework] = report["by_framework"].get(framework, 0) + 1
            
            # Count features
            if endpoint.get("requestBody"):
                report["with_request_body"] += 1
            
            if endpoint.get("responses"):
                report["with_response_schema"] += 1
            
            if endpoint.get("security"):
                report["with_authentication"] += 1
            
            if endpoint.get("pathParameters"):
                report["with_path_parameters"] += 1
            
            # Accumulate confidence
            confidence = endpoint.get("confidence", 0.0)
            total_confidence += confidence
            
            # Add endpoint summary
            report["endpoints"].append({
                "method": method,
                "path": endpoint.get("path"),
                "handler": endpoint.get("handler", {}).get("class"),
                "confidence": confidence,
                "has_request_body": bool(endpoint.get("requestBody")),
                "has_response_schema": bool(endpoint.get("responses")),
                "has_authentication": bool(endpoint.get("security")),
            })
        
        # Calculate average confidence
        if endpoints:
            report["average_confidence"] = total_confidence / len(endpoints)
        
        return report

    def export_to_openapi(
        self,
        endpoints: List[Dict[str, Any]],
        title: str = "API Documentation",
        version: str = "1.0.0"
    ) -> Dict[str, Any]:
        """
        Export endpoints to OpenAPI 3.0 format.
        
        Args:
            endpoints: List of extracted endpoints
            title: API title
            version: API version
            
        Returns:
            OpenAPI 3.0 specification dictionary
        """
        openapi_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": title,
                "version": version,
                "description": "Generated from source code analysis"
            },
            "paths": {}
        }
        
        for endpoint in endpoints:
            path = endpoint.get("path", "/")
            method = endpoint.get("method", "GET").lower()
            
            if path not in openapi_spec["paths"]:
                openapi_spec["paths"][path] = {}
            
            operation = {
                "summary": endpoint.get("summary", self.extract_summary_from_endpoint(endpoint)),
                "description": endpoint.get("description", ""),
                "tags": endpoint.get("tags", []),
                "parameters": self._build_openapi_parameters(endpoint),
                "responses": self._build_openapi_responses(endpoint)
            }
            
            # Add request body if present
            if endpoint.get("requestBody"):
                operation["requestBody"] = self._build_openapi_request_body(endpoint)
            
            # Add security if present
            if endpoint.get("security"):
                operation["security"] = [{"bearerAuth": []}]
            
            openapi_spec["paths"][path][method] = operation
        
        return openapi_spec

    def _build_openapi_parameters(self, endpoint: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build OpenAPI parameters from endpoint."""
        parameters = []
        
        # Path parameters
        for param in endpoint.get("pathParameters", []):
            parameters.append({
                "name": param.get("name"),
                "in": "path",
                "required": True,
                "schema": {
                    "type": param.get("type", "string")
                },
                "description": param.get("description", "")
            })
        
        # Query parameters
        for param in endpoint.get("query_params", []):
            parameters.append({
                "name": param.get("name"),
                "in": "query",
                "required": param.get("required", False),
                "schema": {
                    "type": param.get("type", "string")
                },
                "description": param.get("description", "")
            })
        
        return parameters

    def _build_openapi_request_body(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """Build OpenAPI request body from endpoint."""
        request_body = endpoint.get("requestBody", {})
        
        return {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {
                        "type": request_body.get("type", "object"),
                        "properties": request_body.get("properties", {}),
                        "required": request_body.get("required", [])
                    }
                }
            }
        }

    def _build_openapi_responses(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """Build OpenAPI responses from endpoint."""
        responses = {}
        
        # Add status codes
        for status_code in endpoint.get("statusCodes", [200]):
            responses[str(status_code)] = {
                "description": self._get_status_description(status_code),
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object"
                        }
                    }
                }
            }
        
        # If no status codes, add default 200
        if not responses:
            responses["200"] = {
                "description": "Successful response",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object"
                        }
                    }
                }
            }
        
        return responses

    def _get_status_description(self, code: int) -> str:
        """Get description for HTTP status code."""
        descriptions = {
            200: "OK",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            422: "Unprocessable Entity",
            500: "Internal Server Error",
        }
        return descriptions.get(code, f"HTTP {code}")
