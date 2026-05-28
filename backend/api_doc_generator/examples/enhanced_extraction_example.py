"""
Example: Using Enhanced Extraction Pipeline

This example demonstrates how to use the enhanced extraction pipeline
to dynamically extract detailed API documentation from Laravel code.
"""

import json
from pathlib import Path
from typing import List

# Import the enhanced pipeline
from backend.api_doc_generator.extractors.enhanced_extraction_pipeline import EnhancedExtractionPipeline
from backend.api_doc_generator.generators.documentation_generator import DocumentationGenerator


def example_extract_laravel_api():
    """
    Example: Extract detailed API documentation from Laravel routes.
    """
    
    # Initialize the pipeline
    repo_path = "/path/to/laravel/project"
    pipeline = EnhancedExtractionPipeline(repo_path)
    
    # Get all PHP files in the repository
    repo_files = list(Path(repo_path).rglob("*.php"))
    repo_files = [str(f) for f in repo_files]
    
    # Extract endpoints from routes/api.php
    routes_file = f"{repo_path}/routes/api.php"
    endpoints = pipeline.extract_from_laravel_routes(routes_file, repo_files)
    
    # Print extracted endpoints
    print(f"Extracted {len(endpoints)} endpoints\n")
    
    for endpoint in endpoints:
        print(f"Method: {endpoint.get('method')}")
        print(f"Path: {endpoint.get('path')}")
        print(f"Handler: {endpoint.get('handler', {}).get('class')}@{endpoint.get('handler', {}).get('method')}")
        print(f"Confidence: {endpoint.get('confidence', 0.0):.2f}")
        
        # Request body
        if endpoint.get("requestBody"):
            print(f"Request Body: {json.dumps(endpoint['requestBody'], indent=2)}")
        
        # Response schema
        if endpoint.get("responses"):
            print(f"Responses: {json.dumps(endpoint['responses'], indent=2)}")
        
        # Status codes
        if endpoint.get("statusCodes"):
            print(f"Status Codes: {endpoint['statusCodes']}")
        
        # Authentication
        if endpoint.get("security"):
            print(f"Authentication: {endpoint['security']}")
        
        print("-" * 80)
    
    return endpoints


def example_generate_documentation(endpoints: List[dict]):
    """
    Example: Generate HTML and Markdown documentation.
    """
    
    # Generate HTML documentation
    html_doc = DocumentationGenerator.generate_html(
        endpoints,
        title="My API Documentation"
    )
    
    # Save HTML
    with open("api_documentation.html", "w") as f:
        f.write(html_doc)
    
    print("HTML documentation saved to api_documentation.html")
    
    # Generate Markdown documentation
    markdown_doc = DocumentationGenerator.generate_markdown(
        endpoints,
        title="My API Documentation"
    )
    
    # Save Markdown
    with open("api_documentation.md", "w") as f:
        f.write(markdown_doc)
    
    print("Markdown documentation saved to api_documentation.md")


def example_generate_report(endpoints: List[dict]):
    """
    Example: Generate extraction report.
    """
    
    pipeline = EnhancedExtractionPipeline()
    report = pipeline.generate_endpoint_report(endpoints)
    
    print("\n=== EXTRACTION REPORT ===\n")
    print(f"Total Endpoints: {report['total_endpoints']}")
    print(f"Average Confidence: {report['average_confidence']:.2f}")
    print(f"\nBy Method:")
    for method, count in report['by_method'].items():
        print(f"  {method}: {count}")
    
    print(f"\nBy Framework:")
    for framework, count in report['by_framework'].items():
        print(f"  {framework}: {count}")
    
    print(f"\nFeature Coverage:")
    print(f"  With Request Body: {report['with_request_body']}")
    print(f"  With Response Schema: {report['with_response_schema']}")
    print(f"  With Authentication: {report['with_authentication']}")
    print(f"  With Path Parameters: {report['with_path_parameters']}")
    
    return report


def example_export_openapi(endpoints: List[dict]):
    """
    Example: Export to OpenAPI 3.0 format.
    """
    
    pipeline = EnhancedExtractionPipeline()
    openapi_spec = pipeline.export_to_openapi(
        endpoints,
        title="My API",
        version="1.0.0"
    )
    
    # Save OpenAPI spec
    with open("openapi.json", "w") as f:
        json.dump(openapi_spec, f, indent=2)
    
    print("OpenAPI specification saved to openapi.json")
    
    return openapi_spec


def example_detailed_endpoint_analysis():
    """
    Example: Analyze a single endpoint in detail.
    """
    
    endpoint = {
        "method": "POST",
        "path": "/api/users",
        "handler": {
            "class": "App\\Http\\Controllers\\UserController",
            "method": "store"
        },
        "framework": "laravel",
        "confidence": 0.95,
        "requestBody": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "required": True,
                    "rules": "required|string|max:255"
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "required": True,
                    "rules": "required|email|unique:users"
                },
                "password": {
                    "type": "string",
                    "required": True,
                    "rules": "required|string|min:8"
                }
            },
            "required": ["name", "email", "password"],
            "source": "form_request",
            "confidence": 0.95
        },
        "responses": {
            200: {
                "type": "object",
                "resource": "UserResource",
                "source": "resource_class",
                "confidence": 0.90
            },
            422: {
                "type": "object",
                "source": "validation_error",
                "confidence": 0.85
            }
        },
        "statusCodes": [200, 422],
        "security": ["auth:api"],
        "pathParameters": [],
        "summary": "Create a new user",
        "description": "Create a new user account with email and password"
    }
    
    print("\n=== DETAILED ENDPOINT ANALYSIS ===\n")
    print(f"Endpoint: {endpoint['method']} {endpoint['path']}")
    print(f"Handler: {endpoint['handler']['class']}@{endpoint['handler']['method']}")
    print(f"Confidence: {endpoint['confidence']:.2f}")
    
    print("\nRequest Body:")
    for field, schema in endpoint['requestBody']['properties'].items():
        required = "✓" if schema.get('required') else "✗"
        print(f"  {field} ({schema['type']}) [{required}] - {schema.get('rules', '')}")
    
    print("\nResponses:")
    for status_code, response in endpoint['responses'].items():
        print(f"  {status_code}: {response.get('resource', response.get('source', 'unknown'))}")
    
    print("\nAuthentication:")
    for auth in endpoint['security']:
        print(f"  - {auth}")
    
    return endpoint


if __name__ == "__main__":
    # Run examples
    print("=" * 80)
    print("ENHANCED EXTRACTION PIPELINE EXAMPLES")
    print("=" * 80)
    
    # Example 1: Detailed endpoint analysis
    endpoint = example_detailed_endpoint_analysis()
    
    # Example 2: Extract from Laravel (requires actual Laravel project)
    # endpoints = example_extract_laravel_api()
    
    # Example 3: Generate documentation
    # example_generate_documentation(endpoints)
    
    # Example 4: Generate report
    # report = example_generate_report(endpoints)
    
    # Example 5: Export to OpenAPI
    # openapi_spec = example_export_openapi(endpoints)
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)
