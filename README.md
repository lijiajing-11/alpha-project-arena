<div align="center">

# ⚡ ARA — GitHub 仓库分析利器

> **中文** | [English ↓](#english-version)

**实时追踪、PK 对比、深度分析任何 GitHub 仓库 — 全在终端里完成。**  
*零依赖 · 一条命令 · 实时刷新 · 无需浏览器*

</div>

---

<a name="english-version"></a>

<h1 align="center">⚡ ARA — Arena Star Tracker</h1>

<p align="center">
  <b>Track, watch, battle, and compare any GitHub repo — right from your terminal.</b><br>
  <i>Zero dependencies. One command. Real-time. No browser needed.</i>
</p>

<p align="center">
  <a href="https://github.com/lijiajing-11/alpha-project-arena/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/lijiajing-11/alpha-project-arena/ci.yml?style=for-the-badge&logo=githubactions&label=CI" alt="CI"/>
  </a>
  <a href="https://github.com/lijiajing-11/alpha-project-arena">
    <img src="https://img.shields.io/github/stars/lijiajing-11/alpha-project-arena?style=for-the-badge&logo=github&color=gold" alt="Stars"/>
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+"/>
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT"/>
  </a>
  <a href="https://pypi.org/project/ara/">
    <img src="https://img.shields.io/pypi/v/ara?style=for-the-badge&logo=pypi&color=blue" alt="PyPI"/>
  </a>
  <a href="http://makeapullrequest.com">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge" alt="PRs Welcome"/>
  </a>
</p>

<p align="center">
  <sub><b>v0.3.2</b> · 13 commands · 16 modules · 276+ tests · stdlib-only</sub>
</p>

---

## 👀 What Is ARA?

Ever caught yourself opening 5 browser tabs to compare GitHub repos?  
Or refreshing a repo page every hour to watch its star count grow?

**ARA is the antidote.**

A single Python CLI that puts GitHub's pulse in your terminal — star counts,
growth velocity, head-to-head battles, live watches, and ranked leaderboards.
All from one command. No browser scrolling. No context switching.

```bash
# 2 seconds. One command. Done.
pip install ara
ara stars tensorflow/tensorflow
```

> **Think of it as `htop` for GitHub.** 🖥️

---

## 🚀 Install in 5 Seconds

```bash
pip install ara
```

**That's it.** No npm, no Docker, no config file. Pure Python from the standard library.

> ⚙️ **Rate limits:** Unauthenticated = 60 req/h. Set `export GITHUB_TOKEN=ghp_...` for 5,000/h.
> ARA auto-retries on 429s with exponential backoff + jitter.

```bash
# Clone and run directly — zero dependency setup.
git clone https://github.com/lijiajing-11/alpha-project-arena.git
cd alpha-project-arena
python -m ara stars python/cpython
```

---

## ⚡ 3 Commands to Get Hooked

```bash
# 1. Quick star check — 2 seconds, zero fuss
ara stars python/cpython
# → ★ python/cpython: 63,475 stars

# 2. Pit frameworks against each other — ASCII arena showdown
ara battle facebook/react vuejs/core sveltejs/svelte
# → React dominates with 230,000 ★ — Vue trails at 47,000

# 3. Watch a repo live (30s auto-refresh with desktop notifications)
ara watch --notify tensorflow/tensorflow
# → Live dashboard: stars, forks, issues — colour-coded deltas
```

Every command supports `--json` for CI pipelines, dashboards, and `jq` piping.

---

## 🎬 In Action — See It in Under 10 Seconds

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

### 📡 `ara watch` — Real-Time Dashboard

```text
$ ara watch tensorflow/tensorflow

╔════════════════════════════════════════════╗
║        📡 ARA Star Tracker — WATCH         ║
╚════════════════════════════════════════════╝
┌────────────────────┬────────────────────────┐
│ Repository         │ tensorflow/tensorflow   │
├────────────────────┼────────────────────────┤
│ ⭐ Stars           │ 187,634  (+5)           │
│ ⑂ Forks            │ 78,234   (+1)           │
│ ⚠ Issues           │ 1,200    (-2)           │
│ 🔤 Language        │ Python                  │
│ 📜 License         │ Apache 2.0              │
│ 🕐 Updated         │ 2026-05-19 14:30:22     │
└────────────────────┴────────────────────────┘
```

### 🧠 `ara insight` — Deep Repository Intelligence

```text
  facebook/react  — Insight
  A declarative UI library

  ★ 226,000 stars  ·  46.2/day  🔥 Hypersonic
  ⑂ 47,000 forks  ·  ⚠ 1,200 open issues
  ⎆ JavaScript  ·  © MIT
  🏷  react, ui, javascript, declarative, frontend
  📅 Created 2013-05-29  ·  Last updated 2 hours ago
```

**NEW — Multi-repo `ara insight repo1 repo2 repo3 ...`** — compare up to N repos side-by-side with community **Influence Score**:

```text
$ ara insight facebook/react vuejs/core sveltejs/svelte

  facebook/react                           │  vuejs/core                              │  sveltejs/svelte
  A declarative UI library                 │  🖖 Vue.js is a progressive...            │  Cybernetically enhanced web apps
                                           │                                           │
  ★ 226,000 stars · +62.8/day  🚀 Hyp...   │  ★ 47,000 stars · +19.5/day  🔥 Rapid    │  ★ 18,000 stars · +7.2/day  📊 Steady
  ⎊ 47,000 forks · ☠ 1,200 open issues     │  ⎊ 7,000 forks · ☠ 800 open issues        │  ⎊ 1,200 forks · ☠ 400 open issues
  ⎆ JavaScript · © MIT · 📅 13yo Veteran   │  ⎆ TypeScript · © MIT · 📅 6.4yo Prime   │  ⎆ TypeScript · © MIT · 📅 8.1yo Veteran
  🏷  React · Ui · Javascript · Decl...     │  🏷  Vue · Typescript · Frontend          │  🏷  Svelte · Javascript · Compiler

  ════════════════════════════════════════════  COMPARISON  ═════════════════════════════════════════════

  ★ Top: facebook/react (226,000 ★)
  📈 Influence Ranking:
    🥇 facebook/react                        129.40  (High)
    🥈 vuejs/core                             27.80  (Moderate)
    🥉 sveltejs/svelte                        10.55  (Moderate)
  ⚡ Average velocity: 29.8 stars/day
  📅 Youngest: vuejs/core (6.4yo)
```

### 📈 `ara history` — Star Growth Timeline

```text
  ★ facebook/react — Star History
    245,114 stars total

    │                    ●●
    │                   ●●●
    │                 ●●●●●
    │                ●●●●●●
    │              ●●●●●●●●
    │            ●●●●●●●●●●
    │          ●●●●●●●●●●●●
    │        ●●●●●●●●●●●●●●
    │      ●●●●●●●●●●●●●●●●
    │ ●●●●●●●●●●●●●●●●●●●●●
    └─────────────────────
     2013-05-24   2026-05-18
```

### 🆚 `ara history --compare` — Multi-Repo Showdown

```text
$ ara history --compare facebook/react vuejs/core sveltejs/svelte

  ╔══════════════════════════════════════════╗
  ║     ⭐ Star History Comparison (all-time) ║
  ╚══════════════════════════════════════════╝

  facebook/react            ██████████████████████████████████████████████████ 230,000 ★
  vuejs/core                ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  47,000 ★
  sveltejs/svelte           ██████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  82,000 ★

  📅 Timeline: 2013-05-29 — 2026-05-19
```

---

## 📖 Full Command Reference

| Command | Description | Quick example |
|---------|-------------|---------------|
| 🆕 `ara summary <repo>` | One-line repo summary (README-ready) | `ara summary owner/project` |
| 📊 `ara dashboard <repo...>` | Full repo overview panel | `ara dashboard owner/project` |
| 🔍 `ara stars <repo...>` | Quick star count(s) | `ara stars owner/project` |
| 👀 `ara watch <repo...>` | Real-time live watch (30s refresh) | `ara watch owner/project` |
| 👀 `ara watch --alert <condition>` | Live watch + alert when condition met | `ara watch owner/proj --alert "velocity > 50"` |
| 📄 **`ara report <repo>`** | **Generate Markdown/HTML report** | **`ara report owner/proj --format md`** |
| 📈 `ara history <repo>` | Star growth ASCII timeline chart | `ara history owner/project` |
| 📈 `ara history --compare <repo...>` | Multi-repo star history comparison (coloured bars) | `ara history --compare react vue svelte` |
| 🏟️ `ara battle <repo...>` | Arena bar-chart battle | `ara battle libA libB libC` |
| 🏆 `ara rank [--top N]` | Live Top N repo leaderboard 🔥 | `ara rank --top 10` |
| 📈 `ara trends <repo>` | Star trend chart over time | `ara trends owner/repo` |
| 📋 `ara info <repo...>` | Full repo metadata dump | `ara info owner/project` |
|| 🧠 `ara insight <repo...>` | Deep insight — star velocity, topics, age + N-repo compare with Influence Score | `ara insight owner/proj1 owner/proj2 owner/proj3` |
| 🛠️ `ara generate-stars <repo>` | Fetch stargazers to JSON (demo tool) | `ara generate-stars python/cpython` |
| ⚖️ `ara compare <r1> <r2>` | Head-to-head comparison table | `ara compare a/A b/B` |

> 💡 **New in v0.4.0:** `ara report <repo>` — generate Markdown/HTML reports. `ara watch --alert <condition>` — threshold alerting for stars, forks, velocity.
> Terminal bell + plyer desktop notification with graceful fallback on WSL.
>
> 🚀 **New in v0.4.0:** `ara insight repo1 repo2 repo3 ...` — **multi-repo comparison** with community **Influence Score** (Stars×0.5 + Forks×0.3 + Issues×0.2 / 1000). Up to N repos, side-by-side, ranked by influence.
>
> 🆕 **v0.3.0:** `ara rank` — live Top 10 repo leaderboard. Try `ara rank --top 20`!
>
> 🆕 **Hot off the press:** `ara insight` — star velocity, topics, age, and more.

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

### 👀 `ara watch` — Real-Time Dashboard

Watch a single repo with a **multi-field dashboard** — stars, forks, issues, language, license, and color-coded deltas. Press `Ctrl+C` to stop.
Add `--notify` to receive desktop notifications when star count changes.

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

```

### 📄 `ara report` — One-Command README-Ready Report

Generate a full Markdown report (ready to paste into README or article) or an HTML snippet (ready to embed in a webpage).

```text
$ ara report facebook/react --format md

# 📊 facebook/react
> The library for web and native user interfaces.

| ⭐ Stars          | 245,363  | 🚀 Star Velocity   | 51.6/day (🚀 Hypersonic) |
| 📅 Created        | 2013-05  | 🏆 Influence Score | 138.3                    |
| 🍴 Forks          | 51,147   | 🐛 Open Issues     | 1,308                    |
```

```bash
# Save HTML snippet to file
ara report facebook/react --format html --output react-card.html

# Generate Markdown and pipe to clipboard
ara report facebook/react --format md | pbcopy   # macOS
ara report facebook/react --format md | clip      # Windows
```

> 💡 **Use case:** Write a tech article. Run `ara report owner/repo --format md`. Paste the output. Done.

### 👀 `ara watch --alert` — Threshold Alerting

```bash
# Alert when star velocity exceeds 50/day
ara watch facebook/react --alert "velocity > 50"
# 🚨 ALERT: facebook/react velocity(51.6/day) > 50

# Alert when total stars exceed 200K
ara watch facebook/react --alert "stars > 200000"
# 🚨 ALERT: facebook/react stars(245363.0) > 200000

# Alert when a small project breaks into 4-digit stars
ara watch your-new-project/repo --alert "stars > 1000"
```

Triggered alerts fire once (no repeat spam) + desktop notification when available.

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

### 📦 JSON Output — Pipe into Everything

Every ARA command accepts `--json` for machine-readable output — perfect for CI pipelines, dashboards, and scripts:

| Command | JSON flag | What you get |
|---------|-----------|--------------|
| `ara stars --json owner/repo` | ✅ | Array of `{repo, stars}` objects |
| `ara summary --json owner/repo` | ✅ | One-line summary with `{name, stars, language, description}` |
| `ara rank --json` | ✅ | Leaderboard as sorted array with rank, stars, forks |
| `ara watch --json owner/repo` | ✅ | One JSON object per 30s tick |
| `ara battle --json owner/a owner/b` | ✅ | Battle results with `winner` field |
| `ara compare --json owner/a owner/b` | ✅ | Full comparison with `winner`, `lead_by`, `fork_leader` |
| `ara trends --json owner/repo` | ✅ | Trend data with `buckets`, `total`, `best_hour` |
| `ara info --json owner/repo` | ✅ | Full repo metadata as JSON |
| `ara history --json owner/repo` | ✅ | Timeline array with `current_stars`, `created_at` |
| `ara history --compare --json <repos>` | ✅ | Dict of repos → timeline arrays |

```bash
# Example: pipe to jq for quick analysis
ara compare --json facebook/react vuejs/core | jq '.winner'
# Output: "facebook/react"
```

> 🎥 **Want to contribute a proper GIF?** Record with `asciinema rec docs/ara-demo.cast` and convert with `agg docs/ara-demo.cast docs/ara-demo.gif` — then open a PR!

---

## 🏗️ Architecture

ARA is designed as a **single-file-per-responsibility** Python package — no framework, no wiring, no over-engineering.

| Module | Responsibility |
|--------|---------------|
| `ara/__init__.py` | Package init, `__version__` |
| `ara/__main__.py` | Entry point for `python -m ara` |
| `ara/cli.py` | Argument parsing + command dispatch (13 commands) |
| `ara/core.py` | GitHub API client, cache, data models |
| `ara/summary.py` | One-line repo overview |
| `ara/dashboard.py` | Full repo overview panel |
| `ara/rank.py` | Top N repo leaderboard |
| `ara/insight.py` | Deep repo intelligence (star velocity, topics) |
| `ara/display.py` | Live watch terminal UI, formatting |
| `ara/battle.py` | Arena battle ASCII bars |
| `ara/trends.py` | Star trend analysis + ASCII charts |
| `ara/history.py` | Star growth ASCII timeline chart |
| `ara/generate_stars.py` | Stargazer JSON export |
| `ara/chart.py` | Shared ASCII chart engine (bars, sparklines) |
| `ara/colors.py` | ANSI color constants |
| `ara/console.py` | Console entry point (`console_scripts`) |
| **Total** | **16 modules** — pure Python, zero framework |

```
alpha-project-arena/
├── ara/                  # Package source
│   ├── __init__.py       # Package init, __version__
│   ├── __main__.py       # Entry point for `python -m ara`
│   ├── cli.py            # CLI argument parser & all commands
│   ├── core.py           # Data models, cache, GitHub API client
│   ├── display.py        # Watch display formatting
│   ├── summary.py        # One-line repo overview
│   ├── dashboard.py      # Full repo overview panel
│   ├── rank.py           # Top N repo leaderboard
│   ├── insight.py        # Deep repo intelligence
│   ├── battle.py         # Battle display & ASCII bars
│   ├── *compare in cli.py* # Head-to-head comparison
│   ├── trends.py         # Star trend analysis
│   ├── history.py        # Star growth timeline chart
│   ├── chart.py          # Shared ASCII chart engine
│   ├── generate_stars.py # Stargazer JSON tool
│   ├── colors.py         # Shared ANSI colour constants
│   └── console.py        # Console entry point
├── tests/                # Test suite (pytest, 276+ tests)
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
pip install -e '.[dev]'

# Run the full test suite (276+ tests passing)
pytest tests/ -v

# Lint with ruff
ruff check ara/ tests/

# Generate demo output
python scripts/demo.py
```

> ✅ **Pre-commit checklist:** `pytest tests/ -q && ruff check ara/ tests/` — both should pass clean.
>
> See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines, PR process, and the feature wishlist.

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

## 🤝 Contributing

All contributions welcome — code, docs, ideas, or bug reports!

**Quick start for contributors:**

```bash
# Fork the repo first, then:
git clone https://github.com/your-username/alpha-project-arena.git
cd alpha-project-arena
python -m venv venv && source venv/bin/activate
pip install -e '.[dev]'
pytest tests/ -v      # 276+ tests should all pass
ruff check ara/ tests/ # zero warnings
```

> 📖 Full guide in [CONTRIBUTING.md](CONTRIBUTING.md) — PR guidelines, code style, testing, and the feature wishlist.
>
> 💡 **New to open source?** Start with a `good first issue` — we label them for easy pickings.
> Found a bug? Open an issue before sending a PR so we can discuss the approach.

---

## 👤 Who Should Use ARA?

| You are… | And you… | ARA is for you ✅ |
|-----------|----------|-------------------|
| 🐱 **Open-source maintainer** | Watch your star count hourly | `ara watch your/repo --notify` — live dashboard + desktop alerts |
| 📊 **Tech journalist / analyst** | Compare repos for a write-up | `ara battle react vue svelte` — instant chart |
| 🎯 **Investor / scout** | Track which projects are heating up | `ara rank --top 50` — pulse of GitHub |
| 🛠️ **CI pipeline** | Need star data in your dashboard | `ara stars --json owner/repo \| jq` |
| 🧑‍💻 **Curious dev** | Just want to know "is this repo popular?" | `ara summary facebook/react` — 1 line answer |

> **tl;dr** — If you breathe repos, ARA is your pulse check. One command, zero clicks. No browser needed.

---

## ⏳ Rate Limits & Reliability

<details>
<summary>Click to expand</summary>

| Auth | Limit | Setup |
|------|-------|-------|
| None | 60 req/h | Just works — fine for casual use |
| Token | 5,000 req/h | `export GITHUB_TOKEN=ghp_...` |

ARA automatically **retries** on rate limits (429), server errors (5xx), and transient network failures using exponential backoff with jitter. Results are cached for **60 seconds** to minimize unnecessary API calls.

### Feature Matrix

| Feature | Status | Notes |
|---------|--------|-------|
| `ara stars` | ✅ | Quick star count(s) |
| `ara summary` | ✅ | One-line repo overview |
| `ara dashboard` | ✅ | Full repo overview panel |
| `ara info` | ✅ | Full repo metadata dump |
| `ara rank` | ✅ | Live Top N repo leaderboard |
| `ara battle` | ✅ | Arena bar-chart showdown |
| `ara compare` | ✅ | Head-to-head comparison table |
| `ara watch` | ✅ | Real-time live dashboard (30s refresh) |
| `ara watch --alert` | ✅ | Threshold alerting (stars, forks, velocity) | | `ara report` | ✅ | Generate Markdown/HTML reports |
| `ara history` | ✅ | Star growth ASCII timeline chart |
| `ara history --compare` | ✅ | Multi-repo star history comparison |
| `ara trends` | ✅ | Star trend analysis over time |
| `ara insight` | ✅ | Deep repo intelligence |
| `ara generate-stars` | ✅ | Stargazer JSON export tool |
| `--json` support | ✅ | Every command pipes to jq |
| **Total commands** | **13** | `ara --help` to see them all |
| **Test suite** | ✅ | **276+ passing, 0 failed** |
| **Coverage report** | 🟢 | HTML report via `coverage html` |
| **Zero dependencies** | ✅ | Stdlib only + optional `plyer` |
| **Rate-limit retry** | ✅ | Exponential backoff + jitter |

</details>

---

## 📝 License

MIT © [lijiajing-11](https://github.com/lijiajing-11) — see [LICENSE](LICENSE) for details.

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
