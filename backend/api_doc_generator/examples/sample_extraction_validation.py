"""
Sample Extraction Validation - Demonstrates all extracted details.

This example shows a complete endpoint extraction with all details
from the sample API documentation image:
- Request headers (Authorization, Accept, etc.)
- Query parameters with types and descriptions
- Request body with field types and descriptions
- Response schemas with field types and descriptions
- Status codes with descriptions
- Authentication methods
- Middleware
- Tags and categories
- Rate limits
- Response examples
"""

from backend.api_doc_generator.extractors.extraction_validator import ExtractionValidator
import json


def create_sample_endpoint():
    """Create a sample endpoint with all extracted details."""
    return {
        "method": "POST",
        "path": "/api/users",
        "summary": "Create a new user",
        "description": "Create a new user account with email and password",
        "handler": {
            "class": "App\\Http\\Controllers\\UserController",
            "method": "store",
            "file": "/path/to/UserController.php"
        },
        "framework": "laravel",
        "confidence": 0.95,
        
        # Request headers
        "headers": [
            {
                "name": "Authorization",
                "in": "header",
                "required": True,
                "type": "string",
                "description": "Bearer token for authentication"
            },
            {
                "name": "Accept",
                "in": "header",
                "required": True,
                "type": "string",
                "description": "application/json"
            },
            {
                "name": "Content-Type",
                "in": "header",
                "required": True,
                "type": "string",
                "description": "application/json"
            }
        ],
        
        # Query parameters
        "queryParameters": [
            {
                "name": "include",
                "in": "query",
                "required": False,
                "type": "string",
                "description": "Include related resources (e.g., profile, settings)"
            },
            {
                "name": "fields",
                "in": "query",
                "required": False,
                "type": "string",
                "description": "Comma-separated list of fields to return"
            }
        ],
        
        # Path parameters
        "pathParameters": [],
        
        # Request body schema
        "requestBody": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "required": True,
                    "maximum": 255,
                    "description": "User's full name"
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "required": True,
                    "description": "User's email address (must be unique)"
                },
                "password": {
                    "type": "string",
                    "required": True,
                    "minimum": 8,
                    "description": "User's password (minimum 8 characters)"
                },
                "role": {
                    "type": "string",
                    "required": False,
                    "enum": ["user", "admin", "moderator"],
                    "description": "User's role"
                },
                "is_active": {
                    "type": "boolean",
                    "required": False,
                    "description": "Whether the user account is active"
                }
            },
            "required": ["name", "email", "password"],
            "source": "form_request",
            "confidence": 0.95
        },
        
        # Response schemas
        "responses": {
            200: {
                "type": "object",
                "description": "User created successfully",
                "resource": "UserResource",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description": "User ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "User's full name"
                        },
                        "email": {
                            "type": "string",
                            "description": "User's email address"
                        },
                        "role": {
                            "type": "string",
                            "description": "User's role"
                        },
                        "is_active": {
                            "type": "boolean",
                            "description": "Whether the user account is active"
                        },
                        "created_at": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Account creation timestamp"
                        }
                    }
                },
                "example": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john@example.com",
                    "role": "user",
                    "is_active": True,
                    "created_at": "2024-05-27T10:30:00Z"
                },
                "source": "resource_class",
                "confidence": 0.90
            },
            422: {
                "type": "object",
                "description": "Validation failed",
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Error message"
                        },
                        "errors": {
                            "type": "object",
                            "description": "Validation errors by field"
                        }
                    }
                },
                "example": {
                    "message": "The given data was invalid.",
                    "errors": {
                        "email": ["The email has already been taken."],
                        "password": ["The password must be at least 8 characters."]
                    }
                },
                "source": "validation_error",
                "confidence": 0.85
            },
            401: {
                "type": "object",
                "description": "Unauthorized - authentication required",
                "schema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Error message"
                        }
                    }
                },
                "example": {
                    "message": "Unauthenticated."
                },
                "source": "authentication_error",
                "confidence": 0.90
            }
        },
        
        # HTTP status codes
        "statusCodes": [200, 201, 422, 401],
        
        # Authentication
        "security": ["auth:api"],
        
        # Middleware
        "middleware": ["api", "auth:api"],
        
        # Tags/categories
        "tags": ["Users"],
        
        # Rate limiting
        "rateLimit": {
            "requests": 60,
            "period": "1 minute",
            "description": "Rate limit: 60 requests per 1 minute"
        }
    }


