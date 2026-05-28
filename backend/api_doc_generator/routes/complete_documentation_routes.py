"""
Complete Production Documentation Routes - Returns all 30+ data points in structured format.
"""

import json
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from api_doc_generator.extractors.laravel_extractor import LaravelExtractor
from api_doc_generator.extractors.production_data_extractor import ProductionDataExtractor
from api_doc_generator.generators.production_openapi_generator import ProductionOpenAPIGenerator
from api_doc_generator.scanner.backend_detector import FrameworkCandidateDetector


router = APIRouter(tags=["Complete Documentation"])

# In-memory job storage
jobs: Dict[str, Dict[str, Any]] = {}


class ExtractRequest(BaseModel):
    """Production extraction request"""
    repo_path: str
    framework: Optional[str] = None


class CompleteDocumentation:
    """Complete production documentation with all 30+ data points"""
    
    def __init__(self, job_id: str, repo_path: str, framework: Optional[str] = None):
        self.job_id = job_id
        self.repo_path = Path(repo_path)
        self.framework = framework
        self.status = "pending"
        
        # API Level (9 points)
        self.api_name = ""
        self.api_description = ""
        self.api_version = ""
        self.framework_name = ""
        self.base_url = ""
        self.contact_info = {}
        self.license_info = {}
        self.terms_of_service = ""
        self.openapi_version = "3.1.0"
        
        # Infrastructure (7 points)
        self.authentication = []  # Bearer, JWT, OAuth2, API Key, Session, Sanctum, Passport
        self.environments = []  # Development, Staging, Production
        self.rate_limits = {}
        self.global_headers = []
        self.versioning = {}
        self.webhooks = []
        self.error_definitions = []
        self.changelog = []
        
        # Per-Endpoint (20+ points)
        self.endpoints = []
        self.schemas = {}
        
        # Statistics
        self.stats = {
            "total_endpoints": 0,
            "endpoints_by_method": {},
            "endpoints_by_tag": {},
            "authentication_methods": 0,
            "environments_count": 0,
            "error_definitions_count": 0,
            "webhooks_count": 0,
            "changelog_entries": 0,
            "schemas_count": 0,
            "validation_rules_extracted": 0,
            "examples_generated": 0,
            "source_files_traced": 0,
            "confidence_average": 0.0
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response"""
        return {
            "job_id": self.job_id,
            "status": self.status,
            "framework": self.framework_name,
            
            # API Level (9 points)
            "api": {
                "name": self.api_name,
                "description": self.api_description,
                "version": self.api_version,
                "framework": self.framework_name,
                "baseUrl": self.base_url,
                "openapi": self.openapi_version,
                "contact": self.contact_info,
                "license": self.license_info,
                "termsOfService": self.terms_of_service
            },
            
            # Infrastructure (7 points)
            "authentication": self.authentication,
            "environments": self.environments,
            "rateLimits": self.rate_limits,
            "globalHeaders": self.global_headers,
            "versioning": self.versioning,
            "webhooks": self.webhooks,
            "errorDefinitions": self.error_definitions,
            "changelog": self.changelog,
            
            # Endpoints with all 20+ data points
            "endpoints": self.endpoints,
            "schemas": self.schemas,
            
            # Statistics
            "stats": self.stats
        }


@router.post("/extract")
async def extract_complete_documentation(
    request: ExtractRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Extract complete production-grade API documentation with all 30+ data points.
    
    Returns:
    - API metadata (9 points)
    - Authentication (1 point)
    - Environments (1 point)
    - Rate limiting (1 point)
    - Global headers (1 point)
    - Versioning (1 point)
    - Webhooks (1 point)
    - Error definitions (1 point)
    - Changelog (1 point)
    - Endpoints with 20+ data points each
    """
    
    # Validate repo path
    repo_path = Path(request.repo_path)
    if not repo_path.exists():
        raise HTTPException(status_code=400, detail="Repository path does not exist")
    
    # Create job
    job_id = str(uuid.uuid4())
    doc = CompleteDocumentation(job_id, str(repo_path), request.framework)
    jobs[job_id] = doc
    
    # Start extraction in background
    background_tasks.add_task(
        _extract_complete_documentation,
        job_id,
        str(repo_path),
        request.framework
    )
    
    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Extraction started"
    }


@router.get("/extract/{job_id}")
async def get_complete_documentation(job_id: str) -> Dict[str, Any]:
    """Get complete documentation with all 30+ data points"""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    doc = jobs[job_id]
    return doc.to_dict()


