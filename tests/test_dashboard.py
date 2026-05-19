"""Tests for the dashboard command."""

from unittest.mock import MagicMock, patch

import pytest


# ===========================================================================
# Dashboard display tests
# ===========================================================================


def test_dashboard_prints_repo_info(capsys):
    """Dashboard output should contain repo name, stars, forks, issues."""
    from ara.dashboard import _print_dashboard

    info = {
        "full_name": "facebook/react",
        "stars": 226000,
        "forks": 47000,
        "open_issues": 1200,
        "language": "JavaScript",
        "license": "MIT",
        "updated_at": "2026-05-18T12:00:00Z",
        "description": "A declarative JavaScript library for building UIs",
    }

    _print_dashboard(info)
    captured = capsys.readouterr()

    assert "facebook/react" in captured.out
    assert "226,000" in captured.out
    assert "47,000" in captured.out
    assert "1,200" in captured.out
    assert "JavaScript" in captured.out
    assert "MIT" in captured.out


def test_dashboard_multi_repo(capsys):
    """Dashboard with two repos should print both."""
    from ara.dashboard import _print_dashboard

    info_a = {
        "full_name": "vuejs/core",
        "stars": 50000,
        "forks": 7000,
        "open_issues": 300,
        "language": "TypeScript",
        "license": "MIT",
        "updated_at": "2026-05-17T00:00:00Z",
        "description": "Vue.js core",
    }
    info_b = {
        "full_name": "sveltejs/svelte",
        "stars": 80000,
        "forks": 4000,
        "open_issues": 200,
        "language": "TypeScript",
        "license": "MIT",
        "updated_at": "2026-05-16T00:00:00Z",
        "description": "Svelte framework",
    }

    _print_dashboard(info_a)
    print()  # blank line between repos (simulated)
    _print_dashboard(info_b)

    captured = capsys.readouterr()
    assert "vuejs/core" in captured.out
    assert "sveltejs/svelte" in captured.out


def test_dashboard_empty_fields(capsys):
    """Dashboard should handle missing description and language gracefully."""
    from ara.dashboard import _print_dashboard

    info = {
        "full_name": "owner/minimal",
        "stars": 100,
        "forks": 10,
        "open_issues": 0,
        "language": None,
        "license": None,
        "updated_at": None,
        "description": None,
    }

    _print_dashboard(info)
    captured = capsys.readouterr()

    assert "N/A" in captured.out  # language fallback
    assert "No description" in captured.out
    assert "None" in captured.out  # license fallback


# ===========================================================================
# Parser tests
# ===========================================================================


def test_parser_dashboard_command():
    """Parser should parse 'dashboard' subcommand."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["dashboard", "owner/repo"])
    assert args.command == "dashboard"
    assert args.repos == ["owner/repo"]


def test_parser_dashboard_multiple_repos():
    """Parser should accept multiple repos with dashboard."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["dashboard", "owner/a", "owner/b", "owner/c"])
    assert args.repos == ["owner/a", "owner/b", "owner/c"]


# ===========================================================================
# Integration test
# ===========================================================================


@patch("ara.cli.GitHubClient")
def test_main_dashboard_command(MockClient):
    """main() should dispatch dashboard command successfully."""
    from ara.cli import main

    mock_instance = MagicMock()
    MockClient.return_value = mock_instance
    mock_instance.get_repo_info.return_value = {
        "full_name": "owner/test-repo",
        "stars": 500,
        "forks": 100,
        "open_issues": 10,
        "language": "Python",
        "license": "MIT",
        "updated_at": "2026-05-18T12:00:00Z",
        "description": "A test repo",
        "name": "test-repo",
    }

    result = main(["dashboard", "owner/test-repo"])
    assert result == 0
