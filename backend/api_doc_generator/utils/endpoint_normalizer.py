"""Stage 12: Endpoint Normalization - Normalize and deduplicate endpoints."""

from typing import Dict, List, Tuple


class EndpointNormalizer:
    """Normalize and deduplicate endpoints."""

    @staticmethod
    def normalize_path(path: str) -> str:
        """Normalize path for consistent comparison."""
        # Remove trailing slash (except root)
        if path != "/" and path.endswith("/"):
            path = path[:-1]

        # Remove duplicate slashes
        while "//" in path:
            path = path.replace("//", "/")

        # Normalize path parameters
        path = path.replace(":id", "{id}")
        path = path.replace("<id>", "{id}")

        # Ensure leading slash
        if not path.startswith("/"):
            path = "/" + path

        return path

    @staticmethod
    def deduplicate(endpoints: List[Dict]) -> List[Dict]:
        """Deduplicate endpoints by method and normalized path."""
        seen = {}
        result = []

        for endpoint in endpoints:
            method = endpoint.get("method", "GET").upper()
            path = EndpointNormalizer.normalize_path(endpoint.get("path", "/"))
            key = (method, path)

            if key not in seen:
                seen[key] = endpoint
                result.append(endpoint)
            else:
                # Keep endpoint with higher confidence
                existing = seen[key]
                if endpoint.get("confidence", 0) > existing.get("confidence", 0):
                    # Replace with higher confidence endpoint
                    result.remove(existing)
                    result.append(endpoint)
                    seen[key] = endpoint
                else:
                    # Merge provenance
                    if "provenance" in endpoint and "provenance" in existing:
                        if isinstance(existing.get("provenance"), list):
                            existing["provenance"].append(endpoint["provenance"])
                        else:
                            existing["provenance"] = [existing["provenance"], endpoint["provenance"]]

        return result

    @staticmethod
    def normalize_endpoint(endpoint: Dict) -> Dict:
        """Normalize all fields in endpoint."""
        normalized = endpoint.copy()

        # Normalize path
        normalized["path"] = EndpointNormalizer.normalize_path(endpoint.get("path", "/"))

        # Normalize method
        normalized["method"] = endpoint.get("method", "GET").upper()

        # Ensure confidence is in valid range
        confidence = normalized.get("confidence", 0.5)
        normalized["confidence"] = max(0.0, min(1.0, confidence))

        return normalized
