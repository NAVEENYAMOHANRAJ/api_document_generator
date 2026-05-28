"""Normalize endpoints for DB storage and rehydrate for API responses."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _infer_path_params(path: str) -> List[Dict[str, Any]]:
    names = re.findall(r"\{([^}]+)\}", path or "")
    return [{"name": name, "in": "path", "required": True} for name in names]


def _handler_function_name(endpoint: Dict[str, Any]) -> Optional[str]:
    handler = endpoint.get("handler")
    if isinstance(handler, dict):
        return handler.get("method") or handler.get("function")
    return endpoint.get("function_name")


def _handler_source_file(endpoint: Dict[str, Any]) -> str:
    source = endpoint.get("source") or {}
    if isinstance(source, dict):
        return source.get("file") or source.get("route_file") or ""
    provenance = endpoint.get("provenance") or {}
    if isinstance(provenance, dict):
        return provenance.get("source_file") or ""
    return endpoint.get("source_file") or ""


def prepare_endpoint_for_storage(endpoint: Dict[str, Any]) -> Dict[str, Any]:
    """Map extractor shapes to DB fields and stash extras in provenance."""
    ep = dict(endpoint)

    path_params = ep.get("path_params") or ep.get("pathParameters") or []
    if not path_params:
        path_params = _infer_path_params(ep.get("path", ""))

    query_params = ep.get("query_params") or ep.get("queryParameters") or []
    request_body = ep.get("request_body") or ep.get("requestBody")
    responses = ep.get("responses") or []
    if isinstance(responses, dict):
        responses = [
            {"status_code": int(code) if str(code).isdigit() else code, **(body if isinstance(body, dict) else {"description": str(body)})}
            for code, body in responses.items()
        ]

    middleware = _as_list(ep.get("middleware") or ep.get("dependencies"))
    security = _as_list(ep.get("security"))
    headers = _as_list(ep.get("headers"))

    provenance = dict(ep.get("provenance") or {})
    provenance["extras"] = {
        "middleware": middleware,
        "security": security,
        "headers": headers,
        "handler": ep.get("handler"),
        "source": ep.get("source"),
        "framework": provenance.get("framework") or ep.get("framework"),
        "validation_rules": ep.get("validation_rules") or ep.get("validationRules"),
        "curl_example": ep.get("curl_example") or ep.get("curlExample"),
        "request_example": ep.get("request_example") or ep.get("requestExample"),
    }

    return {
        "method": (ep.get("method") or "GET").upper(),
        "path": ep.get("path") or "/",
        "description": ep.get("description") or ep.get("summary"),
        "source_file": _handler_source_file(ep) or ep.get("source_file") or "",
        "function_name": _handler_function_name(ep),
        "path_params": path_params,
        "query_params": query_params,
        "request_body": request_body,
        "response_model": ep.get("response_model") or ep.get("responseModel"),
        "responses": responses,
        "tags": ep.get("tags") or [],
        "deprecated": ep.get("deprecated", False),
        "confidence": ep.get("confidence"),
        "provenance": provenance,
        "headers": headers,
        "middleware": middleware,
        "security": security,
    }


def hydrate_endpoint_from_db(row: Dict[str, Any]) -> Dict[str, Any]:
    """Merge provenance extras back into endpoint payload for clients."""
    ep = dict(row)
    provenance = ep.get("provenance") or {}
    extras = {}
    if isinstance(provenance, dict):
        extras = provenance.get("extras") or {}

    for key in ("middleware", "security", "headers", "handler", "source"):
        if not ep.get(key) and extras.get(key):
            ep[key] = extras[key]

    if extras.get("framework") and not (ep.get("provenance") or {}).get("framework"):
        prov = dict(provenance) if isinstance(provenance, dict) else {}
        prov.setdefault("framework", extras["framework"])
        ep["provenance"] = prov

    if extras.get("validation_rules"):
        ep["validation_rules"] = extras["validation_rules"]
    if extras.get("curl_example"):
        ep["curl_example"] = extras["curl_example"]
    if extras.get("request_example"):
        ep["request_example"] = extras["request_example"]

    if isinstance(ep.get("source"), dict) and not ep.get("source_file"):
        ep["source_file"] = ep["source"].get("file") or ep["source"].get("route_file")

    return ep


def enrich_endpoints_from_openapi(endpoints: List[Dict[str, Any]], openapi_document: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Merge operation-level OpenAPI data back into extracted endpoints.
    This improves downstream UI coverage without inventing values.
    """
    if not openapi_document or not isinstance(openapi_document, dict):
        return endpoints

    paths = openapi_document.get("paths") or {}
    if not isinstance(paths, dict):
        return endpoints

    enriched: List[Dict[str, Any]] = []
    for endpoint in endpoints:
        ep = dict(endpoint)
        method = str(ep.get("method", "GET")).lower()
        path = str(ep.get("path", ""))
        operation = (paths.get(path) or {}).get(method) if isinstance(paths.get(path), dict) else None
        if not isinstance(operation, dict):
            enriched.append(ep)
            continue

        params = operation.get("parameters") or []
        if params and isinstance(params, list):
            if not ep.get("path_params"):
                ep["path_params"] = [p for p in params if isinstance(p, dict) and p.get("in") == "path"]
            if not ep.get("query_params"):
                ep["query_params"] = [p for p in params if isinstance(p, dict) and p.get("in") == "query"]
            if not ep.get("headers"):
                ep["headers"] = [p for p in params if isinstance(p, dict) and p.get("in") == "header"]

        if not ep.get("security") and operation.get("security"):
            ep["security"] = operation.get("security")

        if not ep.get("request_body") and operation.get("requestBody"):
            body = operation.get("requestBody")
            if isinstance(body, dict):
                content = body.get("content") or {}
                app_json = content.get("application/json") if isinstance(content, dict) else {}
                ep["request_body"] = {
                    "required": bool(body.get("required")),
                    "schema": (app_json or {}).get("schema"),
                    "example": (app_json or {}).get("example"),
                }

        if not ep.get("responses") and operation.get("responses"):
            responses = []
            op_responses = operation.get("responses") or {}
            if isinstance(op_responses, dict):
                for code, value in op_responses.items():
                    if not isinstance(value, dict):
                        continue
                    content = value.get("content") or {}
                    app_json = content.get("application/json") if isinstance(content, dict) else {}
                    responses.append(
                        {
                            "status_code": int(code) if str(code).isdigit() else code,
                            "description": value.get("description"),
                            "schema": (app_json or {}).get("schema"),
                            "example": (app_json or {}).get("example"),
                        }
                    )
            if responses:
                ep["responses"] = responses

        if operation.get("x-pagination") and not ep.get("pagination"):
            ep["pagination"] = operation.get("x-pagination")

        if operation.get("x-curl-example") and not ep.get("curl_example"):
            ep["curl_example"] = operation.get("x-curl-example")

        enriched.append(ep)

    return enriched
