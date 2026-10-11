"""Quarantine buffer: gated, delayed-commit updates (Phase 2a, CLAUDE.md §5 2a).

Per window, in packet-time order:
  1. Release: queued windows older than `t_delay_s` leave the queue. They are
     committed (detector.learn_one + profile.commit) only if no alert fired
     while they were queued; otherwise they are purged.
  2. Score the new window *before* any learning on it.
  3. score >= tau_alert  -> alert: the window is rejected, and the `purge_k` most
     recently queued windows are purged at once (the pre-attack ramp-up).
     tau_admit <= score < tau_alert -> rejected (not learned, no alert).
     score < tau_admit  -> quarantined (queued).

The profile cache behind the "new IP / port / domain" features is committed by
the same rule, so poisoning cannot teach the cache through a side door (§8).
The queue is a bounded FIFO, so the C port can use a static ring buffer.
"""

from __future__ import annotations

import logging
import math
from collections import deque
from dataclasses import dataclass, field
from typing import Any

from rad.features.profile_cache import ProfileCache, WindowObservation
from rad.models.base import Detector

log = logging.getLogger(__name__)

QUARANTINED, REJECTED, COMMITTED, PURGED = "quarantined", "rejected", "committed", "purged"


@dataclass(frozen=True)
class QuarantineConfig:
    tau_admit: float
    tau_alert: float
    t_delay_s: float = 86_400.0
    purge_k: int = 10
    taint_on_alert: bool = True  # an alert disqualifies every window queued at that moment (rule 4)
    max_queue: int | None = None  # default: enough windows for t_delay_s at window_s

    def __post_init__(self) -> None:
        if not self.tau_admit <= self.tau_alert:
            raise ValueError(f"need tau_admit <= tau_alert, got {self.tau_admit} > {self.tau_alert}")
        if self.t_delay_s < 0 or self.purge_k < 0:
            raise ValueError("t_delay_s and purge_k must be non-negative")

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "QuarantineConfig":
        return cls(**d)


@dataclass
class _Item:
    t: float
    x: dict[str, float]
    obs: WindowObservation | None
    tainted: bool = False


@dataclass
class QuarantineStep:
    """What happened when one window arrived."""

    t: float
    score: float
    alert: bool
    decision: str  # this window: quarantined | rejected
    committed: list[float] = field(default_factory=list)  # earlier windows committed now
    purged: list[float] = field(default_factory=list)  # earlier windows purged now


@dataclass
class QuarantineStats:
    windows: int = 0
    alerts: int = 0
    quarantined: int = 0
    rejected: int = 0
    committed: int = 0
    purged: int = 0
    forced_releases: int = 0  # queue full before t_delay_s (irregular window spacing)


class QuarantinedLearner:
    """Wraps any `Detector` (and optionally the profile cache) with the quarantine rule."""

    def __init__(self, detector: Detector, cfg: QuarantineConfig, profile: ProfileCache | None = None,
                 window_s: float = 30.0) -> None:
        self.detector = detector
        self.cfg = cfg
        self.profile = profile
        cap = cfg.max_queue or math.ceil(cfg.t_delay_s / window_s) + 1
        self.queue: deque[_Item] = deque()
        self.max_queue = max(1, cap)
        self.stats = QuarantineStats()
        self.outcome: dict[float, str] = {}  # final decision per window start (the per-window log)

    def process(self, t: float, x: dict[str, float], obs: WindowObservation | None = None) -> QuarantineStep:
        """Handle one closed window: release due items, score, then gate."""
        step = QuarantineStep(t=t, score=0.0, alert=False, decision=REJECTED)
        self._release_due(t, step)

        score = float(self.detector.score_one(x))  # scored before any learning on x
        step.score = score
        self.stats.windows += 1
        if score >= self.cfg.tau_alert:
            step.alert = True
            self.stats.alerts += 1
            self._on_alert(step)
            self._decide(t, REJECTED)
            step.decision = REJECTED
        elif score < self.cfg.tau_admit:
            if len(self.queue) >= self.max_queue:
                self.stats.forced_releases += 1
                self._release(self.queue.popleft(), step)
            self.queue.append(_Item(t, x, obs))
            self._decide(t, QUARANTINED)
            step.decision = QUARANTINED
        else:
            self._decide(t, REJECTED)
            step.decision = REJECTED
        log.debug("t=%.0f score=%.4f alert=%s decision=%s committed=%d purged=%d", t, score, step.alert,
                  step.decision, len(step.committed), len(step.purged))
        return step

    def flush(self, t_end: float) -> QuarantineStep:
        """Release everything due by `t_end` (end of stream). Items not yet due stay quarantined."""
        step = QuarantineStep(t=t_end, score=float("nan"), alert=False, decision="")
        self._release_due(t_end, step)
        return step

    # -- internals ---------------------------------------------------------------

    def _decide(self, t: float, decision: str) -> None:
        self.outcome[t] = decision
        if decision == QUARANTINED:
            self.stats.quarantined += 1
        elif decision == REJECTED:
            self.stats.rejected += 1

    def _release_due(self, now: float, step: QuarantineStep) -> None:
        while self.queue and self.queue[0].t + self.cfg.t_delay_s <= now:
            self._release(self.queue.popleft(), step)

    def _release(self, item: _Item, step: QuarantineStep) -> None:
        if item.tainted:
            self._purge(item, step)
            return
        self.detector.learn_one(item.x)
        if self.profile is not None and item.obs is not None:
            self.profile.commit(item.obs)
        self.outcome[item.t] = COMMITTED
        self.stats.committed += 1
        step.committed.append(item.t)

    def _purge(self, item: _Item, step: QuarantineStep) -> None:
        self.outcome[item.t] = PURGED
        self.stats.purged += 1
        step.purged.append(item.t)

    def _on_alert(self, step: QuarantineStep) -> None:
        for _ in range(min(self.cfg.purge_k, len(self.queue))):
            self._purge(self.queue.pop(), step)  # most recent first: the ramp-up before the alert
        if self.cfg.taint_on_alert:
            for item in self.queue:
                item.tainted = True
