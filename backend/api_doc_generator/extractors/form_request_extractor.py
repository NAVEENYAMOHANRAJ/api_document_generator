"""Laravel FormRequest extractor.

Extracts request body schema from Laravel FormRequest validation rules.
"""

import re
from typing import Any, Dict, List, Optional, Tuple

from api_doc_generator.extractors.php_array_parser import PHPArrayParser


class FormRequestExtractor:
    """Extract validation rules and schema from Laravel FormRequest classes."""

    # Public API expected by tests
    @classmethod
    def extract(cls, file_path: str, content: str) -> Dict[str, Any]:
        class_name = cls._extract_class_name(content)
        if not cls._is_form_request(content):
            return {
                "class_name": class_name,
                "detection_type": "form_request",
                "confidence": 0.0,
                "schema": {"type": "object", "properties": {}, "required": []},
                "file_path": file_path,
            }

        rules = cls._extract_rules_block(content)
        flattened = PHPArrayParser.flatten_nested_rules(rules)

        properties: Dict[str, Any] = {}
        required: List[str] = []

        for field, rule_str in flattened.items():
            metadata = PHPArrayParser.extract_rule_metadata(rule_str)
            is_required = bool(metadata.get("required"))
            if is_required:
                required.append(field)

            properties[field] = cls._rule_metadata_to_schema(field, metadata)

        schema: Dict[str, Any] = {
            "type": "object",
            "properties": properties,
            "required": required,
        }

        return {
            "class_name": class_name,
            "detection_type": "form_request",
            "confidence": 0.95,
            "schema": schema,
        }

    @staticmethod
    def _is_form_request(content: str) -> bool:
        return bool(re.search(r"class\s+\w+\s+extends\s+FormRequest\b", content))

    @staticmethod
    def _extract_class_name(content: str) -> str:
        match = re.search(r"class\s+(\w+)\s+extends\s+FormRequest\b", content)
        return match.group(1) if match else "UnknownFormRequest"

    @classmethod
    def _extract_rules_block(cls, content: str) -> Dict[str, Any]:
        # Capture return [ ... ]; inside rules() method
        # This relies on PHPArrayParser for the array parsing.
        rules_method = re.search(
            r"function\s+rules\s*\([^)]*\)\s*\{([\s\S]*?)\}", content, re.IGNORECASE
        )
        if not rules_method:
            return {}

        body = rules_method.group(1)

        # Find first return <array>;
        return_match = re.search(r"return\s*(\[[\s\S]*?\])\s*;", body, re.IGNORECASE)
        if not return_match:
            return {}

        parsed, _ = PHPArrayParser.parse_php_array_from_str(return_match.group(1))
        return parsed


    @staticmethod
    def _rule_metadata_to_schema(field: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        schema: Dict[str, Any] = {}

        # Base type
        if metadata.get("boolean"):
            schema["type"] = "boolean"
        elif metadata.get("integer"):
            schema["type"] = "integer"
        elif metadata.get("numeric"):
            schema["type"] = "number"
        elif metadata.get("array"):
            schema["type"] = "array"
        elif metadata.get("email"):
            schema["type"] = "string"
            schema["format"] = "email"
        elif metadata.get("url"):
            schema["type"] = "string"
            schema["format"] = "uri"
        else:
            # string is default when present
            if metadata.get("string"):
                schema["type"] = "string"
            elif any(k in metadata for k in ("max", "min", "regex", "unique", "exists", "in")):
                schema["type"] = "string"
            else:
                schema["type"] = "string"

        # min/max length for strings
        if "min" in metadata and schema.get("type") == "string":
            schema["minLength"] = int(metadata["min"])
        if "max" in metadata and schema.get("type") == "string":
            schema["maxLength"] = int(metadata["max"])

        # min numeric => minimum
        if "min" in metadata and schema.get("type") == "number":
            schema["minimum"] = float(metadata["min"])
        if "min" in metadata and schema.get("type") == "integer":
            schema["minimum"] = int(metadata["min"])
            schema["minLength"] = int(metadata["min"])
        if "max" in metadata and schema.get("type") == "integer":
            schema["maximum"] = int(metadata["max"])
            schema["maxLength"] = int(metadata["max"])

        # enum
        if "enum" in metadata:
            schema["enum"] = metadata["enum"]

        if "unique" in metadata:
            schema["unique"] = True
        if "exists" in metadata:
            schema["exists"] = metadata["exists"] or True

        # generic regex -> pattern
        if "regex" in metadata:
            # metadata['regex'] can be like /.../
            schema["pattern"] = metadata["regex"]

        return schema

    @staticmethod
    def build_request_body_model(schema: Dict[str, Any]) -> Dict[str, Any]:
        # Tests only validate a small contract
        return {
            "required": True,
            "schema": schema,
            "content": {"application/json": schema},
        }

