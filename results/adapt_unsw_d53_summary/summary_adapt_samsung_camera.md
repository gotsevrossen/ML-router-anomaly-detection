# adapt_unsw_d53

## false_alarms_per_day

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 7.512 | 7.512 |
| ecod_router | full | 7.512 | 7.512 |
| ecod_router | gated | 7.512 | 7.512 |
| ecod_router | naive | 7.512 | 7.512 |
| robust_z_router | frozen | 6.104 | 6.104 |
| robust_z_router | full | 22.54 | 22.54 |
| robust_z_router | gated | 22.54 | 22.54 |
| robust_z_router | naive | 4.695 | 4.695 |

## event_detection

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| ecod_router | naive | 0.4848 | 0.4848 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 0.8485 | 0.8485 |
| robust_z_router | gated | 0.6364 | 0.6364 |
| robust_z_router | naive | 0.1212 | 0.1212 |

## window_detection

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0.7352 | 0.7352 |
| ecod_router | full | 0.7352 | 0.7352 |
| ecod_router | gated | 0.7352 | 0.7352 |
| ecod_router | naive | 0.2214 | 0.2214 |
| robust_z_router | frozen | 0.657 | 0.657 |
| robust_z_router | full | 0.5557 | 0.5557 |
| robust_z_router | gated | 0.4168 | 0.4168 |
| robust_z_router | naive | 0.07091 | 0.07091 |

## attack_committed

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| ecod_router | naive | 691 | 691 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 5 | 5 |
| robust_z_router | gated | 5 | 5 |
| robust_z_router | naive | 691 | 691 |

## benign_committed

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| ecod_router | naive | 6266 | 6266 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 345 | 345 |
| robust_z_router | gated | 742 | 742 |
| robust_z_router | naive | 6266 | 6266 |

## drift_notices

| detector | rule | samsung_camera | mean |
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

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 2.605 | 2.605 |
| ecod_router | full | 2.605 | 2.605 |
| ecod_router | gated | 2.605 | 2.605 |
| ecod_router | naive | 2.604 | 2.604 |
| robust_z_router | frozen | 2.605 | 2.605 |
| robust_z_router | full | 2.605 | 2.605 |
| robust_z_router | gated | 2.605 | 2.605 |
| robust_z_router | naive | 2.604 | 2.604 |

## quiet_top_z_gt3

| detector | rule | samsung_camera | mean |
|---|---|---|---|
| ecod_router | frozen | 0.001308 | 0.001308 |
| ecod_router | full | 0.001308 | 0.001308 |
| ecod_router | gated | 0.001308 | 0.001308 |
| ecod_router | naive | 0.001308 | 0.001308 |
| robust_z_router | frozen | 0.001797 | 0.001797 |
| robust_z_router | full | 0.001807 | 0.001807 |
| robust_z_router | gated | 0.001807 | 0.001807 |
| robust_z_router | naive | 0.001796 | 0.001796 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 437 | 71 | 16 | 0 | 7 | 2 |
| ecod_router | full | 437 | 71 | 16 | 0 | 7 | 2 |
| ecod_router | gated | 437 | 71 | 16 | 0 | 7 | 2 |
| ecod_router | naive | 79 | 74 | 8 | 8 | 1 | 2 |
| robust_z_router | frozen | 384 | 70 | 13 | 0 | 6 | 0 |
| robust_z_router | full | 256 | 128 | 20 | 28 | 5 | 1 |
| robust_z_router | gated | 224 | 64 | 20 | 28 | 5 | 0 |
| robust_z_router | naive | 31 | 18 | 5 | 5 | 0 | 0 |
