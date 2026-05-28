import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

import re
from api_doc_generator.extractors.extraction_pipeline import ExtractionPipeline
from api_doc_generator.generators.openapi_generator import OpenAPIGenerator
from api_doc_generator.extractors.generic_framework_extractor import GenericFrameworkExtractor


def test_spring_boot_extractor_overhaul():
    controller_content = """
    package com.example.demo;
    import org.springframework.web.bind.annotation.*;
    import org.springframework.web.server.ResponseStatusException;
    import org.springframework.http.HttpStatus;

    @RestController
    @RequestMapping("/api/v1/products")
    public class ProductController {

        @GetMapping("/{id}")
        public Product getProduct(
            @PathVariable("id") Long productId,
            @RequestParam(value = "search", required = false) String query
        ) {
            if (productId < 0) {
                throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Product not found");
            }
            return new Product();
        }

        @PostMapping
        public Product createProduct(@RequestBody ProductDto dto) {
            return new Product();
        }
    }
    """
    dto_content = """
    package com.example.demo;
    public class ProductDto {
        private String name;
        private int price;
        private boolean active;
    }
    """
    
    pipeline = ExtractionPipeline(batch_size=10)
    pipeline.add_files([
        {"path": "src/main/java/com/example/demo/ProductController.java", "content": controller_content},
        {"path": "src/main/java/com/example/demo/ProductDto.java", "content": dto_content}
    ])
    endpoints, errors, stats = pipeline.run()
    
    assert errors == []
    get_endpoint = next(e for e in endpoints if e["path"] == "/api/v1/products/{id}" and e["method"] == "GET")
    assert get_endpoint["framework"] == "Spring Boot"
    assert len(get_endpoint["path_params"]) == 1
    assert get_endpoint["path_params"][0]["name"] == "id"
    assert len(get_endpoint["query_params"]) == 1
    assert get_endpoint["query_params"][0]["name"] == "search"
    assert any(r["status_code"] == 404 for r in get_endpoint["responses"])
    
    post_endpoint = next(e for e in endpoints if e["path"] == "/api/v1/products" and e["method"] == "POST")
    assert post_endpoint["request_body"]["model"] == "ProductDto"
    props = post_endpoint["request_body"]["schema"]["properties"]
    assert props["name"]["type"] == "string"
    assert props["price"]["type"] == "integer"
    assert props["active"]["type"] == "boolean"


def test_express_router_cross_file_prefix_propagation():
    server_content = """
    const express = require('express');
    const productRoutes = require('./routes/products');
    const app = express();
    app.use('/api/v1', productRoutes);
    """
    routes_content = """
    const express = require('express');
    const router = express.Router();
    
    router.get('/list', (req, res) => {
        res.json({ products: [] });
    });
    
    module.exports = router;
    """
    
    pipeline = ExtractionPipeline(batch_size=10)
    pipeline.add_files([
        {"path": "server.js", "content": server_content},
        {"path": "routes/products.js", "content": routes_content}
    ])
    endpoints, errors, stats = pipeline.run()
    
    assert errors == []
    endpoint = next(e for e in endpoints if e["path"] == "/api/v1/list")
    assert endpoint["framework"] == "Express"
    assert endpoint["method"] == "GET"


