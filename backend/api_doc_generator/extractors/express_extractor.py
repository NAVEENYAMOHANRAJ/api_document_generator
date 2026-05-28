"""Express extractor using regex parsing."""

import re
from typing import Dict, List


class ExpressExtractor:
    """Extract Express routes using regex parsing."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.routes = []

    @classmethod
    def extract(cls, file_path: str, content: str) -> List[Dict]:
        """Extract Express routes from file content."""
        extractor = cls(file_path)
        extractor._extract_routes(content)
        return extractor.routes

    def _extract_routes(self, content: str) -> None:
        """Extract routes from app/router methods."""
        pattern = r"(app|router)\.(get|post|put|patch|delete|options|head)\s*\(\s*['\"]([^'\"]+)['\"]"
        for match in re.finditer(pattern, content, re.IGNORECASE):
            _, method, path = match.groups()
            self.routes.append({
                'method': method.upper(),
                'path': path,
                'source_file': self.file_path,
                'line_number': content[:match.start()].count('\n') + 1,
                'confidence': 0.88
            })
