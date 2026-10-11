"""Quarantine buffer (Phase 2a) on scripted streams with known answers."""

from __future__ import annotations

import pytest

from rad.continual.quarantine import (
    COMMITTED,
    PURGED,
    QUARANTINED,
    REJECTED,
    QuarantineConfig,
    QuarantinedLearner,
)
from rad.features.profile_cache import ProfileCache, WindowObservation

W = 30.0
TAU_ADMIT, TAU_ALERT = 0.5, 0.9


class ScriptedDetector:
    """score = x['s']; records what it learned and checks no window is learned before it is scored."""

    def __init__(self) -> None:
        self.learned: list[float] = []
        self.scored: set[float] = set()

    def bootstrap(self, xs) -> None:
        pass

    def score_one(self, x) -> float:
        self.scored.add(x["t"])
        return x["s"]

    def learn_one(self, x) -> None:
        assert x["t"] in self.scored, "learned a window before scoring it"
        self.learned.append(x["t"])


def make(t_delay_windows: int = 4, purge_k: int = 2, taint: bool = True, profile: ProfileCache | None = None,
         max_queue: int | None = None):
    det = ScriptedDetector()
    cfg = QuarantineConfig(tau_admit=TAU_ADMIT, tau_alert=TAU_ALERT, t_delay_s=t_delay_windows * W,
                           purge_k=purge_k, taint_on_alert=taint, max_queue=max_queue)
    return det, QuarantinedLearner(det, cfg, profile=profile, window_s=W)


def feed(q: QuarantinedLearner, scores: list[float], ip_prefix: str = "8.8.8."):
    steps = []
    for i, s in enumerate(scores):
        t = i * W
        obs = WindowObservation(t, dst_ips=(f"{ip_prefix}{i}",))
        steps.append(q.process(t, {"t": t, "s": s}, obs))
    return steps


def test_benign_windows_commit_only_after_the_delay():
    det, q = make(t_delay_windows=4)
    steps = feed(q, [0.1] * 10)
    assert [s.decision for s in steps] == [QUARANTINED] * 10
    assert steps[3].committed == [] and steps[4].committed == [0.0]  # window 0 is due at t = 4 W
    assert det.learned == [i * W for i in range(6)]  # windows 6..9 still quarantined
    assert q.outcome[5 * W] == COMMITTED and q.outcome[9 * W] == QUARANTINED


def test_obviously_anomalous_window_is_never_committed():
    det, q = make(t_delay_windows=2, purge_k=0, taint=False)
    feed(q, [0.1, 0.99, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    assert q.outcome[1 * W] == REJECTED
    assert 1 * W not in det.learned
    assert q.stats.alerts == 1


def test_mid_band_window_is_rejected_without_alert():
    det, q = make(t_delay_windows=1)
    steps = feed(q, [0.1, 0.7, 0.1, 0.1])
    assert (steps[1].decision, steps[1].alert) == (REJECTED, False)
    assert 1 * W not in det.learned and q.stats.alerts == 0


def test_alert_purges_the_windows_just_before_it():
    det, q = make(t_delay_windows=10, purge_k=2, taint=False)
    steps = feed(q, [0.1, 0.1, 0.1, 0.4, 0.45, 0.95])
    assert steps[5].alert and steps[5].purged == [4 * W, 3 * W]  # the ramp-up, most recent first
    assert q.outcome[3 * W] == q.outcome[4 * W] == PURGED
    feed_more = [q.process(t, {"t": t, "s": 0.1}) for t in (W * k for k in range(6, 14))]
    assert det.learned == [0.0, W, 2 * W]  # without taint the older windows still commit
    assert all(3 * W != t and 4 * W != t for s in feed_more for t in s.committed)


def test_alert_taints_everything_queued_at_that_moment():
    det, q = make(t_delay_windows=3, purge_k=1, taint=True)
    feed(q, [0.1, 0.1, 0.1, 0.95, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    # Window 0 fell due at 3 W and was released before window 3 was scored, so it committed.
    # Window 2 is purged at once (purge_k=1); window 1 was queued during the alert, so it never commits.
    assert [q.outcome[k * W] for k in range(4)] == [COMMITTED, PURGED, PURGED, REJECTED]
    assert det.learned == [0.0, 4 * W, 5 * W, 6 * W]  # later windows commit normally once due


def test_profile_cache_only_learns_committed_windows():
    profile = ProfileCache()
    det, q = make(t_delay_windows=2, purge_k=1, taint=False, profile=profile)
    feed(q, [0.1, 0.1, 0.95, 0.1, 0.1, 0.1, 0.1])
    committed = {t for t, d in q.outcome.items() if d == COMMITTED}
    for k in range(7):
        assert profile.has_ip(f"8.8.8.{k}") == (k * W in committed), k
    assert not profile.has_ip("8.8.8.2")  # the alerting window
    assert not profile.has_ip("8.8.8.1")  # purged ramp-up


def test_queue_is_bounded():
    det, q = make(t_delay_windows=100, max_queue=3)
    feed(q, [0.1] * 6)
    assert len(q.queue) == 3 and q.stats.forced_releases == 3
    assert det.learned == [0.0, W, 2 * W]


def test_default_queue_capacity_covers_the_delay():
    _, q = make(t_delay_windows=4)
    assert q.max_queue == 5
    _, q = make(t_delay_windows=4, max_queue=None)
    feed(q, [0.1] * 20)
    assert q.stats.forced_releases == 0  # regular windows never overflow the default capacity


def test_flush_releases_due_items_only():
    det, q = make(t_delay_windows=2)
    feed(q, [0.1] * 3)
    step = q.flush(t_end=3 * W)
    assert step.committed == [W] and det.learned == [0.0, W]
    assert q.outcome[2 * W] == QUARANTINED


def test_every_window_gets_a_final_outcome():
    _, q = make(t_delay_windows=2, purge_k=1)
    scores = [0.1, 0.6, 0.1, 0.95, 0.1, 0.1, 0.1]
    feed(q, scores)
    assert sorted(q.outcome) == [k * W for k in range(len(scores))]
    assert set(q.outcome.values()) <= {QUARANTINED, REJECTED, COMMITTED, PURGED}
    s = q.stats
    assert s.windows == len(scores) and s.quarantined + s.rejected == len(scores)


def test_config_validation():
    with pytest.raises(ValueError):
        QuarantineConfig(tau_admit=0.9, tau_alert=0.5)
    with pytest.raises(ValueError):
        QuarantineConfig(tau_admit=0.1, tau_alert=0.5, purge_k=-1)
    assert QuarantineConfig.from_dict({"tau_admit": 0.1, "tau_alert": 0.5}).t_delay_s == 86_400
