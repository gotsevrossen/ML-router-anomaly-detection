"""Per-device streaming pipeline: score -> update rule -> disambiguation -> output record (Phase 2d).

Update rules (the Phase 3 ablation arms):
  frozen  learn nothing after bootstrap (detector and profile cache)
  naive   learn every window right after scoring it
  gated   quarantine buffer only (D18)
  full    quarantine + drift budget + anchor model (D19); gating uses
          max(fast score, anchor score), so a drifted fast model cannot wave
          through what the anchor still finds anomalous

Output record per window (CLAUDE.md §5 2d), plus a few fields for analysis:
  {"t", "device", "score", "state", "alert", "threat_score", "top_features",
   "update_decision", "drift_notice", "raw_alert", "fast_score", "anchor_score",
   "divergence", "released", "alarm_score"}
"""

from __future__ import annotations

import copy
import logging
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

import numpy as np

from rad.continual.anchor import AnchorModel
from rad.continual.disambiguation import DisambiguationConfig, classify, group_z, top_features
from rad.continual.drift_budget import DriftBudget
from rad.continual.profile_stats import RobustProfile
from rad.continual.quarantine import COMMITTED, REJECTED, QuarantineConfig, QuarantinedLearner
from rad.pipeline.alarm import StrictDualAlarm
from rad.eval import metrics as M
from rad.features.profile_cache import ProfileCache, WindowObservation
from rad.models.base import Detector

log = logging.getLogger(__name__)

UPDATE_RULES = ("frozen", "naive", "gated", "full")


@dataclass
class PipelineConfig:
    update_rule: str = "full"
    quarantine: dict[str, Any] = field(default_factory=dict)  # t_delay_s, purge_k, taint_on_alert
    budget: dict[str, Any] = field(default_factory=lambda: {"b_daily": 1.0, "b_total": 3.0})
    anchor: dict[str, Any] = field(default_factory=lambda: {"update_every_s": None})
    disambiguation: dict[str, Any] = field(default_factory=dict)
    alert_k: int = 2  # alert when >= k of the last n windows reach tau_alert
    alert_n: int = 3
    top_k: int = 3
    profile_half_life_days: float = 1.0
    # D53: {"mode": "k_of_n"} (alert_k/alert_n above) or {"mode": "strict_dual", "k": 8, "margin": 0.02};
    # D60: "score": "learned" (default) or "min_reference" (learned and frozen bootstrap model must agree)
    alarm: dict[str, Any] = field(default_factory=lambda: {"mode": "k_of_n"})

    def __post_init__(self) -> None:
        if self.update_rule not in UPDATE_RULES:
            raise ValueError(f"update_rule must be one of {UPDATE_RULES}, got {self.update_rule!r}")
        if not 1 <= self.alert_k <= self.alert_n:
            raise ValueError("need 1 <= alert_k <= alert_n")
        if self.alarm.get("mode", "k_of_n") not in ("k_of_n", "strict_dual"):
            raise ValueError(f"alarm mode must be k_of_n or strict_dual, got {self.alarm.get('mode')!r}")
        if self.alarm.get("score", "learned") not in ("learned", "min_reference"):
            raise ValueError(f"alarm score must be learned or min_reference, got {self.alarm.get('score')!r}")
        if self.alarm.get("score") == "min_reference" and self.alarm.get("mode") != "strict_dual":
            raise ValueError("alarm score min_reference is implemented for the strict_dual alarm only")

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "PipelineConfig":
        return cls(**d)


def calibrate_thresholds(validation_scores: Sequence[float], window_s: float, alarms_per_day: float,
                         admit_quantile: float) -> tuple[float, float]:
    """(tau_admit, tau_alert) from benign validation scores only (CLAUDE.md §8)."""
    s = np.asarray(validation_scores, dtype=float)
    tau_alert = M.threshold_for_alarm_rate(s, alarms_per_day, window_s)
    tau_admit = min(float(np.quantile(s, admit_quantile)), tau_alert)
    return tau_admit, tau_alert


class _MaxScorer:
    """Scores with max(fast, anchor); learning goes to the fast model only."""

    def __init__(self, fast: Detector, anchor: AnchorModel) -> None:
        self.fast, self.anchor = fast, anchor
        self.last: tuple[float, float] = (0.0, 0.0)

    def bootstrap(self, xs) -> None:  # both models are bootstrapped by the pipeline
        pass

    def score_one(self, x: dict[str, float]) -> float:
        self.last = (float(self.fast.score_one(x)), self.anchor.score_one(x))
        return max(self.last)

    def learn_one(self, x: dict[str, float]) -> None:
        self.fast.learn_one(x)


