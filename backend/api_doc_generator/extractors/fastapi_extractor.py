"""FastAPI extractor using AST parsing."""

import ast
from typing import Dict, List, Optional


class FastAPIExtractor(ast.NodeVisitor):
    """Extract FastAPI routes using AST parsing."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.routes = []
        self.routers = {}
        self.app_name = None
        self.current_prefix = ''

    @classmethod
    def extract(cls, file_path: str, content: str) -> List[Dict]:
        """Extract FastAPI routes from file content."""
        extractor = cls(file_path)
        try:
            tree = ast.parse(content)
            extractor.visit(tree)
        except SyntaxError:
            pass
        return extractor.routes

    def visit_Assign(self, node: ast.Assign) -> None:
        """Track router and app assignments."""
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                func_name = node.value.func.id
                if func_name in ('FastAPI', 'APIRouter'):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.routers[target.id] = {
                                'type': func_name,
                                'prefix': self._extract_prefix_from_call(node.value)
                            }
                            if func_name == 'FastAPI':
                                self.app_name = target.id
        self.generic_visit(node)

    def visit_Expr(self, node: ast.Expr) -> None:
        """Handle standalone expressions like app.include_router()."""
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Attribute):
                if node.value.func.attr == 'include_router':
                    # Extract router inclusion
                    pass
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Extract routes from function decorators."""
        for decorator in node.decorator_list:
            route_info = self._extract_route_from_decorator(decorator, node.lineno)
            if route_info:
                self.routes.append(route_info)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Extract routes from async function decorators."""
        for decorator in node.decorator_list:
            route_info = self._extract_route_from_decorator(decorator, node.lineno)
            if route_info:
                self.routes.append(route_info)
        self.generic_visit(node)

    def _extract_route_from_decorator(self, decorator: ast.expr, lineno: int) -> Optional[Dict]:
        """Extract route information from decorator."""
        if not isinstance(decorator, ast.Call):
            return None

        if isinstance(decorator.func, ast.Attribute):
            method = decorator.func.attr
            if method not in ('get', 'post', 'put', 'delete', 'patch', 'options', 'head'):
                return None

            if decorator.args and isinstance(decorator.args[0], ast.Constant):
                path = decorator.args[0].value
                if isinstance(path, str):
                    # Extract tags if available
                    tags = []
                    for keyword in decorator.keywords:
                        if keyword.arg == 'tags' and isinstance(keyword.value, ast.List):
                            tags = [elt.value for elt in keyword.value.elts if isinstance(elt, ast.Constant)]
                    
                    return {
                        'method': method.upper(),
                        'path': path,
                        'source_file': self.file_path,
                        'line_number': lineno,
                        'confidence': 0.95,
                        'tags': tags if tags else [],
                        'detection_type': 'framework_route_definition',
                        'provenance': {
                            'source_file': self.file_path,
                            'detection_type': 'framework_route_definition',
                            'framework': 'FastAPI',
                            'line_number': lineno,
                        }
                    }
        return None

    def _extract_prefix_from_call(self, call_node: ast.Call) -> Optional[str]:
        """Extract prefix from APIRouter() call."""
        for keyword in call_node.keywords:
            if keyword.arg == 'prefix' and isinstance(keyword.value, ast.Constant):
                return keyword.value.value
        return None

