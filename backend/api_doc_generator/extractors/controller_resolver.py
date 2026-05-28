"""Stage 7: Controller Resolution - Resolve route handlers to actual files with import tracking."""

import re
from pathlib import Path
from typing import Dict, Optional, List, Tuple


class ControllerResolver:
    """Resolve controller references to actual files with full import resolution."""

    def __init__(self, repo_path: str, framework: str = "laravel", imports: Optional[Dict[str, str]] = None):
        self.repo_path = Path(repo_path)
        self.framework = framework
        self.imports = imports or {}  # alias -> full_class_path
        self.controller_cache = {}
        self.file_cache = {}

    def resolve(self, controller_action: str, namespace: str = "", imports: Optional[Dict[str, str]] = None) -> Optional[Dict]:
        """Resolve controller@action to file and method with full import resolution."""
        if not controller_action:
            return None

        # Update imports if provided
        if imports:
            self.imports.update(imports)

        cache_key = f"{namespace}::{controller_action}"
        if cache_key in self.controller_cache:
            return self.controller_cache[cache_key]

        result = None
        if self.framework == "laravel":
            result = self._resolve_laravel(controller_action, namespace)
        elif self.framework == "express":
            result = self._resolve_express(controller_action)
        elif self.framework == "fastapi":
            result = self._resolve_fastapi(controller_action)

        self.controller_cache[cache_key] = result
        return result

    def _resolve_laravel(self, controller_action: str, namespace: str = "") -> Optional[Dict]:
        """Resolve Laravel controller@action with full import resolution."""
        if "@" not in controller_action:
            return None

        controller_name, action = controller_action.split("@", 1)

        # Step 1: Resolve controller class name
        full_class = self._resolve_controller_class(controller_name, namespace)
        if not full_class:
            return None

        # Step 2: Convert class path to file path
        file_path = self._class_to_file_path(full_class)
        if not file_path or not file_path.exists():
            return None

        # Step 3: Verify method exists in controller and extract metadata
        method_info = self._extract_method_info(file_path, action)
        if not method_info:
            return None

        # Calculate confidence based on evidence found
        confidence = self._calculate_confidence(
            has_import=controller_name in self.imports,
            has_namespace=bool(namespace),
            method_found=True,
            has_docblock=method_info.get("has_docblock", False),
            has_parameters=method_info.get("has_parameters", False)
        )

        return {
            "file_path": str(file_path),
            "class_name": controller_name,
            "method_name": action,
            "full_class": full_class,
            "confidence": confidence,
            "resolved": True,
            "method_info": method_info
        }

    def _resolve_controller_class(self, controller_name: str, namespace: str = "") -> Optional[str]:
        """Resolve controller class name to full class path."""
        # Step 1: Check if it's already a full class path
        if "\\" in controller_name:
            return controller_name

        # Step 2: Check imports (use statements)
        if controller_name in self.imports:
            return self.imports[controller_name]

        # Step 3: Check if namespace is provided
        if namespace:
            return f"{namespace}\\{controller_name}"

        # Step 4: Default to App\Http\Controllers
        return f"App\\Http\\Controllers\\{controller_name}"

    def _class_to_file_path(self, full_class: str) -> Optional[Path]:
        """Convert full class path to file path."""
        # Remove leading backslash if present
        full_class = full_class.lstrip("\\")

        # Split namespace and class name
        parts = full_class.split("\\")
        class_name = parts[-1]
        namespace_parts = parts[:-1]

        # Map namespace to directory
        if namespace_parts[0] == "App":
            # App\Http\Controllers\Auth\AuthenticatedSessionController
            # -> app/Http/Controllers/Auth/AuthenticatedSessionController.php
            rel_path = Path("app") / Path(*namespace_parts[1:]) / f"{class_name}.php"
        else:
            # Fallback for other namespaces
            rel_path = Path(*namespace_parts) / f"{class_name}.php"

        file_path = self.repo_path / rel_path
        return file_path

    def _method_exists_in_controller(self, file_path: Path, method_name: str) -> bool:
        """Check if method exists in controller file."""
        if not file_path.exists():
            return False

        # Cache file content
        if str(file_path) not in self.file_cache:
            try:
                self.file_cache[str(file_path)] = file_path.read_text()
            except (IOError, UnicodeDecodeError):
                return False

        content = self.file_cache[str(file_path)]

        # Look for method definition
        pattern = rf"public\s+function\s+{method_name}\s*\("
        return bool(re.search(pattern, content))

    def _extract_method_info(self, file_path: Path, method_name: str) -> Optional[Dict]:
        """Extract method information from controller using AST-like parsing."""
        if not file_path.exists():
            return None

        # Cache file content
        if str(file_path) not in self.file_cache:
            try:
                self.file_cache[str(file_path)] = file_path.read_text()
            except (IOError, UnicodeDecodeError):
                return None

        content = self.file_cache[str(file_path)]

        # Find method definition
        method_pattern = rf"(public|protected|private)\s+function\s+{method_name}\s*\((.*?)\)"
        method_match = re.search(method_pattern, content, re.DOTALL)
        
        if not method_match:
            return None

        # Extract method information
        visibility = method_match.group(1)
        parameters = method_match.group(2).strip()

        # Check for docblock
        method_start = method_match.start()
        docblock_pattern = r"/\*\*.*?\*/"
        docblock_match = re.search(docblock_pattern, content[:method_start], re.DOTALL)
        has_docblock = bool(docblock_match)

        return {
            "visibility": visibility,
            "has_parameters": bool(parameters),
            "parameters": parameters,
            "has_docblock": has_docblock,
            "line_number": content[:method_start].count("\n") + 1
        }

    def _calculate_confidence(self, has_import: bool, has_namespace: bool, method_found: bool, 
                            has_docblock: bool, has_parameters: bool) -> float:
        """Calculate confidence score based on evidence found."""
        confidence = 0.0

        # Base score for method found
        if method_found:
            confidence += 0.6

        # Bonus for explicit import
        if has_import:
            confidence += 0.2

        # Bonus for namespace context
        if has_namespace:
            confidence += 0.1

        # Bonus for docblock (indicates well-documented code)
        if has_docblock:
            confidence += 0.05

        # Bonus for parameters (indicates real implementation)
        if has_parameters:
            confidence += 0.05

        return min(confidence, 0.99)

    def _resolve_express(self, controller_action: str) -> Optional[Dict]:
        """Resolve Express controller reference."""
        # Express typically uses imported functions or class methods
        # This would require more complex resolution
        return None

    def _resolve_fastapi(self, controller_action: str) -> Optional[Dict]:
        """Resolve FastAPI function reference."""
        # FastAPI uses decorated functions
        # This would require more complex resolution
        return None
