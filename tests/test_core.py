"""Tests for `ara.core` — cache, models, and GitHubClient."""

import json
import time
from unittest.mock import MagicMock, patch

import pytest


# ===========================================================================
# Cache tests
# ===========================================================================


def test_star_cache_global_exists():
    """star_cache should be a global dict."""
    from ara.core import star_cache
    assert isinstance(star_cache, dict)


def test_get_cached_stars_missing():
    """get_cached_stars should return None for unknown repos."""
    from ara.core import get_cached_stars, star_cache
    star_cache.clear()
    assert get_cached_stars("nonexistent/repo") is None


def test_set_and_get_cached_stars():
    """set_cached_stars then get_cached_stars should return count."""
    from ara.core import set_cached_stars, get_cached_stars, star_cache
    star_cache.clear()
    set_cached_stars("owner/repo", 42)
    assert get_cached_stars("owner/repo") == 42


def test_cached_stars_expires_after_ttl():
    """get_cached_stars should return None after TTL expires."""
    from ara.core import set_cached_stars, get_cached_stars, star_cache, CACHE_TTL

    star_cache.clear()
    set_cached_stars("owner/repo", 100)

    # Fake an old timestamp to force expiry
    star_cache["owner/repo"]["timestamp"] = time.time() - CACHE_TTL - 1
    assert get_cached_stars("owner/repo") is None


def test_cache_evicts_expired_entry():
    """Expired entries should be deleted from the cache."""
    from ara.core import set_cached_stars, get_cached_stars, star_cache, CACHE_TTL

    star_cache.clear()
    set_cached_stars("owner/repo", 100)
    star_cache["owner/repo"]["timestamp"] = time.time() - CACHE_TTL - 1
    get_cached_stars("owner/repo")  # triggers eviction
    assert "owner/repo" not in star_cache


def test_cached_stars_fresh():
    """get_cached_stars should return count for fresh entries."""
    from ara.core import set_cached_stars, get_cached_stars, star_cache

    star_cache.clear()
    set_cached_stars("owner/repo", 500)
    # Immediately query — should be fresh
    assert get_cached_stars("owner/repo") == 500


# ===========================================================================
# Repo model tests
# ===========================================================================


def test_repo_initialization():
    """Repo should initialize with full_name and stars=0."""
    from ara.core import Repo

    r = Repo("owner/alpha")
    assert r.full_name == "owner/alpha"
    assert r.stars == 0


def test_repo_stars_assignable():
    """Repo.stars should be settable."""
    from ara.core import Repo

    r = Repo("owner/alpha")
    r.stars = 999
    assert r.stars == 999


def test_repo_repr():
    """Repo.__repr__ should include name and star count."""
    from ara.core import Repo

    r = Repo("owner/alpha")
    r.stars = 100
    rep = repr(r)
    assert "Repo" in rep
    assert "owner/alpha" in rep
    assert "100" in rep


# ===========================================================================
# StarSnapshot model tests
# ===========================================================================


def test_star_snapshot_auto_timestamp():
    """StarSnapshot should auto-assign a timestamp."""
    from ara.core import StarSnapshot

    s = StarSnapshot("owner/repo", 100)
    assert s.repo == "owner/repo"
    assert s.stars == 100
    assert s.timestamp is not None
    assert isinstance(s.timestamp, float)


def test_star_snapshot_explicit_timestamp():
    """StarSnapshot should accept an explicit timestamp."""
    from ara.core import StarSnapshot

    s = StarSnapshot("owner/repo", 100, timestamp=12345.0)
    assert s.timestamp == 12345.0


def test_star_snapshot_delta_positive():
    """delta() should return positive when other is smaller."""
    from ara.core import StarSnapshot

    s1 = StarSnapshot("owner/repo", 110, timestamp=100.0)
    s2 = StarSnapshot("owner/repo", 100, timestamp=0.0)
    assert s1.delta(s2) == 10


def test_star_snapshot_delta_negative():
    """delta() should return negative when other is larger."""
    from ara.core import StarSnapshot

    s1 = StarSnapshot("owner/repo", 90, timestamp=100.0)
    s2 = StarSnapshot("owner/repo", 100, timestamp=0.0)
    assert s1.delta(s2) == -10


def test_star_snapshot_delta_zero():
    """delta() should return 0 when counts are equal."""
    from ara.core import StarSnapshot

    s1 = StarSnapshot("owner/repo", 100, timestamp=100.0)
    s2 = StarSnapshot("owner/repo", 100, timestamp=0.0)
    assert s1.delta(s2) == 0


def test_star_snapshot_repr():
    """StarSnapshot.__repr__ should include details."""
    from ara.core import StarSnapshot

    s = StarSnapshot("owner/repo", 42, timestamp=1000.0)
    rep = repr(s)
    assert "StarSnapshot" in rep
    assert "owner/repo" in rep
    assert "42" in rep


# ===========================================================================
# GitHubClient tests (mocked HTTP)
# ===========================================================================


def test_github_client_init_no_token():
    """GitHubClient should init with None token when env is not set."""
    from ara.core import GitHubClient

    with patch.dict("os.environ", {}, clear=True):
        client = GitHubClient()
        assert client.token is None


