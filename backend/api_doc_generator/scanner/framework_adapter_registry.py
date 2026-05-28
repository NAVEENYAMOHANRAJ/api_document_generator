from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Dict, List, Set


@dataclass(frozen=True)
class FrameworkCapabilities:
    supports_ast: bool = False
    supports_dynamic_routes: bool = False
    supports_nested_routers: bool = False
    supports_controller_prefix: bool = False
    supports_resource_routes: bool = False
    supports_openapi_annotations: bool = False
    supports_middleware_extraction: bool = False
    supports_auth_extraction: bool = False
    supports_versioning: bool = False


@dataclass(frozen=True)
class FrameworkAdapter:
    name: str
    languages: Set[str]
    extensions: Set[str]
    path_tokens: Set[str] = field(default_factory=set)
    content_tokens: Set[str] = field(default_factory=set)
    extraction_status: str = "supported"
    capabilities: FrameworkCapabilities = field(default_factory=FrameworkCapabilities)
    route_patterns: List[str] = field(default_factory=list)
    router_patterns: List[str] = field(default_factory=list)
    controller_patterns: List[str] = field(default_factory=list)
    middleware_patterns: List[str] = field(default_factory=list)
    auth_patterns: List[str] = field(default_factory=list)
    versioning_patterns: List[str] = field(default_factory=list)



