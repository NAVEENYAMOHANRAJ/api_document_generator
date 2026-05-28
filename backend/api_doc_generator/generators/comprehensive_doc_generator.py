"""
Comprehensive API Documentation Generator

Generates production-grade API documentation with all 10 sections:
1. Overview
2. Authentication
3. Endpoints
4. Error Handling
5. Rate Limiting
6. Data Models/Schemas
7. Pagination
8. Webhooks
9. Code Examples
10. Changelog & Versioning
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime


class ComprehensiveDocGenerator:
    """Generate complete API documentation from extracted data"""
    
    def __init__(self, api_data: Dict[str, Any]):
        self.api_data = api_data
        self.base_url = api_data.get("api", {}).get("baseUrl", "https://api.example.com")
        self.api_name = api_data.get("api", {}).get("name", "API")
        self.api_version = api_data.get("api", {}).get("version", "v1")
        self.framework = api_data.get("api", {}).get("framework", "Unknown")
    
    def generate_markdown(self) -> str:
        """Generate complete markdown documentation"""
        sections = [
            self._generate_overview(),
            self._generate_authentication(),
            self._generate_endpoints(),
            self._generate_error_handling(),
            self._generate_rate_limiting(),
            self._generate_data_models(),
            self._generate_pagination(),
            self._generate_webhooks(),
            self._generate_code_examples(),
            self._generate_changelog()
        ]
        
        return "\n\n".join(filter(None, sections))
    
    def generate_html(self) -> str:
        """Generate complete HTML documentation"""
        markdown = self.generate_markdown()
        # Convert markdown to HTML (simplified)
        html = self._markdown_to_html(markdown)
        return self._wrap_html(html)
    
    def generate_json(self) -> Dict[str, Any]:
        """Generate documentation as structured JSON"""
        return {
            "overview": self._get_overview_data(),
            "authentication": self._get_authentication_data(),
            "endpoints": self._get_endpoints_data(),
            "errorHandling": self._get_error_handling_data(),
            "rateLimiting": self._get_rate_limiting_data(),
            "dataModels": self._get_data_models_data(),
            "pagination": self._get_pagination_data(),
            "webhooks": self._get_webhooks_data(),
            "codeExamples": self._get_code_examples_data(),
            "changelog": self._get_changelog_data()
        }
    
    # ============================================================================
    # SECTION 1: OVERVIEW
    # ============================================================================
    
    def _generate_overview(self) -> str:
        """Generate Overview section"""
        api = self.api_data.get("api", {})
        versioning = self.api_data.get("versioning", {})
        
        doc = f"""# 1. Overview

## API Description
{api.get('description', 'REST API for managing resources.')}

## Base URL
```
{self.base_url}
```

## Supported Formats
- **JSON** (default) - `Content-Type: application/json`
- **XML** (if supported) - `Content-Type: application/xml`

## API Versioning Strategy
**Strategy:** {versioning.get('strategy', 'URI Versioning')}

**Current Version:** `{versioning.get('current', 'v1')}`

**Versioning Format:**
- Version in URL path: `/v1/`, `/v2/`, etc.
- Example: `{self.base_url}/users`

**Deprecated Versions:**
{self._format_deprecated_versions(versioning.get('deprecated', []))}

## Framework
**Built with:** {self.framework}

## Contact
{self._format_contact_info(api.get('contact', {}))}

