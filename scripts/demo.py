#!/usr/bin/env python3
"""Demo script: generates sample output for README screenshots."""

import subprocess
import sys
import os

DEMO_DIR = os.path.join(os.path.dirname(__file__), "..", "demo")
os.makedirs(DEMO_DIR, exist_ok=True)

REPO = "li1050109098/alpha-project"


def capture(cmd: str, filename: str):
    """Run a command and save output to file."""
    print(f"  Running: {cmd}")
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=os.path.dirname(__file__)
    )
    output = result.stdout + result.stderr
    filepath = os.path.join(DEMO_DIR, filename)
    with open(filepath, "w") as f:
        f.write(output)
    print(f"    → saved to {filepath} ({len(output)} bytes)")


def main():
    print("ARA Demo Script")
    print("=" * 50)
    
    # Use known popular repos for a good demo
    demos = [
        ("ara --help", "demo-help.txt"),
        ("python -m ara stars tiangolo/fastapi pallets/flask", "demo-stars.txt"),
        ("python -m ara battle tiangolo/fastapi pallets/flask psf/requests facebook/react", "demo-battle.txt"),
        ("python -m ara info tiangolo/fastapi", "demo-info.txt"),
    ]
    
    for cmd, filename in demos:
        capture(cmd, filename)
    
    print(f"\nDone! {len(demos)} demo outputs saved to {DEMO_DIR}/")
    print("Use these to create README screenshots or GIFs.")


if __name__ == "__main__":
    main()
