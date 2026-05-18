"""Core data model for ARA - Arena Star Tracker.

Provides:
- star_cache: In-memory cache for star counts (60s TTL)
- GitHubClient: Fetches star counts from GitHub API
"""

import time
import json
import os
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# In-memory cache
# ---------------------------------------------------------------------------

star_cache: dict = {}
"""Cache dict: repo_name -> {"count": int, "timestamp": float}.
60-second TTL enforced on reads. Populated by GitHubClient."""

CACHE_TTL = 60  # seconds


def get_cached_stars(repo: str) -> int | None:
    """Return cached star count if still fresh, else None."""
    entry = star_cache.get(repo)
    if entry is None:
        return None
    if time.time() - entry["timestamp"] > CACHE_TTL:
        del star_cache[repo]
        return None
    return entry["count"]


def set_cached_stars(repo: str, count: int) -> None:
    """Store a star count in the cache."""
    star_cache[repo] = {"count": count, "timestamp": time.time()}


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

class Repo:
    """Simple repo representation."""

    def __init__(self, full_name: str):
        self.full_name = full_name
        self.stars: int = 0

    def __repr__(self) -> str:
        return f"Repo({self.full_name}, ★ {self.stars})"


class StarSnapshot:
    """A snapshot of a repo's star count at a point in time."""

    def __init__(self, repo: str, stars: int, timestamp: float | None = None):
        self.repo = repo
        self.stars = stars
        self.timestamp = timestamp or time.time()

    def delta(self, other: "StarSnapshot") -> int:
        """Star difference from another snapshot."""
        return self.stars - other.stars

    def __repr__(self) -> str:
        return f"StarSnapshot({self.repo}, ★ {self.stars} @ {self.timestamp})"


# ---------------------------------------------------------------------------
# GitHub API Client
# ---------------------------------------------------------------------------

GITHUB_API = "https://api.github.com/repos"


class GitHubClient:
    """Client for fetching GitHub star counts."""

    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")

    def _make_request(self, url: str) -> dict:
        """Make a GET request to the GitHub API."""
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github.v3+json")
        req.add_header("User-Agent", "ARA-CLI/0.1.0")
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ValueError(f"Repository not found: {url.rsplit('/', 2)[-2]}/{url.rsplit('/', 1)[-1]}")
            elif e.code == 403:
                raise RuntimeError("GitHub API rate limit exceeded. Set GITHUB_TOKEN for higher limits.")
            else:
                raise RuntimeError(f"GitHub API error {e.code}: {e.reason}")

    def get_stars(self, repo: str) -> int:
        """Fetch star count for a repo (owner/name format)."""
        # Check cache first
        cached = get_cached_stars(repo)
        if cached is not None:
            return cached

        url = f"{GITHUB_API}/{repo}"
        data = self._make_request(url)
        stars = data.get("stargazers_count", 0)
        set_cached_stars(repo, stars)
        return stars
