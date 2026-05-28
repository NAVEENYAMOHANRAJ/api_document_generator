"""
11-Feature Extraction System for API Endpoints
Extracts comprehensive features from source code for ML training and analysis
"""

import ast
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class Feature:
    """Represents an extracted feature"""
    name: str
    value: Any
    confidence: float
    source: str


@dataclass
class EndpointFeatures:
    """Complete feature set for an endpoint"""
    # Feature 1: Authentication
    authentication: Feature
    
    # Feature 2: Rate Limiting
    rate_limiting: Feature
    
    # Feature 3: Caching
    caching: Feature
    
    # Feature 4: Pagination
    pagination: Feature
    
    # Feature 5: Filtering
    filtering: Feature
    
    # Feature 6: Sorting
    sorting: Feature
    
    # Feature 7: Error Handling
    error_handling: Feature
    
    # Feature 8: Input Validation
    input_validation: Feature
    
    # Feature 9: Response Transformation
    response_transformation: Feature
    
    # Feature 10: Versioning
    versioning: Feature
    
    # Feature 11: Documentation
    documentation: Feature


class FeatureExtractor:
    """Extract 11 key features from API endpoints"""
    
    def __init__(self, source_code: str, file_path: str = ""):
        self.source_code = source_code
        self.file_path = file_path
        self.tree = None
        self.lines = source_code.split('\n')
        
        try:
            self.tree = ast.parse(source_code)
        except:
            self.tree = None
    
    def extract_all_features(self, endpoint_node: Optional[ast.AST] = None) -> EndpointFeatures:
        """Extract all 11 features from endpoint"""
        return EndpointFeatures(
            authentication=self._extract_authentication(endpoint_node),
            rate_limiting=self._extract_rate_limiting(endpoint_node),
            caching=self._extract_caching(endpoint_node),
            pagination=self._extract_pagination(endpoint_node),
            filtering=self._extract_filtering(endpoint_node),
            sorting=self._extract_sorting(endpoint_node),
            error_handling=self._extract_error_handling(endpoint_node),
            input_validation=self._extract_input_validation(endpoint_node),
            response_transformation=self._extract_response_transformation(endpoint_node),
            versioning=self._extract_versioning(endpoint_node),
            documentation=self._extract_documentation(endpoint_node)
        )
    
    # Feature 1: Authentication
    def _extract_authentication(self, endpoint_node: Optional[ast.AST]) -> Feature:
        """
        Extract authentication mechanisms
        Detects: JWT, OAuth, API Key, Basic Auth, Bearer tokens
        """
        auth_patterns = {
            'jwt': r'(jwt|JWT|JsonWebToken)',
            'oauth': r'(oauth|OAuth|oauth2)',
            'api_key': r'(api[_-]?key|API[_-]?KEY|x[_-]?api[_-]?key)',
            'bearer': r'(bearer|Bearer|BEARER)',
            'basic': r'(basic[_-]?auth|BasicAuth)',
            'session': r'(session|Session|SESSION)',
            'token': r'(token|Token|TOKEN)',
        }
        
        detected_auth = []
        confidence = 0.0
        
        # Check decorators
        if endpoint_node and isinstance(endpoint_node, ast.FunctionDef):
            for decorator in endpoint_node.decorator_list:
                decorator_str = ast.unparse(decorator) if hasattr(ast, 'unparse') else str(decorator)
                for auth_type, pattern in auth_patterns.items():
                    if re.search(pattern, decorator_str, re.IGNORECASE):
                        detected_auth.append(auth_type)
                        confidence = max(confidence, 0.9)
        
        # Check source code
        for pattern_name, pattern in auth_patterns.items():
            if re.search(pattern, self.source_code, re.IGNORECASE):
                if pattern_name not in detected_auth:
                    detected_auth.append(pattern_name)
                confidence = max(confidence, 0.7)
        
        return Feature(
            name="authentication",
            value=detected_auth if detected_auth else ["none"],
            confidence=confidence,
            source="code_analysis"
        )
    
    # Feature 2: Rate Limiting
    def _extract_rate_limiting(self, endpoint_node: Optional[ast.AST]) -> Feature:
        """
        Extract rate limiting configuration
        Detects: throttle, rate_limit, ratelimit, requests per minute/hour
        """
        rate_limit_patterns = {
            'throttle': r'(throttle|Throttle)',
            'rate_limit': r'(rate[_-]?limit|RateLimit)',
            'requests_per_minute': r'(\d+)\s*(requests?|req)\s*(?:per|/)\s*(?:minute|min)',
            'requests_per_hour': r'(\d+)\s*(requests?|req)\s*(?:per|/)\s*(?:hour|hr)',
            'requests_per_second': r'(\d+)\s*(requests?|req)\s*(?:per|/)\s*(?:second|sec)',
        }
        
        detected_limits = {}
        confidence = 0.0
        
        for limit_type, pattern in rate_limit_patterns.items():
            matches = re.findall(pattern, self.source_code, re.IGNORECASE)
            if matches:
                detected_limits[limit_type] = matches
                confidence = max(confidence, 0.85)
        
        return Feature(
            name="rate_limiting",
            value=detected_limits if detected_limits else {"enabled": False},
            confidence=confidence,
            source="code_analysis"
        )
    
    # Feature 3: Caching
    def _extract_caching(self, endpoint_node: Optional[ast.AST]) -> Feature:
        """
        Extract caching strategy
        Detects: cache, redis, memcached, etag, cache-control headers
        """
        cache_patterns = {
            'redis': r'(redis|Redis|REDIS)',
            'memcached': r'(memcached|Memcached)',
            'cache_decorator': r'(@cache|@cached|cache_page)',
            'etag': r'(etag|ETag|ETAG)',
            'cache_control': r'(cache[_-]?control|Cache[_-]?Control)',
            'ttl': r'(ttl|TTL|time[_-]?to[_-]?live)',
        }
        
        detected_caching = []
        confidence = 0.0
        
        for cache_type, pattern in cache_patterns.items():
            if re.search(pattern, self.source_code, re.IGNORECASE):
                detected_caching.append(cache_type)
                confidence = max(confidence, 0.8)
        
        return Feature(
            name="caching",
            value=detected_caching if detected_caching else ["none"],
            confidence=confidence,
            source="code_analysis"
        )
    
    # Feature 4: Pagination
    def _extract_pagination(self, endpoint_node: Optional[ast.AST]) -> Feature:
        """
        Extract pagination implementation
        Detects: limit, offset, page, per_page, cursor
        """
        pagination_patterns = {
            'limit_offset': r'(limit|offset)',
            'page_based': r'(page|per[_-]?page|page[_-]?size)',
            'cursor_based': r'(cursor|next[_-]?token|continuation)',
            'keyset': r'(keyset|seek)',
        }
        
        detected_pagination = []
        confidence = 0.0
        
        for pag_type, pattern in pagination_patterns.items():
            if re.search(pattern, self.source_code, re.IGNORECASE):
                detected_pagination.append(pag_type)
                confidence = max(confidence, 0.85)
        
        return Feature(
            name="pagination",
            value=detected_pagination if detected_pagination else ["none"],
            confidence=confidence,
            source="code_analysis"
        )
    
    # Feature 5: Filtering
    def _extract_filtering(self, endpoint_node: Optional[ast.AST]) -> Feature:
        """
        Extract filtering capabilities
        Detects: filter, where, query parameters, search
        """
        filter_patterns = {
            'query_params': r'(query|Query|params|Params)',
            'filter_decorator': r'(@filter|@filters|FilterSet)',
            'search': r'(search|Search|SEARCH)',
            'where_clause': r'(where|Where|WHERE)',
            'advanced_filters': r'(advanced[_-]?filter|complex[_-]?filter)',
        }
        
        detected_filters = []
        confidence = 0.0
        
        for filter_type, pattern in filter_patterns.items():
            if re.search(pattern, self.source_code, re.IGNORECASE):
                detected_filters.append(filter_type)
                confidence = max(confidence, 0.8)
        
        return Feature(
            name="filtering",
            value=detected_filters if detected_filters else ["none"],
            confidence=confidence,
            source="code_analysis"
        )
    
    # Feature 6: Sorting
    def _extract_sorting(self, endpoint_node: Optional[ast.AST]) -> Feature:
        """
        Extract sorting capabilities
        Detects: sort, order_by, order, ascending, descending
        """
        sort_patterns = {
            'sort_param': r'(sort|Sort|SORT)',
            'order_by': r'(order[_-]?by|OrderBy)',
            'ascending': r'(asc|ascending|Ascending)',
            'descending': r'(desc|descending|Descending)',
            'multi_sort': r'(multi[_-]?sort|multiple[_-]?sort)',
        }
        
        detected_sorting = []
        confidence = 0.0
        
        for sort_type, pattern in sort_patterns.items():
            if re.search(pattern, self.source_code, re.IGNORECASE):
                detected_sorting.append(sort_type)
                confidence = max(confidence, 0.8)
        
        return Feature(
            name="sorting",
            value=detected_sorting if detected_sorting else ["none"],
            confidence=confidence,
            source="code_analysis"
        )
    
    # Feature 7: Error Handling
    def _extract_error_handling(self, endpoint_node: Optional[ast.AST]) -> Feature:
        """
        Extract error handling patterns
        Detects: try-catch, exception handling, error codes, error messages
        """
        error_patterns = {
            'try_except': r'(try|except|Exception)',
            'error_codes': r'(400|401|403|404|500|502|503)',
            'error_messages': r'(error|Error|ERROR)',
            'validation_errors': r'(ValidationError|validation[_-]?error)',
            'custom_exceptions': r'(raise|Raise|throw|Throw)',
        }
        
        detected_errors = []
        confidence = 0.0
        
        # Check AST for try-except
        if self.tree:
            for node in ast.walk(self.tree):
                if isinstance(node, ast.Try):
                    detected_errors.append('try_except')
                    confidence = max(confidence, 0.95)
                    break
        
        # Check patterns
        for error_type, pattern in error_patterns.items():
            if re.search(pattern, self.source_code, re.IGNORECASE):
                if error_type not in detected_errors:
                    detected_errors.append(error_type)
                confidence = max(confidence, 0.8)
        
        return Feature(
            name="error_handling",
            value=detected_errors if detected_errors else ["none"],
            confidence=confidence,
            source="code_analysis"
        )
    
    # Feature 8: Input Validation
    def _extract_input_validation(self, endpoint_node: Optional[ast.AST]) -> Feature:
        """
        Extract input validation mechanisms
        Detects: validators, schema validation, type hints, assertions
        """
        validation_patterns = {
            'type_hints': r'(:\s*\w+|:\s*List|:\s*Dict|:\s*Optional)',
            'pydantic': r'(BaseModel|Field|validator)',
            'marshmallow': r'(Schema|fields\.|validate)',
            'assertions': r'(assert|Assert)',
            'custom_validators': r'(validate|Validate|VALIDATE)',
            'regex_validation': r'(re\.match|re\.search|regex)',
        }
        
        detected_validation = []
        confidence = 0.0
        
        # Check for type hints in AST
        if self.tree and endpoint_node and isinstance(endpoint_node, ast.FunctionDef):
            for arg in endpoint_node.args.args:
                if arg.annotation:
                    detected_validation.append('type_hints')
                    confidence = max(confidence, 0.9)
                    break
        
        # Check patterns
        for val_type, pattern in validation_patterns.items():
            if re.search(pattern, self.source_code, re.IGNORECASE):
                if val_type not in detected_validation:
                    detected_validation.append(val_type)
                confidence = max(confidence, 0.85)
        
        return Feature(
            name="input_validation",
            value=detected_validation if detected_validation else ["none"],
            confidence=confidence,
            source="code_analysis"
        )
    
    # Feature 9: Response Transformation
    def _extract_response_transformation(self, endpoint_node: Optional[ast.AST]) -> Feature:
        """
        Extract response transformation patterns
        Detects: serialization, JSON conversion, data mapping, formatting
        """
        transform_patterns = {
            'json_serialization': r'(json\.dumps|JSONEncoder|to_json)',
            'serializers': r'(Serializer|serializer|serialize)',
            'data_mapping': r'(map|Map|transform|Transform)',
            'formatting': r'(format|Format|FORMAT)',
            'compression': r'(gzip|compress|Compress)',
            'pagination_wrapper': r'(paginated|pagination|page_data)',
        }
        
        detected_transforms = []
        confidence = 0.0
        
        for transform_type, pattern in transform_patterns.items():
            if re.search(pattern, self.source_code, re.IGNORECASE):
                detected_transforms.append(transform_type)
                confidence = max(confidence, 0.8)
        
        return Feature(
            name="response_transformation",
            value=detected_transforms if detected_transforms else ["none"],
            confidence=confidence,
            source="code_analysis"
        )
    
    # Feature 10: Versioning
    def _extract_versioning(self, endpoint_node: Optional[ast.AST]) -> Feature:
        """
        Extract API versioning strategy
        Detects: URL versioning, header versioning, query parameter versioning
        """
        versioning_patterns = {
            'url_versioning': r'(/v\d+/|/api/v\d+)',
            'header_versioning': r'(api[_-]?version|API[_-]?VERSION)',
            'query_versioning': r'(version=|api_version=)',
            'accept_header': r'(Accept|application/vnd)',
            'deprecation': r'(deprecated|Deprecated|DEPRECATED)',
        }
        
        detected_versioning = []
        confidence = 0.0
        
        for version_type, pattern in versioning_patterns.items():
            if re.search(pattern, self.source_code, re.IGNORECASE):
                detected_versioning.append(version_type)
                confidence = max(confidence, 0.85)
        
        return Feature(
            name="versioning",
            value=detected_versioning if detected_versioning else ["none"],
            confidence=confidence,
            source="code_analysis"
        )
    
    # Feature 11: Documentation
    def _extract_documentation(self, endpoint_node: Optional[ast.AST]) -> Feature:
        """
        Extract documentation quality
        Detects: docstrings, comments, type hints, examples
        """
        doc_quality = {
            'has_docstring': False,
            'has_comments': False,
            'has_type_hints': False,
            'has_examples': False,
            'docstring_length': 0,
        }
        
        confidence = 0.0
        
        # Check docstring
        if endpoint_node and isinstance(endpoint_node, ast.FunctionDef):
            docstring = ast.get_docstring(endpoint_node)
            if docstring:
                doc_quality['has_docstring'] = True
                doc_quality['docstring_length'] = len(docstring)
                confidence = max(confidence, 0.9)
                
                # Check for examples in docstring
                if 'example' in docstring.lower() or '>>>' in docstring:
                    doc_quality['has_examples'] = True
            
            # Check type hints
            if endpoint_node.returns or any(arg.annotation for arg in endpoint_node.args.args):
                doc_quality['has_type_hints'] = True
                confidence = max(confidence, 0.85)
        
        # Check for comments
        comment_count = len(re.findall(r'#.*$', self.source_code, re.MULTILINE))
        if comment_count > 0:
            doc_quality['has_comments'] = True
            confidence = max(confidence, 0.7)
        
        return Feature(
            name="documentation",
            value=doc_quality,
            confidence=confidence,
            source="code_analysis"
        )


