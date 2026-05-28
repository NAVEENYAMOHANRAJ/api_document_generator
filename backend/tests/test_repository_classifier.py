"""
Property-based tests for RepositoryClassifier.

Tests validate:
- Framework confidence bounds (0.1-0.99)
- Repository confidence calculation
- Non-backend classification
"""

import pytest
from hypothesis import given, strategies as st
from api_doc_generator.scanner.repository_classifier import RepositoryClassifier


class TestRepositoryClassifierProperties:
    """Property-based tests for repository classification."""

    # **Feature: api-doc-enhancements, Property 1: Framework Confidence Bounds**
    # **Validates: Requirements 1.2**
    @given(
        file_paths=st.lists(
            st.text(min_size=1, max_size=100),
            min_size=1,
            max_size=50,
        ),
        content=st.dictionaries(
            st.text(min_size=1, max_size=100),
            st.text(min_size=0, max_size=1000),
            min_size=0,
            max_size=20,
        ),
    )
    def test_framework_confidence_bounds(self, file_paths, content):
        """
        For any detected framework, the confidence score SHALL be between 0.1 and 0.99 (inclusive).

        Validates: Requirements 1.2
        """
        _, framework_scores = RepositoryClassifier.calculate_repository_confidence(
            file_paths, content
        )

        for framework, confidence in framework_scores.items():
            assert isinstance(confidence, float), f"Confidence for {framework} is not float"
            assert 0.1 <= confidence <= 0.99, (
                f"Framework {framework} confidence {confidence} outside bounds [0.1, 0.99]"
            )

    # **Feature: api-doc-enhancements, Property 2: Repository Confidence Calculation**
    # **Validates: Requirements 1.3**
    def test_repository_confidence_calculation_manifest(self):
        """Test that manifest files add exactly 50 points."""
        file_paths_with = ["package.json", "src/main.js"]
        file_paths_without = ["src/main.js"]

        conf_with, _ = RepositoryClassifier.calculate_repository_confidence(file_paths_with, {})
        conf_without, _ = RepositoryClassifier.calculate_repository_confidence(file_paths_without, {})

        assert conf_with - conf_without == 50.0, "Manifest should add exactly 50 points"

    def test_repository_confidence_calculation_folders(self):
        """Test that backend folders add 30 points each."""
        file_paths_one_folder = ["src/routes/file.js"]
        file_paths_two_folders = ["src/routes/file.js", "src/controllers/file.js"]

        conf_one, _ = RepositoryClassifier.calculate_repository_confidence(file_paths_one_folder, {})
        conf_two, _ = RepositoryClassifier.calculate_repository_confidence(file_paths_two_folders, {})

        assert conf_two - conf_one == 30.0, "Each backend folder should add 30 points"

    def test_repository_confidence_calculation_content(self):
        """Test that framework content adds 40 points."""
        content_with = {"src/main.py": "from fastapi import FastAPI"}
        content_without = {"src/main.py": "print('hello')"}

        conf_with, _ = RepositoryClassifier.calculate_repository_confidence(["src/main.py"], content_with)
        conf_without, _ = RepositoryClassifier.calculate_repository_confidence(["src/main.py"], content_without)

        assert conf_with - conf_without == 40.0, "Framework content should add 40 points"

    # **Feature: api-doc-enhancements, Property 3: Non-Backend Classification**
    # **Validates: Requirements 1.4, 1.5**
    @given(
        confidence_score=st.floats(min_value=0.0, max_value=100.0),
    )
    def test_non_backend_classification(self, confidence_score):
        """
        For any repository with confidence below 15 points, the system SHALL classify
        it as non-backend and return an empty endpoint list.

        Validates: Requirements 1.4, 1.5
        """
        # Create file paths that will result in specific confidence
        file_paths = []
        content_by_path = {}

        # Build paths to achieve target confidence
        if confidence_score >= 50:
            file_paths.append("package.json")
        if confidence_score >= 80:
            file_paths.append("src/routes/users.js")
        if confidence_score >= 120:
            content_by_path["src/routes/users.js"] = "from fastapi import APIRouter"

        actual_confidence, _ = RepositoryClassifier.calculate_repository_confidence(
            file_paths, content_by_path
        )

        is_backend, _, _ = RepositoryClassifier.is_backend_repository(
            file_paths, content_by_path
        )

        # If confidence < 15, should not be backend
        if actual_confidence < 15.0:
            assert not is_backend, (
                f"Repository with confidence {actual_confidence} should not be classified as backend"
            )
        # If confidence >= 15, should be backend
        elif actual_confidence >= 15.0:
            assert is_backend, (
                f"Repository with confidence {actual_confidence} should be classified as backend"
            )


