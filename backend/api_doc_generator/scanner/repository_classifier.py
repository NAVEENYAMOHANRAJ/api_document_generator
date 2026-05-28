"""
Repository classifier to determine if a repository contains backend code.

This module implements confidence-based backend detection using:
- Manifest detection (+50 points): package.json, requirements.txt, pom.xml, etc.
- Folder structure (+30 points): routes, controllers, api, app, src, backend, server, config
- Content patterns (+40 points): framework imports, route definitions, HTTP methods

Threshold: 15 points minimum for backend classification
"""

from typing import Dict, List, Optional, Tuple
from pathlib import PurePosixPath


class RepositoryClassifier:
    """Classify repositories and calculate backend confidence scores."""

    # Manifest files that indicate backend code (+50 points each)
    BACKEND_MANIFESTS = {
        "package.json",  # Node.js (Express, NestJS, etc.)
        "requirements.txt",  # Python (Flask, Django, FastAPI)
        "setup.py",  # Python packages
        "pyproject.toml",  # Python packages
        "pom.xml",  # Java/Spring Boot
        "build.gradle",  # Java/Gradle
        "composer.json",  # PHP/Laravel
        "Gemfile",  # Ruby/Rails
        "go.mod",  # Go
        "Cargo.toml",  # Rust
        ".csproj",  # C#/.NET
        "pubspec.yaml",  # Dart/Flutter
    }

    # Folder structures that indicate backend code (+30 points each)
    BACKEND_FOLDERS = {
        "routes",
        "controllers",
        "api",
        "app",
        "src",
        "backend",
        "server",
        "config",
        "middleware",
        "services",
        "models",
        "serializers",
        "handlers",
        "endpoints",
    }

    # Folders to ignore when scoring
    IGNORE_FOLDERS = {
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
        "benchmark",
        "deps",
        "generated",
        "lib",
        "libs",
        "third_party",
        "3rdparty",
    }

    # Framework-specific content patterns (+40 points each)
    FRAMEWORK_PATTERNS = {
        "fastapi": [
            "from fastapi import",
            "import fastapi",
            "apirouter",
            "@app.get",
            "@app.post",
            "@router.get",
            "@router.post",
        ],
        "flask": [
            "from flask import",
            "import flask",
            "@app.route",
            "@bp.route",
            "flask.blueprints",
        ],
        "django": [
            "from django",
            "import django",
            "django.urls",
            "django.views",
            "from rest_framework",
        ],
        "laravel": [
            "route::",
            "Route::get",
            "Route::post",
            "Route::put",
            "Route::delete",
            "Route::resource",
        ],
        "express": [
            "express.router",
            "app.get",
            "app.post",
            "app.put",
            "app.delete",
            "require('express')",
            'require("express")',
        ],
        "nestjs": [
            "@nestjs/common",
            "@controller",
            "@get",
            "@post",
            "@put",
            "@delete",
        ],
        "spring_boot": [
            "@restcontroller",
            "@requestmapping",
            "@getmapping",
            "@postmapping",
            "@putmapping",
            "@deletemapping",
            "import org.springframework",
        ],
        "aspnet": [
            "[apicontroller]",
            "[httpget]",
            "[httppost]",
            "[httpput]",
            "[httpdelete]",
            "using system.web.mvc",
        ],
        "go": [
            "github.com/gin-gonic/gin",
            "github.com/gofiber/fiber",
            "github.com/labstack/echo",
            "func (r *router)",
        ],
    }

    @classmethod
    def calculate_repository_confidence(
        cls, file_paths: List[str], content_by_path: Optional[Dict[str, str]] = None
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calculate repository confidence score and framework scores.

        Returns:
            Tuple of (total_confidence, framework_scores_dict)
            - total_confidence: Sum of manifest (+50), folder (+30), and content (+40) boosts
            - framework_scores_dict: Individual framework confidence scores

        Validates: Requirements 1.3
        """
        content_by_path = content_by_path or {}
        total_score = 0.0
        framework_scores = {}

        # Check for manifest files (+50 points each)
        manifest_score = cls._score_manifests(file_paths)
        total_score += manifest_score

        # Check for backend folder structures (+30 points each)
        folder_score = cls._score_folders(file_paths)
        total_score += folder_score

        # Check for framework-specific content patterns (+40 points each)
        content_score, framework_scores = cls._score_content(content_by_path)
        total_score += content_score

        return total_score, framework_scores

    @classmethod
    def is_backend_repository(
        cls, file_paths: List[str], content_by_path: Optional[Dict[str, str]] = None
    ) -> Tuple[bool, float, Dict[str, float]]:
        """
        Determine if repository is a backend repository.

        Threshold: 15 points minimum for backend classification

        Returns:
            Tuple of (is_backend, confidence, framework_scores)

        Validates: Requirements 1.4, 1.5
        """
        confidence, framework_scores = cls.calculate_repository_confidence(
            file_paths, content_by_path
        )

        # Threshold: 15 points minimum
        is_backend = confidence >= 15.0

        return is_backend, confidence, framework_scores

    @classmethod
    def classify_repository_type(
        cls, file_paths: List[str], content_by_path: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Classify repository type.

        Returns:
            One of: 'backend_api', 'backend_web', 'frontend', 'library', 'other'

        Validates: Requirements 1.3
        """
        # Check if it's frontend first (before backend check)
        if cls._is_frontend_repository(file_paths):
            return "frontend"

        # Check if it's library
        if cls._is_library_repository(file_paths):
            return "library"

        is_backend, confidence, framework_scores = cls.is_backend_repository(
            file_paths, content_by_path
        )

        if not is_backend:
            return "other"

        # It's backend - determine if API or web
        if cls._is_api_repository(file_paths, content_by_path):
            return "backend_api"
        else:
            return "backend_web"

    @classmethod
    def _score_manifests(cls, file_paths: List[str]) -> float:
        """
        Score based on manifest files (+50 points each).

        Validates: Requirements 1.3
        """
        score = 0.0
        normalized_paths = {str(PurePosixPath(p)).lower() for p in file_paths}

        for manifest in cls.BACKEND_MANIFESTS:
            # Check if manifest exists in any path
            if any(manifest.lower() in path for path in normalized_paths):
                score += 50.0
                break  # Only count once

        return score

    @classmethod
    def _score_folders(cls, file_paths: List[str]) -> float:
        """
        Score based on backend folder structures (+30 points each).

        Validates: Requirements 1.3
        """
        score = 0.0
        found_folders = set()

        for path in file_paths:
            path_lower = str(PurePosixPath(path)).lower()
            parts = PurePosixPath(path).parts

            # Skip ignored folders
            if any(part.lower() in cls.IGNORE_FOLDERS for part in parts):
                continue

            # Check for backend folders
            for part in parts:
                if part.lower() in cls.BACKEND_FOLDERS:
                    found_folders.add(part.lower())

        # Score: +30 points for each unique backend folder found
        score = len(found_folders) * 30.0

        return score

    @classmethod
    def _score_content(
        cls, content_by_path: Dict[str, str]
    ) -> Tuple[float, Dict[str, float]]:
        """
        Score based on framework-specific content patterns (+40 points each).

        Returns:
            Tuple of (total_content_score, framework_scores_dict)

        Validates: Requirements 1.3
        """
        score = 0.0
        framework_scores = {}
        found_frameworks = set()

        for path, content in content_by_path.items():
            content_lower = content.lower()

            # Check each framework's patterns
            for framework, patterns in cls.FRAMEWORK_PATTERNS.items():
                if framework in found_frameworks:
                    continue

                # Check if any pattern matches
                if any(pattern.lower() in content_lower for pattern in patterns):
                    found_frameworks.add(framework)
                    score += 40.0

                    # Calculate framework confidence (0.1-0.99)
                    matches = sum(
                        1 for pattern in patterns if pattern.lower() in content_lower
                    )
                    confidence = min(0.99, max(0.1, 0.5 + (matches * 0.1)))
                    framework_scores[framework] = round(confidence, 2)

        return score, framework_scores

    @classmethod
    def _is_frontend_repository(cls, file_paths: List[str]) -> bool:
        """
        Check if repository is a frontend project.

        Indicators:
        - HTML/CSS/JS/JSX/TSX/Vue files
        - No backend frameworks
        """
        normalized_paths = {str(PurePosixPath(p)).lower() for p in file_paths}

        # Check for HTML/CSS/JS files
        frontend_extensions = {".html", ".css", ".jsx", ".tsx", ".vue"}
        if any(path.endswith(ext) for path in normalized_paths for ext in frontend_extensions):
            return True

        return False

    @classmethod
    def _is_library_repository(cls, file_paths: List[str]) -> bool:
        """
        Check if repository is a library/package.

        Indicators:
        - setup.py, pyproject.toml, package.json with "type": "module"
        - No main application entry point
        - Primarily utility/helper code
        """
        normalized_paths = {str(PurePosixPath(p)).lower() for p in file_paths}

        library_indicators = {"setup.py", "pyproject.toml", "cargo.toml", "gemfile"}

        return any(indicator in path for path in normalized_paths for indicator in library_indicators)

    @classmethod
    def _is_api_repository(
        cls, file_paths: List[str], content_by_path: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        Check if backend repository is an API (vs web app).

        Indicators:
        - REST/GraphQL route definitions
        - JSON responses
        - No HTML templates
        - No form handling
        """
        content_by_path = content_by_path or {}

        # Check for REST/GraphQL patterns
        api_patterns = {
            "rest",
            "graphql",
            "json",
            "api",
            "endpoint",
            "route",
            "controller",
        }

        for content in content_by_path.values():
            content_lower = content.lower()
            if any(pattern in content_lower for pattern in api_patterns):
                return True

        # Check for absence of template files
        template_extensions = {".html", ".jinja", ".erb", ".blade.php", ".pug"}
        has_templates = any(
            path.endswith(ext) for path in file_paths for ext in template_extensions
        )

        return not has_templates
