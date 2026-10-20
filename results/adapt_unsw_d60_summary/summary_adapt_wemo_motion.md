# adapt_unsw_d60

## false_alarms_per_day

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## event_detection

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| robust_z_router | frozen | 0.9167 | 0.9167 |
| robust_z_router | full | 0.9167 | 0.9167 |
| robust_z_router | gated | 0.9167 | 0.9167 |

## window_detection

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 0.7495 | 0.7495 |
| ecod_router | full | 0.7495 | 0.7495 |
| ecod_router | gated | 0.7495 | 0.7495 |
| robust_z_router | frozen | 0.8032 | 0.8032 |
| robust_z_router | full | 0.8032 | 0.8032 |
| robust_z_router | gated | 0.8032 | 0.8032 |

## attack_committed

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 941 | 941 |
| ecod_router | gated | 941 | 941 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 914 | 914 |
| robust_z_router | gated | 917 | 917 |

## drift_notices

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 2.855 | 2.855 |
| ecod_router | full | 2.855 | 2.855 |
| ecod_router | gated | 2.855 | 2.855 |
| robust_z_router | frozen | 2.855 | 2.855 |
| robust_z_router | full | 2.855 | 2.855 |
| robust_z_router | gated | 2.855 | 2.855 |

## quiet_top_z_gt3

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 0.0006291 | 0.0006291 |
| ecod_router | full | 0.0006291 | 0.0006291 |
| ecod_router | gated | 0.0006291 | 0.0006291 |
| robust_z_router | frozen | 0.0006291 | 0.0006291 |
| robust_z_router | full | 0.0006291 | 0.0006291 |
| robust_z_router | gated | 0.0006291 | 0.0006291 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 234 | 143 | 0 | 0 | 2 | 4 |
| ecod_router | full | 234 | 143 | 0 | 0 | 2 | 4 |
| ecod_router | gated | 234 | 143 | 0 | 0 | 2 | 4 |
| robust_z_router | frozen | 233 | 171 | 0 | 0 | 1 | 8 |
| robust_z_router | full | 233 | 171 | 0 | 0 | 1 | 8 |
| robust_z_router | gated | 233 | 171 | 0 | 0 | 1 | 8 |
