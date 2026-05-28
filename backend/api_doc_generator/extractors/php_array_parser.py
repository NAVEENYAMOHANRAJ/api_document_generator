"""PHP array parser for Laravel validation rules.

This module is intentionally lightweight: it tokenizes PHP array syntax used in
Laravel validation rules, then extracts a Python representation.

The unit tests in `backend/tests/test_php_array_parser.py` define the required API.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple


def _strip_quotes(s: str) -> str:
    s = (s or "").strip()
    if len(s) >= 2 and ((s[0] == s[-1] == "'") or (s[0] == s[-1] == '"')):
        return s[1:-1]
    return s


class PHPArrayParser:
    """Parse PHP arrays and extract Laravel validation rule metadata.

    Supported by unit tests:
    - associative arrays using short syntax: ['k' => 'v', ...]
    - associative arrays using array(...): array('k' => 'v', ...)
    - nested associative arrays: ['user' => ['name' => 'John', ...]]
    - list values in nested position: ['tags' => ['admin','user',...]]
    - values that include punctuation in original PHP:
      email john@example.com => tokens [john, example, com]
      rule strings required|email|max:255 => tokens [required, email, max, 255]
    - floats like 19.99 => tokens [19, 99]
    """ 


    @staticmethod
    def _unquote_string(value: str) -> str:
        return _strip_quotes(value)

    @classmethod
    def parse_php_array(cls, tokens: List[str], start_index: int) -> Tuple[Dict[Any, Any], int]:
        """Parse PHP short arrays and array(...) calls from tokenized source."""
        if not tokens:
            return {}, 0

        i = start_index
        close_token = None
        if tokens[i].lower() == "array":
            i += 1
            if i < len(tokens) and tokens[i] == "(":
                close_token = ")"
                i += 1
        elif tokens[i] == "[":
            close_token = "]"
            i += 1

        result: Dict[Any, Any] = {}
        list_index = 0

        while i < len(tokens):
            if close_token and tokens[i] == close_token:
                return result, i + 1
            if tokens[i] == ",":
                i += 1
                continue

            key_or_value, i = cls._parse_value(tokens, i)

            if i < len(tokens) and tokens[i] == "=>":
                i += 1
                value, i = cls._parse_value(tokens, i)
                result[key_or_value] = value
            else:
                result[list_index] = key_or_value
                list_index += 1

            if i < len(tokens) and tokens[i] == ",":
                i += 1

        return result, i


    @classmethod
    def _parse_value(cls, tokens: List[str], i: int) -> Tuple[Any, int]:
        if i >= len(tokens):
            return None, i

        tok = tokens[i]

        if tok == '[':
            parsed, j = cls.parse_php_array(tokens, i)
            return parsed, j

        if tok.lower() == 'array' and i + 1 < len(tokens) and tokens[i + 1] == '(':
            parsed, j = cls.parse_php_array(tokens, i)
            return parsed, j

        if tok.lower() == 'true':
            return True, i + 1
        if tok.lower() == 'false':
            return False, i + 1
        if tok.lower() == 'null':
            return None, i + 1

        if isinstance(tok, str) and (tok.startswith("'") or tok.startswith('"')):
            return cls._unquote_string(tok), i + 1

        if re.fullmatch(r"-?\d+\.\d+", tok or ""):
            return float(tok), i + 1
        if re.fullmatch(r"-?\d+", tok or ""):
            return int(tok), i + 1

        # Fallback identifier
        return tok, i + 1

    @classmethod
    def parse_php_array_from_str(cls, array_source: str) -> Tuple[Dict[Any, Any], int]:
        # Use base_parser tokenizer
        from api_doc_generator.extractors.base_parser import tokenize_code

        tokens = tokenize_code(array_source)
        parsed, idx = cls.parse_php_array(tokens, 0)
        return parsed, idx

    @classmethod
    def extract_array_from_call(cls, tokens: List[str], function_name: str) -> Optional[Dict[Any, Any]]:
        """Extract array argument from calls like $request->validate([ ... ]) or Validator::make($d, [ ... ])."""
        fn = function_name
        for i, tok in enumerate(tokens):
            if tok == fn:
                j = i + 1
                depth = 0
                while j < len(tokens):
                    if tokens[j] == "(":
                        depth += 1
                    elif tokens[j] == ")":
                        if depth == 0:
                            break
                        depth -= 1
                    if tokens[j] == '[':
                        parsed, _ = cls.parse_php_array(tokens, j)
                        return parsed
                    if tokens[j].lower() == 'array' and j + 1 < len(tokens) and tokens[j + 1] == '(':
                        parsed, _ = cls.parse_php_array(tokens, j)
                        return parsed
                    j += 1
        return None

    @classmethod
    def flatten_nested_rules(cls, rules: Dict[str, Any]) -> Dict[str, Any]:
        flattened: Dict[str, Any] = {}

        def rec(prefix: str, obj: Any):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    rec(f"{prefix}.{k}" if prefix else k, v)
            else:
                flattened[prefix] = obj

        rec("", rules)
        return flattened

    @classmethod
    def extract_rule_metadata(cls, rule_str: str) -> Dict[str, Any]:
        parts = [p.strip() for p in (rule_str or "").split('|') if p.strip()]
        metadata: Dict[str, Any] = {}

        for part in parts:
            if ':' in part:
                name, val = part.split(':', 1)
                name = name.strip()
                val = val.strip()
                if name in ('min', 'max'):
                    metadata[name] = val
                elif name == 'between':
                    # between:18,100
                    a, b = val.split(',', 1)
                    metadata['min'] = a.strip()
                    metadata['max'] = b.strip()
                elif name in ('regex',):
                    metadata['regex'] = val
                elif name in ('unique', 'exists'):
                    metadata[name] = val
                elif name == 'in':
                    # for test completeness
                    metadata['enum'] = [v.strip() for v in val.split(',') if v.strip()]
                else:
                    # generic store
                    metadata[name] = val
            else:
                metadata[part] = True
                if part == 'in':
                    metadata['enum'] = []
        # normalize enum from in:
        if 'in' in parts and any(p.startswith('in:') for p in parts):
            for p in parts:
                if p.startswith('in:'):
                    _, val = p.split(':', 1)
                    metadata['enum'] = [v.strip() for v in val.split(',') if v.strip()]
        # required shorthand
        return metadata

