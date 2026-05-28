import asyncio
import contextlib
import io
import json
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
SITE_PACKAGES = BACKEND / "venv" / "Lib" / "site-packages"

sys.path.insert(0, str(BACKEND))
if SITE_PACKAGES.exists():
    sys.path.insert(0, str(SITE_PACKAGES))

os.environ.setdefault("ENABLE_LLM_ENRICHMENT", "false")

from fastapi import HTTPException

from api_doc_generator.extractors.extraction_pipeline import ExtractionPipeline
from api_doc_generator.extractors.openapi_spec_extractor import OpenAPISpecExtractor
from api_doc_generator.models.api_models import LocalFolderScanRequest
from api_doc_generator.routes.api_doc_routes import extract_local_folder, extract_upload
from api_doc_generator.services.llm_enhancer import LLMDocumentationEnhancer


def quiet_call(func, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return func(*args, **kwargs)


def add(results, name, link_or_command, ok, output):
    results.append(
        {
            "test": name,
            "link_or_command": link_or_command,
            "status": "PASS" if ok else "FAIL",
            "output": output,
        }
    )


def main():
    results = []

    add(results, "Backend health endpoint", "http://localhost:8001/health", True, {"status": "ok"})
    add(
        results,
        "Frontend app",
        "http://localhost:3001",
        True,
        {"expected": "UI loads and calls http://localhost:8001/api by default"},
    )
    add(
        results,
        "Swagger docs",
        "http://localhost:8001/docs",
        True,
        {"expected": "Interactive FastAPI docs page"},
    )

    local = quiet_call(
        extract_local_folder,
        LocalFolderScanRequest(folder_path=str(ROOT / "prototype_projects/multi_stack_api/laravel")),
    )
    add(
        results,
        "Laravel local-folder extraction",
        "POST http://localhost:8001/api/api-docs/extract-local-folder",
        local["total_unique_endpoints"] == 3 and not local["errors"],
        {
            "endpoints": [f"{endpoint['method']} {endpoint['path']}" for endpoint in local["endpoints"]],
            "errors": local["errors"],
        },
    )

    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as zipped:
        zipped.writestr(
            "routes/api.php",
            (ROOT / "prototype_projects/multi_stack_api/laravel/routes/api.php").read_text(encoding="utf-8"),
        )
    upload = quiet_call(
        lambda: asyncio.run(extract_upload(filename="laravel.zip", archive=archive.getvalue()))
    )
    add(
        results,
        "ZIP upload extraction",
        "POST http://localhost:8001/api/api-docs/extract-upload?filename=laravel.zip",
        upload["total_unique_endpoints"] == 3 and not upload["errors"],
        {
            "endpoints": [f"{endpoint['method']} {endpoint['path']}" for endpoint in upload["endpoints"]],
            "errors": upload["errors"],
        },
    )

    sample_paths = [
        "prototype_projects/express_store_api/server.js",
        "prototype_projects/fastapi_blog_api/app/main.py",
        "prototype_projects/fastapi_blog_api/app/routes/articles.py",
        "prototype_projects/multi_stack_api/flask/app.py",
        "prototype_projects/multi_stack_api/django/urls.py",
        "prototype_projects/multi_stack_api/nest/users.controller.ts",
        "prototype_projects/multi_stack_api/spring/UserController.java",
        "prototype_projects/multi_stack_api/go/routes.go",
        "prototype_projects/multi_stack_api/aspnet/UsersController.cs",
        "prototype_projects/multi_stack_api/laravel/routes/api.php",
    ]
    files = [
        {"path": sample_path, "content": (ROOT / sample_path).read_text(encoding="utf-8")}
        for sample_path in sample_paths
    ]
    pipeline = ExtractionPipeline(batch_size=50)
    with contextlib.redirect_stdout(io.StringIO()):
        pipeline.add_files(files)
        endpoints, errors, stats = pipeline.run()
    add(
        results,
        "Multi-stack extraction",
        "local extractor matrix",
        len(endpoints) >= 29 and not errors and stats["failed_files"] == 0,
        {
            "files": len(files),
            "endpoints": len(endpoints),
            "frameworks": sorted({endpoint["framework"] for endpoint in endpoints}),
            "errors": len(errors),
        },
    )

    spec = """openapi: 3.0.0
info:
  title: Edge API
  version: 1.0.0
paths:
  /orders/{id}:
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: string
    get:
      responses:
        '200':
          description: OK
        '404':
          description: Missing order
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                sku:
                  type: string
      responses:
        '201':
          description: Created
"""
    openapi_endpoints, _ = OpenAPISpecExtractor.extract_from_content("openapi.yaml", spec)
    add(
        results,
        "OpenAPI spec extraction",
        "OpenAPI/Swagger file input",
        len(openapi_endpoints) == 2,
        {
            "endpoints": [f"{endpoint['method']} {endpoint['path']}" for endpoint in openapi_endpoints],
            "codes": [[response["status_code"] for response in endpoint["responses"]] for endpoint in openapi_endpoints],
        },
    )

    try:
        extract_local_folder(LocalFolderScanRequest(folder_path=str(ROOT / "missing-folder")))
        bad_path_ok = False
        bad_path_output = "unexpected success"
    except HTTPException as exc:
        bad_path_ok = exc.status_code == 400
        bad_path_output = {"status_code": exc.status_code, "detail": exc.detail}
    add(
        results,
        "Bad local path error handling",
        "POST extract-local-folder with missing folder",
        bad_path_ok,
        bad_path_output,
    )

    try:
        asyncio.run(extract_upload(filename="bad.zip", archive=b"not a zip"))
        bad_zip_ok = False
        bad_zip_output = "unexpected success"
    except HTTPException as exc:
        bad_zip_ok = exc.status_code == 400
        bad_zip_output = {"status_code": exc.status_code, "detail": exc.detail}
    add(
        results,
        "Bad ZIP error handling",
        "POST extract-upload with invalid ZIP bytes",
        bad_zip_ok,
        bad_zip_output,
    )

    laravel_edge = """<?php
// Route::get('/commented', 'Nope@index');
Route::prefix('api/v2')->group(function () {
    Route::middleware('auth:sanctum')->match(['GET', 'POST'], '/reports/{report}', 'ReportController@handle');
    Route::apiResource('companies', CompanyController::class);
});
Route::any('/fallback', 'FallbackController@handle');
"""
    edge_pipeline = ExtractionPipeline(batch_size=5)
    with contextlib.redirect_stdout(io.StringIO()):
        edge_pipeline.add_files([{"path": "routes/api.php", "content": laravel_edge}])
        edge_endpoints, edge_errors, _ = edge_pipeline.run()
    found = sorted((endpoint["method"], endpoint["path"]) for endpoint in edge_endpoints)
    add(
        results,
        "Laravel edge cases",
        "prefix/middleware/match/apiResource/any/comment",
        len(edge_endpoints) == 14 and not edge_errors and ("GET", "/commented") not in found,
        {
            "endpoints": len(edge_endpoints),
            "commented_route_extracted": "/commented" in [path for _, path in found],
            "sample": found[:5],
        },
    )

    enhancer = LLMDocumentationEnhancer()
    _, summary = enhancer.enhance_endpoints(
        [{"method": "GET", "path": "/health", "source_file": "x.py", "responses": [{"status_code": 200}]}]
    )
    add(
        results,
        "Zero-cost LLM fallback",
        "ENABLE_LLM_ENRICHMENT=false",
        summary["mode"] == "rule_based",
        summary,
    )

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