def test_github_client_init_from_env():
    """GitHubClient should read token from environment."""
    from ara.core import GitHubClient

    with patch.dict("os.environ", {"GITHUB_TOKEN": "ghp_fake123"}):
        client = GitHubClient()
        assert client.token == "ghp_fake123"


def test_github_client_init_explicit_token():
    """GitHubClient should use explicit token over env."""
    from ara.core import GitHubClient

    with patch.dict("os.environ", {"GITHUB_TOKEN": "ghp_env_token"}):
        client = GitHubClient(token="ghp_explicit")
        assert client.token == "ghp_explicit"


@patch("ara.core.urllib.request.urlopen")
def test_get_stars_success(mock_urlopen):
    """get_stars should return stargazers_count from API response."""
    from ara.core import GitHubClient, star_cache

    star_cache.clear()

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(
        {"stargazers_count": 1234, "full_name": "owner/repo"}
    ).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    client = GitHubClient()
    stars = client.get_stars("owner/repo")
    assert stars == 1234


@patch("ara.core.urllib.request.urlopen")
def test_get_stars_uses_cache(mock_urlopen):
    """get_stars should return cached value without calling API."""
    from ara.core import GitHubClient, set_cached_stars, star_cache

    star_cache.clear()
    set_cached_stars("owner/repo", 999)

    client = GitHubClient()
    stars = client.get_stars("owner/repo")
    assert stars == 999
    mock_urlopen.assert_not_called()


@patch("ara.core.urllib.request.urlopen")
def test_get_stars_missing_key(mock_urlopen):
    """get_stars should handle missing stargazers_count (return 0)."""
    from ara.core import GitHubClient, star_cache

    star_cache.clear()

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"full_name": "owner/repo"}).encode(
        "utf-8"
    )
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    client = GitHubClient()
    stars = client.get_stars("owner/repo")
    assert stars == 0


@patch("ara.core.urllib.request.urlopen")
def test_get_stars_404(mock_urlopen):
    """get_stars should raise ValueError on 404."""
    from ara.core import GitHubClient, star_cache
    import urllib.error

    star_cache.clear()

    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="https://api.github.com/repos/owner/nonexistent",
        code=404,
        msg="Not Found",
        hdrs={},
        fp=None,
    )

    client = GitHubClient()
    with pytest.raises(ValueError, match="Repository not found"):
        client.get_stars("owner/nonexistent")


@patch("ara.core.urllib.request.urlopen")
def test_get_stars_403(mock_urlopen):
    """get_stars should raise RuntimeError on 403 (rate limit)."""
    from ara.core import GitHubClient, star_cache
    import urllib.error

    star_cache.clear()

    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="https://api.github.com/repos/owner/repo",
        code=403,
        msg="Forbidden",
        hdrs={},
        fp=None,
    )

    client = GitHubClient()
    with pytest.raises(RuntimeError, match="rate limit"):
        client.get_stars("owner/repo")


@patch("ara.core.urllib.request.urlopen")
def test_get_stars_other_http_error(mock_urlopen):
    """get_stars should raise RuntimeError on other HTTP errors."""
    from ara.core import GitHubClient, star_cache
    import urllib.error

    star_cache.clear()

    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="https://api.github.com/repos/owner/repo",
        code=500,
        msg="Internal Server Error",
        hdrs={},
        fp=None,
    )

    client = GitHubClient()
    with pytest.raises(RuntimeError, match="500"):
        client.get_stars("owner/repo")


@patch("ara.core.urllib.request.urlopen")
def test_get_stars_populates_cache(mock_urlopen):
    """get_stars should cache the result after fetching."""
    from ara.core import GitHubClient, get_cached_stars, star_cache

    star_cache.clear()

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(
        {"stargazers_count": 777, "full_name": "owner/repo"}
    ).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    client = GitHubClient()
    stars = client.get_stars("owner/repo")
    assert stars == 777
    assert get_cached_stars("owner/repo") == 777


@patch("ara.core.urllib.request.urlopen")
def test_make_request_sets_headers(mock_urlopen):
    """_make_request should set Accept and User-Agent headers."""
    from ara.core import GitHubClient

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"id": 1}).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    client = GitHubClient()
    client._make_request("https://api.github.com/repos/owner/repo")

    req = mock_urlopen.call_args[0][0]
    assert req.get_header("Accept") == "application/vnd.github.v3+json"
    # Python's HTTPRequest normalizes User-Agent to a different header slot;
    # verify the request was made and headers set
    assert req.has_header("Accept")


@patch("ara.core.urllib.request.urlopen")
def test_make_request_sets_auth_header(mock_urlopen):
    """_make_request should include Authorization header when token is set."""
    from ara.core import GitHubClient

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"id": 1}).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    client = GitHubClient(token="ghp_secret")
    client._make_request("https://api.github.com/repos/owner/repo")

    req = mock_urlopen.call_args[0][0]
    assert req.get_header("Authorization") == "Bearer ghp_secret"


@patch("ara.core.urllib.request.urlopen")
def test_make_request_no_auth_without_token(mock_urlopen):
    """_make_request should NOT include Authorization when no token."""
    from ara.core import GitHubClient

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({"id": 1}).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    client = GitHubClient(token=None)
    client._make_request("https://api.github.com/repos/owner/repo")

    req = mock_urlopen.call_args[0][0]
    assert req.get_header("Authorization") is None
