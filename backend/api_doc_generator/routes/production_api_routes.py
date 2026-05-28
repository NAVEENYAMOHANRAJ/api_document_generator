"""
Production-Grade API Routes - Integrated with FastAPI
"""

from dataclasses import asdict, is_dataclass

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import io
from pathlib import Path

from api_doc_generator.extractors.production_extractor import ProductionExtractor
from api_doc_generator.services.repository_service import RepositoryService

router = APIRouter(prefix="/v1/production", tags=["Production API"])
repo_service = RepositoryService()


class AnalyzeRequest(BaseModel):
    source: str
    cleanup: bool = True


@router.post("/analyze")
async def analyze_repository(request: AnalyzeRequest):
    """Analyze repository and extract complete API documentation"""
    try:
        # Get or clone repository
        repo_path, repo_type = repo_service.get_or_clone_repository(request.source)
        
        # Validate repository
        is_valid, framework = repo_service.validate_repository(repo_path)
        if not is_valid:
            if request.cleanup and repo_type == "cloned":
                repo_service.cleanup_repository(repo_path)
            raise HTTPException(status_code=400, detail=f"Invalid repository: {framework}")
        
        # Extract documentation
        extractor = ProductionExtractor(repo_path)
        documentation = extractor.extract_complete_documentation()
        
        # Get repository info
        repo_info = repo_service.get_repository_info(repo_path)
        git_info = repo_service.get_git_info(repo_path)
        
        # Serialize documentation
        doc_dict = _serialize_documentation(documentation)
        
        # Cleanup if requested
        if request.cleanup and repo_type == "cloned":
            repo_service.cleanup_repository(repo_path)
        
        return {
            "status": "success",
            "documentation": doc_dict,
            "metadata": {
                "repository": repo_info,
                "git": git_info,
                "framework": framework,
                "source_type": repo_type
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export-openapi")
async def export_openapi(data: Dict[str, Any]):
    """Export documentation as OpenAPI 3.1.0"""
    try:
        documentation = data.get("documentation")
        if not documentation:
            raise HTTPException(status_code=400, detail="documentation is required")
        
        openapi_spec = _generate_openapi_spec(documentation)
        return openapi_spec
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "Production API Documentation Generator",
        "version": "1.0.0"
    }


def _serialize_documentation(doc) -> Dict[str, Any]:
    """Serialize documentation object to dict"""
    result = asdict(doc) if is_dataclass(doc) else dict(doc)
    result["rateLimits"] = result.get("rate_limits")
    result["globalHeaders"] = result.get("global_headers")
    for endpoint in result.get("endpoints") or []:
        endpoint["pathParameters"] = endpoint.get("path_parameters")
        endpoint["queryParameters"] = endpoint.get("query_parameters")
        endpoint["requestBody"] = endpoint.get("request_body")
        endpoint["requestExample"] = endpoint.get("request_example")
        endpoint["curlExample"] = endpoint.get("curl_example")
        endpoint["statusCodes"] = [
            response.get("status_code")
            for response in endpoint.get("responses") or []
            if response.get("status_code")
        ]
    return result


def _generate_openapi_spec(documentation: Dict[str, Any]) -> Dict[str, Any]:
    """Generate OpenAPI 3.1.0 specification"""
    api = documentation.get('api', {})
    
    spec = {
        'openapi': '3.1.0',
        'info': {
            'title': api.get('name', 'API'),
            'description': api.get('description', ''),
            'version': api.get('version', '1.0.0'),
            'contact': api.get('contact', {}),
            'license': api.get('license', {})
        },
        'servers': [
            {'url': env['url'], 'description': env.get('description', '')}
            for env in documentation.get('environments', [])
        ],
        'paths': {},
        'components': {
            'schemas': documentation.get('schemas', {}),
            'securitySchemes': _generate_security_schemes(documentation.get('authentication', []))
        }
    }
    
    for endpoint in documentation.get('endpoints', []):
        path = endpoint['path']
        method = endpoint['method'].lower()
        
        if path not in spec['paths']:
            spec['paths'][path] = {}
        
        spec['paths'][path][method] = {
            'summary': endpoint.get('summary', ''),
            'description': endpoint.get('description', ''),
            'tags': endpoint.get('tags', []),
            'deprecated': endpoint.get('deprecated', False),
            'security': endpoint.get('security', []),
            'parameters': _generate_parameters(endpoint),
            'requestBody': _generate_request_body(endpoint.get('request_body') or endpoint.get('requestBody')),
            'responses': _generate_responses(endpoint),
        }
    
    return spec


def _generate_parameters(endpoint: Dict[str, Any]) -> list:
    params = []
    for location, key in (("path", "path_parameters"), ("query", "query_parameters"), ("header", "headers")):
        for param in endpoint.get(key) or endpoint.get(key.replace("_", "")) or []:
            params.append({
                "name": param.get("name"),
                "in": param.get("in") or location,
                "required": bool(param.get("required") or location == "path"),
                "description": param.get("description") or "",
                "schema": {
                    "type": param.get("param_type") or param.get("type") or "string",
                    **({"default": param.get("default")} if param.get("default") is not None else {}),
                },
            })
    return params


def _generate_request_body(request_body: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not request_body:
        return None
    schema = request_body.get("schema") or request_body
    return {
        "required": bool(request_body.get("required", True)),
        "content": {
            request_body.get("content_type", "application/json"): {
                "schema": schema,
                **({"example": request_body.get("example")} if request_body.get("example") else {}),
            }
        },
    }


def _generate_responses(endpoint: Dict[str, Any]) -> Dict[str, Any]:
    responses = {}
    for response in endpoint.get("responses") or []:
        code = str(response.get("status_code") or 200)
        responses[code] = {
            "description": response.get("description") or "Response",
            **({"content": {"application/json": {"schema": response.get("schema")}}} if response.get("schema") else {}),
        }
    return responses or {"200": {"description": "Successful response"}}


def _generate_security_schemes(auth_methods: list) -> Dict[str, Any]:
    """Generate OpenAPI security schemes"""
    schemes = {}
    
    for auth in auth_methods:
        if auth['type'] in ['Bearer Token', 'JWT']:
            schemes['bearerAuth'] = {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT'
            }
        elif auth['type'] == 'API Key':
            schemes['apiKeyAuth'] = {
                'type': 'apiKey',
                'in': 'header',
                'name': 'X-API-Key'
            }
    
    return schemes
