"""Service for database operations."""

import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from api_doc_generator.models.database_models import (
    ExtractionJob,
    Endpoint,
    Documentation,
    Cache,
)


class DatabaseService:
    """Handle all database operations."""

    @staticmethod
    def create_job(db: Session, repo_url: str, repo_name: str) -> str:
        """Create a new extraction job."""
        job_id = str(uuid.uuid4())
        job = ExtractionJob(
            job_id=job_id,
            repo_url=repo_url,
            repo_name=repo_name,
            status="pending",
        )
        try:
            db.add(job)
            db.commit()
            db.refresh(job)
            print(f"[Database] Created job: {job_id}", flush=True)
            return job_id
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_job(db: Session, job_id: str) -> Optional[ExtractionJob]:
        """Get job by ID."""
        return db.query(ExtractionJob).filter(ExtractionJob.job_id == job_id).first()

    @staticmethod
    def update_job(
        db: Session,
        job_id: str,
        status: str,
        total_endpoints: int = 0,
        processed_files: int = 0,
        failed_files: int = 0,
        errors: List = None,
        metadata: dict = None,
    ):
        """Update job status and metadata."""
        try:
            job = db.query(ExtractionJob).filter(ExtractionJob.job_id == job_id).first()
            if job:
                job.status = status
                if total_endpoints is not None:
                    job.total_endpoints = total_endpoints
                if processed_files is not None:
                    job.processed_files = processed_files
                if failed_files is not None:
                    job.failed_files = failed_files
                if errors is not None:
                    job.errors = errors
                if metadata is not None:
                    job.job_metadata = metadata
                if status in ("completed", "failed"):
                    job.completed_at = datetime.utcnow()
                db.commit()
                db.refresh(job)
                print(f"[Database] Updated job {job_id}: {status}", flush=True)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def save_endpoints(db: Session, job_id: str, endpoints: List[dict]):
        """Save extracted endpoints."""
        from api_doc_generator.services.endpoint_storage import prepare_endpoint_for_storage

        try:
            # Delete any existing endpoints for this job to support retries cleanly
            db.query(Endpoint).filter(Endpoint.job_id == job_id).delete()
            for endpoint in endpoints:
                endpoint = prepare_endpoint_for_storage(endpoint)
                conf_val = endpoint.get("confidence")
                if conf_val is None:
                    confidence = 85
                elif isinstance(conf_val, (float, int)):
                    if conf_val <= 1.0:
                        confidence = int(conf_val * 100)
                    else:
                        confidence = int(conf_val)
                else:
                    try:
                        f_val = float(conf_val)
                        if f_val <= 1.0:
                            confidence = int(f_val * 100)
                        else:
                            confidence = int(f_val)
                    except ValueError:
                        confidence = 85

                db_endpoint = Endpoint(
                    job_id=job_id,
                    method=endpoint.get("method", "GET"),
                    path=endpoint.get("path", ""),
                    description=endpoint.get("description"),
                    source_file=endpoint.get("source_file", ""),
                    function_name=endpoint.get("function_name"),
                    path_params=endpoint.get("path_params", []),
                    query_params=endpoint.get("query_params", []),
                    request_body=endpoint.get("request_body"),
                    response_model=endpoint.get("response_model"),
                    responses=endpoint.get("responses", []),
                    tags=endpoint.get("tags", []),
                    deprecated=endpoint.get("deprecated", False),
                    confidence=confidence,
                    provenance=endpoint.get("provenance"),
                )
                db.add(db_endpoint)
            db.commit()
            print(f"[Database] Saved {len(endpoints)} endpoints for job {job_id}", flush=True)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_endpoints(db: Session, job_id: str) -> List[Endpoint]:
        """Get all endpoints for a job."""
        return db.query(Endpoint).filter(Endpoint.job_id == job_id).all()

    @staticmethod
    def get_endpoints_by_method(db: Session, job_id: str, method: str) -> List[Endpoint]:
        """Get endpoints filtered by HTTP method."""
        return (
            db.query(Endpoint)
            .filter(Endpoint.job_id == job_id, Endpoint.method == method.upper())
            .all()
        )

    @staticmethod
    def search_endpoints(db: Session, job_id: str, query: str) -> List[Endpoint]:
        """Search endpoints by path or description."""
        return (
            db.query(Endpoint)
            .filter(
                Endpoint.job_id == job_id,
                (Endpoint.path.ilike(f"%{query}%") | Endpoint.description.ilike(f"%{query}%")),
            )
            .all()
        )

    @staticmethod
    def save_documentation(db: Session, job_id: str, openapi_spec: dict, markdown_doc: str, html_doc: str):
        """Save generated documentation."""
        try:
            db.query(Documentation).filter(Documentation.job_id == job_id).delete()
            doc = Documentation(
                job_id=job_id,
                openapi_spec=openapi_spec,
                markdown_doc=markdown_doc,
                html_doc=html_doc,
            )
            db.add(doc)
            db.commit()
            db.refresh(doc)
            print(f"[Database] Saved documentation for job {job_id}", flush=True)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_documentation(db: Session, job_id: str) -> Optional[Documentation]:
        """Get documentation for a job."""
        return db.query(Documentation).filter(Documentation.job_id == job_id).first()

    @staticmethod
    def cache_set(db: Session, key: str, data: dict, ttl_hours: int = 24):
        """Set cache value."""
        try:
            expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
            
            # Delete existing cache entry if it exists
            db.query(Cache).filter(Cache.cache_key == key).delete()
            
            cache = Cache(cache_key=key, data=data, expires_at=expires_at)
            db.add(cache)
            db.commit()
            print(f"[Database] Cached: {key}", flush=True)
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def cache_get(db: Session, key: str) -> Optional[dict]:
        """Get cache value if not expired."""
        try:
            cache = db.query(Cache).filter(Cache.cache_key == key).first()
            if cache and cache.expires_at > datetime.utcnow():
                print(f"[Database] Cache hit: {key}", flush=True)
                return cache.data
            elif cache:
                # Delete expired cache
                db.delete(cache)
                db.commit()
            return None
        except Exception:
            db.rollback()
            return None

    @staticmethod
    def get_job_history(db: Session, limit: int = 50) -> List[ExtractionJob]:
        """Get recent extraction jobs."""
        return (
            db.query(ExtractionJob)
            .order_by(ExtractionJob.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_stats(db: Session) -> dict:
        """Get database statistics."""
        total_jobs = db.query(ExtractionJob).count()
        completed_jobs = db.query(ExtractionJob).filter(ExtractionJob.status == "completed").count()
        total_endpoints = db.query(Endpoint).count()
        
        return {
            "total_jobs": total_jobs,
            "completed_jobs": completed_jobs,
            "total_endpoints": total_endpoints,
        }

    @staticmethod
    def diff_endpoints(db: Session, base_job_id: str, head_job_id: str) -> dict:
        """
        Compare endpoints between two job runs (e.g., base and head).
        Returns a dict containing lists of added, removed, and modified endpoints.
        """
        base_eps = db.query(Endpoint).filter(Endpoint.job_id == base_job_id).all()
        head_eps = db.query(Endpoint).filter(Endpoint.job_id == head_job_id).all()
        
        base_map = {(ep.method.upper(), ep.path): ep for ep in base_eps}
        head_map = {(ep.method.upper(), ep.path): ep for ep in head_eps}
        
        added = []
        removed = []
        modified = []
        
        # Check for added and modified
        for key, head_ep in head_map.items():
            if key not in base_map:
                added.append({
                    "method": head_ep.method,
                    "path": head_ep.path,
                    "description": head_ep.description,
                    "source_file": head_ep.source_file
                })
            else:
                base_ep = base_map[key]
                # Check if modified
                is_modified = False
                changes = {}
                
                if head_ep.description != base_ep.description:
                    is_modified = True
                    changes["description"] = {"old": base_ep.description, "new": head_ep.description}
                    
                if head_ep.path_params != base_ep.path_params:
                    is_modified = True
                    changes["path_params"] = {"old": base_ep.path_params, "new": head_ep.path_params}
                    
                if head_ep.query_params != base_ep.query_params:
                    is_modified = True
                    changes["query_params"] = {"old": base_ep.query_params, "new": head_ep.query_params}
                    
                if head_ep.request_body != base_ep.request_body:
                    is_modified = True
                    changes["request_body"] = {"old": base_ep.request_body, "new": head_ep.request_body}
                    
                if head_ep.responses != base_ep.responses:
                    is_modified = True
                    changes["responses"] = {"old": base_ep.responses, "new": head_ep.responses}
                    
                if is_modified:
                    modified.append({
                        "method": head_ep.method,
                        "path": head_ep.path,
                        "changes": changes,
                        "source_file": head_ep.source_file
                    })
                    
        # Check for removed
        for key, base_ep in base_map.items():
            if key not in head_map:
                removed.append({
                    "method": base_ep.method,
                    "path": base_ep.path,
                    "description": base_ep.description,
                    "source_file": base_ep.source_file
                })
                
        return {
            "added": added,
            "removed": removed,
            "modified": modified
        }


