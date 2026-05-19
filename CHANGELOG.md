# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.3.0] - 2026-05-19

### Added
- `ara dashboard <repo...>` — Full repo overview dashboard panel
- `ara summary <repo>` — One-line repo overview (stars, forks, issues, language, license, description)
- `ara rank [--top N] [--json] [<repo> ...]` — Live Top N repo leaderboard 🔥
- `ara insight <repo>` — Deep repository intelligence (star velocity, topics, age, relative time)
- `ara compare` 3+ repos — N-way multi-repo comparison with 🥇🥈🥉 ranking
- `ara history <repo>` — Star growth ASCII timeline chart (simulated from created_at + current stars)
- `ara watch --notify` — Desktop notification (terminal bell) on star changes

### Changed
- Version bump to 0.3.0
- README v13 — Updated architecture table (added `chart.py`), BLOAT status synced, test count badge updated
- Test suite expanded to **251 tests** (0 failed) — chart engine extracted from history.py
- CLI now has **13 commands** accessible via `ara --help`

### Fixed
- Syntax error in cli.py (duplicate closing brace) — fixed
- Import error for cmd_summary_json — now properly exported
- `ara watch` terminal flicker — replaced full-screen clear with cursor-position refresh

## [0.2.0] - 2026-05-19

### Added
- `ara trends <repo>` — Star trend analysis with ASCII chart and JSON output
- `ara generate-stars <repo>` — Fetch stargazers and save to JSON file
- `pyproject.toml` build configuration

### Changed
- CLI help output includes trends command
- README restructured with navigation table, health badges, try-it-now hero
- core.py: refactored `_fetch_page_with_headers()` into shared `_request()` with header return
- core.py: extracted `_raise_api_error()` for centralized HTTP error handling

### Fixed
- setup.py URLs corrected from li1050109098 → lijiajing-11
- Test suite expanded to 140+ tests with trends edge cases

## [0.1.0] - 2026-05-18

### Added
- `ara stars <repo...>` — Quick star count(s) with mini leaderboard
- `ara watch <repo...>` — Real-time star watching with 30s refresh
- `ara battle <repo...>` — Side-by-side ASCII arena bar chart
- `ara info <repo...>` — Full repository metadata
- `ara compare <repo1> <repo2>` — Head-to-head comparison table
- JSON output mode (`--json`) on every command
- CI workflow (`.github/workflows/ci.yml`)
- Zero external dependencies (stdlib only)
- 126 initial tests (83% coverage)
