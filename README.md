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

<p align="center">
  <a href="https://github.com/lijiajing-11/alpha-project-arena/stargazers">
    <img src="https://img.shields.io/github/stars/lijiajing-11/alpha-project-arena?style=social" alt="GitHub Stars"/>
  </a>
  <a href="https://github.com/lijiajing-11/alpha-project-arena/forks">
    <img src="https://img.shields.io/github/forks/lijiajing-11/alpha-project-arena?style=social" alt="GitHub Forks"/>
  </a>
  <a href="https://x.com/ATechInc">
    <img src="https://img.shields.io/twitter/follow/ATechInc?style=social" alt="Follow on X"/>
  </a>
</p>

<p align="center">
  <a href="https://pypi.org/project/ara/">
    <img src="https://img.shields.io/pypi/v/ara?color=8A2BE2&label=PyPI%20v0.3.0" alt="PyPI"/>
  </a>
  <a href="https://pypi.org/project/ara/">
    <img src="https://img.shields.io/pypi/dm/ara?color=3b82f6&label=downloads" alt="Downloads"/>
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+"/>
  </a>
  <a href="https://github.com/lijiajing-11/alpha-project-arena/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-22c55e" alt="MIT"/>
  </a>
  <a href="https://github.com/lijiajing-11/alpha-project-arena/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/lijiajing-11/alpha-project-arena?color=22c55e" alt="Contributors"/>
  </a>
  <a href="https://github.com/lijiajing-11/alpha-project-arena/issues">
    <img src="https://img.shields.io/github/issues/lijiajing-11/alpha-project-arena?label=open%20issues" alt="Issues"/>
  </a>
  <a href="https://github.com/lijiajing-11/alpha-project-arena">
    <img src="https://img.shields.io/github/last-commit/lijiajing-11/alpha-project-arena?label=updated" alt="Last Commit"/>
  </a>
  <a href="https://github.com/lijiajing-11/alpha-project-arena">
    <img src="https://img.shields.io/badge/PRs-welcome-22c55e" alt="PRs Welcome"/>
  </a>
</p>

## 🎬 Gallery

> Get a feel for ARA in action — four commands, four vibes.

### 🏆 `ara rank` — Live Repository Leaderboard

```text
🏆 ARA Rank — Top 10 Hot Repos
┌───┬──────────────────────────────┬────────────┬────────┬────────────┐
│ # │ Repo                         │     Stars   │  Forks │ Language   │
├───┼──────────────────────────────┼────────────┼────────┼────────────┤
│ 🥇 1 │ facebook/react               │    226,000 │  47k   │ JavaScript │
│ 🥈 2 │ sveltejs/svelte              │     82,000 │   4k   │ TypeScript │
│ 🥉 3 │ vuejs/core                   │     47,000 │   7k   │ TypeScript │
│   4 │ vercel/next.js               │    126,000 │  26k   │ JavaScript │
│   5 │ twbs/bootstrap               │    170,000 │  79k   │ CSS        │
│   6 │ angular/angular              │     96,000 │  26k   │ TypeScript │
│   7 │ d3/d3                        │    110,000 │  33k   │ JavaScript │
│   8 │ nodejs/node                  │    108,000 │  30k   │ JavaScript │
│   9 │ lodash/lodash                │     60,000 │   7k   │ JavaScript │
│  10 │ jquery/jquery                │     60,000 │  21k   │ JavaScript │
└───┴──────────────────────────────┴────────────┴────────┴────────────┘
```

### 📝 `ara summary` — One-Line Repo Overview

```text
$ ara summary facebook/react
★ facebook/react · 226,000 stars · 47,000 forks · 1,200 issues · JavaScript · MIT License  —  A declarative UI library
```

### 🔔 `ara watch --notify` — Real-Time Monitoring + Desktop Notification

```text
$ ara watch --notify facebook/react

ARA Star Tracker v0.3.0
Watching 1 repo(s). Press Ctrl+C to stop.
🔔 Notification mode: you'll hear a beep when stars change.

┌ facebook/react ─────────────────────────────────────────────┐
│ ⭐ 226,000 stars                                             │
│ 🍴 47,000  forks                                             │
│ ⚠  1,200   issues                                            │
│ 📦 JavaScript                                                │
│ 📄 MIT License                                               │
└─────────────────────────────────────────────────────────────┘
✨ +3 new stars gained while watching!
```

### 📊 `ara dashboard` — Full Repo Overview

```text
$ ara dashboard facebook/react

╔══════════════════════════════════════╗
║  📊 ARA Dashboard                   ║
╟──────────────────────────────────────╢
║  🔥 facebook/react                   ║
║  ⭐ 226,000  stars                    ║
║  🍴 47,000   forks                    ║
║  ⚠  1,200    open issues              ║
║  📦 JavaScript                       ║
║  📄 MIT License                      ║
╚══════════════════════════════════════╝
```

---

## 🖼️ See It in Action ⚡

> **From a quick glance to deep analysis — get any repo's story in one command.**

