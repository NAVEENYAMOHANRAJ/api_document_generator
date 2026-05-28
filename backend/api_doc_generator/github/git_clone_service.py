import os
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, Tuple
from urllib.parse import quote, urlparse

from api_doc_generator.services.data_processor import parse_github_repo_url


class GitCloneServiceError(Exception):
    """Raised when a GitHub repository cannot be cloned safely."""


class GitCloneService:
    """Clone GitHub repositories into temporary local folders for extraction."""

    CLONE_TIMEOUT_SECONDS = 240

    @classmethod
    @contextmanager
    def clone_to_temp(cls, repo_url: str, token: Optional[str] = None) -> Iterator[Tuple[Path, str, str]]:
        owner, repo = parse_github_repo_url(repo_url)
        clone_url = cls._clone_url(owner, repo, token)
        safe_url = cls._clone_url(owner, repo, None)

        with tempfile.TemporaryDirectory(prefix="api-doc-generator-") as temp_dir:
            target = Path(temp_dir) / repo
            cls._run_clone(clone_url, safe_url, target)
            yield target, owner, repo

    @staticmethod
    def _clone_url(owner: str, repo: str, token: Optional[str]) -> str:
        repo_name = repo[:-4] if repo.endswith(".git") else repo
        if not token:
            return f"https://github.com/{owner}/{repo_name}.git"

        safe_token = quote(token, safe="")
        return f"https://x-access-token:{safe_token}@github.com/{owner}/{repo_name}.git"

    @classmethod
    def _run_clone(cls, clone_url: str, safe_url: str, target: Path) -> None:
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"

        command = [
            "git",
            "clone",
            "--depth",
            "1",
            "--single-branch",
            clone_url,
            str(target),
        ]
        print(f"[GitCloneService] Cloning repository: {safe_url}", flush=True)

        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=cls.CLONE_TIMEOUT_SECONDS,
                env=env,
            )
        except FileNotFoundError:
            raise GitCloneServiceError("git executable was not found. Install Git and try again.")
        except subprocess.TimeoutExpired:
            raise GitCloneServiceError("Repository clone timed out. Try a smaller repository or check network access.")

        if result.returncode != 0:
            stderr = cls._redact_clone_url(result.stderr or result.stdout or "Unknown git clone error", clone_url)
            raise GitCloneServiceError(f"git clone failed: {stderr.strip()}")

        if not target.exists() or not target.is_dir():
            raise GitCloneServiceError("Repository clone completed but the checkout folder was not created.")

        print(f"[GitCloneService] Clone complete: {safe_url}", flush=True)

    @staticmethod
    def _redact_clone_url(message: str, clone_url: str) -> str:
        parsed = urlparse(clone_url)
        if parsed.username or parsed.password:
            redacted = clone_url.replace(parsed.netloc, "github.com")
            message = message.replace(clone_url, redacted)
        return message
