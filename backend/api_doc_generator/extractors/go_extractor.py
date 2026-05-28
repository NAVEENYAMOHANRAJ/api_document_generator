"""Go (Gin/Fiber) extractor using regex parsing."""

import re
from typing import Dict, List


class GoExtractor:
    """Extract Go Gin/Fiber routes using regex parsing."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.routes = []

    @classmethod
    def extract(cls, file_path: str, content: str) -> List[Dict]:
        """Extract Go routes from file content."""
        extractor = cls(file_path)
        extractor._extract_routes(content)
        return extractor.routes

    def _extract_routes(self, content: str) -> None:
        """Extract routes from router methods."""
        # Match: router.GET("/path", handler) or app.Post("/path", handler)
        pattern = r"(router|app|r|engine)\.(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)\s*\(\s*['\"]([^'\"]+)['\"]"
        for match in re.finditer(pattern, content, re.IGNORECASE):
            _, method, path = match.groups()
            self.routes.append({
                'method': method.upper(),
                'path': path,
                'source_file': self.file_path,
                'line_number': content[:match.start()].count('\n') + 1,
                'confidence': 0.87
            })
