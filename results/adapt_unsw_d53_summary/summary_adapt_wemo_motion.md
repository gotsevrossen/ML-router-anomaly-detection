# adapt_unsw_d53

## false_alarms_per_day

| detector | rule | wemo_motion | mean |
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

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| ecod_router | naive | 0.625 | 0.625 |
| robust_z_router | frozen | 0.9583 | 0.9583 |
| robust_z_router | full | 0.9583 | 0.9583 |
| robust_z_router | gated | 0.9583 | 0.9583 |
| robust_z_router | naive | 0.7083 | 0.7083 |

## window_detection

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 0.7495 | 0.7495 |
| ecod_router | full | 0.7853 | 0.7853 |
| ecod_router | gated | 0.7853 | 0.7853 |
| ecod_router | naive | 0.3837 | 0.3837 |
| robust_z_router | frozen | 0.6382 | 0.6382 |
| robust_z_router | full | 0.6382 | 0.6382 |
| robust_z_router | gated | 0.6382 | 0.6382 |
| robust_z_router | naive | 0.4513 | 0.4513 |

## attack_committed

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| ecod_router | naive | 503 | 503 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |
| robust_z_router | naive | 503 | 503 |

## benign_committed

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 941 | 941 |
| ecod_router | gated | 941 | 941 |
| ecod_router | naive | 6454 | 6454 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 3400 | 3400 |
| robust_z_router | gated | 3430 | 3430 |
| robust_z_router | naive | 6454 | 6454 |

## drift_notices

| detector | rule | wemo_motion | mean |
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

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 2.855 | 2.855 |
| ecod_router | full | 2.855 | 2.855 |
| ecod_router | gated | 2.855 | 2.855 |
| ecod_router | naive | 2.855 | 2.855 |
| robust_z_router | frozen | 2.855 | 2.855 |
| robust_z_router | full | 2.855 | 2.855 |
| robust_z_router | gated | 2.855 | 2.855 |
| robust_z_router | naive | 2.855 | 2.855 |

## quiet_top_z_gt3

| detector | rule | wemo_motion | mean |
|---|---|---|---|
| ecod_router | frozen | 0.0006291 | 0.0006291 |
| ecod_router | full | 0.0006291 | 0.0006291 |
| ecod_router | gated | 0.0006291 | 0.0006291 |
| ecod_router | naive | 0.0006291 | 0.0006291 |
| robust_z_router | frozen | 0.0006291 | 0.0006291 |
| robust_z_router | full | 0.0006291 | 0.0006291 |
| robust_z_router | gated | 0.0006291 | 0.0006291 |
| robust_z_router | naive | 0.0006291 | 0.0006291 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 234 | 143 | 0 | 0 | 2 | 4 |
| ecod_router | full | 243 | 152 | 0 | 0 | 4 | 5 |
| ecod_router | gated | 243 | 152 | 0 | 0 | 4 | 5 |
| ecod_router | naive | 94 | 99 | 0 | 0 | 1 | 3 |
| robust_z_router | frozen | 188 | 133 | 0 | 0 | 3 | 11 |
| robust_z_router | full | 188 | 133 | 0 | 0 | 3 | 11 |
| robust_z_router | gated | 188 | 133 | 0 | 0 | 3 | 11 |
| robust_z_router | naive | 119 | 108 | 0 | 0 | 2 | 10 |
