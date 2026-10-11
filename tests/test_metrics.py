from __future__ import annotations

import math

import numpy as np
import pytest

from rad.eval import metrics as M

Y = np.array([0, 0, 0, 0, 1, 1, 1, 1])


def test_perfect_separation():
    s = np.array([0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9])
    assert M.tpr_at_fpr(Y, s, 1e-3) == 1.0
    assert M.partial_auc(Y, s, 0.1) == pytest.approx(1.0)


def test_tpr_at_fpr_counts_only_points_within_budget():
    # One benign window outscores two attacks: at FPR 0 only the top attack is caught.
    s = np.array([0.1, 0.2, 0.3, 0.85, 0.6, 0.7, 0.8, 0.9])
    assert M.tpr_at_fpr(Y, s, 0.0) == pytest.approx(0.25)
    assert M.tpr_at_fpr(Y, s, 0.25) == pytest.approx(1.0)


def test_single_class_gives_nan():
    assert math.isnan(M.tpr_at_fpr(np.zeros(3), np.arange(3), 0.1))
    assert math.isnan(M.partial_auc(np.ones(3), np.arange(3), 0.1))


def test_threshold_from_short_validation_sits_just_above_its_max():
    tau = M.threshold_for_alarm_rate(np.array([0.2, 0.5, 0.3]), alarms_per_day=1, window_s=30)
    assert tau > 0.5 and tau == pytest.approx(0.5)
    assert M.false_alarms_per_day(np.array([0.2, 0.5, 0.3]), tau, 30) == 0.0


def test_threshold_quantile_when_validation_resolves_the_rate():
    # 2880 windows = 1 day; 2 alarms/day allows exactly the top 2 validation windows to alert.
    scores = np.arange(2880, dtype=float)
    tau = M.threshold_for_alarm_rate(scores, alarms_per_day=2, window_s=30)
    assert tau == 2878
    assert M.false_alarms_per_day(scores, tau, 30) == pytest.approx(2.0)


def test_detection_rate_and_time_to_detect():
    starts = np.arange(8) * 30.0
    s = np.array([0.1, 0.2, 0.3, 0.4, 0.3, 0.7, 0.8, 0.2])
    assert M.detection_rate(s[Y == 1], 0.5) == pytest.approx(0.5)
    assert M.time_to_detect(starts, Y, s, 0.5) == 30.0  # attack starts at window 4, first alert at 5
    assert math.isnan(M.time_to_detect(starts, Y, s, 0.95))
