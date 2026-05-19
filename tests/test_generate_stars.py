"""Tests for `ara generate-stars` command (Task 006-B)."""

import json
import os
import tempfile
import time
from unittest.mock import MagicMock, patch

from ara.trends import StarEvent


def test_safe_filename():
    """_safe_filename should convert owner/repo to safe filename."""
    from ara.generate_stars import _safe_filename

    assert _safe_filename("owner/repo") == "stargazers_owner_repo.json"
    assert _safe_filename("python/cpython") == "stargazers_python_cpython.json"
    assert _safe_filename("a/b") == "stargazers_a_b.json"


@patch("ara.generate_stars.get_star_history")
def test_cmd_generate_stars_saves_file(mock_get_history):
    """cmd_generate_stars should create a JSON file with correct data."""
    from ara.generate_stars import cmd_generate_stars

    now = time.time()
    mock_get_history.return_value = [
        StarEvent(timestamp=now - 3600, repo="owner/repo"),
        StarEvent(timestamp=now - 1800, repo="owner/repo"),
        StarEvent(timestamp=now - 100, repo="owner/repo"),
    ]

    class MockArgs:
        repo = "owner/repo"
        pages = 3
        output = None

    client = MagicMock()

    # Use temp dir to avoid polluting repo
    orig_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        try:
            output_path = cmd_generate_stars(MockArgs(), client)

            assert output_path == "stargazers_owner_repo.json"
            assert os.path.exists(output_path)

            with open(output_path) as f:
                data = json.load(f)

            assert len(data) == 3
            assert data[0]["repo"] == "owner/repo"
            assert "timestamp" in data[0]
            assert "iso_date" in data[0]
        finally:
            os.chdir(orig_cwd)


@patch("ara.generate_stars.get_star_history")
def test_cmd_generate_stars_empty_repo(mock_get_history):
    """Empty stargazers should produce empty array, no crash."""
    from ara.generate_stars import cmd_generate_stars

    mock_get_history.return_value = []

    class MockArgs:
        repo = "empty/repo"
        pages = 3
        output = None

    client = MagicMock()

    orig_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        try:
            output_path = cmd_generate_stars(MockArgs(), client)

            assert os.path.exists(output_path)
            with open(output_path) as f:
                data = json.load(f)
            assert data == []
        finally:
            os.chdir(orig_cwd)


@patch("ara.generate_stars.get_star_history")
def test_cmd_generate_stars_shows_stats(mock_get_history):
    """Output should include stats lines for repos with data."""
    from ara.generate_stars import cmd_generate_stars

    now = time.time()
    mock_get_history.return_value = [
        StarEvent(timestamp=now - 100_000, repo="stats/repo"),
        StarEvent(timestamp=now - 50_000, repo="stats/repo"),
        StarEvent(timestamp=now - 10_000, repo="stats/repo"),
    ]

    class MockArgs:
        repo = "stats/repo"
        pages = 3
        output = None

    client = MagicMock()

    orig_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        try:
            # Capture stdout to check stats output
            from io import StringIO
            import sys
            captured = StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured
            try:
                cmd_generate_stars(MockArgs(), client)
            finally:
                sys.stdout = old_stdout

            output = captured.getvalue()
            assert "Total stargazers fetched" in output
            assert "Peak hour" in output
            assert "Highest single-day" in output
        finally:
            os.chdir(orig_cwd)
