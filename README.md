<p align="center">
  <img src="https://img.shields.io/badge/⚡_ARA_|_Arena_Star_Tracker-8A2BE2?style=for-the-badge" alt="ARA Banner"/>
</p>

<h1 align="center">⚡ ARA — Arena Star Tracker</h1>

<p align="center">
  <b>Zero-dependency CLI that tracks, watches, compares, and battles GitHub repos — right from your terminal.</b><br>
  <i>Think Google Analytics for GitHub Stars, but you never leave the command line.</i>
</p>

<p align="center">
  <sup><i>Built by <b>Α-Tech Inc.</b> — where we turn data into arenas. 🏟️</i></sup>
</p>

---

## 📑 Navigation

| # | Section | What's inside |
|---|---------|---------------|
| 🎯 | [What is ARA?](#-what-is-ara) | Scenario table, 8 core highlights |
| 🚀 | [Quick Start](#-quick-start) | `pip install`, first commands, run without install |
| 📖 | [Commands](#-commands) | All 6 commands with live output examples |
| 🏗️ | [Architecture](#️-architecture) | Module map, project structure tree |
| 🔧 | [Development](#-development) | Clone, venv, test, lint, demo |
| ⏳ | [Rate Limits](#-rate-limits--reliability) | Token setup, retry + cache details |
| 🤝 | [Contributing](#-contributing) | PR guide + idea wishlist |
| 📝 | [License](#-license) | MIT + links |

---

### ⚡ Try it now — no install required

```bash
git clone https://github.com/lijiajing-11/alpha-project-arena.git
cd alpha-project-arena
python -m ara stars python/cpython
```

---

## 🏅 Project Health

| Category | Badges |
|----------|--------|
| **Python** | <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+"/></a> <a href="https://github.com/lijiajing-11/alpha-project-arena"><img src="https://img.shields.io/github/languages/top/lijiajing-11/alpha-project-arena?color=blueviolet" alt="Language"/></a> |
| **Release** | <a href="https://pypi.org/project/ara/"><img src="https://img.shields.io/pypi/v/ara?color=8A2BE2&label=pypi" alt="PyPI"/></a> <a href="https://pypi.org/project/ara/"><img src="https://img.shields.io/pypi/dm/ara?color=3b82f6" alt="Downloads"/></a> <a href="https://github.com/lijiajing-11/alpha-project-arena/releases"><img src="https://img.shields.io/badge/status-alpha-f97316" alt="Status"/></a> |
| **Quality** | <a href="https://github.com/lijiajing-11/alpha-project-arena/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/lijiajing-11/alpha-project-arena/ci.yml?label=CI&color=22c55e" alt="CI"/></a> <a href="https://github.com/lijiajing-11/alpha-project-arena"><img src="https://img.shields.io/badge/code%20style-ruff-9749eb" alt="Code Style"/></a> <a href="https://github.com/lijiajing-11/alpha-project-arena"><img src="https://img.shields.io/badge/tests-90%2B-22c55e" alt="Tests"/></a> |
| **Community** | <a href="https://github.com/lijiajing-11/alpha-project-arena"><img src="https://img.shields.io/github/stars/lijiajing-11/alpha-project-arena?label=stars&color=facc15" alt="Stars"/></a> <a href="https://github.com/lijiajing-11/alpha-project-arena/graphs/contributors"><img src="https://img.shields.io/github/contributors/lijiajing-11/alpha-project-arena?color=22c55e" alt="Contributors"/></a> <a href="https://github.com/lijiajing-11/alpha-project-arena/issues"><img src="https://img.shields.io/github/issues/lijiajing-11/alpha-project-arena?label=open%20issues" alt="Issues"/></a> |
| **Meta** | <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e" alt="MIT"/></a> <a href="https://github.com/lijiajing-11/alpha-project-arena"><img src="https://img.shields.io/github/last-commit/lijiajing-11/alpha-project-arena?label=updated" alt="Last Commit"/></a> <a href="https://github.com/lijiajing-11/alpha-project-arena"><img src="https://img.shields.io/badge/OS-linux_%7C_macOS_%7C_windows-555" alt="OS"/></a> <a href="https://x.com/ATechInc"><img src="https://img.shields.io/badge/🐦-follow_%40ATechInc-1DA1F2" alt="Twitter/X"/></a> <a href="https://github.com/lijiajing-11/alpha-project-arena"><img src="https://img.shields.io/badge/PRs-welcome-22c55e" alt="PRs Welcome"/></a> |

---

```text
$ ara --help

usage: ara [-h] {stars,watch,battle,info,compare} ...

Zero-dependency GitHub Star tracker. Track, compare, and battle repos.

positional arguments:
  {stars,watch,battle,info,compare}
    stars       Get star count(s) for one or more repos
    watch       Watch repos in real-time (30s refresh)
    battle      Side-by-side arena battle with ASCII bars
    info        Detailed repo metadata (stars, forks, license, etc.)
    compare     Head-to-head comparison table

options:
  -h, --help   show this help message and exit
  --json       Machine-readable JSON output (every command)
```

---

## 🎯 What is ARA?

**ARA** is a pure-Python CLI for monitoring GitHub stars in real time. No `requests`, no `httpx`, no `aiohttp` — just `urllib` from the standard library. It installs in 5 seconds and works immediately.

**Built by [Α-Tech Inc.](https://github.com/lijiajing-11/alpha-project-arena)** — where we turn data into arenas. 🏟️

| Scenario | Why ARA? | One-liner |
|----------|----------|-----------|
| 👀 **New release day** | Watch stars roll in live | `ara watch owner/repo` |
| 🏟️ **Shootout your stack** | Battle two frameworks | `ara battle react vue` |
| 📋 **Due diligence** | Full repo metadata | `ara info owner/repo` |
| ⚖️ **Side-by-side** | Compare forks, license, age | `ara compare a/A b/B` |
| 🤖 **CI / scripting** | JSON output, pipe to jq | `ara stars --json repo` |

### ✨ Highlights

| # | Feature | Why it matters |
|---|---------|----------------|
| 1 | 🍃 **Zero external deps** | `pip install ara` → done. No npm, no Docker, no `requirements.txt` |
| 2 | ⚡ **Real-time watching** | Live polling with color-coded deltas. Press Ctrl+C for a session summary |
| 3 | 🏆 **Arena Battle mode** | Side-by-side comparison _with animated ASCII bars_. Yes, really |
| 4 | 🎨 **Beautiful terminal output** | ANSI colors, box-drawing tables, leaderboards |
| 5 | 📦 **JSON output** | Every command supports `--json`. Pipe to jq, feed dashboards, log to files |
| 6 | ⏳ **Smart retry + caching** | Exponential backoff on rate limits, 60s TTL cache |
| 7 | 🔧 **Extensible** | Add a new command by adding one function to `cli.py` |
| 8 | 📈 **Trend analysis** | `ara trends` shows stargazer history as an ASCII chart. Custom time windows and JSON export |

---

## 🚀 Quick Start

### Install

```bash
pip install ara
```

That's it. No config, no API tokens required to get started.

> ⚠️ **Rate limits:** Without a `GITHUB_TOKEN`, unauthenticated limit is **60 req/h**. Set `export GITHUB_TOKEN=...` for 5,000/h. ARA auto-retries on 429s with exponential backoff + jitter.

### First Commands

```bash
# ① Check any repo's stars
ara stars python/cpython

# ② Watch live as stars tick up
ara watch tensorflow/tensorflow

# ③ Battle your favorite frameworks
ara battle facebook/react vuejs/core sveltejs/svelte

# ④ See star trend history over 72 hours
ara trends tensorflow/tensorflow
```

> 💡 **Tip:** Run `ara --help` anytime to see all available commands and flags.

---

## 📖 Commands

Six commands, sorted from quick-check to head-to-head analysis. Every command supports `--json`.

| Command | Description | Quick example |
|---------|-------------|---------------|
| 🔍 `ara stars <repo...>` | Quick star count(s) | `ara stars owner/project` |
| 👀 `ara watch <repo...>` | Real-time live watch (30s refresh) | `ara watch owner/project` |
| 🏟️ `ara battle <repo...>` | Arena bar-chart battle | `ara battle libA libB libC` |
| 📈 `ara trends <repo>` | Star trend chart over time | `ara trends owner/repo` |
| 📋 `ara info <repo...>` | Full repo metadata dump | `ara info owner/project` |
| ⚖️ `ara compare <r1> <r2>` | Head-to-head comparison table | `ara compare a/A b/B` |

---

### 🔍 `ara stars` — Quick Check

```text
$ ara stars python/cpython tensorflow/tensorflow

  ★ python/cpython: 63,475 stars
  ★ tensorflow/tensorflow: 187,634 stars

  Mini Leaderboard
  ────────────────────────────────────────
  🥇 tensorflow/tensorflow         187,634 ★
  🥈 python/cpython                  63,475 ★
```

```bash
# JSON mode for scripting
ara stars --json python/cpython tensorflow/tensorflow
```

---

### 👀 `ara watch` — Real-Time Dashboard

Watch a single repo with a **multi-field dashboard** — stars, forks, issues, language, license, and color-coded deltas. Press `Ctrl+C` to stop.

```text
$ ara watch owner/repo

╔════════════════════════════════════════════╗
║        📡 ARA Star Tracker — WATCH         ║
╚════════════════════════════════════════════╝

┌────────────────────┬────────────────────────┐
│ Repository         │ owner/repo              │
├────────────────────┼────────────────────────┤
│ ⭐ Stars           │ 12,345  (+5)            │
│ ⑂ Forks            │ 234     (+1)            │
│ ⚠ Issues           │ 12     (-2)             │
│ 🔤 Language        │ Python                  │
│ 📜 License         │ MIT                     │
│ 🕐 Updated         │ 2026-05-19 14:30:22     │
│ 📅 Created         │ 2020-01-15              │
└────────────────────┴────────────────────────┘

Last updated: 14:30:52  |  Press Ctrl+C to stop
```

Delta values are **color-coded**: green for growth, red for decline.

Watch **multiple repos** side-by-side in a compact table:

```text
$ ara watch owner/repo-a owner/repo-b

╔══════════════════════════════════════════════════════════════════╗
║        📡 ARA Multi-Watch                                       ║
╚══════════════════════════════════════════════════════════════════╝

┌──────────┬──────────┬───────┬────────┬────────┬────────┐
│ Repo     │ ⭐ Stars │ ⑂ Forks│ ⚠ Issues│ 🔤 Lang│ 📜 Lic │
├──────────┼──────────┼───────┼────────┼────────┼────────┤
│ owner/a  │ 12,345   │ 234   │ 12     │ Python │ MIT    │
│ owner/b  │ 567      │ 12    │ 3      │ Rust   │ Apache │
└──────────┴──────────┴───────┴────────┴────────┴────────┘

Watching 2 repos  ·  14:30:52  ·  Ctrl+C to stop
```

```bash
# JSON mode — one JSON object per tick
ara watch --json owner/repo-a owner/repo-b
```

---

### 🏟️ `ara battle` — Arena Showdown

```text
$ ara battle facebook/react vuejs/core

  ╔══════════════════════════════════════════╗
  ║          ★ ARENA BATTLE ★               ║
  ║                                          ║
  ║  ★ facebook/react                        ║
  ║    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 230,000 ★      ║
  ║                                          ║
  ║  ★ vuejs/core                            ║
  ║    ▓▓▓▓▓▓▓▓░░░░░░░░░░░░ 47,000 ★        ║
  ║                                          ║
  ║  ✦ facebook/react dominates the arena! ✦ ║
  ╚══════════════════════════════════════════╝
```

```bash
# Winner declared in JSON
ara battle --json facebook/react vuejs/core
```

---

### 📋 `ara info` — Repository Details

```text
$ ara info python/cpython

  ┌─────────────────────────────────────────────┐
  │  python/cpython                              │
  ├─────────────────────────────────────────────┤
  │  ⭐ Stars        63,475                      │
  │  ⑂ Forks         26,134                      │
  │  ⚠ Issues        1,234                       │
  │  🔤 Language     Python                      │
  │  📜 License      Python Software Foundation  │
  │  🕐 Updated      2026-05-18                   │
  │  📅 Created      1990-01-01                   │
  └─────────────────────────────────────────────┘
```

```bash
ara info --json python/cpython
```

---

### ⚖️ `ara compare` — Head-to-Head

```text
$ ara compare facebook/react vuejs/core

  ╔══════════════════════════════════════════════════════════╗
  ║                    ⚖️  REPO COMPARISON                    ║
  ╚══════════════════════════════════════════════════════════╝

  ┌─────────────┬──────────────────┬──────────────────┬────────┐
  │ Metric      │ facebook/react   │ vuejs/core       │ Victor │
  ├─────────────┼──────────────────┼──────────────────┼────────┤
  │ ⭐ Stars    │ 230,000          │ 47,000           │ 🏆 a  │
  │ ⑂ Forks     │ 48,000           │ 7,000            │ 🏆 a  │
  │ ⚠ Issues    │ 1,200            │ 800              │ 🏆 b  │
  │ 🔤 Language │ JavaScript       │ TypeScript       │ —      │
  │ 📜 License  │ MIT              │ MIT              │ —      │
  │ 📅 Created  │ 2013-05-29       │ 2019-12-14       │ —      │
  │ 🕐 Updated  │ 2026-05-19       │ 2026-05-18       │ —      │
  └─────────────┴──────────────────┴──────────────────┴────────┘

  🏆 facebook/react WINS!
     Leads by 183,000 stars over vuejs/core
     Also leads in forks: 41,000 more
```

```bash
ara compare --json facebook/react vuejs/core
```

```json
{
  "command": "compare",
  "repos": [
    {
      "full_name": "facebook/react",
      "stars": 230000,
      "forks": 48000,
      "open_issues": 1200,
      "language": "JavaScript",
      "license": "MIT",
      "created_at": "2013-05-29T00:00:00Z",
      "updated_at": "2026-05-19T12:00:00Z"
    },
    {
      "full_name": "vuejs/core",
      "stars": 47000,
      "forks": 7000,
      "open_issues": 800,
      "language": "TypeScript",
      "license": "MIT",
      "created_at": "2019-12-14T00:00:00Z",
      "updated_at": "2026-05-18T10:00:00Z"
    }
  ],
  "winner": "facebook/react",
  "lead_by": 183000,
  "fork_leader": "facebook/react",
  "issue_leader": "vuejs/core",
  "errors": null
}
```

---

### 📈 `ara trends` — Star Trend Analysis

Watch how a repo's stars accumulate over time with ASCII trend charts. No external data — uses the GitHub Stargazers API directly.

```text
$ ara trends owner/repo

📈 Trends for owner/repo (last 72h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Time              Stars    ▲/▼
──────────────────────────────────────
2026-05-18 09:00    12    ▲ +3
2026-05-18 12:00    10    ▲ +1
2026-05-18 15:00     9     ▼ -0
2026-05-18 18:00    14    ▲ +5
2026-05-18 21:00    11     ▼ -1
2026-05-19 00:00     8     ▼ -2
2026-05-19 03:00     6     ▼ -2
2026-05-19 06:00    15    ▲ +6
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total new stars: 85   Best hour: 06:00 (+6)
```

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--hours` | `72` | Lookback window in hours |
| `--interval` | `60` | Bucket size in minutes |
| `--json` | — | Machine-readable JSON output |

```bash
# 24-hour window, 30-minute buckets
ara trends owner/repo --hours 24 --interval 30

# JSON for your dashboard
ara trends --json owner/repo
```

```json
{
  "repo": "owner/repo",
  "hours": 72,
  "buckets": [
    {"label": "2026-05-18 09:00", "count": 12, "delta": 3}
  ],
  "total": 85,
  "best_hour": "06:00"
}
```

---

### 📦 JSON Output

Every ARA command accepts `--json` for machine-readable output — perfect for CI pipelines, dashboards, and scripts:

| Command | JSON flag | What you get |
|---------|-----------|--------------|
| `ara stars --json owner/repo` | ✅ | Array of `{repo, stars}` objects |
| `ara watch --json owner/repo` | ✅ | One JSON object per 30s tick |
| `ara battle --json owner/a owner/b` | ✅ | Battle results with `winner` field |
| `ara compare --json owner/a owner/b` | ✅ | Full comparison with `winner`, `lead_by`, `fork_leader` |
| `ara trends --json owner/repo` | ✅ | Trend data with `buckets`, `total`, `best_hour` |
| `ara info --json owner/repo` | ✅ | Full repo metadata as JSON |

```bash
# Example: pipe to jq for quick analysis
ara compare --json facebook/react vuejs/core | jq '.winner'

# Output: "facebook/react"
```

---

## 🖼️ Screenshots

![ARA Battle Demo](https://img.shields.io/badge/screenshot-coming_soon-8A2BE2?style=flat-square)

> 🎥 **Want to contribute a screenshot?** Record one with `asciinema rec docs/ara-demo.cast` and convert to GIF with `agg`. Drop the `.gif` in `docs/` and update this section!

```text
  ╔══════════════════════════════════════════╗
  ║          ★ ARENA BATTLE ★               ║
  ║                                          ║
  ║  ★ facebook/react         ▓▓▓▓▓▓▓▓      ║
  ║  ★ vuejs/core             ▓▓░░░░░░      ║
  ║                                          ║
  ║  ✦ react dominates!                     ║
  ╚══════════════════════════════════════════╝
```

---

## 🏗️ Architecture

ARA is designed as a **single-file-per-responsibility** Python package — no framework, no wiring, no over-engineering.

| Module | Responsibility |
|--------|---------------|
| `ara/cli.py` | Argument parsing + command dispatch |
| `ara/core.py` | GitHub API client, cache, data models |
| `ara/display.py` | Live watch terminal UI |
| `ara/battle.py` | Arena battle ASCII bars |
| `ara/colors.py` | ANSI color constants |
| `ara/console.py` | Console entry point (`console_scripts`) |

---

## 🔧 Development

```bash
# Clone
git clone https://github.com/lijiajing-11/alpha-project-arena.git
cd alpha-project-arena

# Virtual env + editable install
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Run the full test suite (90+ tests passing)
pytest tests/ -v

# Lint with ruff
ruff check .

# Generate demo output
python scripts/demo.py
```

### Project Structure

```
alpha-project-arena/
├── ara/                  # Package source
│   ├── __init__.py       # Package init, __version__
│   ├── __main__.py       # Entry point for `python -m ara`
│   ├── cli.py            # CLI argument parser & all commands
│   ├── core.py           # Data models, cache, GitHub API client
│   ├── display.py        # Watch display formatting
│   ├── battle.py         # Battle display & ASCII bars
│   ├── colors.py         # Shared ANSI colour constants
│   └── console.py        # Console entry point
├── tests/                # Test suite (pytest, 90+ tests)
│   ├── conftest.py
│   ├── test_cli.py
│   ├── test_core.py
│   ├── test_battle.py
│   ├── test_info.py
│   └── test_watch.py
├── scripts/
│   └── demo.py           # Demo output generator
├── docs/                 # Documentation & screenshots (coming soon)
├── setup.py              # Package metadata
├── LICENSE               # MIT license
└── README.md             # ← You are here! 🎉
```

---

## ⏳ Rate Limits & Reliability

<details>
<summary>Click to expand</summary>

| Auth | Limit | Setup |
|------|-------|-------|
| None | 60 req/h | Just works — fine for casual use |
| Token | 5,000 req/h | `export GITHUB_TOKEN=ghp_...` |

ARA automatically **retries** on rate limits (429), server errors (5xx), and transient network failures using exponential backoff with jitter. Results are cached for **60 seconds** to minimize unnecessary API calls.

</details>

---

## 🤝 Contributing

All contributions welcome — code, docs, ideas, or bug reports!

1. 🍴 **Fork** the repo
2. 🌿 `git checkout -b feat/your-idea`
3. 🛠️ Make your changes (Python 3.10+, ruff style)
4. ✅ `pytest tests/ -v` — keep the suite green
5. 📬 Open a **Pull Request** against `main`

### Ideas to run with

| Idea | Difficulty |
|------|------------|
| 🕸️ Web UI / dashboard | Medium |
| 💬 Slack & Discord webhook integration | Easy |
| 📈 Historical star charts (daily snapshots → plot) | Medium |
| 🏅 GitHub Action badge generator from ARA data | Easy |
| 📊 Export to CSV / JSON / Markdown | Easy |
| 🔒 Private repo support (token-authed) | Easy |
| 📈 `ara trend` — find fast-growing repos in a topic | Medium |
| 🎥 Asciinema demo GIF | Easy |

---

## 📝 License

MIT © [lijiajing-11](https://github.com/lijiajing-11)

---

<p align="center">
  <sub>
    <b>Built by </b>
    <img src="https://img.shields.io/badge/Α--Tech_Inc.-8A2BE2?style=flat-square" alt="Α-Tech Inc."/>
    <br/>
    <i>"Watch. Compete. Win."</i>
  </sub>
  <br/><br/>
  <a href="https://github.com/lijiajing-11/alpha-project-arena">GitHub</a>
  ·
  <a href="https://pypi.org/project/ara/">PyPI</a>
  ·
  <a href="https://github.com/lijiajing-11/alpha-project-arena/issues">Issues</a>
  ·
  <a href="https://x.com/ATechInc">Twitter/X</a>
  <br/><br/>
  <sub>⭐ Star us on GitHub — every star feeds the arena! ⭐</sub>
  <br/>
  <sub>
    <a href="mailto:dev@alpha-project.dev">dev@alpha-project.dev</a>
  </sub>
</p>
