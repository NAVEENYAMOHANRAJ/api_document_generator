import re
import hashlib
import json
from typing import Any, Dict, List, Optional

from api_doc_generator.generators.documentation_generator import DocumentationGenerator


class OpenAPIGenerator:
    """Generate a lightweight OpenAPI 3.1.0 document from extracted endpoints."""

    @staticmethod
    def _hash_schema(schema: Any) -> str:
        """Compute a deterministic hash for a schema object to identify duplicate schemas."""
        try:
            serialized = json.dumps(schema, sort_keys=True)
            return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        except Exception:
            return str(hash(str(schema)))

    @staticmethod
    def generate(endpoints: List[Dict[str, Any]], title: str = "Generated API Docs") -> Dict[str, Any]:
        paths: Dict[str, Dict[str, Any]] = {}
        
        processed_endpoints = []
        for ep in endpoints:
            new_ep = dict(ep)
            if "request_body" in new_ep and isinstance(new_ep["request_body"], dict):
                new_ep["request_body"] = dict(new_ep["request_body"])
            if "responses" in new_ep and isinstance(new_ep["responses"], list):
                new_ep["responses"] = [dict(resp) for resp in new_ep["responses"] if isinstance(resp, dict)]
            processed_endpoints.append(new_ep)
        endpoints = processed_endpoints

        for ep in endpoints:
            path = OpenAPIGenerator._normalize_openapi_path(ep.get("path", "/"))
            tag = OpenAPIGenerator._tag_for_path(path, ep)
            tag = re.sub(r'[^a-zA-Z0-9_]', '', tag)
            if not tag:
                tag = "Default"
            method = str(ep.get("method", "GET")).upper()
            
            path_clean = re.sub(r'\{[^}]+\}', '', path)
            parts = [p for p in path_clean.split('/') if p]
            generic = {"api", "v1", "v2", "v3", tag.lower()}
            parts = [p for p in parts if p.lower() not in generic]
            parts = [re.sub(r'[^a-zA-Z0-9_]', '', p) for p in parts]
            path_desc = "".join(p.title() for p in parts if p)
            
            # Do not synthesize request/response model names.
            # If model names are not detected from source, schemas will remain inline or omitted.

        schemas = OpenAPIGenerator._build_components(endpoints)
        
        # Schema hashing deduplication
        schema_hashes = {}
        dedup_map = {}
        for key in list(schemas.keys()):
            sch = schemas[key]
            h = OpenAPIGenerator._hash_schema(sch)
            suffix = "Request" if key.endswith("Request") else "Response" if key.endswith("Response") else ""
            h_key = f"{h}_{suffix}"
            if h_key in schema_hashes:
                # Map this duplicate schema to the existing one
                dedup_map[key] = schema_hashes[h_key]
            else:
                schema_hashes[h_key] = key

        # Resolve nested schemas and components
        for key in list(schemas.keys()):
            if key in dedup_map:
                del schemas[key]
                continue
            suffix = "Request" if key.endswith("Request") else "Response"
            schemas[key] = OpenAPIGenerator._resolve_nested_serializers_in_schema(schemas[key], suffix)
            
        schema_reuse_count = len(dedup_map)

        sorted_endpoints = OpenAPIGenerator._sort_endpoints(endpoints)
        for endpoint in sorted_endpoints:
            raw_path = endpoint.get("path")
            if not raw_path:
                continue
            path = OpenAPIGenerator._normalize_openapi_path(raw_path)
            method = endpoint.get("method", "").lower()
            if not method:
                continue
            if method.upper() not in {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"}:
                continue

            paths.setdefault(path, {})
            operation: Dict[str, Any] = {
                "operationId": OpenAPIGenerator._operation_id(endpoint),
                "tags": [OpenAPIGenerator._tag_for_path(path, endpoint)],
                "summary": endpoint.get("summary") or "",
                "description": endpoint.get("description") or "",
                "x-source-file": endpoint.get("source_file"),
                "x-source-route": endpoint.get("x-source-route") or endpoint.get("source_file"),
                "x-source-view": endpoint.get("x-source-view"),
                "x-source-serializer": endpoint.get("x-source-serializer"),
                "x-source-model": endpoint.get("x-source-model"),
                "x-framework-confidence": endpoint.get("x-framework-confidence") or endpoint.get("confidence_score"),
                "parameters": OpenAPIGenerator._build_parameters(endpoint),
                "responses": OpenAPIGenerator._build_responses(endpoint),
            }
            security = OpenAPIGenerator._build_security(endpoint)
            if security:
                operation["security"] = security
            if endpoint.get("ai_notes"):
                operation["x-ai-notes"] = endpoint["ai_notes"]

            request_body = OpenAPIGenerator._build_request_body(endpoint)
            if request_body:
                operation["requestBody"] = request_body
                operation["x-curl-example"] = DocumentationGenerator._curl_example(endpoint)
            else:
                operation["x-curl-example"] = DocumentationGenerator._curl_example(endpoint)

            pagination = OpenAPIGenerator._detect_pagination(endpoint)
            if pagination:
                operation["x-pagination"] = pagination

            schema_reuse_count += OpenAPIGenerator._replace_operation_schemas_with_refs(operation, endpoint, schemas, dedup_map)

            if operation.get("requestBody"):
                content = operation["requestBody"].get("content", {})
                for media_type, media_obj in content.items():
                    if "schema" in media_obj:
                        media_obj["schema"] = OpenAPIGenerator._resolve_nested_serializers_in_schema(media_obj["schema"], "Request")
            
            for status, resp_obj in operation.get("responses", {}).items():
                content = resp_obj.get("content", {})
                for media_type, media_obj in content.items():
                    if "schema" in media_obj:
                        media_obj["schema"] = OpenAPIGenerator._resolve_nested_serializers_in_schema(media_obj["schema"], "Response")

            paths[path][method] = operation

        components: Dict[str, Any] = {"schemas": schemas}
        security_schemes = OpenAPIGenerator._security_schemes(endpoints)
        if security_schemes:
            components["securitySchemes"] = security_schemes

        document = {
            "openapi": "3.1.0",
            "info": {
                "title": title,
                "version": "1.0.0",
            },
            "tags": [{"name": tag} for tag in sorted({OpenAPIGenerator._tag_for_path(OpenAPIGenerator._normalize_openapi_path(endpoint.get("path", "/")), endpoint) for endpoint in sorted_endpoints})],
            "components": components,
            "x-schema-reuse-count": schema_reuse_count,
            "paths": paths,
        }
        document["x-openapi-validation"] = OpenAPIGenerator._validate_document(document)
        return document

    @staticmethod
    def _detect_pagination(endpoint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Infer pagination scheme based on framework/parameters."""
        path = endpoint.get("path", "").lower()
        method = endpoint.get("method", "GET").upper()
        if method != "GET":
            return None
            
        params = {p.get("name") for p in endpoint.get("query_params", []) or []}
        if "limit" in params and "offset" in params:
            return {"type": "limit_offset", "parameters": ["limit", "offset"]}
        if "page" in params:
            return {"type": "page_number", "parameters": ["page"]}
        if "cursor" in params:
            return {"type": "cursor", "parameters": ["cursor"]}
        
        # Check defaults for DRF / Laravel collections
        if endpoint.get("framework") == "Django REST Framework" and any(p in path for p in ["list", "snippets", "users"]):
            return {"type": "limit_offset", "parameters": ["limit", "offset"]}
        return None

    @staticmethod
    def _build_parameters(endpoint: Dict[str, Any]) -> List[Dict[str, Any]]:
        parameters = []

        for param in endpoint.get("path_params", []) or []:
            parameters.append(OpenAPIGenerator._parameter(param, "path", required=True))

        for param in endpoint.get("query_params", []) or []:
            parameters.append(OpenAPIGenerator._parameter(param, "query"))

        for param in endpoint.get("headers", []) or []:
            parameters.append(OpenAPIGenerator._parameter(param, "header"))

        return parameters

    @staticmethod
    def _parameter(param: Dict[str, Any], location: str, required: bool = False) -> Dict[str, Any]:
        schema = {
            key: value
            for key, value in param.items()
            if key in {"type", "format", "minimum", "maximum", "pattern", "enum", "nullable"}
        }
        name = param.get("name") or ""
        name = name.replace("?", "").split(":")[0]
        return {
            "name": name,
            "in": location,
            "required": required or bool(param.get("required")),
            "schema": schema or {"type": "string"},
        }

    @staticmethod
    def _build_request_body(endpoint: Dict[str, Any]) -> Dict[str, Any]:
        request_body = endpoint.get("request_body")
        if not request_body:
            return {}

        schema = request_body.get("schema") or {"type": "object"}
        body: Dict[str, Any] = {
            "required": bool(request_body.get("required")),
            "content": {
                "application/json": {
                    "schema": schema,
                }
            },
        }
        example = DocumentationGenerator._sample_from_schema(schema)
        if example is not None:
            body["content"]["application/json"]["example"] = example
        return body

    @staticmethod
    def _build_responses(endpoint: Dict[str, Any]) -> Dict[str, Any]:
        responses = {}

        for response in endpoint.get("responses", []) or []:
            status_code = str(response.get("status_code") or 200)
            response_obj: Dict[str, Any] = {
                "description": response.get("description") or "Response",
            }
            if status_code == "204":
                responses[status_code] = response_obj
                continue
            schema = response.get("schema")
            if schema:
                example = DocumentationGenerator._sample_from_schema(schema)
                response_obj["content"] = {
                    "application/json": {
                        "schema": schema,
                    }
                }
                if example is not None:
                    response_obj["content"]["application/json"]["example"] = example
            responses[status_code] = response_obj

        if not responses:
            # OpenAPI requires at least one response object per operation; avoid fabricated schemas/examples.
            responses["200"] = {"description": "Response (schema not detected in source code)"}

        return responses

    @staticmethod
    def _build_components(endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
        schemas: Dict[str, Any] = {}
        all_drf_serializers = {}
        
        for endpoint in endpoints:
            if "x-serializers" in endpoint:
                all_drf_serializers.update(endpoint["x-serializers"])
                
            request_body = endpoint.get("request_body") or {}
            model = request_body.get("model")
            if model and request_body.get("schema"):
                schemas[OpenAPIGenerator._component_key(str(model), "Request")] = request_body["schema"]
            for response in endpoint.get("responses", []) or []:
                model = response.get("model")
                schema = response.get("schema")
                if model and schema:
                    if schema.get("type") == "array" and schema.get("items"):
                        schemas[OpenAPIGenerator._component_key(str(model), "Response")] = schema["items"]
                    else:
                        schemas[OpenAPIGenerator._component_key(str(model), "Response")] = schema
                        
        referenced_resolved = set()
        # Prevent infinite loops due to circular references
        loop_counter = 0
        while loop_counter < 100:
            referenced = set()
            for schema in schemas.values():
                referenced.update(OpenAPIGenerator._find_referenced_serializer_names(schema))
                
            new_refs = referenced - referenced_resolved
            if not new_refs:
                break
                
            for ref_name in new_refs:
                s_info = all_drf_serializers.get(ref_name) or all_drf_serializers.get(ref_name.split(".")[-1])
                if s_info:
                    req_key = OpenAPIGenerator._component_key(ref_name, "Request")
                    resp_key = OpenAPIGenerator._component_key(ref_name, "Response")
                    if "request_schema" in s_info:
                        schemas[req_key] = s_info["request_schema"]
                    elif "schema" in s_info:
                        schemas[req_key] = s_info["schema"]
                        
                    if "response_schema" in s_info:
                        schemas[resp_key] = s_info["response_schema"]
                    elif "schema" in s_info:
                        schemas[resp_key] = s_info["schema"]
                referenced_resolved.add(ref_name)
            loop_counter += 1
                
        return schemas

    @staticmethod
    def _replace_operation_schemas_with_refs(
        operation: Dict[str, Any],
        endpoint: Dict[str, Any],
        schemas: Dict[str, Any],
        dedup_map: Dict[str, str],
    ) -> int:
        count = 0
        request_body = endpoint.get("request_body") or {}
        request_model = request_body.get("model")
        if request_model:
            req_key = OpenAPIGenerator._component_key(str(request_model), "Request")
            # Apply deduplication lookup
            resolved_key = dedup_map.get(req_key, req_key)
            if resolved_key in schemas and operation.get("requestBody"):
                operation["requestBody"]["content"]["application/json"]["schema"] = {"$ref": f"#/components/schemas/{resolved_key}"}
                count += 1

        responses_by_status = operation.get("responses") or {}
        for response in endpoint.get("responses", []) or []:
            model = response.get("model")
            status = str(response.get("status_code") or 200)
            if not model or status not in responses_by_status:
                continue
            resp_key = OpenAPIGenerator._component_key(str(model), "Response")
            resolved_key = dedup_map.get(resp_key, resp_key)
            if resolved_key not in schemas:
                continue
            content = responses_by_status[status].get("content")
            if not content:
                continue
            schema = response.get("schema") or {}
            if schema.get("type") == "array":
                content["application/json"]["schema"] = {
                    "type": "array",
                    "items": {"$ref": f"#/components/schemas/{resolved_key}"},
                }
            else:
                content["application/json"]["schema"] = {"$ref": f"#/components/schemas/{resolved_key}"}
            count += 1
        return count

    @staticmethod
    def _schema_ref(model: str, suffix: str = "") -> Dict[str, str]:
        return {"$ref": f"#/components/schemas/{OpenAPIGenerator._component_key(model, suffix)}"}

    @staticmethod
    def _component_key(model: str, suffix: str = "") -> str:
        base = model.replace(".", "_")
        if base.endswith("Serializer"):
            base = base[: -len("Serializer")]
        return f"{base}{suffix}" if suffix else base

    @staticmethod
    def _sort_endpoints(endpoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        method_order = {"GET": 0, "POST": 1, "PUT": 2, "PATCH": 3, "DELETE": 4}
        return sorted(
            endpoints,
            key=lambda endpoint: (
                OpenAPIGenerator._resource_key(OpenAPIGenerator._normalize_openapi_path(str(endpoint.get("path", "/")))),
                method_order.get(str(endpoint.get("method", "GET")).upper(), 99),
                OpenAPIGenerator._normalize_openapi_path(str(endpoint.get("path", "/"))),
            ),
        )

    @staticmethod
    def _resource_key(path: str) -> str:
        return "/".join(part for part in path.split("/") if part and not part.startswith("{"))

    @staticmethod
    def _tag_for_path(path: str, endpoint: Dict[str, Any] | None = None) -> str:
        if endpoint:
            model = OpenAPIGenerator._model_resource(endpoint)
            if model:
                return model
        path = OpenAPIGenerator._normalize_openapi_path(path)
        generic = {"api", "v1", "v2", "v3"}
        first = next((part for part in str(path).split("/") if part and not part.startswith("{") and part.lower() not in generic), "Default")
        return first.replace("-", " ").replace("_", " ").title().replace(" ", "")

    @staticmethod
    def _operation_id(endpoint: Dict[str, Any]) -> str:
        method = str(endpoint.get("method", "GET")).upper()
        path = OpenAPIGenerator._normalize_openapi_path(str(endpoint.get("path", "/")))
        resource = OpenAPIGenerator._tag_for_path(path, endpoint)
        singular = resource[:-1] if resource.endswith("s") and len(resource) > 1 else resource
        has_id = "{" in path
        tail = next((part for part in reversed(path.split("/")) if part and not part.startswith("{")), "")
        drf_action = str(endpoint.get("x-drf-action") or "")
        standard_actions = {"list", "retrieve", "create", "update", "partial_update", "destroy"}
        if drf_action and drf_action not in standard_actions:
            return f"{OpenAPIGenerator._camel(drf_action)}{singular}"
        custom_action = tail and tail.lower() not in {"api", resource.lower(), singular.lower()} and has_id
        action_map = {
            ("GET", False): "list",
            ("POST", False): "create",
            ("GET", True): "retrieve",
            ("PUT", True): "update",
            ("PATCH", True): "partialUpdate",
            ("DELETE", True): "delete",
        }
        if custom_action:
            verb = OpenAPIGenerator._camel(tail)
        else:
            verb = action_map.get((method, has_id), method.lower())
        return f"{OpenAPIGenerator._camel(verb)}{singular if verb not in {'list'} else resource}"

    @staticmethod
    def _model_resource(endpoint: Dict[str, Any]) -> str:
        request_model = (endpoint.get("request_body") or {}).get("model")
        response_model = next((response.get("model") for response in endpoint.get("responses", []) or [] if response.get("model")), "")
        model = str(request_model or response_model or "")
        for suffix in ("Serializer", "Request", "Response"):
            if model.endswith(suffix):
                model = model[: -len(suffix)]
        return model

    @staticmethod
    def _camel(value: str) -> str:
        parts = [part for part in value.replace("_", "-").split("-") if part]
        if not parts:
            return value
        return parts[0].lower() + "".join(part[:1].upper() + part[1:] for part in parts[1:])

    @staticmethod
    def _security_schemes(endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
        referenced_schemes = set()
        for endpoint in endpoints:
            sec_reqs = OpenAPIGenerator._build_security(endpoint)
            for req in sec_reqs:
                for scheme_key in req.keys():
                    referenced_schemes.add(scheme_key)
                    
        schemes: Dict[str, Any] = {}
        if "basicAuth" in referenced_schemes:
            schemes["basicAuth"] = {"type": "http", "scheme": "basic"}
        if "sessionAuth" in referenced_schemes:
            schemes["sessionAuth"] = {"type": "apiKey", "in": "cookie", "name": "sessionid"}
        if "tokenAuth" in referenced_schemes:
            schemes["tokenAuth"] = {"type": "apiKey", "in": "header", "name": "Authorization"}
        if "jwtAuth" in referenced_schemes:
            schemes["jwtAuth"] = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        if "sanctumAuth" in referenced_schemes:
            schemes["sanctumAuth"] = {"type": "apiKey", "in": "header", "name": "Authorization"}
        if "oauth2Auth" in referenced_schemes:
            schemes["oauth2Auth"] = {"type": "oauth2", "flows": {}}
        if "apiKeyAuth" in referenced_schemes:
            schemes["apiKeyAuth"] = {"type": "apiKey", "in": "header", "name": "Authorization"}
            
        for ref in referenced_schemes:
            if ref not in schemes:
                schemes[ref] = {"type": "apiKey", "in": "header", "name": "Authorization"}
                
        return schemes

    @staticmethod
    def _build_security(endpoint: Dict[str, Any]) -> List[Dict[str, List[str]]]:
        if endpoint.get("security"):
            return endpoint["security"]

        auth_classes = [auth.split(".")[-1] for auth in endpoint.get("x-authentication") or []]
        security = []
        for auth in auth_classes:
            if "BasicAuthentication" in auth:
                security.append({"basicAuth": []})
            elif "SessionAuthentication" in auth:
                security.append({"sessionAuth": []})
            elif "TokenAuthentication" in auth:
                security.append({"tokenAuth": []})
            elif "JWT" in auth or "SimpleJWT" in auth:
                security.append({"jwtAuth": []})
            elif "Laravel Sanctum" in auth:
                security.append({"sanctumAuth": []})
            elif "Laravel Passport" in auth:
                security.append({"oauth2Auth": []})
            elif "Laravel API Token" in auth or "Laravel auth middleware" in auth:
                security.append({"apiKeyAuth": []})
                
        return security

    @staticmethod
    def _validate_document(document: Dict[str, Any]) -> Dict[str, Any]:
        errors = []
        valid_methods = {"get", "post", "put", "patch", "delete", "options", "head"}
        schemas = set(((document.get("components") or {}).get("schemas") or {}).keys())
        for path, path_item in (document.get("paths") or {}).items():
            if any(token in path for token in ("(?P", "\\w", "\\d", "[^", "/?")):
                errors.append({"path": path, "reason": "Path contains raw regex syntax"})
            for method, operation in path_item.items():
                if method not in valid_methods:
                    errors.append({"path": path, "method": method, "reason": "Invalid HTTP method"})
                for ref in OpenAPIGenerator._iter_refs(operation):
                    key = ref.rsplit("/", 1)[-1]
                    if key not in schemas:
                        errors.append({"path": path, "method": method, "reason": f"Missing schema ref {ref}"})
        return {"valid": not errors, "errors": errors}

    @staticmethod
    def _iter_refs(value: Any):
        if isinstance(value, dict):
            ref = value.get("$ref")
            if ref:
                yield ref
            for child in value.values():
                yield from OpenAPIGenerator._iter_refs(child)
        elif isinstance(value, list):
            for child in value:
                yield from OpenAPIGenerator._iter_refs(child)

    @staticmethod
    def _normalize_openapi_path(path: str) -> str:
        if not path:
            return "/"
        if not path.startswith("/"):
            path = "/" + path
        if path != "/" and path.endswith("/"):
            path = path[:-1]
        path = re.sub(r"\{([A-Za-z0-9_]+)\?\}", r"{\1}", path)
        path = re.sub(r"\{([A-Za-z0-9_]+):[^}]+\}", r"{\1}", path)
        path = re.sub(r"/+", "/", path)
        return path

    @staticmethod
    def _find_referenced_serializer_names(schema: Any) -> List[str]:
        names = []
        if isinstance(schema, dict):
            if "x-nested-serializer" in schema:
                names.append(schema["x-nested-serializer"])
            for val in schema.values():
                names.extend(OpenAPIGenerator._find_referenced_serializer_names(val))
        elif isinstance(schema, list):
            for item in schema:
                names.extend(OpenAPIGenerator._find_referenced_serializer_names(item))
        return names

    @staticmethod
    def _resolve_nested_serializers_in_schema(schema: Any, suffix: str) -> Any:
        if isinstance(schema, dict):
            if "x-nested-serializer" in schema:
                nested_name = schema["x-nested-serializer"]
                ref_key = OpenAPIGenerator._component_key(nested_name, suffix)
                return {"$ref": f"#/components/schemas/{ref_key}"}
            new_dict = {}
            for k, v in schema.items():
                new_dict[k] = OpenAPIGenerator._resolve_nested_serializers_in_schema(v, suffix)
            return new_dict
        elif isinstance(schema, list):
            return [OpenAPIGenerator._resolve_nested_serializers_in_schema(item, suffix) for item in schema]
        return schema
