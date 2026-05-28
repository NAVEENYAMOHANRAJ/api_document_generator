"""Enhanced API routes with database integration and caching."""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from api_doc_generator.models.database_models import get_db, init_db
from api_doc_generator.services.database_service import DatabaseService
from api_doc_generator.services.endpoint_storage import hydrate_endpoint_from_db


def _serialize_endpoint(ep) -> dict:
    row = {
        "id": ep.id,
        "method": ep.method,
        "path": ep.path,
        "description": ep.description,
        "source_file": ep.source_file,
        "function_name": ep.function_name,
        "path_params": ep.path_params,
        "query_params": ep.query_params,
        "request_body": ep.request_body,
        "response_model": ep.response_model,
        "responses": ep.responses,
        "tags": ep.tags,
        "confidence": ep.confidence / 100,
        "provenance": ep.provenance,
    }
    return hydrate_endpoint_from_db(row)
from api_doc_generator.routes.api_doc_routes import (
    scan_repository,
    extract_endpoints,
    extract_local_folder,
    extract_upload,
)

router = APIRouter()

# Initialize database on startup
init_db()


@router.get("/api/jobs")
def get_jobs(limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    """Get recent extraction jobs."""
    jobs = DatabaseService.get_job_history(db, limit=limit)
    return {
        "status": "success",
        "jobs": [
            {
                "job_id": job.job_id,
                "repo_url": job.repo_url,
                "repo_name": job.repo_name,
                "status": job.status,
                "total_endpoints": job.total_endpoints,
                "processed_files": job.processed_files,
                "failed_files": job.failed_files,
                "created_at": job.created_at.isoformat(),
                "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            }
            for job in jobs
        ],
    }


@router.get("/api/jobs/{job_id}")
def get_job_details(job_id: str, db: Session = Depends(get_db)):
    """Get detailed information about a job."""
    job = DatabaseService.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    endpoints = DatabaseService.get_endpoints(db, job_id)
    documentation = DatabaseService.get_documentation(db, job_id)

    return {
        "status": "success",
        "job": {
            "job_id": job.job_id,
            "repo_url": job.repo_url,
            "repo_name": job.repo_name,
            "status": job.status,
            "total_endpoints": job.total_endpoints,
            "processed_files": job.processed_files,
            "failed_files": job.failed_files,
            "errors": job.errors,
            "metadata": job.job_metadata,
            "created_at": job.created_at.isoformat(),
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        },
        "endpoints": [_serialize_endpoint(ep) for ep in endpoints],
        "documentation": {
            "openapi_spec": documentation.openapi_spec if documentation else None,
            "markdown_doc": documentation.markdown_doc if documentation else None,
            "html_doc": documentation.html_doc if documentation else None,
        } if documentation else None,
    }


@router.get("/api/jobs/{job_id}/endpoints")
def get_job_endpoints(
    job_id: str,
    method: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db),
):
    """Get endpoints for a job with optional filtering."""
    job = DatabaseService.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if search:
        endpoints = DatabaseService.search_endpoints(db, job_id, search)
    elif method:
        endpoints = DatabaseService.get_endpoints_by_method(db, job_id, method)
    else:
        endpoints = DatabaseService.get_endpoints(db, job_id)

    return {
        "status": "success",
        "job_id": job_id,
        "total": len(endpoints),
        "endpoints": [_serialize_endpoint(ep) for ep in endpoints],
    }


@router.get("/api/jobs/{job_id}/documentation")
def get_job_documentation(job_id: str, format: str = Query("html"), db: Session = Depends(get_db)):
    """Get generated documentation for a job."""
    job = DatabaseService.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    documentation = DatabaseService.get_documentation(db, job_id)
    if not documentation:
        raise HTTPException(status_code=404, detail="Documentation not found")

    if format == "openapi":
        return documentation.openapi_spec
    elif format == "markdown":
        return {"content": documentation.markdown_doc}
    else:  # html
        return {"content": documentation.html_doc}


@router.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get database statistics."""
    stats = DatabaseService.get_stats(db)
    return {
        "status": "success",
        "stats": stats,
    }


@router.post("/api/extract-with-cache")
def extract_with_cache(
    repo_url: str = Query(...),
    github_token: str = Query(None),
    use_cache: bool = Query(True),
    db: Session = Depends(get_db),
):
    """Extract endpoints with caching support."""
    cache_key = f"extraction:{repo_url}"

    # Check cache if enabled
    if use_cache:
        cached = DatabaseService.cache_get(db, cache_key)
        if cached:
            return {
                "status": "success",
                "from_cache": True,
                "data": cached,
            }

    # Create job
    repo_name = repo_url.split("/")[-1]
    job_id = DatabaseService.create_job(db, repo_url, repo_name)

    # Extract endpoints (this would call the actual extraction logic)
    # For now, return job ID for polling
    return {
        "status": "processing",
        "job_id": job_id,
        "from_cache": False,
    }


@router.get("/api/methods-summary/{job_id}")
def get_methods_summary(job_id: str, db: Session = Depends(get_db)):
    """Get summary of HTTP methods used in endpoints."""
    endpoints = DatabaseService.get_endpoints(db, job_id)
    
    methods_summary = {}
    for ep in endpoints:
        method = ep.method
        if method not in methods_summary:
            methods_summary[method] = 0
        methods_summary[method] += 1

    return {
        "status": "success",
        "job_id": job_id,
        "methods_summary": methods_summary,
        "total_endpoints": len(endpoints),
    }


@router.get("/api/tags-summary/{job_id}")
def get_tags_summary(job_id: str, db: Session = Depends(get_db)):
    """Get summary of tags used in endpoints."""
    endpoints = DatabaseService.get_endpoints(db, job_id)
    
    tags_summary = {}
    for ep in endpoints:
        for tag in ep.tags:
            if tag not in tags_summary:
                tags_summary[tag] = 0
            tags_summary[tag] += 1

    return {
        "status": "success",
        "job_id": job_id,
        "tags_summary": tags_summary,
        "total_tags": len(tags_summary),
    }
