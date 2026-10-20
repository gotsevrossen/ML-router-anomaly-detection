# adapt_unsw_oct_d60

## false_alarms_per_day

| detector | rule | hue_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 55.26 | 55.26 |
| ecod_router | full | 55.26 | 55.26 |
| ecod_router | gated | 55.26 | 55.26 |
| robust_z_router | frozen | 62.41 | 62.41 |
| robust_z_router | full | 62.41 | 62.41 |
| robust_z_router | gated | 62.41 | 62.41 |

## event_detection

| detector | rule | mean |
|---|---|---|

## window_detection

| detector | rule | mean |
|---|---|---|

## attack_committed

| detector | rule | hue_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | hue_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 665 | 665 |
| ecod_router | gated | 5319 | 5319 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 661 | 661 |
| robust_z_router | gated | 8032 | 8032 |

## drift_notices

| detector | rule | hue_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 2 | 2 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 2 | 2 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | hue_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 1.799 | 1.799 |
| ecod_router | full | 1.799 | 1.799 |
| ecod_router | gated | 1.799 | 1.799 |
| robust_z_router | frozen | 1.799 | 1.799 |
| robust_z_router | full | 1.799 | 1.799 |
| robust_z_router | gated | 1.799 | 1.799 |

## quiet_top_z_gt3

| detector | rule | hue_bulb | mean |
|---|---|---|---|
| ecod_router | frozen | 0.008601 | 0.008601 |
| ecod_router | full | 0.008601 | 0.008601 |
| ecod_router | gated | 0.008601 | 0.008601 |
| robust_z_router | frozen | 0.007101 | 0.007101 |
| robust_z_router | full | 0.007101 | 0.007101 |
| robust_z_router | gated | 0.007101 | 0.007101 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 0 | 0 | 6 | 226 | 0 | 0 |
| ecod_router | full | 0 | 0 | 6 | 226 | 0 | 0 |
| ecod_router | gated | 0 | 0 | 6 | 226 | 0 | 0 |
| robust_z_router | frozen | 0 | 0 | 31 | 231 | 0 | 0 |
| robust_z_router | full | 0 | 0 | 31 | 231 | 0 | 0 |
| robust_z_router | gated | 0 | 0 | 31 | 231 | 0 | 0 |