class DevicePipeline:
    """One device's detector plus update rule. `process` is called once per closed window."""

    def __init__(self, device: str, features: Sequence[str], detector_factory: Callable[[], Detector],
                 bootstrap_rows: Sequence[dict[str, float]], cfg: PipelineConfig, tau_admit: float, tau_alert: float,
                 window_s: float = 30.0, profile_cache: ProfileCache | None = None,
                 bootstrapped_fast: Detector | None = None, alarm: StrictDualAlarm | None = None) -> None:
        """`alarm`: the calibrated D53 strict dual alarm when cfg.alarm["mode"] == "strict_dual"."""
        if cfg.alarm.get("mode", "k_of_n") == "strict_dual" and alarm is None:
            raise ValueError("alarm mode strict_dual needs a calibrated StrictDualAlarm (see rad.pipeline.alarm)")
        self.alarm = alarm
        self.device = device
        self.features = tuple(features)
        self.cfg = cfg
        self.tau_admit, self.tau_alert = float(tau_admit), float(tau_alert)
        self.profile_cache = profile_cache
        self.fast = bootstrapped_fast
        if self.fast is None:
            self.fast = detector_factory()
            self.fast.bootstrap(list(bootstrap_rows))
        # D60: alarm only when the learned model AND a frozen copy of the bootstrapped model both find the window
        # anomalous (min of the two scores). Learning may widen "normal" but never make alarms stricter than at
        # bootstrap (D44's principle, applied to the alarm). Gating is unchanged (it stays conservative).
        self.reference: Detector | None = None
        if cfg.alarm.get("score", "learned") == "min_reference":
            self.reference = copy.deepcopy(self.fast)
        self.robust = RobustProfile(self.features, bootstrap_rows, cfg.profile_half_life_days)
        self.disamb = DisambiguationConfig.from_dict(cfg.disambiguation)
        self.recent: deque[bool] = deque(maxlen=cfg.alert_n)
        self.budget: DriftBudget | None = None
        self.anchor: AnchorModel | None = None
        self.quarantine: QuarantinedLearner | None = None
        self._notices_seen = 0

        rule = cfg.update_rule
        if rule in ("gated", "full"):
            qcfg = QuarantineConfig(tau_admit=self.tau_admit, tau_alert=self.tau_alert, **cfg.quarantine)
            scorer: Detector = self.fast
            gate = None
            on_commit = self._commit_to_robust
            if rule == "full":
                self.anchor = AnchorModel(detector_factory(), bootstrap_rows, **cfg.anchor)
                self.budget = DriftBudget(self.features, bootstrap_rows, profile=self.robust, **cfg.budget)
                scorer = _MaxScorer(self.fast, self.anchor)
                gate = self.budget.try_commit  # adds accepted commits to the shared robust profile
                on_commit = self.anchor.observe_commit
            self.quarantine = QuarantinedLearner(scorer, qcfg, profile=profile_cache, window_s=window_s, gate=gate,
                                                 on_commit=on_commit)

    def _commit_to_robust(self, t: float, x: dict[str, float]) -> None:
        self.robust.add(x)

    def process(self, t: float, x: dict[str, float], obs: WindowObservation | None = None) -> dict[str, Any]:
        self.robust.advance(t)
        if self.anchor is not None:
            self.anchor.tick(t)
        released = {"committed": 0, "purged": 0, "blocked": 0}
        anchor_score = None
        rule = self.cfg.update_rule
        if self.quarantine is not None:
            step = self.quarantine.process(t, x, obs)
            score = step.score
            decision = step.decision
            released = {"committed": len(step.committed), "purged": len(step.purged), "blocked": len(step.blocked)}
            fast_score = score
            if isinstance(self.quarantine.detector, _MaxScorer):
                fast_score, anchor_score = self.quarantine.detector.last
        else:
            score = fast_score = float(self.fast.score_one(x))  # scored before any learning
            if rule == "naive":
                self.fast.learn_one(x)
                self.robust.add(x)
                if self.profile_cache is not None and obs is not None:
                    self.profile_cache.commit(obs)
                decision = COMMITTED
            else:
                decision = REJECTED  # frozen: nothing is ever learned

        raw_alert = score >= self.tau_alert
        self.recent.append(raw_alert)
        alarm_score = score
        if self.reference is not None:  # D60: the learned model and the frozen reference must agree
            alarm_score = min(float(fast_score), float(self.reference.score_one(x)))
        if self.alarm is not None:  # D53: strict persistence OR a raw window beyond everything benign seen
            alert = self.alarm.update(t, alarm_score)[0]
        else:
            alert = sum(self.recent) >= self.cfg.alert_k
        persistence = sum(self.recent) / self.cfg.alert_n
        magnitude = float(np.clip((score - self.tau_admit) / max(1e-12, 1.0 - self.tau_admit), 0.0, 1.0))
        z = self.robust.robust_z(x)
        state = classify(alert, *group_z(z, self.disamb), self.disamb)

        drift_notice = False
        if self.budget is not None and len(self.budget.notices) > self._notices_seen:
            drift_notice = True
            self._notices_seen = len(self.budget.notices)
        if self.anchor is not None and (raw_alert or drift_notice):
            self.anchor.observe_alarm(t)

        return {
            "t": t,
            "device": self.device,
            "score": round(float(score), 6),
            "state": state,
            "alert": bool(alert),
            "threat_score": round(persistence * magnitude, 4),
            "top_features": top_features(z, self.cfg.top_k),
            "update_decision": decision,
            "drift_notice": drift_notice,
            "raw_alert": bool(raw_alert),
            "fast_score": round(float(fast_score), 6),
            "anchor_score": None if anchor_score is None else round(float(anchor_score), 6),
            "divergence": anchor_score is not None and anchor_score >= self.tau_alert > fast_score,
            "released": released,
            "alarm_score": round(float(alarm_score), 6),
        }