def test_drf_nested_serializers_and_serializer_method_field():
    files = [
        {
            "path": "proj/urls.py",
            "content": (
                "from django.urls import include, path\n"
                "from .views import AuthorViewSet\n"
                "from rest_framework.routers import DefaultRouter\n"
                "router = DefaultRouter()\n"
                "router.register('authors', AuthorViewSet, basename='author')\n"
                "urlpatterns = [path('', include(router.urls))]\n"
            ),
        },
        {
            "path": "proj/models.py",
            "content": (
                "from django.db import models\n"
                "class Author(models.Model):\n"
                "    name = models.CharField(max_length=100)\n"
            ),
        },
        {
            "path": "proj/serializers.py",
            "content": (
                "from rest_framework import serializers\n"
                "from .models import Author\n"
                "class BookSerializer(serializers.Serializer):\n"
                "    title = serializers.CharField()\n"
                "    pages = serializers.IntegerField()\n"
                "class AuthorSerializer(serializers.ModelSerializer):\n"
                "    favorite_book = BookSerializer()\n"
                "    is_active = serializers.SerializerMethodField()\n"
                "    class Meta:\n"
                "        model = Author\n"
                "        fields = ['name', 'favorite_book', 'is_active']\n"
                "    def get_is_active(self, obj):\n"
                "        return True\n"
            ),
        },
        {
            "path": "proj/views.py",
            "content": (
                "from rest_framework import viewsets\n"
                "from .models import Author\n"
                "from .serializers import AuthorSerializer\n"
                "class AuthorViewSet(viewsets.ModelViewSet):\n"
                "    queryset = Author.objects.all()\n"
                "    serializer_class = AuthorSerializer\n"
            ),
        },
    ]
    
    pipeline = ExtractionPipeline(batch_size=10)
    pipeline.add_files(files)
    endpoints, errors, stats = pipeline.run()
    
    assert errors == []
    openapi = OpenAPIGenerator.generate(endpoints, "Author API")
    
    assert "BookResponse" in openapi["components"]["schemas"]
    assert "BookRequest" in openapi["components"]["schemas"]
    
    author_resp = openapi["components"]["schemas"]["AuthorResponse"]
    assert author_resp["properties"]["favorite_book"] == {
        "$ref": "#/components/schemas/BookResponse"
    }
    
    assert author_resp["properties"]["is_active"]["type"] == "boolean"


def test_laravel_middleware_validation_and_form_requests():
    routes_content = """
    <?php
    use Illuminate\\Support\\Facades\\Route;
    use App\\Http\\Controllers\\ProductController;

    Route::middleware('auth:sanctum')->prefix('v2')->group(function () {
        Route::post('/products', [ProductController::class, 'store']);
        Route::get('/products/{product}', [ProductController::class, 'show']);
    });
    """
    
    controller_content = """
    <?php
    namespace App\\Http\\Controllers;
    use App\\Http\\Requests\\StoreProductRequest;
    use Illuminate\\Http\\Request;

    class ProductController extends Controller {
        public function __construct() {
            $this->middleware('auth:api')->only('show');
        }

        public function store(StoreProductRequest $request) {
            return response()->json(['message' => 'success'], 201);
        }

        public function show(Request $request, $product) {
            $request->validate([
                'detail_level' => 'required|string'
            ]);
            return response()->json(['id' => 1], 200);
        }
    }
    """
    
    request_content = """
    <?php
    namespace App\\Http\\Requests;
    class StoreProductRequest {
        public function rules() {
            return [
                'title' => 'required|string',
                'price' => 'required|integer',
                'tags' => ['nullable', 'array']
            ];
        }
    }
    """
    
    pipeline = ExtractionPipeline(batch_size=10)
    pipeline.add_files([
        {"path": "routes/api.php", "content": routes_content},
        {"path": "app/Http/Controllers/ProductController.php", "content": controller_content},
        {"path": "app/Http/Requests/StoreProductRequest.php", "content": request_content}
    ])
    endpoints, errors, stats = pipeline.run()
    
    assert errors == []
    
    post_prod = next(e for e in endpoints if e["path"] == "/v2/products" and e["method"] == "POST")
    assert post_prod["request_body"]["model"] == "StoreProductRequest"
    assert "title" in post_prod["request_body"]["schema"]["properties"]
    assert post_prod["request_body"]["schema"]["properties"]["price"]["type"] == "integer"
    assert post_prod["request_body"]["schema"]["required"] == ["title", "price"]
    assert post_prod["security"] == [{"tokenAuth": []}, {"jwtAuth": []}]
    assert any(r["status_code"] == 401 for r in post_prod["responses"])
    
    get_prod = next(e for e in endpoints if e["path"] == "/v2/products/{product}" and e["method"] == "GET")
    assert get_prod["path"] == "/v2/products/{product}"
    assert len(get_prod["query_params"]) == 1
    assert get_prod["query_params"][0]["name"] == "detail_level"
    assert get_prod["query_params"][0]["required"] is True
    assert get_prod["security"] == [{"tokenAuth": []}, {"jwtAuth": []}]
