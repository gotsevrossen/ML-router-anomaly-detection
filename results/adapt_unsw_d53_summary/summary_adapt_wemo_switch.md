# adapt_unsw_d53

## false_alarms_per_day

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 5.756 | 5.756 |
| ecod_router | full | 6.198 | 6.198 |
| ecod_router | gated | 5.756 | 5.756 |
| ecod_router | naive | 6.198 | 6.198 |
| robust_z_router | frozen | 5.756 | 5.756 |
| robust_z_router | full | 5.756 | 5.756 |
| robust_z_router | gated | 5.756 | 5.756 |
| robust_z_router | naive | 5.756 | 5.756 |

## event_detection

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| ecod_router | naive | 0.8333 | 0.8333 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |
| robust_z_router | naive | 1 | 1 |

## window_detection

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 0.6905 | 0.6905 |
| ecod_router | full | 0.6905 | 0.6905 |
| ecod_router | gated | 0.6905 | 0.6905 |
| ecod_router | naive | 0.5423 | 0.5423 |
| robust_z_router | frozen | 0.6799 | 0.6799 |
| robust_z_router | full | 0.6799 | 0.6799 |
| robust_z_router | gated | 0.6746 | 0.6746 |
| robust_z_router | naive | 0.6746 | 0.6746 |

## attack_committed

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| ecod_router | naive | 378 | 378 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |
| robust_z_router | naive | 378 | 378 |

## benign_committed

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 849 | 849 |
| ecod_router | gated | 849 | 849 |
| ecod_router | naive | 6577 | 6577 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 3144 | 3144 |
| robust_z_router | gated | 3145 | 3145 |
| robust_z_router | naive | 6577 | 6577 |

## drift_notices

| detector | rule | wemo_switch | mean |
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

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 2.641 | 2.641 |
| ecod_router | full | 2.64 | 2.64 |
| ecod_router | gated | 2.64 | 2.64 |
| ecod_router | naive | 2.64 | 2.64 |
| robust_z_router | frozen | 2.641 | 2.641 |
| robust_z_router | full | 2.64 | 2.64 |
| robust_z_router | gated | 2.64 | 2.64 |
| robust_z_router | naive | 2.64 | 2.64 |

## quiet_top_z_gt3

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 0.001232 | 0.001232 |
| ecod_router | full | 0.001232 | 0.001232 |
| ecod_router | gated | 0.001232 | 0.001232 |
| ecod_router | naive | 0.001232 | 0.001232 |
| robust_z_router | frozen | 0.001232 | 0.001232 |
| robust_z_router | full | 0.001232 | 0.001232 |
| robust_z_router | gated | 0.001232 | 0.001232 |
| robust_z_router | naive | 0.001232 | 0.001232 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 232 | 29 | 13 | 0 | 8 | 3 |
| ecod_router | full | 232 | 29 | 14 | 0 | 8 | 3 |
| ecod_router | gated | 232 | 29 | 13 | 0 | 7 | 3 |
| ecod_router | naive | 177 | 28 | 14 | 0 | 10 | 3 |
| robust_z_router | frozen | 231 | 26 | 13 | 0 | 14 | 2 |
| robust_z_router | full | 231 | 26 | 13 | 0 | 14 | 2 |
| robust_z_router | gated | 229 | 26 | 13 | 0 | 14 | 2 |
| robust_z_router | naive | 229 | 26 | 13 | 0 | 10 | 1 |
