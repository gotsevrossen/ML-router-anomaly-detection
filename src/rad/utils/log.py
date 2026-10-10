"""Logging setup. Modules log through `logging.getLogger(__name__)`; nothing prints."""

from __future__ import annotations

import logging

_FORMAT = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"


def setup_logging(level: str | int = "INFO") -> None:
    """Configure the root logger once for CLI entry points."""
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=level, format=_FORMAT, force=True)
