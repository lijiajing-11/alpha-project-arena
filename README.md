
<p align="center">
  <img src="https://img.shields.io/badge/ARA-Arena%20Star%20Tracker-8A2BE2?style=for-the-badge&logo=github&logoColor=white" alt="ARA Banner"/>
</p>

<h1 align="center">⚡ ARA — Arena Star Tracker</h1>

<p align="center">
  <b>Track GitHub Stars from your terminal. Compare repos. Win the arena.</b>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3.10+"/></a>
  <a href="https://pypi.org/project/ara/"><img src="https://img.shields.io/badge/pypi-v0.1.0--alpha-8A2BE2?style=flat&logo=pypi&logoColor=white" alt="PyPI"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e?style=flat" alt="MIT License"/></a>
  <a href="https://github.com/li1050109098/alpha-project"><img src="https://img.shields.io/github/stars/li1050109098/alpha-project?style=flat&label=stars&color=facc15" alt="GitHub Stars"/></a>
  <a href="#"><img src="https://img.shields.io/badge/status-alpha-f97316?style=flat" alt="Alpha Status"/></a>
  <a href="https://github.com/li1050109098/alpha-project/actions"><img src="https://img.shields.io/badge/CI-passing-22c55e?style=flat&logo=githubactions" alt="CI"/></a>
  <br/>
  <a href="#-quick-start"><img src="https://img.shields.io/badge/▶️-Quick%20Start-22c55e?style=flat" alt="Quick Start"/></a>
  <a href="#-commands"><img src="https://img.shields.io/badge/📖-Commands-3b82f6?style=flat" alt="Commands"/></a>
  <a href="#-development"><img src="https://img.shields.io/badge/🧪-Development-8A2BE2?style=flat" alt="Development"/></a>
</p>

---

## 🎯 What is ARA?

**ARA** (Arena Star Tracker) 是一个精致、零依赖的 CLI 工具，直接在终端里**实时追踪 GitHub Stars**。没有 Web 仪表盘、没有数据库、没有 API token 也能跑——一条命令，看遍天下开源之星。

```bash
# 查星数 — 快速看一眼
ara stars tensorflow/tensorflow

# 盯盘 — 实时刷新，看数字跳动
ara watch python/cpython

# 擂台赛 — 两个项目当面掰手腕
ara battle facebook/react vuejs/core

# 深挖 — 项目详情：星数、fork、语言、issue
ara info rust-lang/rust

# 排行榜 — 所有追踪过的仓库，按星排序
ara leaderboard
```

### ✨ Highlights

- **🍃 Zero external deps** — 纯 Python 3.10+，stdlib only，pip install 秒完
- **⚡ Real-time watching** — 间隔轮询，彩色 delta 显示，Ctrl+C 出总结
- **🎨 Beautiful terminal** — ANSI 颜色、ASCII 艺术框、emoji 胜负标识
- **🏆 Arena Battle** — 并排对比，带进度条，自动判定 WINNER 🏆
- **📊 Rate-limit aware** — 自动显示剩余 API 次数，1 分钟缓存防浪费
- **🔧 Extensible** — Info / Leaderboard / Battle / Watch，更多命令在路

### 🏁 Who's it for?

- **独立开发者** — 刚开源一个新库？用 `ara watch` 看着星星一颗颗涨起来
- **创业团队** — 跟踪竞品或自己的 GitHub 影响力，不用打开浏览器
- **Hackathon 团队** — 赛中比谁 star 涨得快，现场 battle
- **极端闲人（褒义）** — 喜欢看着 ⭐ 数字跳动带来的多巴胺

---

## 🚀 Quick Start

```bash
# 安装（有了 pip 就完事了，啥依赖没有）
pip install ara

# 查星数
ara stars python/cpython

# 看详情
ara info rust-lang/rust

# 擂台对决
ara battle facebook/react vuejs/core
```

**从安装到看到结果 ≈ 10 秒。** 没有配置文件、没有环境变量、没有数据库迁移、没有 Docker。

> ⚠️ **Rate Limit:** 不带 `GITHUB_TOKEN` 每小时 60 次，设了 `export GITHUB_TOKEN=ghp_xxx` 每小时 5,000 次。够用到手软。

---

