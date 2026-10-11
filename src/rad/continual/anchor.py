"""Anchor model M_anchor (Phase 2b): a slow, gated copy of the detector.

M_fast learns every committed window. M_anchor is either frozen at bootstrap
(`update_every_s=None`, the default) or learns, once per period (weekly by
default), the windows M_fast committed during that period. It does so only if
the period was clean: no alert and no drift notice. Scoring with both lets the
pipeline flag windows the anchor still finds anomalous after the fast model
has drifted ("fast and anchor models diverge", CLAUDE.md §1).
"""

from __future__ import annotations

import logging
import math
from collections import deque
from typing import Sequence

from rad.models.base import Detector

log = logging.getLogger(__name__)

WEEK_S = 7 * 86_400.0


class AnchorModel:
    def __init__(self, detector: Detector, bootstrap_rows: Sequence[dict[str, float]],
                 update_every_s: float | None = None, max_pending: int = 7 * 2880) -> None:
        self.detector = detector
        self.detector.bootstrap(list(bootstrap_rows))
        self.update_every_s = update_every_s
        self.pending: deque[dict[str, float]] = deque(maxlen=max_pending)  # bounded: one period of windows
        self._period: int | None = None
        self._tainted = False
        self.updates = 0
        self.skipped_updates = 0

    def score_one(self, x: dict[str, float]) -> float:
        return float(self.detector.score_one(x))

    def observe_commit(self, t: float, x: dict[str, float]) -> None:
        if self.update_every_s is not None:
            self._roll(t)
            self.pending.append(x)

    def observe_alarm(self, t: float) -> None:
        """An alert or drift notice taints the current period, so it will not reach the anchor."""
        if self.update_every_s is not None:
            self._roll(t)
            self._tainted = True

    def tick(self, t: float) -> bool:
        """Call once per window; returns True when the anchor was updated at this period boundary."""
        return self.update_every_s is not None and self._roll(t)

    def _roll(self, t: float) -> bool:
        period = math.floor(t / self.update_every_s)
        if self._period is None:
            self._period = period
            return False
        if period == self._period:
            return False
        updated = False
        if self.pending and not self._tainted:
            for x in self.pending:
                self.detector.learn_one(x)
            self.updates += 1
            updated = True
            log.info("Anchor updated with %d committed windows from period %d", len(self.pending), self._period)
        elif self.pending:
            self.skipped_updates += 1
            log.info("Anchor update skipped: period %d had an alert or drift notice", self._period)
        self.pending.clear()
        self._tainted = False
        self._period = period
        return updated
