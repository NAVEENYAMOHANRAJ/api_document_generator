"""NestJS extractor using regex parsing."""

import re
from typing import Dict, List


class NestJSExtractor:
    """Extract NestJS routes using regex parsing."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.routes = []

    @classmethod
    def extract(cls, file_path: str, content: str) -> List[Dict]:
        """Extract NestJS routes from file content."""
        extractor = cls(file_path)
        extractor._extract_controller_routes(content)
        return extractor.routes

    def _extract_controller_routes(self, content: str) -> None:
        """Extract routes from @Controller and @Get/@Post decorators."""
        # Extract controller prefix
        controller_pattern = r"@Controller\s*\(\s*['\"]([^'\"]*)['\"]"
        controller_match = re.search(controller_pattern, content)
        controller_prefix = controller_match.group(1) if controller_match else ''

        # Extract route methods
        method_pattern = r"@(Get|Post|Put|Patch|Delete|Options|Head)\s*\(\s*['\"]([^'\"]*)['\"]"
        for match in re.finditer(method_pattern, content):
            method, path = match.groups()
            full_path = self._normalize_path(controller_prefix + path)
            self.routes.append({
                'method': method.upper(),
                'path': full_path,
                'source_file': self.file_path,
                'line_number': content[:match.start()].count('\n') + 1,
                'confidence': 0.90
            })

    def _normalize_path(self, path: str) -> str:
        """Normalize path."""
        if not path.startswith('/'):
            path = '/' + path
        return path
