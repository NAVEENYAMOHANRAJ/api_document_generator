"""OpenAPI/Swagger spec extractor."""

import json
import yaml
from typing import Dict, List, Optional, Tuple


class OpenAPISpecExtractor:
    """Extract endpoints from OpenAPI/Swagger specifications."""

    # OpenAPI/Swagger spec file patterns
    SPEC_FILE_PATTERNS = {
        'openapi.json',
        'openapi.yaml',
        'openapi.yml',
        'swagger.json',
        'swagger.yaml',
        'swagger.yml',
        'api.json',
        'api.yaml',
        'api.yml',
    }

    @classmethod
    def find_spec_files(cls, tree_entries: List[Dict]) -> List[Dict]:
        """
        Find OpenAPI/Swagger specification files in tree entries.
        
        Returns list of file entries that match spec file patterns.
        """
        spec_files = []
        
        for entry in tree_entries:
            path = entry.get('path', '').lower()
            
            # Check if file matches spec patterns
            for pattern in cls.SPEC_FILE_PATTERNS:
                if path.endswith(pattern):
                    spec_files.append(entry)
                    break
            
            # Also check for common spec file locations
            if any(indicator in path for indicator in ['openapi', 'swagger', 'spec', 'api-docs']):
                if path.endswith(('.json', '.yaml', '.yml')):
                    spec_files.append(entry)
                    break
        
        return spec_files

    @classmethod
    def extract_from_content(cls, file_path: str, content: str) -> Tuple[List[Dict], List[Dict]]:
        """
        Extract endpoints from OpenAPI spec content.
        
        Returns:
            Tuple of (endpoints, errors)
        """
        errors = []
        
        try:
            if file_path.endswith('.json'):
                spec = json.loads(content)
            else:
                spec = yaml.safe_load(content)
            
            endpoints = cls._extract_from_spec(spec, file_path)
            return endpoints, errors
        except json.JSONDecodeError as e:
            errors.append({
                'file': file_path,
                'error': f'Invalid JSON: {str(e)}'
            })
            return [], errors
        except yaml.YAMLError as e:
            errors.append({
                'file': file_path,
                'error': f'Invalid YAML: {str(e)}'
            })
            return [], errors
        except Exception as e:
            errors.append({
                'file': file_path,
                'error': f'Failed to parse spec: {str(e)}'
            })
            return [], errors

    @classmethod
    def extract(cls, file_path: str, content: str) -> List[Dict]:
        """Extract endpoints from OpenAPI spec."""
        endpoints, _ = cls.extract_from_content(file_path, content)
        return endpoints

    @classmethod
    def _extract_from_spec(cls, spec: Dict, file_path: str) -> List[Dict]:
        """Extract endpoints from parsed spec."""
        endpoints = []
        paths = spec.get('paths', {})
        
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.upper() in ('GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'):
                    endpoint = {
                        'method': method.upper(),
                        'path': path,
                        'source_file': file_path,
                        'confidence': 0.99,
                        'detection_type': 'openapi_spec_definition',
                        'provenance': {
                            'source_file': file_path,
                            'detection_type': 'openapi_spec_definition',
                        }
                    }
                    
                    # Extract summary if available
                    if isinstance(details, dict) and 'summary' in details:
                        endpoint['summary'] = details['summary']
                    
                    # Extract description if available
                    if isinstance(details, dict) and 'description' in details:
                        endpoint['description'] = details['description']
                    
                    # Extract tags if available
                    if isinstance(details, dict) and 'tags' in details:
                        endpoint['tags'] = details['tags']
                    
                    endpoints.append(endpoint)
        
        return endpoints
