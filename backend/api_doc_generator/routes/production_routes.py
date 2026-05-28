"""
Production-Grade API Routes - Exposes all production-level extraction features.

Endpoints:
- POST /extract - Extract complete API documentation
- GET /extract/{job_id} - Get extraction results
- GET /extract/{job_id}/openapi - Get OpenAPI spec
- GET /extract/{job_id}/markdown - Get Markdown documentation
- GET /extract/{job_id}/html - Get HTML documentation
- GET /extract/{job_id}/stats - Get extraction statistics
"""

import json
import uuid
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel

from api_doc_generator.extractors.laravel_extractor import LaravelExtractor
from api_doc_generator.extractors.production_data_extractor import ProductionDataExtractor
from api_doc_generator.generators.production_openapi_generator import ProductionOpenAPIGenerator
from api_doc_generator.services.local_code_service import LocalCodeService
from api_doc_generator.scanner.backend_detector import BackendFileDetector, FrameworkCandidateDetector
from api_doc_generator.models.api_models import ProductionAPIDocumentation


router = APIRouter(prefix="/production", tags=["Production API"])

# In-memory job storage (in production, use database)
jobs: Dict[str, Dict[str, Any]] = {}


class ExtractRequest(BaseModel):
    """Production extraction request"""
    repo_path: str
    framework: Optional[str] = None


class ExtractionJob:
    """Represents an extraction job"""
    
    def __init__(self, job_id: str, repo_path: str, framework: Optional[str] = None):
        self.job_id = job_id
        self.repo_path = Path(repo_path)
        self.framework = framework
        self.status = "pending"
        self.endpoints = []
        self.api_metadata = {}
        self.authentication = None
        self.environments = None
        self.rate_limits = None
        self.global_headers = None
        self.versioning = None
        self.webhooks = None
        self.errors = None
        self.changelog = None
        self.schemas = None
        self.openapi_spec = None
        self.markdown_doc = None
        self.html_doc = None
        self.stats = {}
        self.error = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "job_id": self.job_id,
            "status": self.status,
            "framework": self.framework,
            "endpoints_count": len(self.endpoints),
            "api_metadata": self.api_metadata,
            "stats": self.stats,
            "error": self.error
        }


