# adapt_unsw_oct_d60

## false_alarms_per_day

| detector | rule | lifx_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 4.176 | 4.176 |
| ecod_router | full | 4.176 | 4.176 |
| ecod_router | gated | 4.176 | 4.176 |
| robust_z_router | frozen | 2844 | 2844 |
| robust_z_router | full | 877.9 | 877.9 |
| robust_z_router | gated | 877.9 | 877.9 |

## event_detection

| detector | rule | lifx_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |

## window_detection

| detector | rule | lifx_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 0.879 | 0.879 |
| ecod_router | full | 0.8758 | 0.8758 |
| ecod_router | gated | 0.8758 | 0.8758 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 0.9522 | 0.9522 |
| robust_z_router | gated | 0.9522 | 0.9522 |

## attack_committed

| detector | rule | lifx_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | lifx_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 1832 | 1832 |
| ecod_router | gated | 5111 | 5111 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 2095 | 2095 |
| robust_z_router | gated | 5648 | 5648 |

## drift_notices

| detector | rule | lifx_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | lifx_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 2.2 | 2.2 |
| ecod_router | full | 1.932 | 1.932 |
| ecod_router | gated | 1.932 | 1.932 |
| robust_z_router | frozen | 2.2 | 2.2 |
| robust_z_router | full | 1.358 | 1.358 |
| robust_z_router | gated | 1.358 | 1.358 |

## quiet_top_z_gt3

| detector | rule | lifx_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 0.001367 | 0.001367 |
| ecod_router | full | 0.001367 | 0.001367 |
| ecod_router | gated | 0.001367 | 0.001367 |
| robust_z_router | frozen | 0.006757 | 0.006757 |
| robust_z_router | full | 0.0008588 | 0.0008588 |
| robust_z_router | gated | 0.0008588 | 0.0008588 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 0 | 276 | 0 | 17 | 1 | 2 |
| ecod_router | full | 0 | 275 | 0 | 17 | 1 | 2 |
| ecod_router | gated | 0 | 275 | 0 | 17 | 1 | 2 |
| robust_z_router | frozen | 0 | 314 | 1136 | 10441 | 5 | 47 |
| robust_z_router | full | 0 | 299 | 334 | 3240 | 3 | 14 |
| robust_z_router | gated | 0 | 299 | 334 | 3240 | 3 | 14 |
