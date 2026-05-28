from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Type

from api_doc_generator.frameworks.base import FrameworkRouteExtractor
from api_doc_generator.extractors.fastapi_extractor import FastAPIExtractor
from api_doc_generator.extractors.flask_extractor import FlaskExtractor
from api_doc_generator.extractors.django_extractor import DjangoExtractor
from api_doc_generator.extractors.laravel_extractor import LaravelExtractor
from api_doc_generator.extractors.express_extractor import ExpressExtractor
from api_doc_generator.extractors.nestjs_extractor import NestJSExtractor
from api_doc_generator.extractors.spring_boot_extractor import SpringBootExtractor
from api_doc_generator.extractors.aspnet_extractor import AspNetExtractor
from api_doc_generator.extractors.go_extractor import GoExtractor


@dataclass(frozen=True)
class FrameworkExtractorEntry:
    name: str
    strategy: str  # ast | regex | spec
    extractor: object


class FrameworkExtractorRegistry:
    """
    Central routing for framework extractors.

    This is the single place where we decide which extractor is used per framework.
    The extractor must return only source-grounded metadata.
    """

    _REGISTRY: Dict[str, FrameworkExtractorEntry] = {
        "FastAPI": FrameworkExtractorEntry(name="FastAPI", strategy="ast", extractor=FastAPIExtractor),
        "Flask": FrameworkExtractorEntry(name="Flask", strategy="ast", extractor=FlaskExtractor),
        "Django REST Framework": FrameworkExtractorEntry(name="Django REST Framework", strategy="ast", extractor=DjangoExtractor),
        "Django": FrameworkExtractorEntry(name="Django", strategy="ast", extractor=DjangoExtractor),
        "Laravel": FrameworkExtractorEntry(name="Laravel", strategy="regex", extractor=LaravelExtractor),
        "Express": FrameworkExtractorEntry(name="Express", strategy="regex", extractor=ExpressExtractor),
        "NestJS": FrameworkExtractorEntry(name="NestJS", strategy="regex", extractor=NestJSExtractor),
        "Spring Boot": FrameworkExtractorEntry(name="Spring Boot", strategy="regex", extractor=SpringBootExtractor),
        "ASP.NET Core": FrameworkExtractorEntry(name="ASP.NET Core", strategy="regex", extractor=AspNetExtractor),
        "Go Gin/Fiber": FrameworkExtractorEntry(name="Go Gin/Fiber", strategy="regex", extractor=GoExtractor),
    }

    @classmethod
    def get(cls, framework: str) -> Optional[FrameworkExtractorEntry]:
        return cls._REGISTRY.get(framework)