## License
{api.get('license', {}).get('name', 'MIT')}
"""
        return doc
    
    def _get_overview_data(self) -> Dict[str, Any]:
        """Get overview data as structured object"""
        api = self.api_data.get("api", {})
        versioning = self.api_data.get("versioning", {})
        
        return {
            "name": self.api_name,
            "description": api.get("description", ""),
            "baseUrl": self.base_url,
            "version": self.api_version,
            "framework": self.framework,
            "supportedFormats": ["JSON", "XML"],
            "versioningStrategy": versioning.get("strategy", "URI"),
            "currentVersion": versioning.get("current", "v1"),
            "deprecatedVersions": versioning.get("deprecated", []),
            "contact": api.get("contact", {}),
            "license": api.get("license", {})
        }
    
    # ============================================================================
    # SECTION 2: AUTHENTICATION
    # ============================================================================
    
    def _generate_authentication(self) -> str:
        """Generate Authentication section"""
        auth_methods = self.api_data.get("authentication", [])
        
        if not auth_methods:
            return ""
        
        doc = "# 2. Authentication\n\n"
        
        for i, auth in enumerate(auth_methods, 1):
            doc += f"## {auth.get('type', 'Authentication Method')} ({i})\n\n"
            doc += f"**Scheme:** {auth.get('scheme', 'Bearer')}\n\n"
            doc += f"**Header:** `{auth.get('header', 'Authorization')}`\n\n"
            doc += f"**Format:** `{auth.get('format', 'Bearer <token>')}`\n\n"
            doc += f"**Description:** {auth.get('description', '')}\n\n"
            
            # Example
            doc += "### Example Request\n"
            doc += "```bash\n"
            doc += f"curl -X GET \"{self.base_url}/users\" \\\n"
            doc += f"  -H \"{auth.get('header', 'Authorization')}: {auth.get('format', 'Bearer <token>')}\"\n"
            doc += "```\n\n"
            
            # Token generation
            doc += "### How to Obtain Credentials\n"
            doc += "1. Register an account\n"
            doc += "2. Generate API key from dashboard\n"
            doc += "3. Use key in Authorization header\n\n"
            
            # Token expiry
            doc += "### Token Expiry & Refresh\n"
            doc += "- **Token Expiry:** 24 hours\n"
            doc += "- **Refresh Endpoint:** `POST /auth/refresh`\n\n"
            doc += "```json\n"
            doc += "{\n"
            doc += '  "refresh_token": "your_refresh_token_here"\n'
            doc += "}\n"
            doc += "```\n\n"
        
        return doc
    
    def _get_authentication_data(self) -> Dict[str, Any]:
        """Get authentication data as structured object"""
        return {
            "methods": self.api_data.get("authentication", []),
            "tokenExpiry": "24 hours",
            "refreshEndpoint": "POST /auth/refresh",
            "refreshExample": {
                "refresh_token": "your_refresh_token_here"
            }
        }
    
    # ============================================================================
    # SECTION 3: ENDPOINTS
    # ============================================================================
    
    def _generate_endpoints(self) -> str:
        """Generate Endpoints section"""
        endpoints = self.api_data.get("endpoints", [])
        
        if not endpoints:
            return ""
        
        doc = "# 3. Endpoints\n\n"
        
        # Group by tags
        grouped = self._group_endpoints_by_tag(endpoints)
        
        for tag, tag_endpoints in grouped.items():
            doc += f"## {tag or 'General'}\n\n"
            
            for endpoint in tag_endpoints:
                doc += self._generate_endpoint_doc(endpoint)
                doc += "\n"
        
        return doc
    
    def _generate_endpoint_doc(self, endpoint: Dict[str, Any]) -> str:
        """Generate documentation for a single endpoint"""
        method = endpoint.get("method", "GET")
        path = endpoint.get("path", "/")
        summary = endpoint.get("summary", "")
        description = endpoint.get("description", "")
        
        doc = f"### {method} {path}\n\n"
        doc += f"**Summary:** {summary}\n\n"
        
        if description:
            doc += f"**Description:** {description}\n\n"
        
        # Path Parameters
        path_params = endpoint.get("pathParameters", [])
        if path_params:
            doc += "#### Path Parameters\n\n"
            doc += "| Parameter | Type | Required | Description |\n"
            doc += "|-----------|------|----------|-------------|\n"
            for param in path_params:
                doc += f"| {param.get('name')} | {param.get('type', 'string')} | "
                doc += f"{'Yes' if param.get('required') else 'No'} | "
                doc += f"{param.get('description', '')} |\n"
            doc += "\n"
        
        # Query Parameters
        query_params = endpoint.get("queryParameters", [])
        if query_params:
            doc += "#### Query Parameters\n\n"
            doc += "| Parameter | Type | Required | Default | Description |\n"
            doc += "|-----------|------|----------|---------|-------------|\n"
            for param in query_params:
                doc += f"| {param.get('name')} | {param.get('type', 'string')} | "
                doc += f"{'Yes' if param.get('required') else 'No'} | "
                doc += f"{param.get('default', '-')} | "
                doc += f"{param.get('description', '')} |\n"
            doc += "\n"
        
        # Request Headers
        doc += "#### Request Headers\n\n"
        doc += "```\n"
        doc += "Authorization: Bearer <token>\n"
        doc += "Content-Type: application/json\n"
        doc += "Accept: application/json\n"
        doc += "```\n\n"
        
        # Request Body
        request_body = endpoint.get("requestBody")
        if request_body:
            doc += "#### Request Body\n\n"
            doc += "```json\n"
            doc += json.dumps(request_body.get("schema", {}), indent=2)
            doc += "\n```\n\n"
        
        # Example Request
        doc += "#### Example Request\n\n"
        doc += "```bash\n"
        doc += f"curl -X {method} \"{self.base_url}{path}\" \\\n"
        doc += "  -H \"Authorization: Bearer <token>\" \\\n"
        doc += "  -H \"Content-Type: application/json\"\n"
        doc += "```\n\n"
        
        # Example Response
        responses = endpoint.get("responses", [])
        if responses:
            doc += "#### Example Response\n\n"
            for response in responses:
                status = response.get("statusCode", 200)
                doc += f"**{status} {self._get_status_text(status)}**\n\n"
                doc += "```json\n"
                example = response.get("example", {})
                if example:
                    doc += json.dumps(example, indent=2)
                else:
                    doc += json.dumps(response.get("schema", {}), indent=2)
                doc += "\n```\n\n"
        
        # Error Responses
        error_responses = endpoint.get("errorResponses", {})
        if error_responses:
            doc += "#### Error Responses\n\n"
            for status, error in error_responses.items():
                doc += f"**{status}** - {error.get('message', 'Error')}\n\n"
        
        return doc
    
    def _get_endpoints_data(self) -> List[Dict[str, Any]]:
        """Get endpoints data as structured list"""
        return self.api_data.get("endpoints", [])
    
    # ============================================================================
    # SECTION 4: ERROR HANDLING
    # ============================================================================
    
    def _generate_error_handling(self) -> str:
        """Generate Error Handling section"""
        errors = self.api_data.get("errorDefinitions", [])
        
        doc = "# 4. Error Handling\n\n"
        doc += "## Error Response Format\n\n"
        doc += "All errors follow this standard format:\n\n"
        doc += "```json\n"
        doc += "{\n"
        doc += '  "error": {\n'
        doc += '    "code": 404,\n'
        doc += '    "message": "Resource not found",\n'
        doc += '    "details": "No resource exists with the provided ID"\n'
        doc += "  }\n"
        doc += "}\n"
        doc += "```\n\n"
        
        doc += "## Error Codes\n\n"
        doc += "| Code | Status | Meaning |\n"
        doc += "|------|--------|----------|\n"
        
        for error in errors:
            code = error.get("code", "UNKNOWN")
            status = error.get("status_code", 500)
            message = error.get("message", "")
            doc += f"| {code} | {status} | {message} |\n"
        
        doc += "\n"
        
        return doc
    
    def _get_error_handling_data(self) -> Dict[str, Any]:
        """Get error handling data as structured object"""
        return {
            "format": {
                "error": {
                    "code": "error_code",
                    "message": "error_message",
                    "details": "error_details"
                }
            },
            "definitions": self.api_data.get("errorDefinitions", [])
        }
    
    # ============================================================================
    # SECTION 5: RATE LIMITING
    # ============================================================================
    
    def _generate_rate_limiting(self) -> str:
        """Generate Rate Limiting section"""
        rate_limits = self.api_data.get("rateLimits", {})
        
        doc = "# 5. Rate Limiting\n\n"
        doc += "## Rate Limit Policy\n\n"
        doc += f"- **Limit:** {rate_limits.get('limit', 1000)} requests\n"
        doc += f"- **Window:** {rate_limits.get('window', '1 hour')}\n"
        doc += f"- **Description:** {rate_limits.get('description', '')}\n\n"
        
        doc += "## Rate Limit Headers\n\n"
        doc += "Every response includes rate limit information:\n\n"
        doc += "```\n"
        doc += "X-RateLimit-Limit: 1000\n"
        doc += "X-RateLimit-Remaining: 950\n"
        doc += "X-RateLimit-Reset: 1706184000\n"
        doc += "```\n\n"
        
        doc += "## Exceeding Rate Limits\n\n"
        doc += "When rate limit is exceeded, you'll receive a 429 response:\n\n"
        doc += "```json\n"
        doc += "{\n"
        doc += '  "error": {\n'
        doc += '    "code": 429,\n'
        doc += '    "message": "Rate limit exceeded",\n'
        doc += '    "details": "Retry after 60 seconds"\n'
        doc += "  }\n"
        doc += "}\n"
        doc += "```\n\n"
        
        return doc
    
    def _get_rate_limiting_data(self) -> Dict[str, Any]:
        """Get rate limiting data as structured object"""
        return {
            "policy": self.api_data.get("rateLimits", {}),
            "headers": {
                "X-RateLimit-Limit": "1000",
                "X-RateLimit-Remaining": "950",
                "X-RateLimit-Reset": "1706184000"
            }
        }
    
    # ============================================================================
    # SECTION 6: DATA MODELS / SCHEMAS
    # ============================================================================
    
    def _generate_data_models(self) -> str:
        """Generate Data Models section"""
        schemas = self.api_data.get("schemas", {})
        
        if not schemas:
            return ""
        
        doc = "# 6. Data Models / Schemas\n\n"
        
        for schema_name, schema_def in schemas.items():
            doc += f"## {schema_name} Object\n\n"
            doc += "| Field | Type | Description |\n"
            doc += "|-------|------|-------------|\n"
            
            if isinstance(schema_def, dict):
                for field_name, field_info in schema_def.items():
                    field_type = field_info.get("type", "string") if isinstance(field_info, dict) else "string"
                    description = field_info.get("description", "") if isinstance(field_info, dict) else ""
                    doc += f"| {field_name} | {field_type} | {description} |\n"
            
            doc += "\n"
        
        return doc
    
    def _get_data_models_data(self) -> Dict[str, Any]:
        """Get data models as structured object"""
        return self.api_data.get("schemas", {})
    
    # ============================================================================
    # SECTION 7: PAGINATION
    # ============================================================================
    
    def _generate_pagination(self) -> str:
        """Generate Pagination section"""
        doc = "# 7. Pagination\n\n"
        doc += "## Pagination Parameters\n\n"
        doc += "List endpoints support pagination using query parameters:\n\n"
        doc += "```\n"
        doc += "GET /users?page=2&limit=20\n"
        doc += "```\n\n"
        
        doc += "| Parameter | Type | Default | Description |\n"
        doc += "|-----------|------|---------|-------------|\n"
        doc += "| page | integer | 1 | Page number (1-indexed) |\n"
        doc += "| limit | integer | 20 | Items per page (max 100) |\n"
        doc += "| sort | string | - | Sort field (e.g., `created_at`) |\n"
        doc += "| order | string | asc | Sort order: `asc` or `desc` |\n\n"
        
        doc += "## Paginated Response Format\n\n"
        doc += "```json\n"
        doc += "{\n"
        doc += '  "data": [\n'
        doc += "    { /* resource objects */ }\n"
        doc += "  ],\n"
        doc += '  "pagination": {\n'
        doc += '    "total": 200,\n'
        doc += '    "page": 2,\n'
        doc += '    "limit": 20,\n'
        doc += '    "total_pages": 10,\n'
        doc += '    "next": "/users?page=3&limit=20",\n'
        doc += '    "prev": "/users?page=1&limit=20"\n'
        doc += "  }\n"
        doc += "}\n"
        doc += "```\n\n"
        
        return doc
    
    def _get_pagination_data(self) -> Dict[str, Any]:
        """Get pagination data as structured object"""
        return {
            "parameters": {
                "page": {"type": "integer", "default": 1},
                "limit": {"type": "integer", "default": 20},
                "sort": {"type": "string"},
                "order": {"type": "string", "default": "asc"}
            },
            "responseFormat": {
                "data": [],
                "pagination": {
                    "total": 0,
                    "page": 1,
                    "limit": 20,
                    "total_pages": 0,
                    "next": None,
                    "prev": None
                }
            }
        }
    
    # ============================================================================
    # SECTION 8: WEBHOOKS
    # ============================================================================
    
    def _generate_webhooks(self) -> str:
        """Generate Webhooks section"""
        webhooks = self.api_data.get("webhooks", [])
        
        if not webhooks:
            return ""
        
        doc = "# 8. Webhooks\n\n"
        doc += "## Webhook Events\n\n"
        
        for webhook in webhooks:
            event = webhook.get("event", "unknown")
            doc += f"### {event}\n\n"
            doc += f"**Description:** {webhook.get('description', '')}\n\n"
            doc += "**Payload Example:**\n\n"
            doc += "```json\n"
            doc += json.dumps(webhook.get("payload", {}), indent=2)
            doc += "\n```\n\n"
        
        return doc
    
    def _get_webhooks_data(self) -> List[Dict[str, Any]]:
        """Get webhooks data as structured list"""
        return self.api_data.get("webhooks", [])
    
    # ============================================================================
    # SECTION 9: CODE EXAMPLES
    # ============================================================================
    
    def _generate_code_examples(self) -> str:
        """Generate Code Examples section"""
        doc = "# 9. Code Examples\n\n"
        doc += "## Python\n\n"
        doc += "```python\n"
        doc += "import requests\n\n"
        doc += "headers = {\n"
        doc += '    "Authorization": "Bearer <token>",\n'
        doc += '    "Content-Type": "application/json"\n'
        doc += "}\n\n"
        doc += f"response = requests.get(\n"
        doc += f'    "{self.base_url}/users/123",\n'
        doc += "    headers=headers\n"
        doc += ")\n\n"
        doc += "data = response.json()\n"
        doc += "print(data)\n"
        doc += "```\n\n"
        
        doc += "## JavaScript\n\n"
        doc += "```javascript\n"
        doc += "const headers = {\n"
        doc += '  "Authorization": "Bearer <token>",\n'
        doc += '  "Content-Type": "application/json"\n'
        doc += "};\n\n"
        doc += "const response = await fetch(\n"
        doc += f'  "{self.base_url}/users/123",\n'
        doc += "  { headers }\n"
        doc += ");\n\n"
        doc += "const data = await response.json();\n"
        doc += "console.log(data);\n"
        doc += "```\n\n"
        
        doc += "## cURL\n\n"
        doc += "```bash\n"
        doc += f"curl -X GET \"{self.base_url}/users/123\" \\\n"
        doc += '  -H "Authorization: Bearer <token>" \\\n'
        doc += '  -H "Content-Type: application/json"\n'
        doc += "```\n\n"
        
        doc += "## PHP\n\n"
        doc += "```php\n"
        doc += "<?php\n"
        doc += "$ch = curl_init();\n"
        doc += f"curl_setopt($ch, CURLOPT_URL, \"{self.base_url}/users/123\");\n"
        doc += "curl_setopt($ch, CURLOPT_HTTPHEADER, [\n"
        doc += '    "Authorization: Bearer <token>",\n'
        doc += '    "Content-Type: application/json"\n'
        doc += "]);\n"
        doc += "$response = curl_exec($ch);\n"
        doc += "$data = json_decode($response, true);\n"
        doc += "print_r($data);\n"
        doc += "?>\n"
        doc += "```\n\n"
        
        doc += "## Go\n\n"
        doc += "```go\n"
        doc += "package main\n\n"
        doc += "import (\n"
        doc += '    "fmt"\n'
        doc += '    "io/ioutil"\n'
        doc += '    "net/http"\n'
        doc += ")\n\n"
        doc += "func main() {\n"
        doc += f'    req, _ := http.NewRequest("GET", "{self.base_url}/users/123", nil)\n'
        doc += '    req.Header.Add("Authorization", "Bearer <token>")\n'
        doc += "    client := &http.Client{}\n"
        doc += "    resp, _ := client.Do(req)\n"
        doc += "    body, _ := ioutil.ReadAll(resp.Body)\n"
        doc += "    fmt.Println(string(body))\n"
        doc += "}\n"
        doc += "```\n\n"
        
        return doc
    
    def _get_code_examples_data(self) -> Dict[str, str]:
        """Get code examples as structured object"""
        return {
            "python": "import requests\nheaders = {'Authorization': 'Bearer <token>'}\nresponse = requests.get(...)",
            "javascript": "const response = await fetch(..., {headers: {...}})",
            "curl": "curl -X GET ... -H 'Authorization: Bearer <token>'",
            "php": "curl_init(); curl_setopt(...)",
            "go": "http.NewRequest(...)"
        }
    
    # ============================================================================
    # SECTION 10: CHANGELOG & VERSIONING
    # ============================================================================
    
    def _generate_changelog(self) -> str:
        """Generate Changelog section"""
        changelog = self.api_data.get("changelog", [])
        
        doc = "# 10. Changelog & Versioning\n\n"
        doc += "## Version History\n\n"
        doc += "| Version | Date | Changes |\n"
        doc += "|---------|------|----------|\n"
        
        if changelog:
            for entry in changelog:
                version = entry.get("version", "v1.0")
                date = entry.get("date", datetime.now().strftime("%Y-%m-%d"))
                changes = entry.get("changes", [])
                changes_str = "; ".join(changes) if isinstance(changes, list) else str(changes)
                doc += f"| {version} | {date} | {changes_str} |\n"
        else:
            doc += "| v1.0 | 2024-01-01 | Initial release |\n"
        
        doc += "\n"
        
        return doc
    
    def _get_changelog_data(self) -> List[Dict[str, Any]]:
        """Get changelog data as structured list"""
        return self.api_data.get("changelog", [])
    
    # ============================================================================
    # HELPER METHODS
    # ============================================================================
    
    def _group_endpoints_by_tag(self, endpoints: List[Dict]) -> Dict[str, List[Dict]]:
        """Group endpoints by tag"""
        grouped = {}
        for endpoint in endpoints:
            tags = endpoint.get("tags", ["General"])
            for tag in tags:
                if tag not in grouped:
                    grouped[tag] = []
                grouped[tag].append(endpoint)
        return grouped
    
    def _format_contact_info(self, contact: Dict) -> str:
        """Format contact information"""
        if not contact:
            return "Contact information not provided"
        
        lines = []
        if contact.get("name"):
            lines.append(f"- **Name:** {contact['name']}")
        if contact.get("email"):
            lines.append(f"- **Email:** {contact['email']}")
        if contact.get("url"):
            lines.append(f"- **URL:** {contact['url']}")
        
        return "\n".join(lines) if lines else "Contact information not provided"
    
    def _format_deprecated_versions(self, deprecated: List) -> str:
        """Format deprecated versions"""
        if not deprecated:
            return "None"
        return ", ".join(deprecated)
    
    def _get_status_text(self, status_code: int) -> str:
        """Get HTTP status text"""
        status_map = {
            200: "OK",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            429: "Too Many Requests",
            500: "Internal Server Error"
        }
        return status_map.get(status_code, "Unknown")
    
    def _markdown_to_html(self, markdown: str) -> str:
        """Convert markdown to HTML (simplified)"""
        # This is a simplified conversion
        # In production, use a proper markdown library like `markdown2` or `mistune`
        html = markdown
        html = html.replace("# ", "<h1>").replace("\n", "</h1>\n")
        html = html.replace("## ", "<h2>").replace("\n", "</h2>\n")
        html = html.replace("### ", "<h3>").replace("\n", "</h3>\n")
        html = html.replace("**", "<strong>").replace("**", "</strong>")
        html = html.replace("`", "<code>").replace("`", "</code>")
        return html
    
    def _wrap_html(self, html: str) -> str:
        """Wrap HTML with proper structure"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.api_name} API Documentation</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
        h1, h2, h3 {{ color: #0066cc; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 12px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #f4f4f4; }}
    </style>
</head>
<body>
    {html}
</body>
</html>
"""