@router.post("/extract")
async def extract_production_api(
    request: ExtractRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Extract complete production-grade API documentation.
    
    Returns job ID for async processing.
    """
    
    # Validate repo path
    repo_path = Path(request.repo_path)
    if not repo_path.exists():
        raise HTTPException(status_code=400, detail="Repository path does not exist")
    
    # Create job
    job_id = str(uuid.uuid4())
    job = ExtractionJob(job_id, str(repo_path), request.framework)
    jobs[job_id] = job
    
    # Start extraction in background
    background_tasks.add_task(
        _extract_production_documentation,
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
async def get_extraction_result(job_id: str) -> Dict[str, Any]:
    """Get extraction results"""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    return {
        "job_id": job_id,
        "status": job.status,
        "framework": job.framework,
        "endpoints_count": len(job.endpoints),
        "api_metadata": job.api_metadata,
        "stats": job.stats,
        "error": job.error
    }


@router.get("/extract/{job_id}/openapi")
async def get_openapi_spec(job_id: str) -> Dict[str, Any]:
    """Get OpenAPI specification"""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Extraction not completed")
    
    if not job.openapi_spec:
        raise HTTPException(status_code=400, detail="OpenAPI spec not generated")
    
    return job.openapi_spec


@router.get("/extract/{job_id}/markdown")
async def get_markdown_documentation(job_id: str) -> Dict[str, str]:
    """Get Markdown documentation"""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Extraction not completed")
    
    if not job.markdown_doc:
        raise HTTPException(status_code=400, detail="Markdown documentation not generated")
    
    return {"markdown": job.markdown_doc}


@router.get("/extract/{job_id}/html")
async def get_html_documentation(job_id: str) -> Dict[str, str]:
    """Get HTML documentation"""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Extraction not completed")
    
    if not job.html_doc:
        raise HTTPException(status_code=400, detail="HTML documentation not generated")
    
    return {"html": job.html_doc}


@router.get("/extract/{job_id}/stats")
async def get_extraction_stats(job_id: str) -> Dict[str, Any]:
    """Get extraction statistics"""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    return {
        "job_id": job_id,
        "status": job.status,
        "framework": job.framework,
        "endpoints_count": len(job.endpoints),
        "stats": job.stats,
        "error": job.error
    }


# Background task

def _extract_production_documentation(job_id: str, repo_path: str, framework: Optional[str]):
    """Extract production documentation (background task)"""
    
    job = jobs[job_id]
    job.status = "processing"
    
    try:
        repo_path_obj = Path(repo_path)
        
        # Detect framework if not provided
        if not framework:
            detector = FrameworkCandidateDetector()
            candidates = detector.detect_frameworks(repo_path)
            if candidates:
                framework = list(candidates.keys())[0]
            else:
                framework = "Unknown"
        
        job.framework = framework
        
        # Extract endpoints
        endpoints = _extract_endpoints(repo_path, framework)
        job.endpoints = endpoints
        
        # Extract production data
        extractor = ProductionDataExtractor(repo_path_obj, framework)
        
        job.api_metadata = extractor.extract_api_metadata()
        job.authentication = extractor.extract_authentication()
        job.environments = extractor.extract_environments()
        job.rate_limits = extractor.extract_rate_limits()
        job.global_headers = extractor.extract_global_headers()
        job.versioning = extractor.extract_versioning()
        job.webhooks = extractor.extract_webhooks()
        job.errors = extractor.extract_error_definitions()
        job.changelog = extractor.extract_changelog()
        
        # Enhance endpoints with production data
        for endpoint in job.endpoints:
            endpoint = extractor.extract_endpoint_details(endpoint)
        
        # Generate OpenAPI spec
        openapi_gen = ProductionOpenAPIGenerator(job.api_metadata)
        job.openapi_spec = openapi_gen.generate(
            endpoints=job.endpoints,
            authentication=job.authentication,
            environments=job.environments,
            rate_limits=job.rate_limits,
            global_headers=job.global_headers,
            versioning=job.versioning,
            webhooks=job.webhooks,
            errors=job.errors,
            changelog=job.changelog,
            schemas=job.schemas
        )
        
        # Generate Markdown documentation
        job.markdown_doc = _generate_markdown_documentation(job)
        
        # Generate HTML documentation
        job.html_doc = _generate_html_documentation(job)
        
        # Calculate statistics
        job.stats = {
            "total_endpoints": len(job.endpoints),
            "endpoints_by_method": _count_by_method(job.endpoints),
            "endpoints_by_tag": _count_by_tag(job.endpoints),
            "authentication_methods": len(job.authentication or []),
            "environments": len(job.environments or []),
            "error_definitions": len(job.errors or []),
            "webhooks": len(job.webhooks or []),
            "changelog_entries": len(job.changelog or [])
        }
        
        job.status = "completed"
        
    except Exception as e:
        job.status = "failed"
        job.error = str(e)


def _extract_endpoints(repo_path: str, framework: str) -> list:
    """Extract endpoints based on framework"""
    
    endpoints = []
    repo_path_obj = Path(repo_path)
    
    if framework == "Laravel":
        # Extract Laravel routes
        routes_files = list(repo_path_obj.glob("routes/*.php"))
        
        for routes_file in routes_files:
            try:
                content = routes_file.read_text()
                extracted = LaravelExtractor.extract(str(routes_file), content, repo_path)
                endpoints.extend(extracted)
            except Exception as e:
                print(f"Error extracting from {routes_file}: {e}")
    
    # Add more framework extractors as needed
    
    return endpoints


def _generate_markdown_documentation(job: ExtractionJob) -> str:
    """Generate Markdown documentation"""
    
    md = f"# {job.api_metadata.get('name', 'API')} Documentation\n\n"
    md += f"{job.api_metadata.get('description', '')}\n\n"
    md += f"**Version:** {job.api_metadata.get('version', 'v1')}\n\n"
    
    # Authentication
    if job.authentication:
        md += "## Authentication\n\n"
        for auth in job.authentication:
            md += f"- **{auth.get('type')}**: {auth.get('description', '')}\n"
        md += "\n"
    
    # Endpoints
    md += "## Endpoints\n\n"
    
    for endpoint in job.endpoints:
        method = endpoint.get("method", "GET")
        path = endpoint.get("path", "/")
        summary = endpoint.get("summary", "")
        
        md += f"### {method} {path}\n\n"
        md += f"{summary}\n\n"
        
        if endpoint.get("description"):
            md += f"{endpoint['description']}\n\n"
        
        # Parameters
        if endpoint.get("path_parameters"):
            md += "**Path Parameters:**\n\n"
            for param in endpoint["path_parameters"]:
                md += f"- `{param.get('name')}` ({param.get('type')}): {param.get('description', '')}\n"
            md += "\n"
        
        # Request body
        if endpoint.get("request_body"):
            md += "**Request Body:**\n\n"
            md += "```json\n"
            md += json.dumps(endpoint["request_body"].get("example", {}), indent=2)
            md += "\n```\n\n"
        
        # Responses
        if endpoint.get("responses"):
            md += "**Responses:**\n\n"
            for response in endpoint["responses"]:
                md += f"- `{response.get('status_code')}`: {response.get('description', '')}\n"
            md += "\n"
        
        # cURL example
        if endpoint.get("curl_example"):
            md += "**Example:**\n\n"
            md += "```bash\n"
            md += endpoint["curl_example"]
            md += "\n```\n\n"
    
    return md


def _generate_html_documentation(job: ExtractionJob) -> str:
    """Generate HTML documentation"""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{job.api_metadata.get('name', 'API')} Documentation</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .endpoint {{ border: 1px solid #ddd; padding: 10px; margin: 10px 0; }}
            .method {{ font-weight: bold; color: #0066cc; }}
            code {{ background: #f4f4f4; padding: 2px 5px; }}
            pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>{job.api_metadata.get('name', 'API')} Documentation</h1>
        <p>{job.api_metadata.get('description', '')}</p>
        <p><strong>Version:</strong> {job.api_metadata.get('version', 'v1')}</p>
    """
    
    # Authentication
    if job.authentication:
        html += "<h2>Authentication</h2><ul>"
        for auth in job.authentication:
            html += f"<li><strong>{auth.get('type')}</strong>: {auth.get('description', '')}</li>"
        html += "</ul>"
    
    # Endpoints
    html += "<h2>Endpoints</h2>"
    
    for endpoint in job.endpoints:
        method = endpoint.get("method", "GET")
        path = endpoint.get("path", "/")
        summary = endpoint.get("summary", "")
        
        html += f"""
        <div class="endpoint">
            <h3><span class="method">{method}</span> {path}</h3>
            <p>{summary}</p>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    
    return html


def _count_by_method(endpoints: list) -> Dict[str, int]:
    """Count endpoints by HTTP method"""
    counts = {}
    for endpoint in endpoints:
        method = endpoint.get("method", "GET")
        counts[method] = counts.get(method, 0) + 1
    return counts


def _count_by_tag(endpoints: list) -> Dict[str, int]:
    """Count endpoints by tag"""
    counts = {}
    for endpoint in endpoints:
        tags = endpoint.get("tags", [])
        for tag in tags:
            counts[tag] = counts.get(tag, 0) + 1
    return counts
