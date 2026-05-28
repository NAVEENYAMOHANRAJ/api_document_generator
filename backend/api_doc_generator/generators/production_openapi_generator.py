"""
Production-Grade OpenAPI Generator - Generates complete OpenAPI 3.1.0 specs.

Includes all 30+ data points:
- API metadata
- Authentication
- Environments
- Rate limiting
- Global headers
- Versioning
- Endpoints with full details
- Request/response schemas
- Validation rules
- Examples
- Error definitions
- Webhooks
- Changelogs
"""

import json
from typing import Dict, List, Any, Optional


class ProductionOpenAPIGenerator:
    """Generate production-grade OpenAPI 3.1.0 specifications"""
    
    def __init__(self, api_metadata: Dict[str, Any]):
        self.api_metadata = api_metadata
    
    def generate(
        self,
        endpoints: List[Dict[str, Any]],
        authentication: Optional[List[Dict[str, Any]]] = None,
        environments: Optional[List[Dict[str, Any]]] = None,
        rate_limits: Optional[Dict[str, Any]] = None,
        global_headers: Optional[List[Dict[str, Any]]] = None,
        versioning: Optional[Dict[str, Any]] = None,
        webhooks: Optional[List[Dict[str, Any]]] = None,
        errors: Optional[List[Dict[str, Any]]] = None,
        changelog: Optional[List[Dict[str, Any]]] = None,
        schemas: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate complete OpenAPI specification"""
        
        spec = {
            "openapi": "3.1.0",
            "info": self._generate_info(),
            "servers": self._generate_servers(environments),
            "paths": self._generate_paths(endpoints),
            "components": self._generate_components(
                authentication, global_headers, schemas, errors
            ),
            "security": self._generate_security(authentication),
            "tags": self._generate_tags(endpoints),
            "x-rate-limits": rate_limits,
            "x-versioning": versioning,
            "x-webhooks": webhooks,
            "x-changelog": changelog
        }
        
        # Remove None values
        spec = {k: v for k, v in spec.items() if v is not None}
        
        return spec
    
    def _generate_info(self) -> Dict[str, Any]:
        """Generate info object"""
        info = {
            "title": self.api_metadata.get("name", "API"),
            "description": self.api_metadata.get("description", ""),
            "version": self.api_metadata.get("version", "1.0.0"),
            "x-framework": self.api_metadata.get("framework", "Unknown")
        }
        
        if self.api_metadata.get("contact"):
            info["contact"] = self.api_metadata["contact"]
        
        if self.api_metadata.get("license"):
            info["license"] = self.api_metadata["license"]
        
        if self.api_metadata.get("terms_of_service"):
            info["termsOfService"] = self.api_metadata["terms_of_service"]
        
        return info
    
    def _generate_servers(self, environments: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Generate servers array"""
        servers = []
        
        if environments:
            for env in environments:
                servers.append({
                    "url": env.get("url", ""),
                    "description": env.get("description", ""),
                    "x-environment": env.get("name", "")
                })
        else:
            servers.append({
                "url": self.api_metadata.get("base_url", "https://api.example.com"),
                "description": "Production"
            })
        
        return servers
    
    def _generate_paths(self, endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate paths object"""
        paths = {}
        
        for endpoint in endpoints:
            path = endpoint.get("path", "/")
            method = endpoint.get("method", "GET").lower()
            
            if path not in paths:
                paths[path] = {}
            
            paths[path][method] = self._generate_operation(endpoint)
        
        return paths
    
    def _generate_operation(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """Generate operation object for an endpoint"""
        operation = {
            "summary": endpoint.get("summary", ""),
            "description": endpoint.get("description", ""),
            "tags": endpoint.get("tags", []),
            "operationId": self._generate_operation_id(endpoint),
            "parameters": self._generate_parameters(endpoint),
            "requestBody": self._generate_request_body(endpoint),
            "responses": self._generate_responses(endpoint),
            "security": self._generate_operation_security(endpoint),
            "x-middleware": endpoint.get("middleware", []),
            "x-source": endpoint.get("source", {}),
            "x-confidence": endpoint.get("confidence_score", 0.0),
            "x-examples": {
                "curl": endpoint.get("curl_example"),
                "request": endpoint.get("request_example"),
                "sdk": endpoint.get("sdk_examples")
            }
        }
        
        # Remove None/empty values
        operation = {k: v for k, v in operation.items() if v}
        
        return operation
    
    def _generate_operation_id(self, endpoint: Dict[str, Any]) -> str:
        """Generate operationId"""
        method = endpoint.get("method", "GET").lower()
        path = endpoint.get("path", "/").replace("/", "_").replace("{", "").replace("}", "")
        return f"{method}_{path}".strip("_")
    
    def _generate_parameters(self, endpoint: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Generate parameters array"""
        parameters = []
        
        # Path parameters
        if endpoint.get("path_parameters"):
            for param in endpoint["path_parameters"]:
                parameters.append({
                    "name": param.get("name"),
                    "in": "path",
                    "required": param.get("required", True),
                    "description": param.get("description"),
                    "schema": {
                        "type": param.get("type", "string"),
                        "example": param.get("example")
                    }
                })
        
        # Query parameters
        if endpoint.get("query_parameters"):
            for param in endpoint["query_parameters"]:
                parameters.append({
                    "name": param.get("name"),
                    "in": "query",
                    "required": param.get("required", False),
                    "description": param.get("description"),
                    "schema": {
                        "type": param.get("type", "string"),
                        "default": param.get("default"),
                        "example": param.get("example")
                    }
                })
        
        # Headers
        if endpoint.get("headers"):
            for header in endpoint["headers"]:
                parameters.append({
                    "name": header.get("name"),
                    "in": "header",
                    "required": header.get("required", False),
                    "description": header.get("description"),
                    "schema": {
                        "type": header.get("type", "string"),
                        "example": header.get("example")
                    }
                })
        
        return parameters if parameters else None
    
    def _generate_request_body(self, endpoint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate requestBody object"""
        request_body = endpoint.get("request_body")
        
        if not request_body:
            return None
        
        return {
            "required": request_body.get("required", False),
            "content": {
                request_body.get("content_type", "application/json"): {
                    "schema": request_body.get("schema", {}),
                    "example": request_body.get("example")
                }
            }
        }
    
    def _generate_responses(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """Generate responses object"""
        responses = {}
        
        if endpoint.get("responses"):
            for response in endpoint["responses"]:
                status_code = str(response.get("status_code", 200))
                responses[status_code] = {
                    "description": response.get("description", ""),
                    "content": {
                        "application/json": {
                            "schema": response.get("schema", {}),
                            "example": response.get("example")
                        }
                    }
                }
        else:
            # Default response
            responses["200"] = {
                "description": "Success",
                "content": {
                    "application/json": {
                        "schema": {"type": "object"}
                    }
                }
            }
        
        return responses
    
    def _generate_security(self, authentication: Optional[List[Dict[str, Any]]]) -> Optional[List[Dict[str, Any]]]:
        """Generate global security requirements"""
        if not authentication:
            return None
        
        security = []
        for auth in authentication:
            auth_type = auth.get("type", "Bearer")
            security.append({auth_type: []})
        
        return security if security else None
    
    def _generate_operation_security(self, endpoint: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Generate operation-level security"""
        if endpoint.get("security"):
            return [{sec: []} for sec in endpoint["security"]]
        
        return None
    
    def _generate_components(
        self,
        authentication: Optional[List[Dict[str, Any]]],
        global_headers: Optional[List[Dict[str, Any]]],
        schemas: Optional[Dict[str, Any]],
        errors: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Generate components object"""
        components = {}
        
        # Security schemes
        if authentication:
            components["securitySchemes"] = self._generate_security_schemes(authentication)
        
        # Schemas
        if schemas:
            components["schemas"] = schemas
        
        # Error schemas
        if errors:
            components["schemas"] = components.get("schemas", {})
            for error in errors:
                error_name = error.get("code", "Error")
                components["schemas"][error_name] = {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "example": error.get("code")},
                        "message": {"type": "string", "example": error.get("message")},
                        "status_code": {"type": "integer", "example": error.get("status_code")}
                    }
                }
        
        # Headers
        if global_headers:
            components["headers"] = self._generate_header_schemas(global_headers)
        
        return components if components else {}
    
    def _generate_security_schemes(self, authentication: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate securitySchemes"""
        schemes = {}
        
        for auth in authentication:
            auth_type = auth.get("type", "Bearer")
            scheme = auth.get("scheme", "bearer")
            
            if scheme.lower() == "bearer":
                schemes[auth_type] = {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": auth.get("format", "JWT"),
                    "description": auth.get("description", "")
                }
            elif scheme.lower() == "oauth2":
                schemes[auth_type] = {
                    "type": "oauth2",
                    "flows": {
                        "implicit": {
                            "authorizationUrl": "https://example.com/oauth/authorize",
                            "scopes": {}
                        }
                    }
                }
            elif scheme.lower() == "apikey":
                schemes[auth_type] = {
                    "type": "apiKey",
                    "in": "header",
                    "name": auth.get("header", "X-API-Key"),
                    "description": auth.get("description", "")
                }
            else:
                schemes[auth_type] = {
                    "type": "http",
                    "scheme": scheme.lower(),
                    "description": auth.get("description", "")
                }
        
        return schemes
    
    def _generate_header_schemas(self, headers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate header schemas"""
        header_schemas = {}
        
        for header in headers:
            header_name = header.get("name", "")
            header_schemas[header_name] = {
                "description": header.get("description", ""),
                "schema": {
                    "type": header.get("type", "string"),
                    "example": header.get("example")
                }
            }
        
        return header_schemas
    
    def _generate_tags(self, endpoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate tags array"""
        tags_set = set()
        
        for endpoint in endpoints:
            if endpoint.get("tags"):
                tags_set.update(endpoint["tags"])
        
        return [{"name": tag} for tag in sorted(tags_set)]
    
    def to_json(self, spec: Dict[str, Any]) -> str:
        """Convert spec to JSON"""
        return json.dumps(spec, indent=2)
    
    def to_yaml(self, spec: Dict[str, Any]) -> str:
        """Convert spec to YAML"""
        try:
            import yaml
            return yaml.dump(spec, default_flow_style=False)
        except ImportError:
            # Fallback to JSON if YAML not available
            return self.to_json(spec)
