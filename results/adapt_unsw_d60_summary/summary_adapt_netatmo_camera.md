# adapt_unsw_d60

## false_alarms_per_day

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0.4376 | 0.4376 |
| robust_z_router | full | 0.4376 | 0.4376 |
| robust_z_router | gated | 0.4376 | 0.4376 |

## event_detection

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |

## window_detection

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0.7778 | 0.7778 |
| ecod_router | full | 0.7778 | 0.7778 |
| ecod_router | gated | 0.7778 | 0.7778 |
| robust_z_router | frozen | 0.981 | 0.981 |
| robust_z_router | full | 0.981 | 0.981 |
| robust_z_router | gated | 0.981 | 0.981 |

## attack_committed

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 1469 | 1469 |
| ecod_router | gated | 1469 | 1469 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 1293 | 1293 |
| robust_z_router | gated | 1295 | 1295 |

## drift_notices

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 2.019 | 2.019 |
| ecod_router | full | 2.019 | 2.019 |
| ecod_router | gated | 2.019 | 2.019 |
| robust_z_router | frozen | 2.019 | 2.019 |
| robust_z_router | full | 2.019 | 2.019 |
| robust_z_router | gated | 2.019 | 2.019 |

## quiet_top_z_gt3

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0.0003039 | 0.0003039 |
| ecod_router | full | 0.0003039 | 0.0003039 |
| ecod_router | gated | 0.0003039 | 0.0003039 |
| robust_z_router | frozen | 0.000152 | 0.000152 |
| robust_z_router | full | 0.000152 | 0.000152 |
| robust_z_router | gated | 0.000152 | 0.000152 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 205 | 40 | 0 | 0 | 0 | 3 |
| ecod_router | full | 205 | 40 | 0 | 0 | 0 | 3 |
| ecod_router | gated | 205 | 40 | 0 | 0 | 0 | 3 |
| robust_z_router | frozen | 250 | 59 | 1 | 0 | 0 | 0 |
| robust_z_router | full | 250 | 59 | 1 | 0 | 0 | 0 |
| robust_z_router | gated | 250 | 59 | 1 | 0 | 0 | 0 |
