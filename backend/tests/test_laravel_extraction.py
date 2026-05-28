from api_doc_generator.extractors.extraction_pipeline import ExtractionPipeline
from api_doc_generator.extractors.generic_framework_extractor import GenericFrameworkExtractor
from api_doc_generator.scanner.backend_detector import BackendFileDetector, FrameworkCandidateDetector


def test_laravel_route_file_is_detected_and_extracted():
    content = """
    <?php

    use Illuminate\\Support\\Facades\\Route;

    Route::get('/users', 'UserController@index');
    Route::post('/users', 'UserController@store');
    Route::match(['put', 'patch'], '/users/{id}', 'UserController@update');
    Route::apiResource('posts', PostController::class);
    """
    tree_entries = [{"path": "routes/api.php", "size": len(content)}]

    backend_files = BackendFileDetector().find_backend_files(tree_entries)
    assert backend_files == [{"path": "routes/api.php", "size": len(content)}]
    assert FrameworkCandidateDetector.detect(backend_files) == ["Laravel"]

    pipeline = ExtractionPipeline(batch_size=10)
    pipeline.add_files([{"path": "routes/api.php", "content": content}])
    endpoints, errors, stats = pipeline.run()

    assert errors == []
    assert stats["processed_files"] == 1
    extracted = {(endpoint["method"], endpoint["path"]) for endpoint in endpoints}
    assert ("GET", "/users") in extracted
    assert ("POST", "/users") in extracted
    assert ("PUT", "/users/{id}") in extracted
    assert ("PATCH", "/users/{id}") in extracted
    assert ("DELETE", "/posts/{post}") in extracted


def test_laravel_prefixed_group_and_any_routes_are_extracted():
    content = """
    <?php

    Route::prefix('v1')->group(function () {
        Route::middleware('auth:sanctum')->get('/profile', 'ProfileController@show');
        Route::any('/search', 'SearchController@handle');
    });
    """

    endpoints = GenericFrameworkExtractor.extract("routes/api.php", content, "Laravel")
    extracted = {(endpoint["method"], endpoint["path"]) for endpoint in endpoints}

    assert ("GET", "/v1/profile") in extracted
    assert ("GET", "/v1/search") in extracted
    assert ("POST", "/v1/search") in extracted
    assert ("DELETE", "/v1/search") in extracted
    assert ("GET", "/profile") not in extracted
    assert ("GET", "/search") not in extracted


def test_laravel_dynamic_controller_analysis():
    routes_content = """
    <?php
    use Illuminate\\Support\\Facades\\Route;
    use App\\Http\\Controllers\\ContactController;

    Route::post('/contacts', [ContactController::class, 'store']);
    Route::get('/contacts', 'ContactController@index');
    Route::delete('/contacts/{id}', 'ContactController@destroy');
    Route::post('/closure-route', function (Request $request) {
        $request->validate([
            'closure_field' => 'required|string'
        ]);
        return response()->json(['status' => 'closure_success'], 201);
    });
    """

    controller_content = """
    <?php
    namespace App\\Http\\Controllers;
    use App\\Http\\Requests\\StoreContactRequest;
    use Illuminate\\Http\\Request;

    class ContactController extends Controller {
        public function store(StoreContactRequest $request) {
            return response()->json(['message' => 'Created successfully', 'id' => 123], 201);
        }

        public function index(Request $request) {
            $request->validate([
                'search' => 'nullable|string',
                'limit' => 'integer'
            ]);
            $page = $request->query('page');
            return response()->json(['data' => []], 200);
        }

        public function destroy(Request $request, $id) {
            if (!$id) {
                return response()->json(['error' => 'Id is required'], 400);
            }
            return response()->json(['message' => 'Deleted'], 200);
        }
    }
    """

    request_content = """
    <?php
    namespace App\\Http\\Requests;
    class StoreContactRequest {
        public function rules() {
            return [
                'name' => 'required|string',
                'email' => 'required|email|unique:users',
                'age' => ['nullable', 'integer']
            ];
        }
    }
    """

    pipeline = ExtractionPipeline(batch_size=10)
    pipeline.add_files([
        {"path": "routes/api.php", "content": routes_content},
        {"path": "app/Http/Controllers/ContactController.php", "content": controller_content},
        {"path": "app/Http/Requests/StoreContactRequest.php", "content": request_content}
    ])
    endpoints, errors, stats = pipeline.run()

    assert errors == []
    
    get_contact = next(e for e in endpoints if e["path"] == "/contacts" and e["method"] == "GET")
    assert get_contact["status_code"] == 200
    assert len(get_contact["query_params"]) == 3
    query_names = {p["name"] for p in get_contact["query_params"]}
    assert "search" in query_names
    assert "limit" in query_names
    assert "page" in query_names
    
    post_contact = next(e for e in endpoints if e["path"] == "/contacts" and e["method"] == "POST")
    assert post_contact["status_code"] == 201
    assert post_contact["function_name"] == "ContactController@store"
    assert "request_body" in post_contact
    assert post_contact["request_body"]["model"] == "StoreContactRequest"
    body_properties = post_contact["request_body"]["schema"]["properties"]
    assert "name" in body_properties
    assert "email" in body_properties
    assert "age" in body_properties
    assert post_contact["request_body"]["schema"]["required"] == ["name", "email"]
    
    delete_contact = next(e for e in endpoints if e["path"] == "/contacts/{id}" and e["method"] == "DELETE")
    assert len(delete_contact["responses"]) == 2
    response_statuses = {r["status_code"] for r in delete_contact["responses"]}
    assert 200 in response_statuses
    assert 400 in response_statuses
    
    closure_endpoint = next(e for e in endpoints if e["path"] == "/closure-route")
    assert closure_endpoint["status_code"] == 201
    assert "closure_field" in closure_endpoint["request_body"]["schema"]["properties"]


