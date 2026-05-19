"""Core data model for ARA - Arena Star Tracker.

Provides:
- star_cache: In-memory cache for star counts (60s TTL)
- GitHubClient: Fetches star counts from GitHub API
"""

import time
import json
import os
import random
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0  # seconds, doubles each attempt

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


def _retryable_http_error(exc: urllib.error.HTTPError) -> bool:
    """Return True if the HTTP error is worth retrying (server-side)."""
    return exc.code in (429, 500, 502, 503, 504)


def _raise_api_error(exc: urllib.error.HTTPError, url: str) -> None:
    """Map HTTP errors to appropriate ARA exceptions."""
    if exc.code == 404:
        raise ValueError(
            f"Repository not found: "
            f"{url.rsplit('/', 2)[-2]}/{url.rsplit('/', 1)[-1]}"
        )
    elif exc.code == 403:
        raise RuntimeError(
            "GitHub API rate limit exceeded. "
            "Set GITHUB_TOKEN for higher limits."
        )
    raise RuntimeError(f"GitHub API error {exc.code}: {exc.reason}")


def _retry_delay(attempt: int, base: float = DEFAULT_RETRY_DELAY) -> float:
    """Exponential backoff with jitter: base * 2^attempt + random(0, 0.5)."""
    return base * (2 ** attempt) + random.uniform(0, 0.5)


class GitHubClient:
    """Client for fetching GitHub star counts."""

    def __init__(
        self,
        token: str | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
    ):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _request(self, url: str) -> tuple[any, dict]:
        """Core request method — returns (parsed_json, headers_dict).

        Handles retries, auth, and common error mapping for all callers.
        """
        last_exc: Exception | None = None

        for attempt in range(self.max_retries + 1):
            req = urllib.request.Request(url)
            req.add_header("Accept", "application/vnd.github.v3+json")
            req.add_header("User-Agent", "ARA-CLI/0.1.0")
            if self.token:
                req.add_header("Authorization", f"Bearer {self.token}")

            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    return data, dict(resp.headers)
            except urllib.error.HTTPError as e:
                if _retryable_http_error(e) and attempt < self.max_retries:
                    last_exc = e
                    delay = _retry_delay(attempt, self.retry_delay)
                    time.sleep(delay)
                    continue
                _raise_api_error(e, url)
            except urllib.error.URLError as e:
                if attempt < self.max_retries:
                    last_exc = e
                    delay = _retry_delay(attempt, self.retry_delay)
                    time.sleep(delay)
                    continue
                raise RuntimeError(
                    f"Network error after {self.max_retries} retries: {e.reason}"
                )

        raise RuntimeError(
            f"GitHub API error {last_exc.code}: {last_exc.reason}"
        )

    def _make_request_raw(self, url: str) -> any:
        """Make a GET request and return raw parsed JSON (dict or list).

        Used for endpoints that return arrays (e.g. stargazers).
        """
        data, _ = self._request(url)
        return data

    def _fetch_page_with_headers(self, url: str) -> tuple[any, dict]:
        """Fetch a URL and return (parsed_json, headers_dict) with retry support.

        Used for paginated endpoints (e.g. stargazers) where the Link
        header is needed to discover the next page URL.
        """
        return self._request(url)

    def _make_request(self, url: str) -> dict:
        """Make a GET request to the GitHub API with automatic retry.

        Retries on 429 (rate-limit), 500, 502, 503, 504 with exponential
        backoff + jitter. Non-retryable errors (404, 403, etc.) are raised
        immediately.
        """
        last_exc: Exception | None = None

        for attempt in range(self.max_retries + 1):
            req = urllib.request.Request(url)
            req.add_header("Accept", "application/vnd.github.v3+json")
            req.add_header("User-Agent", "ARA-CLI/0.1.0")
            if self.token:
                req.add_header("Authorization", f"Bearer {self.token}")

            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if _retryable_http_error(e) and attempt < self.max_retries:
                    last_exc = e
                    delay = _retry_delay(attempt, self.retry_delay)
                    time.sleep(delay)
                    continue
                if e.code == 404:
                    raise ValueError(
                        f"Repository not found: "
                        f"{url.rsplit('/', 2)[-2]}/{url.rsplit('/', 1)[-1]}"
                    )
                elif e.code == 403:
                    raise RuntimeError(
                        "GitHub API rate limit exceeded. "
                        "Set GITHUB_TOKEN for higher limits."
                    )
                raise RuntimeError(f"GitHub API error {e.code}: {e.reason}")
            except urllib.error.URLError as e:
                # Transient network errors are retryable
                if attempt < self.max_retries:
                    last_exc = e
                    delay = _retry_delay(attempt, self.retry_delay)
                    time.sleep(delay)
                    continue
                raise RuntimeError(f"Network error after {self.max_retries} retries: {e.reason}")

        # If we exhaust retries, raise the last HTTP error we saw
        raise RuntimeError(
            f"GitHub API error {last_exc.code}: {last_exc.reason}"  # type: ignore[union-attr]
        )

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

    def get_multiple_repos_info(self, repos: list[str]) -> list[dict]:
        """Batch-fetch info for multiple repos.

        Fetches each repo sequentially (synchronous), checking cache first.
        Returns a list of info dicts in input order.
        If a single repo fails, its dict contains {"error": "..."}
        and fetching continues for remaining repos.
        """
        results: list[dict] = []
        for repo in repos:
            try:
                info = self.get_repo_info(repo)
                results.append(info)
            except (ValueError, RuntimeError) as e:
                results.append({"error": str(e), "full_name": repo})
        return results

    def get_repo_info(self, repo: str) -> dict:
        """Fetch full repository information from GitHub API.

        Returns a dict with keys:
            name, full_name, description, stars, forks, open_issues,
            language, topics, license, created_at, updated_at, pushed_at,
            html_url

        Raises ValueError on 404, RuntimeError on API errors.
        """
        url = f"{GITHUB_API}/{repo}"
        data = self._make_request(url)
        return {
            "name": data.get("name", ""),
            "full_name": data.get("full_name", repo),
            "description": data.get("description") or "",
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "open_issues": data.get("open_issues_count", 0),
            "language": data.get("language"),
            "topics": data.get("topics", []),
            "license": data.get("license", {}).get("spdx_id") if data.get("license") else None,
            "created_at": data.get("created_at", ""),
            "updated_at": data.get("updated_at", ""),
            "pushed_at": data.get("pushed_at", ""),
            "html_url": data.get("html_url", f"https://github.com/{repo}"),
        }
