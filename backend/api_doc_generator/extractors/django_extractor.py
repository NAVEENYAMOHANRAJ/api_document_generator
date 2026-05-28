"""Django REST Framework extractor using AST parsing."""

import ast
import re
from typing import Dict, List, Optional


class DjangoExtractor(ast.NodeVisitor):
    """Extract Django URL patterns using AST parsing."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.routes = []
        self.current_prefix = ''

    @classmethod
    def extract(cls, file_path: str, content: str) -> List[Dict]:
        """Extract Django URL patterns from file content."""
        extractor = cls(file_path)
        try:
            tree = ast.parse(content)
            extractor.visit(tree)
        except SyntaxError:
            pass
        return extractor.routes

    def visit_Assign(self, node: ast.Assign) -> None:
        """Find urlpatterns assignments."""
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'urlpatterns':
                if isinstance(node.value, ast.List):
                    for elt in node.value.elts:
                        self._extract_from_element(elt, '', node.lineno)
        self.generic_visit(node)

    def _extract_from_element(self, element: ast.expr, prefix: str, lineno: int) -> None:
        """Extract routes from list elements."""
        if not isinstance(element, ast.Call):
            return

        if isinstance(element.func, ast.Name):
            func_name = element.func.id
            
            # Handle path() and re_path()
            if func_name in ('path', 're_path') and element.args:
                if isinstance(element.args[0], ast.Constant):
                    path = element.args[0].value
                    if isinstance(path, str):
                        full_path = self._normalize_path(prefix + path)
                        
                        # Try to extract HTTP method from view
                        method = self._extract_method_from_view(element)
                        
                        self.routes.append({
                            'method': method,
                            'path': full_path,
                            'source_file': self.file_path,
                            'line_number': element.lineno,
                            'confidence': 0.85,
                            'detection_type': 'framework_route_definition',
                            'provenance': {
                                'source_file': self.file_path,
                                'detection_type': 'framework_route_definition',
                                'framework': 'Django',
                                'line_number': element.lineno,
                            }
                        })
            
            # Handle include()
            elif func_name == 'include' and element.args:
                # Extract prefix from include if available
                include_prefix = prefix
                if len(element.args) > 1 and isinstance(element.args[1], ast.Constant):
                    include_prefix = prefix + element.args[1].value
                
                # Note: We can't easily follow includes without file system access
                # This would require cross-file resolution

    def _extract_method_from_view(self, element: ast.Call) -> str:
        """Try to extract HTTP method from view."""
        # Default to GET
        method = 'GET'
        
        # Check if there's a view argument
        if len(element.args) > 1:
            view_arg = element.args[1]
            # Try to infer method from view name
            if isinstance(view_arg, ast.Attribute):
                attr_name = view_arg.attr.lower()
                if 'post' in attr_name:
                    method = 'POST'
                elif 'put' in attr_name:
                    method = 'PUT'
                elif 'delete' in attr_name:
                    method = 'DELETE'
                elif 'patch' in attr_name:
                    method = 'PATCH'
        
        return method

    def _normalize_path(self, path: str) -> str:
        """Normalize path."""
        # Remove regex patterns for display
        path = re.sub(r'\^', '', path)
        path = re.sub(r'\$', '', path)
        path = re.sub(r'\?P<[^>]+>', '{', path)
        path = re.sub(r'>', '}', path)
        
        # Normalize slashes
        path = re.sub(r'/+', '/', path)
        
        # Remove trailing slash (except for root)
        if path != '/' and path.endswith('/'):
            path = path[:-1]
        
        # Ensure leading slash
        if not path.startswith('/'):
            path = '/' + path
        
        return path

