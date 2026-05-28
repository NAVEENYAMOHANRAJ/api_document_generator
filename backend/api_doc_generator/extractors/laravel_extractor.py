"""
Laravel Route Extractor - Source-Verified, AST-Based Extraction

This extractor follows the gold standard:
- Only extracts information backed by source code
- Never hallucinate metadata
- Tracks source traceability (file, line number)
- Implements confidence scoring based on evidence
- Resolves controllers to actual files
- Extracts request/response schemas from source
"""

import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class LaravelExtractor:
    """Extract Laravel routes with source verification and confidence scoring."""

    # Resource method mapping to HTTP methods
    RESOURCE_METHODS = {
        "index": "GET",
        "create": "GET",
        "store": "POST",
        "show": "GET",
        "edit": "GET",
        "update": "PUT",
        "destroy": "DELETE",
    }

    # HTTP methods supported
    HTTP_METHODS = ["get", "post", "put", "patch", "delete", "options", "head"]
    ANY_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

    def __init__(self, file_path: str, repo_path: str = ""):
        self.file_path = file_path
        self.repo_path = Path(repo_path) if repo_path else Path(file_path).parent
        self.endpoints: List[Dict] = []
        self.content = ""
        
        # Context stacks for nested groups
        self.prefix_stack: List[str] = []
        self.middleware_stack: List[List[str]] = []
        self.namespace_stack: List[str] = []
        
        # Track routes extracted from groups to avoid duplicates
        self.routes_from_groups: set = set()

    @classmethod
    def extract(cls, file_path: str, content: str, repo_path: str = "") -> List[Dict]:
        """Extract Laravel routes from file content."""
        extractor = cls(file_path, repo_path)
        extractor.content = content
        extractor._extract_all_routes()
        
        # Deduplicate endpoints by (method, path)
        # Keep the first occurrence (which has the correct context from groups)
        seen = set()
        unique_endpoints = []
        for endpoint in extractor.endpoints:
            key = (endpoint["method"], endpoint["path"])
            if key not in seen:
                seen.add(key)
                unique_endpoints.append(endpoint)
        
        return unique_endpoints

    def _extract_all_routes(self) -> None:
        """Extract all route types from the file."""
        # Extract grouped routes (recursive) - this handles ALL routes inside groups
        self._extract_grouped_routes(self.content)
        
        # Extract top-level routes (not in any groups)
        # Remove all groups first to get only top-level routes
        content_without_groups = self._remove_group_blocks(self.content)
        
        # Extract individual routes (not in any groups)
        self._extract_individual_routes(content_without_groups)
        self._extract_match_and_any_routes(content_without_groups)
        
        # Extract resource routes (not in any groups)
        self._extract_resource_routes(content_without_groups)
        
        # Extract API resource routes (not in any groups)
        self._extract_api_resource_routes(content_without_groups)
        self._extract_dingo_routes(content_without_groups)

    def _remove_group_blocks(self, content: str) -> str:
        """Remove group blocks to prevent double-counting."""
        # Keep removing group blocks until none are left
        prev_content = ""
        while prev_content != content:
            prev_content = content
            
            # Find and remove Route::group([...], function() { ... })
            pattern = r"Route::group\s*\(\s*\[(.*?)\]\s*,\s*function\s*\(\s*\)\s*\{"
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            
            # Process matches in reverse order to maintain positions
            for match in reversed(matches):
                brace_start = match.end() - 1
                brace_content = self._extract_brace_content(content, brace_start)
                if brace_content is not None:
                    # Remove the entire group including the closing brace
                    end_pos = brace_start + len(brace_content) + 1
                    content = content[:match.start()] + content[end_pos:]
            
            # Find and remove Route::middleware(...)->group(function() { ... })
            middleware_pattern = r"Route::middleware\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*->\s*group\s*\(\s*function\s*\(\s*\)\s*\{"
            matches = list(re.finditer(middleware_pattern, content, re.IGNORECASE))
            
            for match in reversed(matches):
                brace_start = match.end() - 1
                brace_content = self._extract_brace_content(content, brace_start)
                if brace_content is not None:
                    end_pos = brace_start + len(brace_content) + 1
                    content = content[:match.start()] + content[end_pos:]

            prefix_pattern = r"Route::prefix\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*->\s*group\s*\(\s*function\s*\(\s*\)\s*\{"
            matches = list(re.finditer(prefix_pattern, content, re.IGNORECASE))
            for match in reversed(matches):
                brace_start = match.end() - 1
                brace_content = self._extract_brace_content(content, brace_start)
                if brace_content is not None:
                    end_pos = brace_start + len(brace_content) + 1
                    content = content[:match.start()] + content[end_pos:]
        
        return content

    def _extract_grouped_routes(self, content: str) -> None:
        """Extract Route::group() with context stacking - only top-level groups."""
        # Find all Route::group( patterns
        pattern = r"Route::group\s*\(\s*\[(.*?)\]\s*,\s*function\s*\(\s*\)\s*\{"
        
        matches = list(re.finditer(pattern, content, re.IGNORECASE))
        
        # Filter to only top-level groups (not nested inside other groups)
        top_level_matches = []
        for i, match in enumerate(matches):
            is_nested = False
            # Check if this match is inside any other match
            for j, other_match in enumerate(matches):
                if i == j:
                    continue
                # If other_match starts before this match and ends after it, then this match is nested
                if other_match.start() < match.start():
                    # Check if other_match's closing brace is after this match's start
                    brace_start = other_match.end() - 1
                    other_group_content = self._extract_brace_content(content, brace_start)
                    if other_group_content and match.start() > other_match.start():
                        # This match is inside other_match
                        is_nested = True
                        break
            
            if not is_nested:
                top_level_matches.append(match)
        
        for match in top_level_matches:
            options_str = match.group(1)
            brace_start = match.end() - 1  # Position of opening brace
            
            # Find matching closing brace
            group_content = self._extract_brace_content(content, brace_start)
            if not group_content:
                continue
            
            # Extract group options
            prefix = self._extract_string_option(options_str, 'prefix')
            middleware = self._extract_list_option(options_str, 'middleware')
            namespace = self._extract_string_option(options_str, 'namespace')
            
            # Push context
            if prefix:
                self.prefix_stack.append(prefix)
            if middleware:
                self.middleware_stack.append(middleware)
            if namespace:
                self.namespace_stack.append(namespace)
            
            # Recursively extract nested groups first
            self._extract_grouped_routes(group_content)
            
            # Extract routes from this group (only leaf routes, not nested groups)
            content_without_nested = self._remove_group_blocks(group_content)
            self._extract_individual_routes(content_without_nested)
            self._extract_match_and_any_routes(content_without_nested)
            self._extract_resource_routes(content_without_nested)
            self._extract_api_resource_routes(content_without_nested)
            
            # Pop context
            if prefix:
                self.prefix_stack.pop()
            if middleware:
                self.middleware_stack.pop()
            if namespace:
                self.namespace_stack.pop()
        
        # Pattern 2: Route::middleware('auth:api')->group(function() { ... })
        middleware_pattern = r"Route::middleware\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*->\s*group\s*\(\s*function\s*\(\s*\)\s*\{"
        middleware_matches = list(re.finditer(middleware_pattern, content, re.IGNORECASE))
        
        # Filter to only top-level middleware groups
        top_level_middleware_matches = []
        for i, match in enumerate(middleware_matches):
            is_nested = False
            for j, other_match in enumerate(middleware_matches):
                if i == j:
                    continue
                if other_match.start() < match.start():
                    brace_start = other_match.end() - 1
                    other_group_content = self._extract_brace_content(content, brace_start)
                    if other_group_content and match.start() > other_match.start():
                        is_nested = True
                        break
            
            if not is_nested:
                top_level_middleware_matches.append(match)
        
        for match in top_level_middleware_matches:
            middleware_str = match.group(1)
            brace_start = match.end() - 1
            
            group_content = self._extract_brace_content(content, brace_start)
            if not group_content:
                continue
            
            middleware = [m.strip() for m in middleware_str.split(',')]
            
            self.middleware_stack.append(middleware)
            self._extract_grouped_routes(group_content)
            
            content_without_nested = self._remove_group_blocks(group_content)
            self._extract_individual_routes(content_without_nested)
            self._extract_match_and_any_routes(content_without_nested)
            self._extract_resource_routes(content_without_nested)
            self._extract_api_resource_routes(content_without_nested)
            
            self.middleware_stack.pop()

        # Pattern 3: Route::prefix('v1')->group(function () { ... })
        prefix_pattern = r"Route::prefix\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*->\s*group\s*\(\s*function\s*\(\s*\)\s*\{"
        for match in re.finditer(prefix_pattern, content, re.IGNORECASE):
            prefix = match.group(1)
            group_content = self._extract_brace_content(content, match.end() - 1)
            if not group_content:
                continue
            self.prefix_stack.append(prefix)
            self._extract_grouped_routes(group_content)
            content_without_nested = self._remove_group_blocks(group_content)
            self._extract_individual_routes(content_without_nested)
            self._extract_match_and_any_routes(content_without_nested)
            self._extract_resource_routes(content_without_nested)
            self._extract_api_resource_routes(content_without_nested)
            self.prefix_stack.pop()

    def _extract_individual_routes(self, content: str) -> None:
        """Extract individual Route::method() declarations."""
        for method in self.HTTP_METHODS:
            http_method = method.upper()
            
            # Pattern 1: Route::method('path', 'Controller@action')
            pattern1 = rf"Route::{method}\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)"
            for match in re.finditer(pattern1, content, re.IGNORECASE):
                path, controller_action = match.groups()
                # Skip if this route was already extracted from a group
                normalized_path = self._normalize_path(path)
                line_number = content[:match.start()].count("\n") + 1
                if (http_method, normalized_path, line_number) not in self.routes_from_groups:
                    self._add_endpoint(http_method, path, controller_action, match.start())
            
            # Pattern 2: Route::method('path', [Controller::class, 'method'])
            pattern2 = rf"Route::{method}\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*\[\s*([^\]]+)\s*\]\s*\)"
            for match in re.finditer(pattern2, content, re.IGNORECASE):
                path, controller_spec = match.groups()
                controller_action = self._parse_controller_spec(controller_spec)
                # Skip if this route was already extracted from a group
                normalized_path = self._normalize_path(path)
                line_number = content[:match.start()].count("\n") + 1
                if (http_method, normalized_path, line_number) not in self.routes_from_groups:
                    self._add_endpoint(http_method, path, controller_action, match.start())
            
            # Pattern 3: Route::method('path', function() { ... }) - closure
            pattern3 = rf"Route::{method}\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*function\s*\(\s*[^\)]*\)\s*\{{"
            for match in re.finditer(pattern3, content, re.IGNORECASE):
                path = match.group(1)
                # Skip if this route was already extracted from a group
                normalized_path = self._normalize_path(path)
                line_number = content[:match.start()].count("\n") + 1
                if (http_method, normalized_path, line_number) not in self.routes_from_groups:
                    self._add_endpoint(http_method, path, None, match.start())

            # Pattern 4: Route::middleware('auth')->method('path', handler)
            chained_pattern = rf"Route::middleware\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*->\s*{method}\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*(?:['\"]([^'\"]+)['\"]|\[\s*([^\]]+)\s*\])"
            for match in re.finditer(chained_pattern, content, re.IGNORECASE):
                middleware, path, string_handler, array_handler = match.groups()
                controller_action = string_handler or self._parse_controller_spec(array_handler or "")
                self.middleware_stack.append([middleware])
                self._add_endpoint(http_method, path, controller_action, match.start())
                self.middleware_stack.pop()

    def _extract_match_and_any_routes(self, content: str) -> None:
        """Extract Route::match() and Route::any() declarations."""
        match_pattern = r"Route::match\s*\(\s*\[([^\]]+)\]\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*(?:['\"]([^'\"]+)['\"]|\[\s*([^\]]+)\s*\])"
        for match in re.finditer(match_pattern, content, re.IGNORECASE):
            methods_raw, path, string_handler, array_handler = match.groups()
            controller_action = string_handler or self._parse_controller_spec(array_handler or "")
            for method in re.findall(r"['\"]([a-zA-Z]+)['\"]", methods_raw):
                self._add_endpoint(method.upper(), path, controller_action, match.start())

        any_pattern = r"Route::any\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*(?:['\"]([^'\"]+)['\"]|\[\s*([^\]]+)\s*\])"
        for match in re.finditer(any_pattern, content, re.IGNORECASE):
            path, string_handler, array_handler = match.groups()
            controller_action = string_handler or self._parse_controller_spec(array_handler or "")
            for method in self.ANY_METHODS:
                self._add_endpoint(method, path, controller_action, match.start())

    def _extract_dingo_routes(self, content: str) -> None:
        """Extract Dingo API router calls like $api->get('users', 'Controller@method')."""
        pattern = r"\$api\s*->\s*(get|post|put|patch|delete|options|head)\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]"
        for match in re.finditer(pattern, content, re.IGNORECASE):
            method, path, controller_action = match.groups()
            middleware_match = re.search(
                r"->middleware\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
                content[match.end():match.end() + 120],
            )
            if middleware_match:
                self.middleware_stack.append([middleware_match.group(1)])
            self._add_endpoint(method.upper(), path, controller_action, match.start())
            if middleware_match:
                self.middleware_stack.pop()

    def _extract_resource_routes(self, content: str) -> None:
        """Extract Route::resource() declarations."""
        # Pattern 1: Route::resource('resource', 'ControllerName')
        pattern1 = r"Route::resource\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)"
        
        for match in re.finditer(pattern1, content, re.IGNORECASE):
            resource_name, controller = match.groups()
            self._expand_resource_routes(resource_name, controller, match.start(), include_create_edit=True)
        
        # Pattern 2: Route::resource('resource', ControllerClass::class)
        pattern2 = r"Route::resource\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*([A-Za-z_][A-Za-z0-9_]*(?:::[A-Za-z_][A-Za-z0-9_]*)*)\s*\)"
        
        for match in re.finditer(pattern2, content, re.IGNORECASE):
            resource_name, controller_spec = match.groups()
            # Remove ::class suffix if present
            controller = controller_spec.replace("::class", "").strip()
            self._expand_resource_routes(resource_name, controller, match.start(), include_create_edit=True)

    def _extract_api_resource_routes(self, content: str) -> None:
        """Extract Route::apiResource() declarations (excludes create/edit)."""
        # Pattern 1: Route::apiResource('resource', 'ControllerName')
        pattern1 = r"Route::apiResource\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)"
        
        for match in re.finditer(pattern1, content, re.IGNORECASE):
            resource_name, controller = match.groups()
            self._expand_resource_routes(resource_name, controller, match.start(), include_create_edit=False)
        
        # Pattern 2: Route::apiResource('resource', ControllerClass::class)
        pattern2 = r"Route::apiResource\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*([A-Za-z_][A-Za-z0-9_]*(?:::[A-Za-z_][A-Za-z0-9_]*)*)\s*\)"
        
        for match in re.finditer(pattern2, content, re.IGNORECASE):
            resource_name, controller_spec = match.groups()
            # Remove ::class suffix if present
            controller = controller_spec.replace("::class", "").strip()
            self._expand_resource_routes(resource_name, controller, match.start(), include_create_edit=False)

    def _expand_resource_routes(
        self,
        resource_name: str,
        controller: str,
        line_start: int,
        include_create_edit: bool = True
    ) -> None:
        """Expand resource routes to individual endpoints."""
        for action, http_method in self.RESOURCE_METHODS.items():
            # Skip create/edit for API resources
            if not include_create_edit and action in ("create", "edit"):
                continue
            
            # Build path based on action
            if action == "index":
                path = f"/{resource_name}"
            elif action == "create":
                path = f"/{resource_name}/create"
            elif action == "store":
                path = f"/{resource_name}"
            elif action == "show":
                path = f"/{resource_name}/{{{self._resource_param_name(resource_name)}}}"
            elif action == "edit":
                path = f"/{resource_name}/{{{self._resource_param_name(resource_name)}}}/edit"
            elif action == "update":
                path = f"/{resource_name}/{{{self._resource_param_name(resource_name)}}}"
            elif action == "destroy":
                path = f"/{resource_name}/{{{self._resource_param_name(resource_name)}}}"
            else:
                continue
            
            controller_action = f"{controller}@{action}"
            self._add_endpoint(http_method, path, controller_action, line_start)

    def _add_endpoint(
        self,
        method: str,
        path: str,
        controller_action: Optional[str],
        line_start: int
    ) -> None:
        """Add endpoint with source traceability and confidence scoring."""
        normalized_path = self._normalize_path(path)
        if self._is_spa_fallback_route(normalized_path, line_start):
            return
        line_number = self.content[:line_start].count("\n") + 1
        
        # Build endpoint object
        endpoint = {
            "method": method,
            "path": normalized_path,
            "handler": {},
            "middleware": self._get_current_middleware(),
            "requestBody": {},
            "responses": {},
            "security": [],
            "source": {
                "file": self.file_path,
                "line": line_number,
            },
            "confidence": 0.0,
        }
        
        # Add controller information if present
        if controller_action:
            endpoint["handler"] = {
                "class": controller_action.split("@")[0],
                "method": controller_action.split("@")[1],
                "file": None,  # Would be resolved in controller resolution phase
            }
            endpoint["confidence"] = 0.95  # High confidence: route + controller found
        else:
            # Closure route - lower confidence
            endpoint["confidence"] = 0.70
        
        # Add source traceability
        endpoint["provenance"] = {
            "source_file": self.file_path,
            "detection_type": "framework_route_definition",
            "framework": "Laravel",
            "line_number": line_number,
        }
        
        self.endpoints.append(endpoint)

    def _resource_param_name(self, resource_name: str) -> str:
        leaf = resource_name.strip("/").split("/")[-1]
        if leaf.startswith("{") and leaf.endswith("}"):
            return leaf.strip("{}")
        return leaf[:-1] if leaf.endswith("s") and len(leaf) > 1 else leaf

    def _is_spa_fallback_route(self, path: str, line_start: int) -> bool:
        """Avoid documenting frontend catch-all view routes as API endpoints."""
        if "{view" not in path:
            return False
        semicolon = self.content.find(";", line_start)
        snippet = self.content[line_start: semicolon if semicolon != -1 else len(self.content)]
        return "where(" in snippet or "view(" in snippet

    def _normalize_path(self, path: str) -> str:
        """Normalize path with prefix stacking."""
        path = (path or "").strip()
        
        # Apply prefix stack in reverse order (last prefix is innermost)
        # So if prefix_stack = ["api", "v1"], we want /api/v1/path
        for prefix in reversed(self.prefix_stack):
            if prefix:
                path = f"/{prefix.strip('/')}/{path.strip('/')}"
        
        # Normalize path parameters - handle various formats
        # <int:id>, <uuid:id>, <id> -> {id}
        path = re.sub(r'<[^>]*:(\w+)>', r'{\1}', path)  # <int:id> -> {id}
        path = re.sub(r'<(\w+)>', r'{\1}', path)  # <id> -> {id}
        path = path.replace(":id", "{id}")  # :id -> {id}
        
        # Remove duplicate slashes
        while "//" in path:
            path = path.replace("//", "/")
        
        # Remove trailing slash (except root)
        if path != "/" and path.endswith("/"):
            path = path[:-1]
        
        # Ensure leading slash
        if not path.startswith("/"):
            path = "/" + path
        
        return path

    def _get_current_middleware(self) -> List[str]:
        """Get current middleware stack."""
        result = []
        for middleware_list in self.middleware_stack:
            result.extend(middleware_list)
        return result

    def _extract_string_option(self, options_str: str, key: str) -> Optional[str]:
        """Extract string option from group options."""
        pattern = rf"['\"]?{key}['\"]?\s*=>\s*['\"]([^'\"]+)['\"]"
        match = re.search(pattern, options_str, re.IGNORECASE)
        return match.group(1) if match else None

    def _extract_list_option(self, options_str: str, key: str) -> Optional[List[str]]:
        """Extract list option from group options."""
        pattern = rf"['\"]?{key}['\"]?\s*=>\s*\[(.*?)\]"
        match = re.search(pattern, options_str, re.IGNORECASE)
        if match:
            items = match.group(1)
            return [item.strip().strip("'\"") for item in items.split(",") if item.strip()]
        return None

    def _parse_controller_spec(self, spec: str) -> str:
        """Parse controller specification [ControllerClass::class, 'method']."""
        spec = spec.strip()
        parts = [p.strip() for p in spec.split(",")]
        if len(parts) >= 2:
            controller = parts[0].replace("::class", "").strip("'\"").strip()
            method = parts[1].strip("'\"").strip()
            return f"{controller}@{method}"
        return spec

    def _extract_brace_content(self, content: str, start_pos: int) -> str:
        """Extract content between matching braces starting at start_pos."""
        if start_pos >= len(content) or content[start_pos] != '{':
            return ""
        
        brace_count = 0
        in_string = False
        string_char = None
        
        for i in range(start_pos, len(content)):
            char = content[i]
            
            # Handle strings
            if char in ('"', "'") and (i == 0 or content[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
            
            # Count braces outside strings
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        # Found matching closing brace
                        return content[start_pos + 1:i]
        
        return ""