class FrameworkAdapterRegistry:
    """Registry of API technologies supported by the technology-independent design."""

    ADAPTERS = [
        # PYTHON
        FrameworkAdapter(
            name="FastAPI",
            languages={"Python"},
            extensions={".py"},
            path_tokens={"fastapi", "api", "routes", "main", "app"},
            content_tokens={"FastAPI(", "APIRouter", "include_router", "from fastapi"},
            extraction_status="implemented_ast",
            capabilities=FrameworkCapabilities(
                supports_ast=True,
                supports_dynamic_routes=True,
                supports_nested_routers=True,
                supports_controller_prefix=True,
                supports_openapi_annotations=True,
                supports_middleware_extraction=True,
                supports_auth_extraction=True,
                supports_versioning=True,
            ),
            route_patterns=[r"@\w+\.(get|post|put|patch|delete|options|head)\s*\("],
            router_patterns=[r"\binclude_router\b"],
        ),
        FrameworkAdapter(
            name="Flask",
            languages={"Python"},
            extensions={".py"},
            path_tokens={"flask", "views", "routes", "app"},
            content_tokens={"Flask(", "@app.route", "Blueprint("},
            extraction_status="implemented_regex",
            capabilities=FrameworkCapabilities(
                supports_nested_routers=True,
                supports_controller_prefix=True,
                supports_middleware_extraction=True,
            ),
            route_patterns=[r"@\w+\.route\s*\(", r"@\w+\.(get|post|put|delete|patch)\s*\("],
            router_patterns=[r"\bBlueprint\s*\("],
        ),
        FrameworkAdapter(
            name="Django REST Framework",
            languages={"Python"},
            extensions={".py"},
            path_tokens={"django", "views", "urls", "serializers"},
            content_tokens={"APIView", "ViewSet", "DefaultRouter", "urlpatterns", "register"},
            extraction_status="implemented_regex",
            capabilities=FrameworkCapabilities(
                supports_ast=True,
                supports_dynamic_routes=True,
                supports_nested_routers=True,
                supports_resource_routes=True,
                supports_openapi_annotations=True,
                supports_middleware_extraction=True,
                supports_auth_extraction=True,
            ),
            route_patterns=[r"\bpath\s*\(", r"\burl\s*\("],
            router_patterns=[r"\brouter\.register\s*\("],
        ),
        FrameworkAdapter(
            name="Django Ninja",
            languages={"Python"},
            extensions={".py"},
            path_tokens={"ninja", "api", "routes"},
            content_tokens={"NinjaAPI", "Router", "from ninja"},
            extraction_status="supported",
            capabilities=FrameworkCapabilities(supports_openapi_annotations=True),
        ),
        FrameworkAdapter(
            name="Starlette",
            languages={"Python"},
            extensions={".py"},
            path_tokens={"starlette", "routes"},
            content_tokens={"Starlette", "Route(", "Mount("},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Litestar",
            languages={"Python"},
            extensions={".py"},
            content_tokens={"Litestar", "from litestar"},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Falcon",
            languages={"Python"},
            extensions={".py"},
            content_tokens={"falcon.App", "add_route"},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Sanic",
            languages={"Python"},
            extensions={".py"},
            content_tokens={"Sanic(", "@app.get(", "Blueprint("},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Tornado",
            languages={"Python"},
            extensions={".py"},
            content_tokens={"tornado.web.Application", "RequestHandler"},
            extraction_status="supported",
        ),

        # NODE
        FrameworkAdapter(
            name="Express",
            languages={"JavaScript", "TypeScript"},
            extensions={".js", ".ts"},
            path_tokens={"express", "routes", "controllers", "server", "app"},
            content_tokens={"express.Router", "app.get(", "router.get(", "app.use(", "require(\"express\")", "require('express')"},
            extraction_status="implemented_regex",
            capabilities=FrameworkCapabilities(
                supports_nested_routers=True,
                supports_controller_prefix=True,
                supports_middleware_extraction=True,
                supports_auth_extraction=True,
            ),
            route_patterns=[r"\b(app|router)\.(get|post|put|patch|delete)\s*\("],
            router_patterns=[r"\bapp\.use\s*\("],
        ),
        FrameworkAdapter(
            name="NestJS",
            languages={"TypeScript"},
            extensions={".ts"},
            path_tokens={"nestjs", "controller", "controllers", "module"},
            content_tokens={"@Controller", "@Get(", "@Post(", "@Body(", "@Param(", "@nestjs/common"},
            extraction_status="implemented_regex",
            capabilities=FrameworkCapabilities(
                supports_nested_routers=True,
                supports_controller_prefix=True,
                supports_openapi_annotations=True,
                supports_middleware_extraction=True,
                supports_auth_extraction=True,
                supports_versioning=True,
            ),
            route_patterns=[r"@Controller\s*\(", r"@Controller\s*\(\s*['\"](?P<prefix>[^'\"]+)['\"]\s*\)"],
        ),
        FrameworkAdapter(
            name="Koa",
            languages={"JavaScript", "TypeScript"},
            extensions={".js", ".ts"},
            content_tokens={"new Koa(", "koa-router"},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Hapi",
            languages={"JavaScript"},
            extensions={".js"},
            content_tokens={"Hapi.server(", "server.route("},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="AdonisJS",
            languages={"TypeScript"},
            extensions={".ts"},
            content_tokens={"Route.get(", "Route.group("},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Feathers",
            languages={"JavaScript", "TypeScript"},
            extensions={".js", ".ts"},
            content_tokens={"feathers()"},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Sails",
            languages={"JavaScript"},
            extensions={".js"},
            content_tokens={"sails.config.routes"},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="LoopBack",
            languages={"TypeScript"},
            extensions={".ts"},
            content_tokens={"@loopback/rest", "RestApplication"},
            extraction_status="supported",
        ),

        # PHP
        FrameworkAdapter(
            name="Laravel",
            languages={"PHP"},
            extensions={".php"},
            path_tokens={"routes", "controllers", "laravel", "provider", "serviceprovider"},
            content_tokens={
                "Route::get", "Route::post", "Route::put", "Route::patch", "Route::delete",
                "Route::match", "Route::any", "Route::resource", "Route::apiResource",
                "Route::prefix", "Route::group", "loadRoutesFrom", "Dingo\\Api\\Routing\\Router"
            },
            extraction_status="implemented_regex",
            capabilities=FrameworkCapabilities(
                supports_nested_routers=True,
                supports_controller_prefix=True,
                supports_resource_routes=True,
                supports_middleware_extraction=True,
                supports_auth_extraction=True,
                supports_versioning=True,
            ),
            route_patterns=[r"\bRoute::(get|post|put|patch|delete|any|match)\b"],
            router_patterns=[r"\bRoute::group\b", r"\bRoute::prefix\b", r"\bRoute::middleware\b"],
        ),
        FrameworkAdapter(
            name="Symfony",
            languages={"PHP"},
            extensions={".php"},
            content_tokens={"use Symfony\\Component\\Routing", "@Route", "RouteAnnotation"},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Slim",
            languages={"PHP"},
            extensions={".php"},
            content_tokens={"Slim\\Factory\\AppFactory", "$app->get(", "$app->group("},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Laminas",
            languages={"PHP"},
            extensions={".php"},
            content_tokens={"Laminas\\Router", "RouteMatch"},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="CodeIgniter",
            languages={"PHP"},
            extensions={".php"},
            content_tokens={"$routes->get(", "$routes->add("},
            extraction_status="supported",
        ),

        # JAVA
        FrameworkAdapter(
            name="Spring Boot",
            languages={"Java", "Kotlin"},
            extensions={".java", ".kt"},
            path_tokens={"controller", "controllers", "spring"},
            content_tokens={"@RestController", "@RequestMapping", "@GetMapping", "@PostMapping"},
            extraction_status="implemented_regex",
            capabilities=FrameworkCapabilities(
                supports_nested_routers=True,
                supports_controller_prefix=True,
                supports_openapi_annotations=True,
                supports_middleware_extraction=True,
                supports_auth_extraction=True,
            ),
            route_patterns=[r"@(Get|Post|Put|Delete|Patch)Mapping\b"],
            router_patterns=[r"@RequestMapping\b"],
        ),
        FrameworkAdapter(
            name="Micronaut",
            languages={"Java"},
            extensions={".java"},
            content_tokens={"@Controller", "io.micronaut.http.annotation"},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Quarkus",
            languages={"Java"},
            extensions={".java"},
            content_tokens={"@Path", "@GET", "@POST", "javax.ws.rs"},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Javalin",
            languages={"Java", "Kotlin"},
            extensions={".java", ".kt"},
            content_tokens={"Javalin.create", "app.get("},
            extraction_status="supported",
        ),

        # GO
        FrameworkAdapter(
            name="Go Gin/Fiber",
            languages={"Go"},
            extensions={".go"},
            path_tokens={"handler", "handlers", "routes", "router", "main"},
            content_tokens={".GET(", ".POST(", "gin.Default(", "fiber.New(", "gin.Context"},
            extraction_status="implemented_regex",
            capabilities=FrameworkCapabilities(
                supports_nested_routers=True,
                supports_controller_prefix=True,
                supports_middleware_extraction=True,
            ),
            route_patterns=[r"\b\w+\.(GET|POST|PUT|DELETE|PATCH)\b"],
            router_patterns=[r"\bGroup\s*\("],
        ),
        FrameworkAdapter(
            name="Echo",
            languages={"Go"},
            extensions={".go"},
            content_tokens={"echo.New(", ".GET(", "echo.Context"},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Chi",
            languages={"Go"},
            extensions={".go"},
            content_tokens={"chi.NewRouter(", "r.Get(", "r.Mount("},
            extraction_status="supported",
        ),

        # RUBY
        FrameworkAdapter(
            name="Rails",
            languages={"Ruby"},
            extensions={".rb"},
            path_tokens={"routes", "controllers"},
            content_tokens={"ActionController::Base", "Rails.application.routes.draw"},
            extraction_status="supported",
            capabilities=FrameworkCapabilities(
                supports_nested_routers=True,
                supports_resource_routes=True,
                supports_versioning=True,
            ),
        ),
        FrameworkAdapter(
            name="Sinatra",
            languages={"Ruby"},
            extensions={".rb"},
            content_tokens={"require 'sinatra'", "get '/", "post '/"},
            extraction_status="supported",
        ),
        FrameworkAdapter(
            name="Grape",
            languages={"Ruby"},
            extensions={".rb"},
            content_tokens={"Grape::API", "version '"},
            extraction_status="supported",
        ),

        # .NET
        FrameworkAdapter(
            name="ASP.NET Core",
            languages={"C#"},
            extensions={".cs"},
            path_tokens={"controllers", "api", "controller"},
            content_tokens={"[ApiController]", "[HttpGet", "[HttpPost", "MapGet(", "ControllerBase"},
            extraction_status="implemented_regex",
            capabilities=FrameworkCapabilities(
                supports_nested_routers=True,
                supports_controller_prefix=True,
                supports_openapi_annotations=True,
                supports_middleware_extraction=True,
                supports_auth_extraction=True,
            ),
            route_patterns=[r"\[Http(Get|Post|Put|Delete|Patch)"],
            router_patterns=[r"\[Route\s*\("],
        ),

        # OpenAPI Spec Extractor
        FrameworkAdapter(
            name="OpenAPI/Swagger",
            languages={"Spec"},
            extensions={".json", ".yaml", ".yml"},
            path_tokens={"openapi", "swagger", "api-docs"},
            content_tokens={"openapi:", "\"openapi\"", "swagger:", "\"swagger\""},
            extraction_status="implemented_spec",
        ),
    ]

    @classmethod
    def candidate_extensions(cls) -> Set[str]:
        extensions = set()
        for adapter in cls.ADAPTERS:
            extensions.update(adapter.extensions)
        return extensions

    @classmethod
    def detect_from_path(cls, path: str) -> List[str]:
        path_obj = PurePosixPath(path)
        suffix = path_obj.suffix.lower()
        lower_path = path.lower()
        detected = []
        for adapter in cls.ADAPTERS:
            if suffix not in adapter.extensions:
                continue
            if any(token in lower_path for token in adapter.path_tokens):
                detected.append(adapter.name)
        return detected

    @classmethod
    def detect_from_content(cls, path: str, content: str) -> List[str]:
        suffix = PurePosixPath(path).suffix.lower()
        detected = []
        for adapter in cls.ADAPTERS:
            if suffix not in adapter.extensions:
                continue
            if any(token.lower() in content.lower() for token in adapter.content_tokens):
                detected.append(adapter.name)
        return detected

    @classmethod
    def capabilities(cls) -> List[Dict[str, str]]:
        return [
            {
                "name": adapter.name,
                "languages": ", ".join(sorted(adapter.languages)),
                "status": adapter.extraction_status,
            }
            for adapter in cls.ADAPTERS
        ]
