"""Tests for ara.chart — ASCII chart rendering."""

import pytest
from ara.chart import render_line_chart


class TestRenderChart:
    """Tests for render_line_chart function."""

    def test_empty_timeline(self):
        result = render_line_chart([], "test/repo")
        assert "No history" in result

    def test_single_point(self):
        result = render_line_chart([{"stars": 100, "date": "2025-01-01"}], "test/repo")
        assert "test/repo" in result
        assert "100" in result

    def test_multiple_points(self):
        timeline = [
            {"stars": 0, "date": "2020-01-01"},
            {"stars": 50, "date": "2022-01-01"},
            {"stars": 100, "date": "2024-01-01"},
            {"stars": 200, "date": "2026-01-01"},
        ]
        result = render_line_chart(timeline, "growing/repo")
        assert "growing/repo" in result
        assert "●" in result

    def test_upward_trend_label(self):
        result = render_line_chart(
            [{"stars": 10, "date": "2020-01-01"}, {"stars": 500, "date": "2026-01-01"}],
            "trend/repo",
        )
        assert "Star History" in result

    def test_chart_has_dates(self):
        timeline = [
            {"stars": 10, "date": "2020-01-01"},
            {"stars": 30, "date": "2026-12-31"},
        ]
        result = render_line_chart(timeline, "dated/repo")
        assert "2020-01-01" in result
        assert "2026-12-31" in result

    def test_large_star_count_formatting(self):
        timeline = [{"stars": 0, "date": "2013-01-01"}, {"stars": 226000, "date": "2026-01-01"}]
        result = render_line_chart(timeline, "big/repo")
        assert "226,000" in result

    def test_custom_bar_char(self):
        timeline = [{"stars": 0, "date": "2020-01-01"}, {"stars": 100, "date": "2026-01-01"}]
        result = render_line_chart(timeline, "custom/repo", bar_char="█")
        assert "█" in result
