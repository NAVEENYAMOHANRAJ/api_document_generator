"""Stage 11: Authentication Detection - Detect authentication mechanisms from source code."""

import re
from pathlib import Path
from typing import Dict, Optional, List


class AuthenticationDetector:
    """Detect authentication mechanisms from route and controller code."""

    def __init__(self, framework: str = "laravel"):
        self.framework = framework

    def detect_from_route(self, route: Dict) -> Optional[Dict]:
        """Detect authentication from route middleware."""
        if self.framework == "laravel":
            return self._detect_laravel_from_route(route)
        return None

    def detect_from_controller(self, file_path: str, method_name: str) -> Optional[Dict]:
        """Detect authentication from controller code."""
        if not Path(file_path).exists():
            return None

        content = Path(file_path).read_text()

        if self.framework == "laravel":
            return self._detect_laravel_from_controller(content, method_name)
        return None

    def _detect_laravel_from_route(self, route: Dict) -> Optional[Dict]:
        """Detect Laravel authentication from route middleware."""
        middleware = route.get("middleware", [])
        if not middleware:
            return None

        for mw in middleware:
            if "auth:sanctum" in mw:
                return {
                    "mechanism": "Sanctum",
                    "type": "bearer",
                    "source": "middleware",
                    "package": "laravel/sanctum",
                    "confidence": 0.95
                }
            elif "auth:passport" in mw:
                return {
                    "mechanism": "Passport",
                    "type": "oauth2",
                    "source": "middleware",
                    "package": "laravel/passport",
                    "confidence": 0.95
                }
            elif "auth:api" in mw:
                return {
                    "mechanism": "API Token",
                    "type": "bearer",
                    "source": "middleware",
                    "confidence": 0.85
                }
            elif "auth" in mw:
                return {
                    "mechanism": "Session",
                    "type": "session",
                    "source": "middleware",
                    "confidence": 0.75
                }

        return None

    def _detect_laravel_from_controller(self, content: str, method_name: str) -> Optional[Dict]:
        """Detect Laravel authentication from controller code."""
        # Find method definition
        method_pattern = rf"function\s+{method_name}\s*\(\s*([^)]*)\s*\)"
        method_match = re.search(method_pattern, content)
        if not method_match:
            return None

        method_start = method_match.start()
        method_body_start = content.find("{", method_start)
        method_body_end = self._find_matching_brace(content, method_body_start)
        method_body = content[method_body_start:method_body_end]

        # Check for JWT usage
        if "jwt" in method_body.lower() or "token" in method_body.lower():
            # Check for tymon/jwt-auth package
            if "JWTAuth" in method_body or "jwt()" in method_body:
                return {
                    "mechanism": "JWT",
                    "type": "bearer",
                    "source": "controller",
                    "package": "tymon/jwt-auth",
                    "confidence": 0.90
                }

        # Check for Sanctum usage
        if "auth()->user()" in method_body or "Auth::user()" in method_body:
            return {
                "mechanism": "Sanctum",
                "type": "bearer",
                "source": "controller",
                "package": "laravel/sanctum",
                "confidence": 0.80
            }

        # Check for API token usage
        if "api_token" in method_body or "apiToken" in method_body:
            return {
                "mechanism": "API Token",
                "type": "bearer",
                "source": "controller",
                "confidence": 0.75
            }

        return None

    def _find_matching_brace(self, content: str, start: int) -> int:
        """Find matching closing brace."""
        count = 1
        i = start + 1
        while i < len(content) and count > 0:
            if content[i] == "{":
                count += 1
            elif content[i] == "}":
                count -= 1
            i += 1
        return i
