# adapt_unsw

## false_alarms_per_day

| detector | rule | netatmo_camera | samsung_camera | tplink_plug | wemo_motion | wemo_switch | mean |
|---|---|---|---|---|---|---|---|
| hst_slog_proj | frozen | 2.625 | 3.287 | 0 | 0 | 0 | 1.182 |
| hst_slog_proj | full | 2.625 | 3.287 | 0 | 0 | 0 | 1.182 |
| hst_slog_proj | gated | 2.625 | 3.287 | 0 | 0 | 0 | 1.182 |
| hst_slog_proj | naive | 1.75 | 1.878 | 0 | 0 | 0 | 0.7257 |
| robust_z_router | frozen | 1.75 | 11.74 | 1.793 | 0 | 8.855 | 4.827 |
| robust_z_router | full | 1.75 | 11.74 | 1.793 | 0 | 8.855 | 4.827 |
| robust_z_router | gated | 1.75 | 11.74 | 1.793 | 0 | 8.855 | 4.827 |
| robust_z_router | naive | 47.69 | 1.409 | 0 | 0 | 0 | 9.82 |

## event_detection

| detector | rule | netatmo_camera | samsung_camera | tplink_plug | wemo_motion | wemo_switch | mean |
|---|---|---|---|---|---|---|---|
| hst_slog_proj | frozen | 0.8667 | 0.2121 | 0 | 0 | 0 | 0.2158 |
| hst_slog_proj | full | 0.8667 | 0.2121 | 0 | 0 | 0 | 0.2158 |
| hst_slog_proj | gated | 0.8667 | 0.09091 | 0 | 0 | 0.05556 | 0.2026 |
| hst_slog_proj | naive | 0.6 | 0.0303 | 0 | 0 | 0 | 0.1261 |
| robust_z_router | frozen | 1 | 0.6364 | 1 | 0.7083 | 0.8333 | 0.8356 |
| robust_z_router | full | 1 | 0.6364 | 1 | 0.7083 | 0.8333 | 0.8356 |
| robust_z_router | gated | 1 | 0.6364 | 1 | 0.7083 | 0.8333 | 0.8356 |
| robust_z_router | naive | 1 | 0.1818 | 0.3333 | 0.04167 | 0 | 0.3114 |

## window_detection

| detector | rule | netatmo_camera | samsung_camera | tplink_plug | wemo_motion | wemo_switch | mean |
|---|---|---|---|---|---|---|---|
| hst_slog_proj | frozen | 0.8127 | 0.09117 | 0 | 0 | 0 | 0.1808 |
| hst_slog_proj | full | 0.8127 | 0.09117 | 0 | 0 | 0 | 0.1808 |
| hst_slog_proj | gated | 0.8127 | 0.05933 | 0 | 0 | 0.002646 | 0.1749 |
| hst_slog_proj | naive | 0.5238 | 0.008683 | 0 | 0 | 0 | 0.1065 |
| robust_z_router | frozen | 0.9492 | 0.6035 | 0.9524 | 0.5706 | 0.7778 | 0.7707 |
| robust_z_router | full | 0.9492 | 0.6035 | 0.9524 | 0.5706 | 0.7778 | 0.7707 |
| robust_z_router | gated | 0.9492 | 0.6035 | 0.9524 | 0.5706 | 0.7778 | 0.7707 |
| robust_z_router | naive | 0.8984 | 0.05065 | 0.04762 | 0.003976 | 0 | 0.2001 |

## attack_committed

| detector | rule | netatmo_camera | samsung_camera | tplink_plug | wemo_motion | wemo_switch | mean |
|---|---|---|---|---|---|---|---|
| hst_slog_proj | frozen | 0 | 0 | 0 | 0 | 0 | 0 |
| hst_slog_proj | full | 0 | 0 | 0 | 0 | 0 | 0 |
| hst_slog_proj | gated | 0 | 0 | 0 | 76 | 0 | 15.2 |
| hst_slog_proj | naive | 315 | 691 | 441 | 503 | 378 | 465.6 |
| robust_z_router | frozen | 0 | 0 | 0 | 0 | 0 | 0 |
| robust_z_router | full | 0 | 0 | 0 | 0 | 0 | 0 |
| robust_z_router | gated | 0 | 0 | 0 | 0 | 0 | 0 |
| robust_z_router | naive | 315 | 691 | 441 | 503 | 378 | 465.6 |

## benign_committed

| detector | rule | netatmo_camera | samsung_camera | tplink_plug | wemo_motion | wemo_switch | mean |
|---|---|---|---|---|---|---|---|
| hst_slog_proj | frozen | 0 | 0 | 0 | 0 | 0 | 0 |
| hst_slog_proj | full | 0 | 0 | 0 | 0 | 0 | 0 |
| hst_slog_proj | gated | 0 | 359 | 0 | 2290 | 853 | 700.4 |
| hst_slog_proj | naive | 6642 | 6266 | 6510 | 6454 | 6577 | 6490 |
| robust_z_router | frozen | 0 | 0 | 0 | 0 | 0 | 0 |
| robust_z_router | full | 0 | 0 | 0 | 0 | 0 | 0 |
| robust_z_router | gated | 355 | 0 | 0 | 359 | 357 | 214.2 |
| robust_z_router | naive | 6642 | 6266 | 6510 | 6454 | 6577 | 6490 |

## drift_notices

| detector | rule | netatmo_camera | samsung_camera | tplink_plug | wemo_motion | wemo_switch | mean |
|---|---|---|---|---|---|---|---|
| hst_slog_proj | frozen | 0 | 0 | 0 | 0 | 0 | 0 |
| hst_slog_proj | full | 0 | 1 | 0 | 1 | 1 | 0.6 |
| hst_slog_proj | gated | 0 | 0 | 0 | 0 | 0 | 0 |
| hst_slog_proj | naive | 0 | 0 | 0 | 0 | 0 | 0 |
| robust_z_router | frozen | 0 | 0 | 0 | 0 | 0 | 0 |
| robust_z_router | full | 1 | 0 | 0 | 1 | 1 | 0.6 |
| robust_z_router | gated | 0 | 0 | 0 | 0 | 0 | 0 |
| robust_z_router | naive | 0 | 0 | 0 | 0 | 0 | 0 |

