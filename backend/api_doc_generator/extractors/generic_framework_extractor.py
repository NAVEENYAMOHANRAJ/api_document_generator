"""Generic framework extractor - dispatcher for framework-specific extractors."""

from typing import Dict, List, Optional, Callable

Endpoint = Dict
Resolver = Optional[Callable[[str], Optional[str]]]


class GenericFrameworkExtractor:
    """Generic extractor that dispatches to framework-specific extractors."""

    @classmethod
    def extract(
        cls,
        file_path: str,
        content: str,
        framework: str,
        cross_file_resolver: Resolver = None,
    ) -> List[Endpoint]:
        """Extract endpoints based on framework."""
        from api_doc_generator.extractors.fastapi_extractor import FastAPIExtractor
        from api_doc_generator.extractors.flask_extractor import FlaskExtractor
        from api_doc_generator.extractors.django_extractor import DjangoExtractor
        from api_doc_generator.extractors.laravel_extractor import LaravelExtractor
        from api_doc_generator.extractors.express_extractor import ExpressExtractor
        from api_doc_generator.extractors.nestjs_extractor import NestJSExtractor
        from api_doc_generator.extractors.spring_boot_extractor import SpringBootExtractor
        from api_doc_generator.extractors.aspnet_extractor import AspNetExtractor
        from api_doc_generator.extractors.go_extractor import GoExtractor

        if framework == "FastAPI":
            return FastAPIExtractor.extract(file_path, content)
        elif framework == "Flask":
            return FlaskExtractor.extract(file_path, content)
        elif framework in ("Django REST Framework", "Django"):
            return DjangoExtractor.extract(file_path, content)
        elif framework == "Laravel":
            return LaravelExtractor.extract(file_path, content)
        elif framework == "Express":
            return ExpressExtractor.extract(file_path, content)
        elif framework == "NestJS":
            return NestJSExtractor.extract(file_path, content)
        elif framework == "Spring Boot":
            return SpringBootExtractor.extract(file_path, content)
        elif framework == "ASP.NET Core":
            return AspNetExtractor.extract(file_path, content)
        elif framework == "Go Gin/Fiber":
            return GoExtractor.extract(file_path, content)
        
        return []
