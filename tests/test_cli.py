"""Tests for `ara.cli` — parser building, command routing, argument validation."""

import argparse
from unittest.mock import MagicMock, patch

import pytest


# ===========================================================================
# Parser building tests
# ===========================================================================


def test_build_parser_returns_parser():
    """build_parser should return an ArgumentParser instance."""
    from ara.cli import build_parser

    parser = build_parser()
    assert isinstance(parser, argparse.ArgumentParser)


def test_build_parser_no_args_prints_help():
    """Building parser and parsing empty args should print help (no crash)."""
    from ara.cli import build_parser

    parser = build_parser()
    # parse_args with no args shows help and exits; just verify structure
    assert parser.prog == "ara"
    assert parser.description is not None


def test_parser_has_version_flag():
    """Parser should accept --version."""
    from ara.cli import build_parser

    parser = build_parser()
    # Verify the action exists without calling parse_args (which exits)
    for action in parser._actions:
        if hasattr(action, "option_strings") and "--version" in action.option_strings:
            return
    pytest.fail("No --version action found")


def test_parser_stars_command():
    """Parser should parse 'stars' subcommand with repos argument."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["stars", "owner/repo"])
    assert args.command == "stars"
    assert args.repos == ["owner/repo"]


def test_parser_stars_multiple_repos():
    """Parser should accept multiple repos for 'stars'."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["stars", "owner/a", "owner/b", "owner/c"])
    assert args.command == "stars"
    assert args.repos == ["owner/a", "owner/b", "owner/c"]


def test_parser_stars_missing_repo():
    """Parser should reject 'stars' without a repo argument."""
    from ara.cli import build_parser

    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["stars"])


def test_parser_watch_command():
    """Parser should parse 'watch' subcommand with repos argument."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["watch", "owner/repo"])
    assert args.command == "watch"
    assert args.repos == ["owner/repo"]


def test_parser_watch_multiple_repos():
    """Parser should accept multiple repos for 'watch'."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["watch", "owner/a", "owner/b"])
    assert args.command == "watch"
    assert args.repos == ["owner/a", "owner/b"]


def test_parser_watch_missing_repo():
    """Parser should reject 'watch' without a repo argument."""
    from ara.cli import build_parser

    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["watch"])


def test_parser_battle_command():
    """Parser should parse 'battle' subcommand with repos argument."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["battle", "owner/a", "owner/b"])
    assert args.command == "battle"
    assert args.repos == ["owner/a", "owner/b"]


def test_parser_battle_three_or_more():
    """Parser should accept 3+ repos for 'battle'."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["battle", "owner/a", "owner/b", "owner/c", "owner/d"])
    assert args.command == "battle"
    assert args.repos == ["owner/a", "owner/b", "owner/c", "owner/d"]


def test_parser_battle_missing_repo():
    """Parser should reject 'battle' without repos."""
    from ara.cli import build_parser

    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["battle"])


def test_parser_unknown_command():
    """Parser should reject unknown commands."""
    from ara.cli import build_parser

    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["unknown"])


def test_parser_sets_func_on_stars():
    """Stars subcommand should have func set to cmd_stars."""
    from ara.cli import build_parser, cmd_stars

    parser = build_parser()
    args = parser.parse_args(["stars", "owner/repo"])
    assert args.func == cmd_stars


def test_parser_sets_func_on_watch():
    """Watch subcommand should have func set to cmd_watch."""
    from ara.cli import build_parser, cmd_watch

    parser = build_parser()
    args = parser.parse_args(["watch", "owner/repo"])
    assert args.func == cmd_watch


def test_parser_sets_func_on_battle():
    """Battle subcommand should have func set to cmd_battle."""
    from ara.cli import build_parser, cmd_battle

    parser = build_parser()
    args = parser.parse_args(["battle", "owner/a", "owner/b"])
    assert args.func == cmd_battle


# ===========================================================================
# run_watch tests
# ===========================================================================


def test_run_watch_returns_star_count():
    """run_watch should call client.get_stars and return the count."""
    from ara.cli import run_watch

    mock_client = MagicMock()
    mock_client.get_stars.return_value = 1234

    result = run_watch("owner/repo", mock_client)
    assert result == 1234
    mock_client.get_stars.assert_called_once_with("owner/repo")


def test_run_watch_accepts_previous_param():
    """run_watch should accept (and ignore) the previous parameter."""
    from ara.cli import run_watch

    mock_client = MagicMock()
    mock_client.get_stars.return_value = 567

    result = run_watch("owner/repo", mock_client, previous=100)
    assert result == 567


def test_run_watch_returns_zero():
    """run_watch should return 0 when API returns 0."""
    from ara.cli import run_watch

    mock_client = MagicMock()
    mock_client.get_stars.return_value = 0

    result = run_watch("owner/repo", mock_client)
    assert result == 0


# ===========================================================================
# run_battle tests
# ===========================================================================


def test_run_battle_fetches_all_repos():
    """run_battle should fetch stars for each repo and format battle."""
    from ara.cli import run_battle

    mock_client = MagicMock()

    def mock_get_stars(repo):
        return {"owner/alpha": 1234, "owner/beta": 567}.get(repo, 0)

    mock_client.get_stars.side_effect = mock_get_stars

    result = run_battle(["owner/alpha", "owner/beta"], mock_client)
    assert mock_client.get_stars.call_count == 2
    assert "owner/alpha" in result
    assert "owner/beta" in result


