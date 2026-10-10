"""Run metadata written next to every output: git commit, time, package versions."""

from __future__ import annotations

import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any

_TRACKED_PACKAGES = ("rad", "dpkt", "numpy", "pandas", "pyarrow", "pyyaml", "river", "scikit-learn", "torch")


def git_commit(repo_dir: str | Path | None = None) -> str:
    """Return the current commit hash (with '-dirty' if uncommitted changes), or 'nogit'."""
    cwd = Path(repo_dir) if repo_dir else Path(__file__).resolve().parents[3]
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=cwd, capture_output=True, text=True, check=True
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain"], cwd=cwd, capture_output=True, text=True, check=True
        ).stdout.strip()
        return f"{commit}-dirty" if dirty else commit
    except (OSError, subprocess.CalledProcessError):
        return "nogit"


def run_metadata() -> dict[str, Any]:
    """Collect what is needed to reproduce a run."""
    versions: dict[str, str] = {}
    for pkg in _TRACKED_PACKAGES:
        try:
            versions[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            continue
    return {
        "git_commit": git_commit(),
        "utc_time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": versions,
    }
