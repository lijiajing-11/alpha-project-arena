"""Pytest configuration and shared fixtures for ARA tests."""

import sys
from pathlib import Path

# Add repo root to path so imports work
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
