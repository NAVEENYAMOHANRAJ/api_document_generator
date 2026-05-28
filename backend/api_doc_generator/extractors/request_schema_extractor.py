"""Stage 9: Request Schema Extraction - Extract request body schemas from source code."""

import re
from pathlib import Path
from typing import Dict, Optional, List


class RequestSchemaExtractor:
    """Extract request body schemas from controller code."""

    def __init__(self, framework: str = "laravel"):
        self.framework = framework

    def extract(self, file_path: str, method_name: str) -> Optional[Dict]:
        """Extract request schema from controller method."""
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
        """Extract Laravel request schema."""
        # Find method definition
        method_pattern = rf"function\s+{method_name}\s*\(\s*([^)]*)\s*\)"
        method_match = re.search(method_pattern, content)
        if not method_match:
            return None

        method_start = method_match.start()
        method_body_start = content.find("{", method_start)
        method_body_end = self._find_matching_brace(content, method_body_start)
        method_body = content[method_body_start:method_body_end]

        # Extract validation rules
        schema = self._extract_laravel_validation(method_body)
        if schema:
            return {
                "type": "object",
                "properties": schema,
                "detection_method": "laravel_validation",
                "confidence": 0.85
            }

        # Check for FormRequest type hint
        form_request = self._extract_form_request(method_match.group(1))
        if form_request:
            return {
                "type": "object",
                "form_request_class": form_request,
                "detection_method": "form_request",
                "confidence": 0.80
            }

        return None

    def _extract_laravel_validation(self, method_body: str) -> Optional[Dict]:
        """Extract validation rules from $request->validate()."""
        # Pattern: $request->validate([...])
        pattern = r"\$request->validate\s*\(\s*\[([\s\S]*?)\]\s*\)"
        match = re.search(pattern, method_body)
        if not match:
            return None

        rules_str = match.group(1)
        schema = {}

        # Parse each rule
        for line in rules_str.split(","):
            line = line.strip()
            if not line:
                continue

            # Pattern: 'field' => 'rules'
            field_match = re.match(r"['\"]([^'\"]+)['\"]\s*=>\s*['\"]([^'\"]+)['\"]", line)
            if field_match:
                field_name = field_match.group(1)
                rules = field_match.group(2)

                # Parse rules
                field_schema = self._parse_laravel_rules(rules)
                schema[field_name] = field_schema

        return schema if schema else None

    def _parse_laravel_rules(self, rules: str) -> Dict:
        """Parse Laravel validation rules into schema."""
        schema = {"type": "string"}  # Default type

        rules_list = [r.strip() for r in rules.split("|")]

        for rule in rules_list:
            if rule == "required":
                schema["required"] = True
            elif rule == "email":
                schema["format"] = "email"
            elif rule == "integer":
                schema["type"] = "integer"
            elif rule == "boolean":
                schema["type"] = "boolean"
            elif rule == "array":
                schema["type"] = "array"
            elif rule.startswith("max:"):
                schema["maxLength"] = int(rule.split(":")[1])
            elif rule.startswith("min:"):
                schema["minLength"] = int(rule.split(":")[1])

        return schema

    def _extract_form_request(self, parameters: str) -> Optional[str]:
        """Extract FormRequest class from method parameters."""
        # Pattern: StoreUserRequest $request
        pattern = r"(\w+Request)\s+\$\w+"
        match = re.search(pattern, parameters)
        return match.group(1) if match else None

    def _extract_express(self, content: str, method_name: str) -> Optional[Dict]:
        """Extract Express request schema."""
        # Look for validation middleware or schema definitions
        return None

    def _extract_fastapi(self, content: str, method_name: str) -> Optional[Dict]:
        """Extract FastAPI request schema."""
        # Look for Pydantic model definitions
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
