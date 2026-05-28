"""Flask extractor using AST parsing."""

import ast
from typing import Dict, List, Optional


class FlaskExtractor(ast.NodeVisitor):
    """Extract Flask routes using AST parsing."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.routes = []
        self.blueprints = {}
        self.app_name = None

    @classmethod
    def extract(cls, file_path: str, content: str) -> List[Dict]:
        """Extract Flask routes from file content."""
        extractor = cls(file_path)
        try:
            tree = ast.parse(content)
            extractor.visit(tree)
        except SyntaxError:
            pass
        return extractor.routes

    def visit_Assign(self, node: ast.Assign) -> None:
        """Track app and blueprint assignments."""
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name):
                func_name = node.value.func.id
                if func_name == 'Flask':
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.app_name = target.id
                elif func_name == 'Blueprint':
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            prefix = self._extract_blueprint_prefix(node.value)
                            self.blueprints[target.id] = {'prefix': prefix}
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Extract routes from function decorators."""
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
            if decorator.func.attr != 'route':
                return None

            if decorator.args and isinstance(decorator.args[0], ast.Constant):
                path = decorator.args[0].value
                if isinstance(path, str):
                    methods = ['GET']
                    for keyword in decorator.keywords:
                        if keyword.arg == 'methods' and isinstance(keyword.value, ast.List):
                            methods = [elt.value.upper() for elt in keyword.value.elts if isinstance(elt, ast.Constant)]

                    routes = []
                    for method in methods:
                        routes.append({
                            'method': method,
                            'path': path,
                            'source_file': self.file_path,
                            'line_number': lineno,
                            'confidence': 0.90,
                            'detection_type': 'framework_route_definition',
                            'provenance': {
                                'source_file': self.file_path,
                                'detection_type': 'framework_route_definition',
                                'framework': 'Flask',
                                'line_number': lineno,
                            }
                        })
                    
                    # Return first route (will be added to self.routes)
                    return routes[0] if routes else None
        return None

    def _extract_blueprint_prefix(self, call_node: ast.Call) -> Optional[str]:
        """Extract url_prefix from Blueprint call."""
        for keyword in call_node.keywords:
            if keyword.arg == 'url_prefix' and isinstance(keyword.value, ast.Constant):
                return keyword.value.value
        return None