### 1. `ara dashboard` — Full Repo Overview

```text
$ ara dashboard facebook/react

  facebook/react
  ─────────────────────────────────────────────────
    ★ Stars:      226,000
    🍴 Forks:      47,000
    ⚠  Issues:      1,200
    ──────────────────────────────
    📦 Language:   JavaScript
    📄 License:    MIT
    🕐  Updated:    2026-05-18
    📝 A declarative, efficient, and flexible JavaScript library...
```

### 2. `ara battle` — Repo Smackdown

```text
$ ara battle facebook/react vercel/next.js

╔════════════════════════════════════════════════╗
║           ★ REPO BATTLE ARENA ★               ║
╠════════════════════════════════════════════════╣
║                                                ║
║  facebook/react  ══════════▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 226,000 ★ ║
║  vercel/next.js  ══════════▓▓▓▓▓▓▓▓▓▓▓▓       139,500 ★ ║
║                                                ║
║  🏆 Winner: facebook/react by 86,500 stars!    ║
║                                                ║
╚════════════════════════════════════════════════╝
```

### 3. `ara watch` — Real-time Monitoring

```text
$ ara watch facebook/react

ARA Star Tracker v0.3.0
Watching 1 repo(s). Press Ctrl+C to stop.

╔═════════════════════════════════════╗
║          ★  ARA  WATCH  ★          ║
╠═════════════════════════════════════╣
║                                     ║
║  facebook/react                     ║
║  ★ Stars:      226,000  (+12 ▲🔥)  ║
║  🍴 Forks:      47,000  (+1  ▲)    ║
║  ⚠  Issues:      1,200  (-2  ▼)    ║
║  📦 Language:   JavaScript          ║
║  📄 License:    MIT                 ║
║  🕐  Updated:   30s ago             ║
║                                     ║
╚═════════════════════════════════════╝

  ⏱  Press Ctrl+C to stop — a summary will print.
```

> 💡 **Every command supports `--json`** — pipe into dashboards, CI, or `jq`.
>
> 🆕 **New in v0.3.0:** `ara rank` — live Top 10 repo leaderboard. Try `ara rank --top 20`!

---

## 🚀 Install in 5 seconds

```bash
pip install ara
```

**That's it.** No npm, no Docker, no `requirements.txt`, no config file. Just pure Python from the standard library.

> ⚙️ **Rate limits:** Unauthenticated = 60 req/h. Set `export GITHUB_TOKEN=ghp_...` for 5,000/h. ARA auto-retries on 429s with exponential backoff + jitter.

### Try it now — no install required

```bash
git clone https://github.com/lijiajing-11/alpha-project-arena.git
cd alpha-project-arena
python -m ara stars python/cpython
```

---

## 🔥 4 commands to get you hooked

| # | Command | What it does | Try it |
|---|---------|--------------|--------|
| 1 | `ara stars <repo>` | Quick star count + mini leaderboard | `ara stars python/cpython` |
| 2 | `ara battle <r1> <r2> <r3>` | Side-by-side ASCII arena showdown | `ara battle react vue svelte` |
| 3 | `ara watch <repo>` | Real-time dashboard (30s refresh) | `ara watch tensorflow/tensorflow` |
| 4 | `ara rank [--top N]` | Live Top N repo leaderboard 🔥 | `ara rank --top 10` |

Every command supports `--json` for piping into dashboards, CI pipelines, or `jq`.

---

## 📖 Commands

All 10 commands, sorted from quick-check to head-to-head analysis. Every command supports `--json`.

| Command | Description | Quick example |
|---------|-------------|---------------|
| 🆕 `ara summary <repo...>` | One-line repo summary (README-ready) | `ara summary owner/project` |
| 📊 `ara dashboard <repo...>` | Full repo overview panel | `ara dashboard owner/project` |
| 🔍 `ara stars <repo...>` | Quick star count(s) | `ara stars owner/project` |
| 👀 `ara watch <repo...>` | Real-time live watch (30s refresh) | `ara watch owner/project` |
| 🏟️ `ara battle <repo...>` | Arena bar-chart battle | `ara battle libA libB libC` |
| 🏆 `ara rank [--top N]` | Live Top N repo leaderboard 🔥 | `ara rank --top 10` |
| 📈 `ara trends <repo>` | Star trend chart over time | `ara trends owner/repo` |
| 📋 `ara info <repo...>` | Full repo metadata dump | `ara info owner/project` |
| 🛠️ `ara generate-stars <repo>` | Fetch stargazers to JSON (demo tool) | `ara generate-stars python/cpython` |
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
    { "full_name": "facebook/react", "stars": 230000, "forks": 48000, "open_issues": 1200, "language": "JavaScript", "license": "MIT" },
    { "full_name": "vuejs/core", "stars": 47000, "forks": 7000, "open_issues": 800, "language": "TypeScript", "license": "MIT" }
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

## 🖼️ Screenshots & Demos

### Arena Battle — 3-way showdown

