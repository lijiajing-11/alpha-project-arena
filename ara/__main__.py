"""Allow `python -m ara` to invoke the CLI."""
from ara.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
