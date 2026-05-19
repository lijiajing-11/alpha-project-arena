<p align="center">
  <img src="https://img.shields.io/badge/⚡_ARA-Arena_Star_Tracker-8A2BE2?style=for-the-badge" alt="ARA Banner"/>
</p>

<h1 align="center">⚡ ARA — Arena Star Tracker</h1>

<p align="center">
  <b>Zero-dependency CLI that tracks, watches, compares, and battles GitHub repos — right from your terminal.</b><br>
  <i>Think Google Analytics for GitHub Stars, but you never leave the command line.</i>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10+"/></a>
  <a href="https://pypi.org/project/ara/"><img src="https://img.shields.io/pypi/v/ara?color=8A2BE2" alt="PyPI"/></a>
  <a href="https://pypi.org/project/ara/"><img src="https://img.shields.io/pypi/dm/ara?color=3b82f6" alt="Downloads"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e" alt="MIT"/></a>
  <a href="#"><img src="https://img.shields.io/github/stars/lijiajing-11/alpha-project-arena?label=stars&color=facc15" alt="Stars"/></a>
  <a href="https://github.com/lijiajing-11/alpha-project-arena/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/lijiajing-11/alpha-project-arena/ci.yml?label=CI&color=22c55e" alt="CI"/></a>
  <a href="#"><img src="https://img.shields.io/badge/status-alpha-f97316" alt="Status"/></a>
  <a href="#"><img src="https://img.shields.io/github/languages/top/lijiajing-11/alpha-project-arena?color=blueviolet" alt="Language"/></a>
  <a href="#"><img src="https://img.shields.io/badge/OS-linux_%7C_macOS_%7C_windows-555" alt="OS"/></a>
  <br/>
  <a href="#"><img src="https://img.shields.io/github/issues/lijiajing-11/alpha-project-arena?label=issues" alt="Issues"/></a>
  <a href="#"><img src="https://img.shields.io/github/last-commit/lijiajing-11/alpha-project-arena?label=updated" alt="Last Commit"/></a>
  <a href="#"><img src="https://img.shields.io/badge/code%20style-ruff-9749eb" alt="Code Style"/></a>
  <a href="#"><img src="https://img.shields.io/badge/tests-90%2B-22c55e" alt="Tests"/></a>
  <a href="#"><img src="https://img.shields.io/badge/PRs-welcome-22c55e" alt="PRs Welcome"/></a>
  <a href="#"><img src="https://img.shields.io/badge/🐦-follow_%40ATechInc-1DA1F2" alt="Twitter"/></a>
</p>

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
```

> 💡 **Tip:** Run `ara --help` anytime to see all available commands and flags.

### Run Without Installing

```bash
git clone https://github.com/lijiajing-11/alpha-project-arena.git
cd alpha-project-arena
python -m ara stars python/cpython
```

---

## 📖 Commands

Five commands, sorted from quick-check to head-to-head analysis. Every command supports `--json`.

| Command | Description | Quick example |
|---------|-------------|---------------|
| 🔍 `ara stars <repo...>` | Quick star count(s) | `ara stars owner/project` |
| 👀 `ara watch <repo...>` | Real-time live watch (30s refresh) | `ara watch owner/project` |
| 🏟️ `ara battle <repo...>` | Arena bar-chart battle | `ara battle libA libB libC` |
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

### 👀 `ara watch` — Real-Time Monitoring

```text
$ ara watch python/cpython

  ARA Star Tracker v0.1.0
  Watching 1 repo(s). Press Ctrl+C to stop.

  ╔══ ARA Multi-Watch @ 14:32:01 ══╗
  ║  python/cpython               ★ 63,475  (0)
  ╚══════════════════════════════════╝
```

Press `Ctrl+C` to stop — ARA prints a session summary with final counts and elapsed time.

```bash
# One JSON tick per line, pipe to your own dashboard
ara watch --json python/cpython
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
  └─────────────┴──────────────────┴──────────────────┴────────┘

  🏆 facebook/react WINS!
     Leads by 183,000 stars over vuejs/core
```

```bash
ara compare --json facebook/react vuejs/core
```

---

## 🖼️ Screenshots

<!-- TODO: Replace with real terminal capture -->

```
  ╔══════════════════════════════════════════╗
  ║          ★ ARENA BATTLE ★               ║
  ║                                          ║
  ║  ★ facebook/react         ▓▓▓▓▓▓▓▓      ║
  ║  ★ vuejs/core             ▓▓░░░░░░      ║
  ║                                          ║
  ║  ✦ react dominates!                     ║
  ╚══════════════════════════════════════════╝
```

> 🎥 **Want to contribute a screenshot?** Record one with `asciinema rec docs/ara-demo.cast` and convert to GIF with `agg`. Drop the `.gif` in `docs/` and update this section!

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

**Ideas to run with:**

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
  <a href="https://twitter.com/ATechInc">Twitter/X</a>
  <br/><br/>
  <sub>⭐ Star us on GitHub — every star feeds the arena! ⭐</sub>
</p>
