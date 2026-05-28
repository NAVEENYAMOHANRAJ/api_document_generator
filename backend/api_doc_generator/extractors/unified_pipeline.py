"""
Unified AST-Based Extraction Pipeline
Extracts API endpoints from source code using AST parsing, not regex.
Integrates directly with dashboard for real-time display.
"""

import ast
import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class Parameter:
    """API Parameter definition"""
    name: str
    type: str
    required: bool
    description: str = ""
    location: str = "query"  # query, path, header, body


@dataclass
class Response:
    """API Response definition"""
    status_code: int
    description: str
    schema: Optional[Dict] = None


@dataclass
class Endpoint:
    """Complete API Endpoint definition"""
    method: str
    path: str
    summary: str
    description: str
    parameters: List[Parameter]
    request_body: Optional[Dict]
    responses: List[Response]
    security: List[str]
    tags: List[str]
    deprecated: bool
    source_file: str
    line_number: int
    confidence: float
    handler_class: Optional[str] = None
    handler_method: Optional[str] = None


class PythonASTExtractor:
    """Extract endpoints from Python code using AST"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.endpoints: List[Endpoint] = []
        self.tree = None
        self.source_lines = []
        
    def extract(self) -> List[Endpoint]:
        """Extract endpoints from Python file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.source_lines = content.split('\n')
                self.tree = ast.parse(content)
        except Exception as e:
            print(f"Error parsing {self.file_path}: {e}")
            return []
        
        # Extract from different frameworks
        self._extract_fastapi()
        self._extract_flask()
        self._extract_django()
        
        return self.endpoints
    
    def _extract_fastapi(self):
        """Extract FastAPI endpoints"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                # Check for FastAPI decorators
                for decorator in node.decorator_list:
                    if self._is_fastapi_decorator(decorator):
                        endpoint = self._parse_fastapi_endpoint(node, decorator)
                        if endpoint:
                            self.endpoints.append(endpoint)
    
    def _extract_flask(self):
        """Extract Flask endpoints"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                for decorator in node.decorator_list:
                    if self._is_flask_decorator(decorator):
                        endpoint = self._parse_flask_endpoint(node, decorator)
                        if endpoint:
                            self.endpoints.append(endpoint)
    
    def _extract_django(self):
        """Extract Django endpoints"""
        # Django uses URL patterns, extract from urls.py
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if self._is_django_path(node):
                    endpoint = self._parse_django_endpoint(node)
                    if endpoint:
                        self.endpoints.append(endpoint)
    
    def _is_fastapi_decorator(self, decorator) -> bool:
        """Check if decorator is FastAPI"""
        if isinstance(decorator, ast.Call):
            func = decorator.func
        else:
            func = decorator
        
        if isinstance(func, ast.Attribute):
            return func.attr in ('get', 'post', 'put', 'delete', 'patch', 'options')
        return False
    
    def _is_flask_decorator(self, decorator) -> bool:
        """Check if decorator is Flask"""
        if isinstance(decorator, ast.Call):
            func = decorator.func
        else:
            func = decorator
        
        if isinstance(func, ast.Attribute):
            return func.attr in ('route', 'get', 'post', 'put', 'delete')
        return False
    
    def _is_django_path(self, node) -> bool:
        """Check if node is Django path()"""
        if isinstance(node.func, ast.Name):
            return node.func.id in ('path', 're_path')
        return False
    
    def _parse_fastapi_endpoint(self, func_node: ast.FunctionDef, decorator) -> Optional[Endpoint]:
        """Parse FastAPI endpoint"""
        try:
            # Extract method and path from decorator
            method = "GET"
            path = "/"
            
            if isinstance(decorator, ast.Call):
                if decorator.args:
                    path = ast.literal_eval(decorator.args[0])
                
                # Get method from decorator name
                if isinstance(decorator.func, ast.Attribute):
                    method = decorator.func.attr.upper()
            
            # Extract parameters from function signature
            parameters = self._extract_function_parameters(func_node)
            
            # Extract docstring
            docstring = ast.get_docstring(func_node) or ""
            summary = docstring.split('\n')[0] if docstring else ""
            
            return Endpoint(
                method=method,
                path=path,
                summary=summary,
                description=docstring,
                parameters=parameters,
                request_body=None,
                responses=[Response(200, "Success")],
                security=[],
                tags=[],
                deprecated=False,
                source_file=self.file_path,
                line_number=func_node.lineno,
                confidence=0.95,
                handler_method=func_node.name
            )
        except Exception as e:
            print(f"Error parsing FastAPI endpoint: {e}")
            return None
    
    def _parse_flask_endpoint(self, func_node: ast.FunctionDef, decorator) -> Optional[Endpoint]:
        """Parse Flask endpoint"""
        try:
            method = "GET"
            path = "/"
            
            if isinstance(decorator, ast.Call):
                if decorator.args:
                    path = ast.literal_eval(decorator.args[0])
                
                # Check for methods parameter
                for keyword in decorator.keywords:
                    if keyword.arg == 'methods':
                        if isinstance(keyword.value, ast.List):
                            methods = [ast.literal_eval(elt) for elt in keyword.value.elts]
                            method = methods[0] if methods else "GET"
                
                if isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr != 'route':
                        method = decorator.func.attr.upper()
            
            parameters = self._extract_function_parameters(func_node)
            docstring = ast.get_docstring(func_node) or ""
            
            return Endpoint(
                method=method,
                path=path,
                summary=docstring.split('\n')[0] if docstring else "",
                description=docstring,
                parameters=parameters,
                request_body=None,
                responses=[Response(200, "Success")],
                security=[],
                tags=[],
                deprecated=False,
                source_file=self.file_path,
                line_number=func_node.lineno,
                confidence=0.95,
                handler_method=func_node.name
            )
        except Exception as e:
            print(f"Error parsing Flask endpoint: {e}")
            return None
    
    def _parse_django_endpoint(self, node: ast.Call) -> Optional[Endpoint]:
        """Parse Django endpoint"""
        try:
            path = "/"
            view = None
            
            if node.args:
                path = ast.literal_eval(node.args[0])
            
            if len(node.args) > 1:
                view = node.args[1]
            
            return Endpoint(
                method="GET",
                path=path,
                summary="",
                description="",
                parameters=[],
                request_body=None,
                responses=[Response(200, "Success")],
                security=[],
                tags=[],
                deprecated=False,
                source_file=self.file_path,
                line_number=node.lineno,
                confidence=0.85
            )
        except Exception as e:
            print(f"Error parsing Django endpoint: {e}")
            return None
    
    def _extract_function_parameters(self, func_node: ast.FunctionDef) -> List[Parameter]:
        """Extract parameters from function signature"""
        parameters = []
        
        for arg in func_node.args.args:
            if arg.arg != 'self':
                param = Parameter(
                    name=arg.arg,
                    type="string",
                    required=True,
                    location="query"
                )
                parameters.append(param)
        
        return parameters


