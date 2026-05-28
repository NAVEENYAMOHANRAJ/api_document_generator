from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol


@dataclass(frozen=True)
class ExtractionWarning:
    code: str
    message: str
    file: Optional[str] = None
    line: Optional[int] = None


class FrameworkRouteExtractor(Protocol):
    """Extract routes/endpoints from a single source file."""

    framework_name: str

    def extract(self, file_path: str, content: str) -> tuple[list[Dict[str, Any]], list[ExtractionWarning]]: ...

