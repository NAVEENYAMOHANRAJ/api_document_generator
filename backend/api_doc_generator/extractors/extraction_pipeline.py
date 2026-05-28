"""Extraction pipeline for processing repository files."""

from typing import Dict, List, Tuple, Optional
from pathlib import PurePosixPath

from api_doc_generator.scanner.backend_detector import BackendFileDetector, FrameworkCandidateDetector
from api_doc_generator.frameworks.registry import FrameworkExtractorRegistry


class ExtractionPipeline:
    """Batch endpoint extraction over repository files."""

    def __init__(self, batch_size: int = 50, progress_callback=None):
        self.batch_size = batch_size
        self.files: List[Dict[str, str]] = []
        self.progress_callback = progress_callback

    def add_files(self, files: List[Dict[str, str]]) -> None:
        self.files.extend(files)

    def run(self):
        """Run the extraction pipeline."""
        # Normalize all paths to posix-style for consistent matching across Windows/Linux.
        raw_content_by_path = {item.get("path", ""): item.get("content", "") for item in self.files}
        content_by_path = {
            str(PurePosixPath(path)): content for path, content in raw_content_by_path.items() if path
        }
        tree_entries = [{"path": path, "size": len(content)} for path, content in content_by_path.items()]
        backend_files = BackendFileDetector().find_backend_files(tree_entries, content_by_path)

        if not backend_files:
            backend_files = tree_entries

        # Detect frameworks at repository level (not per-file)
        repo_frameworks = FrameworkCandidateDetector.detect(backend_files, content_by_path)
        
        endpoints = []
        errors = []
        processed = 0
        total_files = len(backend_files)

        for entry in backend_files:
            path = entry.get("path", "")
            content = content_by_path.get(path, "")
            
            # Use repository-level frameworks if available, otherwise check per-file
            if repo_frameworks:
                frameworks_to_try = repo_frameworks
            else:
                frameworks_to_try = FrameworkCandidateDetector.detect([entry], {path: content})
            
            try:
                for framework in frameworks_to_try:
                    endpoints.extend(self._extract_endpoints(path, content, framework))
                processed += 1
            except Exception as exc:
                errors.append({"file": path, "error": str(exc)})

            if self.progress_callback:
                try:
                    self.progress_callback({
                        "completed": processed,
                        "failed": len(errors),
                        "total": total_files,
                        "current_file": path
                    })
                except Exception:
                    pass

        deduped, duplicates_removed = self._dedupe(endpoints)
        filtered = [endpoint for endpoint in deduped if self._valid_endpoint(endpoint)]

        stats = {
            "processed_files": processed,
            "failed_files": len(errors),
            "duplicates_removed": duplicates_removed,
            "total_unique_endpoints": len(filtered),
        }
        
        return filtered, errors, stats

    def _extract_endpoints(self, file_path: str, content: str, framework: str) -> List[Dict]:
        """Extract endpoints based on framework."""
        entry = FrameworkExtractorRegistry.get(framework)
        if not entry:
            return []
        extractor = entry.extractor
        # Existing extractors use `.extract(file_path, content)` API.
        return extractor.extract(file_path, content)

    @staticmethod
    def _dedupe(endpoints):
        """Remove duplicate endpoints."""
        result = []
        seen: Dict[Tuple[str, str, str], int] = {}
        duplicates = 0

        def richness_score(endpoint: Dict) -> float:
            score = 0.0
            for key in ("path_params", "query_params", "headers", "middleware", "security", "responses"):
                value = endpoint.get(key)
                if isinstance(value, list):
                    score += min(len(value), 5) * 1.5
                elif value:
                    score += 1.0
            if endpoint.get("request_body") or endpoint.get("requestBody"):
                score += 3.0
            if endpoint.get("response_model"):
                score += 1.0
            conf = endpoint.get("confidence")
            if isinstance(conf, (int, float)):
                score += float(conf)
            return score

        for endpoint in endpoints:
            key = (endpoint.get("method"), endpoint.get("path"), endpoint.get("source_file"))
            if key in seen:
                duplicates += 1
                existing_index = seen[key]
                existing = result[existing_index]
                if richness_score(endpoint) > richness_score(existing):
                    # Preserve provenance trail where possible.
                    if existing.get("provenance") and not endpoint.get("provenance"):
                        endpoint["provenance"] = existing.get("provenance")
                    result[existing_index] = endpoint
                else:
                    # Merge any missing rich fields into existing endpoint.
                    for field in ("middleware", "security", "headers", "query_params", "path_params", "responses"):
                        if not existing.get(field) and endpoint.get(field):
                            existing[field] = endpoint.get(field)
                    if not existing.get("request_body") and endpoint.get("request_body"):
                        existing["request_body"] = endpoint.get("request_body")
                    if not existing.get("requestBody") and endpoint.get("requestBody"):
                        existing["requestBody"] = endpoint.get("requestBody")
                continue
            seen[key] = len(result)
            result.append(endpoint)
        return result, duplicates

    @staticmethod
    def _valid_endpoint(endpoint) -> bool:
        """Check if endpoint is valid."""
        path = endpoint.get("path", "")
        return path.startswith("/")
