"""Spring Boot extractor using regex parsing."""

import re
from typing import Dict, List


class SpringBootExtractor:
    """Extract Spring Boot routes using regex parsing."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.routes = []

    @classmethod
    def extract(cls, file_path: str, content: str) -> List[Dict]:
        """Extract Spring Boot routes from file content."""
        extractor = cls(file_path)
        extractor._extract_controller_routes(content)
        return extractor.routes

    def _extract_controller_routes(self, content: str) -> None:
        """Extract routes from @RequestMapping and @GetMapping decorators."""
        # Extract class-level RequestMapping
        class_pattern = r"@RequestMapping\s*\(\s*['\"]([^'\"]*)['\"]"
        class_match = re.search(class_pattern, content)
        class_prefix = class_match.group(1) if class_match else ''

        # Extract method-level mappings
        method_pattern = r"@(GetMapping|PostMapping|PutMapping|PatchMapping|DeleteMapping)\s*\(\s*['\"]([^'\"]*)['\"]"
        for match in re.finditer(method_pattern, content):
            mapping_type, path = match.groups()
            method = mapping_type.replace('Mapping', '').upper()
            full_path = self._normalize_path(class_prefix + path)
            self.routes.append({
                'method': method,
                'path': full_path,
                'source_file': self.file_path,
                'line_number': content[:match.start()].count('\n') + 1,
                'confidence': 0.92
            })

    def _normalize_path(self, path: str) -> str:
        """Normalize path."""
        if not path.startswith('/'):
            path = '/' + path
        return path
