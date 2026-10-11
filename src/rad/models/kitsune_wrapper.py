"""Kitsune / KitNET baseline around the vendored, unmodified Kitsune-py (third_party/kitsune_py).

Kitsune works per packet with its own AfterImage features (netStat). We feed it
our already-parsed packets (no tshark/scapy) and align its per-packet scores to
our windows by taking the maximum score inside each window (CLAUDE.md §5 1c).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

from rad.features.packet_schema import PacketRecord
from rad.models.base import squash

log = logging.getLogger(__name__)

_VENDOR_DIR = Path(__file__).resolve().parents[3] / "third_party" / "kitsune_py"
_HOST_LIMIT = 100_000_000_000  # same limits Kitsune's own FeatureExtractor uses


def _import_kitsune():
    """Import netStat and KitNET from the vendored copy without editing it."""
    if not hasattr(np, "Inf"):
        np.Inf = np.inf  # removed in NumPy 2.0; AfterImage.py still uses it (VENDORED.md)
    if str(_VENDOR_DIR) not in sys.path:
        sys.path.insert(0, str(_VENDOR_DIR))
    import netStat  # noqa: PLC0415
    from KitNET.KitNET import KitNET  # noqa: PLC0415

    return netStat, KitNET


def kitsune_packet_fields(r: PacketRecord) -> tuple:
    """Our record -> the arguments of netStat.updateGetStats, mirroring Kitsune's scapy parser."""
    ip_type: float = np.nan
    if r.ip_version == 4:
        ip_type = 0
    elif r.ip_version == 6:
        ip_type = 1
    src_ip, dst_ip = r.src_ip, r.dst_ip
    if r.src_port >= 0:
        src_proto, dst_proto = str(r.src_port), str(r.dst_port)
    elif r.ip_version == 0:  # ARP
        src_proto = dst_proto = "arp"
        ip_type = 0
    elif r.ip_proto == 1:  # scapy's ICMP layer is ICMPv4 only
        src_proto = dst_proto = "icmp"
        ip_type = 0
    else:
        src_proto = dst_proto = ""
    return (ip_type, r.src_mac, r.dst_mac, src_ip, src_proto, dst_ip, dst_proto, int(r.cap_len), float(r.ts))


class KitNETDetector:
    """KitNET over arbitrary feature vectors, behind the common Detector interface.

    `bootstrap` sets KitNET's grace periods to the bootstrap length: the first
    `fm_frac` of it learns the feature map, the rest trains the autoencoders.
    Score = squash(RMSE).
    """

    def __init__(self, features: Sequence[str] | None = None, max_autoencoder_size: int = 10,
                 fm_frac: float = 0.1, learning_rate: float = 0.1, hidden_ratio: float = 0.75) -> None:
        self.features = tuple(features) if features is not None else None
        self.max_autoencoder_size = max_autoencoder_size
        self.fm_frac = fm_frac
        self.learning_rate = learning_rate
        self.hidden_ratio = hidden_ratio
        self.model = None

    def _vec(self, x) -> np.ndarray:
        if isinstance(x, dict):
            return np.array([x[f] for f in self.features], dtype=float)
        return np.asarray(x, dtype=float)

    def start(self, n_features: int, n_bootstrap: int) -> None:
        _, KitNET = _import_kitsune()
        fm = max(1, int(self.fm_frac * n_bootstrap))
        self.model = KitNET(n_features, self.max_autoencoder_size, fm, max(1, n_bootstrap - fm),
                            self.learning_rate, self.hidden_ratio)

    def bootstrap(self, xs: Sequence) -> None:
        vecs = [self._vec(x) for x in xs]
        self.start(len(vecs[0]), len(vecs))
        for v in vecs:
            self.model.process(v)

    def score_one(self, x) -> float:
        return squash(self.model.execute(self._vec(x)))

    def learn_one(self, x) -> None:
        self.model.train(self._vec(x))


def kitsune_window_scores(records: Iterable[PacketRecord], windows: Sequence[tuple[int, int]],
                          n_bootstrap_windows: int, *, max_autoencoder_size: int = 10,
                          fm_frac: float = 0.1) -> np.ndarray:
    """Per-window Kitsune score: max packet score among the window's records.

    `windows` are (first_pkt_index, last_pkt_index) pairs in order (-1, -1 for an
    empty window). Packets of the first `n_bootstrap_windows` windows train
    KitNET (frozen afterwards, as Kitsune does); those windows score 0.
    """
    netStat, _ = _import_kitsune()
    stats = netStat.netStat(np.nan, _HOST_LIMIT, _HOST_LIMIT)
    boot_last = max((last for _, last in windows[:n_bootstrap_windows]), default=-1)

    # Index of the window each record belongs to, via the windows' pkt_index ranges.
    bounds = [(i, first, last) for i, (first, last) in enumerate(windows) if first >= 0]
    scores = np.zeros(len(windows))
    det = KitNETDetector(max_autoencoder_size=max_autoencoder_size, fm_frac=fm_frac)
    pos = 0
    pending_bootstrap: list[np.ndarray] = []
    for n, rec in enumerate(records, 1):
        if n % 50_000 == 0:
            log.info("Kitsune: %d packets processed (window %d of %d)", n, bounds[min(pos, len(bounds) - 1)][0] + 1,
                     len(windows))
        while pos < len(bounds) and rec.pkt_index > bounds[pos][2]:
            pos += 1
        if pos == len(bounds) or rec.pkt_index < bounds[pos][1]:
            continue  # record outside every window (cannot happen for extractor output)
        vec = np.asarray(stats.updateGetStats(*kitsune_packet_fields(rec)), dtype=float)
        if rec.pkt_index <= boot_last:
            pending_bootstrap.append(vec)
            continue
        if det.model is None:
            det.bootstrap(pending_bootstrap)
            pending_bootstrap.clear()
        i = bounds[pos][0]
        scores[i] = max(scores[i], det.score_one(vec))
    return scores
