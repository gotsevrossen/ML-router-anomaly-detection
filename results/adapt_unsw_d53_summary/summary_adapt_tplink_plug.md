# adapt_unsw_d53

## false_alarms_per_day

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| ecod_router | naive | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |
| robust_z_router | naive | 0 | 0 |

## event_detection

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| ecod_router | naive | 0.2857 | 0.2857 |
| robust_z_router | frozen | 0.8571 | 0.8571 |
| robust_z_router | full | 0.8571 | 0.8571 |
| robust_z_router | gated | 0.8571 | 0.8571 |
| robust_z_router | naive | 0.2381 | 0.2381 |

## window_detection

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0.8912 | 0.8912 |
| ecod_router | full | 0.941 | 0.941 |
| ecod_router | gated | 0.941 | 0.941 |
| ecod_router | naive | 0.1338 | 0.1338 |
| robust_z_router | frozen | 0.6939 | 0.6939 |
| robust_z_router | full | 0.6939 | 0.6939 |
| robust_z_router | gated | 0.6939 | 0.6939 |
| robust_z_router | naive | 0.127 | 0.127 |

## attack_committed

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| ecod_router | naive | 441 | 441 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |
| robust_z_router | naive | 441 | 441 |

## benign_committed

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 1315 | 1315 |
| ecod_router | gated | 1316 | 1316 |
| ecod_router | naive | 6510 | 6510 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 1705 | 1705 |
| robust_z_router | gated | 1705 | 1705 |
| robust_z_router | naive | 6510 | 6510 |

## drift_notices

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| ecod_router | naive | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |
| robust_z_router | naive | 0 | 0 |

## quiet_top_z_p50

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 2.743 | 2.743 |
| ecod_router | full | 2.743 | 2.743 |
| ecod_router | gated | 2.743 | 2.743 |
| ecod_router | naive | 2.743 | 2.743 |
| robust_z_router | frozen | 2.743 | 2.743 |
| robust_z_router | full | 2.743 | 2.743 |
| robust_z_router | gated | 2.743 | 2.743 |
| robust_z_router | naive | 2.743 | 2.743 |

## quiet_top_z_gt3

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0.003579 | 0.003579 |
| ecod_router | full | 0.003579 | 0.003579 |
| ecod_router | gated | 0.003579 | 0.003579 |
| ecod_router | naive | 0.001245 | 0.001245 |
| robust_z_router | frozen | 0.003579 | 0.003579 |
| robust_z_router | full | 0.003579 | 0.003579 |
| robust_z_router | gated | 0.003579 | 0.003579 |
| robust_z_router | naive | 0.001245 | 0.001245 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 252 | 141 | 0 | 0 | 1 | 1 |
| ecod_router | full | 274 | 141 | 0 | 0 | 1 | 1 |
| ecod_router | gated | 274 | 141 | 0 | 0 | 1 | 1 |
| ecod_router | naive | 48 | 11 | 0 | 0 | 0 | 0 |
| robust_z_router | frozen | 228 | 78 | 0 | 0 | 0 | 0 |
| robust_z_router | full | 228 | 78 | 0 | 0 | 0 | 0 |
| robust_z_router | gated | 228 | 78 | 0 | 0 | 0 | 0 |
| robust_z_router | naive | 34 | 22 | 0 | 0 | 0 | 0 |
