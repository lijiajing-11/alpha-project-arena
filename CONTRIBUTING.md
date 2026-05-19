# Contributing to ARA

🎉 Thanks for your interest in ARA (Arena Star Tracker)!

## Quick Start

```bash
git clone https://github.com/lijiajing-11/alpha-project-arena.git
cd alpha-project-arena
python -m venv venv && source venv/bin/activate
pip install -e .
python -m ara --help
```

## Running Tests

```bash
python -m pytest tests/ -v
```

Tests use `pytest` and `unittest.mock`. No external test dependencies.

## Code Style

- 4-space indentation (Python standard)
- No external dependencies (stdlib only)
- Type hints strongly encouraged
- Keep functions under 50 lines
- Every feature needs a test

## Adding a Command

1. Create a module in `ara/your_command.py` (if more than 10 lines)
2. Add the function + argparse setup in `ara/cli.py` → `build_parser()`
3. Import and register in `main()` dispatch
4. Add tests in `tests/test_your_command.py`

### JSON support

Every command should support `--json`. Add a handler in `build_parser()`'s `json_handlers` dict:

```python
json_handlers = {
    ...
    "your-command": cmd_your_command_json,
}
```

## Pull Request Process

1. Fork the repo and create a feature branch
2. Write tests first (TDD encouraged)
3. Ensure `python -m pytest tests/ -q` passes (all tests)
4. Update README if adding a new command or flag
5. Add a changelog entry
6. Submit PR against `main`

## Reporting Issues

Open an issue with:
- Command you ran
- Full error output
- Python version (`python --version`)
- OS

## Feature Wishlist

- [x] **Desktop notifications** (`ara watch --notify`) — ✅ shipped in v0.3.1
- [x] **Multi-repo compare** (`ara history repo1 repo2 repo3`) — ✅ shipped in v0.3.1
- [ ] CSV/Excel export
- [ ] PyPI release automation
- [ ] GitHub Actions CI badge auto-update
- [ ] `ara compare` — 4+ repos side-by-side

## License

MIT — see LICENSE for details.
