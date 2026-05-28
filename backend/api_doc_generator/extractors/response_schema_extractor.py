"""Stage 10: Response Schema Extraction - Extract response body schemas from source code."""

import re
from pathlib import Path
from typing import Dict, Optional, List


class ResponseSchemaExtractor:
    """Extract response body schemas from controller code."""

    def __init__(self, framework: str = "laravel"):
        self.framework = framework

    def extract(self, file_path: str, method_name: str) -> Optional[Dict]:
        """Extract response schema from controller method."""
        if not Path(file_path).exists():
            return None

        content = Path(file_path).read_text()

        if self.framework == "laravel":
            return self._extract_laravel(content, method_name)
        elif self.framework == "express":
            return self._extract_express(content, method_name)
        elif self.framework == "fastapi":
            return self._extract_fastapi(content, method_name)

        return None

    def _extract_laravel(self, content: str, method_name: str) -> Optional[Dict]:
        """Extract Laravel response schema."""
        # Find method definition
        method_pattern = rf"function\s+{method_name}\s*\(\s*([^)]*)\s*\)"
        method_match = re.search(method_pattern, content)
        if not method_match:
            return None

        method_start = method_match.start()
        method_body_start = content.find("{", method_start)
        method_body_end = self._find_matching_brace(content, method_body_start)
        method_body = content[method_body_start:method_body_end]

        # Extract return statements
        responses = {}

        # Pattern: return response()->json(...)
        json_pattern = r"return\s+response\(\)->json\s*\(([\s\S]*?)\)"
        for match in re.finditer(json_pattern, method_body):
            responses[200] = {
                "type": "object",
                "detection_method": "response_json",
                "confidence": 0.80
            }

        # Pattern: return UserResource::make(...)
        resource_pattern = r"return\s+(\w+Resource)::make\s*\("
        for match in re.finditer(resource_pattern, method_body):
            resource_class = match.group(1)
            responses[200] = {
                "type": "object",
                "resource_class": resource_class,
                "detection_method": "resource_class",
                "confidence": 0.85
            }

        # Pattern: return User::all()
        collection_pattern = r"return\s+(\w+)::all\s*\(\)"
        for match in re.finditer(collection_pattern, method_body):
            model_class = match.group(1)
            responses[200] = {
                "type": "array",
                "items": {
                    "type": "object",
                    "model_class": model_class
                },
                "detection_method": "model_collection",
                "confidence": 0.75
            }

        # Extract status codes
        status_pattern = r"->status\s*\(\s*(\d+)\s*\)"
        for match in re.finditer(status_pattern, method_body):
            status_code = int(match.group(1))
            if status_code not in responses:
                responses[status_code] = {
                    "type": "object",
                    "detection_method": "status_code",
                    "confidence": 0.60
                }

        return responses if responses else None

    def _extract_express(self, content: str, method_name: str) -> Optional[Dict]:
        """Extract Express response schema."""
        # Look for res.json() calls
        return None

    def _extract_fastapi(self, content: str, method_name: str) -> Optional[Dict]:
        """Extract FastAPI response schema."""
        # Look for response_model definitions
        return None

    def _find_matching_brace(self, content: str, start: int) -> int:
        """Find matching closing brace."""
        count = 1
        i = start + 1
        while i < len(content) and count > 0:
            if content[i] == "{":
                count += 1
            elif content[i] == "}":
                count -= 1
            i += 1
        return i