class FeatureAnalyzer:
    """Analyze and score features for ML training"""
    
    @staticmethod
    def score_features(features: EndpointFeatures) -> Dict[str, float]:
        """Score each feature (0-1)"""
        scores = {}
        
        # Score authentication (0-1)
        auth_score = 0.0
        if features.authentication.value != ["none"]:
            auth_score = min(len(features.authentication.value) * 0.3, 1.0)
        scores['authentication'] = auth_score
        
        # Score rate limiting (0-1)
        rate_score = 0.0
        if features.rate_limiting.value != {"enabled": False}:
            rate_score = 0.8
        scores['rate_limiting'] = rate_score
        
        # Score caching (0-1)
        cache_score = 0.0
        if features.caching.value != ["none"]:
            cache_score = min(len(features.caching.value) * 0.25, 1.0)
        scores['caching'] = cache_score
        
        # Score pagination (0-1)
        pag_score = 0.0
        if features.pagination.value != ["none"]:
            pag_score = min(len(features.pagination.value) * 0.3, 1.0)
        scores['pagination'] = pag_score
        
        # Score filtering (0-1)
        filter_score = 0.0
        if features.filtering.value != ["none"]:
            filter_score = min(len(features.filtering.value) * 0.25, 1.0)
        scores['filtering'] = filter_score
        
        # Score sorting (0-1)
        sort_score = 0.0
        if features.sorting.value != ["none"]:
            sort_score = min(len(features.sorting.value) * 0.25, 1.0)
        scores['sorting'] = sort_score
        
        # Score error handling (0-1)
        error_score = 0.0
        if features.error_handling.value != ["none"]:
            error_score = min(len(features.error_handling.value) * 0.2, 1.0)
        scores['error_handling'] = error_score
        
        # Score input validation (0-1)
        val_score = 0.0
        if features.input_validation.value != ["none"]:
            val_score = min(len(features.input_validation.value) * 0.2, 1.0)
        scores['input_validation'] = val_score
        
        # Score response transformation (0-1)
        resp_score = 0.0
        if features.response_transformation.value != ["none"]:
            resp_score = min(len(features.response_transformation.value) * 0.2, 1.0)
        scores['response_transformation'] = resp_score
        
        # Score versioning (0-1)
        version_score = 0.0
        if features.versioning.value != ["none"]:
            version_score = 0.8
        scores['versioning'] = version_score
        
        # Score documentation (0-1)
        doc_score = 0.0
        if isinstance(features.documentation.value, dict):
            doc_quality = features.documentation.value
            doc_score = (
                (0.3 if doc_quality.get('has_docstring') else 0) +
                (0.2 if doc_quality.get('has_comments') else 0) +
                (0.25 if doc_quality.get('has_type_hints') else 0) +
                (0.25 if doc_quality.get('has_examples') else 0)
            )
        scores['documentation'] = doc_score
        
        return scores
    
    @staticmethod
    def calculate_overall_quality(scores: Dict[str, float]) -> float:
        """Calculate overall API quality score (0-100)"""
        if not scores:
            return 0.0
        
        # Weight each feature
        weights = {
            'authentication': 0.15,
            'rate_limiting': 0.10,
            'caching': 0.08,
            'pagination': 0.10,
            'filtering': 0.08,
            'sorting': 0.08,
            'error_handling': 0.12,
            'input_validation': 0.12,
            'response_transformation': 0.08,
            'versioning': 0.05,
            'documentation': 0.04,
        }
        
        total_score = 0.0
        for feature, score in scores.items():
            weight = weights.get(feature, 0.0)
            total_score += score * weight
        
        return round(total_score * 100, 2)
