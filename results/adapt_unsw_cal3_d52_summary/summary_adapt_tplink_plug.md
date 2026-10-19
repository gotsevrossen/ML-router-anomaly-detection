# adapt_unsw_cal3_d52

## false_alarms_per_day

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| robust_z_router | full | 2.689 | 2.689 |
| robust_z_router | gated | 2.689 | 2.689 |

## event_detection

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |

## window_detection

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| robust_z_router | full | 0.9524 | 0.9524 |
| robust_z_router | gated | 0.9501 | 0.9501 |

## attack_committed

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| robust_z_router | full | 1244 | 1244 |
| robust_z_router | gated | 1244 | 1244 |

## drift_notices

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| robust_z_router | full | 2.743 | 2.743 |
| robust_z_router | gated | 2.743 | 2.743 |

## quiet_top_z_gt3

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| robust_z_router | full | 0.003271 | 0.003271 |
| robust_z_router | gated | 0.003271 | 0.003271 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| robust_z_router | full | 273 | 147 | 3 | 3 | 4 | 20 |
| robust_z_router | gated | 272 | 147 | 3 | 3 | 4 | 20 |
