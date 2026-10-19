# adapt_unsw_cal3_d52

## false_alarms_per_day

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| robust_z_router | full | 10.33 | 10.33 |
| robust_z_router | gated | 10.33 | 10.33 |

## event_detection

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| robust_z_router | full | 0.6364 | 0.6364 |
| robust_z_router | gated | 0.6364 | 0.6364 |

## window_detection

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| robust_z_router | full | 0.6035 | 0.6035 |
| robust_z_router | gated | 0.6035 | 0.6035 |

## attack_committed

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| robust_z_router | full | 981 | 981 |
| robust_z_router | gated | 983 | 983 |

## drift_notices

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| robust_z_router | full | 2.604 | 2.604 |
| robust_z_router | gated | 2.604 | 2.604 |

## quiet_top_z_gt3

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| robust_z_router | full | 0.0003272 | 0.0003272 |
| robust_z_router | gated | 0.0003272 | 0.0003272 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| robust_z_router | full | 374 | 43 | 20 | 2 | 5 | 17 |
| robust_z_router | gated | 374 | 43 | 20 | 2 | 5 | 17 |
