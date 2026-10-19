# adapt_unsw_cal3_d52

## false_alarms_per_day

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## event_detection

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| robust_z_router | full | 0.7083 | 0.7083 |
| robust_z_router | gated | 0.7083 | 0.7083 |

## window_detection

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| robust_z_router | full | 0.5706 | 0.5706 |
| robust_z_router | gated | 0.5706 | 0.5706 |

## attack_committed

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| robust_z_router | full | 1085 | 1085 |
| robust_z_router | gated | 1085 | 1085 |

## drift_notices

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| robust_z_router | full | 2.855 | 2.855 |
| robust_z_router | gated | 2.855 | 2.855 |

## quiet_top_z_gt3

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| robust_z_router | full | 0.0006291 | 0.0006291 |
| robust_z_router | gated | 0.0006291 | 0.0006291 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| robust_z_router | full | 206 | 81 | 0 | 0 | 7 | 5 |
| robust_z_router | gated | 206 | 81 | 0 | 0 | 7 | 5 |