def test_run_battle_single_repo():
    """run_battle should work with a single repo."""
    from ara.cli import run_battle

    mock_client = MagicMock()
    mock_client.get_stars.return_value = 42

    result = run_battle(["owner/solo"], mock_client)
    assert "owner/solo" in result


def test_run_battle_empty_list():
    """run_battle should handle empty repo list gracefully."""
    from ara.cli import run_battle

    mock_client = MagicMock()
    result = run_battle([], mock_client)
    assert isinstance(result, str)
    mock_client.get_stars.assert_not_called()


# ===========================================================================
# cmd_stars tests
# ===========================================================================


def test_cmd_stars_print_stars(capsys):
    """cmd_stars should print star counts."""
    from ara.cli import cmd_stars

    mock_client = MagicMock()
    mock_client.get_stars.return_value = 1234

    args = argparse.Namespace(repos=["owner/repo"])
    cmd_stars(args, mock_client)

    captured = capsys.readouterr()
    assert "owner/repo" in captured.out
    assert "1,234" in captured.out
    assert "★" in captured.out


def test_cmd_stars_multiple_repos(capsys):
    """cmd_stars should print star counts for multiple repos."""
    from ara.cli import cmd_stars

    mock_client = MagicMock()

    def mock_get_stars(repo):
        return {"owner/a": 100, "owner/b": 200}.get(repo, 0)

    mock_client.get_stars.side_effect = mock_get_stars

    args = argparse.Namespace(repos=["owner/a", "owner/b"])
    cmd_stars(args, mock_client)

    captured = capsys.readouterr()
    assert "owner/a" in captured.out
    assert "owner/b" in captured.out


def test_cmd_stars_none_result(capsys):
    """cmd_stars should print error when get_stars returns None."""
    from ara.cli import cmd_stars

    mock_client = MagicMock()
    mock_client.get_stars.return_value = None  # e.g., fetch failure

    args = argparse.Namespace(repos=["owner/missing"])
    cmd_stars(args, mock_client)

    captured = capsys.readouterr()
    assert "could not fetch" in captured.out


# ===========================================================================
# cmd_battle tests
# ===========================================================================


def test_cmd_battle_calls_format_battle(capsys):
    """cmd_battle should fetch stars, format battle, and print."""
    from ara.cli import cmd_battle

    mock_client = MagicMock()

    def mock_get_stars(repo):
        return {"owner/alpha": 1000, "owner/beta": 500}.get(repo, 0)

    mock_client.get_stars.side_effect = mock_get_stars

    args = argparse.Namespace(repos=["owner/alpha", "owner/beta"])
    cmd_battle(args, mock_client)

    captured = capsys.readouterr()
    assert "owner/alpha" in captured.out
    assert "owner/beta" in captured.out
    # Should contain some battle formatting
    assert "★" in captured.out or "BATTLE" in captured.out.upper()


# ===========================================================================
# main() tests
# ===========================================================================


@patch("ara.cli.GitHubClient")
def test_main_stars_command(MockClient):
    """main() should create a client and dispatch stars command."""
    from ara.cli import main

    mock_instance = MagicMock()
    MockClient.return_value = mock_instance
    mock_instance.get_stars.return_value = 42

    result = main(["stars", "owner/repo"])
    assert result == 0
    mock_instance.get_stars.assert_called_with("owner/repo")


@patch("ara.cli.GitHubClient")
def test_main_battle_command(MockClient):
    """main() should dispatch battle command successfully."""
    from ara.cli import main

    mock_instance = MagicMock()

    def mock_get_stars(repo):
        return {"owner/a": 100, "owner/b": 200}.get(repo, 0)

    mock_instance.get_stars.side_effect = mock_get_stars
    MockClient.return_value = mock_instance

    result = main(["battle", "owner/a", "owner/b"])
    assert result == 0


def test_main_no_command():
    """main() with no command should return 1 and print help."""
    from ara.cli import main

    result = main([])
    assert result == 1


def test_main_unknown_command():
    """main() with unknown command should return error."""
    from ara.cli import main

    with pytest.raises(SystemExit) as exc_info:
        main(["unknown"])
    assert exc_info.value.code == 2


@patch("ara.cli.GitHubClient")
def test_main_value_error_handling(MockClient):
    """main() should catch ValueError and return 1."""
    from ara.cli import main

    mock_instance = MagicMock()
    MockClient.return_value = mock_instance
    mock_instance.get_stars.side_effect = ValueError("Repository not found")

    result = main(["stars", "owner/nonexistent"])
    assert result == 1


@patch("ara.cli.GitHubClient")
def test_main_runtime_error_handling(MockClient):
    """main() should catch RuntimeError and return 1."""
    from ara.cli import main

    mock_instance = MagicMock()
    MockClient.return_value = mock_instance
    mock_instance.get_stars.side_effect = RuntimeError("GitHub API error")

    result = main(["stars", "owner/repo"])
    assert result == 1
