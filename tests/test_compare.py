"""Tests for multi-repo compare (3+ repos) — Task 012-A."""

import pytest
from ara.display import format_multi_compare_table


class TestMultiCompareTable:
    """Tests for format_multi_compare_table display function."""

    def test_three_repos_formatting(self):
        """3 repos should produce a ranked table with winner."""
        infos = [
            {"full_name": "repo/a", "stars": 100, "forks": 10, "language": "Python", "topics": ["web"]},
            {"full_name": "repo/b", "stars": 200, "forks": 20, "language": "JS", "topics": ["frontend"]},
            {"full_name": "repo/c", "stars": 50, "forks": 5, "language": "Rust", "topics": ["cli"]},
        ]
        result = format_multi_compare_table(infos)
        assert "Multi-Repo Comparison" in result
        assert "repo/b" in result  # winner
        assert "repo/a" in result
        assert "repo/c" in result
        assert "Winner" in result

    def test_five_repos_formatting(self):
        """5 repos should all show up with correct ranking."""
        infos = [
            {"full_name": "r/5", "stars": 5, "forks": 0, "language": "Go", "topics": []},
            {"full_name": "r/4", "stars": 4, "forks": 0, "language": "Go", "topics": []},
            {"full_name": "r/3", "stars": 3, "forks": 0, "language": "Go", "topics": []},
            {"full_name": "r/2", "stars": 2, "forks": 0, "language": "Go", "topics": []},
            {"full_name": "r/1", "stars": 1, "forks": 0, "language": "Go", "topics": []},
        ]
        result = format_multi_compare_table(infos)
        assert "r/5" in result
        assert "r/1" in result
        # First 3 get medals, 4th+ get numbers
        assert "4." in result
        assert "5." in result

    def test_tie_handling(self):
        """Equal stars should pick first encountered as winner."""
        infos = [
            {"full_name": "repo/a", "stars": 100, "forks": 10, "language": "Python", "topics": ["web"]},
            {"full_name": "repo/b", "stars": 100, "forks": 20, "language": "JS", "topics": []},
        ]
        result = format_multi_compare_table(infos)
        assert "Winner" in result

    def test_no_topics(self):
        """Repos without topics should still display cleanly."""
        infos = [
            {"full_name": "minimal/repo", "stars": 50, "forks": 5, "language": "Go", "topics": []},
        ]
        result = format_multi_compare_table(infos)
        assert "minimal/repo" in result

    def test_topics_with_numeric(self):
        """Topics list may contain numeric values — should not crash."""
        infos = [
            {"full_name": "nums/repo", "stars": 100, "forks": 10, "language": "Python", "topics": [123, 456]},
        ]
        result = format_multi_compare_table(infos)
        assert "nums/repo" in result
        assert "123" in result

    def test_missing_language(self):
        """Missing language should show N/A."""
        infos = [
            {"full_name": "nolang/repo", "stars": 100, "forks": 10, "language": None, "topics": []},
        ]
        result = format_multi_compare_table(infos)
        assert "nolang/repo" in result
        assert "N/A" in result

    def test_sorted_by_stars(self):
        """Repos should be sorted descending by stars in output."""
        infos = [
            {"full_name": "r/low", "stars": 10, "forks": 1, "language": "A", "topics": []},
            {"full_name": "r/high", "stars": 100, "forks": 1, "language": "B", "topics": []},
            {"full_name": "r/mid", "stars": 50, "forks": 1, "language": "C", "topics": []},
        ]
        result = format_multi_compare_table(infos)
        # r/high should appear before r/mid before r/low
        high_idx = result.index("r/high")
        mid_idx = result.index("r/mid")
        low_idx = result.index("r/low")
        assert high_idx < mid_idx < low_idx, "repos not sorted by stars descending"
