# adapt_unsw_d60

## false_alarms_per_day

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 5.756 | 5.756 |
| ecod_router | full | 5.756 | 5.756 |
| ecod_router | gated | 5.756 | 5.756 |
| robust_z_router | frozen | 11.51 | 11.51 |
| robust_z_router | full | 11.07 | 11.07 |
| robust_z_router | gated | 11.07 | 11.07 |

## event_detection

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |

## window_detection

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 0.6905 | 0.6905 |
| ecod_router | full | 0.6905 | 0.6905 |
| ecod_router | gated | 0.6905 | 0.6905 |
| robust_z_router | frozen | 0.8889 | 0.8889 |
| robust_z_router | full | 0.8889 | 0.8889 |
| robust_z_router | gated | 0.8889 | 0.8889 |

## attack_committed

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 849 | 849 |
| ecod_router | gated | 849 | 849 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 956 | 956 |
| robust_z_router | gated | 956 | 956 |

## drift_notices

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 2.641 | 2.641 |
| ecod_router | full | 2.64 | 2.64 |
| ecod_router | gated | 2.64 | 2.64 |
| robust_z_router | frozen | 2.641 | 2.641 |
| robust_z_router | full | 2.64 | 2.64 |
| robust_z_router | gated | 2.64 | 2.64 |

## quiet_top_z_gt3

| detector | rule | wemo_switch | mean |
|---|---|---|---|
| ecod_router | frozen | 0.001232 | 0.001232 |
| ecod_router | full | 0.001232 | 0.001232 |
| ecod_router | gated | 0.001232 | 0.001232 |
| robust_z_router | frozen | 0.0001543 | 0.0001543 |
| robust_z_router | full | 0.0001543 | 0.0001543 |
| robust_z_router | gated | 0.0001543 | 0.0001543 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 232 | 29 | 13 | 0 | 8 | 3 |
| ecod_router | full | 232 | 29 | 13 | 0 | 7 | 3 |
| ecod_router | gated | 232 | 29 | 13 | 0 | 7 | 3 |
| robust_z_router | frozen | 299 | 37 | 25 | 1 | 15 | 0 |
| robust_z_router | full | 299 | 37 | 24 | 1 | 15 | 0 |
| robust_z_router | gated | 299 | 37 | 24 | 1 | 15 | 0 |
