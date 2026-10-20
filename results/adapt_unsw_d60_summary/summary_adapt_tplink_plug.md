# adapt_unsw_d60

## false_alarms_per_day

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 7.619 | 7.619 |
| robust_z_router | full | 7.619 | 7.619 |
| robust_z_router | gated | 7.619 | 7.619 |

## event_detection

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |

## window_detection

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0.8912 | 0.8912 |
| ecod_router | full | 0.8912 | 0.8912 |
| ecod_router | gated | 0.8912 | 0.8912 |
| robust_z_router | frozen | 0.9977 | 0.9977 |
| robust_z_router | full | 0.9977 | 0.9977 |
| robust_z_router | gated | 0.9977 | 0.9977 |

## attack_committed

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 1315 | 1315 |
| ecod_router | gated | 1316 | 1316 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 1227 | 1227 |
| robust_z_router | gated | 1227 | 1227 |

## drift_notices

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 2.743 | 2.743 |
| ecod_router | full | 2.743 | 2.743 |
| ecod_router | gated | 2.743 | 2.743 |
| robust_z_router | frozen | 2.743 | 2.743 |
| robust_z_router | full | 2.743 | 2.743 |
| robust_z_router | gated | 2.743 | 2.743 |

## quiet_top_z_gt3

| detector | rule | tplink_plug | mean |
|---|---|---|---|
| ecod_router | frozen | 0.003579 | 0.003579 |
| ecod_router | full | 0.003579 | 0.003579 |
| ecod_router | gated | 0.003579 | 0.003579 |
| robust_z_router | frozen | 0.001092 | 0.001092 |
| robust_z_router | full | 0.001092 | 0.001092 |
| robust_z_router | gated | 0.001092 | 0.001092 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 252 | 141 | 0 | 0 | 1 | 1 |
| ecod_router | full | 252 | 141 | 0 | 0 | 1 | 1 |
| ecod_router | gated | 252 | 141 | 0 | 0 | 1 | 1 |
| robust_z_router | frozen | 288 | 152 | 17 | 0 | 4 | 1 |
| robust_z_router | full | 288 | 152 | 17 | 0 | 4 | 1 |
| robust_z_router | gated | 288 | 152 | 17 | 0 | 4 | 1 |
