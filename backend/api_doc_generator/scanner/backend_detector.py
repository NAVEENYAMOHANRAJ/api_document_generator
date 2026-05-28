from pathlib import PurePosixPath
from typing import Any, Dict, List, Optional, Set

from api_doc_generator.scanner.framework_adapter_registry import FrameworkAdapterRegistry

CANDIDATE_EXTENSIONS = FrameworkAdapterRegistry.candidate_extensions()

IGNORE_DIRS = {
    "node_modules",
    "venv",
    ".git",
    "dist",
    "build",
    "__pycache__",
    "tests",
    "test",
    "spec",
    "examples",
    "example",
    "demo",
    "samples",
    "sample",
    "docs",
    "mock",
    "fixtures",
    "coverage",
    ".github",
    ".gitlab",
    ".vscode",
    ".idea",
    "vendor",
    "storage",
    "bootstrap",
    "obj",
    "bin",
}

IGNORE_FILE_TOKENS = {
    "test",
    "tests",
    "spec",
    "example",
    "examples",
    "demo",
    "sample",
    "samples",
    "docs",
    "mock",
    "fixture",
    "fixtures",
    "coverage",
    "readme",
    "license",
    "changelog",
    "contributing",
    "makefile",
    "dockerfile",
    "package-lock",
    "yarn-lock",
}


class BackendFileDetector:
    """Detect likely backend and production API files in a repository tree using weighted scoring."""

    def _normalize_path(self, path: str) -> str:
        return str(PurePosixPath(path))

    def _has_ignored_segment(self, path: str) -> bool:
        parts = {part.lower() for part in PurePosixPath(path).parts}
        return bool(parts & IGNORE_DIRS)

    def _has_ignored_filename(self, path: str) -> bool:
        name = PurePosixPath(path).name.lower()
        return any(token in name for token in IGNORE_FILE_TOKENS)

    def _has_valid_extension(self, path: str) -> bool:
        return PurePosixPath(path).suffix.lower() in CANDIDATE_EXTENSIONS

    def score_backend_probability(self, path: str, content: str) -> int:
        """Calculate a probability score for a file to determine if it belongs to a backend service."""
        score = 0
        path_lower = path.lower()
        content_lower = content.lower()

        # Route definitions (+40)
        route_patterns = [
            "route::", "app.get", "app.post", "app.put", "app.delete", "app.use",
            "@router.get", "@router.post", "@router.put", "@router.delete", "@app.route",
            "@restcontroller", "@requestmapping", "defaultrouter()", "router.register",
            "api_router", "apirouter", "router.get", "router.post", "router.use"
        ]
        if any(pat in content_lower for pat in route_patterns):
            score += 40

        # Framework imports (+30)
        import_patterns = [
            "import fastapi", "from fastapi", "require(\"express\")", "require('express')",
            "import express", "from rest_framework", "import org.springframework",
            "import \"github.com/gin-gonic/gin\"", "import \"github.com/gofiber/fiber",
            "from flask import", "import flask", "@nestjs/common"
        ]
        if any(pat in content_lower for pat in import_patterns):
            score += 30

        # HTTP method usage (+30)
        http_method_patterns = [
            ".get(", ".post(", ".put(", ".delete(", ".patch(",
            "@getmapping", "@postmapping", "@putmapping", "@deletemapping", "@patchmapping"
        ]
        if any(pat in content_lower for pat in http_method_patterns):
            score += 30

        # Controllers (+20)
        if "controller" in path_lower or "controller" in content_lower or "@controller" in content_lower:
            score += 20

        # Serializers/models/schemas (+15)
        schema_patterns = [
            "serializer", "model", "class meta:", "basemodel", "dto", "request", "response"
        ]
        if any(pat in path_lower or pat in content_lower for pat in schema_patterns):
            score += 15

        # Middleware/Auth (+10)
        middleware_patterns = [
            "middleware", "auth:", "permission_classes", "isauthenticated", "guard", "jwt"
        ]
        if any(pat in path_lower or pat in content_lower for pat in middleware_patterns):
            score += 10

        # Swagger/OpenAPI indicators (+20)
        swagger_patterns = [
            "openapi:", "swagger:", "get_schema_view", "@oas\\", "swagger_auto_schema"
        ]
        if any(pat in content_lower for pat in swagger_patterns):
            score += 20

        # Tests/docs/mock/generated (-50)
        negative_patterns = [
            "test", "spec", "mock", "demo", "example", "docs", "dist", "build", "__pycache__",
            "node_modules", "vendor", "bin/", "obj/", "compiled"
        ]
        if any(pat in path_lower for pat in negative_patterns):
            score -= 50

        return score

    def find_backend_files(self, tree_entries: List[Dict[str, Optional[int]]], content_by_path: Optional[Dict[str, str]] = None) -> List[Dict[str, Optional[int]]]:
        """Filter repository blob entries down to probable backend API files."""
        results = []
        content_by_path = content_by_path or {}

        for entry in tree_entries:
            path = entry.get("path")
            if not path:
                continue

            normalized_path = self._normalize_path(path)
            if self._has_ignored_segment(normalized_path):
                continue
            if self._has_ignored_filename(normalized_path):
                continue
            if not self._has_valid_extension(normalized_path):
                continue

            # Skip binary files, minified bundles, compiled files, etc.
            if any(term in normalized_path.lower() for term in [".min.js", ".min.css", ".pb.go", ".designer.cs"]):
                continue

            content = content_by_path.get(normalized_path, "")
            if content:
                probability = self.score_backend_probability(normalized_path, content)
                if probability > 0:
                    results.append({
                        "path": normalized_path,
                        "size": entry.get("size", 0),
                    })
                    continue

            # Fallback path-based check
            path_lower = normalized_path.lower()
            monorepo_indicators = {"apps", "packages", "services", "modules", "backend", "server", "src", "app"}
            if (any(part in monorepo_indicators for part in PurePosixPath(normalized_path).parts) or
                any(tok in path_lower for tok in {"routes", "controller", "api", "url", "views", "views.py"})):
                results.append({
                    "path": normalized_path,
                    "size": entry.get("size", 0),
                })

        return sorted(results, key=lambda item: item["path"])


