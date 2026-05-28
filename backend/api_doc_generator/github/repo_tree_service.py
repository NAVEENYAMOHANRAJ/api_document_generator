import os
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote, urlparse, urlunparse

import requests


class GitHubRepositoryTreeError(Exception):
    pass


class RepoTreeService:
    """Fetch GitHub repository tree metadata without cloning or downloading repo content."""

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

    def _request(self, url: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        try:
            response = requests.get(url, headers=self.headers, timeout=30)

            if response.status_code == 401:
                raise GitHubRepositoryTreeError(
                    "Bad credentials: GitHub token is invalid or expired."
                )

            if response.status_code == 403:
                if response.headers.get("X-RateLimit-Remaining") == "0":
                    raise GitHubRepositoryTreeError(
                        "GitHub rate limit exceeded. Provide a token or wait for reset."
                    )
                body = response.json() if response.content else {}
                message = body.get("message", "Forbidden by GitHub API")
                raise GitHubRepositoryTreeError(f"GitHub API forbidden: {message}")

            if response.status_code == 404:
                raise GitHubRepositoryTreeError(
                    "Repository or branch not found. Check the URL and token scope."
                )

            if response.status_code >= 400:
                body = response.json() if response.content else {}
                message = body.get("message", "GitHub API error")
                raise GitHubRepositoryTreeError(f"GitHub API error: {message}")

            return response.json(), response.headers
        except requests.exceptions.Timeout:
            raise GitHubRepositoryTreeError(
                "GitHub API request timed out. Try again later."
            )
        except requests.exceptions.ConnectionError:
            raise GitHubRepositoryTreeError(
                "Connection error to GitHub API. Check your internet and try again."
            )

    def sanitize_github_url(self, repo_url: str) -> str:
        """Normalize GitHub repository URLs and remove query, fragment, and trailing slash."""
        if not repo_url or not isinstance(repo_url, str):
            raise GitHubRepositoryTreeError("Invalid GitHub URL provided.")

        original = repo_url
        trimmed = repo_url.strip()
        parsed = urlparse(trimmed)

        if parsed.scheme and parsed.scheme not in {"http", "https"}:
            raise GitHubRepositoryTreeError("Unsupported URL scheme for GitHub URL.")

        if parsed.netloc:
            host = parsed.netloc.lower()
            if host not in {"github.com", "www.github.com"}:
                raise GitHubRepositoryTreeError("Invalid GitHub URL host.")

            sanitized_path = parsed.path.rstrip("/")
            sanitized_url = urlunparse((parsed.scheme, parsed.netloc, sanitized_path, "", "", ""))
        else:
            sanitized_url = trimmed.rstrip("/")

        print(
            f"[RepoTreeService] sanitize_github_url: original={original}, sanitized={sanitized_url}",
            flush=True,
        )
        return sanitized_url

    def parse_github_url(self, repo_url: str) -> tuple[str, str]:
        """Extract owner and repository name from a GitHub URL or owner/repo string."""
        sanitized = self.sanitize_github_url(repo_url)
        parsed = urlparse(sanitized)

        if parsed.netloc:
            path = parsed.path
        else:
            path = sanitized

        parts = [segment for segment in path.split("/") if segment and segment.lower() not in {
            "tree",
            "blob",
            "pulls",
            "issues",
            "commit",
            "releases",
        }]

        if len(parts) < 2:
            raise GitHubRepositoryTreeError(
                "Invalid GitHub URL. Use https://github.com/owner/repo or owner/repo"
            )

        owner = parts[0]
        repo = parts[1]
        if repo.endswith(".git"):
            repo = repo[:-4]

        print(
            f"[RepoTreeService] parse_github_url: owner={owner}, repo={repo}",
            flush=True,
        )
        return owner, repo

    def get_repository_metadata(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch repository metadata and return the default branch."""
        print(f"[RepoTreeService] Fetching repository metadata for {owner}/{repo}", flush=True)
        url = f"{self.base_url}/repos/{owner}/{repo}"
        data, _ = self._request(url)

        branch = data.get("default_branch")
        if not branch:
            raise GitHubRepositoryTreeError(
                "Unable to determine repository default branch from GitHub metadata."
            )

        print(
            f"[RepoTreeService] Repository metadata fetched: default_branch={branch}",
            flush=True,
        )
        return {"default_branch": branch, "full_name": data.get("full_name")}

    def get_default_branch(self, owner: str, repo: str) -> str:
        """Return the repository default branch name."""
        return self.get_repository_metadata(owner, repo)["default_branch"]

    def _fetch_branch_data(self, owner: str, repo: str, branch: str) -> Dict[str, Any]:
        branch_name = quote(branch, safe="")
        print(
            f"[RepoTreeService] Fetching branch details for {owner}/{repo}@{branch_name}",
            flush=True,
        )
        url = f"{self.base_url}/repos/{owner}/{repo}/branches/{branch_name}"
        data, _ = self._request(url)
        return data

    def get_branch_sha(self, owner: str, repo: str, branch: str) -> str:
        """Fetch branch information and return the commit SHA for the default branch."""
        branch_data = self._fetch_branch_data(owner, repo, branch)
        commit = branch_data.get("commit")
        if not isinstance(commit, dict):
            raise GitHubRepositoryTreeError(
                "Unable to resolve branch commit information from GitHub."
            )

        sha = commit.get("sha")
        if not sha:
            sha = commit.get("commit", {}).get("sha")

        if not sha:
            raise GitHubRepositoryTreeError(
                "Unable to resolve commit SHA for the default branch."
            )

        print(
            f"[RepoTreeService] Resolved branch SHA for {owner}/{repo}@{branch}: {sha}",
            flush=True,
        )
        return sha

    def _extract_tree_sha_from_branch_data(self, branch_data: Dict[str, Any]) -> Optional[str]:
        commit = branch_data.get("commit")
        if not isinstance(commit, dict):
            return None
        tree = commit.get("commit", {}).get("tree", {})
        if not isinstance(tree, dict):
            return None
        return tree.get("sha")

    def get_recursive_tree(self, owner: str, repo: str, sha: str) -> tuple[List[Dict[str, Any]], bool]:
        """
        Fetch the repository tree recursively using the provided SHA.

        Returns:
            tuple: (tree_entries, tree_truncated)
        """
        if not sha:
            raise GitHubRepositoryTreeError("Missing SHA when fetching repository tree.")

        print(
            f"[RepoTreeService] Fetching recursive tree for {owner}/{repo} with SHA {sha}",
            flush=True,
        )
        tree_sha = quote(sha, safe="")
        url = f"{self.base_url}/repos/{owner}/{repo}/git/trees/{tree_sha}?recursive=1"
        data, _ = self._request(url)

        tree = data.get("tree")
        if not isinstance(tree, list):
            raise GitHubRepositoryTreeError(
                "Unexpected tree response from GitHub. Expected a list of tree entries."
            )

        # Check if tree was truncated by GitHub API
        truncated = data.get("truncated", False)
        if truncated:
            print(
                f"[RepoTreeService] Tree truncated: True (GitHub API limit reached)",
                flush=True,
            )
        else:
            print(
                f"[RepoTreeService] Tree truncated: False",
                flush=True,
            )

        print(
            f"[RepoTreeService] Recursive tree fetched: {len(tree)} total entries, truncated={truncated}",
            flush=True,
        )
        blob_entries = [entry for entry in tree if entry.get("type") == "blob"]
        return blob_entries, truncated

    def get_repository_tree(self, owner: str, repo: str) -> tuple[List[Dict[str, Any]], bool]:
        """
        Orchestrate the full GitHub repository tree resolution flow.

        Returns:
            tuple: (tree_entries, tree_truncated)
        """
        metadata = self.get_repository_metadata(owner, repo)
        default_branch = metadata["default_branch"]

        try:
            commit_sha = self.get_branch_sha(owner, repo, default_branch)
            return self.get_recursive_tree(owner, repo, commit_sha)
        except GitHubRepositoryTreeError as first_error:
            print(
                f"[RepoTreeService] Primary tree fetch failed: {str(first_error)}",
                flush=True,
            )

        branch_data = self._fetch_branch_data(owner, repo, default_branch)
        tree_sha = self._extract_tree_sha_from_branch_data(branch_data)
        if not tree_sha:
            raise GitHubRepositoryTreeError(
                "Unable to resolve a fallback tree SHA for the default branch."
            )

        print(
            f"[RepoTreeService] Attempting fallback tree fetch using tree SHA {tree_sha}",
            flush=True,
        )
        return self.get_recursive_tree(owner, repo, tree_sha)

    def fetch_repository_tree(self, owner: str, repo: str) -> tuple[List[Dict[str, Any]], bool]:
        """
        Fetch the repository tree metadata using the repository default branch.

        Returns:
            tuple: (tree_entries, tree_truncated)
        """
        return self.get_repository_tree(owner, repo)
