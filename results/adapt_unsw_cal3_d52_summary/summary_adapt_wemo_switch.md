# adapt_unsw_cal3_d52

## false_alarms_per_day

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| robust_z_router | full | 8.855 | 8.855 |
| robust_z_router | gated | 8.855 | 8.855 |

## event_detection

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| robust_z_router | full | 0.8333 | 0.8333 |
| robust_z_router | gated | 0.8333 | 0.8333 |

## window_detection

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| robust_z_router | full | 0.7778 | 0.7778 |
| robust_z_router | gated | 0.7778 | 0.7778 |

## attack_committed

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| robust_z_router | full | 1063 | 1063 |
| robust_z_router | gated | 1070 | 1070 |

## drift_notices

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| robust_z_router | full | 2.64 | 2.64 |
| robust_z_router | gated | 2.64 | 2.64 |

## quiet_top_z_gt3

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| robust_z_router | full | 0.0003084 | 0.0003084 |
| robust_z_router | gated | 0.0003084 | 0.0003084 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| robust_z_router | full | 287 | 7 | 20 | 0 | 10 | 4 |
| robust_z_router | gated | 287 | 7 | 20 | 0 | 10 | 4 |
