# adapt_unsw_oct_d60

## false_alarms_per_day

| detector | rule | ihome | mean |
|---|---|---|---|
| ecod_router | frozen | 6.472 | 6.472 |
| ecod_router | full | 6.472 | 6.472 |
| ecod_router | gated | 6.232 | 6.232 |
| robust_z_router | frozen | 2866 | 2866 |
| robust_z_router | full | 2866 | 2866 |
| robust_z_router | gated | 2866 | 2866 |

## event_detection

| detector | rule | ihome | mean |
|---|---|---|---|
| ecod_router | frozen | 1 | 1 |
| ecod_router | full | 1 | 1 |
| ecod_router | gated | 1 | 1 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |

## window_detection

| detector | rule | ihome | mean |
|---|---|---|---|
| ecod_router | frozen | 0.9365 | 0.9365 |
| ecod_router | full | 0.9365 | 0.9365 |
| ecod_router | gated | 0.9365 | 0.9365 |
| robust_z_router | frozen | 1 | 1 |
| robust_z_router | full | 1 | 1 |
| robust_z_router | gated | 1 | 1 |

## attack_committed

| detector | rule | ihome | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 0 | 0 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## benign_committed

| detector | rule | ihome | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 22 | 22 |
| ecod_router | gated | 4138 | 4138 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## drift_notices

| detector | rule | ihome | mean |
|---|---|---|---|
| ecod_router | frozen | 0 | 0 |
| ecod_router | full | 5 | 5 |
| ecod_router | gated | 0 | 0 |
| robust_z_router | frozen | 0 | 0 |
| robust_z_router | full | 0 | 0 |
| robust_z_router | gated | 0 | 0 |

## quiet_top_z_p50

| detector | rule | ihome | mean |
|---|---|---|---|
| ecod_router | frozen | 1.35 | 1.35 |
| ecod_router | full | 1.35 | 1.35 |
| ecod_router | gated | 1.35 | 1.35 |
| robust_z_router | frozen | 1.35 | 1.35 |
| robust_z_router | full | 1.35 | 1.35 |
| robust_z_router | gated | 1.35 | 1.35 |

## quiet_top_z_gt3

| detector | rule | ihome | mean |
|---|---|---|---|
| ecod_router | frozen | 0.005756 | 0.005756 |
| ecod_router | full | 0.005756 | 0.005756 |
| ecod_router | gated | 0.005839 | 0.005839 |
| robust_z_router | frozen | 0.01667 | 0.01667 |
| robust_z_router | full | 0.01667 | 0.01667 |
| robust_z_router | gated | 0.01667 | 0.01667 |

## RQ4: alerted windows by truth and state (sum over devices)

| detector | rule | alerts_attack_as_attack | alerts_attack_as_drift | alerts_benign_as_attack | alerts_benign_as_drift | alerts_guard_as_attack | alerts_guard_as_drift |
|---|---|---|---|---|---|---|---|
| ecod_router | frozen | 1 | 58 | 26 | 1 | 4 | 0 |
| ecod_router | full | 1 | 58 | 26 | 1 | 4 | 0 |
| ecod_router | gated | 1 | 58 | 25 | 1 | 4 | 0 |
| robust_z_router | frozen | 2 | 61 | 5121 | 6834 | 7 | 5 |
| robust_z_router | full | 2 | 61 | 5121 | 6834 | 7 | 5 |
| robust_z_router | gated | 2 | 61 | 5121 | 6834 | 7 | 5 |
