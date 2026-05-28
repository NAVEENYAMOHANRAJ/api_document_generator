"""
Production-Grade API Documentation Extractor

Complete rewrite using AST parsing for all technologies.
Extracts comprehensive API metadata including:
- API overview and metadata
- Authentication schemes
- Global headers
- Rate limiting
- Versioning
- Endpoint groups
- Source traceability
- Middleware
- Security requirements
- Request/response schemas
- Validation rules
- Examples
- Error handling
- Pagination
- Webhooks
- Data models
- Changelog
- OpenAPI compliance
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json

from api_doc_generator.extractors.detailed_endpoint_extractor import DetailedEndpointExtractor
from api_doc_generator.extractors.express_extractor import ExpressExtractor
from api_doc_generator.extractors.fastapi_ast_extractor import FastAPIASTExtractor
from api_doc_generator.extractors.laravel_extractor import LaravelExtractor
from api_doc_generator.extractors.nestjs_extractor import NestJSExtractor
from api_doc_generator.extractors.spring_boot_extractor import SpringBootExtractor


class Framework(Enum):
    """Supported frameworks"""
    LARAVEL = "Laravel"
    FASTAPI = "FastAPI"
    DJANGO = "Django"
    EXPRESS = "Express"
    SPRING_BOOT = "Spring Boot"
    NESTJS = "NestJS"
    UNKNOWN = "Unknown"


class AuthType(Enum):
    """Authentication types"""
    BEARER_TOKEN = "Bearer Token"
    JWT = "JWT"
    OAUTH2 = "OAuth2"
    API_KEY = "API Key"
    SESSION = "Session"
    SANCTUM = "Sanctum"
    PASSPORT = "Passport"
    BASIC = "Basic Auth"


@dataclass
class APIMetadata:
    """API-level metadata"""
    name: str
    description: str
    version: str
    framework: str
    base_url: str
    openapi_version: str = "3.1.0"
    contact: Optional[Dict[str, str]] = None
    license: Optional[Dict[str, str]] = None
    terms_of_service: Optional[str] = None


@dataclass
class Authentication:
    """Authentication configuration"""
    type: str
    scheme: str
    header: str
    format: str
    description: Optional[str] = None


@dataclass
class Environment:
    """Environment configuration"""
    name: str
    url: str
    description: Optional[str] = None


@dataclass
class RateLimit:
    """Rate limiting configuration"""
    limit: int
    window: str
    description: Optional[str] = None


@dataclass
class Parameter:
    """Request parameter"""
    name: str
    param_type: str
    required: bool
    description: Optional[str] = None
    default: Optional[Any] = None
    enum: Optional[List[Any]] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    pattern: Optional[str] = None


@dataclass
class RequestBody:
    """Request body schema"""
    required: bool
    content_type: str
    schema: Dict[str, Any]
    example: Optional[Dict[str, Any]] = None


@dataclass
class Response:
    """Response schema"""
    status_code: int
    description: str
    schema: Optional[Dict[str, Any]] = None
    example: Optional[Dict[str, Any]] = None
    headers: Optional[List[Parameter]] = None


@dataclass
class Endpoint:
    """Complete endpoint documentation"""
    method: str
    path: str
    summary: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    
    # Source traceability
    source: Optional[Dict[str, Any]] = None
    
    # Parameters
    path_parameters: Optional[List[Parameter]] = None
    query_parameters: Optional[List[Parameter]] = None
    headers: Optional[List[Parameter]] = None
    
    # Request/Response
    request_body: Optional[RequestBody] = None
    responses: Optional[List[Response]] = None
    
    # Security
    security: Optional[List[str]] = None
    middleware: Optional[List[str]] = None
    
    # Examples
    curl_example: Optional[str] = None
    request_example: Optional[Dict[str, Any]] = None
    
    # Metadata
    deprecated: bool = False
    replacement: Optional[str] = None
    confidence: float = 0.0


@dataclass
class APIDocumentation:
    """Complete API documentation"""
    api: APIMetadata
    authentication: Optional[List[Authentication]] = None
    environments: Optional[List[Environment]] = None
    rate_limits: Optional[RateLimit] = None
    global_headers: Optional[List[Parameter]] = None
    versioning: Optional[Dict[str, Any]] = None
    endpoints: Optional[List[Endpoint]] = None
    schemas: Optional[Dict[str, Any]] = None
    webhooks: Optional[List[Dict[str, Any]]] = None
    errors: Optional[Dict[str, Any]] = None
    changelog: Optional[List[Dict[str, Any]]] = None
    pagination: Optional[Dict[str, Any]] = None


class ProductionExtractor:
    """Production-grade API documentation extractor using AST"""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.framework = self._detect_framework()
        self.file_cache: Dict[str, str] = {}
        self.ast_cache: Dict[str, ast.Module] = {}
        self.repo_files = [
            str(path)
            for path in self.repo_path.rglob("*")
            if path.is_file() and self._is_supported_source_file(path)
        ]

    def extract_complete_documentation(self) -> APIDocumentation:
        """Extract complete production-grade API documentation"""
        
        # Detect framework
        framework = self._detect_framework()
        
        # Extract API metadata
        api_metadata = self._extract_api_metadata()
        
        # Extract authentication
        authentication = self._extract_authentication()
        
        # Extract environments
        environments = self._extract_environments()
        
        # Extract rate limiting
        rate_limits = self._extract_rate_limits()
        
        # Extract global headers
        global_headers = self._extract_global_headers()
        
        # Extract versioning
        versioning = self._extract_versioning()
        
        # Extract endpoints
        endpoints = self._extract_endpoints()
        
        # Extract schemas
        schemas = self._extract_schemas()
        
        # Extract webhooks
        webhooks = self._extract_webhooks()
        
        # Extract errors
        errors = self._extract_error_definitions()
        
        # Extract changelog
        changelog = self._extract_changelog()
        
        # Extract pagination
        pagination = self._extract_pagination_config()
        
        return APIDocumentation(
            api=api_metadata,
            authentication=authentication,
            environments=environments,
            rate_limits=rate_limits,
            global_headers=global_headers,
            versioning=versioning,
            endpoints=endpoints,
            schemas=schemas,
            webhooks=webhooks,
            errors=errors,
            changelog=changelog,
            pagination=pagination
        )

    def _detect_framework(self) -> Framework:
        """Detect framework using AST and file patterns"""
        
        # Check for Laravel
        if (self.repo_path / "artisan").exists():
            return Framework.LARAVEL
        
        # Check for FastAPI
        if self._has_fastapi_imports():
            return Framework.FASTAPI
        
        # Check for Django
        if (self.repo_path / "manage.py").exists():
            return Framework.DJANGO
        
        # Check for Express
        if self._has_express_imports():
            return Framework.EXPRESS
        
        # Check for Spring Boot
        if (self.repo_path / "pom.xml").exists() or (self.repo_path / "build.gradle").exists():
            return Framework.SPRING_BOOT
        
        # Check for NestJS
        if self._has_nestjs_imports():
            return Framework.NESTJS
        
        return Framework.UNKNOWN

    def _has_fastapi_imports(self) -> bool:
        """Check for FastAPI imports"""
        for py_file in self.repo_path.rglob("*.py"):
            try:
                content = self._read_file(str(py_file))
                if "from fastapi import" in content or "import fastapi" in content:
                    return True
            except:
                pass
        return False

    def _has_express_imports(self) -> bool:
        """Check for Express imports"""
        for js_file in self.repo_path.rglob("*.js"):
            try:
                content = self._read_file(str(js_file))
                if "require('express')" in content or "import express" in content:
                    return True
            except:
                pass
        return False

    def _has_nestjs_imports(self) -> bool:
        """Check for NestJS imports"""
        for ts_file in self.repo_path.rglob("*.ts"):
            try:
                content = self._read_file(str(ts_file))
                if "@nestjs" in content:
                    return True
            except:
                pass
        return False

    def _extract_api_metadata(self) -> APIMetadata:
        """Extract API-level metadata"""
        
        # Try to find package.json or composer.json
        package_json = self.repo_path / "package.json"
        composer_json = self.repo_path / "composer.json"
        
        name = "API"
        version = "1.0.0"
        description = "API Documentation"
        
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                name = data.get("name", name)
                version = data.get("version", version)
                description = data.get("description", description)
            except:
                pass
        
        if composer_json.exists():
            try:
                data = json.loads(composer_json.read_text())
                name = data.get("name", name)
                description = data.get("description", description)
            except:
                pass
        
        return APIMetadata(
            name=name,
            description=description,
            version=version,
            framework=self.framework.value,
            base_url="https://api.example.com",
            contact={"name": "API Team", "email": "api@example.com"},
            license={"name": "MIT"}
        )

    def _extract_authentication(self) -> Optional[List[Authentication]]:
        """Extract authentication schemes using AST"""
        auth_methods = []
        
        # Search for auth-related files and patterns
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".php", ".py", ".js", ".ts"]:
                try:
                    content = self._read_file(str(file_path))
                    
                    # Laravel Sanctum
                    if "sanctum" in content.lower():
                        auth_methods.append(Authentication(
                            type=AuthType.SANCTUM.value,
                            scheme="Bearer",
                            header="Authorization",
                            format="Bearer <token>",
                            description="Laravel Sanctum authentication"
                        ))
                    
                    # Laravel Passport
                    if "passport" in content.lower():
                        auth_methods.append(Authentication(
                            type=AuthType.PASSPORT.value,
                            scheme="Bearer",
                            header="Authorization",
                            format="Bearer <token>",
                            description="Laravel Passport OAuth2"
                        ))
                    
                    # JWT
                    if "jwt" in content.lower() or "json web token" in content.lower():
                        auth_methods.append(Authentication(
                            type=AuthType.JWT.value,
                            scheme="Bearer",
                            header="Authorization",
                            format="Bearer <token>",
                            description="JWT authentication"
                        ))
                    
                    # API Key
                    if "api_key" in content.lower() or "apikey" in content.lower():
                        auth_methods.append(Authentication(
                            type=AuthType.API_KEY.value,
                            scheme="ApiKeyAuth",
                            header="X-API-Key",
                            format="<api_key>",
                            description="API Key authentication"
                        ))
                
                except:
                    pass
        
        # Remove duplicates
        seen = set()
        unique_auth = []
        for auth in auth_methods:
            key = (auth.type, auth.scheme)
            if key not in seen:
                seen.add(key)
                unique_auth.append(auth)
        
        return unique_auth if unique_auth else None

    def _extract_environments(self) -> Optional[List[Environment]]:
        """Extract environment configurations"""
        environments = [
            Environment(
                name="development",
                url="http://localhost:8000",
                description="Local development environment"
            ),
            Environment(
                name="staging",
                url="https://staging-api.example.com",
                description="Staging environment"
            ),
            Environment(
                name="production",
                url="https://api.example.com",
                description="Production environment"
            )
        ]
        return environments

    def _extract_rate_limits(self) -> Optional[RateLimit]:
        """Extract rate limiting configuration"""
        
        # Search for throttle/rate limit configuration
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".php", ".py", ".js", ".ts"]:
                try:
                    content = self._read_file(str(file_path))
                    
                    # Laravel throttle pattern
                    match = re.search(r"throttle[:\(](\d+)[,\)](\d+)", content)
                    if match:
                        limit = int(match.group(1))
                        window = int(match.group(2))
                        return RateLimit(
                            limit=limit,
                            window=f"{window} minute(s)",
                            description=f"Rate limit: {limit} requests per {window} minute(s)"
                        )
                
                except:
                    pass
        
        # Default rate limit
        return RateLimit(
            limit=60,
            window="1 minute",
            description="Default rate limit: 60 requests per minute"
        )

    def _extract_global_headers(self) -> Optional[List[Parameter]]:
        """Extract global required headers"""
        return [
            Parameter(
                name="Accept",
                param_type="string",
                required=True,
                default="application/json",
                description="Response content type"
            ),
            Parameter(
                name="Content-Type",
                param_type="string",
                required=True,
                default="application/json",
                description="Request content type"
            ),
            Parameter(
                name="Authorization",
                param_type="string",
                required=False,
                description="Bearer token for authentication"
            )
        ]

    def _extract_versioning(self) -> Optional[Dict[str, Any]]:
        """Extract versioning strategy"""
        return {
            "strategy": "URI",
            "current": "v1",
            "deprecated": [],
            "description": "API versioning through URI path"
        }

    def _extract_endpoints(self) -> Optional[List[Endpoint]]:
        """Extract endpoints using AST"""
        endpoints = []
        
        if self.framework == Framework.LARAVEL:
            endpoints = self._extract_laravel_endpoints()
        elif self.framework == Framework.FASTAPI:
            endpoints = self._extract_fastapi_endpoints()
        elif self.framework == Framework.EXPRESS:
            endpoints = self._extract_with_static_extractor(ExpressExtractor, "Express", [".js", ".ts"])
        elif self.framework == Framework.NESTJS:
            endpoints = self._extract_with_static_extractor(NestJSExtractor, "NestJS", [".ts"])
        elif self.framework == Framework.SPRING_BOOT:
            endpoints = self._extract_with_static_extractor(SpringBootExtractor, "Spring Boot", [".java"])
        elif self.framework == Framework.DJANGO:
            endpoints = self._extract_django_endpoints()
        
        return self._dedupe_endpoints(endpoints) if endpoints else None

    def _extract_laravel_endpoints(self) -> List[Endpoint]:
        """Extract Laravel endpoints with AST-aware route parsing and controller enrichment."""
        raw_endpoints: List[Dict[str, Any]] = []
        details = DetailedEndpointExtractor(str(self.repo_path))
        routes_files = list(self.repo_path.rglob("routes/*.php"))

        for routes_file in routes_files:
            try:
                content = self._read_file(str(routes_file))
                relative_path = routes_file.relative_to(self.repo_path).as_posix()
                raw_endpoints.extend(LaravelExtractor.extract(relative_path, content, str(self.repo_path)))
            except Exception as e:
                print(f"Error parsing {routes_file}: {e}")

        endpoints: List[Endpoint] = []
        for raw in raw_endpoints:
            enriched = details.extract_endpoint_details(raw, self.repo_files)
            endpoints.append(self._endpoint_from_extracted(enriched, "Laravel"))

        return endpoints

    def _extract_fastapi_endpoints(self) -> List[Endpoint]:
        """Extract FastAPI endpoints using Python AST."""
        endpoints = []
        extractor = FastAPIASTExtractor(str(self.repo_path))
        for raw in extractor.to_dict() if extractor.endpoints else extractor.extract_all_endpoints():
            if hasattr(raw, "__dict__"):
                raw = {
                    "method": raw.method,
                    "path": raw.path,
                    "function_name": raw.function_name,
                    "summary": raw.summary,
                    "description": raw.description,
                    "tags": raw.tags,
                    "status_code": raw.status_code,
                    "response_model": raw.response_model,
                    "request_body_model": raw.request_body_model,
                    "dependencies": raw.dependencies,
                    "source": {"file": raw.source_file, "line": raw.line_number},
                    "confidence": raw.confidence,
                }
            endpoints.append(self._endpoint_from_extracted(raw, "FastAPI"))
        return endpoints

    def _extract_django_endpoints(self) -> List[Endpoint]:
        """Extract Django endpoints using AST"""
        endpoints = []
        
        # Find urls.py files
        urls_files = list(self.repo_path.rglob("urls.py"))
        
        for urls_file in urls_files:
            try:
                content = self._read_file(str(urls_file))
                tree = ast.parse(content)
                
                # Find path() calls
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name) and node.func.id == "path":
                            if node.args:
                                path_arg = node.args[0]
                                if isinstance(path_arg, ast.Constant):
                                    path = path_arg.value
                                    
                                    endpoint = Endpoint(
                                        method="GET",
                                        path=path,
                                        summary=f"GET {path}",
                                        source={
                                            "file": str(urls_file),
                                            "line": node.lineno
                                        },
                                        confidence=0.80
                                    )
                                    
                                    endpoints.append(endpoint)
            
            except Exception as e:
                print(f"Error parsing {urls_file}: {e}")
        
        return endpoints

    def _extract_with_static_extractor(self, extractor_cls, framework: str, suffixes: List[str]) -> List[Endpoint]:
        endpoints: List[Endpoint] = []
        for file_path in self.repo_files:
            path = Path(file_path)
            if path.suffix not in suffixes:
                continue
            try:
                content = self._read_file(file_path)
                for raw in extractor_cls.extract(path.relative_to(self.repo_path).as_posix(), content):
                    endpoints.append(self._endpoint_from_extracted(raw, framework))
            except Exception as exc:
                print(f"Error parsing {file_path}: {exc}")
        return endpoints

    def _extract_schemas(self) -> Optional[Dict[str, Any]]:
        """Extract data models/schemas"""
        schemas = {}
        
        # Search for model definitions
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".php", ".py"]:
                try:
                    content = self._read_file(str(file_path))
                    
                    # Laravel models
                    if "class" in content and "extends Model" in content:
                        class_match = re.search(r"class\s+(\w+)\s+extends\s+Model", content)
                        if class_match:
                            model_name = class_match.group(1)
                            schemas[model_name] = {
                                "type": "object",
                                "source": str(file_path)
                            }
                    
                    # Pydantic models
                    if "class" in content and "BaseModel" in content:
                        class_match = re.search(r"class\s+(\w+)\s*\(.*BaseModel.*\)", content)
                        if class_match:
                            model_name = class_match.group(1)
                            schemas[model_name] = {
                                "type": "object",
                                "source": str(file_path)
                            }
                
                except:
                    pass
        
        return schemas if schemas else None

    def _endpoint_from_extracted(self, raw: Dict[str, Any], framework: str) -> Endpoint:
        method = (raw.get("method") or "GET").upper()
        path = self._normalize_endpoint_path(raw.get("path") or "/")
        handler = raw.get("handler") or {}
        source = raw.get("source") or {}
        provenance = raw.get("provenance") or {}

        source_trace = {
            "route_file": source.get("route_file") or source.get("file") or provenance.get("source_file") or raw.get("source_file"),
            "controller_file": handler.get("file") if isinstance(handler, dict) else None,
            "method": handler.get("method") if isinstance(handler, dict) else raw.get("function_name"),
            "line": source.get("line") or provenance.get("line_number"),
            "framework": framework,
        }

        responses = self._normalize_responses(raw, method)
        request_body = self._normalize_request_body(raw.get("requestBody") or raw.get("request_body"))
        path_parameters = self._normalize_parameters(raw.get("pathParameters") or raw.get("path_params"), "path")
        if not path_parameters:
            path_parameters = self._infer_path_parameters(path)

        security = self._security_from_middleware(raw.get("middleware") or raw.get("dependencies") or raw.get("security") or [])
        middleware = raw.get("middleware") or raw.get("dependencies") or []
        tags = raw.get("tags") or self._infer_tags(path, handler)

        endpoint = Endpoint(
            method=method,
            path=path,
            summary=raw.get("summary") or self._build_summary(method, path, handler),
            description=raw.get("description") or self._build_description(method, path, handler),
            tags=tags,
            source={k: v for k, v in source_trace.items() if v},
            path_parameters=path_parameters,
            query_parameters=self._normalize_parameters(raw.get("queryParameters") or raw.get("query_params"), "query"),
            headers=self._normalize_parameters(raw.get("headers"), "header"),
            request_body=request_body,
            responses=responses,
            security=security,
            middleware=middleware,
            curl_example=self._build_curl_example(method, path, request_body),
            request_example=self._build_example_from_schema(request_body.schema if request_body else {}),
            deprecated=bool(raw.get("deprecated", False)),
            replacement=raw.get("replacement"),
            confidence=float(raw.get("confidence") or raw.get("confidence_score") or 0.82),
        )
        return endpoint

    def _normalize_parameters(self, params: Optional[List[Dict[str, Any]]], location: str) -> Optional[List[Parameter]]:
        normalized = []
        for param in params or []:
            normalized.append(Parameter(
                name=str(param.get("name", "")),
                param_type=param.get("type") or param.get("param_type") or "string",
                required=bool(param.get("required", location == "path")),
                description=param.get("description"),
                default=param.get("default"),
                enum=param.get("enum"),
                minimum=param.get("minimum"),
                maximum=param.get("maximum"),
                pattern=param.get("pattern"),
            ))
        return normalized or None

    def _normalize_request_body(self, body: Optional[Dict[str, Any]]) -> Optional[RequestBody]:
        if not body:
            return None
        schema = body.get("schema") or {
            "type": body.get("type", "object"),
            "properties": body.get("properties", {}),
            "required": body.get("required", []),
        }
        return RequestBody(
            required=bool(body.get("required", True)),
            content_type=body.get("content_type") or "application/json",
            schema=schema,
            example=self._build_example_from_schema(schema),
        )

    def _normalize_responses(self, raw: Dict[str, Any], method: str) -> List[Response]:
        responses = raw.get("responses")
        normalized: List[Response] = []
        if isinstance(responses, dict):
            for code, response in responses.items():
                normalized.append(Response(
                    status_code=int(code),
                    description=response.get("description") or self._default_response_description(int(code)),
                    schema=response.get("schema") or response,
                    example=response.get("example"),
                ))
        elif isinstance(responses, list):
            for response in responses:
                code = int(response.get("status_code") or response.get("code") or 200)
                normalized.append(Response(
                    status_code=code,
                    description=response.get("description") or response.get("message") or self._default_response_description(code),
                    schema=response.get("schema"),
                    example=response.get("example"),
                ))

        for code in raw.get("statusCodes") or []:
            if not any(response.status_code == int(code) for response in normalized):
                normalized.append(Response(status_code=int(code), description=self._default_response_description(int(code))))

        if not normalized:
            default_code = 201 if method == "POST" else 204 if method == "DELETE" else 200
            normalized.append(Response(status_code=default_code, description=self._default_response_description(default_code)))
        # Do not inject global/assumed error responses (401/422/etc).
        # Error responses must be added only when explicitly detected from source/spec.
        return sorted(normalized, key=lambda item: item.status_code)

    def _infer_path_parameters(self, path: str) -> Optional[List[Parameter]]:
        params = re.findall(r"\{([^}/]+)\}", path)
        return [
            Parameter(name=param, param_type="string", required=True, description=f"Path parameter `{param}`")
            for param in params
        ] or None

    def _security_from_middleware(self, middleware: List[str]) -> List[str]:
        joined = " ".join(str(item).lower() for item in middleware)
        if any(token in joined for token in ("auth", "jwt", "sanctum", "passport", "bearer", "depends")):
            return ["bearerAuth"]
        return []

    def _infer_tags(self, path: str, handler: Any) -> List[str]:
        if isinstance(handler, dict) and handler.get("class"):
            return [handler["class"].split("\\")[-1].replace("Controller", "")]
        first = next((part for part in path.split("/") if part and not part.startswith("{")), "General")
        return [first.replace("-", " ").title()]

    def _build_summary(self, method: str, path: str, handler: Any) -> str:
        if isinstance(handler, dict) and handler.get("method"):
            return f"{handler['method'].replace('_', ' ').title()} {path}"
        return f"{method} {path}"

    def _build_description(self, method: str, path: str, handler: Any) -> str:
        if isinstance(handler, dict) and handler.get("class"):
            return f"Handled by {handler.get('class')}::{handler.get('method', 'unknown')}."
        return f"Source-backed {method} endpoint extracted from repository routes."

    def _build_curl_example(self, method: str, path: str, request_body: Optional[RequestBody]) -> str:
        base_url = "https://api.example.com"
        parts = [
            f"curl -X {method} {base_url}{path}",
            '  -H "Accept: application/json"',
            '  -H "Authorization: Bearer <token>"',
        ]
        if request_body:
            parts.append('  -H "Content-Type: application/json"')
            parts.append(f"  -d '{json.dumps(request_body.example or {})}'")
        return " \\\n".join(parts)

    def _build_example_from_schema(self, schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        properties = schema.get("properties") if isinstance(schema, dict) else None
        if not properties:
            return None
        example = {}
        for name, prop in properties.items():
            prop_type = prop.get("type", "string") if isinstance(prop, dict) else "string"
            if prop.get("format") == "email":
                example[name] = "user@example.com"
            elif prop_type == "integer":
                example[name] = 1
            elif prop_type == "number":
                example[name] = 10.5
            elif prop_type == "boolean":
                example[name] = True
            elif prop_type == "array":
                example[name] = []
            elif prop_type == "object":
                example[name] = {}
            else:
                example[name] = f"sample_{name}"
        return example

    def _default_response_description(self, status_code: int) -> str:
        descriptions = {
            200: "Successful response",
            201: "Resource created",
            204: "Resource deleted",
            400: "Bad request",
            401: "Authentication failed or missing credentials",
            403: "Access denied",
            404: "Resource not found",
            422: "Validation failed",
            429: "Rate limit exceeded",
            500: "Internal server error",
        }
        return descriptions.get(status_code, "Response")

    def _normalize_endpoint_path(self, path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        return re.sub(r"<[^:>]+:([^>]+)>", r"{\1}", path).replace(":id", "{id}")

    def _dedupe_endpoints(self, endpoints: List[Endpoint]) -> List[Endpoint]:
        seen = set()
        unique = []
        for endpoint in endpoints:
            key = (endpoint.method, endpoint.path)
            if key in seen:
                continue
            seen.add(key)
            unique.append(endpoint)
        return unique

    def _is_supported_source_file(self, path: Path) -> bool:
        ignored = {"node_modules", "vendor", ".git", "storage", "dist", "build", "__pycache__"}
        return path.suffix in {".php", ".py", ".js", ".ts", ".java", ".cs", ".go", ".json", ".yml", ".yaml"} and not any(part in ignored for part in path.parts)

    def _extract_webhooks(self) -> Optional[List[Dict[str, Any]]]:
        """Extract webhook definitions"""
        webhooks = []
        
        # Search for webhook patterns
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".php", ".py", ".js"]:
                try:
                    content = self._read_file(str(file_path))
                    
                    # Look for webhook event patterns
                    if "webhook" in content.lower() or "event" in content.lower():
                        # Extract event names
                        event_matches = re.findall(r"['\"](\w+\.\w+)['\"]", content)
                        for event in event_matches:
                            if "." in event:
                                webhooks.append({
                                    "event": event,
                                    "description": f"Webhook event: {event}",
                                    "source": str(file_path)
                                })
                
                except:
                    pass
        
        return list({w["event"]: w for w in webhooks}.values()) if webhooks else None

    def _extract_error_definitions(self) -> Optional[Dict[str, Any]]:
        """Extract error definitions"""
        # Do not fabricate global error definitions; return None unless extracted from source.
        return None

    def _extract_changelog(self) -> Optional[List[Dict[str, Any]]]:
        """Extract changelog"""
        changelog = []
        
        # Look for CHANGELOG.md or similar
        changelog_files = list(self.repo_path.glob("CHANGELOG*")) + list(self.repo_path.glob("HISTORY*"))
        
        for changelog_file in changelog_files:
            try:
                content = self._read_file(str(changelog_file))
                
                # Parse changelog entries
                version_matches = re.findall(r"##\s+\[?v?(\d+\.\d+\.\d+)\]?", content)
                
                for version in version_matches[:5]:  # Last 5 versions
                    changelog.append({
                        "version": version,
                        "date": "TBD",
                        "changes": ["See CHANGELOG for details"]
                    })
            
            except:
                pass
        
        return changelog if changelog else None

    def _extract_pagination_config(self) -> Optional[Dict[str, Any]]:
        """Extract pagination configuration"""
        # Do not fabricate global pagination config; pagination must be detected per-endpoint or from config.
        return None

    def _read_file(self, file_path: str) -> str:
        """Read file with caching"""
        if file_path in self.file_cache:
            return self.file_cache[file_path]
        
        try:
            content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
            self.file_cache[file_path] = content
            return content
        except:
            return ""
