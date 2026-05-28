"""AST-First Extraction Pipeline - Orchestrates all stages with complete production data extraction."""

from pathlib import Path
from typing import Dict, List, Optional

from api_doc_generator.extractors.laravel_extractor import LaravelExtractor
from api_doc_generator.extractors.production_data_extractor import ProductionDataExtractor
from api_doc_generator.extractors.controller_resolver import ControllerResolver
from api_doc_generator.extractors.request_schema_extractor import RequestSchemaExtractor
from api_doc_generator.extractors.response_schema_extractor import ResponseSchemaExtractor
from api_doc_generator.extractors.authentication_detector import AuthenticationDetector
from api_doc_generator.utils.endpoint_normalizer import EndpointNormalizer
from api_doc_generator.utils.confidence_scorer import ConfidenceScorer


class ExtractionPipeline:
    """Complete extraction pipeline with all 30+ production data points."""

    def __init__(self, repo_path: str, framework: str = None):
        self.repo_path = Path(repo_path)
        self.framework = framework
        self.endpoints = []
        
        # All 30+ data points
        self.api_metadata = {}
        self.authentication = []
        self.environments = []
        self.rate_limits = {}
        self.global_headers = []
        self.versioning = {}
        self.webhooks = []
        self.error_definitions = []
        self.changelog = []
        self.schemas = {}
        
        self.stats = {
            "total_endpoints": 0,
            "endpoints_by_method": {},
            "endpoints_by_tag": {},
            "authentication_methods": 0,
            "environments_count": 0,
            "error_definitions_count": 0,
            "webhooks_count": 0,
            "changelog_entries": 0,
            "schemas_count": 0,
        }

    def extract_from_files(self, files: List[Dict]) -> Dict:
        """Extract complete documentation with all 30+ data points."""
        try:
            # Extract production data (all 30+ points)
            self._extract_production_data()
            
            # Extract routes
            self._extract_routes(files)
            
            # Enhance endpoints with details
            self._enhance_endpoints()
            
            # Calculate statistics
            self._calculate_statistics()

            return {
                "success": True,
                "api": self.api_metadata,
                "authentication": self.authentication,
                "environments": self.environments,
                "rateLimits": self.rate_limits,
                "globalHeaders": self.global_headers,
                "versioning": self.versioning,
                "webhooks": self.webhooks,
                "errorDefinitions": self.error_definitions,
                "changelog": self.changelog,
                "endpoints": self.endpoints,
                "schemas": self.schemas,
                "stats": self.stats,
                "framework": self.framework,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stats": self.stats,
            }

    def _extract_production_data(self) -> None:
        """Extract all 30+ production data points."""
        if not self.framework:
            return
        
        extractor = ProductionDataExtractor(self.repo_path, self.framework)
        
        # API Metadata (9 points)
        self.api_metadata = extractor.extract_api_metadata()
        
        # Infrastructure (7 points)
        self.authentication = extractor.extract_authentication() or []
        self.environments = extractor.extract_environments() or []
        self.rate_limits = extractor.extract_rate_limits() or {}
        self.global_headers = extractor.extract_global_headers() or []
        self.versioning = extractor.extract_versioning() or {}
        self.webhooks = extractor.extract_webhooks() or []
        self.error_definitions = extractor.extract_error_definitions() or []
        self.changelog = extractor.extract_changelog() or []
        
        # Update stats
        self.stats["authentication_methods"] = len(self.authentication)
        self.stats["environments_count"] = len(self.environments)
        self.stats["error_definitions_count"] = len(self.error_definitions)
        self.stats["webhooks_count"] = len(self.webhooks)
        self.stats["changelog_entries"] = len(self.changelog)

    def _extract_routes(self, files: List[Dict]) -> None:
        """Extract routes from files."""
        if not self.framework:
            return

        if self.framework == "Laravel":
            self._extract_laravel_routes(files)

    def _extract_laravel_routes(self, files: List[Dict]) -> None:
        """Extract Laravel routes."""
        for file_data in files:
            path = file_data.get("path", "")
            content = file_data.get("content", "")

            if "route" not in path.lower():
                continue

            try:
                routes = LaravelExtractor.extract(path, content, str(self.repo_path))
                self.endpoints.extend(routes)
            except Exception as e:
                print(f"Error extracting routes from {path}: {e}")

    def _enhance_endpoints(self) -> None:
        """Enhance endpoints with all 20+ data points."""
        extractor = ProductionDataExtractor(self.repo_path, self.framework)
        
        for endpoint in self.endpoints:
            # Extract detailed information
            endpoint = extractor.extract_endpoint_details(endpoint)

    def _calculate_statistics(self) -> None:
        """Calculate extraction statistics."""
        self.stats["total_endpoints"] = len(self.endpoints)
        
        for endpoint in self.endpoints:
            method = endpoint.get("method", "GET")
            self.stats["endpoints_by_method"][method] = self.stats["endpoints_by_method"].get(method, 0) + 1
            
            for tag in endpoint.get("tags", []):
                self.stats["endpoints_by_tag"][tag] = self.stats["endpoints_by_tag"].get(tag, 0) + 1
        
        self.stats["schemas_count"] = len(self.schemas)
