
<p align="center">
  <img src="https://img.shields.io/badge/ARA-Arena%20Star%20Tracker-8A2BE2?style=for-the-badge&logo=github&logoColor=white" alt="ARA Banner"/>
</p>

<h1 align="center">⚡ ARA — Arena Star Tracker</h1>

<p align="center">
  <b>Zero‑dependency CLI that tracks, watches, compares, and battles GitHub repos — right from your terminal.</b><br>
  Think <i>Google Analytics for GitHub Stars</i>, but you never leave the command line.
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3.10+"/></a>
  <a href="https://pypi.org/project/ara/"><img src="https://img.shields.io/pypi/v/ara?style=flat&color=8A2BE2" alt="PyPI"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e?style=flat" alt="MIT"/></a>
  <a href="#"><img src="https://img.shields.io/github/stars/li1050109098/alpha-project?style=flat&label=stars&color=facc15" alt="Stars"/></a>
  <a href="https://github.com/li1050109098/alpha-project/actions"><img src="https://img.shields.io/github/actions/workflow/status/li1050109098/alpha-project/ci.yml?style=flat&label=CI&color=22c55e" alt="CI"/></a>
  <a href="#"><img src="https://img.shields.io/badge/status-alpha-f97316?style=flat" alt="Alpha"/></a>
  <a href="https://pypi.org/project/ara/"><img src="https://img.shields.io/pypi/dm/ara?style=flat&color=3b82f6" alt="Downloads"/></a>
  <br/>
  <a href="#-quick-start"><img src="https://img.shields.io/badge/▶️-Quick%20Start-22c55e?style=flat" alt="Quick Start"/></a>
  <a href="#-commands"><img src="https://img.shields.io/badge/📖-Commands-3b82f6?style=flat" alt="Commands"/></a>
  <a href="#-development"><img src="https://img.shields.io/badge/🧪-Development-8A2BE2?style=flat" alt="Development"/></a>
  <a href="#-contributing"><img src="https://img.shields.io/badge/🤝-Contributing-f97316?style=flat" alt="Contributing"/></a>
</p>

---

```text
┌─────────────────────────────────────────────┐
│  ⚡ ONE-LINER:                              │
│  ara stars tensorflow/tensorflow             │
│  → 187,634 ★                                │
│                                              │
│  No pip install? No problem.                 │
│  python -m ara stars owner/repo              │
│  → works. 🔥                                 │
└─────────────────────────────────────────────┘
```

---

## 🎯 What is ARA?

**ARA** is a pure‑Python CLI for monitoring GitHub stars in real time. No `requests`, no `httpx`, no `aiohttp` — just `urllib` from the standard library.

| Scenario                      | Why ARA?                                          |
|-------------------------------|---------------------------------------------------|
| 👀 **New release day**        | `ara watch owner/repo` — see stars roll in live   |
| 🏟️ **Shootout your stack**   | `ara battle react vue svelte` — who wins?         |
| 📋 **Due diligence**          | `ara info owner/repo` — stars, forks, license…    |
| 📊 **Side‑by‑side**           | `ara compare pytorch/pytorch tensorflow/tensorflow` |
| 🤖 **CI / scripting**         | `ara stars --json owner/repo` — pipe to jq         |

### ✨ Highlights

- **🍃 Zero external dependencies** — Pure Python 3.10+, stdlib only
- **⚡ Real‑time watching** — Live polling with colour‑coded deltas
- **🎨 Beautiful terminal output** — ANSI colours, box‑drawing tables, leaderboards
- **🏆 Arena Battle mode** — Side‑by‑side comparison with ASCII bar charts
- **🔍 Info & Compare** — Full repo metadata at a glance
- **📦 JSON output** — Every command supports `--json` for pipes and automation
- **⏳ Smart retry & caching** — Exponential backoff on rate limits, 60‑s TTL cache
- **🔧 Extensible** — Add new commands in one file

---

## 🚀 Quick Start

```bash
# ① Install globally
pip install ara

# ② Start tracking in 5 seconds
ara stars python/cpython

# ③ Real‑time watch
ara watch tensorflow/tensorflow

# ④ Arena battle!
ara battle facebook/react vuejs/core sveltejs/svelte
```

**That's it.** No config, no API tokens required.

