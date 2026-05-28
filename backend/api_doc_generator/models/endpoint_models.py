from typing import Any, Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class AttributionType(str, Enum):
    """Attribution type for metadata"""
    DETECTED = "detected"
    INFERRED = "inferred"
    SYNTHETIC = "synthetic"


class Attribution(BaseModel):
    """Attribution metadata for any field"""
    type: AttributionType
    confidence: float = Field(ge=0.0, le=1.0)
    source_file: Optional[str] = None
    line_number: Optional[int] = None
    inference_method: Optional[str] = None


class Parameter(BaseModel):
    """Request/response parameter"""
    name: str
    param_type: str
    required: bool = False
    description: Optional[str] = None
    default: Optional[Any] = None
    enum: Optional[List[Any]] = None
    minimum: Optional[int] = None
    maximum: Optional[int] = None
    pattern: Optional[str] = None
    example: Optional[Any] = None
    format: Optional[str] = None


class ValidationRule(BaseModel):
    """Validation rule for request field"""
    field: str
    rules: List[str]
    type: str
    required: bool
    constraints: Dict[str, Any]
    description: Optional[str] = None


class RequestBody(BaseModel):
    """Request body schema"""
    required: bool = False
    content_type: str = "application/json"
    schema: Optional[Dict[str, Any]] = None
    validation_rules: Optional[List[ValidationRule]] = None
    example: Optional[Dict[str, Any]] = None


class Response(BaseModel):
    """Response schema"""
    status_code: int
    description: str
    schema: Optional[Dict[str, Any]] = None
    example: Optional[Dict[str, Any]] = None
    headers: Optional[List[Parameter]] = None


class RateLimit(BaseModel):
    """Rate limiting configuration"""
    limit: int
    window: str
    description: Optional[str] = None


class SourceTrace(BaseModel):
    """Source code traceability"""
    route_file: str
    controller_file: Optional[str] = None
    method: Optional[str] = None
    line: Optional[int] = None
    form_request: Optional[str] = None
    resource: Optional[str] = None


class EndpointItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # Core endpoint info
    framework: str
    method: str
    path: str
    summary: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    
    # Source traceability
    source_file: str
    matched_line: str
    source: Optional[SourceTrace] = None
    function_name: Optional[str] = None
    router_prefix: Optional[str] = None
    
    # Parameters
    path_params: Optional[List[Parameter]] = None
    query_params: Optional[List[Parameter]] = None
    headers: Optional[List[Parameter]] = None
    
    # Request/Response
    request_body: Optional[RequestBody] = None
    responses: Optional[List[Response]] = None
    response_model: Optional[str] = None
    status_code: Optional[int] = None
    
    # Security & Middleware
    security: Optional[List[str]] = None
    middleware: Optional[List[str]] = None
    x_authentication: Optional[List[str]] = Field(default=None, alias="x-authentication")
    x_permissions: Optional[List[str]] = Field(default=None, alias="x-permissions")
    
    # Examples
    curl_example: Optional[str] = None
    request_example: Optional[Dict[str, Any]] = None
    sdk_examples: Optional[Dict[str, str]] = None
    
    # Metadata
    deprecated: bool = False
    replacement: Optional[str] = None
    rate_limit: Optional[RateLimit] = None
    pagination: Optional[Dict[str, Any]] = None
    
    # Confidence & Attribution
    confidence_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    low_confidence: bool = False
    summary_attribution: Optional[Attribution] = None
    description_attribution: Optional[Attribution] = None
    request_body_attribution: Optional[Attribution] = None
    response_body_attribution: Optional[Attribution] = None
    authentication_attribution: Optional[Attribution] = None
    
    # Legacy fields for backward compatibility
    ai_notes: Optional[Dict[str, Any]] = None
    ai_enhanced: Optional[bool] = None
    x_framework_confidence: Optional[float] = Field(default=None, alias="x-framework-confidence")
    x_source_route: Optional[str] = Field(default=None, alias="x-source-route")
    x_source_view: Optional[str] = Field(default=None, alias="x-source-view")
    x_source_serializer: Optional[str] = Field(default=None, alias="x-source-serializer")
    x_source_model: Optional[str] = Field(default=None, alias="x-source-model")
    x_source_router: Optional[str] = Field(default=None, alias="x-source-router")
    x_throttling: Optional[List[str]] = Field(default=None, alias="x-throttling")
    x_drf_action: Optional[str] = Field(default=None, alias="x-drf-action")
    x_pagination: Optional[Dict[str, Any]] = Field(default=None, alias="x-pagination")


class ExtractionErrorItem(BaseModel):
    file: str
    error: str


class EndpointExtractionResult(BaseModel):
    status: str
    repository_type: Optional[str] = None
    tree_truncated: bool = False
    total_tree_entries: int = 0
    backend_files: int
    processed_files: int
    failed_files: int
    spec_files_detected: int = 0
    spec_endpoints_extracted: int = 0
    spec_files: List[str] = []
    duplicates_removed: int = 0
    total_unique_endpoints: int
    documentation_summary: Optional[Dict[str, Any]] = None
    extraction_metrics: Optional[Dict[str, Any]] = None
    ai_enhancement_summary: Optional[Dict[str, Any]] = None
    openapi_document: Optional[Dict[str, Any]] = None
    markdown_document: Optional[str] = None
    html_document: Optional[str] = None
    errors: List[ExtractionErrorItem]
    endpoints: List[EndpointItem]
