Created At: 2026-05-25T09:19:19Z
Completed At: 2026-05-25T09:19:20Z
{"name":"__init__.py","sizeBytes":"66"}
{"name":"__pycache__","isDir":true}
{"name":"batch_processor.py","sizeBytes":"7651"}
{"name":"confidence_scorer.py","sizeBytes":"2317"}
{"name":"cross_file_router_resolver.py","sizeBytes":"8462"}
{"name":"django_drf_ast_extractor.py","sizeBytes":"55282"}
{"name":"endpoint_deduplicator.py","sizeBytes":"2175"}
{"name":"endpoint_normalizer.py","sizeBytes":"5803"}
{"name":"enhanced_cross_file_resolver.py","sizeBytes":"17274"}
{"name":"express_extractor.py","sizeBytes":"11624"}
{"name":"extraction_pipeline.py","sizeBytes":"11267"}
{"name":"extractor_manager.py","sizeBytes":"7228"}
{"name":"fastapi_ast_extractor.py","sizeBytes":"21909"}
{"name":"fastapi_extractor.py","sizeBytes":"4268"}
{"name":"generic_framework_extractor.py","sizeBytes":"53011"}
{"name":"global_router_registry.py","sizeBytes":"6977"}
{"name":"import_resolver.py","sizeBytes":"13290"}
{"name":"include_router_extractor.py","sizeBytes":"9173"}
{"name":"openapi_spec_extractor.py","sizeBytes":"9621"}
{"name":"route_classifier.py","sizeBytes":"11719"}
{"name":"route_resolver.py","sizeBytes":"9295"}
{"name":"router_composition_graph.py","sizeBytes":"15388"}

Summary: This directory contains 1 subdirectories and 21 files.

=== STEP ===