def test_laravel_service_provider_routes_auth_and_spa_filtering():
    provider_content = """
    <?php
    namespace Laravel\\Sanctum;
    use Illuminate\\Support\\Facades\\Route;

    class SanctumServiceProvider {
        public function boot() {
            Route::group(['prefix' => 'sanctum', 'middleware' => ['auth:sanctum']], function () {
                Route::get('/csrf-cookie', [CsrfCookieController::class, 'show']);
                Route::post('/tokens/filter', [TokenController::class, 'index']);
            });
            Route::get('/{view}', function () { return view('app'); })->where('view', '.*');
        }
    }
    """
    controller_content = """
    <?php
    class TokenController {
        public function index(Request $request) {
            $ability = $request->query('ability');
            return response()->json(['data' => []]);
        }
    }
    class CsrfCookieController {
        public function show() {
            return response()->json(['csrf' => true], 204);
        }
    }
    """

    pipeline = ExtractionPipeline(batch_size=10)
    pipeline.add_files([
        {"path": "src/SanctumServiceProvider.php", "content": provider_content},
        {"path": "src/Http/Controllers/TokenController.php", "content": controller_content},
    ])
    endpoints, errors, stats = pipeline.run()

    assert errors == []
    extracted = {(endpoint["method"], endpoint["path"]) for endpoint in endpoints}
    assert ("GET", "/sanctum/csrf-cookie") in extracted
    assert ("POST", "/sanctum/tokens/filter") in extracted
    assert ("GET", "/{view}") not in extracted

    filter_endpoint = next(endpoint for endpoint in endpoints if endpoint["path"] == "/sanctum/tokens/filter")
    assert filter_endpoint["status_code"] == 200
    assert "request_body" not in filter_endpoint
    assert filter_endpoint["query_params"][0]["name"] == "ability"
    assert filter_endpoint["x-authentication"] == ["Laravel Sanctum"]
    assert stats["invalid_endpoints_removed"] == 1


def test_laravel_dingo_realworld_style_routes_are_extracted():
    routes_content = """
    <?php
    $api = app('Dingo\\Api\\Routing\\Router');
    $api->version('v1', ['middleware' => 'api.throttle'], function ($api) {
        $api->post('users', 'UsersController@store');
        $api->post('users/login', 'UsersController@login');
        $api->get('user', 'UsersController@show')->middleware('jwt.auth');
        $api->put('user', 'UsersController@update')->middleware('jwt.auth');
        $api->get('profiles/{username}', 'ProfilesController@show');
        $api->post('profiles/{username}/follow', 'ProfilesController@follow')->middleware('jwt.auth');
        $api->get('articles', 'ArticlesController@index');
        $api->post('articles', 'ArticlesController@store')->middleware('jwt.auth');
        $api->get('articles/{slug}', 'ArticlesController@show');
        $api->post('articles/{slug}/favorite', 'ArticlesController@favorite')->middleware('jwt.auth');
        $api->get('articles/{slug}/comments', 'CommentsController@index');
        $api->post('articles/{slug}/comments', 'CommentsController@store')->middleware('jwt.auth');
    });
    """
    controllers = """
    <?php
    class ArticlesController {
        public function index(Request $request) {
            $tag = $request->query('tag');
            return response()->json(['articles' => []], 200);
        }
        public function store(StoreArticleRequest $request) {
            return response()->json(['article' => []], 201);
        }
        public function favorite(Request $request, $slug) {
            return response()->json(['article' => []], 200);
        }
    }
    class UsersController {
        public function store(RegisterRequest $request) { return response()->json(['user' => []], 201); }
        public function login(LoginRequest $request) { return response()->json(['user' => []], 200); }
    }
    class CommentsController {
        public function index(Request $request, $slug) { return response()->json(['comments' => []], 200); }
        public function store(CommentRequest $request, $slug) { return response()->json(['comment' => []], 201); }
    }
    """
    requests = """
    <?php
    class StoreArticleRequest { public function rules() { return ['title' => 'required|string']; } }
    class RegisterRequest { public function rules() { return ['email' => 'required|email', 'password' => 'required|string']; } }
    class LoginRequest { public function rules() { return ['email' => 'required|email', 'password' => 'required|string']; } }
    class CommentRequest { public function rules() { return ['body' => 'required|string']; } }
    """

    pipeline = ExtractionPipeline(batch_size=10)
    pipeline.add_files([
        {"path": "routes/api.php", "content": routes_content},
        {"path": "app/Http/Controllers/ArticlesController.php", "content": controllers},
        {"path": "app/Http/Requests/StoreArticleRequest.php", "content": requests},
    ])
    endpoints, errors, _ = pipeline.run()
    extracted = {(endpoint["method"], endpoint["path"]) for endpoint in endpoints}

    assert errors == []
    assert ("POST", "/users") in extracted
    assert ("POST", "/users/login") in extracted
    assert ("GET", "/user") in extracted
    assert ("PUT", "/user") in extracted
    assert ("GET", "/profiles/{username}") in extracted
    assert ("POST", "/profiles/{username}/follow") in extracted
    assert ("GET", "/articles") in extracted
    assert ("POST", "/articles") in extracted
    assert ("POST", "/articles/{slug}/favorite") in extracted
    assert ("POST", "/articles/{slug}/comments") in extracted

    articles_index = next(endpoint for endpoint in endpoints if endpoint["method"] == "GET" and endpoint["path"] == "/articles")
    assert articles_index["query_params"][0]["name"] == "tag"
    favorite = next(endpoint for endpoint in endpoints if endpoint["path"] == "/articles/{slug}/favorite")
    assert favorite["x-authentication"] == ["JWT"]


