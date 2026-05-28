import base64
import binascii
import os
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote

import requests


class GitHubContentServiceError(Exception):
    pass


class GitHubContentService:
    """Fetch raw backend source files from GitHub using the REST API."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json"
        }
        if self.token:
            if self.token.startswith("github_pat_"):
                self.headers["Authorization"] = f"Bearer {self.token}"
            else:
                self.headers["Authorization"] = f"token {self.token}"
        self.session = requests.Session()

    def _request(self, url: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        try:
            response = self.session.get(url, headers=self.headers, timeout=30)

            if response.status_code == 401:
                raise GitHubContentServiceError(
                    "Bad credentials: GitHub token is invalid or expired."
                )

            if response.status_code == 403:
                if response.headers.get("X-RateLimit-Remaining") == "0":
                    raise GitHubContentServiceError(
                        "GitHub rate limit exceeded. Provide a token or wait for reset."
                    )
                body = response.json() if response.content else {}
                message = body.get("message", "GitHub API forbidden")
                raise GitHubContentServiceError(f"GitHub API forbidden: {message}")

            if response.status_code == 404:
                raise GitHubContentServiceError(
                    "File path not found. Verify the repository tree and file path."
                )

            if response.status_code >= 400:
                body = response.json() if response.content else {}
                message = body.get("message", "GitHub API error")
                raise GitHubContentServiceError(f"GitHub API error: {message}")

            return response.json(), response.headers
        except requests.exceptions.Timeout:
            raise GitHubContentServiceError(
                "GitHub API request timed out while fetching file content."
            )
        except requests.exceptions.ConnectionError:
            raise GitHubContentServiceError(
                "Connection error to GitHub API while fetching file content."
            )

    def fetch_file_content(
        self,
        owner: str,
        repo: str,
        path: str,
        ref: Optional[str] = None,
    ) -> str:
        safe_path = quote(path, safe="/.")
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{safe_path}"
        if ref:
            url = f"{url}?ref={quote(ref, safe='')}"

        print(f"[API Doc Generator] Fetching content from GitHub for: {path}", flush=True)
        data, _ = self._request(url)

        if not isinstance(data, dict):
            raise GitHubContentServiceError(
                f"Unexpected GitHub content response for {path}."
            )

        if data.get("type") != "file":
            raise GitHubContentServiceError(
                f"GitHub content endpoint returned non-file type for {path}."
            )

        encoded_content = data.get("content")
        if not encoded_content or not isinstance(encoded_content, str):
            raise GitHubContentServiceError(
                f"Missing or invalid file content for {path}."
            )

        encoded_content = encoded_content.strip()
        try:
            raw_bytes = base64.b64decode(encoded_content, validate=False)
        except (binascii.Error, ValueError) as exc:
            raise GitHubContentServiceError(
                f"Base64 decode failed for {path}: {str(exc)}"
            )

        decoded_text = raw_bytes.decode("utf-8", errors="ignore")
        if not decoded_text:
            raise GitHubContentServiceError(
                f"Decoded file content is empty for {path}."
            )
        if "\x00" in decoded_text:
            raise GitHubContentServiceError(
                f"Binary-like file detected for {path}."
            )

        print(f"[API Doc Generator] Content decoded successfully for: {path}", flush=True)
        return decoded_text

    def fetch_multiple_files(
        self,
        owner: str,
        repo: str,
        paths: List[str],
        ref: Optional[str] = None,
    ) -> Dict[str, str]:
        contents = {}
        for path in paths:
            contents[path] = self.fetch_file_content(owner, repo, path, ref=ref)
        return contents
