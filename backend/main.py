import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the backend directory to the path so api_doc_generator can be imported
sys.path.insert(0, str(Path(__file__).parent))
load_dotenv(Path(__file__).parent / ".env")

from api_doc_generator.routes.api_doc_routes import router as api_doc_router

app = FastAPI(
    title="API Documentation Generator",
    description="Extract API endpoints from GitHub repositories",
    version="0.1.0",
)

# CORS configuration for frontend integration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
ALLOWED_ORIGINS = {
    FRONTEND_URL,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
}
app.add_middleware(
    CORSMiddleware,
    allow_origins=sorted(ALLOWED_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_doc_router, prefix="/api", tags=["API Documentation"])

try:
    from api_doc_generator.routes.enhanced_api_routes import router as enhanced_router
    from api_doc_generator.models.database_models import init_db

    init_db()
    app.include_router(enhanced_router, tags=["Enhanced API"])
except ImportError as exc:
    print(f"[Startup] Optional database routes disabled: {exc}", flush=True)

try:
    from api_doc_generator.routes.production_api_routes import router as production_router
    app.include_router(production_router, tags=["Production API"])
except ImportError as exc:
    print(f"[Startup] Production API routes disabled: {exc}", flush=True)

try:
    from api_doc_generator.routes.production_routes import router as prod_routes
    app.include_router(prod_routes, tags=["Production"])
except ImportError as exc:
    print(f"[Startup] Production routes disabled: {exc}", flush=True)

try:
    from api_doc_generator.routes.complete_documentation_routes import router as complete_doc_router
    app.include_router(complete_doc_router, prefix="/api/v1", tags=["Complete Documentation"])
except ImportError as exc:
    print(f"[Startup] Complete documentation routes disabled: {exc}", flush=True)

try:
    from api_doc_generator.routes.documentation_routes import router as documentation_router
    app.include_router(documentation_router, prefix="/api/docs", tags=["Documentation Generation"])
except ImportError as exc:
    print(f"[Startup] Documentation generation routes disabled: {exc}", flush=True)

try:
    from api_doc_generator.routes.interactive_testing_routes import router as testing_router
    app.include_router(testing_router, prefix="/api/testing", tags=["Interactive Testing"])
except ImportError as exc:
    print(f"[Startup] Interactive testing routes disabled: {exc}", flush=True)

try:
    from api_doc_generator.routes.dashboard_routes import router as dashboard_router
    app.include_router(dashboard_router, tags=["Dashboard"])
except ImportError as exc:
    print(f"[Startup] Dashboard routes disabled: {exc}", flush=True)

try:
    from api_doc_generator.routes.unified_extraction_routes import router as unified_router
    app.include_router(unified_router, tags=["Unified Extraction"])
except ImportError as exc:
    print(f"[Startup] Unified extraction routes disabled: {exc}", flush=True)

try:
    from api_doc_generator.routes.feature_extraction_routes import router as feature_router
    app.include_router(feature_router, tags=["Feature Extraction"])
except ImportError as exc:
    print(f"[Startup] Feature extraction routes disabled: {exc}", flush=True)

try:
    from api_doc_generator.routes.laravel_routes import router as laravel_router
    app.include_router(laravel_router, tags=["Laravel Extraction"])
except ImportError as exc:
    print(f"[Startup] Laravel extraction routes disabled: {exc}", flush=True)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8001")),
    )
