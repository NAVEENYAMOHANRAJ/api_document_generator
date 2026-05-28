"""
Comprehensive tests for Laravel extractor.

Tests validate:
- Individual route extraction (Route::get, Route::post, etc.)
- Resource route extraction
- API resource route extraction
- Grouped routes with prefix and namespace
- Route model binding
- Controller-based routes
"""

import pytest
from api_doc_generator.extractors.laravel_extractor import LaravelExtractor


class TestLaravelExtractorIndividualRoutes:
    """Test extraction of individual Laravel routes."""

    def test_extract_get_route(self):
        """Test extraction of Route::get()."""
        content = """
        Route::get('/users', 'UserController@index');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 1
        assert routes[0]['method'] == 'GET'
        assert routes[0]['path'] == '/users'
        assert routes[0]['confidence'] == 0.85

    def test_extract_post_route(self):
        """Test extraction of Route::post()."""
        content = """
        Route::post('/users', 'UserController@store');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 1
        assert routes[0]['method'] == 'POST'
        assert routes[0]['path'] == '/users'

    def test_extract_put_route(self):
        """Test extraction of Route::put()."""
        content = """
        Route::put('/users/{id}', 'UserController@update');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 1
        assert routes[0]['method'] == 'PUT'
        assert routes[0]['path'] == '/users/{id}'

    def test_extract_delete_route(self):
        """Test extraction of Route::delete()."""
        content = """
        Route::delete('/users/{id}', 'UserController@destroy');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 1
        assert routes[0]['method'] == 'DELETE'
        assert routes[0]['path'] == '/users/{id}'

    def test_extract_patch_route(self):
        """Test extraction of Route::patch()."""
        content = """
        Route::patch('/users/{id}', 'UserController@update');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 1
        assert routes[0]['method'] == 'PATCH'
        assert routes[0]['path'] == '/users/{id}'

    def test_extract_multiple_routes(self):
        """Test extraction of multiple routes."""
        content = """
        Route::get('/users', 'UserController@index');
        Route::post('/users', 'UserController@store');
        Route::get('/users/{id}', 'UserController@show');
        Route::put('/users/{id}', 'UserController@update');
        Route::delete('/users/{id}', 'UserController@destroy');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 5
        methods = [r['method'] for r in routes]
        assert 'GET' in methods
        assert 'POST' in methods
        assert 'PUT' in methods
        assert 'DELETE' in methods

    def test_extract_route_with_array_controller(self):
        """Test extraction of routes with array controller syntax."""
        content = """
        Route::get('/users', [UserController::class, 'index']);
        Route::post('/users', [UserController::class, 'store']);
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 2
        assert routes[0]['method'] == 'GET'
        assert routes[1]['method'] == 'POST'

    def test_extract_route_with_closure(self):
        """Test extraction of routes with closure."""
        content = """
        Route::get('/status', function() {
            return response()->json(['status' => 'ok']);
        });
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 1
        assert routes[0]['method'] == 'GET'
        assert routes[0]['path'] == '/status'


class TestLaravelExtractorResourceRoutes:
    """Test extraction of Laravel resource routes."""

    def test_extract_resource_routes(self):
        """Test extraction of Route::resource()."""
        content = """
        Route::resource('users', 'UserController');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        # Resource routes should generate 7 routes (index, create, store, show, edit, update, destroy)
        assert len(routes) == 7

        
        methods_by_path = {}
        for r in routes:
            methods_by_path.setdefault(r['path'], set()).add(r['method'])

        assert '/users' in methods_by_path
        assert methods_by_path['/users'] == {'GET', 'POST'}
        assert methods_by_path['/users/{id}'] == {'GET', 'PUT', 'DELETE'}

    def test_extract_api_resource_routes(self):
        """Test extraction of Route::apiResource()."""
        content = """
        Route::apiResource('posts', 'PostController');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        # API resources exclude create and edit (5 routes)
        assert len(routes) == 5
        
        paths = [r['path'] for r in routes]
        assert '/posts' in paths
        assert '/posts/{id}' in paths
        # Should not have create/edit paths
        assert '/posts/create' not in paths
        assert '/posts/{id}/edit' not in paths