class FrameworkCandidateDetector:
    """Infer likely backend framework candidates and their confidence from file paths/contents."""

    @staticmethod
    def detect(framework_files: List[Dict[str, Optional[int]]], content_by_path: Optional[Dict[str, str]] = None) -> List[str]:
        res = FrameworkCandidateDetector.detect_with_confidence(framework_files, content_by_path)
        return sorted([item["framework"] for item in res])

    @staticmethod
    def detect_with_confidence(framework_files: List[Dict[str, Optional[int]]], content_by_path: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        candidates = {}
        content_by_path = content_by_path or {}

        for entry in framework_files:
            path = entry.get("path", "")
            if not path:
                continue

            content = content_by_path.get(path, "")
            detected_names = []
            if content:
                detected_names = FrameworkAdapterRegistry.detect_from_content(path, content)
            if not detected_names:
                detected_names = FrameworkAdapterRegistry.detect_from_path(path)

            for name in detected_names:
                if name not in candidates:
                    candidates[name] = {"framework": name, "score": 0, "count": 0}
                candidates[name]["count"] += 1
                
                # Check for explicit high-recall framework features in content
                if content:
                    content_lower = content.lower()
                    if name == "Laravel" and "route::" in content_lower:
                        candidates[name]["score"] += 10
                    elif name == "Express" and "express.router" in content_lower:
                        candidates[name]["score"] += 10
                    elif name == "Spring Boot" and "@restcontroller" in content_lower:
                        candidates[name]["score"] += 10
                    elif name == "FastAPI" and "apirouter" in content_lower:
                        candidates[name]["score"] += 10
                    elif name == "Django REST Framework" and ("viewset" in content_lower or "defaultrouter" in content_lower):
                        candidates[name]["score"] += 10
                    elif name == "NestJS" and "@controller" in content_lower:
                        candidates[name]["score"] += 10
                    else:
                        candidates[name]["score"] += 2

        # Laravel fallback heuristic from path structures
        paths = set(content_by_path.keys())
        laravel_indicators = 0
        if any(p.endswith("artisan") for p in paths): laravel_indicators += 1
        if any(p.endswith("routes/web.php") for p in paths): laravel_indicators += 1
        if any(p.endswith("routes/api.php") for p in paths): laravel_indicators += 1
        if any("app/http/controllers" in p.lower() for p in paths): laravel_indicators += 1
        if any(p.endswith("config/app.php") for p in paths): laravel_indicators += 1
        if laravel_indicators >= 2:
            if "Laravel" not in candidates:
                candidates["Laravel"] = {"framework": "Laravel", "score": 10, "count": 1}
            else:
                candidates["Laravel"]["score"] += 10

        results = []
        for name, info in candidates.items():
            base_conf = 0.5
            if info["score"] >= 10:
                base_conf = 0.95
            elif info["score"] >= 4:
                base_conf = 0.85
            elif info["count"] >= 2:
                base_conf = 0.75
            
            # Bound confidence between 0.1 and 0.99
            confidence = min(0.99, max(0.1, base_conf + (info["count"] * 0.01)))
            results.append({
                "framework": name,
                "confidence": round(confidence, 2)
            })

        return sorted(results, key=lambda item: item["confidence"], reverse=True)
