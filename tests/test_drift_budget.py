"""Sketch, drift budget and anchor model (Phase 2b) on synthetic streams with known answers."""

from __future__ import annotations

import numpy as np
import pytest

from rad.continual.anchor import AnchorModel
from rad.continual.drift_budget import NOTICE, DriftBudget, robust_scale
from rad.continual.quarantine import BLOCKED, COMMITTED, QuarantineConfig, QuarantinedLearner
from rad.continual.sketch import FeatureHistograms
from rad.features.profile_cache import ProfileCache, WindowObservation

DAY = 86_400.0
W = 30.0
FEATS = ["vol", "div"]


def boot_rows(n=600, seed=0):
    rng = np.random.default_rng(seed)
    return [{"vol": float(v), "div": float(d)} for v, d in zip(rng.normal(100, 10, n), rng.normal(5, 1, n))]


# -- sketch ---------------------------------------------------------------------------

def test_histogram_median_and_quantiles_track_the_data():
    rows = [{"a": float(v)} for v in np.linspace(0, 100, 1001)]
    h = FeatureHistograms.from_rows(["a"], rows, n_bins=100)
    assert h.median()[0] == pytest.approx(50, abs=1.5)
    assert h.quantile(0.25)[0] == pytest.approx(25, abs=1.5)


def test_histogram_overflow_decay_and_copy():
    h = FeatureHistograms.from_rows(["a"], [{"a": 0.0}, {"a": 10.0}], n_bins=10)
    for _ in range(10):
        h.add({"a": 1e9})  # far above the range: overflow bin
    assert h.median()[0] == h.hi_edge[0]
    before = h.quantile(0.3).copy()
    h.decay(0.25)  # uniform decay leaves quantiles unchanged
    assert h.quantile(0.3) == pytest.approx(before)
    c = h.copy()
    c.add({"a": 0.0}, 100)
    assert h.counts.sum() != c.counts.sum()


def test_robust_scale_fallbacks():
    m = np.array([[1.0, 7.0], [2.0, 7.0], [3.0, 7.0], [4.0, 7.0]])
    s = robust_scale(m)
    assert s[0] == pytest.approx(1.5) and s[1] == 1.0  # IQR; constant feature -> 1.0


# -- drift budget ---------------------------------------------------------------------

def test_stationary_benign_stream_never_halts():
    b = DriftBudget(FEATS, boot_rows(), b_daily=1.0, b_total=2.0)
    accepted = [b.try_commit(i * W, r) for i, r in enumerate(boot_rows(3 * 2880, seed=1))]
    assert all(accepted) and b.notices == []


def test_budget_halts_commits_when_exceeded_and_raises_notice():
    """CLAUDE.md Phase 2 'done when' (c): the drift budget halts commits when exceeded."""
    b = DriftBudget(FEATS, boot_rows(), b_daily=0.5, b_total=100.0)
    shifted = [{"vol": 160.0, "div": 5.0}] * 2880  # 6 IQR-ish above the bootstrap median, all on day 0
    accepted = [b.try_commit(i * W, r) for i, r in enumerate(shifted)]
    first_refusal = accepted.index(False)
    assert 0 < first_refusal < 2880
    assert not any(accepted[first_refusal:])  # halted for the rest of the day
    (notice,) = b.notices
    assert (notice.kind, notice.message) == ("daily", NOTICE) and notice.drift > 0.5
    # Next day commits resume, until the daily budget trips again.
    assert b.try_commit(DAY + 1, shifted[0])


def test_refused_commit_leaves_the_profile_unchanged():
    # One window barely moves a median of 600 (that robustness is the point), so use a tiny budget.
    b = DriftBudget(FEATS, boot_rows(), b_daily=1e-12, b_total=100.0)
    before = b.fast.counts.copy()
    assert not b.try_commit(0.0, {"vol": 1e6, "div": 1e6})
    np.testing.assert_array_equal(b.fast.counts, before)


