"""Tests for PHP array parser."""

import pytest
from api_doc_generator.extractors.php_array_parser import PHPArrayParser
from api_doc_generator.extractors.base_parser import tokenize_code


class TestPHPArrayParser:
    """Test PHP array parsing functionality."""

    def test_parse_simple_array(self):
        """Test parsing simple PHP array."""
        code = "['name' => 'John', 'email' => 'john@example.com']"
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert result['name'] == 'John'
        assert result['email'] == 'john@example.com'

    def test_parse_array_syntax(self):
        """Test parsing array() syntax."""
        code = "array('key' => 'value', 'number' => 42)"
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert result['key'] == 'value'
        assert result['number'] == 42

    def test_parse_nested_array(self):
        """Test parsing nested arrays."""
        code = "['user' => ['name' => 'John', 'email' => 'john@example.com']]"
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert isinstance(result['user'], dict)
        assert result['user']['name'] == 'John'
        assert result['user']['email'] == 'john@example.com'

    def test_parse_validation_rules(self):
        """Test parsing Laravel validation rules."""
        code = """[
            'email' => 'required|email',
            'password' => 'required|min:8',
            'name' => 'required|string|max:255'
        ]"""
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert result['email'] == 'required|email'
        assert result['password'] == 'required|min:8'
        assert result['name'] == 'required|string|max:255'

    def test_flatten_nested_rules(self):
        """Test flattening nested validation rules."""
        rules = {
            'user': {
                'name': 'required',
                'email': 'required|email'
            },
            'posts': {
                'title': 'required|string',
                'content': 'required'
            }
        }
        
        flattened = PHPArrayParser.flatten_nested_rules(rules)
        
        assert flattened['user.name'] == 'required'
        assert flattened['user.email'] == 'required|email'
        assert flattened['posts.title'] == 'required|string'
        assert flattened['posts.content'] == 'required'

    def test_extract_rule_metadata(self):
        """Test extracting metadata from rule string."""
        rule = 'required|email|max:255|min:5'
        metadata = PHPArrayParser.extract_rule_metadata(rule)
        
        assert metadata['required'] is True
        assert metadata['email'] is True
        assert metadata['max'] == '255'
        assert metadata['min'] == '5'

    def test_parse_numeric_keys(self):
        """Test parsing arrays with numeric keys."""
        code = "[0 => 'first', 1 => 'second', 2 => 'third']"
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert result[0] == 'first'
        assert result[1] == 'second'
        assert result[2] == 'third'

    def test_parse_mixed_keys(self):
        """Test parsing arrays with mixed key types."""
        code = "['name' => 'John', 0 => 'admin', 'age' => 30]"
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert result['name'] == 'John'
        assert result[0] == 'admin'
        assert result['age'] == 30

    def test_parse_boolean_values(self):
        """Test parsing boolean values."""
        code = "['active' => true, 'deleted' => false]"
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert result['active'] is True
        assert result['deleted'] is False

    def test_parse_null_values(self):
        """Test parsing null values."""
        code = "['value' => null, 'name' => 'test']"
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert result['value'] is None
        assert result['name'] == 'test'

    def test_parse_numeric_values(self):
        """Test parsing numeric values."""
        code = "['count' => 42, 'price' => 19.99, 'quantity' => 100]"
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert result['count'] == 42
        assert result['price'] == 19.99
        assert result['quantity'] == 100

    def test_extract_array_from_validate_call(self):
        """Test extracting array from $request->validate() call."""
        code = "$request->validate(['email' => 'required|email', 'password' => 'required|min:8'])"
        tokens = tokenize_code(code)
        result = PHPArrayParser.extract_array_from_call(tokens, 'validate')
        
        assert result is not None
        assert result['email'] == 'required|email'
        assert result['password'] == 'required|min:8'

    def test_extract_array_from_validator_make(self):
        """Test extracting array from Validator::make() call."""
        code = "Validator::make($data, ['name' => 'required', 'email' => 'required|email'])"
        tokens = tokenize_code(code)
        result = PHPArrayParser.extract_array_from_call(tokens, 'make')
        
        assert result is not None
        assert result['name'] == 'required'
        assert result['email'] == 'required|email'

    def test_parse_empty_array(self):
        """Test parsing empty array."""
        code = "[]"
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert len(result) == 0

    def test_parse_array_with_trailing_comma(self):
        """Test parsing array with trailing comma."""
        code = "['name' => 'John', 'email' => 'john@example.com',]"
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert result['name'] == 'John'
        assert result['email'] == 'john@example.com'

    def test_parse_deeply_nested_array(self):
        """Test parsing deeply nested arrays."""
        code = """[
            'level1' => [
                'level2' => [
                    'level3' => 'value'
                ]
            ]
        ]"""
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert result['level1']['level2']['level3'] == 'value'

    def test_parse_array_with_list_values(self):
        """Test parsing array with list values."""
        code = "['tags' => ['admin', 'user', 'guest']]"
        tokens = tokenize_code(code)
        result, _ = PHPArrayParser.parse_php_array(tokens, 0)
        
        assert result is not None
        assert isinstance(result['tags'], dict)  # Parsed as array with numeric keys

    def test_unquote_string(self):
        """Test unquoting string tokens."""
        assert PHPArrayParser._unquote_string("'hello'") == 'hello'
        assert PHPArrayParser._unquote_string('"world"') == 'world'
        assert PHPArrayParser._unquote_string('hello') == 'hello'

    def test_flatten_simple_rules(self):
        """Test flattening simple (non-nested) rules."""
        rules = {
            'email': 'required|email',
            'password': 'required|min:8'
        }
        
        flattened = PHPArrayParser.flatten_nested_rules(rules)
        
        assert flattened['email'] == 'required|email'
        assert flattened['password'] == 'required|min:8'

    def test_extract_rule_metadata_complex(self):
        """Test extracting metadata from complex rule string."""
        rule = 'required|string|min:5|max:255|regex:/^[a-z]+$/|unique:users,email'
        metadata = PHPArrayParser.extract_rule_metadata(rule)
        
        assert metadata['required'] is True
        assert metadata['string'] is True
        assert metadata['min'] == '5'
        assert metadata['max'] == '255'
        assert metadata['regex'] == '/^[a-z]+$/'
        assert metadata['unique'] == 'users,email'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
