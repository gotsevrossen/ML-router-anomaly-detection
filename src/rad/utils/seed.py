"""Fixed random seeds everywhere (reproducibility rule, CLAUDE.md §2)."""

from __future__ import annotations

import random

import numpy as np


def set_seed(seed: int) -> np.random.Generator:
    """Seed Python's and NumPy's global RNGs and return a dedicated Generator.

    Prefer passing the returned Generator around over relying on global state.
    """
    random.seed(seed)
    np.random.seed(seed)
    return np.random.default_rng(seed)
