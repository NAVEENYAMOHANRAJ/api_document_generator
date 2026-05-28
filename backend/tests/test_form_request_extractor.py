"""
Tests for Laravel FormRequest extraction.

This test suite validates that the system correctly extracts
request body schemas from Laravel FormRequest classes.
"""

import pytest
from api_doc_generator.extractors.form_request_extractor import FormRequestExtractor


class TestFormRequestExtractor:
    """Test FormRequest schema extraction."""

    def test_extract_simple_form_request(self):
        """Extract schema from simple FormRequest."""
        content = """
        class StoreUserRequest extends FormRequest {
            public function rules() {
                return [
                    'name' => 'required|string|max:255',
                    'email' => 'required|email|unique:users',
                    'password' => 'required|min:8'
                ];
            }
        }
        """

        result = FormRequestExtractor.extract('StoreUserRequest.php', content)

        assert result is not None
        assert result['class_name'] == 'StoreUserRequest'
        assert result['detection_type'] == 'form_request'
        assert result['confidence'] == 0.95

        schema = result['schema']
        assert schema['type'] == 'object'
        assert 'name' in schema['properties']
        assert 'email' in schema['properties']
        assert 'password' in schema['properties']

    def test_extract_required_fields(self):
        """Extract required fields from FormRequest."""
        content = """
        class StoreUserRequest extends FormRequest {
            public function rules() {
                return [
                    'name' => 'required|string',
                    'email' => 'required|email',
                    'bio' => 'nullable|string'
                ];
            }
        }
        """

        result = FormRequestExtractor.extract('StoreUserRequest.php', content)
        schema = result['schema']

        assert 'name' in schema['required']
        assert 'email' in schema['required']
        assert 'bio' not in schema['required']

    def test_extract_field_types(self):
        """Extract field types from validation rules."""
        content = """
        class CreatePostRequest extends FormRequest {
            public function rules() {
                return [
                    'title' => 'required|string',
                    'content' => 'required|string',
                    'published' => 'boolean',
                    'views' => 'integer',
                    'rating' => 'numeric',
                    'tags' => 'array'
                ];
            }
        }
        """

        result = FormRequestExtractor.extract('CreatePostRequest.php', content)
        schema = result['schema']

        assert schema['properties']['title']['type'] == 'string'
        assert schema['properties']['published']['type'] == 'boolean'
        assert schema['properties']['views']['type'] == 'integer'
        assert schema['properties']['rating']['type'] == 'number'
        assert schema['properties']['tags']['type'] == 'array'

    def test_extract_constraints(self):
        """Extract field constraints from validation rules."""
        content = """
        class UpdateUserRequest extends FormRequest {
            public function rules() {
                return [
                    'name' => 'required|string|min:3|max:255',
                    'age' => 'integer|between:18,100',
                    'email' => 'required|email|unique:users'
                ];
            }
        }
        """

        result = FormRequestExtractor.extract('UpdateUserRequest.php', content)
        schema = result['schema']

        # Check min/max constraints
        assert schema['properties']['name']['minLength'] == 3
        assert schema['properties']['name']['maxLength'] == 255

        # Check between constraint
        assert schema['properties']['age']['minLength'] == 18
        assert schema['properties']['age']['maxLength'] == 100

        # Check unique constraint
        assert schema['properties']['email'].get('unique') == True

    def test_extract_email_format(self):
        """Extract email format from validation rules."""
        content = """
        class ContactRequest extends FormRequest {
            public function rules() {
                return [
                    'email' => 'required|email',
                    'website' => 'nullable|url'
                ];
            }
        }
        """

        result = FormRequestExtractor.extract('ContactRequest.php', content)
        schema = result['schema']

        assert schema['properties']['email']['format'] == 'email'
        assert schema['properties']['website']['format'] == 'uri'

    def test_extract_enum_values(self):
        """Extract enum values from in() rule."""
        content = """
        class FilterRequest extends FormRequest {
            public function rules() {
                return [
                    'status' => 'required|in:active,inactive,pending',
                    'role' => 'in:admin,user,guest'
                ];
            }
        }
        """

        result = FormRequestExtractor.extract('FilterRequest.php', content)
        schema = result['schema']

        assert 'enum' in schema['properties']['status']
        assert set(schema['properties']['status']['enum']) == {'active', 'inactive', 'pending'}

    def test_is_form_request(self):
        """Identify FormRequest classes."""
        form_request = "class StoreUserRequest extends FormRequest { }"
        not_form_request = "class UserController extends Controller { }"

        assert FormRequestExtractor._is_form_request(form_request) == True
        assert FormRequestExtractor._is_form_request(not_form_request) == False

    def test_extract_class_name(self):
        """Extract class name from FormRequest."""
        content = "class StoreUserRequest extends FormRequest { }"
        name = FormRequestExtractor._extract_class_name(content)
        assert name == 'StoreUserRequest'

    def test_build_request_body_model(self):
        """Build complete request body model."""
        schema = {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'email': {'type': 'string', 'format': 'email'}
            },
            'required': ['name', 'email']
        }

        model = FormRequestExtractor.build_request_body_model(schema)

        assert model['required'] == True
        assert model['schema'] == schema
        assert 'application/json' in model['content']

    def test_critical_issue_form_request_extraction(self):
        """
        CRITICAL TEST: FormRequest extraction should work.

        This validates that the system can extract request body schemas
        from Laravel FormRequest classes, which is currently missing.
        """
        content = """
        class StoreProductRequest extends FormRequest {
            public function rules() {
                return [
                    'name' => 'required|string|max:255',
                    'price' => 'required|numeric|min:0.01',
                    'description' => 'nullable|string',
                    'category_id' => 'required|exists:categories,id'
                ];
            }
        }
        """

        result = FormRequestExtractor.extract('StoreProductRequest.php', content)

        # Verify extraction worked
        assert result is not None
        assert result['class_name'] == 'StoreProductRequest'
        assert result['detection_type'] == 'form_request'

        # Verify schema structure
        schema = result['schema']
        assert schema['type'] == 'object'
        assert len(schema['properties']) == 4
        assert set(schema['required']) == {'name', 'price', 'category_id'}

        # Verify field types
        assert schema['properties']['name']['type'] == 'string'
        assert schema['properties']['price']['type'] == 'number'
        assert schema['properties']['description']['type'] == 'string'

        # Verify constraints
        assert schema['properties']['name']['maxLength'] == 255
        assert schema['properties']['price']['minimum'] == 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
