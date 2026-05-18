<div align="center">

# ★ ARA ★ — Arena Star Tracker

**Battle your repos. Dominate the leaderboard.**

[![GitHub Stars](https://img.shields.io/github/stars/li1050109098/alpha-project?style=for-the-badge&logo=github&label=Stars)](https://github.com/li1050109098/alpha-project)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/li1050109098/alpha-project/ci.yml?style=for-the-badge&logo=githubactions)](https://github.com/li1050109098/alpha-project/actions)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/li1050109098/alpha-project?style=for-the-badge)

```
╔══════════════════════════════════════════════╗
║               ★  A R A  ★                   ║
║          Arena Star Tracker v0.1.0            ║
╚══════════════════════════════════════════════╝
```

</div>

---

## 🎯 What is ARA?

ARA is a **terminal-based GitHub Star tracker** that lets you:

- 📊 **Watch** any repo's stars in real-time
- ⚔️ **Battle** repos side-by-side and declare a winner
- 🏆 **Track** your growth against competitors
- 📈 **Export** data for your README badges

Born from the competitive spirit of open source — because **every star tells a story**.

## ✨ Quick Start

```bash
# Install
pip install ara

# Check your stars
ara stars li1050109098/alpha-project

# Battle two repos
ara battle li1050109098/alpha-project facebook/react

# Watch a repo in real-time
ara watch li1050109098/alpha-project
```

## 🚀 Commands

| Command | Description |
|---------|-------------|
| `ara stars <repo...>` | Get star count for one or more repos |
| `ara watch <repo...>` | Monitor repos in real-time (30s interval) |
| `ara battle <repo...>` | Side-by-side comparison with leaderboard |
| `ara info <repo>` | Detailed repo information |
| `ara leaderboard` | View ranked leaderboard |

## 🎮 Battle Mode

The flagship feature. Run comparison and see who's winning:

```
╔══════════════════════════════════════════════╗
║          ★  A R E N A   B A T T L E  ★     ║
╠══════════════════════════════════════════════╣
║  alpha-project     ▓▓▓▓▓▓▓▓▓▓▓▓░░░░  1,234 ★  ← WINNER! 🏆
║  beta-project      ▓▓▓▓▓▓░░░░░░░░░░    567 ★  ║
╚══════════════════════════════════════════════╝
```

## 🔧 Requirements

- Python 3.10 or higher
- No external dependencies! (stdlib only — `urllib`, `argparse`, `time`)

## 📦 Installation

### From source

```bash
git clone https://github.com/li1050109098/alpha-project.git
cd alpha-project
pip install -e .
```

### Authentication

For higher API rate limits (5,000/hr vs 60/hr), set your GitHub token:

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

Get a token at: [GitHub Settings → Tokens](https://github.com/settings/tokens)

## 🏆 Why ARA?

In the open source arena, **visibility drives growth**. ARA helps you:

1. **Track competitors** — Know exactly how you stack up
2. **Celebrate milestones** — Watch your star count climb in real-time
3. **Motivate your team** — Nothing drives contribution like a leaderboard
4. **Prove your impact** — Star growth = community validation

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/amazing`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing`
5. Open a Pull Request

### Development

```bash
pip install -e ".[dev]"
python -m ara --help
```

## 📜 License

MIT — use it, share it, battle with it.

---

<div align="center">

**⭐ Star the repo and join the arena! ⭐**

[![Star History](https://img.shields.io/github/stars/li1050109098/alpha-project?style=social&label=Star)](https://github.com/li1050109098/alpha-project)

*Built with ❤️ by Alpha Corp*

</div>
