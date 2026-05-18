"""Core data models and GitHub API client for ARA."""

import json
import os
import time
import urllib.request
import urllib.error


# ─── Data Models ────────────────────────────────────────────────────────────

class Repo:
    """Represents a GitHub repository with star tracking data."""

    def __init__(self, full_name: str, stars: int = 0, description: str = ""):
        self.full_name = full_name  # e.g. "owner/repo"
        self.stars = stars
        self.description = description
        self.previous_stars = 0
        self.baseline_stars = 0
        self.last_checked = 0.0

    @property
    def delta(self) -> int:
        return self.stars - self.previous_stars

    @property
    def total_growth(self) -> int:
        return self.stars - self.baseline_stars

    def update(self, stars: int):
        self.previous_stars = self.stars
        self.stars = stars
        self.last_checked = time.time()

    def display_name(self, max_len: int = 20) -> str:
        name = self.full_name
        return name if len(name) <= max_len else name[:max_len - 3] + "..."

    def __repr__(self) -> str:
        return f"Repo({self.full_name}, ★{self.stars})"


class StarSnapshot:
    """A point-in-time snapshot of star counts for multiple repos."""

    def __init__(self, repos: list[Repo], timestamp: float | None = None):
        self.repos = repos
        self.timestamp = timestamp or time.time()

    def sorted_by_stars(self) -> list[Repo]:
        return sorted(self.repos, key=lambda r: r.stars, reverse=True)

    def leaderboard(self) -> list[tuple[int, Repo]]:
        """Return list of (rank, repo) tuples, 1-indexed."""
        return list(enumerate(self.sorted_by_stars(), start=1))


# ─── GitHub API Client ─────────────────────────────────────────────────────

class GitHubClient:
    """Minimal GitHub API client for fetching repository star counts."""

    API_BASE = "https://api.github.com"

    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self._cache: dict[str, tuple[int, float]] = {}  # repo -> (stars, timestamp)
        self.cache_ttl = 60  # seconds
        self.rate_limit_remaining = -1
        self.rate_limit_reset = 0

    def _get_headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ARA-CLI/0.1.0",
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def _is_cache_valid(self, repo_name: str) -> bool:
        if repo_name not in self._cache:
            return False
        _, cached_at = self._cache[repo_name]
        return (time.time() - cached_at) < self.cache_ttl

    def get_stars(self, repo_name: str) -> int | None:
        """Fetch star count for a repo. Returns None on error."""
        # Check cache first
        if self._is_cache_valid(repo_name):
            return self._cache[repo_name][0]

        url = f"{self.API_BASE}/repos/{repo_name}"
        req = urllib.request.Request(url, headers=self._get_headers())

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                stars = data.get("stargazers_count", 0)
                desc = data.get("description", "")

                # Parse rate limit headers
                self.rate_limit_remaining = int(
                    resp.headers.get("X-RateLimit-Remaining", -1)
                )
                self.rate_limit_reset = int(
                    resp.headers.get("X-RateLimit-Reset", 0)
                )

                # Cache it
                self._cache[repo_name] = (stars, time.time())
                return stars

        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"  ⚠  Repo '{repo_name}' not found (404)")
            elif e.code == 403:
                print(f"  ⚠  Rate limited! Reset at {self._reset_time_str()}")
            else:
                print(f"  ⚠  HTTP {e.code} for '{repo_name}'")
            return None
        except urllib.error.URLError as e:
            print(f"  ⚠  Network error for '{repo_name}': {e.reason}")
            return None
        except Exception as e:
            print(f"  ⚠  Unexpected error for '{repo_name}': {e}")
            return None

    def get_repo_info(self, repo_name: str) -> dict | None:
        """Fetch full repo info. Returns dict with stars, description, etc."""
        url = f"{self.API_BASE}/repos/{repo_name}"
        req = urllib.request.Request(url, headers=self._get_headers())

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                self.rate_limit_remaining = int(
                    resp.headers.get("X-RateLimit-Remaining", -1)
                )
                self.rate_limit_reset = int(
                    resp.headers.get("X-RateLimit-Reset", 0)
                )
                return {
                    "stars": data.get("stargazers_count", 0),
                    "description": data.get("description", ""),
                    "language": data.get("language", ""),
                    "forks": data.get("forks_count", 0),
                    "open_issues": data.get("open_issues_count", 0),
                    "full_name": data.get("full_name", repo_name),
                }
        except urllib.error.HTTPError:
            return None

    def invalidate_cache(self, repo_name: str | None = None):
        """Clear cache for a specific repo or all repos."""
        if repo_name:
            self._cache.pop(repo_name, None)
        else:
            self._cache.clear()

    def _reset_time_str(self) -> str:
        if self.rate_limit_reset:
            return time.strftime(
                "%H:%M:%S", time.localtime(self.rate_limit_reset)
            )
        return "unknown"

    def rate_limit_status(self) -> str:
        if self.rate_limit_remaining >= 0:
            return f"API calls remaining: {self.rate_limit_remaining}"
        return "API calls: unknown (no token? 60/hr limit)"