Created At: 2026-05-25T09:19:23Z
Completed At: 2026-05-25T09:19:24Z
{"File":"c:\\Users\\NAVEENYA\\One
if framework == "Django REST Framework":
return cls._extract_django(file_path, content)
return []

@classmethod
def _endpoint(cls, framework: str, method: str, path: str, file_path: str,
## Verification Results

### Automated Tests
Created and ran unit tests in [test_overhaul_accuracy.py](file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/tests/test_overhaul_accuracy.py):
- `test_spring_boot_extractor_overhaul`: Asserts correct Spring Boot parsing of path/query variables, class RequestMapping prefixes, and body schema parsing from Java DTOs.
- `test_express_router_cross_file_prefix_propagation`: Asserts Express cross-file router mounting prefix inheritance.
- `test_drf_nested_serializers_and_serializer_method_field`: Asserts DRF SerializerMethodField type inference and recursive schema component registration for nested serializers.
- `test_laravel_middleware_validation_and_form_requests`: Asserts Laravel FormRequest rules extraction, inline validation arrays, optional parameter path normalization, and controller constructor + group-level sanctum/api auth middleware detection.

Ran `pytest` inside the virtual environment:
```
============================== 9 passed in 0.11s ==============================
```

Ran the prototype verification matrix:
```
python tests/run_demo_matrix.py
```
Output:
- All 11 test suites of the demo matrix pass, verifying accuracy across Django, Laravel, Express, FastAPI, and Spring Boot.

if method not in {"POST", "PUT", "PATCH"}:
return {}

match = re.search(
r"@Body\(\s*(?:['\"]([^'\"]+)['\"])?\s*\)\s*([A-Za-z_][A-Za-z0-9_]*)\??\s*:\s*([^,\)\n]+)",
method_block,
re.IGNORECASE,
)
if not match:
return {}

field_name = match.group(1)
variable_name = match.group(2)
type_name = match.group(3).strip()
schema = model_index.get(type_name) or {"type": "object", "properties": {}}
if field_name:
schema["properties"][field_name] = {"type": cls._map_ts_type(type_name)}

return {
"name": field_name or variable_name,
"model": type_name or "RequestBody",
"required": "?" not in match.group(0).split(":")[0],
"schema": schema,
}

@classmethod
def _typescript_model_index(cls, content: str) -> Dict[str, Dict]:
models = {}
class_pattern = re.compile(r"class\s+([A-Za-z_][A-Za-z0-9_]*)\s*{", re.IGNORECASE)
for match in class_pattern.finditer(content):
class_name = match.group(1)
body_end = cls._find_balanced_end(content, match.end(), "{", "}")
if body_end == -1:
continue
body = content[match.end() : body_end - 1]
properties = {}
required = []
for field_match in re.finditer(
r"^\s*([A-Za-z_][A-Za-z0-9_]*)\??\s*:\s*([^;=\n]+)",
body,
re.MULTILINE,
):
field_name = field_match.group(1)
type_name = field_match.group(2).strip()
properties[field_name] = {
"type": cls._map_ts_type(type_name),
"typescript_type": type_name,
}
if "?" not in field_match.group(0).split(":", 1)[0]:
required.append(field_name)
if properties:
models[class_name] = {
"type": "object",
"model": class_name,
"required": required,
"properties": properties,
}
return models

@classmethod
def _nestjs_responses(cls, method_block: str, method: str) -> List[Dict]:
responses = []
seen = set()
status_match = re.search(r"@HttpCode\(\s*(\d{3})\s*\)", method_block)
success_code = int(status_match.group(1)) if status_match else cls._default_success_code(method)
responses.append({"status_code": success_code, "description": "Success"})
seen.add(success_code)

for match in re.finditer(
r"throw\s+new\s+([A-Za-z]+Exception)\(\s*(?:['\"]([^'\"]+)['\"]|{[^}]*message\s*:\s*['\"]([^'\"]+)['\"])?",
method_block,
):
exception_name = match.group(1)
status_code = cl

@staticmethod
def _default_success_code(method: str) -> int:
if method == "POST":
return 201
if method == "DELETE":
return 200
return 200

@classmethod
def _path_params(cls, path: str) -> List[Dict]:
return [
{"name": name, "type": "string", "required": True}
for name in re.findall(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", cls._normalize_path(path))
]

@staticmethod
def _map_ts_type(type_name: str) -> str:
normalized = (type_name or "").lower()
if "number" in normalized or "int" in normalized:
return "number"
if "boolean" in normalized or "bool" in normalized:
return "boolean"
if "[]" in normalized or "array" in normalized:
return "array"
if "object" in normalized or "dto" in normalized or "record" in normalized:
return "object"
return "string"

@staticmethod
def _find_balanced_end(content: str, start_index: int, open_char: str, close_char: str) -> int:
depth = 1
quote = ""
escaped = False
for idx in range(start_index, len(content)):
char = content[idx]
if quote:
if escaped:
escaped = False
elif char == "\\":
escaped = True
elif char == quote:
quote = ""
continue
if char in {"'", '"', "`"}:
quote = char
elif char == open_char:
depth += 1
elif char == close_char:
depth -= 1
if depth == 0:
return idx + 1
return -1

@classmethod
@classmethod
endpoints = []
class_prefix = cls._first_match(
content,
r"@RequestMapping\(\s*(?:value\s*=\s*)?['\"]([^'\"]*)['\"]",
) or ""
model_index = cls._java_model_index(content)
mapping_pattern = re.compile(
r"@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping)(?:\(\s*(?:value\s*=\s*)?['\"]?([^'\"),]*)['\"]?(?P<args>[^)]*)\))?",
re.IGNORECASE,
)
method_map = {
"GetMapping": "GET",
"PostMapping": "POST",
"PutMapping": "PUT",
"DeleteMapping": "DELETE",
"PatchMapping": "PATCH",
}
for match in mapping_pattern.finditer(content):
annotation = match.group(1)
method = method_map.get(annotation, cls._extract_spring_request_method(match.group("args") or "") or "GET")
path = cls._join_paths(class_prefix, match.group(2) or "")
method_block = cls._extract_java_method_block(content, match.end())
endpoint = cls._endpoint("Spring Boot", method, path, file_path, match.group(0))
endpoint["confidence"] = 0.78
endpoint.update(cls._spring_request_metadata(method_block, endpoint["path"], method, model_index))
responses = cls._spring_response
responses = cls._spring_responses(method_block, method, match.group(0), content[max(0, match.start() - 150):match.start()])
if responses:
endpoint["responses"] = responses
success = next((response for response in responses if 200 <= response["status_code"] < 300), None)
if success:
endpoint["status_code"] = success["status_code"]

if method_is_protected:
if "responses" not in endpoint:
endpoint["responses"] = []
# Avoid duplicate status codes
statuses = {resp["status_code"] for resp in endpoint["responses"]}
if 401 not in statuses:
endpoint["responses"].append({"status_code": 401, "description": "Unauthorized"})
if 403 not in statuses:
endpoint["responses"].append({"status_code": 403, "description": "Forbidden"})
endpoint["security"] = [{"tokenAuth": []}, {"jwtAuth": []}]

endpoints.append(endpoint)
return endpoints

required = []
record_fields = match.group("record")
if record_fields:
for raw_field in record_fields.split(","):
parts = raw_field.strip().split()
if len(parts) >= 2:
type_name, field_name = parts[-2], parts[-1]
properties[field_name] = {"type": cls._map_java_type(type_name), "java_type": type_name}
required.append(field_name)
body_end = cls._find_balanced_end(content, match.end(), "{", "}")
if body_end != -1:
body = content[match.end() : body_end - 1]
for field_match in re.finditer(
r"(?:private|public|protected)?\s+([A-Za-z0-9_<>, ?]+)\s+([A-Za-z_][A-Za-z0-9_]*)\s*;",
body,
):
type_name = field_match.group(1).strip()
field_name = field_match.group(2)
if field_name not in properties:
properties[field_name] = {"type": cls._map_java_type(type_name), "java_type": type_name}
required.append(field_name)
if properties:
models[class_name] = {
"type": "object",
"model": class_name,
"required": required,
"properties": properties,
}
return models

@staticmethod
def _map_java_type(type_name: str) -> str:
normalized = (type_name or "").lower()
if any(token in normalized for token in ["int", "long", "integer"]):
return "integer"
paren_end = cls._find_balanced_end(args_content, 6, "(", ")")
if paren_end != -1:
methods_list = cls._extract_php_string_list(args_content[:paren_end])
rem = args_content[paren_end:].strip()
else:
path_match = re.search(r"['\"]([^'\"]+)['\"]", args_content)
if path_match:
methods_list = [path_match.group(1)]
rem = args_content[path_match.end():].strip()

rem = rem.lstrip(",").strip()
comma_idx = rem.find(",")
if comma_idx == -1:
continue
if any(token in normalized for token in ["map", "object", "dto", "request"]):
return "object"
return "string"

@classmethod
def _extract_laravel(cls, file_path: str, content: str, cross_file_resolver=None) -> List[Dict]:
content = cls._strip_php_comments(content)
return cls._extract_laravel_routes_from_content(file_path, content, "", cross_file_resolver, False)

@classmethod
def _extract_laravel_routes_from_content(
cls,
file_path: str,
content: str,
prefix: str,
cross_file_resolver=None,
is_group_protected: bool = False,
group_auth: Optional[List[str]] = None,
) -> List[Dict]:
endpoints = []
group_ranges = []
group_auth = group_auth or []

for group_prefix, group_is_protected, group_mechanisms, body, start, end in cls._laravel_groups(content):
group_ranges.append((start, end))
endpoints.extend(
cls._extract_laravel_routes_from_content(
file_path,
body,
cls._join_paths(prefix, group_prefix),
cross_file_resolver,
is_group_protected or group_is_protected,
sorted(set(group_auth + group_mechanisms)),
)
)
content_without_groups = cls._remove_ranges(content, group_ranges)
endpoints.extend(
cls._extract_laravel_dingo_routes_from_content(
file_path,
content_without_groups,
prefix,
cross_file_resolver,
is_group_protected,
group_auth,
)
)

route_pattern = re.compile(
r"Route::(?:[A-Za-z0-9_]+\s*\([^;{}]*\)\s*->\s*)*(get|post|put|delete|patch|options|any|match)\s*\(",
re.IGNORECASE
)

for match in route_pattern.finditer(content_without_groups):
verb = match.group(1).lower()
args_start = match.end()
args_end = cls._find_balanced_end(content_without_groups, args_start, "(", ")")
if args_end == -1:
continue

args_content = content_without_groups[args_start : args_end - 1].strip()

is_protected = cls._is_route_individually_protected(
content_without_groups, match.start(), args_end, is_group_protected
)
route_auth = sorted(set(group_auth + cls._laravel_auth_mechanisms(content_without_groups[match.start():args_end])))

if verb == "match":
methods_list = []
rem = args_content
if args_content.startswith("["):
bracket_end = cls._find_balanced_end(args_content, 1, "[", "]")
if bracket_end != -1:
methods_list = cls._extract_php_string_list(args_content[:bracket_end])
rem = args_content[bracket_end:].strip()
elif args_content.lower().startswith("array("):
paren_end = cls._find_balanced_end(args_content, 6, "(", ")")
if paren_end != -1:
methods_list = cls._extract_php_string_list(args_content[:paren_end])
rem = args_content[paren_end:].strip()
else:
path_match = re.search(r"['\"]([^'\"]+)['\"]", args_content)
if path_match:
methods_list = [path_match.group(1)]
rem = args_content[path_match.end():].strip()

rem = rem.lstr
)
for match in resource_pattern.finditer(content_without_groups):
args_start = match.end()
args_end = cls._find_balanced_end(content_without_groups, args_start, "(", ")")
if args_end == -1:
continue
args_content = content_without_groups[args_start : args_end - 1].strip()

is_protected = cls._is_route_individually_protected(
content_without_groups, match.start(), args_end, is_group_protected
)
route_auth = sorted(set(group_auth + cls._laravel_auth_mechanisms(content_without_groups[match.start():args_end])))

path_quote_match = re.search(r"['\"]([^'\"]+)['\"]", args_content)
if not path_quote_match:
continue
resource_path = path_quote_match.group(1)
comma_idx = args_content.find(",", path_quote_match.end())
handler_arg = args_content[comma_idx + 1:].strip() if comma_idx != -1 else ""

controller_class = ""
class_only_match = re.search(r"['\"]([A-Za-z0-9_]+)['\"]", handler_arg)
class_ref_match = re.search(r"([A-Za-z0-9_]+)::class", handler_arg, re.IGNORECASE)
if class_only_match:
controller_class = class_only_match.group(1)
elif class_ref_match:
20:     def extract(cls, file_path: str, content: str, framework: str, cross_file_resolver=None) -> List[Dict]:
21:         if framework == "Flask":
22:             return cls._extract_flask(file_path, content)
23:         if framework == "NestJS":
24:             return cls._extract_nestjs(file_path, content)
25:         if framework == "Spring Boot":
26:             return cls._extract_spring(file_path, content)
27:         if framework == "Laravel":
28:             return cls._extract_laravel(file_path, content, cross_file_resolver)
29:         if framework == "ASP.NET Core":
30:             return cls._extract_aspnet(file_path, content)
31:         if framework == "Go Gin/Fiber":
32:             return cls._extract_go_router(file_path, content)
33:         if framework == "Django REST Framework":
34:             return cls._extract_django(file_path, content)
35:         return []
36: 
37:     @classmethod
38:     def _endpoint(cls, framework: str, method: str, path: str, file_path: str, matched_line: str) -> Dict:
39:         return {
40:             "framework": framework,
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

I will update the `extract` entry point in `generic_framework_extractor.py` to pass the `cross_file_resolver` to the Spring Boot extractor.
endpoints = []
group_auth = group_auth or []
group_ranges = []

for call_name in ("version", "group"):
pattern = re.compile(rf"\$[A-Za-z_][A-Za-z0-9_]*->{call_name}\s*\(", re.IGNORECASE)
for match in pattern.finditer(content):
args_start = match.end()
args_end = cls._find_balanced_end(content, args_start, "(", ")")
if args_end == -1:
continue
args = content[args_start : args_end - 1]
function_start = content.find("{", args_start, args_end)
if function_start == -1:
continue
function_end = cls._find_balanced_end(content, function_start + 1, "{", "}")
if function_end == -1:
continue

options = args[: max(0, args.find("function"))] if "function" in args else args
group_prefix = cls._laravel_option_value(options, "prefix") or ""
# Dingo version('v1', ...) is API metadata, not a URL prefix.
if call_name == "version":
group_prefix = cls._laravel_option_value(options, "prefix") or ""
mechanisms = cls._laravel_auth_mechanisms(options)
protected = is_group_protected or cls._is_laravel_protected(options)
body = content[function_start + 1 : function_end - 1]
group_ranges.append((match.start(), function_end))
endpoints.extend(
cls._extract_laravel_dingo_routes_from_content(
file_path,
body,
cls._join_paths(prefix, group_prefix),
cross_file_resolver,
protected,
sorted(set(group_auth + mechanisms)),
)
)

content_without_groups = cls._remove_ranges(content, group_ranges)
route_pattern = re.compile(
r"\$[A-Za-z_][A-Za-z0-9_]*->(get|post|put|delete|patch|options|any|match)\s*\(",
re.IGNORECASE,
)
for match in route_pattern.finditer(content_without_groups):
verb = match.group(1).lower()
args_start = match.end()
args_end = cls._find_balanced_end(content_without_groups, args_start, "(", ")")
if args_end == -1:
continue
"properties": properties
}
return response

@classmethod
def _resolve_laravel_details(
cls,
method: str,
path: str,
controller_class: Optional[str],
method_name: Optional[str],
closure_body: Optional[str],
cross_file_resolver
) -> Dict:
result = {}
method_block = ""

if controller_class and method_name:
controller_content = cls._find_file_content_by_name(cross_file_resolver, f"{controller_class}.php")
if controller_content:
method_block = cls._extract_php_method_block(controller_content, method_name)

signature_match = re.search(rf"function\s+{method_name}\s*\(([^)]*)\)", controller_content, re.IGNORECASE)
if signature_match:
args = signature_match.group(1)
request_type_match = re.search(r"([A-Za-z0-9_]+)\s+\$request", args, re.IGNORECASE)
if request_type_match:
request_class = request_type_match.group(1)
if request_class not in {"Request", "LaravelRequest", "FormRequest"}:
custom_request_content = cls._find_file_content_by_name(cross_file_resolver, f"{request_class}.php")
if custom_request_content:
rules_method_block = cls._extract_php_method_block(custom_request_content, "rules")
if rules_method_block:
rules = cls._parse_php_validation_rules(rules_method_block)
if rules:
if method.upper() in {"POST", "PUT", "PATCH"}:
properties = {k: {"type": v["type"]} for k, v in rules.items()}
required = [k for k, v in rules.items() if v["required"]]
result["request_body"] = {
"name": "body",
"model": request_class,
"required": True,
"schema": {
"type": "object",
"properties": properties,
"required": required
}
}
else:
result["query_params"] = [
{
"name": k,
"type": v["type"],

seen_status_codes.add(status_code)

response_pattern = re.compile(
r"\bresponse\s*\(\s*(?P<body>[^;]+?)(?:\s*,\s*(?P<status>\d{3}))?\s*\)",
re.IGNORECASE | re.DOTALL
)
for match in response_pattern.finditer(method_block):
if "->json" in method_block[max(0, match.start() - 10):match.end() + 10]:
continue
status_code = int(match.group("status")) if match.group("status") else 200
body = match.group("body")
response = cls._parse_laravel_response(status_code, body)
if status_code not in seen_status_codes:
responses.append(response)
seen_status_codes.add(status_code)

if responses:
result["responses"] = responses
success = next((r for r in responses if 200 <= r["status_code"] < 300), None)
if success:
result["status_code"] = success["status_code"]

return result

@classmethod
def _laravel_endpoint(
cls,
method: str,
path: str,
file_path: str,
matched_line: str,
controller_class: Optional[str] = None,
method_name: Optional[str] = None,
closure_body: Optional[str] = None,
cross_file_resolver = None
) -> Dict:
endpoint = cls._endpoint("Laravel", method, path, file_path, matched_line)
endpoint["confidence"] = 0.82
path_params = cls._path_params(endpoint["path"])
if path_params:
endpoint["path_params"] = path_params

details = cls._resolve_laravel_details(
method,
endpoint["path"],
controller_class,
method_name,
closure_body,
cross_file_resolver
)

if "request_body" in details:
endpoint["request_body"] = details["request_body"]
elif method in {"POST", "PUT", "PATCH"}:
endpoint["request_body"] = {
"name": "request",
"model": "LaravelRequest",
"required": method in {"POST", "PUT"},
"schema": {"type": "object", "properties": {}},
}

if "query_params" in details:
endpoint["query_params"] = details["query_params"]

if "responses" in details:
endpoint["responses"] = details["responses"]
endpoint["status_code"] = details["status_code"]
else:
endpoint["responses"] = [{"status_code": cls._default_success_code(method), "description": "Success"}]
endpoint["status_code"] = cls._default_success_code(method)

if controller_class and method_name:
endpoint["function_name"] = f"{controller_class}@
)
for method, path, method_name in definitions
]

@staticmethod
def _strip_php_comments(content: str) -> str:
content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
content = re.sub(r"^\s*//.*$", "", content, flags=re.MULTILINE)
return re.sub(r"^\s*#.*$", "", content, flags=re.MULTILINE)

@classmethod
def _laravel_prefixed_groups(cls, content: str) -> List[Tuple[str, str, int, int]]:
groups = []
pattern = re.compile(
r"Route::(?:[A-Za-z_][A-Za-z0-9_]*\s*\([^;{}]*?\)\s*->\s*)*"
r"prefix\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*->\s*group\s*\(",
re.IGNORECASE | re.DOTALL,
)
for match in pattern.finditer(content):
function_start = content.find("{", match.end())
if function_start == -1:
continue
function_end = cls._find_balanced_end(content, function_start + 1, "{", "}")
if function_end == -1:
continue
groups.append((match.group(1), content[function_start + 1 : function_end - 1], match.start(), function_end))
return groups

@staticmethod
def _remove_ranges(content: str, ranges: List[Tuple[int, int]]) -> str:
if not ranges:
return content
pieces = []
cursor = 0
for start, end in sorted(ranges):
pieces.append(content[cursor:start])
cursor = max(cursor, end)
pieces.append(content[cursor:])
return "".join(pieces)

@staticmethod
def _extract_php_string_list(content: str) -> List[str]:
return re.findall(r"['\"]([^'\"]+)['\"]", content)

@staticmethod
def _last_path_segment(path: str) -> str:
segments = [segment for segment in path.strip("/").split("/") if segment and not segment.startswith("{")]
return segments[-1] if segments else "id"

@staticmethod
def _singularize_resource(name: str) -> str:
if name.endswith("ies"):
return name[:-3] + "y"
if name.endswith("ses"):
return name[:-2]
if name.endswith("s") and len(name) > 1:
return name[:-1]
return name or "id"

@classmethod
def _extract_aspnet(cls, file_path: str, content: str) -> List[Dict]:
prefix = prefix or ""
path = path or ""
return cls._normalize_path("/".join([prefix.strip("/"), path.strip("/")]).strip("/"))

@staticmethod
def _normalize_path(path: str) -> str:
path = re.sub(r"\(\?P<([A-Za-z_][A-Za-z0-9_]*)>[^)]+\)", r"{\1}", path or "")
path = re.sub(r"\(\?P\{([A-Za-z_][A-Za-z0-9_]*)\}[^)]*\)", r"{\1}", path)
path = re.sub(r"<(?:[^:>]+:)?([^>]+)>", r"{\1}", path)
path = path.replace("\\/", "/")
path = path.replace("^", "").replace("$", "")
path = re.sub(r"/\?", "", path)
path = re.sub(r"\?/?$", "", path)
path = path.replace("<", "{").replace(">", "}")
path = re.sub(r":([A-Za-z_][A-Za-z0-9_]*)", r"{\1}", path)
path = path.replace("[controller]", "{controller}").replace("[action]", "{action}")
if not path.startswith("/"):
path = "/" + path
return re.sub(r"/+", "/", path)

return re.sub(r"^\s*#.*$", "", content, flags=re.MULTILINE)

@classmethod
def _laravel_groups(cls, content: str) -> List[Tuple[str, bool, List[str], str, int, int]]:
groups = []
pattern = re.compile(
r"Route::(?:[A-Za-z_][A-Za-z0-9_]*\s*\([^;{}]*?\)\s*->\s*)*group\s*\(",
re.IGNORECASE | re.DOTALL,
)
for match in pattern.finditer(content):
if re.match(r"Route::group\s*\(", match.group(0), re.IGNORECASE):
continue
function_start = content.find("{", match.end())
if function_start == -1:
continue
function_end = cls._find_balanced_end(content, function_start + 1, "{", "}")
if function_end == -1:
continue

chain = match.group(0)
prefix_match = re.search(r"prefix\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", chain, re.IGNORECASE)
group_prefix = prefix_match.group(1) if prefix_match else ""

is_protected = cls._is_laravel_protected(chain)
auth_mechanisms = cls._laravel_auth_mechanisms(chain)

body = content[function_start + 1 : function_end - 1]
groups.append((group_prefix, is_protected, auth_mechanisms, body, match.start(), function_end))



if args_end == -1:
continue
args = content[args_start : args_end - 1]
function_start = content.find("{", args_start, args_end)
if function_start == -1:
continue
function_end = cls._find_balanced_end(content, function_start + 1, "{", "}")
if function_end == -1:
continue
options = args[: max(0, args.find("function"))] if "function" in args else args
prefix_match = re.search(r"['\"]prefix['\"]\s*=>\s*['\"]([^'\"]+)['\"]", options, re.IGNORECASE)
middleware_match = re.search(r"['\"]middleware['\"]\s*=>\s*(?P<value>\[[^\]]+\]|array\s*\([^)]*\)|['\"][^'\"]+['\"])", options, re.IGNORECASE)
group_prefix = prefix_match.group(1) if prefix_match else ""
middleware_text = middleware_match.group("value") if middleware_match else options
is_protected = cls._is_laravel_protected(middleware_text)
auth_mechanisms = cls._laravel_auth_mechanisms(middleware_text)
body = content[function_start + 1 : function_end - 1]
if not any(start == match.start() and end == function_end for *_, start, end in groups):
groups.append((group_prefix, is_protected, auth_mechanisms, body, match.start(), function_end))
return groups

@classmethod
def _is_laravel_protected(cls, text: str) -> bool:
if not text:
return False
text_lower = text.lower()
if "middleware" in text_lower:
for term in ["auth:sanctum", "auth:api", "auth:passport", "auth:jwt", "auth", "sanctum", "passport", "jwt"]:
path = path.replace("^", "").replace("$", "")
path = re.sub(r"/\?", "", path)
path = re.sub(r"\?/?$", "", path)
path = path.replace("<", "{").replace(">", "}")
path = re.sub(r":([A-Za-z_][A-Za-z0-9_]*)", r"{\1}", path)
path = path.replace("[controller]", "{controller}").replace("[action]", "{action}")
if not path.startswith("/"):
path = "/" + path
return re.sub(r"/+", "/", path)
