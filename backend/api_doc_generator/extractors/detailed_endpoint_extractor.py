"""
Detailed Endpoint Extractor - Dynamically extract comprehensive endpoint metadata.

This extractor goes beyond basic route detection to extract:
- Request body structures from FormRequest classes
- Response structures from Resource classes
- Validation rules and constraints
- Authentication requirements
- Status codes and error responses
- Parameter documentation
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path


class DetailedEndpointExtractor:
    """Extract comprehensive endpoint metadata from source code."""

    def __init__(self, repo_path: str = ""):
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.file_cache: Dict[str, str] = {}

    def extract_endpoint_details(
        self,
        endpoint: Dict[str, Any],
        repo_files: List[str]
    ) -> Dict[str, Any]:
        """
        Extract detailed metadata for an endpoint.
        
        Args:
            endpoint: Basic endpoint from route extractor
            repo_files: List of all files in repository
            
        Returns:
            Enhanced endpoint with detailed metadata
        """
        enhanced = endpoint.copy()

        # If middleware was detected at route-level, translate it into a minimal security hint.
        # (Source-grounded: we only report what appears in code.)
        if enhanced.get("middleware") and not enhanced.get("security"):
            mw = [str(m) for m in (enhanced.get("middleware") or [])]
            auth_like = [m for m in mw if re.search(r"\bauth\b|sanctum|jwt|passport|token", m, re.IGNORECASE)]
            if auth_like:
                enhanced["security"] = [
                    {
                        "middleware": auth_like,
                        "detection_type": "route_middleware",
                        "source_file": (enhanced.get("source") or {}).get("file") or enhanced.get("source_file"),
                        "line_number": (enhanced.get("source") or {}).get("line"),
                    }
                ]
        
        # Extract handler details if available
        if endpoint.get("handler") and endpoint["handler"].get("class"):
            handler_file = self._find_controller_file(
                endpoint["handler"]["class"],
                repo_files
            )
            if handler_file:
                enhanced["handler"]["file"] = handler_file
                
                # Extract request body schema
                request_schema = self._extract_request_schema(
                    handler_file,
                    endpoint["handler"].get("method"),
                    endpoint.get("method")
                )
                if request_schema:
                    enhanced["requestBody"] = request_schema
                
                # Extract response schema
                response_schema = self._extract_response_schema(
                    handler_file,
                    endpoint["handler"].get("method")
                )
                if response_schema:
                    enhanced["responses"] = response_schema
                
                # Extract status codes
                status_codes = self._extract_status_codes(
                    handler_file,
                    endpoint["handler"].get("method")
                )
                if status_codes:
                    enhanced["statusCodes"] = status_codes
                
                # Extract authentication
                auth = self._extract_authentication(
                    handler_file,
                    endpoint["handler"].get("method")
                )
                if auth:
                    enhanced["security"] = auth
                else:
                    # Fallback: controller-level middleware declarations like $this->middleware('auth')
                    controller_auth = self._extract_controller_middleware_auth(handler_file)
                    if controller_auth:
                        enhanced["security"] = controller_auth
                
                # Extract query parameters
                query_params = self._extract_query_parameters(
                    handler_file,
                    endpoint["handler"].get("method")
                )
                if query_params:
                    enhanced["queryParameters"] = query_params
                
                # Extract request headers
                headers = self._extract_request_headers(
                    handler_file,
                    endpoint["handler"].get("method")
                )
                if headers:
                    enhanced["headers"] = headers
                
                # Extract tags/categories
                tags = self._extract_tags(
                    handler_file,
                    endpoint["handler"].get("method")
                )
                if tags:
                    enhanced["tags"] = tags
                
                # Extract rate limiting info
                rate_limit = self._extract_rate_limit(
                    handler_file,
                    endpoint["handler"].get("method")
                )
                if rate_limit:
                    enhanced["rateLimit"] = rate_limit
        
        # Extract path parameters
        path_params = self._extract_path_parameters(endpoint.get("path", ""))
        if path_params:
            enhanced["pathParameters"] = path_params
        
        # Extract query parameters from path if not already extracted
        if "queryParameters" not in enhanced:
            query_from_path = self._extract_query_params_from_path(endpoint.get("path", ""))
            if query_from_path:
                enhanced["queryParameters"] = query_from_path
        
        return enhanced

    def _extract_controller_middleware_auth(self, controller_file: str) -> Optional[List[Dict[str, Any]]]:
        content = self._read_file(controller_file)
        if not content:
            return None
        # $this->middleware('auth'); OR $this->middleware(['auth', 'verified']);
        single_matches = list(re.finditer(r"\$this->middleware\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", content, re.IGNORECASE))
        arr_matches = list(re.finditer(r"\$this->middleware\s*\(\s*\[(.*?)\]\s*\)", content, re.IGNORECASE | re.DOTALL))
        values: List[str] = []
        line_number: Optional[int] = None
        if single_matches:
            line_number = content[: single_matches[0].start()].count("\n") + 1
        for m in single_matches:
            v = (m.group(1) or "").strip()
            if v:
                values.append(v)
        if arr_matches and line_number is None:
            line_number = content[: arr_matches[0].start()].count("\n") + 1
        for m in arr_matches:
            chunk = m.group(1) or ""
            values.extend([x.strip().strip("'\"") for x in chunk.split(",") if x.strip()])
        auth_like = [m for m in values if re.search(r"\bauth\b|sanctum|jwt|passport|token", m, re.IGNORECASE)]
        if not auth_like:
            return None
        return [
            {
                "controller_middleware": auth_like,
                "source": "controller",
                "detection_type": "controller_middleware",
                "source_file": controller_file,
                "line_number": line_number,
            }
        ]

    def _find_controller_file(
        self,
        controller_class: str,
        repo_files: List[str]
    ) -> Optional[str]:
        """Find controller file by class name."""
        # Convert class name to file path
        # e.g., "App\Http\Controllers\UserController" -> "app/Http/Controllers/UserController.php"
        parts = controller_class.replace("\\", "/").split("/")
        class_name = parts[-1]
        
        # Search for file
        for file_path in repo_files:
            if file_path.endswith(f"{class_name}.php"):
                return file_path
        
        return None

    def _extract_request_schema(
        self,
        controller_file: str,
        method_name: Optional[str],
        http_method: str
    ) -> Optional[Dict[str, Any]]:
        """Extract request body schema from controller method."""
        if not method_name:
            return None
        
        content = self._read_file(controller_file)
        if not content:
            return None
        
        # Find method definition
        method_pattern = rf"function\s+{method_name}\s*\(\s*([^)]*)\s*\)"
        method_match = re.search(method_pattern, content)
        if not method_match:
            return None
        
        method_params = method_match.group(1)
        
        # Extract FormRequest type hint
        form_request = self._extract_form_request_class(method_params)
        if form_request:
            form_request_file = self._find_form_request_file(form_request)
            if form_request_file:
                return self._extract_form_request_schema(form_request_file)
        
        # Extract inline validation rules
        method_start = method_match.start()
        method_body_start = content.find("{", method_start)
        method_body_end = self._find_matching_brace(content, method_body_start)
        method_body = content[method_body_start:method_body_end]
        
        # Look for $request->validate() or $this->validate()
        validation_schema = self._extract_validation_rules(method_body)
        if validation_schema:
            return {
                "type": "object",
                "properties": validation_schema,
                "required": list(validation_schema.keys()),
                "source": "validation_rules",
                "confidence": 0.85,
                "detection_type": "validation_rules",
                "source_file": controller_file,
            }
        
        # Only POST/PUT/PATCH typically have request bodies
        if http_method not in ["POST", "PUT", "PATCH"]:
            return None
        
        return None

    def _extract_form_request_class(self, method_params: str) -> Optional[str]:
        """Extract FormRequest class name from method parameters."""
        # Pattern: StoreUserRequest $request
        pattern = r"(\w+Request)\s+\$\w+"
        match = re.search(pattern, method_params)
        if match:
            return match.group(1)
        return None

    def _find_form_request_file(self, class_name: str) -> Optional[str]:
        """Find FormRequest file."""
        # Typically in app/Http/Requests/
        possible_paths = [
            f"app/Http/Requests/{class_name}.php",
            f"app/Requests/{class_name}.php",
        ]
        
        for path in possible_paths:
            full_path = self.repo_path / path
            if full_path.exists():
                return str(full_path)
        
        return None

    def _extract_form_request_schema(self, form_request_file: str) -> Optional[Dict[str, Any]]:
        """Extract schema from FormRequest rules() method."""
        content = self._read_file(form_request_file)
        if not content:
            return None
        
        # Find rules() method
        rules_pattern = r"public\s+function\s+rules\s*\(\s*\)\s*\{([\s\S]*?)\n\s*\}"
        rules_match = re.search(rules_pattern, content)
        if not rules_match:
            return None
        
        rules_body = rules_match.group(1)
        
        # Extract return statement
        return_pattern = r"return\s*\[([\s\S]*?)\]"
        return_match = re.search(return_pattern, rules_body)
        if not return_match:
            return None
        
        rules_str = return_match.group(1)
        properties = {}
        
        # Parse each rule line
        for line in rules_str.split(","):
            line = line.strip()
            if not line:
                continue
            
            # Pattern: 'field' => 'rules'
            field_match = re.match(r"['\"]([^'\"]+)['\"]\s*=>\s*['\"]([^'\"]+)['\"]", line)
            if field_match:
                field_name = field_match.group(1)
                rules = field_match.group(2)
                
                properties[field_name] = self._parse_validation_rules(rules)
        
        return {
            "type": "object",
            "properties": properties,
            "required": [k for k, v in properties.items() if v.get("required")],
            "source": "form_request",
            "confidence": 0.95
        }

    def _extract_validation_rules(self, method_body: str) -> Optional[Dict[str, Any]]:
        """Extract validation rules from $request->validate()."""
        # Pattern: $request->validate([...])
        pattern = r"\$(?:request|this)->validate\s*\(\s*\[([\s\S]*?)\]\s*\)"
        match = re.search(pattern, method_body)
        if not match:
            return None
        
        rules_str = match.group(1)
        properties = {}
        
        for line in rules_str.split(","):
            line = line.strip()
            if not line:
                continue
            
            field_match = re.match(r"['\"]([^'\"]+)['\"]\s*=>\s*['\"]([^'\"]+)['\"]", line)
            if field_match:
                field_name = field_match.group(1)
                rules = field_match.group(2)
                properties[field_name] = self._parse_validation_rules(rules)
        
        return properties if properties else None

    def _parse_validation_rules(self, rules: str) -> Dict[str, Any]:
        """Parse Laravel validation rules into schema."""
        schema = {
            "type": "string",
            "required": "required" in rules,
            "rules": rules
        }
        
        rules_list = [r.strip() for r in rules.split("|")]
        
        for rule in rules_list:
            if rule == "required":
                schema["required"] = True
            elif rule == "nullable":
                schema["nullable"] = True
            elif rule == "email":
                schema["type"] = "string"
                schema["format"] = "email"
            elif rule == "integer":
                schema["type"] = "integer"
            elif rule == "numeric":
                schema["type"] = "number"
            elif rule == "boolean":
                schema["type"] = "boolean"
            elif rule == "array":
                schema["type"] = "array"
            elif rule == "json":
                schema["type"] = "object"
            elif rule.startswith("min:"):
                schema["minimum"] = int(rule.split(":")[1])
            elif rule.startswith("max:"):
                schema["maximum"] = int(rule.split(":")[1])
            elif rule.startswith("size:"):
                schema["minLength"] = int(rule.split(":")[1])
            elif rule.startswith("in:"):
                enum_values = rule.split(":")[1].split(",")
                schema["enum"] = enum_values
            elif rule.startswith("regex:"):
                schema["pattern"] = rule.split(":")[1]
        
        return schema

    def _extract_response_schema(
        self,
        controller_file: str,
        method_name: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Extract response schema from controller method."""
        if not method_name:
            return None
        
        content = self._read_file(controller_file)
        if not content:
            return None
        
        # Find method definition
        method_pattern = rf"function\s+{method_name}\s*\(\s*([^)]*)\s*\)"
        method_match = re.search(method_pattern, content)
        if not method_match:
            return None
        
        method_start = method_match.start()
        method_body_start = content.find("{", method_start)
        method_body_end = self._find_matching_brace(content, method_body_start)
        method_body = content[method_body_start:method_body_end]
        
        responses = {}
        
        # Pattern: return UserResource::make(...)
        resource_pattern = r"return\s+(\w+Resource)::make\s*\("
        for match in re.finditer(resource_pattern, method_body):
            resource_class = match.group(1)
            responses[200] = {
                "type": "object",
                "resource": resource_class,
                "source": "resource_class",
                "confidence": 0.90
            }
        
        # Pattern: return UserResource::collection(...)
        collection_pattern = r"return\s+(\w+Resource)::collection\s*\("
        for match in re.finditer(collection_pattern, method_body):
            resource_class = match.group(1)
            responses[200] = {
                "type": "array",
                "items": {
                    "type": "object",
                    "resource": resource_class
                },
                "source": "resource_collection",
                "confidence": 0.90
            }
        
        # Pattern: return response()->json(...)
        json_pattern = r"return\s+response\(\)->json\s*\(([\s\S]*?)\)"
        for match in re.finditer(json_pattern, method_body):
            responses[200] = {
                "type": "object",
                "source": "response_json",
                "confidence": 0.75
            }
        
        # Pattern: return Model::all()
        collection_model_pattern = r"return\s+(\w+)::all\s*\(\)"
        for match in re.finditer(collection_model_pattern, method_body):
            model_class = match.group(1)
            responses[200] = {
                "type": "array",
                "items": {
                    "type": "object",
                    "model": model_class
                },
                "source": "model_collection",
                "confidence": 0.80
            }
        
        # Pattern: return Model::find(...)
        find_pattern = r"return\s+(\w+)::find\s*\("
        for match in re.finditer(find_pattern, method_body):
            model_class = match.group(1)
            responses[200] = {
                "type": "object",
                "model": model_class,
                "source": "model_find",
                "confidence": 0.80
            }
        
        return responses if responses else None

    def _extract_status_codes(
        self,
        controller_file: str,
        method_name: Optional[str]
    ) -> Optional[List[int]]:
        """Extract HTTP status codes from controller method."""
        if not method_name:
            return None
        
        content = self._read_file(controller_file)
        if not content:
            return None
        
        # Find method definition
        method_pattern = rf"function\s+{method_name}\s*\(\s*([^)]*)\s*\)"
        method_match = re.search(method_pattern, content)
        if not method_match:
            return None
        
        method_start = method_match.start()
        method_body_start = content.find("{", method_start)
        method_body_end = self._find_matching_brace(content, method_body_start)
        method_body = content[method_body_start:method_body_end]
        
        status_codes = set()
        
        # Pattern: ->status(201)
        status_pattern = r"->status\s*\(\s*(\d+)\s*\)"
        for match in re.finditer(status_pattern, method_body):
            status_codes.add(int(match.group(1)))
        
        # Pattern: response()->json(..., 201)
        response_pattern = r"response\(\)->json\s*\([^,]*,\s*(\d+)\s*\)"
        for match in re.finditer(response_pattern, method_body):
            status_codes.add(int(match.group(1)))
        
        # Pattern: abort(404)
        abort_pattern = r"abort\s*\(\s*(\d+)\s*\)"
        for match in re.finditer(abort_pattern, method_body):
            status_codes.add(int(match.group(1)))
        
        # Default status codes based on method
        if not status_codes:
            status_codes.add(200)
        
        return sorted(list(status_codes))

    def _extract_authentication(
        self,
        controller_file: str,
        method_name: Optional[str]
    ) -> Optional[List[str]]:
        """Extract authentication requirements from controller."""
        if not method_name:
            return None
        
        content = self._read_file(controller_file)
        if not content:
            return None
        
        auth_methods = []
        
        # Look for middleware in constructor
        constructor_pattern = r"public\s+function\s+__construct\s*\(\s*\)\s*\{([\s\S]*?)\n\s*\}"
        constructor_match = re.search(constructor_pattern, content)
        if constructor_match:
            constructor_body = constructor_match.group(1)
            
            # Pattern: $this->middleware('auth')
            middleware_pattern = r"\$this->middleware\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
            for match in re.finditer(middleware_pattern, constructor_body):
                auth_methods.append(match.group(1))
        
        # Look for method-level middleware
        method_pattern = rf"function\s+{method_name}\s*\(\s*([^)]*)\s*\)"
        method_match = re.search(method_pattern, content)
        if method_match:
            method_start = method_match.start()
            # Look for #[Middleware(...)] or @middleware above method
            before_method = content[max(0, method_start - 200):method_start]
            
            middleware_attr = r"#\[Middleware\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\]"
            for match in re.finditer(middleware_attr, before_method):
                auth_methods.append(match.group(1))
        
        return auth_methods if auth_methods else None

    def _extract_path_parameters(self, path: str) -> Optional[List[Dict[str, Any]]]:
        """Extract path parameters from route path."""
        # Pattern: {id}, {uuid}, etc.
        param_pattern = r"\{(\w+)\}"
        matches = re.findall(param_pattern, path)
        
        if not matches:
            return None
        
        parameters = []
        for param_name in matches:
            parameters.append({
                "name": param_name,
                "in": "path",
                "required": True,
                "type": "string",
                "description": f"The {param_name} parameter"
            })
        
        return parameters

    def _find_matching_brace(self, content: str, start_pos: int) -> int:
        """Find matching closing brace."""
        if start_pos >= len(content) or content[start_pos] != '{':
            return start_pos
        
        brace_count = 0
        in_string = False
        string_char = None
        
        for i in range(start_pos, len(content)):
            char = content[i]
            
            if char in ('"', "'") and (i == 0 or content[i-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
            
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        return i
        
        return len(content)

    def _read_file(self, file_path: str) -> Optional[str]:
        """Read file with caching."""
        if file_path in self.file_cache:
            return self.file_cache[file_path]
        
        try:
            p = Path(file_path)
            if not p.is_absolute():
                p = (self.repo_path / p).resolve()
            content = p.read_text(encoding='utf-8', errors='ignore')
            self.file_cache[file_path] = content
            return content
        except Exception:
            return None

    def _extract_query_parameters(
        self,
        controller_file: str,
        method_name: Optional[str]
    ) -> Optional[List[Dict[str, Any]]]:
        """Extract query parameters from controller method."""
        if not method_name:
            return None
        
        content = self._read_file(controller_file)
        if not content:
            return None
        
        # Find method definition
        method_pattern = rf"function\s+{method_name}\s*\(\s*([^)]*)\s*\)"
        method_match = re.search(method_pattern, content)
        if not method_match:
            return None
        
        method_start = method_match.start()
        method_body_start = content.find("{", method_start)
        method_body_end = self._find_matching_brace(content, method_body_start)
        method_body = content[method_body_start:method_body_end]
        
        query_params = []
        
        # Pattern: $request->query('param_name')
        query_pattern = r"\$request->query\s*\(\s*['\"]([^'\"]+)['\"]\s*(?:,\s*['\"]([^'\"]+)['\"])?\s*\)"
        for match in re.finditer(query_pattern, method_body):
            param_name = match.group(1)
            default_value = match.group(2)
            
            query_params.append({
                "name": param_name,
                "in": "query",
                "required": False,
                "type": "string",
                "description": f"Query parameter: {param_name}",
                "default": default_value
            })
        
        # Pattern: $request->input('param_name')
        input_pattern = r"\$request->input\s*\(\s*['\"]([^'\"]+)['\"]\s*(?:,\s*['\"]([^'\"]+)['\"])?\s*\)"
        for match in re.finditer(input_pattern, method_body):
            param_name = match.group(1)
            default_value = match.group(2)
            
            # Check if already added
            if not any(p["name"] == param_name for p in query_params):
                query_params.append({
                    "name": param_name,
                    "in": "query",
                    "required": False,
                    "type": "string",
                    "description": f"Query parameter: {param_name}",
                    "default": default_value
                })
        
        return query_params if query_params else None

    def _extract_query_params_from_path(self, path: str) -> Optional[List[Dict[str, Any]]]:
        """Extract query parameters from path if specified."""
        # Pattern: ?param1=type&param2=type
        if "?" not in path:
            return None
        
        query_string = path.split("?")[1]
        params = []
        
        for param in query_string.split("&"):
            if "=" in param:
                name, type_hint = param.split("=", 1)
                params.append({
                    "name": name.strip(),
                    "in": "query",
                    "required": False,
                    "type": type_hint.strip() or "string",
                    "description": f"Query parameter: {name.strip()}"
                })
        
        return params if params else None

    def _extract_request_headers(
        self,
        controller_file: str,
        method_name: Optional[str]
    ) -> Optional[List[Dict[str, Any]]]:
        """Extract request headers from controller method."""
        if not method_name:
            return None
        
        content = self._read_file(controller_file)
        if not content:
            return None
        
        # Find method definition
        method_pattern = rf"function\s+{method_name}\s*\(\s*([^)]*)\s*\)"
        method_match = re.search(method_pattern, content)
        if not method_match:
            return None
        
        method_start = method_match.start()
        method_body_start = content.find("{", method_start)
        method_body_end = self._find_matching_brace(content, method_body_start)
        method_body = content[method_body_start:method_body_end]
        
        headers = []
        
        # Pattern: $request->header('X-Custom-Header')
        header_pattern = r"\$request->header\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
        for match in re.finditer(header_pattern, method_body):
            header_name = match.group(1)
            headers.append({
                "name": header_name,
                "in": "header",
                "required": False,
                "type": "string",
                "description": f"Request header: {header_name}"
            })
        
        # Common headers to check for
        common_headers = ["Authorization", "Accept", "Content-Type", "X-Requested-With"]
        for header in common_headers:
            if header.lower() in content.lower() and not any(h["name"] == header for h in headers):
                headers.append({
                    "name": header,
                    "in": "header",
                    "required": header == "Authorization",
                    "type": "string",
                    "description": f"Request header: {header}"
                })
        
        return headers if headers else None

    def _extract_tags(
        self,
        controller_file: str,
        method_name: Optional[str]
    ) -> Optional[List[str]]:
        """Extract tags/categories from controller method."""
        if not method_name:
            return None
        
        content = self._read_file(controller_file)
        if not content:
            return None
        
        tags = []
        
        # Extract from class name (e.g., UserController -> Users)
        class_pattern = r"class\s+(\w+Controller)"
        class_match = re.search(class_pattern, content)
        if class_match:
            class_name = class_match.group(1)
            # Remove "Controller" suffix and pluralize
            resource = class_name.replace("Controller", "")
            tags.append(resource)
        
        # Extract from method name (e.g., storeUser -> store, user)
        method_words = re.findall(r"[A-Z][a-z]+", method_name)
        for word in method_words:
            if word.lower() not in ["controller"]:
                tags.append(word.lower())
        
        # Extract from docblock tags
        docblock_pattern = rf"/\*\*[\s\S]*?@tag\s+(\w+)[\s\S]*?\*/"
        for match in re.finditer(docblock_pattern, content):
            tag = match.group(1)
            if tag not in tags:
                tags.append(tag)
        
        return tags if tags else None

    def _extract_rate_limit(
        self,
        controller_file: str,
        method_name: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Extract rate limiting information from controller method."""
        if not method_name:
            return None
        
        content = self._read_file(controller_file)
        if not content:
            return None
        
        # Find method definition
        method_pattern = rf"function\s+{method_name}\s*\(\s*([^)]*)\s*\)"
        method_match = re.search(method_pattern, content)
        if not method_match:
            return None
        
        method_start = method_match.start()
        # Look for throttle middleware before method
        before_method = content[max(0, method_start - 500):method_start]
        
        # Pattern: @throttle:60,1 or #[Throttle('60,1')]
        throttle_pattern = r"@throttle:(\d+),(\d+)|#\[Throttle\s*\(\s*['\"](\d+),(\d+)['\"]\s*\)\]"
        throttle_match = re.search(throttle_pattern, before_method)
        
        if throttle_match:
            if throttle_match.group(1):
                requests = int(throttle_match.group(1))
                minutes = int(throttle_match.group(2))
            else:
                requests = int(throttle_match.group(3))
                minutes = int(throttle_match.group(4))
            
            return {
                "requests": requests,
                "period": f"{minutes} minute(s)",
                "description": f"Rate limit: {requests} requests per {minutes} minute(s)"
            }
        
        return None
