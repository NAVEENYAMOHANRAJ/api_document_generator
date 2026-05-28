"""
Test Laravel extractor against gold standard examples.

This test validates that the Laravel extractor produces the expected output
for the gold standard examples provided in the requirements.
"""

import pytest
from api_doc_generator.extractors.laravel_extractor import LaravelExtractor


class TestLaravelExtractorGoldStandard:
    """Test Laravel extractor with gold standard examples."""

    def test_extract_grouped_routes_with_prefix(self):
        """Test extraction of grouped routes with prefix."""
        content = """<?php
Route::group(['prefix' => 'user'], function () {
    Route::post('/login', 'Auth\\LoginController@login');
    Route::post('/', 'Auth\\RegisterController@register');
});
"""
        endpoints = LaravelExtractor.extract("routes/api.php", content)
        
        # Should have 2 endpoints
        assert len(endpoints) == 2
        
        # First endpoint: POST /user/login
        login = next((e for e in endpoints if "login" in e["path"]), None)
        assert login is not None
        assert login["method"] == "POST"
        assert login["path"] == "/user/login"
        assert login["handler"]["class"] == "Auth\\LoginController"
        assert login["handler"]["method"] == "login"
        assert login["source"]["file"] == "routes/api.php"
        assert login["confidence"] == 0.95
        
        # Second endpoint: POST /user
        register = next((e for e in endpoints if e["path"] == "/user"), None)
        assert register is not None
        assert register["method"] == "POST"
        assert register["handler"]["class"] == "Auth\\RegisterController"
        assert register["handler"]["method"] == "register"

    def test_extract_middleware_routes(self):
        """Test extraction of routes with middleware."""
        content = """<?php
Route::middleware('auth:api')->group(function () {
    Route::get('/user', 'UserController@index');
    Route::put('/user', 'UserController@update');
});
"""
        endpoints = LaravelExtractor.extract("routes/api.php", content)
        
        # Should have 2 endpoints
        assert len(endpoints) == 2
        
        # Both should have auth:api middleware
        for endpoint in endpoints:
            assert "auth:api" in endpoint["middleware"]
        
        # GET /user
        get_user = next((e for e in endpoints if e["method"] == "GET"), None)
        assert get_user is not None
        assert get_user["path"] == "/user"
        assert get_user["handler"]["method"] == "index"
        
        # PUT /user
        put_user = next((e for e in endpoints if e["method"] == "PUT"), None)
        assert put_user is not None
        assert put_user["path"] == "/user"
        assert put_user["handler"]["method"] == "update"

    def test_extract_resource_routes(self):
        """Test extraction of resource routes."""
        content = """<?php
Route::resource('posts', 'PostController');
"""
        endpoints = LaravelExtractor.extract("routes/api.php", content)
        
        # Resource should expand to 7 endpoints
        assert len(endpoints) == 7
        
        # Check specific endpoints
        methods_paths = {(e["method"], e["path"]) for e in endpoints}
        
        assert ("GET", "/posts") in methods_paths  # index
        assert ("GET", "/posts/create") in methods_paths  # create
        assert ("POST", "/posts") in methods_paths  # store
        assert ("GET", "/posts/{id}") in methods_paths  # show
        assert ("GET", "/posts/{id}/edit") in methods_paths  # edit
        assert ("PUT", "/posts/{id}") in methods_paths  # update
        assert ("DELETE", "/posts/{id}") in methods_paths  # destroy

    def test_extract_api_resource_routes(self):
        """Test extraction of API resource routes (excludes create/edit)."""
        content = """<?php
Route::apiResource('users', 'UserController');
"""
        endpoints = LaravelExtractor.extract("routes/api.php", content)
        
        # API resource should expand to 5 endpoints (no create/edit)
        assert len(endpoints) == 5
        
        # Check that create and edit are NOT present
        methods_paths = {(e["method"], e["path"]) for e in endpoints}
        
        assert ("GET", "/users") in methods_paths  # index
        assert ("POST", "/users") in methods_paths  # store
        assert ("GET", "/users/{id}") in methods_paths  # show
        assert ("PUT", "/users/{id}") in methods_paths  # update
        assert ("DELETE", "/users/{id}") in methods_paths  # destroy
        
        # These should NOT be present
        assert ("GET", "/users/create") not in methods_paths
        assert ("GET", "/users/{id}/edit") not in methods_paths

    def test_path_normalization(self):
        """Test path normalization."""
        content = """<?php
Route::group(['prefix' => 'api'], function () {
    Route::get('/users/:id', 'UserController@show');
    Route::post('/posts/<int:id>', 'PostController@update');
});
"""
        endpoints = LaravelExtractor.extract("routes/api.php", content)
        
        # Paths should be normalized
        paths = {e["path"] for e in endpoints}
        
        # :id should be converted to {id}
        assert "/api/users/{id}" in paths
        # <int:id> should be converted to {id}
        assert "/api/posts/{id}" in paths

    def test_nested_groups(self):
        """Test extraction of nested route groups."""
        content = """<?php
Route::group(['prefix' => 'api'], function () {
    Route::group(['prefix' => 'v1'], function () {
        Route::get('/users', 'UserController@index');
    });
});
"""
        endpoints = LaravelExtractor.extract("routes/api.php", content)
        
        # Should have 1 endpoint
        assert len(endpoints) == 1
        
        # Path should have both prefixes
        endpoint = endpoints[0]
        assert endpoint["path"] == "/api/v1/users"
        assert endpoint["method"] == "GET"

    def test_source_traceability(self):
        """Test that source traceability is tracked."""
        content = """<?php
Route::get('/users', 'UserController@index');
"""
        endpoints = LaravelExtractor.extract("routes/api.php", content)
        
        # Should have source information
        assert len(endpoints) == 1
        endpoint = endpoints[0]
        
        assert endpoint["source"]["file"] == "routes/api.php"
        assert endpoint["source"]["line"] > 0
        assert endpoint["provenance"]["source_file"] == "routes/api.php"
        assert endpoint["provenance"]["detection_type"] == "framework_route_definition"
        assert endpoint["provenance"]["framework"] == "Laravel"

    def test_confidence_scoring(self):
        """Test confidence scoring."""
        content = """<?php
Route::get('/users', 'UserController@index');
Route::post('/posts', function() {
    return response()->json([]);
});
"""
        endpoints = LaravelExtractor.extract("routes/api.php", content)
        
        # Route with controller should have high confidence
        with_controller = next((e for e in endpoints if e["handler"].get("class")), None)
        assert with_controller is not None
        assert with_controller["confidence"] == 0.95
        
        # Route with closure should have lower confidence
        with_closure = next((e for e in endpoints if not e["handler"].get("class")), None)
        assert with_closure is not None
        assert with_closure["confidence"] == 0.70

    def test_controller_spec_parsing(self):
        """Test parsing of controller specifications."""
        content = """<?php
Route::get('/users', [UserController::class, 'index']);
"""
        endpoints = LaravelExtractor.extract("routes/api.php", content)
        
        # Should parse controller spec correctly
        assert len(endpoints) == 1
        endpoint = endpoints[0]
        
        assert endpoint["handler"]["class"] == "UserController"
        assert endpoint["handler"]["method"] == "index"

    def test_no_hallucination(self):
        """Test that extractor doesn't hallucinate metadata."""
        content = """<?php
Route::get('/users', 'UserController@index');
"""
        endpoints = LaravelExtractor.extract("routes/api.php", content)
        
        # Should have empty request/response bodies (not fabricated)
        assert len(endpoints) == 1
        endpoint = endpoints[0]
        
        assert endpoint["requestBody"] == {}
        assert endpoint["responses"] == {}
        assert endpoint["security"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