def test_laravel_package_routes_inherit_configured_provider_prefix():
    provider_content = """
    <?php
    class TelescopeServiceProvider {
        protected function registerRoutes() {
            Route::group([
                'prefix' => config('telescope.path'),
                'middleware' => 'telescope',
            ], function () {
                $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
            });
        }
    }
    """
    config_content = """
    <?php
    return [
        'path' => env('TELESCOPE_PATH', 'telescope'),
    ];
    """
    routes_content = """
    <?php
    Route::post('/telescope-api/requests', 'RequestsController@index');
    Route::get('/{view?}', 'HomeController@index')->where('view', '(.*)');
    """

    pipeline = ExtractionPipeline(batch_size=10)
    pipeline.add_files([
        {"path": "src/TelescopeServiceProvider.php", "content": provider_content},
        {"path": "config/telescope.php", "content": config_content},
        {"path": "routes/web.php", "content": routes_content},
    ])
    endpoints, errors, stats = pipeline.run()

    assert errors == []
    extracted = {(endpoint["method"], endpoint["path"]) for endpoint in endpoints}
    assert ("POST", "/telescope/telescope-api/requests") in extracted
    assert ("POST", "/middleware/telescope-api/requests") not in extracted
    assert ("GET", "/telescope/{view}") not in extracted
    assert stats["invalid_endpoints_removed"] == 1


def test_laravel_telescope_style_service_provider_extraction():
    provider_content = """
    <?php
    namespace Laravel\\Telescope;
    use Illuminate\\Support\\Facades\\Route;

    class TelescopeServiceProvider {
        protected function registerRoutes() {
            Route::group([
                'prefix' => config('telescope.path', 'telescope'),
                'namespace' => 'Laravel\\Telescope\\Http\\Controllers',
                'middleware' => config('telescope.middleware', 'web'),
            ], function () {
                $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
            });
        }
    }
    """
    
    routes_content = """
    <?php
    use Illuminate\\Support\\Facades\\Route;
    Route::post('/telescope-api/mail', 'MailController@index');
    """
    
    pipeline = ExtractionPipeline(batch_size=10)
    pipeline.add_files([
        {"path": "src/TelescopeServiceProvider.php", "content": provider_content},
        {"path": "routes/web.php", "content": routes_content}
    ])
    endpoints, errors, stats = pipeline.run()
    
    assert errors == []
    extracted = {(endpoint["method"], endpoint["path"]) for endpoint in endpoints}
    assert ("POST", "/telescope/telescope-api/mail") in extracted
    
    mail_endpoint = next(e for e in endpoints if e["path"] == "/telescope/telescope-api/mail")
    assert mail_endpoint["x-authentication"] == ["web"]


def test_laravel_breeze_style_stubs_extraction():
    stubs_routes_content = """
    <?php
    use Illuminate\\Support\\Facades\\Route;
    Route::post('register', [RegisteredUserController::class, 'store']);
    Route::post('login', [AuthenticatedSessionController::class, 'store']);
    """
    
    pipeline = ExtractionPipeline(batch_size=10)
    pipeline.add_files([
        {"path": "stubs/default/routes/auth.php", "content": stubs_routes_content}
    ])
    endpoints, errors, stats = pipeline.run()
    
    assert errors == []
    extracted = {(endpoint["method"], endpoint["path"]) for endpoint in endpoints}
    assert ("POST", "/register") in extracted
    assert ("POST", "/login") in extracted