## 📖 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ara stars <repo...>` | 获取当前星数 | `ara stars owner/project` |
| `ara watch <repo...>` | 实时监控（自动刷新） | `ara watch owner/project -i 10` |
| `ara battle <repo...>` | 并排对比，判胜者 | `ara battle teamA/lib teamB/lib` |
| `ara info <repo>` | 项目详情（星、fork、语言） | `ara info owner/project` |
| `ara leaderboard` | 排行榜（按星排序） | `ara leaderboard` |

### `ara stars` — Quick check

```
$ ara stars python/cpython tensorflow/tensorflow

    ╔══════════════════════════════════════════════╗
    ║               ★  A R A  ★                   ║
    ║          Arena Star Tracker v0.1.0           ║
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
$ ara watch python/cpython -i 10

  Watching python/cpython
  Refreshing every 10s | Press Ctrl+C to stop

  NAME                          STARS       Δ    GROWTH
  ─────────────────────────────────────────────────────
  python/cpython               ★ 63,475     0         0

  API calls remaining: 58
```

按 `Ctrl+C` 停止，自动输出会话摘要（总时长、峰值、平均变化率）。

### `ara battle` — Arena showdown

```
$ ara battle facebook/react vuejs/core

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

每个仓库用进度条直观对比，胜者跳出 🏆，毫无争议。

### `ara info` — Deep dive

```
$ ara info rust-lang/rust

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

### `ara leaderboard` — Ranked view

```
$ ara leaderboard

    ╔══════════════════════════════════════════════╗
    ║         ★  A R A   L E A D E R B O A R D ★  ║
    ╠══════════════════════════════════════════════╣
    ║  #1   tensorflow/tensorflow     ★ 187,634    ║
    ║  #2   facebook/react            ★ 230,000    ║
    ║  #3   rust-lang/rust            ★ 101,000    ║
    ║  #4   vuejs/core                ★ 47,000     ║
    ║  #5   python/cpython            ★ 63,475     ║
    ╚══════════════════════════════════════════════╝
```

---

## ☁️ Rate Limits

GitHub 的 API 限制是这样：

| Auth | Limit | How to set |
|------|-------|------------|
| None | 60 req/hr | 直接跑，够玩一两次 |
| Token | 5,000 req/hr | `export GITHUB_TOKEN=ghp_xxx` |

ARA 会自动显示剩余 API 次数，并且结果缓存 60 秒，避免重复请求浪费配额。

---

## 🔧 Development

```bash
# Clone
git clone https://github.com/li1050109098/alpha-project.git
cd alpha-project

# Run directly (no install needed)
python -m ara stars owner/project

# Or install in dev mode
pip install -e .

# Run tests
python -m pytest tests/ -v

# Run a specific test
python -m pytest tests/test_battle.py -v
```

### Project Structure

```
alpha-project/
├── ara/                  # 包源码
│   ├── __init__.py       # 版本号
│   ├── __main__.py       # Entry point (python -m ara)
│   ├── cli.py            # 命令解析 & 入口
│   ├── display.py        # 终端渲染
│   ├── colors.py         # ANSI 颜色
│   ├── battle.py         # 擂台对比逻辑
│   └── core.py           # 数据模型 & GitHub API
├── tests/                # 测试套件
│   ├── __init__.py
│   ├── conftest.py       # Fixtures
│   ├── test_battle.py
│   ├── test_cli.py
│   └── test_watch.py
├── setup.py              # 包元数据
├── LICENSE               # MIT license
└── README.md             # ← 你现在就在看这个
```

---

## 🤝 Contributing

所有贡献都欢迎！不管你是修 typo、加 feature、还是提 issue。

1. 🍴 Fork the repo
2. 🌿 `git checkout -b feat/your-idea`
3. 🛠️ 改代码
4. ✅ `python -m pytest tests/ -v`（确保测试通过）
5. 📬 Open a Pull Request

**想搞的大方向（欢迎来 PR）：**
- Web UI（在浏览器里看实时星星）
- Slack / Discord bot 集成
- 历史曲线图（GitHub Star history over time）
- GitHub Action badge generator
- 导出 CSV / JSON
- 私有仓库支持
- Email / 桌面通知

---

## 📝 License

MIT © [li1050109098](https://github.com/li1050109098)

---

<p align="center">
  <sub>Built with ❤️ and too much caffeine by <b>Α-Tech Inc.</b> — <i>"Watch, Compete, Win."</i></sub>
</p>
