"""Tests for `ara rank` command (Task 009-B Part 2)."""

import json
from unittest.mock import MagicMock, patch

import pytest

# Sample repo info dicts for testing
REPO_A = {
    "full_name": "facebook/react",
    "stars": 226000,
    "forks": 47000,
    "open_issues": 1200,
    "language": "JavaScript",
    "license": {"key": "mit", "name": "MIT License"},
    "description": "A declarative UI library",
}

REPO_B = {
    "full_name": "vuejs/core",
    "stars": 47000,
    "forks": 7000,
    "open_issues": 800,
    "language": "TypeScript",
    "license": {"key": "mit", "name": "MIT License"},
    "description": "Vue.js core",
}

REPO_C = {
    "full_name": "vercel/next.js",
    "stars": 126000,
    "forks": 27000,
    "open_issues": 3000,
    "language": "JavaScript",
    "license": {"key": "mit", "name": "MIT License"},
    "description": "Next.js framework",
}


# ===========================================================================
# _format_stars tests
# ===========================================================================


def test_format_stars_large():
    """_format_stars should format large numbers with commas."""
    from ara.rank import _format_stars

    result = _format_stars(226000)
    assert result == "226,000"


def test_format_stars_medium():
    """_format_stars should format medium numbers normally."""
    from ara.rank import _format_stars

    result = _format_stars(47000)
    assert result == "47,000"


def test_format_stars_small():
    """_format_stars should not add commas for small numbers."""
    from ara.rank import _format_stars

    result = _format_stars(999)
    assert result == "999"


# ===========================================================================
# _format_forks tests
# ===========================================================================


def test_format_forks_thousands():
    """_format_forks should show 'k' suffix for 1000+."""
    from ara.rank import _format_forks

    result = _format_forks(47000)
    assert result == "47k"


def test_format_forks_small():
    """_format_forks should not show 'k' suffix for < 1000."""
    from ara.rank import _format_forks

    result = _format_forks(500)
    assert result == "500"


# ===========================================================================
# cmd_rank tests
# ===========================================================================


@patch("ara.rank.GitHubClient")
def test_cmd_rank_basic(MockClient, capsys):
    """cmd_rank should print ranking table with sorted repos."""
    from ara.rank import cmd_rank

    mock_client = MockClient.return_value
    infos = [REPO_A, REPO_B, REPO_C]

    def mock_get_repo_info(repo):
        mapping = {
            "facebook/react": REPO_A,
            "vuejs/core": REPO_B,
            "vercel/next.js": REPO_C,
        }
        return mapping.get(repo, {})

    mock_client.get_repo_info.side_effect = mock_get_repo_info

    args = type("Args", (), {"repos": ["facebook/react", "vuejs/core", "vercel/next.js"], "top": 3, "json": False})()
    cmd_rank(args, mock_client)

    captured = capsys.readouterr()
    # Should show sorted: react (226k), next.js (126k), vuejs (47k)
    assert "facebook/react" in captured.out
    assert "226,000" in captured.out
    assert "next.js" in captured.out
    assert "126,000" in captured.out
    assert "vuejs/core" in captured.out
    assert "47,000" in captured.out


@patch("ara.rank.GitHubClient")
def test_cmd_rank_respects_top_n(MockClient, capsys):
    """cmd_rank should limit results to --top N."""
    from ara.rank import cmd_rank

    mock_client = MockClient.return_value
    infos = [REPO_A, REPO_B, REPO_C]

    def mock_get_repo_info(repo):
        mapping = {
            "facebook/react": REPO_A,
            "vuejs/core": REPO_B,
            "vercel/next.js": REPO_C,
        }
        return mapping.get(repo, {})

    mock_client.get_repo_info.side_effect = mock_get_repo_info

    args = type("Args", (), {"repos": ["facebook/react", "vuejs/core", "vercel/next.js"], "top": 2, "json": False})()
    cmd_rank(args, mock_client)

    captured = capsys.readouterr()
    assert "226,000" in captured.out  # #1
    assert "126,000" in captured.out  # #2
    assert "47,000" not in captured.out  # #3 should not appear


@patch("ara.rank.GitHubClient")
def test_cmd_rank_graceful_error(MockClient, capsys):
    """cmd_rank should skip failed repos and show errors."""
    from ara.rank import cmd_rank

    mock_client = MockClient.return_value

    def mock_get_repo_info(repo):
        if repo == "facebook/react":
            return REPO_A
        raise ValueError("Repository not found")

    mock_client.get_repo_info.side_effect = mock_get_repo_info

    args = type("Args", (), {"repos": ["facebook/react", "nonexistent/repo"], "top": 10, "json": False})()
    cmd_rank(args, mock_client)

    captured = capsys.readouterr()
    assert "facebook/react" in captured.out
    assert "226,000" in captured.out
    # Error should be displayed
    assert "Error" in captured.out or "errors" in captured.out.lower()


