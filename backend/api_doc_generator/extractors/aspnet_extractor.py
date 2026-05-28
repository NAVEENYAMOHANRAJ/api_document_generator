"""ASP.NET Core extractor using regex parsing."""

import re
from typing import Dict, List


class AspNetExtractor:
    """Extract ASP.NET Core routes using regex parsing."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.routes = []

    @classmethod
    def extract(cls, file_path: str, content: str) -> List[Dict]:
        """Extract ASP.NET Core routes from file content."""
        extractor = cls(file_path)
        extractor._extract_controller_routes(content)
        return extractor.routes

    def _extract_controller_routes(self, content: str) -> None:
        """Extract routes from [Route] and [HttpGet] decorators."""
        # Extract class-level Route
        class_pattern = r"\[Route\s*\(\s*['\"]([^'\"]*)['\"]"
        class_match = re.search(class_pattern, content)
        class_prefix = class_match.group(1) if class_match else ''

        # Extract method-level HTTP mappings
        method_pattern = r"\[Http(Get|Post|Put|Patch|Delete|Options|Head)\s*\(\s*['\"]([^'\"]*)['\"]"
        for match in re.finditer(method_pattern, content):
            method, path = match.groups()
            full_path = self._normalize_path(class_prefix + path)
            self.routes.append({
                'method': method.upper(),
                'path': full_path,
                'source_file': self.file_path,
                'line_number': content[:match.start()].count('\n') + 1,
                'confidence': 0.91
            })

    def _normalize_path(self, path: str) -> str:
        """Normalize path."""
        if not path.startswith('/'):
            path = '/' + path
        return path
