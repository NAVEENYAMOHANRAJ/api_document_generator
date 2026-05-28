"""
Feature Extraction Routes
Exposes 11-feature extraction for API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import os
from pathlib import Path

from api_doc_generator.extractors.feature_extractor import (
    FeatureExtractor,
    FeatureAnalyzer,
    EndpointFeatures,
)

router = APIRouter()


class FeatureExtractionRequest(BaseModel):
    """Request to extract features from code"""
    code: str
    file_path: str = ""


class FeatureExtractionResponse(BaseModel):
    """Response with extracted features"""
    features: Dict[str, Any]
    scores: Dict[str, float]
    overall_quality: float
    metadata: Dict[str, Any]


@router.post("/api/extract-features", response_model=FeatureExtractionResponse)
async def extract_features(request: FeatureExtractionRequest):
    """
    Extract 11 key features from API endpoint code
    
    Features extracted:
    1. Authentication - JWT, OAuth, API Key, Bearer, Basic Auth, Session, Token
    2. Rate Limiting - Throttle, rate limits, requests per minute/hour/second
    3. Caching - Redis, Memcached, ETags, Cache-Control, TTL
    4. Pagination - Limit/Offset, Page-based, Cursor-based, Keyset
    5. Filtering - Query params, Filter decorators, Search, Where clauses
    6. Sorting - Sort params, Order by, Ascending/Descending, Multi-sort
    7. Error Handling - Try-catch, Exception handling, Error codes, Custom exceptions
    8. Input Validation - Type hints, Pydantic, Marshmallow, Assertions, Validators
    9. Response Transformation - JSON serialization, Serializers, Data mapping, Compression
    10. Versioning - URL versioning, Header versioning, Query versioning, Deprecation
    11. Documentation - Docstrings, Comments, Type hints, Examples
    """
    try:
        # Extract features
        extractor = FeatureExtractor(request.code, request.file_path)
        features = extractor.extract_all_features()
        
        # Helper to format feature values
        def format_value(val):
            if isinstance(val, list):
                return ', '.join(str(v) for v in val) if val else 'Not detected'
            elif isinstance(val, dict):
                if val.get('enabled') == False:
                    return 'Not detected'
                return ', '.join(f"{k}: {v}" for k, v in val.items() if k != 'enabled')
            elif val is None:
                return 'Not detected'
            else:
                return str(val)
        
        # Convert to dict
        features_dict = {
            'authentication': {
                'value': format_value(features.authentication.value),
                'confidence': features.authentication.confidence,
            },
            'rate_limiting': {
                'value': format_value(features.rate_limiting.value),
                'confidence': features.rate_limiting.confidence,
            },
            'caching': {
                'value': format_value(features.caching.value),
                'confidence': features.caching.confidence,
            },
            'pagination': {
                'value': format_value(features.pagination.value),
                'confidence': features.pagination.confidence,
            },
            'filtering': {
                'value': format_value(features.filtering.value),
                'confidence': features.filtering.confidence,
            },
            'sorting': {
                'value': format_value(features.sorting.value),
                'confidence': features.sorting.confidence,
            },
            'error_handling': {
                'value': format_value(features.error_handling.value),
                'confidence': features.error_handling.confidence,
            },
            'input_validation': {
                'value': format_value(features.input_validation.value),
                'confidence': features.input_validation.confidence,
            },
            'response_transformation': {
                'value': format_value(features.response_transformation.value),
                'confidence': features.response_transformation.confidence,
            },
            'versioning': {
                'value': format_value(features.versioning.value),
                'confidence': features.versioning.confidence,
            },
            'documentation': {
                'value': format_value(features.documentation.value),
                'confidence': features.documentation.confidence,
            },
        }
        
        # Score features
        scores = FeatureAnalyzer.score_features(features)
        
        # Calculate overall quality
        overall_quality = FeatureAnalyzer.calculate_overall_quality(scores)
        
        return FeatureExtractionResponse(
            features=features_dict,
            scores=scores,
            overall_quality=overall_quality,
            metadata={
                'file_path': request.file_path,
                'code_length': len(request.code),
                'lines_of_code': len(request.code.split('\n')),
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/extract-features-batch")
async def extract_features_batch(requests: List[FeatureExtractionRequest]):
    """
    Extract features from multiple code snippets
    """
    try:
        def format_value(val):
            if isinstance(val, list):
                return ', '.join(str(v) for v in val) if val else 'Not detected'
            elif isinstance(val, dict):
                if val.get('enabled') == False:
                    return 'Not detected'
                return ', '.join(f"{k}: {v}" for k, v in val.items() if k != 'enabled')
            elif val is None:
                return 'Not detected'
            else:
                return str(val)
        
        results = []
        
        for request in requests:
            extractor = FeatureExtractor(request.code, request.file_path)
            features = extractor.extract_all_features()
            
            features_dict = {
                'authentication': {
                    'value': format_value(features.authentication.value),
                    'confidence': features.authentication.confidence,
                },
                'rate_limiting': {
                    'value': format_value(features.rate_limiting.value),
                    'confidence': features.rate_limiting.confidence,
                },
                'caching': {
                    'value': format_value(features.caching.value),
                    'confidence': features.caching.confidence,
                },
                'pagination': {
                    'value': format_value(features.pagination.value),
                    'confidence': features.pagination.confidence,
                },
                'filtering': {
                    'value': format_value(features.filtering.value),
                    'confidence': features.filtering.confidence,
                },
                'sorting': {
                    'value': format_value(features.sorting.value),
                    'confidence': features.sorting.confidence,
                },
                'error_handling': {
                    'value': format_value(features.error_handling.value),
                    'confidence': features.error_handling.confidence,
                },
                'input_validation': {
                    'value': format_value(features.input_validation.value),
                    'confidence': features.input_validation.confidence,
                },
                'response_transformation': {
                    'value': format_value(features.response_transformation.value),
                    'confidence': features.response_transformation.confidence,
                },
                'versioning': {
                    'value': format_value(features.versioning.value),
                    'confidence': features.versioning.confidence,
                },
                'documentation': {
                    'value': format_value(features.documentation.value),
                    'confidence': features.documentation.confidence,
                },
            }
            
            scores = FeatureAnalyzer.score_features(features)
            overall_quality = FeatureAnalyzer.calculate_overall_quality(scores)
            
            results.append({
                'file_path': request.file_path,
                'features': features_dict,
                'scores': scores,
                'overall_quality': overall_quality,
            })
        
        return {
            'status': 'success',
            'total_analyzed': len(results),
            'results': results,
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/feature-definitions")
async def get_feature_definitions():
    """
    Get definitions of all 11 features
    """
    return {
        'features': [
            {
                'id': 1,
                'name': 'Authentication',
                'description': 'Security mechanisms for API access',
                'detects': ['JWT', 'OAuth', 'API Key', 'Bearer Token', 'Basic Auth', 'Session', 'Token'],
                'importance': 'Critical',
                'weight': 0.15,
            },
            {
                'id': 2,
                'name': 'Rate Limiting',
                'description': 'Request throttling and rate control',
                'detects': ['Throttle', 'Rate Limit', 'Requests per minute/hour/second'],
                'importance': 'High',
                'weight': 0.10,
            },
            {
                'id': 3,
                'name': 'Caching',
                'description': 'Response caching strategies',
                'detects': ['Redis', 'Memcached', 'ETags', 'Cache-Control', 'TTL'],
                'importance': 'High',
                'weight': 0.08,
            },
            {
                'id': 4,
                'name': 'Pagination',
                'description': 'Data pagination mechanisms',
                'detects': ['Limit/Offset', 'Page-based', 'Cursor-based', 'Keyset'],
                'importance': 'High',
                'weight': 0.10,
            },
            {
                'id': 5,
                'name': 'Filtering',
                'description': 'Data filtering capabilities',
                'detects': ['Query Parameters', 'Filter Decorators', 'Search', 'Where Clauses'],
                'importance': 'Medium',
                'weight': 0.08,
            },
            {
                'id': 6,
                'name': 'Sorting',
                'description': 'Data sorting capabilities',
                'detects': ['Sort Parameters', 'Order By', 'Ascending/Descending', 'Multi-sort'],
                'importance': 'Medium',
                'weight': 0.08,
            },
            {
                'id': 7,
                'name': 'Error Handling',
                'description': 'Exception and error management',
                'detects': ['Try-Catch', 'Exception Handling', 'Error Codes', 'Custom Exceptions'],
                'importance': 'Critical',
                'weight': 0.12,
            },
            {
                'id': 8,
                'name': 'Input Validation',
                'description': 'Request data validation',
                'detects': ['Type Hints', 'Pydantic', 'Marshmallow', 'Assertions', 'Validators'],
                'importance': 'Critical',
                'weight': 0.12,
            },
            {
                'id': 9,
                'name': 'Response Transformation',
                'description': 'Response data processing',
                'detects': ['JSON Serialization', 'Serializers', 'Data Mapping', 'Compression'],
                'importance': 'Medium',
                'weight': 0.08,
            },
            {
                'id': 10,
                'name': 'Versioning',
                'description': 'API versioning strategy',
                'detects': ['URL Versioning', 'Header Versioning', 'Query Versioning', 'Deprecation'],
                'importance': 'Medium',
                'weight': 0.05,
            },
            {
                'id': 11,
                'name': 'Documentation',
                'description': 'Code documentation quality',
                'detects': ['Docstrings', 'Comments', 'Type Hints', 'Examples'],
                'importance': 'Low',
                'weight': 0.04,
            },
        ]
    }


@router.post("/api/analyze-code-quality")
async def analyze_code_quality(request: FeatureExtractionRequest):
    """
    Comprehensive code quality analysis
    """
    try:
        extractor = FeatureExtractor(request.code, request.file_path)
        features = extractor.extract_all_features()
        scores = FeatureAnalyzer.score_features(features)
        overall_quality = FeatureAnalyzer.calculate_overall_quality(scores)
        
        # Determine quality level
        if overall_quality >= 80:
            quality_level = "Excellent"
        elif overall_quality >= 60:
            quality_level = "Good"
        elif overall_quality >= 40:
            quality_level = "Fair"
        else:
            quality_level = "Poor"
        
        # Find weak areas
        weak_areas = [feature for feature, score in scores.items() if score < 0.5]
        strong_areas = [feature for feature, score in scores.items() if score >= 0.8]
        
        return {
            'overall_quality': overall_quality,
            'quality_level': quality_level,
            'scores': scores,
            'strong_areas': strong_areas,
            'weak_areas': weak_areas,
            'recommendations': _generate_recommendations(weak_areas, scores),
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _generate_recommendations(weak_areas: List[str], scores: Dict[str, float]) -> List[str]:
    """Generate recommendations based on weak areas"""
    recommendations = []
    
    if 'authentication' in weak_areas:
        recommendations.append("Add authentication mechanism (JWT, OAuth, API Key)")
    
    if 'rate_limiting' in weak_areas:
        recommendations.append("Implement rate limiting to prevent abuse")
    
    if 'caching' in weak_areas:
        recommendations.append("Add caching strategy (Redis, Memcached, ETags)")
    
    if 'pagination' in weak_areas:
        recommendations.append("Implement pagination for large datasets")
    
    if 'filtering' in weak_areas:
        recommendations.append("Add filtering capabilities for better data retrieval")
    
    if 'sorting' in weak_areas:
        recommendations.append("Add sorting capabilities for data organization")
    
    if 'error_handling' in weak_areas:
        recommendations.append("Improve error handling with try-catch blocks")
    
    if 'input_validation' in weak_areas:
        recommendations.append("Add input validation using type hints or validators")
    
    if 'response_transformation' in weak_areas:
        recommendations.append("Add response transformation for consistent output")
    
    if 'versioning' in weak_areas:
        recommendations.append("Implement API versioning strategy")
    
    if 'documentation' in weak_areas:
        recommendations.append("Improve documentation with docstrings and examples")
    
    return recommendations
