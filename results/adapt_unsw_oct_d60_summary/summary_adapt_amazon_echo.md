# adapt_unsw_oct_d60

## false_alarms_per_day

| detector | rule | amazon_echo | mean |
|---|---|---|---|
| ecod_router | frozen | 1615 | 1615 |
| ecod_router | full | 812.5 | 812.5 |
| ecod_router | gated | 812.5 | 812.5 |
| robust_z_router | frozen | 2432 | 2432 |
| robust_z_router | full | 2285 | 2285 |
| robust_z_router | gated | 989.6 | 989.6 |

## event_detection

| detector | rule | amazon_echo | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |

## window_detection

| detector | rule | amazon_echo | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |

## attack_committed

| detector | rule | amazon_echo | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | amazon_echo | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 812 | 812 |
| ecod_router | gated | 2963 | 2963 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 1872 | 1872 |
| robust_z_router | gated | 5101 | 5101 |

## drift_notices

| detector | rule | amazon_echo | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | amazon_echo | mean |
|---|---|---|---|
| ecod_router | frozen | 2.474 | 2.474 |
| ecod_router | full | 2.472 | 2.472 |
| ecod_router | gated | 2.472 | 2.472 |
| robust_z_router | frozen | 2.474 | 2.474 |
| robust_z_router | full | 2.474 | 2.474 |
| robust_z_router | gated | 2.474 | 2.474 |

## quiet_top_z_gt3

| detector | rule | amazon_echo | mean |
|---|---|---|---|
| ecod_router | frozen | 0.004219 | 0.004219 |
| ecod_router | full | 0.002581 | 0.002581 |
| ecod_router | gated | 0.002581 | 0.002581 |
| robust_z_router | frozen | 0.004867 | 0.004867 |
| robust_z_router | full | 0.004077 | 0.004077 |
| robust_z_router | gated | 0.001411 | 0.001411 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 139 | 49 | 3819 | 2841 | 16 | 6 |
| ecod_router | full | 139 | 49 | 2050 | 1300 | 16 | 6 |
| ecod_router | gated | 139 | 49 | 2050 | 1300 | 16 | 6 |
| robust_z_router | frozen | 139 | 49 | 5491 | 4534 | 19 | 9 |
| robust_z_router | full | 100 | 88 | 4864 | 4557 | 18 | 10 |
| robust_z_router | gated | 100 | 88 | 2095 | 1985 | 18 | 10 |
