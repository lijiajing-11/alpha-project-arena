# Changelog

## [0.3.2] — 2026-05-19

### Added
- `ara history --compare` — 多仓库星史对比条形图
- `ara insight --compare` — 双栏仓库洞察对比
- pytest-cov coverage 报告配置

### Changed
- `ara history` 接受多个 repos (nargs="+")
- Development Status → 4 - Beta

### Fixed
- setup.py 版本与 __init__.py 同步 (0.3.0 → 0.3.2)

## [0.3.1] — 2026-05-19

### Added
- `ara watch --notify` — 桌面通知功能 (plyer + stderr fallback)
- `ara insight` — 深度仓库洞察命令

### Changed
- pyproject.toml 完善 pytest + ruff 配置

## [0.3.0] — 2026-05-19

### Added
- `ara rank` — 实时 Top N 仓库排行榜
- `ara dashboard` — 仓库全貌信息面板
- `ara summary` — 一行仓库概览
- `ara history` — 星史 ASCII 折线图
- `ara compare` — 双仓库对比 + 奖牌 🥇🥈🥉
- `ara watch` — 实时监控 (30s 轮询)
- `ara battle` — 仓库对战 ASCII 图
- `ara stars` — 快速查看星数
- `ara info` — 仓库详情
- `ara trends` — 趋势分析 + ASCII 图
- `ara generate-stars` — 获取 stargazers
- JSON 输出支持（所有命令）
- GitHub Actions CI 配置
- Desktop notification (plyer)
