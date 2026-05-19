
<p align="center">
  <img src="https://img.shields.io/badge/ARA-Arena%20Star%20Tracker-8A2BE2?style=for-the-badge&logo=github&logoColor=white" alt="ARA Banner"/>
</p>

<h1 align="center">⚡ ARA — Arena Star Tracker</h1>

<p align="center">
  <b>Track GitHub Stars from your terminal. Compare repos. Win the arena.</b>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3.10+"/></a>
  <a href="#"><img src="https://img.shields.io/badge/version-v0.1.0--alpha-8A2BE2?style=flat" alt="Version"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e?style=flat" alt="MIT"/></a>
  <a href="#"><img src="https://img.shields.io/github/stars/li1050109098/alpha-project?style=flat&label=stars&color=facc15" alt="Stars"/></a>
  <a href="#"><img src="https://img.shields.io/badge/status-alpha-f97316?style=flat" alt="Alpha"/></a>
  <br/>
  <a href="#-quick-start"><img src="https://img.shields.io/badge/▶️-Quick%20Start-22c55e?style=flat" alt="Quick Start"/></a>
  <a href="#-commands"><img src="https://img.shields.io/badge/📖-Commands-3b82f6?style=flat" alt="Commands"/></a>
  <a href="#-development"><img src="https://img.shields.io/badge/🧪-Development-8A2BE2?style=flat" alt="Development"/></a>
</p>

---

## 🎯 What is ARA?

**ARA** is a sleek CLI tool that monitors **GitHub Stars** in real-time from your terminal.

```bash
# Get star counts instantly
ara stars tensorflow/tensorflow

# Watch a repo grow in real-time
ara watch python/cpython

# Compare repos head-to-head
ara battle facebook/react vuejs/core
```

### ✨ Highlights

- **🍃 Zero external dependencies** — Pure Python 3.10+, stdlib only
- **⚡ Real-time watching** — Live polling with color-coded deltas
- **🎨 Beautiful terminal output** — ANSI colors, ASCII art, emoji indicators
- **🏆 Arena Battle mode** — Side-by-side comparison with winner declaration
- **📊 Smart retry & caching** — Exponential backoff on rate limits, 60s TTL cache
- **🔧 Extensible** — Easy to add new commands

---

## 🚀 Quick Start

```bash
# Clone and run (no install needed)
git clone https://github.com/li1050109098/alpha-project.git
cd alpha-project
python -m ara stars python/cpython
```

**That's it.** No pip install, no config, no API tokens needed.

> ⚠️ **Note:** Without a `GITHUB_TOKEN`, GitHub's unauthenticated API limit is **60 requests per hour**. Set `export GITHUB_TOKEN=ghp_xxx` for 5,000/hr.

---

## 📖 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ara stars <repo...>` | Get current star count for one or more repos | `ara stars owner/project` |
| `ara watch <repo...>` | Watch repos in real-time (auto-refresh every 30s) | `ara watch owner/project` |
| `ara battle <repo...>` | Compare repos side-by-side, winner declared | `ara battle teamA/lib teamB/lib` |

### `ara stars` — Quick check

```
$ python -m ara stars python/cpython tensorflow/tensorflow

  ★ python/cpython: 63,475 stars
  ★ tensorflow/tensorflow: 187,634 stars
```

With multiple repos, a mini leaderboard is shown:

```
  🥇 tensorflow/tensorflow         187,634 ★
  🥈 python/cpython                  63,475 ★
```

### `ara watch` — Real-time monitoring

```
$ python -m ara watch python/cpython

╔══ ARA Multi-Watch @ 14:32:01 ══╗
║  python/cpython               ★ 63,475  (0)
╚══════════════════════════════════╝
```

Press `Ctrl+C` to stop and see a session summary.

### `ara battle` — Arena showdown

```
$ python -m ara battle facebook/react vuejs/core

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

---

## 🔧 Development

```bash
# Clone
git clone https://github.com/li1050109098/alpha-project.git
cd alpha-project

# Run directly (no install)
python -m ara stars owner/project

# Install for `ara` command
pip install -e .

# Run tests
python -m pytest tests/ -v
```

### Project Structure

```
alpha-project/
├── ara/                  # Package source
│   ├── __init__.py       # Package init, __version__
│   ├── __main__.py       # Entry point for `python -m ara`
│   ├── cli.py            # CLI argument parser & all commands
│   ├── core.py           # Data models, cache, GitHub API client with retry
│   ├── display.py        # Watch display formatting
│   ├── battle.py         # Battle display & ASCII bars
│   ├── colors.py         # Shared ANSI color constants
│   └── console.py        # Console entry point
├── tests/                # Test suite (pytest, 90+ tests)
│   ├── conftest.py       # Path setup
│   ├── test_cli.py       # CLI command tests
│   ├── test_core.py      # Cache, models, API client tests
│   ├── test_battle.py    # Battle display tests
│   └── test_watch.py     # Watch display tests
├── scripts/
│   └── demo.py           # Demo output generator
├── setup.py              # Package metadata
├── LICENSE               # MIT license
└── README.md             # You are here! 🎉
```

---

## ☁️ Rate Limits & Reliability

| Auth | Limit | Note |
|------|-------|------|
| None | 60 req/hr | Fine for casual use |
| Token | 5,000 req/hr | Set `GITHUB_TOKEN=ghp_xxx` |

ARA automatically **retries** on rate limits (429), server errors (5xx), and transient network failures using exponential backoff with jitter. Results are cached for **60 seconds** to minimize unnecessary API calls.

---

## 🤝 Contributing

All contributions welcome!

1. 🍴 Fork the repo
2. 🌿 `git checkout -b feat/your-idea`
3. 🛠️ Make changes
4. ✅ `python -m pytest tests/ -v` (make sure tests pass)
5. 📬 Open a Pull Request

**Ideas:** Web UI, Slack/Discord integration, historical charts, GitHub Action badge generator, export to CSV/JSON, private repo support.

---

## 📝 License

MIT © [li1050109098](https://github.com/li1050109098)

---

<p align="center">
  <sub>Built with ❤️ by <b>Α-Tech Inc.</b> — <i>"Watch, Compete, Win."</i></sub>
</p>
