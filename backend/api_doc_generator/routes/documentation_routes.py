"""
Documentation Generation Routes

Provides endpoints to generate comprehensive API documentation in multiple formats:
- Markdown
- HTML
- JSON
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from api_doc_generator.generators.documentation_generator import DocumentationGenerator

router = APIRouter(tags=["Documentation"])

# Store for generated documentation
generated_docs: Dict[str, Dict[str, Any]] = {}


@router.post("/generate/{job_id}")
async def generate_documentation(job_id: str, api_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comprehensive API documentation from extracted data
    
    Returns documentation in multiple formats:
    - markdown: Markdown format
    - html: HTML format
    - json: Structured JSON format
    """
    
    try:
        endpoints = api_data.get("endpoints", []) or []
        title = (api_data.get("api", {}) or {}).get("name") or "Generated API Documentation"
        doc_data = {
            "job_id": job_id,
            "markdown": DocumentationGenerator.generate_markdown(endpoints, title=title),
            "html": DocumentationGenerator.generate_html(endpoints, title=title),
            "json": api_data,
            "generated_at": str(__import__('datetime').datetime.now())
        }
        
        generated_docs[job_id] = doc_data
        
        return {
            "job_id": job_id,
            "status": "generated",
            "formats": ["markdown", "html", "json"],
            "message": "Documentation generated successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/markdown/{job_id}")
async def get_markdown_documentation(job_id: str) -> Dict[str, str]:
    """Get documentation in Markdown format"""
    
    if job_id not in generated_docs:
        raise HTTPException(status_code=404, detail="Documentation not found")
    
    return {
        "format": "markdown",
        "content": generated_docs[job_id]["markdown"]
    }


@router.get("/html/{job_id}")
async def get_html_documentation(job_id: str) -> Dict[str, str]:
    """Get documentation in HTML format"""
    
    if job_id not in generated_docs:
        raise HTTPException(status_code=404, detail="Documentation not found")
    
    return {
        "format": "html",
        "content": generated_docs[job_id]["html"]
    }


@router.get("/json/{job_id}")
async def get_json_documentation(job_id: str) -> Dict[str, Any]:
    """Get documentation in JSON format"""
    
    if job_id not in generated_docs:
        raise HTTPException(status_code=404, detail="Documentation not found")
    
    return {
        "format": "json",
        "content": generated_docs[job_id]["json"]
    }


@router.get("/all/{job_id}")
async def get_all_documentation(job_id: str) -> Dict[str, Any]:
    """Get documentation in all formats"""
    
    if job_id not in generated_docs:
        raise HTTPException(status_code=404, detail="Documentation not found")
    
    return generated_docs[job_id]