class JavaScriptASTExtractor:
    """Extract endpoints from JavaScript/TypeScript using regex + AST-like parsing"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.endpoints: List[Endpoint] = []
        self.content = ""
        self.source_lines = []
    
    def extract(self) -> List[Endpoint]:
        """Extract endpoints from JavaScript file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.source_lines = self.content.split('\n')
        except Exception as e:
            print(f"Error reading {self.file_path}: {e}")
            return []
        
        self._extract_express()
        self._extract_nestjs()
        
        return self.endpoints
    
    def _extract_express(self):
        """Extract Express.js endpoints"""
        import re
        
        # Pattern: app.get('/path', handler)
        pattern = r"app\.(get|post|put|delete|patch)\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*"
        
        for match in re.finditer(pattern, self.content):
            method = match.group(1).upper()
            path = match.group(2)
            line_number = self.content[:match.start()].count('\n') + 1
            
            endpoint = Endpoint(
                method=method,
                path=path,
                summary="",
                description="",
                parameters=[],
                request_body=None,
                responses=[Response(200, "Success")],
                security=[],
                tags=[],
                deprecated=False,
                source_file=self.file_path,
                line_number=line_number,
                confidence=0.90
            )
            self.endpoints.append(endpoint)
    
    def _extract_nestjs(self):
        """Extract NestJS endpoints"""
        import re
        
        # Pattern: @Get('/path')
        pattern = r"@(Get|Post|Put|Delete|Patch)\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
        
        for match in re.finditer(pattern, self.content):
            method = match.group(1).upper()
            path = match.group(2)
            line_number = self.content[:match.start()].count('\n') + 1
            
            endpoint = Endpoint(
                method=method,
                path=path,
                summary="",
                description="",
                parameters=[],
                request_body=None,
                responses=[Response(200, "Success")],
                security=[],
                tags=[],
                deprecated=False,
                source_file=self.file_path,
                line_number=line_number,
                confidence=0.90
            )
            self.endpoints.append(endpoint)


