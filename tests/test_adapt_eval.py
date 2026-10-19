from __future__ import annotations

import pandas as pd
import pytest

from rad.eval.adapt import evaluate_records


def test_rq4_confusion_and_explanation_sanity():
    """Windows 0-9 at 30 s; an attack covers windows 3-4, the guard (60 s) windows 5-6."""
    t = [30.0 * i for i in range(10)]
    alert = [False, True, False, True, True, True, False, False, True, False]
    state = ["normal", "suspected_benign_drift", "normal", "suspected_attack", "suspected_benign_drift",
             "suspected_attack", "normal", "normal", "suspected_attack", "normal"]
    top = [[["a", z]] for z in (1.0, 9.0, 2.0, 50.0, 7.0, 6.0, 0.5, 4.0, 8.0, 2.5)]
    recs = pd.DataFrame({"t": t, "alert": alert, "state": state, "top_features": top,
                         "drift_notice": [False] * 10})
    iv = pd.DataFrame({"start": [90.0], "end": [150.0], "attack": ["Scan"]})
    ev = evaluate_records(recs, pd.Series(["rejected"] * 10), iv, 30.0, 60.0)
    assert (ev["alerts_attack_as_attack"], ev["alerts_attack_as_drift"]) == (1, 1)
    assert (ev["alerts_benign_as_attack"], ev["alerts_benign_as_drift"]) == (1, 1)
    assert (ev["alerts_guard_as_attack"], ev["alerts_guard_as_drift"]) == (1, 0)
    # Quiet benign windows (benign, not alerted): 0, 2, 7, 9 with top |z| 1, 2, 4, 2.5.
    assert ev["quiet_top_z_p50"] == pytest.approx(2.25)
    assert ev["quiet_top_z_gt3"] == pytest.approx(0.25)
