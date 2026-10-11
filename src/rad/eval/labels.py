"""Per-window ground truth from per-frame dataset labels. Evaluation only; never a model input."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq


def load_frame_labels(path: str | Path) -> np.ndarray:
    """Kitsune-dataset labels: one 0/1 per capture frame, optionally with a header and an index column."""
    df = pd.read_csv(path, header=None)
    col = df.iloc[:, -1]
    if not pd.api.types.is_numeric_dtype(col):  # header row such as ",x"
        col = pd.to_numeric(col.iloc[1:], errors="raise")
    return col.to_numpy(dtype=np.int8)


def window_attack_fraction(windows: pd.DataFrame, packets_path: str | Path, frame_labels: np.ndarray) -> np.ndarray:
    """Fraction of each window's device records whose capture frame is labelled attack.

    Windows partition the device's records contiguously in capture order (D9), so a
    window's records are exactly those with pkt_index in [first_pkt_index, last_pkt_index].
    Empty windows get 0.
    """
    pkt = pq.read_table(packets_path, columns=["pkt_index"]).column("pkt_index").to_numpy()
    if len(frame_labels) <= pkt.max():
        raise ValueError(f"labels cover {len(frame_labels)} frames but packets reach index {pkt.max()}")
    rec_labels = frame_labels[pkt]
    frac = np.zeros(len(windows))
    for i, (first, last) in enumerate(zip(windows["first_pkt_index"], windows["last_pkt_index"])):
        if first < 0:
            continue
        lo, hi = np.searchsorted(pkt, first, "left"), np.searchsorted(pkt, last, "right")
        frac[i] = rec_labels[lo:hi].mean() if hi > lo else 0.0
    return frac