@router.get("/extract/{job_id}/document")
async def get_documentation_document(job_id: str) -> Dict[str, Any]:
    """Get documentation in document format (like the mockup)"""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    doc = jobs[job_id]
    
    # Format as document structure
    return {
        "title": f"{doc.api_name} - API Documentation",
        "sections": [
            {
                "title": "API Overview",
                "data": {
                    "name": doc.api_name,
                    "description": doc.api_description,
                    "version": doc.api_version,
                    "framework": doc.framework_name,
                    "baseUrl": doc.base_url,
                    "openapi": doc.openapi_version,
                    "contact": doc.contact_info,
                    "license": doc.license_info
                }
            },
            {
                "title": "Authentication",
                "data": doc.authentication
            },
            {
                "title": "Environments",
                "data": doc.environments
            },
            {
                "title": "Rate Limiting",
                "data": doc.rate_limits
            },
            {
                "title": "Global Headers",
                "data": doc.global_headers
            },
            {
                "title": "Versioning",
                "data": doc.versioning
            },
            {
                "title": "Webhooks",
                "data": doc.webhooks
            },
            {
                "title": "Error Definitions",
                "data": doc.error_definitions
            },
            {
                "title": "Changelog",
                "data": doc.changelog
            },
            {
                "title": "Endpoints",
                "data": doc.endpoints,
                "count": len(doc.endpoints)
            },
            {
                "title": "Schemas",
                "data": doc.schemas
            }
        ],
        "stats": doc.stats
    }


def _extract_complete_documentation(job_id: str, repo_path: str, framework: Optional[str]):
    """Extract complete documentation (background task)"""
    
    doc = jobs[job_id]
    doc.status = "processing"
    
    try:
        repo_path_obj = Path(repo_path)
        
        # Detect framework if not provided
        if not framework:
            try:
                detector = FrameworkCandidateDetector()
                candidates = detector.detect_frameworks(repo_path)
                if candidates:
                    framework = list(candidates.keys())[0]
                else:
                    framework = "Laravel"  # Default
            except Exception as e:
                print(f"Framework detection error: {e}")
                framework = "Laravel"  # Default fallback
        
        doc.framework_name = framework
        
        # Extract all production data using AST-based extraction
        extractor = ProductionDataExtractor(repo_path_obj, framework)
        
        # API Metadata (9 points)
        try:
            api_meta = extractor.extract_api_metadata()
            doc.api_name = api_meta.get("name", "API")
            doc.api_description = api_meta.get("description", "")
            doc.api_version = api_meta.get("version", "v1")
            doc.framework_name = api_meta.get("framework", framework)
            doc.base_url = api_meta.get("base_url", "https://api.example.com")
            doc.contact_info = api_meta.get("contact", {})
            doc.license_info = api_meta.get("license", {})
            doc.terms_of_service = api_meta.get("terms_of_service", "")
            doc.openapi_version = api_meta.get("openapi_version", "3.1.0")
        except Exception as e:
            print(f"API metadata extraction error: {e}")
            doc.api_name = "API"
            doc.api_version = "v1"
        
        # Infrastructure (7 points)
        try:
            doc.authentication = extractor.extract_authentication() or []
            doc.environments = extractor.extract_environments() or []
            doc.rate_limits = extractor.extract_rate_limits() or {}
            doc.global_headers = extractor.extract_global_headers() or []
            doc.versioning = extractor.extract_versioning() or {}
            doc.webhooks = extractor.extract_webhooks() or []
            doc.error_definitions = extractor.extract_error_definitions() or []
            doc.changelog = extractor.extract_changelog() or []
        except Exception as e:
            print(f"Infrastructure extraction error: {e}")
        
        # Extract endpoints using AST-based extraction (all 20+ data points)
        try:
            endpoints = extractor.extract_endpoints_ast()
            doc.endpoints = endpoints
        except Exception as e:
            print(f"Endpoints extraction error: {e}")
            doc.endpoints = []
        
        # Update statistics
        doc.stats["total_endpoints"] = len(doc.endpoints)
        doc.stats["authentication_methods"] = len(doc.authentication)
        doc.stats["environments_count"] = len(doc.environments)
        doc.stats["error_definitions_count"] = len(doc.error_definitions)
        doc.stats["webhooks_count"] = len(doc.webhooks)
        doc.stats["changelog_entries"] = len(doc.changelog)
        doc.stats["schemas_count"] = len(doc.schemas)
        
        # Count by method
        for endpoint in doc.endpoints:
            method = endpoint.get("method", "GET")
            doc.stats["endpoints_by_method"][method] = doc.stats["endpoints_by_method"].get(method, 0) + 1
            
            # Count by tag
            for tag in endpoint.get("tags", []):
                doc.stats["endpoints_by_tag"][tag] = doc.stats["endpoints_by_tag"].get(tag, 0) + 1
        
        doc.status = "completed"
        
    except Exception as e:
        import traceback
        print(f"Fatal extraction error: {e}")
        print(traceback.format_exc())
        doc.status = "failed"
        doc.error = str(e)

