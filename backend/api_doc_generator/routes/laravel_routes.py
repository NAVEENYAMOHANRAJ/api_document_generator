"""
Laravel API Extraction Routes
Extracts Laravel endpoints and displays them with all features
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import subprocess
import tempfile
import shutil
from pathlib import Path

from api_doc_generator.extractors.laravel_extractor import LaravelExtractor

router = APIRouter()


class LaravelExtractionRequest(BaseModel):
    """Request to extract Laravel endpoints"""
    repo_url: str
    github_token: Optional[str] = None


class LaravelEndpoint(BaseModel):
    """Laravel endpoint with all details"""
    method: str
    path: str
    handler: Optional[str]
    middleware: List[str]
    source_file: str
    line_number: int
    confidence: float
    summary: str
    description: str


class LaravelExtractionResponse(BaseModel):
    """Response with extracted Laravel endpoints"""
    status: str
    framework: str
    total_endpoints: int
    endpoints: List[Dict[str, Any]]
    statistics: Dict[str, Any]
    metadata: Dict[str, Any]


@router.post("/api/extract-laravel", response_model=LaravelExtractionResponse)
async def extract_laravel_endpoints(request: LaravelExtractionRequest):
    """
    Extract Laravel endpoints from GitHub repository
    
    Extracts:
    - HTTP method and path
    - Handler (Controller@method)
    - Middleware
    - Source file and line number
    - Confidence score
    """
    temp_dir = None
    
    try:
        # Validate input
        if not request.repo_url or not request.repo_url.strip():
            raise HTTPException(status_code=400, detail="Repository URL is required")
        
        repo_url = request.repo_url.strip()
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        
        # Clone the repository
        try:
            clone_cmd = ["git", "clone", "--depth", "1", repo_url, temp_dir]
            
            result = subprocess.run(
                clone_cmd,
                capture_output=True,
                timeout=120,
                text=True
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to clone repository: {error_msg[:200]}"
                )
        
        except subprocess.TimeoutExpired:
            raise HTTPException(
                status_code=504,
                detail="Repository clone operation timed out (>120s). Repository may be too large."
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error cloning repository: {str(e)[:200]}"
            )
        
        # Verify it's a Laravel project
        routes_dir = Path(temp_dir) / "routes"
        if not routes_dir.exists():
            raise HTTPException(
                status_code=422,
                detail="Not a Laravel project: 'routes' directory not found"
            )
        
        # Find route files
        api_routes_file = routes_dir / "api.php"
        web_routes_file = routes_dir / "web.php"
        
        if not api_routes_file.exists() and not web_routes_file.exists():
            raise HTTPException(
                status_code=422,
                detail="No route files found (api.php or web.php)"
            )
        
        endpoints = []
        files_processed = 0
        extraction_errors = []
        
        # Process api.php
        if api_routes_file.exists():
            try:
                with open(api_routes_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if not content.strip():
                    extraction_errors.append("api.php is empty")
                else:
                    extractor = LaravelExtractor(str(api_routes_file), temp_dir)
                    extracted = extractor.extract(str(api_routes_file), content, temp_dir)
                    
                    if extracted:
                        endpoints.extend(extracted)
                        files_processed += 1
                    else:
                        extraction_errors.append("No routes found in api.php")
            
            except Exception as e:
                extraction_errors.append(f"Error processing api.php: {str(e)[:100]}")
        
        # Process web.php
        if web_routes_file.exists():
            try:
                with open(web_routes_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if not content.strip():
                    extraction_errors.append("web.php is empty")
                else:
                    extractor = LaravelExtractor(str(web_routes_file), temp_dir)
                    extracted = extractor.extract(str(web_routes_file), content, temp_dir)
                    
                    if extracted:
                        endpoints.extend(extracted)
                        files_processed += 1
                    else:
                        extraction_errors.append("No routes found in web.php")
            
            except Exception as e:
                extraction_errors.append(f"Error processing web.php: {str(e)[:100]}")
        
        # If no endpoints found, return error
        if not endpoints:
            error_detail = "No endpoints extracted. "
            if extraction_errors:
                error_detail += " ".join(extraction_errors[:2])
            else:
                error_detail += "Route files may not contain valid Laravel routes."
            
            raise HTTPException(status_code=422, detail=error_detail)
        
        # Format endpoints for response
        formatted_endpoints = []
        for ep in endpoints:
            try:
                handler_str = None
                if ep.get("handler"):
                    handler_class = ep.get("handler", {}).get("class", "")
                    handler_method = ep.get("handler", {}).get("method", "")
                    if handler_class and handler_method:
                        handler_str = f"{handler_class}@{handler_method}"
                
                formatted_ep = {
                    "method": ep.get("method", "UNKNOWN").upper(),
                    "path": ep.get("path", "/"),
                    "handler": handler_str,
                    "middleware": ep.get("middleware", []) or [],
                    "source_file": ep.get("source", {}).get("file", "unknown"),
                    "line_number": int(ep.get("source", {}).get("line", 0)),
                    "confidence": float(ep.get("confidence", 0.0)),
                    "summary": f"{ep.get('method', 'UNKNOWN').upper()} {ep.get('path', '/')}",
                    "description": handler_str or "Closure route",
                }
                formatted_endpoints.append(formatted_ep)
            
            except Exception as e:
                # Skip malformed endpoints
                continue
        
        if not formatted_endpoints:
            raise HTTPException(
                status_code=422,
                detail="Failed to format extracted endpoints"
            )
        
        # Calculate statistics
        methods = {}
        for ep in formatted_endpoints:
            method = ep["method"]
            methods[method] = methods.get(method, 0) + 1
        
        avg_confidence = (
            sum(ep["confidence"] for ep in formatted_endpoints) / len(formatted_endpoints)
            if formatted_endpoints
            else 0.0
        )
        
        return LaravelExtractionResponse(
            status="success",
            framework="laravel",
            total_endpoints=len(formatted_endpoints),
            endpoints=formatted_endpoints,
            statistics={
                "total_endpoints": len(formatted_endpoints),
                "methods": methods,
                "files_scanned": files_processed,
                "average_confidence": round(avg_confidence, 2),
            },
            metadata={
                "repository": repo_url,
                "extraction_method": "regex_based",
                "routes_files_found": files_processed,
                "errors": extraction_errors if extraction_errors else None,
            }
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during extraction: {str(e)[:200]}"
        )
    
    finally:
        # Cleanup temp directory
        if temp_dir and Path(temp_dir).exists():
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass


@router.post("/api/extract-laravel-local")
async def extract_laravel_local(folder_path: str):
    """
    Extract Laravel endpoints from local folder
    """
    try:
        # Validate input
        if not folder_path or not folder_path.strip():
            raise HTTPException(status_code=400, detail="Folder path is required")
        
        folder = Path(folder_path.strip())
        
        # Validate folder exists
        if not folder.exists():
            raise HTTPException(status_code=404, detail=f"Folder not found: {folder_path}")
        
        if not folder.is_dir():
            raise HTTPException(status_code=400, detail=f"Path is not a directory: {folder_path}")
        
        # Check for routes directory
        routes_dir = folder / "routes"
        if not routes_dir.exists():
            raise HTTPException(
                status_code=422,
                detail="Not a Laravel project: 'routes' directory not found"
            )
        
        # Find PHP files
        route_files = list(routes_dir.glob("*.php"))
        if not route_files:
            raise HTTPException(
                status_code=422,
                detail="No PHP route files found in routes directory"
            )
        
        endpoints = []
        extraction_errors = []
        
        # Process all PHP files in routes directory
        for route_file in route_files:
            try:
                with open(route_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if not content.strip():
                    extraction_errors.append(f"{route_file.name} is empty")
                    continue
                
                extractor = LaravelExtractor(str(route_file), str(folder))
                extracted = extractor.extract(str(route_file), content, str(folder))
                
                if extracted:
                    endpoints.extend(extracted)
                else:
                    extraction_errors.append(f"No routes found in {route_file.name}")
            
            except Exception as e:
                extraction_errors.append(f"Error processing {route_file.name}: {str(e)[:100]}")
        
        # If no endpoints found, return error
        if not endpoints:
            error_detail = "No endpoints extracted. "
            if extraction_errors:
                error_detail += " ".join(extraction_errors[:2])
            else:
                error_detail += "Route files may not contain valid Laravel routes."
            
            raise HTTPException(status_code=422, detail=error_detail)
        
        # Format response
        formatted_endpoints = []
        for ep in endpoints:
            try:
                handler_str = None
                if ep.get("handler"):
                    handler_class = ep.get("handler", {}).get("class", "")
                    handler_method = ep.get("handler", {}).get("method", "")
                    if handler_class and handler_method:
                        handler_str = f"{handler_class}@{handler_method}"
                
                formatted_ep = {
                    "method": ep.get("method", "UNKNOWN").upper(),
                    "path": ep.get("path", "/"),
                    "handler": handler_str,
                    "middleware": ep.get("middleware", []) or [],
                    "source_file": ep.get("source", {}).get("file", "unknown"),
                    "line_number": int(ep.get("source", {}).get("line", 0)),
                    "confidence": float(ep.get("confidence", 0.0)),
                    "summary": f"{ep.get('method', 'UNKNOWN').upper()} {ep.get('path', '/')}",
                    "description": handler_str or "Closure route",
                }
                formatted_endpoints.append(formatted_ep)
            
            except Exception as e:
                # Skip malformed endpoints
                continue
        
        if not formatted_endpoints:
            raise HTTPException(
                status_code=422,
                detail="Failed to format extracted endpoints"
            )
        
        # Calculate statistics
        methods = {}
        for ep in formatted_endpoints:
            method = ep["method"]
            methods[method] = methods.get(method, 0) + 1
        
        avg_confidence = (
            sum(ep["confidence"] for ep in formatted_endpoints) / len(formatted_endpoints)
            if formatted_endpoints
            else 0.0
        )
        
        return {
            "status": "success",
            "framework": "laravel",
            "total_endpoints": len(formatted_endpoints),
            "endpoints": formatted_endpoints,
            "statistics": {
                "total_endpoints": len(formatted_endpoints),
                "methods": methods,
                "files_scanned": len(route_files),
                "average_confidence": round(avg_confidence, 2),
            },
            "metadata": {
                "folder": str(folder),
                "extraction_method": "regex_based",
                "routes_files_found": len(route_files),
                "errors": extraction_errors if extraction_errors else None,
            }
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during extraction: {str(e)[:200]}"
        )