class TestRepositoryClassifierExamples:
    """Example-based tests for repository classification."""

    def test_fastapi_repository_detection(self):
        """Test detection of a FastAPI repository."""
        file_paths = [
            "requirements.txt",
            "src/main.py",
            "src/routes/users.py",
            "src/routes/posts.py",
            "src/models/user.py",
        ]
        content_by_path = {
            "requirements.txt": "fastapi==0.95.0\npydantic==2.0.0",
            "src/main.py": "from fastapi import FastAPI\napp = FastAPI()",
            "src/routes/users.py": "from fastapi import APIRouter\nrouter = APIRouter()",
        }

        is_backend, confidence, frameworks = RepositoryClassifier.is_backend_repository(
            file_paths, content_by_path
        )

        assert is_backend, "FastAPI repository should be classified as backend"
        assert confidence >= 15.0, "FastAPI repository should have confidence >= 15"
        assert "fastapi" in frameworks, "FastAPI should be detected"

    def test_laravel_repository_detection(self):
        """Test detection of a Laravel repository."""
        file_paths = [
            "composer.json",
            "routes/web.php",
            "routes/api.php",
            "app/Http/Controllers/UserController.php",
        ]
        content_by_path = {
            "routes/api.php": "Route::get('/users', [UserController::class, 'index']);",
            "app/Http/Controllers/UserController.php": "class UserController extends Controller",
        }

        is_backend, confidence, frameworks = RepositoryClassifier.is_backend_repository(
            file_paths, content_by_path
        )

        assert is_backend, "Laravel repository should be classified as backend"
        assert confidence >= 15.0, "Laravel repository should have confidence >= 15"

    def test_django_repository_detection(self):
        """Test detection of a Django repository."""
        file_paths = [
            "requirements.txt",
            "manage.py",
            "myapp/views.py",
            "myapp/urls.py",
            "myapp/models.py",
        ]
        content_by_path = {
            "requirements.txt": "Django==4.2.0\ndjangorestframework==3.14.0",
            "myapp/views.py": "from django.views import View\nfrom rest_framework import viewsets",
            "myapp/urls.py": "from django.urls import path",
        }

        is_backend, confidence, frameworks = RepositoryClassifier.is_backend_repository(
            file_paths, content_by_path
        )

        assert is_backend, "Django repository should be classified as backend"
        assert confidence >= 15.0, "Django repository should have confidence >= 15"

    def test_non_backend_repository(self):
        """Test that non-backend repositories are correctly classified."""
        file_paths = [
            "README.md",
            "LICENSE",
            "docs/guide.md",
            "examples/demo.txt",
        ]
        content_by_path = {}

        is_backend, confidence, _ = RepositoryClassifier.is_backend_repository(
            file_paths, content_by_path
        )

        assert not is_backend, "Non-backend repository should not be classified as backend"
        assert confidence < 15.0, "Non-backend repository should have confidence < 15"

    def test_frontend_repository_classification(self):
        """Test classification of frontend repository."""
        file_paths = [
            "src/App.jsx",
            "src/components/Header.jsx",
            "public/index.html",
        ]
        content_by_path = {}

        repo_type = RepositoryClassifier.classify_repository_type(
            file_paths, content_by_path
        )

        assert repo_type == "frontend", "React repository should be classified as frontend"

    def test_api_repository_classification(self):
        """Test classification of API repository."""
        file_paths = [
            "requirements.txt",
            "src/main.py",
            "src/routes/users.py",
            "src/models/user.py",
        ]
        content_by_path = {
            "requirements.txt": "fastapi==0.95.0",
            "src/main.py": "from fastapi import FastAPI\napp = FastAPI()",
            "src/routes/users.py": "from fastapi import APIRouter\nrouter = APIRouter()",
        }

        repo_type = RepositoryClassifier.classify_repository_type(
            file_paths, content_by_path
        )

        assert repo_type == "backend_api", "FastAPI repository should be classified as backend_api"

    def test_manifest_scoring(self):
        """Test that manifest files are scored correctly."""
        # With manifest
        file_paths_with_manifest = ["package.json", "src/main.js"]
        confidence_with, _ = RepositoryClassifier.calculate_repository_confidence(
            file_paths_with_manifest, {}
        )

        # Without manifest
        file_paths_without_manifest = ["src/main.js"]
        confidence_without, _ = RepositoryClassifier.calculate_repository_confidence(
            file_paths_without_manifest, {}
        )

        # Manifest should add 50 points
        assert confidence_with - confidence_without == 50.0, (
            "Manifest should add exactly 50 points"
        )

    def test_folder_structure_scoring(self):
        """Test that backend folder structures are scored correctly."""
        # With backend folders
        file_paths_with_folders = [
            "src/routes/users.js",
            "src/controllers/auth.js",
            "src/middleware/auth.js",
        ]
        confidence_with, _ = RepositoryClassifier.calculate_repository_confidence(
            file_paths_with_folders, {}
        )

        # Without backend folders
        file_paths_without_folders = ["src/main.js", "src/utils.js"]
        confidence_without, _ = RepositoryClassifier.calculate_repository_confidence(
            file_paths_without_folders, {}
        )

        # Backend folders should add points
        assert confidence_with > confidence_without, (
            "Backend folder structures should increase confidence"
        )

    def test_framework_content_scoring(self):
        """Test that framework-specific content is scored correctly."""
        # With framework content
        content_with = {
            "src/main.py": "from fastapi import FastAPI\napp = FastAPI()"
        }
        confidence_with, frameworks_with = RepositoryClassifier.calculate_repository_confidence(
            ["src/main.py"], content_with
        )

        # Without framework content
        content_without = {"src/main.py": "print('hello')"}
        confidence_without, frameworks_without = RepositoryClassifier.calculate_repository_confidence(
            ["src/main.py"], content_without
        )

        # Framework content should add points
        assert confidence_with > confidence_without, (
            "Framework-specific content should increase confidence"
        )
        assert "fastapi" in frameworks_with, "FastAPI should be detected in frameworks"

    def test_confidence_bounds_in_calculation(self):
        """Test that calculated confidence stays within reasonable bounds."""
        # Maximum possible confidence
        file_paths = [
            "package.json",
            "requirements.txt",
            "pom.xml",
            "src/routes/users.js",
            "src/controllers/auth.js",
            "src/middleware/auth.js",
        ]
        content_by_path = {
            "src/main.py": "from fastapi import FastAPI",
            "src/routes/users.js": "from fastapi import APIRouter",
        }

        confidence, _ = RepositoryClassifier.calculate_repository_confidence(
            file_paths, content_by_path
        )

        # Confidence should be reasonable (not negative, not infinite)
        assert confidence >= 0.0, "Confidence should not be negative"
        assert confidence <= 500.0, "Confidence should be bounded reasonably"
