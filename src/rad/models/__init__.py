"""Detectors behind the common `Detector` interface (see base.py)."""

from __future__ import annotations

from typing import Any, Sequence

from rad.models.base import Detector


def build_detector(name: str, features: Sequence[str], params: dict[str, Any] | None = None) -> Detector:
    """Construct a window-level detector by config name. Imports are lazy so torch loads only if used.

    `params` may carry a `type` key, so one config can hold variants of the same detector
    under different names (e.g. `mad_tail: {type: mad, tail_quantile: 0.999}`), and a
    `preprocess` key ({steps: [slog, project], n_projections, seed}) that wraps any
    detector in the D24 transforms.
    """
    params = dict(params or {})
    name = params.pop("type", name)
    pre = params.pop("preprocess", None)
    if pre:
        from rad.models.preprocess import PreprocessedDetector

        pre = dict(pre)
        steps = pre.pop("steps")
        return PreprocessedDetector(features, lambda feats: build_detector(name, feats, params), steps, **pre)
    if name == "fusion":
        from rad.models.fusion import FusionDetector
        return FusionDetector(features, **params)
    if name == "hst":
        from rad.models.hst import HSTDetector
        return HSTDetector(features, **params)
    if name == "iforest":
        from rad.models.iforest import IForestDetector
        return IForestDetector(features, **params)
    if name == "autoencoder":
        from rad.models.autoencoder import AutoencoderDetector
        return AutoencoderDetector(features, **params)
    if name == "mad":
        from rad.models.mad import MADDetector
        return MADDetector(features, **params)
    if name == "kitnet":
        from rad.models.kitsune_wrapper import KitNETDetector
        return KitNETDetector(features, **params)
    raise ValueError(f"unknown detector {name!r}")
