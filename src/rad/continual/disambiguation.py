"""Drift-vs-attack disambiguation (Phase 2c). A hypothesis under test, not a guarantee.

Benign changes (firmware update, new usage schedule) mostly move *volume*;
attacks raise *diversity* (new destinations, new ports, failed connections).
Given robust z-scores against the committed profile:

    z_vol = max |z_j| over F_vol           (a drop in volume can be benign drift too)
    z_div = max  z_j  over F_div, floored at 0   (only *more* diversity is attack-like)

    normal                  if not alert
    suspected_attack        if alert and z_div > tau_div
    suspected_benign_drift  if alert and z_vol >= z_div
    suspected_attack        otherwise (fail-safe: unexplained alerts are not called benign)

RQ4 reports the confusion matrix of these states against ground-truth event types.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

NORMAL, BENIGN_DRIFT, ATTACK = "normal", "suspected_benign_drift", "suspected_attack"

VOL_FEATURES: tuple[str, ...] = ("bytes_out", "bytes_in", "pkts_out", "pkts_in")
DIV_FEATURES: tuple[str, ...] = (
    "n_new_ext_dst_ips", "n_new_dst_ports", "n_new_domains", "n_failed_tcp", "n_ext_dst_prefixes",
    "n_arp_targets",  # D8: LAN scanning shows up as ARP
)


@dataclass(frozen=True)
class DisambiguationConfig:
    tau_div: float = 3.0
    vol_features: tuple[str, ...] = VOL_FEATURES
    div_features: tuple[str, ...] = DIV_FEATURES

    @classmethod
    def from_dict(cls, d: dict) -> "DisambiguationConfig":
        d = dict(d)
        for key in ("vol_features", "div_features"):
            if key in d:
                d[key] = tuple(d[key])
        return cls(**d)


def group_z(z: dict[str, float], cfg: DisambiguationConfig) -> tuple[float, float]:
    """(z_vol, z_div); features missing from `z` (e.g. excluded by config) are skipped."""
    vol = [abs(z[f]) for f in cfg.vol_features if f in z]
    div = [z[f] for f in cfg.div_features if f in z]
    return (max(vol) if vol else 0.0), max(0.0, max(div) if div else 0.0)


def classify(alert: bool, z_vol: float, z_div: float, cfg: DisambiguationConfig) -> str:
    if not alert:
        return NORMAL
    if z_div > cfg.tau_div:
        return ATTACK
    if z_vol >= z_div:
        return BENIGN_DRIFT
    return ATTACK


def top_features(z: dict[str, float], k: int = 3, exclude: Sequence[str] = ()) -> list[list]:
    """The k features furthest from the committed profile, as [name, signed z] pairs (output record)."""
    ranked = sorted(((f, v) for f, v in z.items() if f not in set(exclude)), key=lambda fv: (-abs(fv[1]), fv[0]))
    return [[f, round(float(v), 3)] for f, v in ranked[:k]]
