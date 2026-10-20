# adapt_unsw_oct_d60

## false_alarms_per_day

| detector | rule | chromecast | mean |
|---|---|---|---|
| ecod_router | frozen | 74.03 | 74.03 |
| ecod_router | full | 26.19 | 26.19 |
| ecod_router | gated | 26.19 | 26.19 |
| robust_z_router | frozen | 1.007 | 1.007 |
| robust_z_router | full | 1.007 | 1.007 |
| robust_z_router | gated | 1.007 | 1.007 |

## event_detection

| detector | rule | chromecast | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 0.9565 | 0.9565 |
| ecod_router | gated | 0.9565 | 0.9565 |
| robust_z_router | frozen | 0.8696 | 0.8696 |
| robust_z_router | full | 0.8696 | 0.8696 |
| robust_z_router | gated | 0.8696 | 0.8696 |

## window_detection

| detector | rule | chromecast | mean |
|---|---|---|---|
| ecod_router | frozen | 0.7199 | 0.7199 |
| ecod_router | full | 0.6667 | 0.6667 |
| ecod_router | gated | 0.6667 | 0.6667 |
| robust_z_router | frozen | 0.7376 | 0.7376 |
| robust_z_router | full | 0.7376 | 0.7376 |
| robust_z_router | gated | 0.7376 | 0.7376 |

## attack_committed

| detector | rule | chromecast | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | chromecast | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 2194 | 2194 |
| ecod_router | gated | 2228 | 2228 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 3849 | 3849 |
| robust_z_router | gated | 3868 | 3868 |

## drift_notices

| detector | rule | chromecast | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | chromecast | mean |
|---|---|---|---|
| ecod_router | frozen | 2.76 | 2.76 |
| ecod_router | full | 2.759 | 2.759 |
| ecod_router | gated | 2.759 | 2.759 |
| robust_z_router | frozen | 2.76 | 2.76 |
| robust_z_router | full | 2.757 | 2.757 |
| robust_z_router | gated | 2.757 | 2.757 |

## quiet_top_z_gt3

| detector | rule | chromecast | mean |
|---|---|---|---|
| ecod_router | frozen | 0.03572 | 0.03572 |
| ecod_router | full | 0.02921 | 0.02921 |
| ecod_router | gated | 0.02921 | 0.02921 |
| robust_z_router | frozen | 0.03927 | 0.03927 |
| robust_z_router | full | 0.0293 | 0.0293 |
| robust_z_router | gated | 0.0293 | 0.0293 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 269 | 137 | 256 | 38 | 17 | 3 |
| ecod_router | full | 248 | 128 | 90 | 14 | 8 | 5 |
| ecod_router | gated | 248 | 128 | 90 | 14 | 8 | 5 |
| robust_z_router | frozen | 300 | 116 | 2 | 2 | 1 | 0 |
| robust_z_router | full | 282 | 134 | 2 | 2 | 0 | 0 |
| robust_z_router | gated | 282 | 134 | 2 | 2 | 0 | 0 |
