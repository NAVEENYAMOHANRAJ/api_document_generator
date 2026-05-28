"""Dashboard API routes for comprehensive documentation display."""

from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict, Any

router = APIRouter()


@router.get("/api-docs/documentation")
async def get_documentation():
    """
    Get comprehensive API documentation for dashboard display.
    
    Returns all sections: overview, authentication, endpoints, errors, rate limits, etc.
    """
    return {
        "api": {
            "name": "Smart API Documentation Generator",
            "version": "1.0.0",
            "baseUrl": "http://localhost:8001/api",
            "description": "Technology-independent API documentation generator that extracts endpoints from source code",
        },
        "authentication": [
            {
                "type": "Bearer Token",
                "description": "Use Bearer token in Authorization header for authenticated requests",
                "example": "Authorization: Bearer YOUR_API_TOKEN",
            },
            {
                "type": "API Key",
                "description": "Include API key in X-API-Key header",
                "example": "X-API-Key: your_api_key_here",
            },
        ],
        "endpoints": [
            {
                "method": "POST",
                "path": "/api-docs/scan-repository",
                "summary": "Scan a GitHub repository",
                "description": "Scan a GitHub repository to detect backend files and framework candidates",
                "parameters": [
                    {
                        "name": "repo_url",
                        "type": "string",
                        "required": True,
                        "description": "GitHub repository URL (owner/repo format)",
                    },
                    {
                        "name": "github_token",
                        "type": "string",
                        "required": False,
                        "description": "GitHub personal access token for private repositories",
                    },
                ],
                "requestBody": {
                    "type": "object",
                    "example": {
                        "repo_url": "owner/repo",
                        "github_token": None,
                    },
                },
                "responses": [
                    {
                        "status": 200,
                        "description": "Repository scanned successfully",
                    },
                    {
                        "status": 400,
                        "description": "Invalid repository URL",
                    },
                    {
                        "status": 404,
                        "description": "Repository not found",
                    },
                ],
            },
            {
                "method": "POST",
                "path": "/api-docs/extract-endpoints",
                "summary": "Extract endpoints from repository",
                "description": "Extract API endpoints from a GitHub repository and generate documentation",
                "parameters": [
                    {
                        "name": "repo_url",
                        "type": "string",
                        "required": True,
                        "description": "GitHub repository URL",
                    },
                    {
                        "name": "github_token",
                        "type": "string",
                        "required": False,
                        "description": "GitHub personal access token",
                    },
                ],
                "requestBody": {
                    "type": "object",
                    "example": {
                        "repo_url": "owner/repo",
                        "github_token": None,
                    },
                },
                "responses": [
                    {
                        "status": 200,
                        "description": "Endpoints extracted successfully",
                    },
                    {
                        "status": 400,
                        "description": "Invalid request parameters",
                    },
                ],
            },
            {
                "method": "POST",
                "path": "/api-docs/extract-local-folder",
                "summary": "Extract endpoints from local folder",
                "description": "Extract API endpoints from a local folder path",
                "parameters": [
                    {
                        "name": "folder_path",
                        "type": "string",
                        "required": True,
                        "description": "Local folder path to scan",
                    },
                ],
                "requestBody": {
                    "type": "object",
                    "example": {
                        "folder_path": "/path/to/project",
                    },
                },
                "responses": [
                    {
                        "status": 200,
                        "description": "Endpoints extracted successfully",
                    },
                    {
                        "status": 400,
                        "description": "Invalid folder path",
                    },
                ],
            },
            {
                "method": "POST",
                "path": "/api-docs/extract-upload",
                "summary": "Extract endpoints from ZIP upload",
                "description": "Extract API endpoints from an uploaded ZIP file",
                "parameters": [
                    {
                        "name": "filename",
                        "type": "string",
                        "required": True,
                        "description": "Name of the uploaded ZIP file",
                    },
                ],
                "requestBody": {
                    "type": "binary",
                    "example": "ZIP file content",
                },
                "responses": [
                    {
                        "status": 200,
                        "description": "ZIP file processed successfully",
                    },
                    {
                        "status": 400,
                        "description": "Invalid ZIP file",
                    },
                ],
            },
        ],
        "rateLimit": {
            "requestsPerMinute": 60,
            "requestsPerHour": 1000,
            "headers": [
                "X-RateLimit-Limit: 60",
                "X-RateLimit-Remaining: 59",
                "X-RateLimit-Reset: 1234567890",
            ],
        },
        "schemas": {
            "Endpoint": {
                "type": "object",
                "properties": {
                    "method": {"type": "string", "example": "GET"},
                    "path": {"type": "string", "example": "/users/{id}"},
                    "summary": {"type": "string"},
                    "description": {"type": "string"},
                    "parameters": {"type": "array"},
                    "requestBody": {"type": "object"},
                    "responses": {"type": "array"},
                },
            },
            "ScanResult": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "backend_files": {"type": "integer"},
                    "framework_candidates": {"type": "array"},
                    "total_unique_endpoints": {"type": "integer"},
                },
            },
        },
        "pagination": {
            "style": "Offset-based pagination",
            "parameters": ["page", "limit"],
            "example": "GET /api/endpoints?page=1&limit=20",
        },
        "webhooks": [
            {
                "event": "extraction.completed",
                "description": "Triggered when endpoint extraction is completed",
                "payload": {
                    "event": "extraction.completed",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "endpoints_count": 42,
                    "repository": "owner/repo",
                },
            },
            {
                "event": "extraction.failed",
                "description": "Triggered when endpoint extraction fails",
                "payload": {
                    "event": "extraction.failed",
                    "timestamp": "2024-01-01T00:00:00Z",
                    "error": "Repository not found",
                    "repository": "owner/repo",
                },
            },
        ],
        "errors": [
            {
                "code": 400,
                "message": "Bad Request",
                "description": "The request was invalid or malformed. Check your parameters.",
            },
            {
                "code": 401,
                "message": "Unauthorized",
                "description": "Authentication is required. Provide a valid API token.",
            },
            {
                "code": 403,
                "message": "Forbidden",
                "description": "You do not have permission to access this resource.",
            },
            {
                "code": 404,
                "message": "Not Found",
                "description": "The requested resource was not found.",
            },
            {
                "code": 429,
                "message": "Too Many Requests",
                "description": "Rate limit exceeded. Please wait before making another request.",
            },
            {
                "code": 500,
                "message": "Internal Server Error",
                "description": "An unexpected error occurred on the server.",
            },
            {
                "code": 503,
                "message": "Service Unavailable",
                "description": "The service is temporarily unavailable. Please try again later.",
            },
        ],
        "changelog": [
            {
                "version": "1.0.0",
                "date": "2024-01-15",
                "changes": [
                    "Initial release",
                    "Support for Laravel, FastAPI, Express, Flask, Django REST Framework",
                    "OpenAPI/Swagger spec generation",
                    "GitHub repository scanning",
                    "Local folder extraction",
                    "ZIP file upload support",
                    "AI-enhanced documentation with LLM",
                ],
            },
            {
                "version": "0.9.0",
                "date": "2024-01-10",
                "changes": [
                    "Beta release",
                    "Core endpoint extraction",
                    "Basic documentation generation",
                ],
            },
        ],
    }


@router.get("/api-docs/health")
async def health_check():
    """Health check endpoint for dashboard."""
    return {"status": "ok", "service": "api-documentation-dashboard"}
