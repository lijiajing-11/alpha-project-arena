
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

# Compare two repos head-to-head
ara battle facebook/react vuejs/core

# Get detailed repo info
ara info rust-lang/rust
```

### ✨ Highlights

- **🍃 Zero external dependencies** — Pure Python 3.10+, stdlib only
- **⚡ Real-time watching** — Live polling with color-coded deltas
- **🎨 Beautiful terminal output** — ANSI colors, ASCII art, emoji indicators
- **🏆 Arena Battle mode** — Side-by-side comparison with winner declaration
- **📊 Rate-limit aware** — Caches results, shows remaining API calls
- **🔧 Extensible** — Info, leaderboard, and more commands coming

### 🏁 Who's it for?

Indie devs launching a new OSS project, startup teams tracking their GitHub presence, hackathon participants, and anyone who loves watching those ⭐ numbers climb.

---

## 🚀 Quick Start

```bash
# Clone and run (no install needed)
git clone https://github.com/li1050109098/alpha-project.git
cd alpha-project
python -m ara stars python/cpython
```

**That's it.** No pip install. No config files. No API tokens. No databases. Two commands and you're tracking Stars.

> ⚠️ **Note:** Without a `GITHUB_TOKEN` environment variable, GitHub's unauthenticated API limit is **60 requests per hour**. Set `export GITHUB_TOKEN=ghp_xxx` in your shell for 5,000/hr.

---

## 📖 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ara stars <repo...>` | Get current star count for one or more repos | `ara stars owner/project` |
| `ara watch <repo...>` | Watch repos in real-time (auto-refresh) | `ara watch owner/project -i 10` |
| `ara battle <repo...>` | Compare repos side-by-side, winner declared | `ara battle teamA/lib teamB/lib` |
| `ara info <repo>` | Show detailed repo info (stars, forks, language) | `ara info owner/project` |
| `ara leaderboard` | Show ranked leaderboard of tracked repos | `ara leaderboard` |

### `ara stars` — Quick check

```
$ python -m ara stars python/cpython tensorflow/tensorflow

    ╔══════════════════════════════════════════════╗
    ║               ★  A R A  ★                   ║
    ║          Arena Star Tracker v0.1.0            ║
    ╚══════════════════════════════════════════════╝

  python/cpython
    ★ 63,475 stars
    Interpreted programming language

  tensorflow/tensorflow
    ★ 187,634 stars
    An Open Source Machine Learning Framework
```

### `ara watch` — Real-time monitoring

```
$ python -m ara watch python/cpython -i 10

  Watching python/cpython
  Refreshing every 10s | Press Ctrl+C to stop

  NAME                          STARS       Δ    GROWTH
  ─────────────────────────────────────────────────────
  python/cpython               ★ 63,475     0         0

  API calls remaining: 58
```

Press `Ctrl+C` to stop watching and see a session summary.

### `ara battle` — Arena showdown

```
$ python -m ara battle facebook/react vuejs/core

    ╔══════════════════════════════════════════════╗
    ║          ★  A R E N A   B A T T L E  ★      ║
    ╠══════════════════════════════════════════════╣
    ║  facebook/react     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░  ★ 230,000  ← WINNER! 🏆
    ║  vuejs/core         ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░  ★ 47,000
    ╠══════════════════════════════════════════════╣
    ║  facebook/react wins by 183,000 ★!           ║
    ╚══════════════════════════════════════════════╝

  API calls remaining: 57
```

### `ara info` — Deep dive

```
$ python -m ara info rust-lang/rust

    ╔══════════════════════════════════════════════╗
    ║               ★  A R A  ★                   ║
    ╚══════════════════════════════════════════════╝

  rust-lang/rust
  ────────────────────────────────────────
    Stars:      ★ 101,000
    Forks:      ★ 13,200
    Language:   Rust
    Issues:     5,432
    About:      Empowering everyone to build reliable and efficient software.

  API calls remaining: 56

  💡 Want to compare?
    ara battle rust-lang/rust <other-repo>
```

---

## 🔧 Development

```bash
# Clone
git clone https://github.com/li1050109098/alpha-project.git
cd alpha-project

# Run directly
python -m ara stars owner/project

# Run tests
python -m pytest tests/ -v

# Run a specific test
python -m pytest tests/test_battle.py -v
```

### Project Structure

```
alpha-project/
├── ara/                  # Package source
│   ├── __init__.py       # Package init, __version__
│   ├── __main__.py       # Entry point for `python -m ara`
│   ├── cli.py            # CLI argument parser & all commands
│   ├── console.py        # Terminal rendering helpers
│   └── core.py           # Data models & GitHub API client
├── tests/                # Test suite
│   ├── __init__.py
│   ├── conftest.py       # Test fixtures
│   ├── test_battle.py    # Battle command tests
│   └── test_watch.py     # Watch command tests
├── setup.py              # Package metadata
├── LICENSE               # MIT license
└── README.md             # You are here! 🎉
```

---

## 🚢 Installing

```bash
# From source (recommended for now)
pip install -e .

# Then use the `ara` command directly
ara stars python/cpython
```

---

## ☁️ Rate Limits

GitHub's API has rate limits:

| Auth | Limit | How to set |
|------|-------|------------|
| None | 60 req/hr | Just run it |
| Token | 5,000 req/hr | `export GITHUB_TOKEN=ghp_xxx` |

ARA automatically shows your remaining API calls and caches results for 60 seconds to reduce unnecessary requests.

---

## 🤝 Contributing

All contributions welcome!

1. 🍴 Fork the repo
2. 🌿 `git checkout -b feat/your-idea`
3. 🛠️ Make changes
4. ✅ `python -m pytest tests/ -v`
5. 📬 Open a Pull Request

**Ideas:** Web UI, Slack/Discord integration, historical charts, GitHub action badge generator, export to CSV/JSON, Grafana datasource, support for private repos, email notifications...

---

## 📝 License

MIT © [li1050109098](https://github.com/li1050109098)

---

<p align="center">
  <sub>Built with ❤️ by <b>Α-Tech Inc.</b> — <i>"Watch, Compete, Win."</i></sub>
</p>

## Updates
- Arena running


## Updates
- Arena running


## Updates
- Arena running


## Updates
- Arena running


## Updates
- Arena running


## Updates
- Arena running


## Updates
- Arena running


## Updates
- Arena running


## Updates
- Arena running


## Updates
- Arena running


## Updates
- Arena running


## Updates
- Arena running

