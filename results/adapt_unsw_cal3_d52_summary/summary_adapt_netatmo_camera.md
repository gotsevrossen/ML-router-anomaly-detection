# adapt_unsw_cal3_d52

## false_alarms_per_day

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## event_detection

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |

## window_detection

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| robust_z_router | full | 0.9429 | 0.9429 |
| robust_z_router | gated | 0.9429 | 0.9429 |

## attack_committed

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| robust_z_router | full | 1302 | 1302 |
| robust_z_router | gated | 1302 | 1302 |

## drift_notices

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| robust_z_router | full | 1.837 | 1.837 |
| robust_z_router | gated | 1.837 | 1.837 |

## quiet_top_z_gt3

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| robust_z_router | full | 0.0003039 | 0.0003039 |
| robust_z_router | gated | 0.0003039 | 0.0003039 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| robust_z_router | full | 241 | 56 | 0 | 0 | 1 | 13 |
| robust_z_router | gated | 241 | 56 | 0 | 0 | 1 | 13 |
