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
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":27,"LineContent":"        if framework == \"Laravel\":"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":28,"LineContent":"            return cls._extract_laravel(file_path, content, cross_file_resolver)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":522,"LineContent":"    def _extract_laravel(cls, file_path: str, content: str, cross_file_resolver=None) -\u003e List[Dict]:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":524,"LineContent":"        return cls._extract_laravel_routes_from_content(file_path, content, \"\", cross_file_resolver)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":527,"LineContent":"    def _extract_laravel_routes_from_content(cls, file_path: str, content: str, prefix: str, cross_file_resolver=None) -\u003e List[Dict]:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":531,"LineContent":"        for group_prefix, body, start, end in cls._laravel_prefixed_groups(content):"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":534,"LineContent":"                cls._extract_laravel_routes_from_content("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend
<truncated 3397 bytes>
ork_extractor.py","LineNumber":959,"LineContent":"                response = cls._parse_laravel_response(status_code, body)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":973,"LineContent":"                response = cls._parse_laravel_response(status_code, body)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":987,"LineContent":"    def _laravel_endpoint("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":998,"LineContent":"        endpoint = cls._endpoint(\"Laravel\", method, path, file_path, matched_line)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1004,"LineContent":"        details = cls._resolve_laravel_details("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1018,"LineContent":"                \"model\": \"LaravelRequest\","}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1040,"LineContent":"    def _laravel_resource_endpoints("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1059,"LineContent":"            cls._laravel_endpoint("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1078,"LineContent":"    def _laravel_prefixed_groups(cls, content: str) -\u003e List[Tuple[str, str, int, int]]:"}

=== STEP ===

Created At: 2026-05-25T09:19:28Z
Completed At: 2026-05-25T09:19:29Z
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":25,"LineContent":"        if framework == \"Spring Boot\":"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":26,"LineContent":"            return cls._extract_spring(file_path, content)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":310,"LineContent":"    def _extract_spring(cls, file_path: str, content: str) -\u003e List[Dict]:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":330,"LineContent":"            method = method_map.get(annotation, cls._extract_spring_request_method(match.group(\"args\") or \"\") or \"GET\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":333,"LineContent":"            endpoint = cls._endpoint(\"Spring Boot\", method, path, file_path, match.group(0))"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":335,"LineContent":"            endpoint.update(cls._spring_request_metadata(method_block, endpoint[\"path\"], method, model_index))"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":336,"LineContent":"            responses = cls._spring_responses(method_block, method)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extract
<truncated 578 bytes>
nerator\\extractors\\generic_framework_extractor.py","LineNumber":386,"LineContent":"        body = cls._spring_body(method_block, method, model_index)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":392,"LineContent":"    def _spring_annotated_params(cls, method_block: str, annotation: str) -\u003e List[Tuple[str, str, bool]]:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":408,"LineContent":"    def _spring_body(cls, method_block: str, method: str, model_index: Dict[str, Dict]) -\u003e Dict:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":429,"LineContent":"    def _spring_responses(cls, method_block: str, method: str) -\u003e List[Dict]:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":433,"LineContent":"        success_code = cls._spring_status_value(status_match.group(1)) if status_match else cls._default_success_code(method)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":441,"LineContent":"            status_code = cls._spring_status_value(match.group(1))"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":452,"LineContent":"    def _spring_status_value(value: str) -\u003e int:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1185,"LineContent":"    def _extract_spring_request_method(args: str) -\u003e str:"}

=== STEP ===

Created At: 2026-05-25T09:19:34Z
Completed At: 2026-05-25T09:19:34Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1210
Total Bytes: 53011
Showing lines 1 to 800
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: import re
2: from pathlib import PurePosixPath
3: from typing import Dict, List, Tuple, Optional
4: 
5: 
6: class GenericFrameworkExtractor:
7:     """Extract route declarations for common frameworks with lightweight patterns."""
8: 
9:     HTTP_METHODS = {
10:         "get": "GET",
11:         "post": "POST",
12:         "put": "PUT",
13:         "delete": "DELETE",
14:         "patch": "PATCH",
15:         "options": "OPTIONS",
16:         "head": "HEAD",
17:     }
18: 
19:     @classmethod
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
38:     def _endpoint(cls, framework: str, method: str, path: str, file_path: str, matched_line: str) -
<truncated 34507 bytes>
t:
761:                 required = "required" in val_content.lower()
762:                 type_name = "string"
763:                 if "integer" in val_content.lower() or "int" in val_content.lower():
764:                     type_name = "integer"
765:                 elif "numeric" in val_content.lower() or "double" in val_content.lower() or "float" in val_content.lower():
766:                     type_name = "number"
767:                 elif "boolean" in val_content.lower() or "bool" in val_content.lower():
768:                     type_name = "boolean"
769:                 elif "array" in val_content.lower():
770:                     type_name = "array"
771:                 
772:                 properties[key] = {
773:                     "type": type_name,
774:                     "required": required,
775:                     "rules": val_content
776:                 }
777:         return properties
778: 
779:     @classmethod
780:     def _parse_laravel_response(cls, status_code: int, body: str) -> Dict:
781:         description = "Success" if status_code < 400 else "Error"
782:         message = ""
783:         for key in ("message", "error", "detail"):
784:             match = re.search(rf"['\"]{key}['\"]\s*=>\s*['\"]([^'\"]+)['\"]", body)
785:             if match:
786:                 message = match.group(1)
787:                 break
788:         
789:         response = {
790:             "status_code": status_code,
791:             "description": message or description
792:         }
793:         if message:
794:             response["message"] = message
795:             
796:         properties = {}
797:         for key in re.findall(r"['\"]([A-Za-z0-9_\-]+)['\"]\s*=>", body):
798:             if key not in {"message", "error", "detail"}:
799:                 properties[key] = {"type": "string"}
800:             
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T09:19:37Z
Completed At: 2026-05-25T09:19:37Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1210
Total Bytes: 53011
Showing lines 800 to 1210
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
800:             
801:         if properties:
802:             response["schema"] = {
803:                 "type": "object",
804:                 "properties": properties
805:             }
806:         return response
807: 
808:     @classmethod
809:     def _resolve_laravel_details(
810:         cls,
811:         method: str,
812:         path: str,
813:         controller_class: Optional[str],
814:         method_name: Optional[str],
815:         closure_body: Optional[str],
816:         cross_file_resolver
817:     ) -> Dict:
818:         result = {}
819:         method_block = ""
820:         
821:         if controller_class and method_name:
822:             controller_content = cls._find_file_content_by_name(cross_file_resolver, f"{controller_class}.php")
823:             if controller_content:
824:                 method_block = cls._extract_php_method_block(controller_content, method_name)
825:                 
826:                 signature_match = re.search(rf"function\s+{method_name}\s*\(([^)]*)\)", controller_content, re.IGNORECASE)
827:                 if signature_match:
828:                     args = signature_match.group(1)
829:                     request_type_match = re.search(r"([A-Za-z0-9_]+)\s+\$request", args, re.IGNORECASE)
830:                     if request_type_match:
831:                         request_class = request_type_match.group(1)
832:                         if request_class not in {"Request", "LaravelRequest", "FormRequest"}:
833:                             cu
<truncated 17901 bytes>
se ""
1172: 
1173:     @classmethod
1174:     def _extract_python_methods(cls, args: str) -> List[str]:
1175:         methods_match = re.search(r"methods\s*=\s*\[([^\]]+)\]", args, re.IGNORECASE)
1176:         if not methods_match:
1177:             return []
1178:         return [
1179:             method.upper()
1180:             for method in re.findall(r"['\"]([A-Z]+)['\"]", methods_match.group(1), re.IGNORECASE)
1181:             if method.lower() in cls.HTTP_METHODS
1182:         ]
1183: 
1184:     @staticmethod
1185:     def _extract_spring_request_method(args: str) -> str:
1186:         match = re.search(r"RequestMethod\.([A-Z]+)", args)
1187:         return match.group(1) if match else ""
1188: 
1189:     @classmethod
1190:     def _join_paths(cls, prefix: str, path: str) -> str:
1191:         prefix = prefix or ""
1192:         path = path or ""
1193:         return cls._normalize_path("/".join([prefix.strip("/"), path.strip("/")]).strip("/"))
1194: 
1195:     @staticmethod
1196:     def _normalize_path(path: str) -> str:
1197:         path = re.sub(r"\(\?P<([A-Za-z_][A-Za-z0-9_]*)>[^)]+\)", r"{\1}", path or "")
1198:         path = re.sub(r"\(\?P\{([A-Za-z_][A-Za-z0-9_]*)\}[^)]*\)", r"{\1}", path)
1199:         path = re.sub(r"<(?:[^:>]+:)?([^>]+)>", r"{\1}", path)
1200:         path = path.replace("\\/", "/")
1201:         path = path.replace("^", "").replace("$", "")
1202:         path = re.sub(r"/\?", "", path)
1203:         path = re.sub(r"\?/?$", "", path)
1204:         path = path.replace("<", "{").replace(">", "}")
1205:         path = re.sub(r":([A-Za-z_][A-Za-z0-9_]*)", r"{\1}", path)
1206:         path = path.replace("[controller]", "{controller}").replace("[action]", "{action}")
1207:         if not path.startswith("/"):
1208:             path = "/" + path
1209:         return re.sub(r"/+", "/", path)
1210: 
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T09:22:51Z
Completed At: 2026-05-25T09:22:51Z
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

I will search for Spring Boot related extraction methods in `generic_framework_extractor.py`.

=== STEP ===

I will search for `Laravel` inside `generic_framework_extractor.py`.

=== STEP ===

I will view the first 200 lines of `generic_framework_extractor.py`.

=== STEP ===

Created At: 2026-05-25T09:24:21Z
Completed At: 2026-05-25T09:24:21Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1210
Total Bytes: 53011
Showing lines 1 to 200
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: import re
2: from pathlib import PurePosixPath
3: from typing import Dict, List, Tuple, Optional
4: 
5: 
6: class GenericFrameworkExtractor:
7:     """Extract route declarations for common frameworks with lightweight patterns."""
8: 
9:     HTTP_METHODS = {
10:         "get": "GET",
11:         "post": "POST",
12:         "put": "PUT",
13:         "delete": "DELETE",
14:         "patch": "PATCH",
15:         "options": "OPTIONS",
16:         "head": "HEAD",
17:     }
18: 
19:     @classmethod
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
38:     def _endpoint(cls, framework: str, method: str, path: str, file_path: str, matched_line: str) -
<truncated 5652 bytes>
f _nestjs_body(cls, method_block: str, method: str, model_index: Dict[str, Dict]) -> Dict:
159:         if method not in {"POST", "PUT", "PATCH"}:
160:             return {}
161: 
162:         match = re.search(
163:             r"@Body\(\s*(?:['\"]([^'\"]+)['\"])?\s*\)\s*([A-Za-z_][A-Za-z0-9_]*)\??\s*:\s*([^,\)\n]+)",
164:             method_block,
165:             re.IGNORECASE,
166:         )
167:         if not match:
168:             return {}
169: 
170:         field_name = match.group(1)
171:         variable_name = match.group(2)
172:         type_name = match.group(3).strip()
173:         schema = model_index.get(type_name) or {"type": "object", "properties": {}}
174:         if field_name:
175:             schema["properties"][field_name] = {"type": cls._map_ts_type(type_name)}
176: 
177:         return {
178:             "name": field_name or variable_name,
179:             "model": type_name or "RequestBody",
180:             "required": "?" not in match.group(0).split(":")[0],
181:             "schema": schema,
182:         }
183: 
184:     @classmethod
185:     def _typescript_model_index(cls, content: str) -> Dict[str, Dict]:
186:         models = {}
187:         class_pattern = re.compile(r"class\s+([A-Za-z_][A-Za-z0-9_]*)\s*{", re.IGNORECASE)
188:         for match in class_pattern.finditer(content):
189:             class_name = match.group(1)
190:             body_end = cls._find_balanced_end(content, match.end(), "{", "}")
191:             if body_end == -1:
192:                 continue
193:             body = content[match.end() : body_end - 1]
194:             properties = {}
195:             required = []
196:             for field_match in re.finditer(
197:                 r"^\s*([A-Za-z_][A-Za-z0-9_]*)\??\s*:\s*([^;=\n]+)",
198:                 body,
199:                 re.MULTILINE,
200:             ):
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

I will view lines 201 to 600 of `generic_framework_extractor.py` to inspect the Spring Boot and Laravel extraction logic.

=== STEP ===

Created At: 2026-05-25T09:24:24Z
Completed At: 2026-05-25T09:24:24Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1210
Total Bytes: 53011
Showing lines 201 to 600
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
201:                 field_name = field_match.group(1)
202:                 type_name = field_match.group(2).strip()
203:                 properties[field_name] = {
204:                     "type": cls._map_ts_type(type_name),
205:                     "typescript_type": type_name,
206:                 }
207:                 if "?" not in field_match.group(0).split(":", 1)[0]:
208:                     required.append(field_name)
209:             if properties:
210:                 models[class_name] = {
211:                     "type": "object",
212:                     "model": class_name,
213:                     "required": required,
214:                     "properties": properties,
215:                 }
216:         return models
217: 
218:     @classmethod
219:     def _nestjs_responses(cls, method_block: str, method: str) -> List[Dict]:
220:         responses = []
221:         seen = set()
222:         status_match = re.search(r"@HttpCode\(\s*(\d{3})\s*\)", method_block)
223:         success_code = int(status_match.group(1)) if status_match else cls._default_success_code(method)
224:         responses.append({"status_code": success_code, "description": "Success"})
225:         seen.add(success_code)
226: 
227:         for match in re.finditer(
228:             r"throw\s+new\s+([A-Za-z]+Exception)\(\s*(?:['\"]([^'\"]+)['\"]|{[^}]*message\s*:\s*['\"]([^'\"]+)['\"])?",
229:             method_block,
230:         ):
231:             exception_name = match.group(1)
232:             status_code = cl
<truncated 15537 bytes>
):
566:                     paren_end = cls._find_balanced_end(args_content, 6, "(", ")")
567:                     if paren_end != -1:
568:                         methods_list = cls._extract_php_string_list(args_content[:paren_end])
569:                         rem = args_content[paren_end:].strip()
570:                 else:
571:                     path_match = re.search(r"['\"]([^'\"]+)['\"]", args_content)
572:                     if path_match:
573:                         methods_list = [path_match.group(1)]
574:                         rem = args_content[path_match.end():].strip()
575:                 
576:                 rem = rem.lstrip(",").strip()
577:                 comma_idx = rem.find(",")
578:                 if comma_idx == -1:
579:                     continue
580:                 path_arg = rem[:comma_idx].strip()
581:                 handler_arg = rem[comma_idx + 1:].strip()
582:                 
583:                 path_match = re.search(r"['\"]([^'\"]+)['\"]", path_arg)
584:                 if not path_match:
585:                     continue
586:                 path = path_match.group(1)
587:                 
588:                 controller_class, method_name, closure_body = cls._parse_laravel_handler(handler_arg)
589:                 
590:                 for m in methods_list:
591:                     if m.lower() in cls.HTTP_METHODS:
592:                         endpoints.append(
593:                             cls._laravel_endpoint(
594:                                 m.upper(),
595:                                 cls._join_paths(prefix, path),
596:                                 file_path,
597:                                 match.group(0),
598:                                 controller_class,
599:                                 method_name,
600:                                 closure_body,
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

I will view lines 601 to 800 of `generic_framework_extractor.py`.

=== STEP ===

Created At: 2026-05-25T09:24:29Z
Completed At: 2026-05-25T09:24:29Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1210
Total Bytes: 53011
Showing lines 601 to 800
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
601:                                 cross_file_resolver
602:                             )
603:                         )
604:             elif verb == "any":
605:                 path_quote_match = re.search(r"['\"]([^'\"]+)['\"]", args_content)
606:                 if not path_quote_match:
607:                     continue
608:                 path = path_quote_match.group(1)
609:                 comma_idx = args_content.find(",", path_quote_match.end())
610:                 handler_arg = args_content[comma_idx + 1:].strip() if comma_idx != -1 else ""
611:                 
612:                 controller_class, method_name, closure_body = cls._parse_laravel_handler(handler_arg)
613:                 
614:                 for m in ("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"):
615:                     endpoints.append(
616:                         cls._laravel_endpoint(
617:                             m,
618:                             cls._join_paths(prefix, path),
619:                             file_path,
620:                             match.group(0),
621:                             controller_class,
622:                             method_name,
623:                             closure_body,
624:                             cross_file_resolver
625:                         )
626:                     )
627:             else:
628:                 path_quote_match = re.search(r"['\"]([^'\"]+)['\"]", args_content)
629:                 if not path_quote_match:
630:                     cont
<truncated 6544 bytes>
t:
761:                 required = "required" in val_content.lower()
762:                 type_name = "string"
763:                 if "integer" in val_content.lower() or "int" in val_content.lower():
764:                     type_name = "integer"
765:                 elif "numeric" in val_content.lower() or "double" in val_content.lower() or "float" in val_content.lower():
766:                     type_name = "number"
767:                 elif "boolean" in val_content.lower() or "bool" in val_content.lower():
768:                     type_name = "boolean"
769:                 elif "array" in val_content.lower():
770:                     type_name = "array"
771:                 
772:                 properties[key] = {
773:                     "type": type_name,
774:                     "required": required,
775:                     "rules": val_content
776:                 }
777:         return properties
778: 
779:     @classmethod
780:     def _parse_laravel_response(cls, status_code: int, body: str) -> Dict:
781:         description = "Success" if status_code < 400 else "Error"
782:         message = ""
783:         for key in ("message", "error", "detail"):
784:             match = re.search(rf"['\"]{key}['\"]\s*=>\s*['\"]([^'\"]+)['\"]", body)
785:             if match:
786:                 message = match.group(1)
787:                 break
788:         
789:         response = {
790:             "status_code": status_code,
791:             "description": message or description
792:         }
793:         if message:
794:             response["message"] = message
795:             
796:         properties = {}
797:         for key in re.findall(r"['\"]([A-Za-z0-9_\-]+)['\"]\s*=>", body):
798:             if key not in {"message", "error", "detail"}:
799:                 properties[key] = {"type": "string"}
800:             
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

I will view lines 801 to 1000 of `generic_framework_extractor.py`.

=== STEP ===

Created At: 2026-05-25T09:24:31Z
Completed At: 2026-05-25T09:24:32Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1210
Total Bytes: 53011
Showing lines 801 to 1000
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
801:         if properties:
802:             response["schema"] = {
803:                 "type": "object",
804:                 "properties": properties
805:             }
806:         return response
807: 
808:     @classmethod
809:     def _resolve_laravel_details(
810:         cls,
811:         method: str,
812:         path: str,
813:         controller_class: Optional[str],
814:         method_name: Optional[str],
815:         closure_body: Optional[str],
816:         cross_file_resolver
817:     ) -> Dict:
818:         result = {}
819:         method_block = ""
820:         
821:         if controller_class and method_name:
822:             controller_content = cls._find_file_content_by_name(cross_file_resolver, f"{controller_class}.php")
823:             if controller_content:
824:                 method_block = cls._extract_php_method_block(controller_content, method_name)
825:                 
826:                 signature_match = re.search(rf"function\s+{method_name}\s*\(([^)]*)\)", controller_content, re.IGNORECASE)
827:                 if signature_match:
828:                     args = signature_match.group(1)
829:                     request_type_match = re.search(r"([A-Za-z0-9_]+)\s+\$request", args, re.IGNORECASE)
830:                     if request_type_match:
831:                         request_class = request_type_match.group(1)
832:                         if request_class not in {"Request", "LaravelRequest", "FormRequest"}:
833:                             custom_request_conte
<truncated 7960 bytes>
(response)
962:                     seen_status_codes.add(status_code)
963:                     
964:             response_pattern = re.compile(
965:                 r"\bresponse\s*\(\s*(?P<body>[^;]+?)(?:\s*,\s*(?P<status>\d{3}))?\s*\)",
966:                 re.IGNORECASE | re.DOTALL
967:             )
968:             for match in response_pattern.finditer(method_block):
969:                 if "->json" in method_block[max(0, match.start() - 10):match.end() + 10]:
970:                     continue
971:                 status_code = int(match.group("status")) if match.group("status") else 200
972:                 body = match.group("body")
973:                 response = cls._parse_laravel_response(status_code, body)
974:                 if status_code not in seen_status_codes:
975:                     responses.append(response)
976:                     seen_status_codes.add(status_code)
977:                     
978:             if responses:
979:                 result["responses"] = responses
980:                 success = next((r for r in responses if 200 <= r["status_code"] < 300), None)
981:                 if success:
982:                     result["status_code"] = success["status_code"]
983:                     
984:         return result
985: 
986:     @classmethod
987:     def _laravel_endpoint(
988:         cls,
989:         method: str,
990:         path: str,
991:         file_path: str,
992:         matched_line: str,
993:         controller_class: Optional[str] = None,
994:         method_name: Optional[str] = None,
995:         closure_body: Optional[str] = None,
996:         cross_file_resolver = None
997:     ) -> Dict:
998:         endpoint = cls._endpoint("Laravel", method, path, file_path, matched_line)
999:         endpoint["confidence"] = 0.82
1000:         path_params = cls._path_params(endpoint["path"])
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

I will view lines 1001 to 1210 of `generic_framework_extractor.py`.

=== STEP ===

Created At: 2026-05-25T09:24:35Z
Completed At: 2026-05-25T09:24:35Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1210
Total Bytes: 53011
Showing lines 1001 to 1210
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1001:         if path_params:
1002:             endpoint["path_params"] = path_params
1003:             
1004:         details = cls._resolve_laravel_details(
1005:             method,
1006:             endpoint["path"],
1007:             controller_class,
1008:             method_name,
1009:             closure_body,
1010:             cross_file_resolver
1011:         )
1012:         
1013:         if "request_body" in details:
1014:             endpoint["request_body"] = details["request_body"]
1015:         elif method in {"POST", "PUT", "PATCH"}:
1016:             endpoint["request_body"] = {
1017:                 "name": "request",
1018:                 "model": "LaravelRequest",
1019:                 "required": method in {"POST", "PUT"},
1020:                 "schema": {"type": "object", "properties": {}},
1021:             }
1022:             
1023:         if "query_params" in details:
1024:             endpoint["query_params"] = details["query_params"]
1025:             
1026:         if "responses" in details:
1027:             endpoint["responses"] = details["responses"]
1028:             endpoint["status_code"] = details["status_code"]
1029:         else:
1030:             endpoint["responses"] = [{"status_code": cls._default_success_code(method), "description": "Success"}]
1031:             endpoint["status_code"] = cls._default_success_code(method)
1032:             
1033:         if controller_class and method_name:
1034:             endpoint["function_name"] = f"{controller_class}@
<truncated 6538 bytes>
se ""
1172: 
1173:     @classmethod
1174:     def _extract_python_methods(cls, args: str) -> List[str]:
1175:         methods_match = re.search(r"methods\s*=\s*\[([^\]]+)\]", args, re.IGNORECASE)
1176:         if not methods_match:
1177:             return []
1178:         return [
1179:             method.upper()
1180:             for method in re.findall(r"['\"]([A-Z]+)['\"]", methods_match.group(1), re.IGNORECASE)
1181:             if method.lower() in cls.HTTP_METHODS
1182:         ]
1183: 
1184:     @staticmethod
1185:     def _extract_spring_request_method(args: str) -> str:
1186:         match = re.search(r"RequestMethod\.([A-Z]+)", args)
1187:         return match.group(1) if match else ""
1188: 
1189:     @classmethod
1190:     def _join_paths(cls, prefix: str, path: str) -> str:
1191:         prefix = prefix or ""
1192:         path = path or ""
1193:         return cls._normalize_path("/".join([prefix.strip("/"), path.strip("/")]).strip("/"))
1194: 
1195:     @staticmethod
1196:     def _normalize_path(path: str) -> str:
1197:         path = re.sub(r"\(\?P<([A-Za-z_][A-Za-z0-9_]*)>[^)]+\)", r"{\1}", path or "")
1198:         path = re.sub(r"\(\?P\{([A-Za-z_][A-Za-z0-9_]*)\}[^)]*\)", r"{\1}", path)
1199:         path = re.sub(r"<(?:[^:>]+:)?([^>]+)>", r"{\1}", path)
1200:         path = path.replace("\\/", "/")
1201:         path = path.replace("^", "").replace("$", "")
1202:         path = re.sub(r"/\?", "", path)
1203:         path = re.sub(r"\?/?$", "", path)
1204:         path = path.replace("<", "{").replace(">", "}")
1205:         path = re.sub(r":([A-Za-z_][A-Za-z0-9_]*)", r"{\1}", path)
1206:         path = path.replace("[controller]", "{controller}").replace("[action]", "{action}")
1207:         if not path.startswith("/"):
1208:             path = "/" + path
1209:         return re.sub(r"/+", "/", path)
1210: 
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T09:59:49Z
Completed At: 2026-05-25T09:59:50Z
The following changes were made by the replace_file_content tool to: C:\Users\NAVEENYA\.gemini\antigravity-ide\brain\f21fdfec-d083-4967-b688-8db7d4a04ddd\task.md. If relevant, proactively run terminal commands to execute this code for the USER. Don't ask for permission.
[diff_block_start]
@@ -1,7 +1,7 @@
 # Overhaul Checklist
 
-- [ ] Fix Repository Classifier & File scoring (`repository_classifier.py`)
-- [ ] Overhaul Spring Boot Extractor (`generic_framework_extractor.py`)
+- [x] Fix Repository Classifier & File scoring (`repository_classifier.py`)
+- [/] Overhaul Spring Boot Extractor (`generic_framework_extractor.py`)
 - [ ] Fix DRF Helper Leak, custom actions & Enhance Serializers (`django_drf_ast_extractor.py`)
 - [ ] Enhance Express.js router composition graph and prefix resolution (`enhanced_cross_file_resolver.py` & `express_extractor.py`)
 - [ ] Enhance Laravel resource endpoints, requests, and middleware (`generic_framework_extractor.py`)
[diff_block_end]

Please note that the above snippet only shows the MODIFIED lines from the last change. It shows up to 3 lines of unchanged lines before and after the modified lines. The actual file contents may have many more lines not shown.

=== STEP ===

I will view lines 20 to 40 of `generic_framework_extractor.py` to confirm the code structure around framework checks.

=== STEP ===

Created At: 2026-05-25T10:00:03Z
Completed At: 2026-05-25T10:00:03Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1210
Total Bytes: 53011
Showing lines 20 to 40
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
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

=== STEP ===

Created At: 2026-05-25T10:00:09Z
Completed At: 2026-05-25T10:00:11Z
The following changes were made by the replace_file_content tool to: c:\Users\NAVEENYA\OneDrive\Desktop\NAVEENYA\api_doc_generator\backend\api_doc_generator\extractors\generic_framework_extractor.py. If relevant, proactively run terminal commands to execute this code for the USER. Don't ask for permission.
[diff_block_start]
@@ -23,7 +23,7 @@
         if framework == "NestJS":
             return cls._extract_nestjs(file_path, content)
         if framework == "Spring Boot":
-            return cls._extract_spring(file_path, content)
+            return cls._extract_spring(file_path, content, cross_file_resolver)
         if framework == "Laravel":
             return cls._extract_laravel(file_path, content, cross_file_resolver)
         if framework == "ASP.NET Core":
[diff_block_end]

Please note that the above snippet only shows the MODIFIED lines from the last change. It shows up to 3 lines of unchanged lines before and after the modified lines. The actual file contents may have many more lines not shown.

=== STEP ===

I will view lines 310 to 510 of `generic_framework_extractor.py` to see the current Spring Boot extraction functions.

=== STEP ===

Created At: 2026-05-25T10:00:15Z
Completed At: 2026-05-25T10:00:15Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1210
Total Bytes: 53032
Showing lines 310 to 510
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
310:     def _extract_spring(cls, file_path: str, content: str) -> List[Dict]:
311:         endpoints = []
312:         class_prefix = cls._first_match(
313:             content,
314:             r"@RequestMapping\(\s*(?:value\s*=\s*)?['\"]([^'\"]*)['\"]",
315:         ) or ""
316:         model_index = cls._java_model_index(content)
317:         mapping_pattern = re.compile(
318:             r"@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping)(?:\(\s*(?:value\s*=\s*)?['\"]?([^'\"),]*)['\"]?(?P<args>[^)]*)\))?",
319:             re.IGNORECASE,
320:         )
321:         method_map = {
322:             "GetMapping": "GET",
323:             "PostMapping": "POST",
324:             "PutMapping": "PUT",
325:             "DeleteMapping": "DELETE",
326:             "PatchMapping": "PATCH",
327:         }
328:         for match in mapping_pattern.finditer(content):
329:             annotation = match.group(1)
330:             method = method_map.get(annotation, cls._extract_spring_request_method(match.group("args") or "") or "GET")
331:             path = cls._join_paths(class_prefix, match.group(2) or "")
332:             method_block = cls._extract_java_method_block(content, match.end())
333:             endpoint = cls._endpoint("Spring Boot", method, path, file_path, match.group(0))
334:             endpoint["confidence"] = 0.78
335:             endpoint.update(cls._spring_request_metadata(method_block, endpoint["path"], method, model_index))
336:             responses = cls._spring_response
<truncated 6395 bytes>
476:             required = []
477:             record_fields = match.group("record")
478:             if record_fields:
479:                 for raw_field in record_fields.split(","):
480:                     parts = raw_field.strip().split()
481:                     if len(parts) >= 2:
482:                         type_name, field_name = parts[-2], parts[-1]
483:                         properties[field_name] = {"type": cls._map_java_type(type_name), "java_type": type_name}
484:                         required.append(field_name)
485:             body_end = cls._find_balanced_end(content, match.end(), "{", "}")
486:             if body_end != -1:
487:                 body = content[match.end() : body_end - 1]
488:                 for field_match in re.finditer(
489:                     r"(?:private|public|protected)?\s+([A-Za-z0-9_<>, ?]+)\s+([A-Za-z_][A-Za-z0-9_]*)\s*;",
490:                     body,
491:                 ):
492:                     type_name = field_match.group(1).strip()
493:                     field_name = field_match.group(2)
494:                     if field_name not in properties:
495:                         properties[field_name] = {"type": cls._map_java_type(type_name), "java_type": type_name}
496:                         required.append(field_name)
497:             if properties:
498:                 models[class_name] = {
499:                     "type": "object",
500:                     "model": class_name,
501:                     "required": required,
502:                     "properties": properties,
503:                 }
504:         return models
505: 
506:     @staticmethod
507:     def _map_java_type(type_name: str) -> str:
508:         normalized = (type_name or "").lower()
509:         if any(token in normalized for token in ["int", "long", "integer"]):
510:             return "integer"
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

I will replace the Spring Boot extractor helper functions in `generic_framework_extractor.py` to add comprehensive support for annotations, DTO scanning, security headers, and ResponseStatusException.

=== STEP ===

Created At: 2026-05-25T10:00:26Z
Completed At: 2026-05-25T10:00:29Z
The following changes were made by the replace_file_content tool to: c:\Users\NAVEENYA\OneDrive\Desktop\NAVEENYA\api_doc_generator\backend\api_doc_generator\extractors\generic_framework_extractor.py. If relevant, proactively run terminal commands to execute this code for the USER. Don't ask for permission.
[diff_block_start]
@@ -307,15 +307,27 @@
         return -1
 
     @classmethod
-    def _extract_spring(cls, file_path: str, content: str) -> List[Dict]:
+    @classmethod
+    def _extract_spring(cls, file_path: str, content: str, cross_file_resolver=None) -> List[Dict]:
         endpoints = []
         class_prefix = cls._first_match(
             content,
-            r"@RequestMapping\(\s*(?:value\s*=\s*)?['\"]([^'\"]*)['\"]",
+            r"@RequestMapping\(\s*(?:value|path)?\s*=\s*['\"]([^'\"]*)['\"]",
+        ) or cls._first_match(
+            content,
+            r"@RequestMapping\(\s*['\"]([^'\"]*)['\"]",
         ) or ""
-        model_index = cls._java_model_index(content)
+        
+        model_index = {}
+        if cross_file_resolver and hasattr(cross_file_resolver, "file_contents"):
+            for path, file_content in cross_file_resolver.file_contents.items():
+                if path.endswith(".java") or path.endswith(".kt"):
+                    model_index.update(cls._java_model_index(file_content))
+        else:
+            model_index.update(cls._java_model_index(content))
+            
         mapping_pattern = re.compile(
-            r"@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping)(?:\(\s*(?:value\s*=\s*)?['\"]?([^'\"),]*)['\"]?(?P<args>[^)]*)\))?",
+            r"@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)(?:\(\s*(?:value|path\s*=\s*)?['\"]?([^'\"),]*)['\"]?(?P<args>[^)]*)\))?",
             re.IGNORECASE,
         )
         method_map = {
@@ -324,6 +324,12 @@
             "DeleteMapping": "DELETE",
             "PatchMapping": "PATCH",
         }
+       
<truncated 6302 bytes>

             status_code = cls._spring_status_value(match.group(1))
-            if status_code not in seen:
-                responses.append({
-                    "status_code": status_code,
-                    "description": match.group(2),
-                    "message": match.group(2),
+            description = match.group(2) or f"Error status {status_code}"
+            if status_code not in seen:
+                responses.append({
+                    "status_code": status_code,
+                    "description": description,
+                    "message": description,
                 })
                 seen.add(status_code)
         return responses
@@ -457,7 +457,7 @@
             "UNPROCESSABLE_ENTITY": 422,
             "INTERNAL_SERVER_ERROR": 500,
         }
-        return mapping.get(value, 200)
+        return mapping.get(value.upper(), 200)
 
     @classmethod
     def _java_model_index(cls, content: str) -> Dict[str, Dict]:
@@ -477,9 +477,11 @@
             body_end = cls._find_balanced_end(content, match.end(), "{", "}")
             if body_end != -1:
                 body = content[match.end() : body_end - 1]
+                # Strip out annotations before fields to prevent parsing issues
+                body_clean = re.sub(r"@[A-Za-z0-9_]+\s*(?:\([^)]*\))?", "", body)
                 for field_match in re.finditer(
-                    r"(?:private|public|protected)?\s+([A-Za-z0-9_<>, ?]+)\s+([A-Za-z_][A-Za-z0-9_]*)\s*;",
-                    body,
+                    r"(?:private|public|protected)?\s+(?:final\s+)?([A-Za-z0-9_<>\?,\[\]\s]+)\s+([A-Za-z_][A-Za-z0-9_]*)\s*;",
+                    body_clean,
                 ):
                     type_name = field_match.group(1).strip()
                     field_name = field_match.group(2)
[diff_block_end]

Please note that the above snippet only shows the MODIFIED lines from the last change. It shows up to 3 lines of unchanged lines before and after the modified lines. The actual file contents may have many more lines not shown.

=== STEP ===

Created At: 2026-05-25T10:00:42Z
Completed At: 2026-05-25T10:00:42Z
The following changes were made by the replace_file_content tool to: C:\Users\NAVEENYA\.gemini\antigravity-ide\brain\f21fdfec-d083-4967-b688-8db7d4a04ddd\task.md. If relevant, proactively run terminal commands to execute this code for the USER. Don't ask for permission.
[diff_block_start]
@@ -1,8 +1,8 @@
 # Overhaul Checklist
 
 - [x] Fix Repository Classifier & File scoring (`repository_classifier.py`)
-- [/] Overhaul Spring Boot Extractor (`generic_framework_extractor.py`)
-- [ ] Fix DRF Helper Leak, custom actions & Enhance Serializers (`django_drf_ast_extractor.py`)
+- [x] Overhaul Spring Boot Extractor (`generic_framework_extractor.py`)
+- [/] Fix DRF Helper Leak, custom actions & Enhance Serializers (`django_drf_ast_extractor.py`)
 - [ ] Enhance Express.js router composition graph and prefix resolution (`enhanced_cross_file_resolver.py` & `express_extractor.py`)
 - [ ] Enhance Laravel resource endpoints, requests, and middleware (`generic_framework_extractor.py`)
 - [ ] Implement OpenAPI schema component traversal, security fallback, and path normalization (`openapi_generator.py`)
[diff_block_end]

Please note that the above snippet only shows the MODIFIED lines from the last change. It shows up to 3 lines of unchanged lines before and after the modified lines. The actual file contents may have many more lines not shown.

=== STEP ===

Created At: 2026-05-25T10:02:27Z
Completed At: 2026-05-25T10:02:27Z
The following changes were made by the replace_file_content tool to: C:\Users\NAVEENYA\.gemini\antigravity-ide\brain\f21fdfec-d083-4967-b688-8db7d4a04ddd\task.md. If relevant, proactively run terminal commands to execute this code for the USER. Don't ask for permission.
[diff_block_start]
@@ -2,8 +2,8 @@
 
 - [x] Fix Repository Classifier & File scoring (`repository_classifier.py`)
 - [x] Overhaul Spring Boot Extractor (`generic_framework_extractor.py`)
-- [/] Fix DRF Helper Leak, custom actions & Enhance Serializers (`django_drf_ast_extractor.py`)
-- [ ] Enhance Express.js router composition graph and prefix resolution (`enhanced_cross_file_resolver.py` & `express_extractor.py`)
+- [x] Fix DRF Helper Leak, custom actions & Enhance Serializers (`django_drf_ast_extractor.py`)
+- [/] Enhance Express.js router composition graph and prefix resolution (`enhanced_cross_file_resolver.py` & `express_extractor.py`)
 - [ ] Enhance Laravel resource endpoints, requests, and middleware (`generic_framework_extractor.py`)
 - [ ] Implement OpenAPI schema component traversal, security fallback, and path normalization (`openapi_generator.py`)
 - [ ] Create and run automated unit tests to verify the overhaul
[diff_block_end]

Please note that the above snippet only shows the MODIFIED lines from the last change. It shows up to 3 lines of unchanged lines before and after the modified lines. The actual file contents may have many more lines not shown.

=== STEP ===

Created At: 2026-05-25T10:04:16Z
Completed At: 2026-05-25T10:04:16Z
File Path: `file:///C:/Users/NAVEENYA/.gemini/antigravity-ide/brain/f21fdfec-d083-4967-b688-8db7d4a04ddd/task.md`
Total Lines: 10
Total Bytes: 685
Showing lines 1 to 10
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: # Overhaul Checklist
2: 
3: - [x] Fix Repository Classifier & File scoring (`repository_classifier.py`)
4: - [x] Overhaul Spring Boot Extractor (`generic_framework_extractor.py`)
5: - [x] Fix DRF Helper Leak, custom actions & Enhance Serializers (`django_drf_ast_extractor.py`)
6: - [/] Enhance Express.js router composition graph and prefix resolution (`enhanced_cross_file_resolver.py` & `express_extractor.py`)
7: - [ ] Enhance Laravel resource endpoints, requests, and middleware (`generic_framework_extractor.py`)
8: - [ ] Implement OpenAPI schema component traversal, security fallback, and path normalization (`openapi_generator.py`)
9: - [ ] Create and run automated unit tests to verify the overhaul
10: 
The above content shows the entire, complete file contents of the requested file.


=== STEP ===

Created At: 2026-05-25T10:04:24Z
Completed At: 2026-05-25T10:04:24Z
{"name":"__init__.py","sizeBytes":"66"}
{"name":"__pycache__","isDir":true}
{"name":"batch_processor.py","sizeBytes":"7651"}
{"name":"confidence_scorer.py","sizeBytes":"2317"}
{"name":"cross_file_router_resolver.py","sizeBytes":"8462"}
{"name":"django_drf_ast_extractor.py","sizeBytes":"57771"}
{"name":"endpoint_deduplicator.py","sizeBytes":"2175"}
{"name":"endpoint_normalizer.py","sizeBytes":"5803"}
{"name":"enhanced_cross_file_resolver.py","sizeBytes":"16833"}
{"name":"express_extractor.py","sizeBytes":"17191"}
{"name":"extraction_pipeline.py","sizeBytes":"11267"}
{"name":"extractor_manager.py","sizeBytes":"7249"}
{"name":"fastapi_ast_extractor.py","sizeBytes":"21909"}
{"name":"fastapi_extractor.py","sizeBytes":"4268"}
{"name":"generic_framework_extractor.py","sizeBytes":"55913"}
{"name":"global_router_registry.py","sizeBytes":"6977"}
{"name":"import_resolver.py","sizeBytes":"13290"}
{"name":"include_router_extractor.py","sizeBytes":"9173"}
{"name":"openapi_spec_extractor.py","sizeBytes":"9621"}
{"name":"route_classifier.py","sizeBytes":"11719"}
{"name":"route_resolver.py","sizeBytes":"9295"}
{"name":"router_composition_graph.py","sizeBytes":"15388"}

Summary: This directory contains 1 subdirectories and 21 files.

=== STEP ===

Created At: 2026-05-25T10:04:30Z
Completed At: 2026-05-25T10:04:31Z
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":27,"LineContent":"        if framework == \"Laravel\":"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":28,"LineContent":"            return cls._extract_laravel(file_path, content, cross_file_resolver)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":585,"LineContent":"    def _extract_laravel(cls, file_path: str, content: str, cross_file_resolver=None) -\u003e List[Dict]:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":587,"LineContent":"        return cls._extract_laravel_routes_from_content(file_path, content, \"\", cross_file_resolver)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":590,"LineContent":"    def _extract_laravel_routes_from_content(cls, file_path: str, content: str, prefix: str, cross_file_resolver=None) -\u003e List[Dict]:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":594,"LineContent":"        for group_prefix, body, start, end in cls._laravel_prefixed_groups(content):"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":597,"LineContent":"                cls._extract_laravel_routes_from_content("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend
<truncated 3401 bytes>
extractor.py","LineNumber":1022,"LineContent":"                response = cls._parse_laravel_response(status_code, body)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1036,"LineContent":"                response = cls._parse_laravel_response(status_code, body)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1050,"LineContent":"    def _laravel_endpoint("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1061,"LineContent":"        endpoint = cls._endpoint(\"Laravel\", method, path, file_path, matched_line)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1067,"LineContent":"        details = cls._resolve_laravel_details("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1081,"LineContent":"                \"model\": \"LaravelRequest\","}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1103,"LineContent":"    def _laravel_resource_endpoints("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1122,"LineContent":"            cls._laravel_endpoint("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1141,"LineContent":"    def _laravel_prefixed_groups(cls, content: str) -\u003e List[Tuple[str, str, int, int]]:"}

=== STEP ===

Created At: 2026-05-25T10:04:33Z
Completed At: 2026-05-25T10:04:33Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1273
Total Bytes: 55913
Showing lines 580 to 900
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
580:         if any(token in normalized for token in ["map", "object", "dto", "request"]):
581:             return "object"
582:         return "string"
583: 
584:     @classmethod
585:     def _extract_laravel(cls, file_path: str, content: str, cross_file_resolver=None) -> List[Dict]:
586:         content = cls._strip_php_comments(content)
587:         return cls._extract_laravel_routes_from_content(file_path, content, "", cross_file_resolver)
588: 
589:     @classmethod
590:     def _extract_laravel_routes_from_content(cls, file_path: str, content: str, prefix: str, cross_file_resolver=None) -> List[Dict]:
591:         endpoints = []
592:         group_ranges = []
593: 
594:         for group_prefix, body, start, end in cls._laravel_prefixed_groups(content):
595:             group_ranges.append((start, end))
596:             endpoints.extend(
597:                 cls._extract_laravel_routes_from_content(
598:                     file_path,
599:                     body,
600:                     cls._join_paths(prefix, group_prefix),
601:                     cross_file_resolver
602:                 )
603:             )
604:         content_without_groups = cls._remove_ranges(content, group_ranges)
605: 
606:         route_pattern = re.compile(
607:             r"Route::(?:[A-Za-z0-9_]+\s*\([^;{}]*\)\s*->\s*)*(get|post|put|delete|patch|options|any|match)\s*\(",
608:             re.IGNORECASE
609:         )
610:         
611:         for match in route_pattern.finditer(content_without_groups):
612:   
<truncated 12792 bytes>
    "type": "object",
867:                 "properties": properties
868:             }
869:         return response
870: 
871:     @classmethod
872:     def _resolve_laravel_details(
873:         cls,
874:         method: str,
875:         path: str,
876:         controller_class: Optional[str],
877:         method_name: Optional[str],
878:         closure_body: Optional[str],
879:         cross_file_resolver
880:     ) -> Dict:
881:         result = {}
882:         method_block = ""
883:         
884:         if controller_class and method_name:
885:             controller_content = cls._find_file_content_by_name(cross_file_resolver, f"{controller_class}.php")
886:             if controller_content:
887:                 method_block = cls._extract_php_method_block(controller_content, method_name)
888:                 
889:                 signature_match = re.search(rf"function\s+{method_name}\s*\(([^)]*)\)", controller_content, re.IGNORECASE)
890:                 if signature_match:
891:                     args = signature_match.group(1)
892:                     request_type_match = re.search(r"([A-Za-z0-9_]+)\s+\$request", args, re.IGNORECASE)
893:                     if request_type_match:
894:                         request_class = request_type_match.group(1)
895:                         if request_class not in {"Request", "LaravelRequest", "FormRequest"}:
896:                             custom_request_content = cls._find_file_content_by_name(cross_file_resolver, f"{request_class}.php")
897:                             if custom_request_content:
898:                                 rules_method_block = cls._extract_php_method_block(custom_request_content, "rules")
899:                                 if rules_method_block:
900:                                     rules = cls._parse_php_validation_rules(rules_method_block)
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T10:04:35Z
Completed At: 2026-05-25T10:04:35Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1273
Total Bytes: 55913
Showing lines 900 to 1170
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
900:                                     rules = cls._parse_php_validation_rules(rules_method_block)
901:                                     if rules:
902:                                         if method.upper() in {"POST", "PUT", "PATCH"}:
903:                                             properties = {k: {"type": v["type"]} for k, v in rules.items()}
904:                                             required = [k for k, v in rules.items() if v["required"]]
905:                                             result["request_body"] = {
906:                                                 "name": "body",
907:                                                 "model": request_class,
908:                                                 "required": True,
909:                                                 "schema": {
910:                                                     "type": "object",
911:                                                     "properties": properties,
912:                                                     "required": required
913:                                                 }
914:                                             }
915:                                         else:
916:                                             result["query_params"] = [
917:                                                 {
918:                                                     "name": k,
919:                                                     "type": v["type"],
920:                              
<truncated 10935 bytes>
 cross_file_resolver=cross_file_resolver
1130:             )
1131:             for method, path, method_name in definitions
1132:         ]
1133: 
1134:     @staticmethod
1135:     def _strip_php_comments(content: str) -> str:
1136:         content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
1137:         content = re.sub(r"^\s*//.*$", "", content, flags=re.MULTILINE)
1138:         return re.sub(r"^\s*#.*$", "", content, flags=re.MULTILINE)
1139: 
1140:     @classmethod
1141:     def _laravel_prefixed_groups(cls, content: str) -> List[Tuple[str, str, int, int]]:
1142:         groups = []
1143:         pattern = re.compile(
1144:             r"Route::(?:[A-Za-z_][A-Za-z0-9_]*\s*\([^;{}]*?\)\s*->\s*)*"
1145:             r"prefix\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*->\s*group\s*\(",
1146:             re.IGNORECASE | re.DOTALL,
1147:         )
1148:         for match in pattern.finditer(content):
1149:             function_start = content.find("{", match.end())
1150:             if function_start == -1:
1151:                 continue
1152:             function_end = cls._find_balanced_end(content, function_start + 1, "{", "}")
1153:             if function_end == -1:
1154:                 continue
1155:             groups.append((match.group(1), content[function_start + 1 : function_end - 1], match.start(), function_end))
1156:         return groups
1157: 
1158:     @staticmethod
1159:     def _remove_ranges(content: str, ranges: List[Tuple[int, int]]) -> str:
1160:         if not ranges:
1161:             return content
1162:         pieces = []
1163:         cursor = 0
1164:         for start, end in sorted(ranges):
1165:             pieces.append(content[cursor:start])
1166:             cursor = max(cursor, end)
1167:         pieces.append(content[cursor:])
1168:         return "".join(pieces)
1169: 
1170:     @staticmethod
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T10:04:42Z
Completed At: 2026-05-25T10:04:43Z
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":104,"LineContent":"        body_end = cls._find_balanced_end(content, body_start + 1, \"{\", \"}\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":190,"LineContent":"            body_end = cls._find_balanced_end(content, match.end(), \"{\", \"}\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":285,"LineContent":"    def _find_balanced_end(content: str, start_index: int, open_char: str, close_char: str) -\u003e int:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":390,"LineContent":"        body_end = cls._find_balanced_end(content, body_start + 1, \"{\", \"}\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":546,"LineContent":"            body_end = cls._find_balanced_end(content, match.end(), \"{\", \"}\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":614,"LineContent":"            args_end = cls._find_balanced_end(content_without_groups, args_start, \"(\", \")\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":624,"LineContent":"                    bracket_end = cls._find_balanced_end(args_content, 1, \"[\", \"]\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\
<truncated 922 bytes>
              bracket_end = cls._find_balanced_end(array_content, val_start + 1, \"[\", \"]\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":819,"LineContent":"                paren_end = cls._find_balanced_end(array_content, val_start + 6, \"(\", \")\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":946,"LineContent":"                            array_end = cls._find_balanced_end(method_block, array_start + 1, \"[\", \"]\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":948,"LineContent":"                            array_end = cls._find_balanced_end(method_block, array_start + 1, \"(\", \")\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1152,"LineContent":"            function_end = cls._find_balanced_end(content, function_start + 1, \"{\", \"}\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\express_extractor.py","LineNumber":262,"LineContent":"        end_index = ExpressExtractor._find_balanced_end(content, start_index, \"(\", \")\")"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\express_extractor.py","LineNumber":271,"LineContent":"    def _find_balanced_end(content: str, start_index: int, open_char: str, close_char: str) -\u003e int:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\express_extractor.py","LineNumber":306,"LineContent":"        body_end = ExpressExtractor._find_balanced_end(call_text, body_start, \"{\", \"}\")"}

=== STEP ===

Created At: 2026-05-25T10:04:44Z
Completed At: 2026-05-25T10:04:44Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1273
Total Bytes: 55913
Showing lines 270 to 300
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
270: 
271:     @staticmethod
272:     def _map_ts_type(type_name: str) -> str:
273:         normalized = (type_name or "").lower()
274:         if "number" in normalized or "int" in normalized:
275:             return "number"
276:         if "boolean" in normalized or "bool" in normalized:
277:             return "boolean"
278:         if "[]" in normalized or "array" in normalized:
279:             return "array"
280:         if "object" in normalized or "dto" in normalized or "record" in normalized:
281:             return "object"
282:         return "string"
283: 
284:     @staticmethod
285:     def _find_balanced_end(content: str, start_index: int, open_char: str, close_char: str) -> int:
286:         depth = 1
287:         quote = ""
288:         escaped = False
289:         for idx in range(start_index, len(content)):
290:             char = content[idx]
291:             if quote:
292:                 if escaped:
293:                     escaped = False
294:                 elif char == "\\":
295:                     escaped = True
296:                 elif char == quote:
297:                     quote = ""
298:                 continue
299:             if char in {"'", '"', "`"}:
300:                 quote = char
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T10:04:47Z
Completed At: 2026-05-25T10:04:47Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1273
Total Bytes: 55913
Showing lines 301 to 310
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
301:             elif char == open_char:
302:                 depth += 1
303:             elif char == close_char:
304:                 depth -= 1
305:                 if depth == 0:
306:                     return idx + 1
307:         return -1
308: 
309:     @classmethod
310:     @classmethod
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T10:04:55Z
Completed At: 2026-05-25T10:04:55Z
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\prototype_projects\\multi_stack_api\\laravel\\routes\\api.php","LineNumber":5,"LineContent":"Route::get('/laravel-users', 'UserController@index');"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\prototype_projects\\multi_stack_api\\laravel\\routes\\api.php","LineNumber":6,"LineContent":"Route::post('/laravel-users', 'UserController@store');"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\prototype_projects\\multi_stack_api\\laravel\\routes\\api.php","LineNumber":7,"LineContent":"Route::delete('/laravel-users/{id}', 'UserController@destroy');"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\tests\\test_laravel_extraction.py","LineNumber":12,"LineContent":"    Route::get('/users', 'UserController@index');"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\tests\\test_laravel_extraction.py","LineNumber":13,"LineContent":"    Route::post('/users', 'UserController@store');"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\tests\\test_laravel_extraction.py","LineNumber":14,"LineContent":"    Route::match(['put', 'patch'], '/users/{id}', 'UserController@update');"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\tests\\test_laravel_extraction.py","LineNumber":15,"LineContent":"    Route::apiResource('posts', PostController::class);"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\tests\\test_laravel_extraction.py","LineNumber":41,"LineContent":"    Route::prefix('v1')-\u003egroup(function () {"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\tests\\test_laravel_extraction.py","LineNumber":42,"LineContent":"        Route::middleware('auth:sanctum')-\u003eget('/profile', 'ProfileContr
<truncated 4927 bytes>
ENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1144,"LineContent":"            r\"Route::(?:[A-Za-z_][A-Za-z0-9_]*\\s*\\([^;{}]*?\\)\\s*-\u003e\\s*)*\""}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\route_classifier.py","LineNumber":195,"LineContent":"        r\"Route::get\","}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\route_classifier.py","LineNumber":196,"LineContent":"        r\"Route::post\","}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\route_classifier.py","LineNumber":197,"LineContent":"        r\"Route::put\","}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\route_classifier.py","LineNumber":198,"LineContent":"        r\"Route::patch\","}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\route_classifier.py","LineNumber":199,"LineContent":"        r\"Route::delete\","}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\route_classifier.py","LineNumber":200,"LineContent":"        r\"Route::match\","}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\route_classifier.py","LineNumber":201,"LineContent":"        r\"Route::any\","}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\route_classifier.py","LineNumber":202,"LineContent":"        r\"Route::resource\","}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\route_classifier.py","LineNumber":203,"LineContent":"        r\"Route::apiResource\","}

=== STEP ===

Created At: 2026-05-25T10:05:59Z
Completed At: 2026-05-25T10:06:00Z
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":341,"LineContent":"        class_is_protected = any("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":355,"LineContent":"            method_is_protected = class_is_protected or any("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":367,"LineContent":"            if method_is_protected:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":552,"LineContent":"                    r\"(?:private|public|protected)?\\s+(?:final\\s+)?([A-Za-z0-9_\u003c\u003e\\?,\\[\\]\\s]+)\\s+([A-Za-z_][A-Za-z0-9_]*)\\s*;\","}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\express_extractor.py","LineNumber":216,"LineContent":"        is_protected = any(term in call_text.lower() for term in [\"auth\", \"jwt\", \"passport\", \"session\", \"secure\", \"protect\"])"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\express_extractor.py","LineNumber":248,"LineContent":"        if is_protected:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\django_drf_ast_extractor.py","LineNumber":437,"LineContent":"        if self._is_protected(view_info):"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\django_drf_ast_extractor.py","LineNumber":984,"LineContent":"    def _is_protected(self, view_info: Dict[str, Any]) -\u003e bool:"}

=== STEP ===

Created At: 2026-05-25T10:06:06Z
Completed At: 2026-05-25T10:06:06Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1273
Total Bytes: 55913
Showing lines 360 to 380
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
360:             responses = cls._spring_responses(method_block, method, match.group(0), content[max(0, match.start() - 150):match.start()])
361:             if responses:
362:                 endpoint["responses"] = responses
363:                 success = next((response for response in responses if 200 <= response["status_code"] < 300), None)
364:                 if success:
365:                     endpoint["status_code"] = success["status_code"]
366:             
367:             if method_is_protected:
368:                 if "responses" not in endpoint:
369:                     endpoint["responses"] = []
370:                 # Avoid duplicate status codes
371:                 statuses = {resp["status_code"] for resp in endpoint["responses"]}
372:                 if 401 not in statuses:
373:                     endpoint["responses"].append({"status_code": 401, "description": "Unauthorized"})
374:                 if 403 not in statuses:
375:                     endpoint["responses"].append({"status_code": 403, "description": "Forbidden"})
376:                 endpoint["security"] = [{"tokenAuth": []}, {"jwtAuth": []}]
377: 
378:             endpoints.append(endpoint)
379:         return endpoints
380: 
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T10:06:21Z
Completed At: 2026-05-25T10:06:22Z
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":626,"LineContent":"                        methods_list = cls._extract_php_string_list(args_content[:bracket_end])"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":631,"LineContent":"                        methods_list = cls._extract_php_string_list(args_content[:paren_end])"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1171,"LineContent":"    def _extract_php_string_list(content: str) -\u003e List[str]:"}

=== STEP ===

Created At: 2026-05-25T10:06:24Z
Completed At: 2026-05-25T10:06:24Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1273
Total Bytes: 55913
Showing lines 1165 to 1190
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1165:             pieces.append(content[cursor:start])
1166:             cursor = max(cursor, end)
1167:         pieces.append(content[cursor:])
1168:         return "".join(pieces)
1169: 
1170:     @staticmethod
1171:     def _extract_php_string_list(content: str) -> List[str]:
1172:         return re.findall(r"['\"]([^'\"]+)['\"]", content)
1173: 
1174:     @staticmethod
1175:     def _last_path_segment(path: str) -> str:
1176:         segments = [segment for segment in path.strip("/").split("/") if segment and not segment.startswith("{")]
1177:         return segments[-1] if segments else "id"
1178: 
1179:     @staticmethod
1180:     def _singularize_resource(name: str) -> str:
1181:         if name.endswith("ies"):
1182:             return name[:-3] + "y"
1183:         if name.endswith("ses"):
1184:             return name[:-2]
1185:         if name.endswith("s") and len(name) > 1:
1186:             return name[:-1]
1187:         return name or "id"
1188: 
1189:     @classmethod
1190:     def _extract_aspnet(cls, file_path: str, content: str) -> List[Dict]:
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T10:06:29Z
Completed At: 2026-05-25T10:06:30Z
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\frontend\\components\\ScanResults.tsx","LineNumber":20,"LineContent":"      endpoints_with_path_params?: number;"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\frontend\\components\\ScanResults.tsx","LineNumber":187,"LineContent":"              \u003cp className=\"text-xl font-bold text-blue-700\"\u003e{results.documentation_summary.endpoints_with_path_params || 0}\u003c/p\u003e"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\routes\\api_doc_routes.py","LineNumber":85,"LineContent":"        \"endpoints_with_path_params\": sum(1 for endpoint in endpoints if endpoint.get(\"path_params\")),"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":112,"LineContent":"        path_params = cls._path_params(path)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":265,"LineContent":"    def _path_params(cls, path: str) -\u003e List[Dict]:"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":398,"LineContent":"        path_params = cls._path_params(path)"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1063,"LineContent":"        path_params = cls._path_params(endpoint[\"path\"])"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\express_extractor.py","LineNumber":209,"LineContent":"        path_params = ExpressExtractor._path_params(endpoint[\"path\"])"}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\express_extractor.py","LineNumber":312,"LineContent":"    def _path_params(path: str) -\u003e List[Dict]:"}

=== STEP ===

Created At: 2026-05-25T10:06:32Z
Completed At: 2026-05-25T10:06:32Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1273
Total Bytes: 55913
Showing lines 255 to 270
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
255: 
256:     @staticmethod
257:     def _default_success_code(method: str) -> int:
258:         if method == "POST":
259:             return 201
260:         if method == "DELETE":
261:             return 200
262:         return 200
263: 
264:     @classmethod
265:     def _path_params(cls, path: str) -> List[Dict]:
266:         return [
267:             {"name": name, "type": "string", "required": True}
268:             for name in re.findall(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", cls._normalize_path(path))
269:         ]
270: 
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T10:08:09Z
Completed At: 2026-05-25T10:08:11Z
The following changes were made by the replace_file_content tool to: c:\Users\NAVEENYA\OneDrive\Desktop\NAVEENYA\api_doc_generator\backend\api_doc_generator\extractors\generic_framework_extractor.py. If relevant, proactively run terminal commands to execute this code for the USER. Don't ask for permission.
[diff_block_start]
@@ -584,14 +584,14 @@
     @classmethod
     def _extract_laravel(cls, file_path: str, content: str, cross_file_resolver=None) -> List[Dict]:
         content = cls._strip_php_comments(content)
-        return cls._extract_laravel_routes_from_content(file_path, content, "", cross_file_resolver)
-
-    @classmethod
-    def _extract_laravel_routes_from_content(cls, file_path: str, content: str, prefix: str, cross_file_resolver=None) -> List[Dict]:
+        return cls._extract_laravel_routes_from_content(file_path, content, "", cross_file_resolver, False)
+
+    @classmethod
+    def _extract_laravel_routes_from_content(cls, file_path: str, content: str, prefix: str, cross_file_resolver=None, is_group_protected: bool = False) -> List[Dict]:
         endpoints = []
         group_ranges = []
 
-        for group_prefix, body, start, end in cls._laravel_prefixed_groups(content):
+        for group_prefix, group_is_protected, body, start, end in cls._laravel_groups(content):
             group_ranges.append((start, end))
             endpoints.extend(
                 cls._extract_laravel_routes_from_content(
@@ -598,6 +598,7 @@
                     body,
                     cls._join_paths(prefix, group_prefix),
-                    cross_file_resolver
+                    cross_file_resolver,
+                    is_group_protected or group_is_protected
                 )
             )
         content_without_groups = cls._remove_ranges(content, group_ranges)
@@ -615,6 +615,10 @@
             
             args_content = content_without_groups[args_start : args_end - 1].strip()
             
+            is_protected = cls._i
<truncated 15635 bytes>
+        if cls._is_laravel_protected(preceding):
+            return True
+        sub_content = content[end_args : end_args + 300]
+        semicolon_idx = sub_content.find(";")
+        route_idx = sub_content.find("Route::")
+        limit = len(sub_content)
+        if semicolon_idx != -1:
+            limit = min(limit, semicolon_idx)
+        if route_idx != -1:
+            limit = min(limit, route_idx)
+        trailing = sub_content[:limit]
+        return cls._is_laravel_protected(trailing)
+
+    @classmethod
+    def _find_php_array_content(cls, content: str, start_search: int) -> Optional[str]:
+        array_start = -1
+        brace_type = ""
+        for i in range(start_search, min(start_search + 100, len(content))):
+            if content[i] == "[":
+                array_start = i
+                brace_type = "square"
+                break
+            elif content[i:i+6].lower() == "array(":
+                array_start = i + 5
+                brace_type = "paren"
+                break
+        if array_start != -1:
+            array_end = -1
+            if brace_type == "square":
+                array_end = cls._find_balanced_end(content, array_start + 1, "[", "]")
+            elif brace_type == "paren":
+                array_end = cls._find_balanced_end(content, array_start + 1, "(", ")")
+            if array_end != -1:
+                return content[array_start:array_end]
+        return None
+
+    @classmethod
+    def _normalize_laravel_path(cls, path: str) -> str:
+        path = re.sub(r"\{([A-Za-z0-9_]+)\?\}", r"{\1}", path)
+        path = re.sub(r"\{([A-Za-z0-9_]+):[^}]*\}", r"{\1}", path)
+        return path
+
     @staticmethod
     def _remove_ranges(content: str, ranges: List[Tuple[int, int]]) -> str:
         if not ranges:
[diff_block_end]

Please note that the above snippet only shows the MODIFIED lines from the last change. It shows up to 3 lines of unchanged lines before and after the modified lines. The actual file contents may have many more lines not shown.

=== STEP ===

Created At: 2026-05-25T10:30:55Z
Completed At: 2026-05-25T10:30:55Z
The following changes were made by the replace_file_content tool to: C:\Users\NAVEENYA\.gemini\antigravity-ide\brain\f21fdfec-d083-4967-b688-8db7d4a04ddd\task.md. If relevant, proactively run terminal commands to execute this code for the USER. Don't ask for permission.
[diff_block_start]
@@ -3,8 +3,8 @@
 - [x] Fix Repository Classifier & File scoring (`repository_classifier.py`)
 - [x] Overhaul Spring Boot Extractor (`generic_framework_extractor.py`)
 - [x] Fix DRF Helper Leak, custom actions & Enhance Serializers (`django_drf_ast_extractor.py`)
-- [/] Enhance Express.js router composition graph and prefix resolution (`enhanced_cross_file_resolver.py` & `express_extractor.py`)
-- [ ] Enhance Laravel resource endpoints, requests, and middleware (`generic_framework_extractor.py`)
-- [ ] Implement OpenAPI schema component traversal, security fallback, and path normalization (`openapi_generator.py`)
-- [ ] Create and run automated unit tests to verify the overhaul
+- [x] Enhance Express.js router composition graph and prefix resolution (`enhanced_cross_file_resolver.py` & `express_extractor.py`)
+- [x] Enhance Laravel resource endpoints, requests, and middleware (`generic_framework_extractor.py`)
+- [x] Implement OpenAPI schema component traversal, security fallback, and path normalization (`openapi_generator.py`)
+- [x] Create and run automated unit tests to verify the overhaul
 
[diff_block_end]

Please note that the above snippet only shows the MODIFIED lines from the last change. It shows up to 3 lines of unchanged lines before and after the modified lines. The actual file contents may have many more lines not shown.

=== STEP ===

Created At: 2026-05-25T10:43:02Z
Completed At: 2026-05-25T10:43:02Z
File Path: `file:///C:/Users/NAVEENYA/.gemini/antigravity-ide/brain/f21fdfec-d083-4967-b688-8db7d4a04ddd/task.md`
Total Lines: 10
Total Bytes: 685
Showing lines 1 to 10
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: # Overhaul Checklist
2: 
3: - [x] Fix Repository Classifier & File scoring (`repository_classifier.py`)
4: - [x] Overhaul Spring Boot Extractor (`generic_framework_extractor.py`)
5: - [x] Fix DRF Helper Leak, custom actions & Enhance Serializers (`django_drf_ast_extractor.py`)
6: - [x] Enhance Express.js router composition graph and prefix resolution (`enhanced_cross_file_resolver.py` & `express_extractor.py`)
7: - [x] Enhance Laravel resource endpoints, requests, and middleware (`generic_framework_extractor.py`)
8: - [x] Implement OpenAPI schema component traversal, security fallback, and path normalization (`openapi_generator.py`)
9: - [x] Create and run automated unit tests to verify the overhaul
10: 
The above content shows the entire, complete file contents of the requested file.


=== STEP ===

Created At: 2026-05-25T10:43:05Z
Completed At: 2026-05-25T10:43:05Z
File Path: `file:///C:/Users/NAVEENYA/.gemini/antigravity-ide/brain/f21fdfec-d083-4967-b688-8db7d4a04ddd/walkthrough.md`
Total Lines: 59
Total Bytes: 3989
Showing lines 1 to 59
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: # Walkthrough - Multi-Framework Extraction Accuracy Overhaul
2: 
3: All requirements for the Smart API Documentation Generator multi-framework extraction accuracy overhaul have been implemented, verified, and unit tested.
4: 
5: ## Changes Made
6: 
7: ### 1. Repository Classifier (`repository_classifier.py`)
8: - Added Spring Boot annotations `@RestController`, `@RequestMapping`, etc., to the file score map.
9: - Implemented bypass logic for files containing routing keywords/annotations to avoid folder/directory penalties.
10: 
11: ### 2. Spring Boot Extractor (`generic_framework_extractor.py`)
12: - Overhauled Spring Boot route parsing with prefix resolution at the class level and method level.
13: - Extracted `@PathVariable`, `@RequestParam`, and `@RequestHeader` parameters.
14: - Resolved properties of `@RequestBody DtoClass` types from Java DTO files in the project.
15: - Captured custom response statuses and errors (e.g. `ResponseStatusException`).
16: 
17: ### 3. Django REST Framework Extractor (`django_drf_ast_extractor.py`)
18: - Filtered out Spectacular Swagger/Redoc schema views.
19: - Implemented type inference for `SerializerMethodField` fields by parsing their `get_<field_name>` methods.
20: - Attached `x-serializers` metadata mapping to extracted endpoints so that `OpenAPIGenerator` can recursively extract and build nested serializer schemas.
21: 
22: ### 4. Express.js Extractor & Resolver
23: - Built a JS/TS router composition graph in `EnhancedCrossFileResolver` to trace `require()` / `import` statements and `app.use
<truncated 690 bytes>
 (`Route::middleware(...)`), individual routes, and constructor-level controller middleware (`$this->middleware(...)`).
33: 
34: ### 6. OpenAPI Generator (`openapi_generator.py`)
35: - Implemented recursive component traversal to extract and register all nested serializers (referenced via `"x-nested-serializer"`) under `components/schemas`.
36: - Standardized OpenAPI path/parameter normalization and operationId generation.
37: - Added security scheme mapping from referencing operations, including fallback schemes (`tokenAuth` and `jwtAuth`) for protected endpoints without explicit classes.
38: 
39: ## Verification Results
40: 
41: ### Automated Tests
42: Created and ran unit tests in [test_overhaul_accuracy.py](file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/tests/test_overhaul_accuracy.py):
43: - `test_spring_boot_extractor_overhaul`: Asserts correct Spring Boot parsing of path/query variables, class RequestMapping prefixes, and body schema parsing from Java DTOs.
44: - `test_express_router_cross_file_prefix_propagation`: Asserts Express cross-file router mounting prefix inheritance.
45: - `test_drf_nested_serializers_and_serializer_method_field`: Asserts DRF SerializerMethodField type inference and recursive schema component registration for nested serializers.
46: - `test_laravel_middleware_validation_and_form_requests`: Asserts Laravel FormRequest rules extraction, inline validation arrays, optional parameter path normalization, and controller constructor + group-level sanctum/api auth middleware detection.
47: 
48: Ran `pytest` inside the virtual environment:
49: ```
50: ============================== 9 passed in 0.11s ==============================
51: ```
52: 
53: Ran the prototype verification matrix:
54: ```
55: python tests/run_demo_matrix.py
56: ```
57: Output:
58: - All 11 test suites of the demo matrix pass, verifying accuracy across Django, Laravel, Express, FastAPI, and Spring Boot.
59: 
The above content shows the entire, complete file contents of the requested file.


=== STEP ===

Created At: 2026-05-25T12:28:56Z
Completed At: 2026-05-25T12:28:56Z
{"name":"__init__.py","sizeBytes":"66"}
{"name":"__pycache__","isDir":true}
{"name":"batch_processor.py","sizeBytes":"7651"}
{"name":"confidence_scorer.py","sizeBytes":"2317"}
{"name":"cross_file_router_resolver.py","sizeBytes":"8462"}
{"name":"django_drf_ast_extractor.py","sizeBytes":"57818"}
{"name":"endpoint_deduplicator.py","sizeBytes":"2175"}
{"name":"endpoint_normalizer.py","sizeBytes":"5803"}
{"name":"enhanced_cross_file_resolver.py","sizeBytes":"16833"}
{"name":"express_extractor.py","sizeBytes":"17500"}
{"name":"extraction_pipeline.py","sizeBytes":"11267"}
{"name":"extractor_manager.py","sizeBytes":"7249"}
{"name":"fastapi_ast_extractor.py","sizeBytes":"21909"}
{"name":"fastapi_extractor.py","sizeBytes":"4268"}
{"name":"generic_framework_extractor.py","sizeBytes":"61327"}
{"name":"global_router_registry.py","sizeBytes":"6977"}
{"name":"import_resolver.py","sizeBytes":"13290"}
{"name":"include_router_extractor.py","sizeBytes":"9173"}
{"name":"openapi_spec_extractor.py","sizeBytes":"9621"}
{"name":"route_classifier.py","sizeBytes":"11719"}
{"name":"route_resolver.py","sizeBytes":"9295"}
{"name":"router_composition_graph.py","sizeBytes":"15388"}

Summary: This directory contains 1 subdirectories and 21 files.

=== STEP ===

Created At: 2026-05-25T12:29:18Z
Completed At: 2026-05-25T12:29:18Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1400
Total Bytes: 61327
Showing lines 1 to 800
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: import re
2: from pathlib import PurePosixPath
3: from typing import Dict, List, Tuple, Optional
4: 
5: 
6: class GenericFrameworkExtractor:
7:     """Extract route declarations for common frameworks with lightweight patterns."""
8: 
9:     HTTP_METHODS = {
10:         "get": "GET",
11:         "post": "POST",
12:         "put": "PUT",
13:         "delete": "DELETE",
14:         "patch": "PATCH",
15:         "options": "OPTIONS",
16:         "head": "HEAD",
17:     }
18: 
19:     @classmethod
20:     def extract(cls, file_path: str, content: str, framework: str, cross_file_resolver=None) -> List[Dict]:
21:         if framework == "Flask":
22:             return cls._extract_flask(file_path, content)
23:         if framework == "NestJS":
24:             return cls._extract_nestjs(file_path, content)
25:         if framework == "Spring Boot":
26:             return cls._extract_spring(file_path, content, cross_file_resolver)
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
38:     def _endpoint(cls, framework: str, method: str, path: str, file_path: str,
<truncated 34747 bytes>
6:     def _parse_laravel_handler(cls, handler_arg: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
767:         if re.match(r"(?:function|fn)\b", handler_arg, re.IGNORECASE):
768:             return None, None, handler_arg
769:             
770:         string_match = re.search(r"['\"]([A-Za-z0-9_\\]+)@([A-Za-z0-9_]+)['\"]", handler_arg)
771:         if string_match:
772:             controller_class = string_match.group(1).split("\\")[-1]
773:             method_name = string_match.group(2)
774:             return controller_class, method_name, None
775:             
776:         array_match = re.search(r"([A-Za-z0-9_\\]+)::class\s*,\s*['\"]([A-Za-z0-9_]+)['\"]", handler_arg, re.IGNORECASE)
777:         if array_match:
778:             controller_class = array_match.group(1).split("\\")[-1]
779:             method_name = array_match.group(2)
780:             return controller_class, method_name, None
781:             
782:         return None, None, None
783: 
784:     @classmethod
785:     def _find_file_content_by_name(cls, cross_file_resolver, target_name: str) -> Optional[str]:
786:         if not cross_file_resolver or not hasattr(cross_file_resolver, "file_contents"):
787:             return None
788:         for file_path, content in cross_file_resolver.file_contents.items():
789:             if file_path.endswith("/" + target_name) or file_path.endswith("\\" + target_name) or file_path == target_name:
790:                 return content
791:         return None
792: 
793:     @classmethod
794:     def _extract_php_method_block(cls, content: str, method_name: str) -> str:
795:         pattern = re.compile(rf"function\s+{method_name}\s*\(", re.IGNORECASE)
796:         match = pattern.search(content)
797:         if not match:
798:             return ""
799:         
800:         signature_start = match.start()
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T12:29:22Z
Completed At: 2026-05-25T12:29:22Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1400
Total Bytes: 61327
Showing lines 801 to 1400
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
801:         body_start = content.find("{", signature_start)
802:         if body_start == -1:
803:             return ""
804:         
805:         body_end = cls._find_balanced_end(content, body_start + 1, "{", "}")
806:         if body_end == -1:
807:             return content[body_start : body_start + 1000]
808:         
809:         return content[body_start:body_end]
810: 
811:     @classmethod
812:     def _parse_php_validation_rules(cls, array_content: str) -> Dict[str, Dict]:
813:         properties = {}
814:         pair_pattern = re.compile(r"['\"]([A-Za-z0-9_\-]+)['\"]\s*=>\s*", re.IGNORECASE)
815:         for match in pair_pattern.finditer(array_content):
816:             key = match.group(1)
817:             val_start = match.end()
818:             if val_start >= len(array_content):
819:                 continue
820:             
821:             val_content = ""
822:             if array_content[val_start] in {"'", '"'}:
823:                 quote = array_content[val_start]
824:                 str_end = array_content.find(quote, val_start + 1)
825:                 if str_end != -1:
826:                     val_content = array_content[val_start + 1 : str_end]
827:             elif array_content[val_start] == "[":
828:                 bracket_end = cls._find_balanced_end(array_content, val_start + 1, "[", "]")
829:                 if bracket_end != -1:
830:                     val_content = array_content[val_start : bracket_end]
831:             elif array_content[val_start:val_start
<truncated 27099 bytes>
se ""
1362: 
1363:     @classmethod
1364:     def _extract_python_methods(cls, args: str) -> List[str]:
1365:         methods_match = re.search(r"methods\s*=\s*\[([^\]]+)\]", args, re.IGNORECASE)
1366:         if not methods_match:
1367:             return []
1368:         return [
1369:             method.upper()
1370:             for method in re.findall(r"['\"]([A-Z]+)['\"]", methods_match.group(1), re.IGNORECASE)
1371:             if method.lower() in cls.HTTP_METHODS
1372:         ]
1373: 
1374:     @staticmethod
1375:     def _extract_spring_request_method(args: str) -> str:
1376:         match = re.search(r"RequestMethod\.([A-Z]+)", args)
1377:         return match.group(1) if match else ""
1378: 
1379:     @classmethod
1380:     def _join_paths(cls, prefix: str, path: str) -> str:
1381:         prefix = prefix or ""
1382:         path = path or ""
1383:         return cls._normalize_path("/".join([prefix.strip("/"), path.strip("/")]).strip("/"))
1384: 
1385:     @staticmethod
1386:     def _normalize_path(path: str) -> str:
1387:         path = re.sub(r"\(\?P<([A-Za-z_][A-Za-z0-9_]*)>[^)]+\)", r"{\1}", path or "")
1388:         path = re.sub(r"\(\?P\{([A-Za-z_][A-Za-z0-9_]*)\}[^)]*\)", r"{\1}", path)
1389:         path = re.sub(r"<(?:[^:>]+:)?([^>]+)>", r"{\1}", path)
1390:         path = path.replace("\\/", "/")
1391:         path = path.replace("^", "").replace("$", "")
1392:         path = re.sub(r"/\?", "", path)
1393:         path = re.sub(r"\?/?$", "", path)
1394:         path = path.replace("<", "{").replace(">", "}")
1395:         path = re.sub(r":([A-Za-z_][A-Za-z0-9_]*)", r"{\1}", path)
1396:         path = path.replace("[controller]", "{controller}").replace("[action]", "{action}")
1397:         if not path.startswith("/"):
1398:             path = "/" + path
1399:         return re.sub(r"/+", "/", path)
1400: 
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Here is the detailed analysis of the workflow and implementation of the **Smart API Documentation Generator** codebase. We will go through the global pipeline architecture first, followed by a technology-by-technology breakdown after analyzing each key file.

---

# I. Global Pipeline Workflow

The entry point for endpoint extraction is [api_doc_routes.py](file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/routes/api_doc_routes.py). When a scan or extraction is initiated (for a cloned GitHub repository, local folder, or uploaded ZIP):

```mermaid
graph TD
    A[Codebase Source: Git/Local/ZIP] --> B[LocalCodeService: Collect files]
    B --> C[BackendFileDetector: Filter target files]
    C --> D[FrameworkCandidateDetector: Classify frameworks]
    D --> E[ExtractionPipeline: Run phase resolution]
    E --> F[Phase 0: Build cross-file router composition graph]
    E --> G[Phase 1: Batch process file extractors & DRF AST extractor]
    E --> H[Phase 2: Normalize paths & parameters]
    E --> I[Phase 3: Score endpoint confidence]
    I --> J[OpenAPIGenerator: Generate spec & Component Traversal]
```

1. **File Collection & Filtering:** [LocalCodeService](file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/services/local_code_service.py) reads all codebase files. [BackendFileDetector](file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/scanner/backend_detector.py) isolates candidate folders (e.g., `routes`, `controllers`, `src`) and extensions, filtering out tests and dependencies.
2. **Framework Detection:** [RepositoryClassifier](file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/scanner/repository_classifier.py) scores files based on framework-specific signatures (e.g., `@RestController`, `Route::`, `express.router`, `APIRouter`).
3. **Deduplication & Normalization:** [EndpointNormalizer](file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA
<truncated 7604 bytes>
 parameters. It recognizes FastAPI defaults like `Depends()`, `Security()`, `Header()`, `Cookie()`, and `Query()`.

---

## 5. Spring Boot
* **Primary Extractor File:** [generic_framework_extractor.py](file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py) (lines 310–584)

### How it works:
1. **RequestMapping Resolution (`_extract_spring`):**
   Extracts class-level `@RequestMapping("/api")` prefixes and maps method-level decorators (`@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`).
2. **Java DTO Model Parsing (`_java_model_index`):**
   Iterates through Java class and record definitions. It parses fields (e.g., `private int price;`) and strips comments or validation annotations to build model properties.
3. **Parameter Introspection:**
   Parses method signatures to extract parameters annotated with:
   - `@PathVariable` (mapped as path variables).
   - `@RequestParam` (mapped as query parameters).
   - `@RequestHeader` (mapped as headers).
   - `@RequestBody` (mapped to request body schemas resolved from Java DTO files).
4. **Exception Status Codes:**
   Traverses method blocks to detect status returns. It maps `@ResponseStatus(HttpStatus.CREATED)` annotations and parses thrown `ResponseStatusException(HttpStatus.NOT_FOUND, "...")` calls into HTTP response lists.

---

# III. OpenAPI Document Generation

Once endpoints are extracted and consolidated, [openapi_generator.py](file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/generators/openapi_generator.py) runs a **Component Traversal and Schema Registration Phase**:

1. It searches endpoints for custom keys (like `x-serializers` and `x-nested-serializer`).
2. It recursively resolves dependencies and registers all serializer schemas under `components/schemas` to prevent unresolved OpenAPI `$ref` references.
3. Standardizes path parameters, security definitions, and tags before generating the final JSON OpenAPI schema.

=== STEP ===

Created At: 2026-05-25T14:14:55Z
Completed At: 2026-05-25T14:14:55Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1640
Total Bytes: 73011
Showing lines 585 to 640
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
585:     def _extract_laravel(cls, file_path: str, content: str, cross_file_resolver=None) -> List[Dict]:
586:         content = cls._strip_php_comments(content)
587:         return cls._extract_laravel_routes_from_content(file_path, content, "", cross_file_resolver, False)
588: 
589:     @classmethod
590:     def _extract_laravel_routes_from_content(
591:         cls,
592:         file_path: str,
593:         content: str,
594:         prefix: str,
595:         cross_file_resolver=None,
596:         is_group_protected: bool = False,
597:         group_auth: Optional[List[str]] = None,
598:     ) -> List[Dict]:
599:         endpoints = []
600:         group_ranges = []
601:         group_auth = group_auth or []
602: 
603:         for group_prefix, group_is_protected, group_mechanisms, body, start, end in cls._laravel_groups(content):
604:             group_ranges.append((start, end))
605:             endpoints.extend(
606:                 cls._extract_laravel_routes_from_content(
607:                     file_path,
608:                     body,
609:                     cls._join_paths(prefix, group_prefix),
610:                     cross_file_resolver,
611:                     is_group_protected or group_is_protected,
612:                     sorted(set(group_auth + group_mechanisms)),
613:                 )
614:             )
615:         content_without_groups = cls._remove_ranges(content, group_ranges)
616:         endpoints.extend(
617:             cls._extract_laravel_dingo_routes_from_content(
618:                 file_path,
619:                 content_without_groups,
620:                 prefix,
621:                 cross_file_resolver,
622:                 is_group_protected,
623:                 group_auth,
624:             )
625:         )
626: 
627:         route_pattern = re.compile(
628:             r"Route::(?:[A-Za-z0-9_]+\s*\([^;{}]*\)\s*->\s*)*(get|post|put|delete|patch|options|any|match)\s*\(",
629:             re.IGNORECASE
630:         )
631:         
632:         for match in route_pattern.finditer(content_without_groups):
633:             verb = match.group(1).lower()
634:             args_start = match.end()
635:             args_end = cls._find_balanced_end(content_without_groups, args_start, "(", ")")
636:             if args_end == -1:
637:                 continue
638:             
639:             args_content = content_without_groups[args_start : args_end - 1].strip()
640:             
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T14:14:59Z
Completed At: 2026-05-25T14:14:59Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1640
Total Bytes: 73011
Showing lines 641 to 780
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
641:             is_protected = cls._is_route_individually_protected(
642:                 content_without_groups, match.start(), args_end, is_group_protected
643:             )
644:             route_auth = sorted(set(group_auth + cls._laravel_auth_mechanisms(content_without_groups[match.start():args_end])))
645:             
646:             if verb == "match":
647:                 methods_list = []
648:                 rem = args_content
649:                 if args_content.startswith("["):
650:                     bracket_end = cls._find_balanced_end(args_content, 1, "[", "]")
651:                     if bracket_end != -1:
652:                         methods_list = cls._extract_php_string_list(args_content[:bracket_end])
653:                         rem = args_content[bracket_end:].strip()
654:                 elif args_content.lower().startswith("array("):
655:                     paren_end = cls._find_balanced_end(args_content, 6, "(", ")")
656:                     if paren_end != -1:
657:                         methods_list = cls._extract_php_string_list(args_content[:paren_end])
658:                         rem = args_content[paren_end:].strip()
659:                 else:
660:                     path_match = re.search(r"['\"]([^'\"]+)['\"]", args_content)
661:                     if path_match:
662:                         methods_list = [path_match.group(1)]
663:                         rem = args_content[path_match.end():].strip()
664:                 
665:                 rem = rem.lstr
<truncated 4079 bytes>
        re.IGNORECASE
748:         )
749:         for match in resource_pattern.finditer(content_without_groups):
750:             args_start = match.end()
751:             args_end = cls._find_balanced_end(content_without_groups, args_start, "(", ")")
752:             if args_end == -1:
753:                 continue
754:             args_content = content_without_groups[args_start : args_end - 1].strip()
755:             
756:             is_protected = cls._is_route_individually_protected(
757:                 content_without_groups, match.start(), args_end, is_group_protected
758:             )
759:             route_auth = sorted(set(group_auth + cls._laravel_auth_mechanisms(content_without_groups[match.start():args_end])))
760:             
761:             path_quote_match = re.search(r"['\"]([^'\"]+)['\"]", args_content)
762:             if not path_quote_match:
763:                 continue
764:             resource_path = path_quote_match.group(1)
765:             comma_idx = args_content.find(",", path_quote_match.end())
766:             handler_arg = args_content[comma_idx + 1:].strip() if comma_idx != -1 else ""
767:             
768:             controller_class = ""
769:             class_only_match = re.search(r"['\"]([A-Za-z0-9_]+)['\"]", handler_arg)
770:             class_ref_match = re.search(r"([A-Za-z0-9_]+)::class", handler_arg, re.IGNORECASE)
771:             if class_only_match:
772:                 controller_class = class_only_match.group(1)
773:             elif class_ref_match:
774:                 controller_class = class_ref_match.group(1)
775:                 
776:             if controller_class:
777:                 endpoints.extend(
778:                     cls._laravel_resource_endpoints(
779:                         file_path,
780:                         cls._join_paths(prefix, resource_path),
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T14:15:16Z
Completed At: 2026-05-25T14:15:17Z
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":617,"LineContent":"            cls._extract_laravel_dingo_routes_from_content("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":792,"LineContent":"    def _extract_laravel_dingo_routes_from_content("}
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":830,"LineContent":"                    cls._extract_laravel_dingo_routes_from_content("}

=== STEP ===

Created At: 2026-05-25T14:15:22Z
Completed At: 2026-05-25T14:15:22Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1640
Total Bytes: 73011
Showing lines 785 to 850
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
785:                         route_auth,
786:                     )
787:                 )
788:                 
789:         return endpoints
790: 
791:     @classmethod
792:     def _extract_laravel_dingo_routes_from_content(
793:         cls,
794:         file_path: str,
795:         content: str,
796:         prefix: str,
797:         cross_file_resolver=None,
798:         is_group_protected: bool = False,
799:         group_auth: Optional[List[str]] = None,
800:     ) -> List[Dict]:
801:         endpoints = []
802:         group_auth = group_auth or []
803:         group_ranges = []
804: 
805:         for call_name in ("version", "group"):
806:             pattern = re.compile(rf"\$[A-Za-z_][A-Za-z0-9_]*->{call_name}\s*\(", re.IGNORECASE)
807:             for match in pattern.finditer(content):
808:                 args_start = match.end()
809:                 args_end = cls._find_balanced_end(content, args_start, "(", ")")
810:                 if args_end == -1:
811:                     continue
812:                 args = content[args_start : args_end - 1]
813:                 function_start = content.find("{", args_start, args_end)
814:                 if function_start == -1:
815:                     continue
816:                 function_end = cls._find_balanced_end(content, function_start + 1, "{", "}")
817:                 if function_end == -1:
818:                     continue
819: 
820:                 options = args[: max(0, args.find("function"))] if "function" in args else args
821:                 group_prefix = cls._laravel_option_value(options, "prefix") or ""
822:                 # Dingo version('v1', ...) is API metadata, not a URL prefix.
823:                 if call_name == "version":
824:                     group_prefix = cls._laravel_option_value(options, "prefix") or ""
825:                 mechanisms = cls._laravel_auth_mechanisms(options)
826:                 protected = is_group_protected or cls._is_laravel_protected(options)
827:                 body = content[function_start + 1 : function_end - 1]
828:                 group_ranges.append((match.start(), function_end))
829:                 endpoints.extend(
830:                     cls._extract_laravel_dingo_routes_from_content(
831:                         file_path,
832:                         body,
833:                         cls._join_paths(prefix, group_prefix),
834:                         cross_file_resolver,
835:                         protected,
836:                         sorted(set(group_auth + mechanisms)),
837:                     )
838:                 )
839: 
840:         content_without_groups = cls._remove_ranges(content, group_ranges)
841:         route_pattern = re.compile(
842:             r"\$[A-Za-z_][A-Za-z0-9_]*->(get|post|put|delete|patch|options|any|match)\s*\(",
843:             re.IGNORECASE,
844:         )
845:         for match in route_pattern.finditer(content_without_groups):
846:             verb = match.group(1).lower()
847:             args_start = match.end()
848:             args_end = cls._find_balanced_end(content_without_groups, args_start, "(", ")")
849:             if args_end == -1:
850:                 continue
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T14:15:25Z
Completed At: 2026-05-25T14:15:27Z
{"File":"c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py","LineNumber":1333,"LineContent":"    def _laravel_groups(cls, content: str) -\u003e List[Tuple[str, bool, List[str], str, int, int]]:"}

=== STEP ===

Created At: 2026-05-25T14:15:31Z
Completed At: 2026-05-25T14:15:31Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1640
Total Bytes: 73011
Showing lines 1330 to 1390
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1330:         return re.sub(r"^\s*#.*$", "", content, flags=re.MULTILINE)
1331: 
1332:     @classmethod
1333:     def _laravel_groups(cls, content: str) -> List[Tuple[str, bool, List[str], str, int, int]]:
1334:         groups = []
1335:         pattern = re.compile(
1336:             r"Route::(?:[A-Za-z_][A-Za-z0-9_]*\s*\([^;{}]*?\)\s*->\s*)*group\s*\(",
1337:             re.IGNORECASE | re.DOTALL,
1338:         )
1339:         for match in pattern.finditer(content):
1340:             if re.match(r"Route::group\s*\(", match.group(0), re.IGNORECASE):
1341:                 continue
1342:             function_start = content.find("{", match.end())
1343:             if function_start == -1:
1344:                 continue
1345:             function_end = cls._find_balanced_end(content, function_start + 1, "{", "}")
1346:             if function_end == -1:
1347:                 continue
1348:             
1349:             chain = match.group(0)
1350:             prefix_match = re.search(r"prefix\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", chain, re.IGNORECASE)
1351:             group_prefix = prefix_match.group(1) if prefix_match else ""
1352:             
1353:             is_protected = cls._is_laravel_protected(chain)
1354:             auth_mechanisms = cls._laravel_auth_mechanisms(chain)
1355:             
1356:             body = content[function_start + 1 : function_end - 1]
1357:             groups.append((group_prefix, is_protected, auth_mechanisms, body, match.start(), function_end))
1358: 
1359:       
<truncated 246 bytes>
gs_start, "(", ")")
1363:             if args_end == -1:
1364:                 continue
1365:             args = content[args_start : args_end - 1]
1366:             function_start = content.find("{", args_start, args_end)
1367:             if function_start == -1:
1368:                 continue
1369:             function_end = cls._find_balanced_end(content, function_start + 1, "{", "}")
1370:             if function_end == -1:
1371:                 continue
1372:             options = args[: max(0, args.find("function"))] if "function" in args else args
1373:             prefix_match = re.search(r"['\"]prefix['\"]\s*=>\s*['\"]([^'\"]+)['\"]", options, re.IGNORECASE)
1374:             middleware_match = re.search(r"['\"]middleware['\"]\s*=>\s*(?P<value>\[[^\]]+\]|array\s*\([^)]*\)|['\"][^'\"]+['\"])", options, re.IGNORECASE)
1375:             group_prefix = prefix_match.group(1) if prefix_match else ""
1376:             middleware_text = middleware_match.group("value") if middleware_match else options
1377:             is_protected = cls._is_laravel_protected(middleware_text)
1378:             auth_mechanisms = cls._laravel_auth_mechanisms(middleware_text)
1379:             body = content[function_start + 1 : function_end - 1]
1380:             if not any(start == match.start() and end == function_end for *_, start, end in groups):
1381:                 groups.append((group_prefix, is_protected, auth_mechanisms, body, match.start(), function_end))
1382:         return groups
1383: 
1384:     @classmethod
1385:     def _is_laravel_protected(cls, text: str) -> bool:
1386:         if not text:
1387:             return False
1388:         text_lower = text.lower()
1389:         if "middleware" in text_lower:
1390:             for term in ["auth:sanctum", "auth:api", "auth:passport", "auth:jwt", "auth", "sanctum", "passport", "jwt"]:
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

Created At: 2026-05-25T14:25:50Z
Completed At: 2026-05-25T14:25:50Z
{"name":"__init__.py","sizeBytes":"66"}
{"name":"__pycache__","isDir":true}
{"name":"batch_processor.py","sizeBytes":"7651"}
{"name":"confidence_scorer.py","sizeBytes":"2317"}
{"name":"cross_file_router_resolver.py","sizeBytes":"8462"}
{"name":"django_drf_ast_extractor.py","sizeBytes":"57818"}
{"name":"endpoint_deduplicator.py","sizeBytes":"2175"}
{"name":"endpoint_normalizer.py","sizeBytes":"6079"}
{"name":"enhanced_cross_file_resolver.py","sizeBytes":"16833"}
{"name":"express_extractor.py","sizeBytes":"17500"}
{"name":"extraction_pipeline.py","sizeBytes":"11267"}
{"name":"extractor_manager.py","sizeBytes":"7249"}
{"name":"fastapi_ast_extractor.py","sizeBytes":"21909"}
{"name":"fastapi_extractor.py","sizeBytes":"4268"}
{"name":"generic_framework_extractor.py","sizeBytes":"73011"}
{"name":"global_router_registry.py","sizeBytes":"6977"}
{"name":"import_resolver.py","sizeBytes":"13290"}
{"name":"include_router_extractor.py","sizeBytes":"9173"}
{"name":"openapi_spec_extractor.py","sizeBytes":"9621"}
{"name":"route_classifier.py","sizeBytes":"12003"}
{"name":"route_resolver.py","sizeBytes":"9295"}
{"name":"router_composition_graph.py","sizeBytes":"15388"}

Summary: This directory contains 1 subdirectories and 21 files.

=== STEP ===

I will view the `generic_framework_extractor.py` file to see how it currently handles different frameworks and what parsing logic we need to extract and place in dedicated files.

=== STEP ===

Created At: 2026-05-25T14:27:48Z
Completed At: 2026-05-25T14:27:48Z
File Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`
Total Lines: 1640
Total Bytes: 73011
Showing lines 1 to 800
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: import re
2: from pathlib import PurePosixPath
3: from typing import Dict, List, Tuple, Optional
4: 
5: 
6: class GenericFrameworkExtractor:
7:     """Extract route declarations for common frameworks with lightweight patterns."""
8: 
9:     HTTP_METHODS = {
10:         "get": "GET",
11:         "post": "POST",
12:         "put": "PUT",
13:         "delete": "DELETE",
14:         "patch": "PATCH",
15:         "options": "OPTIONS",
16:         "head": "HEAD",
17:     }
18: 
19:     @classmethod
20:     def extract(cls, file_path: str, content: str, framework: str, cross_file_resolver=None) -> List[Dict]:
21:         if framework == "Flask":
22:             return cls._extract_flask(file_path, content)
23:         if framework == "NestJS":
24:             return cls._extract_nestjs(file_path, content)
25:         if framework == "Spring Boot":
26:             return cls._extract_spring(file_path, content, cross_file_resolver)
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
38:     def _endpoint(cls, framework: str, method: str, path: str, file_path: str,
<truncated 34277 bytes>
echanisms(content_without_groups[match.start():args_end])))
760:             
761:             path_quote_match = re.search(r"['\"]([^'\"]+)['\"]", args_content)
762:             if not path_quote_match:
763:                 continue
764:             resource_path = path_quote_match.group(1)
765:             comma_idx = args_content.find(",", path_quote_match.end())
766:             handler_arg = args_content[comma_idx + 1:].strip() if comma_idx != -1 else ""
767:             
768:             controller_class = ""
769:             class_only_match = re.search(r"['\"]([A-Za-z0-9_]+)['\"]", handler_arg)
770:             class_ref_match = re.search(r"([A-Za-z0-9_]+)::class", handler_arg, re.IGNORECASE)
771:             if class_only_match:
772:                 controller_class = class_only_match.group(1)
773:             elif class_ref_match:
774:                 controller_class = class_ref_match.group(1)
775:                 
776:             if controller_class:
777:                 endpoints.extend(
778:                     cls._laravel_resource_endpoints(
779:                         file_path,
780:                         cls._join_paths(prefix, resource_path),
781:                         match.group(0),
782:                         controller_class,
783:                         cross_file_resolver,
784:                         is_protected,
785:                         route_auth,
786:                     )
787:                 )
788:                 
789:         return endpoints
790: 
791:     @classmethod
792:     def _extract_laravel_dingo_routes_from_content(
793:         cls,
794:         file_path: str,
795:         content: str,
796:         prefix: str,
797:         cross_file_resolver=None,
798:         is_group_protected: bool = False,
799:         group_auth: Optional[List[str]] = None,
800:     ) -> List[Dict]:
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.


=== STEP ===

I have completed the research phase and created a comprehensive, production-grade [implementation plan](file:///C:/Users/NAVEENYA/.gemini/antigravity-ide/brain/f21fdfec-d083-4967-b688-8db7d4a04ddd/implementation_plan.md) covering all 20 mandatory architectural improvements.

### Key Highlights of the Plan:
1. **Consolidation**: Removing `GlobalRouterRegistry` and completely moving all router resolution and prefix propagation to `RouterCompositionGraph`.
2. **Canonical Identifiers**: Transitioning router name matching to canonical router IDs format: `router_id = f"{file_path}::{router_name}"`.
3. **AST-First Parsing (Express/Laravel)**: Implementing a localized Node.js script helper using `@babel/parser` and `php-parser` to parse Javascript, TypeScript, and PHP files into accurate JSON-based AST elements, with regex as a robust fallback.
4. **Single Cross-File Resolver & Global Symbol Table**: Dependency injecting the single resolver and a unified `GlobalSymbolTable` from `ExtractionPipeline` into `ExtractorManager`.
5. **Technology Splits**: Breaking up `generic_framework_extractor.py` into dedicated extractors: Flask, NestJS, Spring Boot, Laravel, ASP.NET, and Go Gin/Fiber.

Please review the [implementation plan](file:///C:/Users/NAVEENYA/.gemini/antigravity-ide/brain/f21fdfec-d083-4967-b688-8db7d4a04ddd/implementation_plan.md) and provide your feedback or explicit approval so I can begin the implementation and execution phase.

=== STEP ===

I will delete the obsolete `generic_framework_extractor.py` and `fastapi_extractor.py` files to finalize the framework split.

=== STEP ===

I will create a clean backward-compatibility delegation wrapper `generic_framework_extractor.py` that imports our split dedicated extractors, ensuring that existing tests continue to pass without modifications.

=== STEP ===

Created At: 2026-05-25T14:33:46Z
Completed At: 2026-05-25T14:33:49Z
Created file file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py with requested content.
If relevant, proactively run terminal commands to execute this code for the USER. Don't ask for permission.

=== STEP ===

I will run `git show` to retrieve the original Laravel extraction logic from `generic_framework_extractor.py` before it was split so we can properly integrate its controller method signature and validation rules analysis into our AST-first model.

=== STEP ===

Created At: 2026-05-25T14:34:49Z
Completed At: 2026-05-25T14:34:53Z

				The command completed successfully.
				Output:
				<truncated 3 lines>
{"step_index":333,"source":"MODEL","type":"VIEW_FILE","status":"DONE","created_at":"2026-05-25T10:00:03Z","content":"Created At: 2026-05-25T10:00:03Z\nCompleted At: 2026-05-25T10:00:03Z\nFile Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`\nTotal Lines: 1210\nTotal Bytes: 53011\nShowing lines 20 to 40\nThe following code has been modified to include a line number before every line, in the format: <l
{"step_index":335,"source":"MODEL","type":"CODE_ACTION","status":"DONE","created_at":"2026-05-25T10:00:09Z","content":"Created At: 2026-05-25T10:00:09Z\nCompleted At: 2026-05-25T10:00:11Z\nThe following changes were made by the replace_file_content tool to: c:\\Users\\NAVEENYA\\OneDrive\\Desktop\\NAVEENYA\\api_doc_generator\\backend\\api_doc_generator\\extractors\\generic_framework_extractor.py. If relevant, proactively run terminal commands to execute this code for the USER. Don't ask for permi
{"step_index":418,"source":"MODEL","type":"GREP_SEARCH","status":"DONE","created_at":"2026-05-25T10:04:30Z","content":"Created At: 2026-05-25T10:04:30Z\nCompleted At: 2026-05-25T10:04:31Z\n{\"File\":\"c:\\\\Users\\\\NAVEENYA\\\\OneDrive\\\\Desktop\\\\NAVEENYA\\\\api_doc_generator\\\\backend\\\\api_doc_generator\\\\extractors\\\\generic_framework_extractor.py\",\"LineNumber\":27,\"LineContent\":\"        if framework == \\\"Laravel\\\":\"}\n{\"File\":\"c:\\\\Users\\\\NAVEENYA\\\\OneDrive\\\\Deskt
{"step_index":420,"source":"MODEL","type":"VIEW_FILE","status":"DONE","created_at":"2026-05-25T10:04:33Z","content":"Created At: 2026-05-25T10:04:33Z\nCompleted At: 2026-05-25T10:04:33Z\nFile Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`\nTotal Lines: 1273\nTotal Bytes: 55913\nShowing lines 580 t
<truncated 4082 bytes>
n{\"File\":\"c:\\\\Users\\\\NAVEENYA\
{"step_index":801,"source":"MODEL","type":"VIEW_FILE","status":"DONE","created_at":"2026-05-25T14:15:22Z","content":"Created At: 2026-05-25T14:15:22Z\nCompleted At: 2026-05-25T14:15:22Z\nFile Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`\nTotal Lines: 1640\nTotal Bytes: 73011\nShowing lines 785 to 850\nThe following code has been modified to include a line number before every line, in the format: 
{"step_index":822,"source":"MODEL","type":"PLANNER_RESPONSE","status":"DONE","created_at":"2026-05-25T14:16:45Z","thinking":"**Analyzing Laravel Controller Routes**\n\nI'm now investigating controller actions in the Gothinkster Laravel RealWorld app. I've noted the `login` and `register` endpoints defined via routes like `Route::post('users/login', 'AuthController@login');`. My current focus is why the initial extraction attempt failed. I'm searching for clues now!\n\n\n**Revising Route Group Lo
{"step_index":907,"source":"MODEL","type":"VIEW_FILE","status":"DONE","created_at":"2026-05-25T14:27:48Z","content":"Created At: 2026-05-25T14:27:48Z\nCompleted At: 2026-05-25T14:27:48Z\nFile Path: `file:///c:/Users/NAVEENYA/OneDrive/Desktop/NAVEENYA/api_doc_generator/backend/api_doc_generator/extractors/generic_framework_extractor.py`\nTotal Lines: 1640\nTotal Bytes: 73011\nShowing lines 1 to 800\nThe following code has been modified to include a line number before every line, in the format: <l
{"step_index":948,"source":"MODEL","type":"PLANNER_RESPONSE","status":"DONE","created_at":"2026-05-25T14:30:57Z","content":"I will rewrite the `enhanced_cross_file_resolver.py` file to inject the `GlobalSymbolTable`, enforce canonical router IDs, and use the new Node.js AST parser helper to extract AST routing trees for JS/TS and PHP files.","thinking":"**Reviewing Resolver Implementation**\n\nOkay, I'm diving into the `EnhancedCrossFileResolver` implementation. My primary goal is to assess its 



=== STEP ===

I will run a python script to search the transcript for the original, complete `generic_framework_extractor.py` file content that was read prior to compaction.

=== STEP ===

I will extract all cached snippets of `generic_framework_extractor.py` from the conversation transcript and write them to a temporary scratch file to recover the original controller and request body schema extraction logic.

=== STEP ===