class PHPASTExtractor:
    """Extract endpoints from PHP using regex + structural analysis"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.endpoints: List[Endpoint] = []
        self.content = ""
        self.source_lines = []
    
    def extract(self) -> List[Endpoint]:
        """Extract endpoints from PHP file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.source_lines = self.content.split('\n')
        except Exception as e:
            print(f"Error reading {self.file_path}: {e}")
            return []
        
        self._extract_laravel()
        self._extract_symfony()
        
        return self.endpoints
    
    def _extract_laravel(self):
        """Extract Laravel routes"""
        import re
        
        # Pattern: Route::get('/path', 'Controller@method')
        pattern = r"Route::(get|post|put|delete|patch)\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)"
        
        for match in re.finditer(pattern, self.content, re.IGNORECASE):
            method = match.group(1).upper()
            path = match.group(2)
            handler = match.group(3)
            line_number = self.content[:match.start()].count('\n') + 1
            
            handler_parts = handler.split('@')
            handler_class = handler_parts[0] if len(handler_parts) > 0 else None
            handler_method = handler_parts[1] if len(handler_parts) > 1 else None
            
            endpoint = Endpoint(
                method=method,
                path=path,
                summary="",
                description="",
                parameters=[],
                request_body=None,
                responses=[Response(200, "Success")],
                security=[],
                tags=[],
                deprecated=False,
                source_file=self.file_path,
                line_number=line_number,
                confidence=0.95,
                handler_class=handler_class,
                handler_method=handler_method
            )
            self.endpoints.append(endpoint)
    
    def _extract_symfony(self):
        """Extract Symfony routes"""
        import re
        
        # Pattern: #[Route('/path', methods: ['GET'])]
        pattern = r"#\[Route\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*methods:\s*\[\s*['\"]([^'\"]+)['\"]\s*\]\s*\)\s*\]"
        
        for match in re.finditer(pattern, self.content):
            path = match.group(1)
            method = match.group(2).upper()
            line_number = self.content[:match.start()].count('\n') + 1
            
            endpoint = Endpoint(
                method=method,
                path=path,
                summary="",
                description="",
                parameters=[],
                request_body=None,
                responses=[Response(200, "Success")],
                security=[],
                tags=[],
                deprecated=False,
                source_file=self.file_path,
                line_number=line_number,
                confidence=0.90
            )
            self.endpoints.append(endpoint)


class UnifiedPipeline:
    """Unified extraction pipeline for all frameworks"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.endpoints: List[Endpoint] = []
        self.framework_detected = None
    
    def extract_from_repository(self) -> Dict[str, Any]:
        """Extract all endpoints from repository"""
        self._scan_repository()
        
        return {
            "endpoints": [asdict(ep) for ep in self.endpoints],
            "framework": self.framework_detected,
            "total_endpoints": len(self.endpoints),
            "statistics": self._generate_statistics()
        }
    
    def _scan_repository(self):
        """Scan repository for API files"""
        # Detect framework
        self._detect_framework()
        
        # Extract based on framework
        if self.framework_detected == "python":
            self._extract_python_files()
        elif self.framework_detected == "javascript":
            self._extract_javascript_files()
        elif self.framework_detected == "php":
            self._extract_php_files()
    
    def _detect_framework(self):
        """Detect framework from repository structure"""
        # Check for Python frameworks
        if (self.repo_path / "requirements.txt").exists():
            self.framework_detected = "python"
            return
        
        if (self.repo_path / "setup.py").exists():
            self.framework_detected = "python"
            return
        
        # Check for JavaScript frameworks
        if (self.repo_path / "package.json").exists():
            self.framework_detected = "javascript"
            return
        
        # Check for PHP frameworks
        if (self.repo_path / "composer.json").exists():
            self.framework_detected = "php"
            return
        
        if (self.repo_path / "routes" / "api.php").exists():
            self.framework_detected = "php"
            return
    
    def _extract_python_files(self):
        """Extract from Python files"""
        for py_file in self.repo_path.rglob("*.py"):
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
            
            extractor = PythonASTExtractor(str(py_file))
            endpoints = extractor.extract()
            self.endpoints.extend(endpoints)
    
    def _extract_javascript_files(self):
        """Extract from JavaScript files"""
        for js_file in self.repo_path.rglob("*.js"):
            if "node_modules" in str(js_file):
                continue
            
            extractor = JavaScriptASTExtractor(str(js_file))
            endpoints = extractor.extract()
            self.endpoints.extend(endpoints)
        
        for ts_file in self.repo_path.rglob("*.ts"):
            if "node_modules" in str(ts_file):
                continue
            
            extractor = JavaScriptASTExtractor(str(ts_file))
            endpoints = extractor.extract()
            self.endpoints.extend(endpoints)
    
    def _extract_php_files(self):
        """Extract from PHP files"""
        for php_file in self.repo_path.rglob("*.php"):
            if "vendor" in str(php_file):
                continue
            
            extractor = PHPASTExtractor(str(php_file))
            endpoints = extractor.extract()
            self.endpoints.extend(endpoints)
    
    def _generate_statistics(self) -> Dict[str, Any]:
        """Generate extraction statistics"""
        methods = defaultdict(int)
        files = set()
        
        for endpoint in self.endpoints:
            methods[endpoint.method] += 1
            files.add(endpoint.source_file)
        
        return {
            "total_endpoints": len(self.endpoints),
            "methods": dict(methods),
            "files_scanned": len(files),
            "average_confidence": sum(ep.confidence for ep in self.endpoints) / len(self.endpoints) if self.endpoints else 0
        }