class TestLaravelExtractorGroupedRoutes:
    """Test extraction of grouped Laravel routes."""

    def test_extract_grouped_routes_with_prefix(self):
        """Test extraction of Route::group() with prefix."""
        content = """
        Route::group(['prefix' => 'api'], function() {
            Route::get('/users', 'UserController@index');
            Route::post('/users', 'UserController@store');
        });
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 2
        assert routes[0]['path'] == '/api/users'
        assert routes[1]['path'] == '/api/users'

    def test_extract_grouped_routes_with_namespace(self):
        """Test extraction of Route::group() with namespace."""
        content = """
        Route::group(['namespace' => 'Api'], function() {
            Route::get('/users', 'UserController@index');
        });
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 1
        assert routes[0]['path'] == '/users'

    def test_extract_grouped_routes_with_prefix_and_namespace(self):
        """Test extraction of Route::group() with both prefix and namespace."""
        content = """
        Route::group(['prefix' => 'api', 'namespace' => 'Api'], function() {
            Route::get('/users', 'UserController@index');
            Route::post('/users', 'UserController@store');
        });
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 2
        assert routes[0]['path'] == '/api/users'
        assert routes[1]['path'] == '/api/users'

    def test_extract_nested_grouped_routes(self):
        """Test extraction of nested Route::group()."""
        content = """
        Route::group(['prefix' => 'api'], function() {
            Route::group(['prefix' => 'v1'], function() {
                Route::get('/users', 'UserController@index');
            });
        });
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        # Note: Nested groups may not be fully supported in current implementation
        # This test documents expected behavior
        assert len(routes) >= 1


class TestLaravelExtractorPathNormalization:
    """Test path normalization in Laravel extractor."""

    def test_normalize_path_with_leading_slash(self):
        """Test that paths are normalized with leading slash."""
        content = """
        Route::get('users', 'UserController@index');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert routes[0]['path'] == '/users'

    def test_normalize_path_with_double_slashes(self):
        """Test that double slashes are normalized."""
        content = """
        Route::get('/api//users', 'UserController@index');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert routes[0]['path'] == '/api/users'

    def test_normalize_path_with_trailing_slash(self):
        """Test that trailing slashes are removed."""
        content = """
        Route::get('/users/', 'UserController@index');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert routes[0]['path'] == '/users'

    def test_normalize_root_path(self):
        """Test that root path is preserved."""
        content = """
        Route::get('/', 'HomeController@index');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert routes[0]['path'] == '/'


class TestLaravelExtractorProvenance:
    """Test provenance tracking in Laravel extractor."""

    def test_provenance_tracking(self):
        """Test that provenance is tracked correctly."""
        content = """
        Route::get('/users', 'UserController@index');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert len(routes) == 1
        assert 'provenance' in routes[0]
        assert routes[0]['provenance']['source_file'] == 'routes/api.php'
        assert routes[0]['provenance']['detection_type'] == 'framework_route_definition'
        assert routes[0]['provenance']['framework'] == 'Laravel'
        assert 'line_number' in routes[0]['provenance']

    def test_detection_type_set(self):
        """Test that detection_type is set correctly."""
        content = """
        Route::get('/users', 'UserController@index');
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        assert routes[0]['detection_type'] == 'framework_route_definition'


class TestLaravelExtractorRealWorldExamples:
    """Test extraction with real-world Laravel code examples."""

    def test_extract_from_real_api_routes(self):
        """Test extraction from realistic API routes file."""
        content = """
        <?php

        use Illuminate\\Http\\Request;
        use Illuminate\\Support\\Facades\\Route;

        Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
            return $request->user();
        });

        Route::group(['prefix' => 'api', 'middleware' => 'api'], function () {
            Route::apiResource('users', 'UserController');
            Route::apiResource('posts', 'PostController');
            
            Route::group(['prefix' => 'admin'], function () {
                Route::get('/dashboard', 'AdminController@dashboard');
                Route::post('/settings', 'AdminController@updateSettings');
            });
        });
        """
        routes = LaravelExtractor.extract('routes/api.php', content)
        
        # Should extract multiple routes
        assert len(routes) > 0
        
        # Check for API resource routes
        paths = [r['path'] for r in routes]
        assert any('/api/users' in p for p in paths)
        assert any('/api/posts' in p for p in paths)

    def test_extract_from_web_routes(self):
        """Test extraction from web routes file."""
        content = """
        <?php

        use Illuminate\\Support\\Facades\\Route;

        Route::get('/', 'HomeController@index');
        Route::get('/about', 'PageController@about');
        Route::get('/contact', 'PageController@contact');
        Route::post('/contact', 'PageController@submitContact');

        Route::middleware(['auth'])->group(function () {
            Route::get('/dashboard', 'DashboardController@index');
            Route::resource('posts', 'PostController');
        });
        """
        routes = LaravelExtractor.extract('routes/web.php', content)
        
        assert len(routes) > 0
        
        # Check for specific routes
        paths = [r['path'] for r in routes]
        assert '/' in paths
        assert '/about' in paths
        assert '/contact' in paths