```text
$ ara battle facebook/react vuejs/core sveltejs/svelte

  ╔══════════════════════════════════════════════════════════╗
  ║                    ★ ARENA BATTLE ★                     ║
  ║                                                          ║
  ║  facebook/react          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 230k ║
  ║  vuejs/core              ▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░  47k ║
  ║  sveltejs/svelte         ▓▓░░░░░░░░░░░░░░░░░░░░░░░  19k ║
  ║                                                          ║
  ║      ✦ facebook/react dominates the arena! ✦            ║
  ╚══════════════════════════════════════════════════════════╝
```

### Watch Dashboard — live monitoring

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
└────────────────────┴────────────────────────┘
```

> 🎥 **Want to contribute a proper GIF?** Record with `asciinema rec docs/ara-demo.cast` and convert with `agg docs/ara-demo.cast docs/ara-demo.gif` — then open a PR!

### Battle of the Titans — Live Leaderboard

```bash
# Top JavaScript frameworks
ara battle facebook/react vuejs/core sveltejs/svelte angular/angular preactjs/preact

# Top AI / ML repos
ara battle tensorflow/tensorflow pytorch/pytorch huggingface/transformers

# Feed the results into a dashboard
ara battle --json pytorch/pytorch tensorflow/tensorflow | jq '.winner'
# → "tensorflow/tensorflow"
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
| `ara/trends.py` | Star trend analysis + ASCII charts |
| `ara/generate_stars.py` | Stargazer JSON export |
| `ara/colors.py` | ANSI color constants |
| `ara/console.py` | Console entry point (`console_scripts`) |

```
alpha-project-arena/
├── ara/                  # Package source
│   ├── __init__.py       # Package init, __version__
│   ├── __main__.py       # Entry point for `python -m ara`
│   ├── cli.py            # CLI argument parser & all commands
│   ├── core.py           # Data models, cache, GitHub API client
│   ├── display.py        # Watch display formatting
│   ├── battle.py         # Battle display & ASCII bars
│   ├── trends.py         # Star trend analysis
│   ├── generate_stars.py # Stargazer JSON tool
│   ├── colors.py         # Shared ANSI colour constants
│   └── console.py        # Console entry point
├── tests/                # Test suite (pytest, 140+ tests)
├── scripts/
│   └── demo.py           # Demo output generator
├── docs/                 # Documentation & screenshots (coming soon)
├── setup.py              # Package metadata
├── pyproject.toml        # Build config
├── LICENSE               # MIT license
└── README.md             # ← You are here! 🎉
```

---

## 🔧 Development

```bash
# Clone + dev install
git clone https://github.com/lijiajing-11/alpha-project-arena.git
cd alpha-project-arena
python -m venv venv && source venv/bin/activate
pip install -e .

# Run the full test suite (140+ tests passing)
pytest tests/ -v

# Lint with ruff
ruff check .

# Generate demo output
python scripts/demo.py
```

> See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines, PR process, and the feature wishlist.

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

**Quick start for contributors:**

```bash
# Fork the repo first, then:
git clone https://github.com/your-username/alpha-project-arena.git
cd alpha-project-arena
python -m venv venv && source venv/bin/activate
pip install -e '.[dev]'
pytest tests/ -v      # 140+ tests should all pass
ruff check .          # zero warnings
```

> 📖 Full guide in [CONTRIBUTING.md](CONTRIBUTING.md) — PR guidelines, code style, testing, and the feature wishlist.

---

## 📝 License

MIT © [lijiajing-11](https://github.com/lijiajing-11) — see [LICENSE](LICENSE) for details.

---

## 🎯 Why ARA?

| You could... | Or just... |
|--------------|------------|
| 🕸️ Open GitHub every time → refresh, scroll, squint | `ara stars tensorflow/tensorflow` — 2 seconds |
| 📝 Tabulate 5 repos in a spreadsheet | `ara battle react vue svelte angular` — instant arena |
| 🔄 Manually check star trends | `ara watch pytorch/pytorch` — live dashboard auto-refreshes |
| 🔍 Google "most starred repos" | `ara rank --top 20` — live leaderboard from the terminal |

**ARA exists because you shouldn't need a browser to stalk repos.** 🔭

> 📋 See [CHANGELOG.md](CHANGELOG.md) for the full version history.

---

## 💬 Stay Connected

| Channel | Where | What for |
|---------|-------|----------|
| 🐙 **GitHub** | [alpha-project-arena](https://github.com/lijiajing-11/alpha-project-arena) | Issues, PRs, star history |
| 📦 **PyPI** | [`ara`](https://pypi.org/project/ara/) | `pip install ara` |
| 🐦 **X / Twitter** | [@ATechInc](https://x.com/ATechInc) | Announcements, teasers |
| 📧 **Email** | dev@alpha-project.dev | Direct feedback |
| ⭐ **Star us** | [Click here](https://github.com/lijiajing-11/alpha-project-arena) | Every star fuels the arena! |

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=lijiajing-11/alpha-project-arena&type=Date)](https://star-history.com/#lijiajing-11/alpha-project-arena&Date)

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
