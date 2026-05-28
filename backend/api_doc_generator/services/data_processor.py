from urllib.parse import urlparse, urlunparse


def parse_github_repo_url(repo_url: str) -> tuple[str, str]:
    """Extract owner and repo name from GitHub URL or owner/repo string."""
    if not repo_url or not isinstance(repo_url, str):
        raise ValueError("Invalid GitHub URL provided.")

    trimmed = repo_url.strip().rstrip("/")
    parsed = urlparse(trimmed)

    if parsed.netloc:
        host = parsed.netloc.lower()
        if host not in {"github.com", "www.github.com"}:
            raise ValueError("Invalid GitHub URL host.")
        path = parsed.path
    else:
        path = trimmed

    parts = [segment for segment in path.split("/") if segment and segment.lower() not in {
        "tree", "blob", "pulls", "issues", "commit", "releases"
    }]

    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL. Use https://github.com/owner/repo or owner/repo")

    owner = parts[0]
    repo = parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo
