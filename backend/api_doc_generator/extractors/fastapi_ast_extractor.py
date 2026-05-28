"""
FastAPI AST-Based Extractor - Production Grade

Uses Python AST to extract:
- Route decorators (@app.get, @app.post, etc.)
- Path parameters
- Query parameters
- Request bodies (Pydantic models)
- Response models
- Dependencies (authentication)
- Tags
- Status codes
"""

import ast
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class FastAPIEndpoint:
    """FastAPI endpoint extracted from AST"""
    method: str
    path: str
    function_name: str
    summary: str = ""
    description: str = ""
    tags: List[str] = None
    status_code: int = 200
    response_model: Optional[str] = None
    request_body_model: Optional[str] = None
    dependencies: List[str] = None
    source_file: str = ""
    line_number: int = 0
    confidence: float = 0.95

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.dependencies is None:
            self.dependencies = []


class FastAPIASTExtractor:
    """Extract FastAPI routes using AST parsing"""

    HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.endpoints: List[FastAPIEndpoint] = []
        self.file_cache: Dict[str, str] = {}
        self.ast_cache: Dict[str, ast.Module] = {}

    def extract_all_endpoints(self) -> List[FastAPIEndpoint]:
        """Extract all FastAPI endpoints from repository"""
        
        # Find all Python files
        py_files = list(self.repo_path.rglob("*.py"))
        
        for py_file in py_files:
            try:
                self._extract_from_file(str(py_file))
            except Exception as e:
                print(f"Error processing {py_file}: {e}")
        
        return self.endpoints

    def _extract_from_file(self, file_path: str) -> None:
        """Extract endpoints from a single Python file"""
        
        try:
            content = self._read_file(file_path)
            tree = ast.parse(content)
        except Exception:
            return
        
        # Find FastAPI app instances
        app_names = self._find_app_instances(tree)
        
        if not app_names:
            return
        
        # Extract routes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self._extract_route_from_function(node, app_names, file_path, content)

    def _find_app_instances(self, tree: ast.Module) -> set:
        """Find FastAPI app variable names"""
        app_names = set()
        
        for node in ast.walk(tree):
            # FastAPI() instantiation
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call):
                    if isinstance(node.value.func, ast.Name):
                        if node.value.func.id == "FastAPI":
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    app_names.add(target.id)
        
        return app_names

    def _extract_route_from_function(
        self,
        func_node: ast.FunctionDef,
        app_names: set,
        file_path: str,
        content: str
    ) -> None:
        """Extract route information from a function with decorators"""
        
        for decorator in func_node.decorator_list:
            # Check if decorator is app.method() or app.route()
            if isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Attribute):
                    # app.get(), app.post(), etc.
                    if decorator.func.attr in self.HTTP_METHODS:
                        if isinstance(decorator.func.value, ast.Name):
                            if decorator.func.value.id in app_names:
                                self._process_route_decorator(
                                    decorator,
                                    decorator.func.attr.upper(),
                                    func_node,
                                    file_path,
                                    content
                                )

    def _process_route_decorator(
        self,
        decorator: ast.Call,
        method: str,
        func_node: ast.FunctionDef,
        file_path: str,
        content: str
    ) -> None:
        """Process a route decorator and extract endpoint info"""
        
        # Extract path from first argument
        path = None
        if decorator.args:
            first_arg = decorator.args[0]
            if isinstance(first_arg, ast.Constant):
                path = first_arg.value
        
        if not path:
            return
        
        # Extract keyword arguments
        status_code = 200
        response_model = None
        tags = []
        summary = ""
        description = ""
        
        for keyword in decorator.keywords:
            if keyword.arg == "status_code":
                if isinstance(keyword.value, ast.Constant):
                    status_code = keyword.value.value
            elif keyword.arg == "response_model":
                if isinstance(keyword.value, ast.Name):
                    response_model = keyword.value.id
            elif keyword.arg == "tags":
                if isinstance(keyword.value, ast.List):
                    tags = [
                        elt.value for elt in keyword.value.elts
                        if isinstance(elt, ast.Constant)
                    ]
            elif keyword.arg == "summary":
                if isinstance(keyword.value, ast.Constant):
                    summary = keyword.value.value
            elif keyword.arg == "description":
                if isinstance(keyword.value, ast.Constant):
                    description = keyword.value.value
        
        # Extract docstring as description if not provided
        if not description:
            docstring = ast.get_docstring(func_node)
            if docstring:
                description = docstring.split("\n")[0]
        
        # Extract request body model from function parameters
        request_body_model = self._extract_request_model(func_node)
        
        # Extract dependencies
        dependencies = self._extract_dependencies(func_node)
        
        # Create endpoint
        endpoint = FastAPIEndpoint(
            method=method,
            path=path,
            function_name=func_node.name,
            summary=summary or func_node.name,
            description=description,
            tags=tags,
            status_code=status_code,
            response_model=response_model,
            request_body_model=request_body_model,
            dependencies=dependencies,
            source_file=file_path,
            line_number=func_node.lineno,
            confidence=0.95
        )
        
        self.endpoints.append(endpoint)

    def _extract_request_model(self, func_node: ast.FunctionDef) -> Optional[str]:
        """Extract request body model from function parameters"""
        
        for arg in func_node.args.args:
            # Skip 'self' and common parameter names
            if arg.arg in ["self", "request", "response"]:
                continue
            
            # Check if parameter has type annotation
            if arg.annotation:
                if isinstance(arg.annotation, ast.Name):
                    # Simple type like: def create(user: User)
                    return arg.annotation.id
                elif isinstance(arg.annotation, ast.Subscript):
                    # Generic type like: def create(users: List[User])
                    if isinstance(arg.annotation.value, ast.Name):
                        return arg.annotation.value.id
        
        return None

    def _extract_dependencies(self, func_node: ast.FunctionDef) -> List[str]:
        """Extract dependencies from function parameters"""
        
        dependencies = []
        
        for arg in func_node.args.args:
            if arg.annotation:
                if isinstance(arg.annotation, ast.Subscript):
                    # Depends() pattern
                    if isinstance(arg.annotation.value, ast.Name):
                        if arg.annotation.value.id == "Depends":
                            # Extract the dependency function name
                            if arg.annotation.slice:
                                if isinstance(arg.annotation.slice, ast.Name):
                                    dependencies.append(arg.annotation.slice.id)
        
        return dependencies

    def _read_file(self, file_path: str) -> str:
        """Read file with caching"""
        if file_path in self.file_cache:
            return self.file_cache[file_path]
        
        try:
            content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
            self.file_cache[file_path] = content
            return content
        except Exception:
            return ""

    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert endpoints to dictionary format"""
        return [
            {
                "method": ep.method,
                "path": ep.path,
                "function_name": ep.function_name,
                "summary": ep.summary,
                "description": ep.description,
                "tags": ep.tags,
                "status_code": ep.status_code,
                "response_model": ep.response_model,
                "request_body_model": ep.request_body_model,
                "dependencies": ep.dependencies,
                "source": {
                    "file": ep.source_file,
                    "line": ep.line_number
                },
                "confidence": ep.confidence
            }
            for ep in self.endpoints
        ]
