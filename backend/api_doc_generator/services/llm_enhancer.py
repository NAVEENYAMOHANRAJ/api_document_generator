import json
import os
from typing import Any, Dict, List, Tuple

import requests
from api_doc_generator.utils.semantic_resolver import SemanticResolver
from api_doc_generator.utils.provenance_validator import ProvenanceValidator


class LLMDocumentationEnhancer:
    """Optionally enrich extracted endpoint metadata with AI-written descriptions."""

    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_API_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
        self.api_url = os.getenv("LLM_API_URL", self.DEFAULT_API_URL)
        self.model = os.getenv("LLM_MODEL", self.DEFAULT_MODEL)
        # Default to disabled to avoid non-source-grounded content in production docs.
        self.enabled = os.getenv("ENABLE_LLM_ENRICHMENT", "false").lower() in {"1", "true", "yes"}
        self.timeout = int(os.getenv("LLM_TIMEOUT_SECONDS", "20"))
        self.max_endpoints = int(os.getenv("LLM_MAX_ENDPOINTS", "40"))

    def enhance_endpoints(self, endpoints: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        if not endpoints:
            return endpoints, self._summary(mode="none", enhanced=0, message="No endpoints to enhance.")

        endpoints = [dict(endpoint) for endpoint in endpoints]
        for endpoint in endpoints:
            self._apply_rule_based_description(endpoint)

        # Validate and remove synthetic content
        endpoints = [ProvenanceValidator.validate_and_clean(ep) for ep in endpoints]

        if not self.enabled:
            return endpoints, self._summary(
                mode="rule_based",
                enhanced=len(endpoints),
                message="LLM enrichment disabled by configuration.",
            )

        if not self.api_key:
            return endpoints, self._summary(
                mode="rule_based",
                enhanced=len(endpoints),
                message="No OPENAI_API_KEY/LLM_API_KEY found; used deterministic summaries.",
            )

        try:
            ai_docs = self._call_llm(endpoints[: self.max_endpoints])
            applied = self._apply_llm_docs(endpoints, ai_docs)
            # Validate again after LLM enhancement
            endpoints = [ProvenanceValidator.validate_and_clean(ep) for ep in endpoints]
            return endpoints, self._summary(
                mode="llm",
                enhanced=applied,
                message=f"LLM enrichment completed with model {self.model}.",
                model=self.model,
            )
        except Exception as exc:
            return endpoints, self._summary(
                mode="rule_based",
                enhanced=len(endpoints),
                message=f"LLM enrichment failed; used deterministic summaries. Reason: {str(exc)}",
            )

    def _call_llm(self, endpoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        payload = {
            "model": self.model,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You generate concise, developer-friendly API documentation. "
                        "Return only valid JSON with an `endpoints` array. Preserve method and path exactly."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "task": "Write summary, description, request_notes, response_notes, and error_notes for each endpoint.",
                            "endpoints": [self._llm_endpoint_view(endpoint) for endpoint in endpoints],
                        },
                        ensure_ascii=True,
                    ),
                },
            ],
        }
        response = requests.post(
            self.api_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(self._strip_json_fence(content))
        return parsed.get("endpoints", []) if isinstance(parsed, dict) else []

    def _apply_llm_docs(self, endpoints: List[Dict[str, Any]], ai_docs: List[Dict[str, Any]]) -> int:
        docs_by_key = {
            (doc.get("method", "").upper(), doc.get("path", "")): doc
            for doc in ai_docs
            if isinstance(doc, dict)
        }
        applied = 0
        for endpoint in endpoints:
            key = (endpoint.get("method", "").upper(), endpoint.get("path", ""))
            doc = docs_by_key.get(key)
            if not doc:
                continue
            endpoint["summary"] = str(doc.get("summary") or endpoint.get("summary") or "")
            endpoint["description"] = str(doc.get("description") or endpoint.get("description") or "")
            endpoint["ai_notes"] = {
                "request": doc.get("request_notes") or "",
                "response": doc.get("response_notes") or "",
                "errors": doc.get("error_notes") or "",
            }
            endpoint["ai_enhanced"] = True
            applied += 1
        return applied

    def _apply_rule_based_description(self, endpoint: Dict[str, Any]):
        # Keep extraction deterministic: do not invent summaries/descriptions.
        # If not present from annotations/spec/source, leave empty and let renderers show "not_detected".
        endpoint.setdefault("ai_enhanced", False)

    def _llm_endpoint_view(self, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "method": endpoint.get("method"),
            "path": endpoint.get("path"),
            "framework": endpoint.get("framework"),
            "handler": endpoint.get("function_name"),
            "path_params": endpoint.get("path_params", []),
            "query_params": endpoint.get("query_params", []),
            "headers": endpoint.get("headers", []),
            "request_body": endpoint.get("request_body"),
            "responses": endpoint.get("responses", []),
        }

    def _resource_name(self, path: str) -> str:
        parts = [part for part in path.strip("/").split("/") if part and not part.startswith("{")]
        return parts[-1].replace("-", " ").replace("_", " ") if parts else ""

    def _strip_json_fence(self, content: str) -> str:
        content = content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            content = content.rsplit("```", 1)[0]
        return content.strip()

    def _summary(self, mode: str, enhanced: int, message: str, model: str = "") -> Dict[str, Any]:
        return {
            "enabled": self.enabled,
            "mode": mode,
            "model": model,
            "enhanced_endpoints": enhanced,
            "message": message,
        }