@patch("ara.rank.GitHubClient")
def test_cmd_rank_default_repos(MockClient, capsys):
    """cmd_rank should use DEFAULT_REPOS when no repos given."""
    from ara.rank import cmd_rank, DEFAULT_REPOS

    mock_client = MockClient.return_value

    def mock_get_repo_info(repo):
        # Return minimal info for default repos
        return {
            "full_name": repo,
            "stars": 10000,
            "forks": 2000,
            "open_issues": 500,
            "language": "JavaScript",
            "license": "MIT",
        }

    mock_client.get_repo_info.side_effect = mock_get_repo_info

    args = type("Args", (), {"repos": None, "top": 5, "json": False})()
    cmd_rank(args, mock_client)

    captured = capsys.readouterr()
    # Should see at least some default repos
    assert "facebook/react" in captured.out
    assert "vuejs/core" in captured.out


# ===========================================================================
# cmd_rank_json tests
# ===========================================================================


@patch("ara.rank.GitHubClient")
def test_cmd_rank_json_output(MockClient, capsys):
    """cmd_rank_json should print valid JSON with sorted ranking."""
    from ara.rank import cmd_rank_json

    mock_client = MockClient.return_value

    def mock_get_repo_info(repo):
        mapping = {
            "facebook/react": REPO_A,
            "vuejs/core": REPO_B,
            "vercel/next.js": REPO_C,
        }
        return mapping.get(repo, {})

    mock_client.get_repo_info.side_effect = mock_get_repo_info

    args = type("Args", (), {"repos": ["facebook/react", "vuejs/core", "vercel/next.js"], "top": 3})()
    cmd_rank_json(args, mock_client)

    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert data["command"] == "rank"
    assert data["top"] == 3
    assert len(data["repos"]) == 3
    assert data["repos"][0]["full_name"] == "facebook/react"
    assert data["repos"][0]["rank"] == 1
    assert data["repos"][1]["full_name"] == "vercel/next.js"
    assert data["repos"][2]["full_name"] == "vuejs/core"


@patch("ara.rank.GitHubClient")
def test_cmd_rank_json_error(MockClient, capsys):
    """cmd_rank_json should include errors for failed repos."""
    from ara.rank import cmd_rank_json

    mock_client = MockClient.return_value

    def mock_get_repo_info(repo):
        if repo == "good/repo":
            return {"full_name": "good/repo", "stars": 500, "forks": 100, "open_issues": 10, "language": "Python"}
        raise RuntimeError("Network error")

    mock_client.get_repo_info.side_effect = mock_get_repo_info

    args = type("Args", (), {"repos": ["good/repo", "bad/repo"], "top": 10})()
    cmd_rank_json(args, mock_client)

    captured = capsys.readouterr()
    data = json.loads(captured.out)

    assert len(data["repos"]) == 1  # Only one successful
    assert data["repos"][0]["full_name"] == "good/repo"
    assert data["errors"] is not None
    assert len(data["errors"]) == 1


# ===========================================================================
# CLI integration tests
# ===========================================================================


def test_parser_rank_command():
    """Parser should parse 'rank' subcommand with --top."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["rank", "--top", "5"])
    assert args.command == "rank"
    assert args.top == 5
    assert args.json is False


def test_parser_rank_json_flag():
    """Parser should accept --json with rank command."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["rank", "--top", "3", "--json"])
    assert args.json is True
    assert args.top == 3


def test_parser_rank_default_top():
    """Parser should default --top to 10."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["rank"])
    assert args.top == 10


@patch("ara.cli.GitHubClient")
def test_main_rank_command(MockClient, capsys):
    """main() should dispatch rank command successfully."""
    from ara.cli import main

    mock_instance = MagicMock()
    MockClient.return_value = mock_instance

    def mock_get_repo_info(repo):
        mapping = {
            "facebook/react": REPO_A,
            "vuejs/core": REPO_B,
        }
        return mapping.get(repo, {"full_name": repo, "stars": 0, "forks": 0})

    mock_instance.get_repo_info.side_effect = mock_get_repo_info

    result = main(["rank", "--top", "2"])
    assert result == 0

    captured = capsys.readouterr()
    assert "facebook/react" in captured.out
    assert "226,000" in captured.out


@patch("ara.cli.GitHubClient")
def test_main_rank_json(MockClient, capsys):
    """main() should dispatch rank --json via json_handlers."""
    from ara.cli import main

    mock_instance = MagicMock()
    MockClient.return_value = mock_instance

    def mock_get_repo_info(repo):
        mapping = {"facebook/react": REPO_A}
        return mapping.get(repo, {"full_name": repo, "stars": 0, "forks": 0})

    mock_instance.get_repo_info.side_effect = mock_get_repo_info

    result = main(["rank", "--json", "--top", "1"])
    assert result == 0

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["command"] == "rank"
    assert data["top"] == 1
