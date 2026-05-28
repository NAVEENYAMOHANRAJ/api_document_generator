from pathlib import Path, PurePosixPath
from typing import Dict, List, Tuple, Optional
from zipfile import BadZipFile, ZipFile
import io
from concurrent.futures import ThreadPoolExecutor

from api_doc_generator.scanner.framework_adapter_registry import FrameworkAdapterRegistry

TEXT_EXTENSIONS = FrameworkAdapterRegistry.candidate_extensions()

IGNORE_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    "env",
    "dist",
    "build",
    "coverage",
}


class LocalCodeServiceError(Exception):
    """Raised when local code input cannot be read safely."""


class LocalCodeService:
    """Read local folders or ZIP uploads into the common extraction file shape with prioritization and encoding fallback."""

    MAX_FILE_SIZE = 10_485_760  # 10MB
    ENCODINGS = ["utf-8", "utf-16", "latin1", "shift-jis"]

    @classmethod
    def collect_from_folder(cls, folder_path: str) -> Tuple[List[Dict], List[Dict]]:
        root = Path(folder_path).expanduser().resolve()
        if not root.exists():
            raise LocalCodeServiceError(f"Folder does not exist: {folder_path}")
        if not root.is_dir():
            raise LocalCodeServiceError(f"Path is not a folder: {folder_path}")

        # Collect paths
        paths = []
        for path in root.rglob("*"):
            if not path.is_file() or not cls._is_candidate_text_file(path):
                continue
            if cls._has_ignored_segment(path.relative_to(root)):
                continue
            paths.append(path)

        # Prioritize files (routes -> controllers -> middleware -> serializers -> views -> models)
        def get_priority(p: Path) -> int:
            n = p.name.lower()
            if "route" in n:
                return 1
            if "controller" in n:
                return 2
            if "middleware" in n:
                return 3
            if "serializer" in n:
                return 4
            if "view" in n:
                return 5
            if "model" in n:
                return 6
            return 7

        paths.sort(key=lambda p: (get_priority(p), str(p)))

        files = []
        errors = []

        def load_file(path: Path) -> Tuple[Optional[Dict], Optional[Dict]]:
            relative_path = str(PurePosixPath(path.relative_to(root).as_posix()))
            try:
                size = path.stat().st_size
                if size > cls.MAX_FILE_SIZE:
                    return None, {"file": relative_path, "error": f"File larger than 10MB skipped ({size} bytes)."}

                # Try multi-encoding decode fallback
                content = None
                for enc in cls.ENCODINGS:
                    try:
                        content = path.read_text(encoding=enc)
                        break
                    except Exception:
                        continue

                if content is None:
                    return None, {"file": relative_path, "error": "Failed to decode file with standard encodings."}

                return {"path": relative_path, "content": content, "size": size}, None
            except Exception as exc:
                return None, {"file": relative_path, "error": str(exc)}

        # Load files in parallel
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(load_file, paths))

        for file_data, err in results:
            if file_data:
                files.append(file_data)
            if err:
                errors.append(err)

        return files, errors

    @classmethod
    def collect_from_zip_bytes(cls, archive_bytes: bytes) -> Tuple[List[Dict], List[Dict]]:
        files = []
        errors = []
        try:
            with ZipFile(io.BytesIO(archive_bytes)) as archive:
                infos = []
                for info in archive.infolist():
                    if info.is_dir():
                        continue

                    path = PurePosixPath(info.filename)
                    if path.is_absolute() or ".." in path.parts:
                        errors.append({"file": info.filename, "error": "Unsafe archive path skipped."})
                        continue
                    if cls._has_ignored_segment(path) or path.suffix.lower() not in TEXT_EXTENSIONS:
                        continue
                    infos.append(info)

                # Prioritize zip infos
                def get_priority(info) -> int:
                    n = PurePosixPath(info.filename).name.lower()
                    if "route" in n:
                        return 1
                    if "controller" in n:
                        return 2
                    if "middleware" in n:
                        return 3
                    if "serializer" in n:
                        return 4
                    if "view" in n:
                        return 5
                    if "model" in n:
                        return 6
                    return 7

                infos.sort(key=lambda info: (get_priority(info), info.filename))

                for info in infos:
                    path = PurePosixPath(info.filename)
                    if info.file_size > cls.MAX_FILE_SIZE:
                        errors.append({"file": str(path), "error": f"File larger than 10MB skipped ({info.file_size} bytes)."})
                        continue

                    try:
                        raw_data = archive.read(info)
                        content = None
                        for enc in cls.ENCODINGS:
                            try:
                                content = raw_data.decode(enc)
                                break
                            except Exception:
                                continue

                        if content is None:
                            errors.append({"file": str(path), "error": "Failed to decode file with standard encodings."})
                            continue

                        files.append({"path": str(path), "content": content, "size": info.file_size})
                    except Exception as exc:
                        errors.append({"file": str(path), "error": str(exc)})
        except BadZipFile:
            raise LocalCodeServiceError("Uploaded file is not a valid ZIP archive.")

        return files, errors

    @staticmethod
    def _is_candidate_text_file(path: Path) -> bool:
        return path.suffix.lower() in TEXT_EXTENSIONS

    @staticmethod
    def _has_ignored_segment(path: PurePosixPath) -> bool:
        return any(part.lower() in IGNORE_DIRS for part in path.parts)
