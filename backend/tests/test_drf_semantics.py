import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from api_doc_generator.extractors.extraction_pipeline import ExtractionPipeline
from api_doc_generator.generators.openapi_generator import OpenAPIGenerator


def test_drf_semantic_extraction_uses_endpoint_aware_pagination_and_components():
    files = [
        {
            "path": "proj/urls.py",
            "content": (
                "from django.urls import include, path\n"
                "from rest_framework.schemas import get_schema_view\n"
                "urlpatterns = [\n"
                "    path('', include('snippets.urls')),\n"
                "    path('docs/', get_schema_view(title='API')),\n"
                "    path('schema/', get_schema_view(title='API')),\n"
                "]\n"
            ),
        },
        {
            "path": "snippets/urls.py",
            "content": (
                "from django.urls import include, path\n"
                "from rest_framework.routers import DefaultRouter\n"
                "from .views import SnippetViewSet\n"
                "router = DefaultRouter()\n"
                "router.register('snippets', SnippetViewSet, basename='snippet')\n"
                "urlpatterns = [path('', include(router.urls))]\n"
            ),
        },
        {
            "path": "snippets/models.py",
            "content": (
                "from django.db import models\n"
                "class Snippet(models.Model):\n"
                "    title = models.CharField(max_length=100, blank=True)\n"
                "    code = models.TextField()\n"
                "    favorited = models.BooleanField(default=False)\n"
                "    created = models.DateTimeField(auto_now_add=True)\n"
            ),
        },
        {
            "path": "snippets/serializers.py",
            "content": (
                "from rest_framework import serializers\n"
                "from .models import Snippet\n"
                "class SnippetSerializer(serializers.ModelSerializer):\n"
                "    id = serializers.IntegerField(read_only=True)\n"
                "    url = serializers.URLField(read_only=True)\n"
                "    owner = serializers.PrimaryKeyRelatedField(read_only=True)\n"
                "    highlight = serializers.HyperlinkedIdentityField(read_only=True)\n"
                "    class Meta:\n"
                "        model = Snippet\n"
                "        fields = ['id', 'url', 'title', 'code', 'owner', 'highlight', 'favorited', 'created']\n"
            ),
        },
        {
            "path": "snippets/views.py",
            "content": (
                "from rest_framework import viewsets\n"
                "from rest_framework.decorators import action\n"
                "from rest_framework.permissions import IsAuthenticated\n"
                "from .models import Snippet\n"
                "from .serializers import SnippetSerializer\n"
                "class SnippetViewSet(viewsets.ModelViewSet):\n"
                "    queryset = Snippet.objects.all()\n"
                "    serializer_class = SnippetSerializer\n"
                "    permission_classes = [IsAuthenticated]\n"
                "    @action(detail=True, methods=['get'], url_path='highlight')\n"
                "    def highlight(self, request, pk=None):\n"
                "        pass\n"
                "    def get_queryset(self):\n"
                "        return Snippet.objects.all()\n"
                "    def filter_queryset(self, queryset):\n"
                "        return queryset\n"
            ),
        },
    ]

    pipeline = ExtractionPipeline(batch_size=20)
    pipeline.add_files(files)
    endpoints, errors, stats = pipeline.run()
    openapi = OpenAPIGenerator.generate(endpoints, "Probe")

    assert errors == []
    by_key = {(endpoint["method"], endpoint["path"]): endpoint for endpoint in endpoints}

    assert by_key[("GET", "/snippets")]["query_params"][0]["name"] == "limit"
    assert by_key[("GET", "/docs")].get("query_params") is None
    assert by_key[("GET", "/schema")].get("query_params") is None

    delete_responses = openapi["paths"]["/snippets/{id}"]["delete"]["responses"]
    assert "204" in delete_responses
    assert "content" not in delete_responses["204"]

    serializer_schema = openapi["components"]["schemas"]["SnippetResponse"]
    assert serializer_schema["required"] == ["code"]
    assert serializer_schema["properties"]["id"]["readOnly"] is True
    assert serializer_schema["properties"]["favorited"]["type"] == "boolean"
    assert serializer_schema["properties"]["created"]["format"] == "date-time"

    assert openapi["paths"]["/snippets"]["get"]["responses"]["200"]["content"]["application/json"]["schema"] == {
        "type": "array",
        "items": {"$ref": "#/components/schemas/SnippetResponse"},
    }
    assert openapi["x-schema-reuse-count"] > 0
    assert stats["models_detected"] == 1
    assert stats["custom_actions_detected"] == 1
    assert stats["router_graph_nodes"] > 0
    assert {endpoint["method"] for endpoint in endpoints} <= {"GET", "POST", "PUT", "PATCH", "DELETE"}


def test_drf_regex_paths_and_internal_actions_are_normalized():
    files = [
        {
            "path": "proj/urls.py",
            "content": (
                "from django.conf.urls import url\n"
                "from .views import ArticleViewSet\n"
                "urlpatterns = [\n"
                "    url(r'^api/articles/(?P<article_slug>[-\\w]+)/favorite/?$', ArticleViewSet.as_view({'post': 'favorite'})),\n"
                "    url(r'^admin/', admin.site.urls),\n"
                "]\n"
            ),
        },
        {
            "path": "proj/models.py",
            "content": (
                "from django.db import models\n"
                "class Article(models.Model):\n"
                "    slug = models.SlugField()\n"
                "    favoritesCount = models.IntegerField(default=0)\n"
                "    createdAt = models.DateTimeField(auto_now_add=True)\n"
            ),
        },
        {
            "path": "proj/serializers.py",
            "content": (
                "from rest_framework import serializers\n"
                "from .models import Article\n"
                "class ArticleSerializer(serializers.ModelSerializer):\n"
                "    favorited = serializers.BooleanField(read_only=True)\n"
                "    class Meta:\n"
                "        model = Article\n"
                "        fields = ['slug', 'favorited', 'favoritesCount', 'createdAt']\n"
            ),
        },
        {
            "path": "proj/views.py",
            "content": (
                "from rest_framework import viewsets\n"
                "from rest_framework.decorators import action\n"
                "from .serializers import ArticleSerializer\n"
                "class ArticleViewSet(viewsets.ModelViewSet):\n"
                "    serializer_class = ArticleSerializer\n"
                "    lookup_field = 'slug'\n"
                "    @action(detail=True, methods=['post'])\n"
                "    def favorite(self, request, article_slug=None):\n"
                "        pass\n"
                "    def get_queryset(self):\n"
                "        pass\n"
                "    def filter_queryset(self, queryset):\n"
                "        pass\n"
            ),
        },
    ]

    pipeline = ExtractionPipeline(batch_size=20)
    pipeline.add_files(files)
    endpoints, errors, _ = pipeline.run()
    openapi = OpenAPIGenerator.generate(endpoints, "Probe")

    assert errors == []
    assert ("post", "/api/articles/{article_slug}/favorite") in {
        (method, path)
        for path, methods in openapi["paths"].items()
        for method in methods
    }
    assert "/admin" not in openapi["paths"]
    assert all(method.upper() in {"GET", "POST", "PUT", "PATCH", "DELETE"} for endpoint in endpoints for method in [endpoint["method"]])
    assert "post" in openapi["paths"]["/api/articles/{article_slug}/favorite"]
    assert openapi["paths"]["/api/articles/{article_slug}/favorite"]["post"]["operationId"] == "favoriteArticle"
    assert openapi["components"]["schemas"]["ArticleResponse"]["properties"]["createdAt"]["format"] == "date-time"
    assert openapi["x-openapi-validation"]["valid"] is True
