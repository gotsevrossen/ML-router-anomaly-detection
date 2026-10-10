"""YAML config loading and saving.

Every experiment is driven by a config file, and every output directory gets a
copy of the resolved config that produced it (reproducibility rule, CLAUDE.md §2).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML config file into a dict. An empty file yields an empty dict."""
    with open(path, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    if cfg is None:
        return {}
    if not isinstance(cfg, dict):
        raise ValueError(f"Config {path} must be a YAML mapping, got {type(cfg).__name__}")
    return cfg


def save_resolved_config(cfg: dict[str, Any], out_path: str | Path) -> Path:
    """Write the fully resolved config next to the outputs it produced."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(cfg, fh, sort_keys=False)
    return out_path
