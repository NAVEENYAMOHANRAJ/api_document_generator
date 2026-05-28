from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class RepositoryScanRequest(BaseModel):
    repo_url: str
    github_token: Optional[str] = None


class LocalFolderScanRequest(BaseModel):
    folder_path: str


class RepositoryScanResult(BaseModel):
    status: str
    framework_candidates: List[str]
    backend_files: List[str]
    total_candidate_files: int


class JobCreationResponse(BaseModel):
    status: str
    job_id: str


# Production-level API metadata models

class ContactInfo(BaseModel):
    """Contact information"""
    name: Optional[str] = None
    email: Optional[str] = None
    url: Optional[str] = None


class License(BaseModel):
    """License information"""
    name: str
    url: Optional[str] = None


class APIMetadata(BaseModel):
    """API-level metadata"""
    name: str
    description: str
    version: str
    framework: str
    base_url: str
    openapi_version: str = "3.1.0"
    contact: Optional[ContactInfo] = None
    license: Optional[License] = None
    terms_of_service: Optional[str] = None


class Authentication(BaseModel):
    """Authentication configuration"""
    type: str
    scheme: str
    header: str
    format: str
    description: Optional[str] = None


class Environment(BaseModel):
    """Environment configuration"""
    name: str
    url: str
    description: Optional[str] = None


class WebhookEvent(BaseModel):
    """Webhook event definition"""
    event: str
    description: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None


class ErrorDefinition(BaseModel):
    """Error response definition"""
    code: str
    status_code: int
    message: str
    description: Optional[str] = None


class ChangelogEntry(BaseModel):
    """Changelog entry"""
    version: str
    date: Optional[str] = None
    changes: List[str]


class ProductionAPIDocumentation(BaseModel):
    """Complete production-grade API documentation"""
    api: APIMetadata
    authentication: Optional[List[Authentication]] = None
    environments: Optional[List[Environment]] = None
    rate_limits: Optional[Dict[str, Any]] = None
    global_headers: Optional[List[Dict[str, Any]]] = None
    versioning: Optional[Dict[str, Any]] = None
    endpoints: Optional[List[Dict[str, Any]]] = None
    schemas: Optional[Dict[str, Any]] = None
    webhooks: Optional[List[WebhookEvent]] = None
    errors: Optional[List[ErrorDefinition]] = None
    changelog: Optional[List[ChangelogEntry]] = None