> ⚠️ **Note:** Without a `GITHUB_TOKEN`, GitHub's unauthenticated API limit is **60 requests/hour**. Set `export GITHUB_TOKEN=ghp_xxx` for 5,000/hour.  
> ARA auto‑retries on 429s with exponential backoff + jitter, so even with the free tier you're covered.

**Prefer not to install?** Run directly from source:

```bash
git clone https://github.com/li1050109098/alpha-project.git
cd alpha-project
python -m ara stars python/cpython
```

---

## 📖 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ara stars <repo...>` | Get current star count(s) | `ara stars owner/project` |
| `ara watch <repo...>` | Watch repos in real‑time (30‑s refresh) | `ara watch owner/project` |
| `ara battle <repo...>` | Side‑by‑side bar‑chart battle | `ara battle teamA/lib teamB/lib` |
| `ara info <repo...>` | Detailed repo metadata | `ara info owner/project` |
| `ara compare <repo1> <repo2>` | Head‑to‑head comparison table | `ara compare a/A b/B` |

All commands support **`--json`** for machine‑readable output.

---

### `ara stars` — Quick check

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
# JSON mode
ara stars --json python/cpython tensorflow/tensorflow
```

---

### `ara watch` — Real‑time monitoring

```text
$ ara watch python/cpython

  ARA Star Tracker v0.1.0
  Watching 1 repo(s). Press Ctrl+C to stop.

  ╔══ ARA Multi-Watch @ 14:32:01 ══╗
  ║  python/cpython               ★ 63,475  (0)
  ╚══════════════════════════════════╝
```

Press `Ctrl+C` to stop and see a session summary with final counts.

```bash
# JSON tick stream (one line per tick)
ara watch --json python/cpython
```

---

### `ara battle` — Arena showdown

```text
$ ara battle facebook/react vuejs/core

  ╔══════════════════════════════════════════╗
  ║          ★ ARENA BATTLE ★               ║
  ║                                          ║
  ║  ★ facebook/react                        ║
  ║    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 230,000 ★      ║
  ║                                          ║
  ║  ★ vuejs/core                            ║
  ║    ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░ 47,000 ★        ║
  ║                                          ║
  ║  ✦ facebook/react dominates the arena! ✦ ║
  ╚══════════════════════════════════════════╝
```

```bash
# JSON winner declaration
ara battle --json facebook/react vuejs/core
```

---

### `ara info` — Repository details

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
# JSON
ara info --json python/cpython
```

---

### `ara compare` — Head‑to‑head

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

---

## 🔧 Development

```bash
# Clone & go
git clone https://github.com/li1050109098/alpha-project.git
cd alpha-project

# Create venv & install editable
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Run tests (90+ passing)
python -m pytest tests/ -v

# Run a single test file
python -m pytest tests/test_core.py -v
```

### Project Structure

```
alpha-project/
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
├── setup.py              # Package metadata
├── LICENSE               # MIT license
└── README.md             # ← You are here! 🎉
```

---

## ⏳ Rate Limits & Reliability

| Auth | Limit | Note |
|------|-------|------|
| None | 60 req/h | Fine for casual use |
| Token | 5,000 req/h | Set `export GITHUB_TOKEN=ghp_xxx` |

ARA automatically **retries** on rate limits (429), server errors (5xx), and transient network failures using exponential backoff with jitter. Results are cached for **60 seconds** to minimise unnecessary API calls.

---

## 🤝 Contributing

All contributions welcome — code, docs, ideas, or bug reports!

1. 🍴 **Fork** the repo
2. 🌿 `git checkout -b feat/your-idea`
3. 🛠️ Make your changes
4. ✅ `python -m pytest tests/ -v` — keep the suite green
5. 📬 Open a **Pull Request** against `main`

**Ideas to run with:**
- Web UI / dashboard
- Slack & Discord webhook integration
- Historical star charts (daily snapshots → plot)
- GitHub Action badge generator from ARA data
- Export to CSV / JSON / Markdown
- Private repo support (token‑authed)
- `ara trend` — find fast‑growing repos in a topic

---

## 📝 License

MIT © [li1050109098](https://github.com/li1050109098)

---

<p align="center">
  <sub>Built with ❤️ by <b>Α-Tech Inc.</b> — <i>"Watch, Compete, Win."</i></sub>
  <br>
  <sub><a href="https://github.com/li1050109098/alpha-project">GitHub</a> · <a href="https://pypi.org/project/ara/">PyPI</a> · <a href="https://github.com/li1050109098/alpha-project/issues">Issues</a></sub>
</p>