def validate_sample_endpoint():
    """Validate the sample endpoint and print report."""
    validator = ExtractionValidator()
    
    # Create sample endpoint
    endpoint = create_sample_endpoint()
    
    print("\n" + "=" * 80)
    print("SAMPLE ENDPOINT EXTRACTION VALIDATION")
    print("=" * 80)
    
    print(f"\nEndpoint: {endpoint['method']} {endpoint['path']}")
    print(f"Summary: {endpoint['summary']}")
    print(f"Handler: {endpoint['handler']['class']}@{endpoint['handler']['method']}")
    
    # Validate endpoint
    print("\n" + "-" * 80)
    print("ENDPOINT VALIDATION")
    print("-" * 80)
    endpoint_report = validator.validate_endpoint(endpoint)
    print(f"Coverage Score: {endpoint_report['coverage_score']:.1f}%")
    print(f"Required Fields Present: {len(endpoint_report['required_fields_present'])}/{len(validator.REQUIRED_FIELDS)}")
    print(f"Important Fields Present: {len(endpoint_report['important_fields_present'])}/{len(validator.IMPORTANT_FIELDS)}")
    
    # Validate request body
    print("\n" + "-" * 80)
    print("REQUEST BODY VALIDATION")
    print("-" * 80)
    request_body_report = validator.validate_request_body(endpoint.get("requestBody"))
    print(f"Score: {request_body_report['score']:.1f}%")
    print(f"Properties: {request_body_report['property_count']}")
    print(f"Properties with Description: {request_body_report['properties_with_description']}")
    print(f"Properties with Constraints: {request_body_report['properties_with_constraints']}")
    
    # Validate response schema
    print("\n" + "-" * 80)
    print("RESPONSE SCHEMA VALIDATION")
    print("-" * 80)
    response_schema_report = validator.validate_response_schema(endpoint.get("responses"))
    print(f"Score: {response_schema_report['score']:.1f}%")
    print(f"Status Codes: {response_schema_report['status_codes']}")
    print(f"Responses with Description: {response_schema_report['responses_with_description']}")
    print(f"Responses with Schema: {response_schema_report['responses_with_schema']}")
    
    # Validate parameters
    print("\n" + "-" * 80)
    print("PARAMETERS VALIDATION")
    print("-" * 80)
    parameter_report = validator.validate_parameters(endpoint)
    print(f"Score: {parameter_report['score']:.1f}%")
    print(f"Total Parameters: {parameter_report['total_parameters']}")
    print(f"Path Parameters: {parameter_report['path_parameters']}")
    print(f"Query Parameters: {parameter_report['query_parameters']}")
    print(f"Headers: {parameter_report['headers']}")
    
    # Validate authentication
    print("\n" + "-" * 80)
    print("AUTHENTICATION VALIDATION")
    print("-" * 80)
    authentication_report = validator.validate_authentication(endpoint)
    print(f"Score: {authentication_report['score']:.1f}%")
    print(f"Security Methods: {authentication_report['security_methods']}")
    print(f"Has Example Token: {authentication_report['has_example_token']}")
    
    # Generate full report
    print("\n" + "-" * 80)
    print("FULL EXTRACTION REPORT")
    print("-" * 80)
    full_report = validator.generate_validation_report([endpoint])
    validator.print_validation_report(full_report)
    
    # Print extracted details
    print("\n" + "=" * 80)
    print("EXTRACTED DETAILS")
    print("=" * 80)
    
    print("\nRequest Headers:")
    for header in endpoint.get("headers", []):
        print(f"  • {header['name']}: {header['description']}")
    
    print("\nQuery Parameters:")
    for param in endpoint.get("queryParameters", []):
        print(f"  • {param['name']} ({param['type']}): {param['description']}")
    
    print("\nRequest Body Fields:")
    for field_name, field_schema in endpoint.get("requestBody", {}).get("properties", {}).items():
        required = "✓" if field_schema.get("required") else "✗"
        print(f"  • {field_name} ({field_schema['type']}) [{required}]: {field_schema.get('description', '')}")
    
    print("\nResponse Status Codes:")
    for status_code, response in endpoint.get("responses", {}).items():
        print(f"  • {status_code}: {response.get('description', '')}")
    
    print("\nAuthentication:")
    for auth in endpoint.get("security", []):
        print(f"  • {auth}")
    
    print("\nMiddleware:")
    for mw in endpoint.get("middleware", []):
        print(f"  • {mw}")
    
    print("\nTags:")
    for tag in endpoint.get("tags", []):
        print(f"  • {tag}")
    
    if endpoint.get("rateLimit"):
        print("\nRate Limiting:")
        print(f"  • {endpoint['rateLimit']['description']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    validate_sample_endpoint()
