# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
