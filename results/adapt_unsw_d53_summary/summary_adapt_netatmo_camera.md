# adapt_unsw_d53

## false_alarms_per_day

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 1.75 | 1.75 |
| ecod_router | gated | 1.75 | 1.75 |
| ecod_router | naive | 1.75 | 1.75 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |
| robust_z_router | naive | 0 | 0 |

## event_detection

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| ecod_router | naive | 0.6667 | 0.6667 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |
| robust_z_router | naive | 0.7333 | 0.7333 |

## window_detection

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0.7778 | 0.7778 |
| ecod_router | full | 0.8286 | 0.8286 |
| ecod_router | gated | 0.8286 | 0.8286 |
| ecod_router | naive | 0.4222 | 0.4222 |
| robust_z_router | frozen | 0.6667 | 0.6667 |
| robust_z_router | full | 0.6667 | 0.6667 |
| robust_z_router | gated | 0.6667 | 0.6667 |
| robust_z_router | naive | 0.4476 | 0.4476 |

## attack_committed

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| ecod_router | naive | 315 | 315 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |
| robust_z_router | naive | 315 | 315 |

## benign_committed

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 1469 | 1469 |
| ecod_router | gated | 1469 | 1469 |
| ecod_router | naive | 6642 | 6642 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 3451 | 3451 |
| robust_z_router | gated | 3453 | 3453 |
| robust_z_router | naive | 6642 | 6642 |

## drift_notices

| detector | rule | netatmo_camera | mean |
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

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 2.019 | 2.019 |
| ecod_router | full | 2.019 | 2.019 |
| ecod_router | gated | 2.019 | 2.019 |
| ecod_router | naive | 2.019 | 2.019 |
| robust_z_router | frozen | 2.019 | 2.019 |
| robust_z_router | full | 2.019 | 2.019 |
| robust_z_router | gated | 2.019 | 2.019 |
| robust_z_router | naive | 2.019 | 2.019 |

## quiet_top_z_gt3

| detector | rule | netatmo_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0.0003039 | 0.0003039 |
| ecod_router | full | 0.000304 | 0.000304 |
| ecod_router | gated | 0.000304 | 0.000304 |
| ecod_router | naive | 0.000304 | 0.000304 |
| robust_z_router | frozen | 0.0003039 | 0.0003039 |
| robust_z_router | full | 0.0003039 | 0.0003039 |
| robust_z_router | gated | 0.0003039 | 0.0003039 |
| robust_z_router | naive | 0.0003039 | 0.0003039 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 205 | 40 | 0 | 0 | 0 | 3 |
| ecod_router | full | 221 | 40 | 1 | 3 | 0 | 5 |
| ecod_router | gated | 221 | 40 | 1 | 3 | 0 | 5 |
| ecod_router | naive | 94 | 39 | 1 | 3 | 0 | 6 |
| robust_z_router | frozen | 171 | 39 | 0 | 0 | 0 | 2 |
| robust_z_router | full | 171 | 39 | 0 | 0 | 0 | 2 |
| robust_z_router | gated | 171 | 39 | 0 | 0 | 0 | 2 |
| robust_z_router | naive | 107 | 34 | 0 | 0 | 0 | 2 |
