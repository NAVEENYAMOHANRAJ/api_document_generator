"""
Repository Service - Clone and analyze repositories dynamically

Handles:
- Repository cloning from URL or local path
- Framework detection
- Dynamic analysis
- Cleanup
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)


class RepositoryService:
    """Service for handling repository operations"""

    def __init__(self, temp_dir: Optional[str] = None):
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.cloned_repos: dict = {}

    def get_or_clone_repository(self, source: str) -> Tuple[str, str]:
        """
        Get repository path - clone if URL, use if local path.
        
        Args:
            source: Git URL or local path
            
        Returns:
            Tuple of (repo_path, repo_type)
        """
        
        # Check if it's a URL
        if self._is_url(source):
            return self._clone_repository(source)
        
        # Check if it's a local path
        if Path(source).exists():
            return source, "local"
        
        raise ValueError(f"Invalid source: {source}")

    def _is_url(self, source: str) -> bool:
        """Check if source is a URL"""
        try:
            result = urlparse(source)
            return result.scheme in ('http', 'https', 'git', 'ssh')
        except:
            return False

    def _clone_repository(self, url: str) -> Tuple[str, str]:
        """Clone repository from URL"""
        
        # Generate unique directory name
        repo_name = url.split('/')[-1].replace('.git', '')
        clone_path = Path(self.temp_dir) / f"repo_{repo_name}_{id(url)}"
        
        try:
            logger.info(f"Cloning repository from {url}")
            
            # Clone repository
            subprocess.run(
                ['git', 'clone', '--depth', '1', url, str(clone_path)],
                check=True,
                capture_output=True,
                timeout=300
            )
            
            logger.info(f"Repository cloned to {clone_path}")
            self.cloned_repos[str(clone_path)] = url
            
            return str(clone_path), "cloned"
        
        except subprocess.TimeoutExpired:
            raise Exception(f"Repository clone timed out: {url}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to clone repository: {e.stderr.decode()}")
        except Exception as e:
            raise Exception(f"Error cloning repository: {str(e)}")

    def cleanup_repository(self, repo_path: str) -> None:
        """Clean up cloned repository"""
        
        try:
            if repo_path in self.cloned_repos:
                if Path(repo_path).exists():
                    shutil.rmtree(repo_path)
                    logger.info(f"Cleaned up repository: {repo_path}")
                    del self.cloned_repos[repo_path]
        except Exception as e:
            logger.error(f"Error cleaning up repository: {e}")

    def cleanup_all(self) -> None:
        """Clean up all cloned repositories"""
        for repo_path in list(self.cloned_repos.keys()):
            self.cleanup_repository(repo_path)

    def get_repository_info(self, repo_path: str) -> dict:
        """Get repository information"""
        
        repo_path_obj = Path(repo_path)
        
        return {
            "path": repo_path,
            "name": repo_path_obj.name,
            "exists": repo_path_obj.exists(),
            "is_git": (repo_path_obj / ".git").exists(),
            "size_mb": self._get_directory_size(repo_path) / (1024 * 1024),
            "file_count": len(list(repo_path_obj.rglob("*"))),
            "is_cloned": repo_path in self.cloned_repos
        }

    def _get_directory_size(self, path: str) -> int:
        """Get directory size in bytes"""
        total = 0
        try:
            for entry in Path(path).rglob("*"):
                if entry.is_file():
                    total += entry.stat().st_size
        except:
            pass
        return total

    def get_git_info(self, repo_path: str) -> Optional[dict]:
        """Get Git repository information"""
        
        try:
            git_dir = Path(repo_path) / ".git"
            if not git_dir.exists():
                return None
            
            # Get current branch
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            branch = result.stdout.strip() if result.returncode == 0 else "unknown"
            
            # Get latest commit
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%H %s'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            commit_info = result.stdout.strip() if result.returncode == 0 else "unknown"
            
            # Get remote URL
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            remote_url = result.stdout.strip() if result.returncode == 0 else "unknown"
            
            return {
                "branch": branch,
                "commit": commit_info,
                "remote_url": remote_url
            }
        
        except Exception as e:
            logger.error(f"Error getting Git info: {e}")
            return None

    def validate_repository(self, repo_path: str) -> Tuple[bool, str]:
        """Validate repository structure"""
        
        repo_path_obj = Path(repo_path)
        
        if not repo_path_obj.exists():
            return False, "Repository path does not exist"
        
        if not repo_path_obj.is_dir():
            return False, "Repository path is not a directory"
        
        # Check for common framework indicators
        has_framework = False
        framework_type = "unknown"
        
        if (repo_path_obj / "artisan").exists():
            has_framework = True
            framework_type = "Laravel"
        elif (repo_path_obj / "manage.py").exists():
            has_framework = True
            framework_type = "Django"
        elif (repo_path_obj / "package.json").exists():
            has_framework = True
            framework_type = "Node.js"
        elif (repo_path_obj / "pom.xml").exists():
            has_framework = True
            framework_type = "Spring Boot"
        
        if not has_framework:
            return False, "No recognized framework found"
        
        return True, framework_type
