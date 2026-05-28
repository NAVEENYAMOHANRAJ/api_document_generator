"""Stage 1: Repository Scanner - Identify backend structure safely."""

import os
import json
from pathlib import Path
from typing import Dict, List, Set


class RepositoryScanner:
    """Scan repository structure and identify backend files."""

    # Directories to ignore
    IGNORE_DIRS = {
        'node_modules', 'vendor', 'dist', 'build', 'coverage', '.git',
        '__pycache__', '.pytest_cache', 'venv', 'env', '.venv',
        'bin', 'obj', 'target', '.gradle', '.maven'
    }

    # File extensions to ignore
    IGNORE_EXTENSIONS = {
        '.so', '.dll', '.exe', '.o', '.a', '.lib', '.pyc', '.class',
        '.jar', '.zip', '.tar', '.gz', '.rar', '.7z'
    }

    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        'laravel': {
            'files': ['artisan', 'composer.json'],
            'dirs': ['routes', 'app/Http/Controllers'],
            'content_patterns': ['laravel/framework']
        },
        'express': {
            'files': ['package.json'],
            'dirs': ['src/routes', 'routes'],
            'content_patterns': ['express']
        },
        'fastapi': {
            'files': ['requirements.txt', 'pyproject.toml'],
            'dirs': ['app', 'src'],
            'content_patterns': ['fastapi']
        },
        'django': {
            'files': ['manage.py'],
            'dirs': ['app', 'apps'],
            'content_patterns': ['django']
        },
        'spring': {
            'files': ['pom.xml', 'build.gradle'],
            'dirs': ['src/main/java'],
            'content_patterns': ['spring-boot']
        }
    }

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.results = {
            'framework': None,
            'language': None,
            'route_files': [],
            'controller_dirs': [],
            'middleware_files': [],
            'dto_files': [],
            'model_files': [],
            'total_files': 0,
            'ignored_dirs': 0
        }

    def scan(self) -> Dict:
        """Scan repository and return structure."""
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {self.repo_path}")

        self._scan_directory(self.repo_path)
        self._detect_framework()
        self._detect_language()

        return self.results

    def _scan_directory(self, path: Path, depth: int = 0) -> None:
        """Recursively scan directory structure."""
        if depth > 5:  # Limit depth
            return

        try:
            for item in path.iterdir():
                # Skip ignored directories
                if item.is_dir():
                    if item.name in self.IGNORE_DIRS or item.name.startswith('.'):
                        self.results['ignored_dirs'] += 1
                        continue

                    self._scan_directory(item, depth + 1)
                    continue

                # Skip ignored file extensions
                if item.suffix in self.IGNORE_EXTENSIONS:
                    continue

                self.results['total_files'] += 1

                # Categorize files
                self._categorize_file(item)

        except (PermissionError, OSError):
            pass

    def _categorize_file(self, file_path: Path) -> None:
        """Categorize file by type."""
        rel_path = str(file_path.relative_to(self.repo_path))

        # Route files
        if file_path.name in ['api.php', 'web.php', 'routes.ts', 'routes.js', 'urls.py']:
            self.results['route_files'].append(rel_path)

        # Controller files
        if 'controller' in file_path.name.lower() or 'handler' in file_path.name.lower():
            self.results['controller_dirs'].append(rel_path)

        # Middleware files
        if 'middleware' in file_path.name.lower():
            self.results['middleware_files'].append(rel_path)

        # DTO/Model files
        if any(x in file_path.name.lower() for x in ['dto', 'request', 'response', 'model', 'entity']):
            if 'dto' in file_path.name.lower() or 'request' in file_path.name.lower():
                self.results['dto_files'].append(rel_path)
            else:
                self.results['model_files'].append(rel_path)

    def _detect_framework(self) -> None:
        """Detect backend framework."""
        for framework, patterns in self.FRAMEWORK_PATTERNS.items():
            score = 0

            # Check for framework files
            for file_name in patterns['files']:
                file_path = self.repo_path / file_name
                if file_path.exists():
                    score += 2
                    # Check content for framework indicators
                    if file_name in ['composer.json', 'package.json', 'requirements.txt', 'pom.xml']:
                        try:
                            content = file_path.read_text()
                            for pattern in patterns['content_patterns']:
                                if pattern in content:
                                    score += 2
                        except (UnicodeDecodeError, IOError):
                            pass

            # Check for framework directories
            for dir_name in patterns['dirs']:
                dir_path = self.repo_path / dir_name
                if dir_path.exists():
                    score += 1

            if score >= 3:
                self.results['framework'] = framework
                break

    def _detect_language(self) -> None:
        """Detect primary programming language."""
        extensions = {}

        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file() and file_path.suffix:
                ext = file_path.suffix
                extensions[ext] = extensions.get(ext, 0) + 1

        # Map extensions to languages
        language_map = {
            '.php': 'PHP',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.py': 'Python',
            '.java': 'Java',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust'
        }

        if extensions:
            most_common_ext = max(extensions, key=extensions.get)
            self.results['language'] = language_map.get(most_common_ext, 'Unknown')
