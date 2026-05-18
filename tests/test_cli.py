"""Tests for ARA CLI entry points and packaging (Task 001 dependencies)."""

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_main_module_entry():
    """`python -m ara` should work without errors."""
    result = subprocess.run(
        [sys.executable, "-m", "ara", "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "ARA" in result.stdout
    assert "stars" in result.stdout
    assert "watch" in result.stdout
    assert "battle" in result.stdout


def test_version_flag():
    """`--version` should display the correct version."""
    result = subprocess.run(
        [sys.executable, "-m", "ara", "--version"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "0.1.0" in result.stdout


def test_no_command_shows_help():
    """Running `ara` with no args should show help and return 1."""
    result = subprocess.run(
        [sys.executable, "-m", "ara"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "usage:" in result.stdout or "usage:" in result.stderr


def test_stars_repo_not_found():
    """`ara stars nonexistent/repo` should show a friendly error."""
    result = subprocess.run(
        [sys.executable, "-m", "ara", "stars", "nonexistent-repo-12345/foobar"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 1
    assert "Error:" in (result.stdout + result.stderr)


def test_battle_no_args():
    """`ara battle` without repos should show help."""
    result = subprocess.run(
        [sys.executable, "-m", "ara", "battle"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2  # argparse error for missing args
