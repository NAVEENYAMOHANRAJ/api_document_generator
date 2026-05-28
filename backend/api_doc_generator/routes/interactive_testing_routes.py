"""
Interactive API Testing Routes

Allows users to test API endpoints directly from documentation.
Handles request execution, response capture, and error handling.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import httpx
import json
import uuid
from datetime import datetime

router = APIRouter(tags=["Interactive Testing"])

# Store test results
test_results: Dict[str, Dict[str, Any]] = {}


class TestRequest(BaseModel):
    """Interactive test request"""
    endpoint_method: str
    endpoint_path: str
    base_url: str
    headers: Dict[str, str] = {}
    query_params: Dict[str, str] = {}
    request_body: Optional[Dict[str, Any]] = None
    auth_token: Optional[str] = None


class TestResponse(BaseModel):
    """Test response data"""
    test_id: str
    status: str
    status_code: Optional[int] = None
    response_body: Optional[Dict[str, Any]] = None
    response_headers: Optional[Dict[str, str]] = None
    execution_time: Optional[float] = None
    error: Optional[str] = None
    timestamp: str


@router.post("/test")
async def execute_test(request: TestRequest, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Execute an interactive API test
    
    Returns test ID for polling results
    """
    test_id = str(uuid.uuid4())
    
    # Initialize test result
    test_results[test_id] = {
        "test_id": test_id,
        "status": "pending",
        "timestamp": datetime.now().isoformat()
    }
    
    # Run test in background
    background_tasks.add_task(
        _execute_test_async,
        test_id,
        request
    )
    
    return {
        "test_id": test_id,
        "status": "pending",
        "message": "Test execution started"
    }


@router.get("/test/{test_id}")
async def get_test_result(test_id: str) -> Dict[str, Any]:
    """Get test result"""
    
    if test_id not in test_results:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return test_results[test_id]


async def _execute_test_async(test_id: str, request: TestRequest):
    """Execute test asynchronously"""
    
    try:
        # Build full URL
        url = f"{request.base_url}{request.endpoint_path}"
        
        # Add query parameters
        if request.query_params:
            query_string = "&".join([f"{k}={v}" for k, v in request.query_params.items()])
            url = f"{url}?{query_string}"
        
        # Prepare headers
        headers = request.headers.copy()
        if request.auth_token:
            headers["Authorization"] = f"Bearer {request.auth_token}"
        
        # Execute request
        async with httpx.AsyncClient(timeout=30.0) as client:
            import time
            start_time = time.time()
            
            if request.endpoint_method.upper() == "GET":
                response = await client.get(url, headers=headers)
            elif request.endpoint_method.upper() == "POST":
                response = await client.post(url, headers=headers, json=request.request_body)
            elif request.endpoint_method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=request.request_body)
            elif request.endpoint_method.upper() == "PATCH":
                response = await client.patch(url, headers=headers, json=request.request_body)
            elif request.endpoint_method.upper() == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {request.endpoint_method}")
            
            execution_time = time.time() - start_time
            
            # Parse response
            try:
                response_body = response.json()
            except:
                response_body = {"raw": response.text}
            
            # Store result
            test_results[test_id] = {
                "test_id": test_id,
                "status": "completed",
                "status_code": response.status_code,
                "response_body": response_body,
                "response_headers": dict(response.headers),
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
    
    except Exception as e:
        test_results[test_id] = {
            "test_id": test_id,
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@router.post("/test/example-payload")
async def generate_example_payload(endpoint: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate example payload for an endpoint
    
    Based on request body schema
    """
    
    request_body = endpoint.get("requestBody", {})
    schema = request_body.get("schema", {})
    
    example = _generate_example_from_schema(schema)
    
    return {
        "example": example,
        "schema": schema
    }


def _generate_example_from_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Generate example data from JSON schema"""
    
    example = {}
    
    for field_name, field_info in schema.items():
        if isinstance(field_info, dict):
            field_type = field_info.get("type", "string")
            
            if field_type == "string":
                if field_info.get("format") == "email":
                    example[field_name] = "user@example.com"
                elif field_info.get("format") == "date":
                    example[field_name] = "2024-01-15"
                elif field_info.get("format") == "date-time":
                    example[field_name] = "2024-01-15T10:30:00Z"
                else:
                    example[field_name] = field_info.get("example", "example_value")
            
            elif field_type == "integer":
                example[field_name] = field_info.get("example", 1)
            
            elif field_type == "number":
                example[field_name] = field_info.get("example", 1.0)
            
            elif field_type == "boolean":
                example[field_name] = True
            
            elif field_type == "array":
                example[field_name] = []
            
            elif field_type == "object":
                example[field_name] = {}
        else:
            example[field_name] = "example_value"
    
    return example


@router.get("/environments")
async def get_environments() -> Dict[str, Any]:
    """Get available environments for testing"""
    
    return {
        "environments": [
            {
                "name": "Local",
                "base_url": "http://localhost:8000",
                "description": "Local development environment"
            },
            {
                "name": "Staging",
                "base_url": "https://staging-api.example.com",
                "description": "Staging environment"
            },
            {
                "name": "Production",
                "base_url": "https://api.example.com",
                "description": "Production environment"
            }
        ]
    }
