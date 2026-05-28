"""Stage 2: Framework Detection - Determine backend framework with confidence scoring."""

import json
from pathlib import Path
from typing import Dict, Tuple


class FrameworkDetector:
    """Detect backend framework with confidence scoring."""

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.results = {}

    def detect(self) -> Dict[str, float]:
        """Detect frameworks and return confidence scores."""
        self.results = {
            'laravel': self._detect_laravel(),
            'express': self._detect_express(),
            'fastapi': self._detect_fastapi(),
            'django': self._detect_django(),
            'spring': self._detect_spring(),
        }
        return self.results

    def get_primary_framework(self, threshold: float = 0.5) -> Tuple[str, float]:
        """Get primary framework above threshold."""
        if not self.results:
            self.detect()

        best_framework = max(self.results, key=self.results.get)
        confidence = self.results[best_framework]

        if confidence >= threshold:
            return best_framework, confidence
        return None, 0.0

    def _detect_laravel(self) -> float:
        """Detect Laravel framework."""
        score = 0.0

        # Check for artisan file (strong signal)
        if (self.repo_path / 'artisan').exists():
            score += 0.4

        # Check for composer.json with laravel/framework
        composer_file = self.repo_path / 'composer.json'
        if composer_file.exists():
            try:
                content = json.loads(composer_file.read_text())
                if 'laravel/framework' in str(content.get('require', {})):
                    score += 0.3
            except (json.JSONDecodeError, IOError):
                pass

        # Check for routes/api.php
        if (self.repo_path / 'routes' / 'api.php').exists():
            score += 0.2

        # Check for app/Http/Controllers
        if (self.repo_path / 'app' / 'Http' / 'Controllers').exists():
            score += 0.1

        return min(score, 0.99)

    def _detect_express(self) -> float:
        """Detect Express framework."""
        score = 0.0

        # Check for package.json with express
        package_file = self.repo_path / 'package.json'
        if package_file.exists():
            try:
                content = json.loads(package_file.read_text())
                deps = {**content.get('dependencies', {}), **content.get('devDependencies', {})}
                if 'express' in deps:
                    score += 0.4
            except (json.JSONDecodeError, IOError):
                pass

        # Check for routes directory
        if (self.repo_path / 'routes').exists():
            score += 0.2

        # Check for src/routes
        if (self.repo_path / 'src' / 'routes').exists():
            score += 0.2

        # Check for express.Router() in files
        score += self._check_file_content(['routes', 'src'], 'express.Router', 0.2)

        return min(score, 0.99)

    def _detect_fastapi(self) -> float:
        """Detect FastAPI framework."""
        score = 0.0

        # Check for requirements.txt or pyproject.toml with fastapi
        for req_file in ['requirements.txt', 'pyproject.toml']:
            req_path = self.repo_path / req_file
            if req_path.exists():
                try:
                    content = req_path.read_text()
                    if 'fastapi' in content:
                        score += 0.4
                except IOError:
                    pass

        # Check for app directory
        if (self.repo_path / 'app').exists():
            score += 0.1

        # Check for @app.get() or APIRouter in files
        score += self._check_file_content(['app', 'src'], '@app.get', 0.2)
        score += self._check_file_content(['app', 'src'], 'APIRouter', 0.2)

        return min(score, 0.99)

    def _detect_django(self) -> float:
        """Detect Django framework."""
        score = 0.0

        # Check for manage.py
        if (self.repo_path / 'manage.py').exists():
            score += 0.4

        # Check for urls.py
        score += self._check_file_exists(['urls.py'], 0.2)

        # Check for settings.py
        score += self._check_file_exists(['settings.py'], 0.1)

        # Check for path() or re_path() in files
        score += self._check_file_content(['app', 'apps'], 'path(', 0.2)

        return min(score, 0.99)

    def _detect_spring(self) -> float:
        """Detect Spring Boot framework."""
        score = 0.0

        # Check for pom.xml or build.gradle
        if (self.repo_path / 'pom.xml').exists():
            try:
                content = (self.repo_path / 'pom.xml').read_text()
                if 'spring-boot' in content:
                    score += 0.4
            except IOError:
                pass

        if (self.repo_path / 'build.gradle').exists():
            try:
                content = (self.repo_path / 'build.gradle').read_text()
                if 'spring-boot' in content:
                    score += 0.4
            except IOError:
                pass

        # Check for src/main/java
        if (self.repo_path / 'src' / 'main' / 'java').exists():
            score += 0.1

        # Check for @RestController in files
        score += self._check_file_content(['src'], '@RestController', 0.2)

        return min(score, 0.99)

    def _check_file_exists(self, file_names: list, score_value: float) -> float:
        """Check if any file exists in repository."""
        for file_name in file_names:
            if list(self.repo_path.rglob(file_name)):
                return score_value
        return 0.0

    def _check_file_content(self, dirs: list, pattern: str, score_value: float) -> float:
        """Check if pattern exists in files within directories."""
        for dir_name in dirs:
            dir_path = self.repo_path / dir_name
            if not dir_path.exists():
                continue

            for file_path in dir_path.rglob('*'):
                if file_path.is_file() and file_path.suffix in ['.py', '.js', '.ts', '.java', '.cs']:
                    try:
                        content = file_path.read_text(errors='ignore')
                        if pattern in content:
                            return score_value
                    except (IOError, UnicodeDecodeError):
                        pass

        return 0.0