def test_many_small_days_trip_the_cumulative_budget():
    """Boiling frog: each day's shift is within b_daily, but the total vs the anchor is not."""
    b = DriftBudget(FEATS, boot_rows(), b_daily=0.6, b_total=2.0, fast_half_life_days=0.5)
    halted_on = None
    for day in range(30):
        level = 100 + 3.0 * day  # ramps 3 units/day (scale ~13), slow enough for the daily budget
        for i in range(2880):
            if not b.try_commit(day * DAY + i * W, {"vol": level, "div": 5.0}) and halted_on is None:
                halted_on = day
    kinds = {n.kind for n in b.notices}
    assert "cumulative" in kinds and b.halted_total
    assert halted_on is not None and halted_on > 1  # it took several within-budget days
    assert all(row["daily_shift"] <= 0.6 + 1e-9 for row in b.daily_log)
    b.rebase()
    assert not b.halted_total


# -- anchor ---------------------------------------------------------------------------

class CountingDetector:
    def __init__(self):
        self.learned = 0

    def bootstrap(self, xs):
        self.boot = len(xs)

    def score_one(self, x):
        return x.get("s", 0.0)

    def learn_one(self, x):
        self.learned += 1


def test_frozen_anchor_never_learns():
    a = AnchorModel(CountingDetector(), boot_rows(10), update_every_s=None)
    for i in range(100):
        a.observe_commit(i * DAY, {"vol": 1.0})
        a.tick(i * DAY)
    assert a.detector.learned == 0


def test_weekly_anchor_learns_clean_periods_only():
    week = 7 * DAY
    a = AnchorModel(CountingDetector(), boot_rows(10), update_every_s=week)
    for i in range(5):
        a.observe_commit(i * DAY, {"vol": 1.0})
    assert a.tick(week + 1) and a.detector.learned == 5  # clean week -> learned at the boundary
    for i in range(3):
        a.observe_commit(week + i * DAY, {"vol": 1.0})
    a.observe_alarm(week + 4 * DAY)
    assert not a.tick(2 * week + 1)
    assert a.detector.learned == 5 and a.skipped_updates == 1


# -- quarantine + budget --------------------------------------------------------------

class ScoreField:
    def __init__(self):
        self.learned = []

    def bootstrap(self, xs):
        pass

    def score_one(self, x):
        return x["s"]

    def learn_one(self, x):
        self.learned.append(x["vol"])


def test_quarantine_blocks_commits_the_budget_refuses():
    profile = ProfileCache()
    budget = DriftBudget(FEATS, boot_rows(), b_daily=0.3, b_total=100.0)
    det = ScoreField()
    q = QuarantinedLearner(det, QuarantineConfig(tau_admit=0.5, tau_alert=0.9, t_delay_s=2 * W), profile=profile,
                           window_s=W, gate=budget.try_commit)
    for i in range(400):
        x = {"vol": 160.0, "div": 5.0, "s": 0.1}  # scores benign, but shifts the profile
        q.process(i * W, x, WindowObservation(i * W, dst_ips=(f"10.0.{i // 250}.{i % 250}",)))
    outcomes = list(q.outcome.values())
    assert COMMITTED in outcomes and BLOCKED in outcomes
    assert q.stats.blocked > 0 and len(det.learned) == q.stats.committed
    blocked_t = [t for t, d in q.outcome.items() if d == BLOCKED]
    i = int(blocked_t[0] / W)
    assert not profile.has_ip(f"10.0.{i // 250}.{i % 250}")  # blocked windows never reach the cache



def test_capped_mean_measure_is_not_dominated_by_a_near_constant_feature():
    from rad.continual.drift_budget import drift_measure
    scale = np.array([1.0, 1.0, 1e-6])
    m, ref = np.array([0.5, 0.5, 1.0]), np.zeros(3)
    assert drift_measure(m, ref, scale) > 1e5  # the sum explodes on the degenerate feature
    assert drift_measure(m, ref, scale, "capped_mean", 3.0) == pytest.approx((0.5 + 0.5 + 3.0) / 3)
