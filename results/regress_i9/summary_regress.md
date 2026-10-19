# regress i9 (reference: i8)

## Means per dataset and detector

| dataset | detector | detection_rate@tau | event_detection@tau | test_fpr@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|---|---|
| kitsune_suite | ecod_router | 0.96 | 1 | nan | 635.6 | 0.8933 | 0.9464 |
| kitsune_suite | robust_z_router | 0.9418 | 1 | nan | 638.4 | 0.9418 | 0.9708 |
| mirai | ecod_router | 1 | 1 | nan | 0 | 1 | 1 |
| mirai | robust_z_router | 1 | 1 | nan | 0 | 1 | 1 |
| nbaiot | ecod_router | 0.8665 | nan | 0.002159 | nan | 0.8443 | 0.9593 |
| nbaiot | robust_z_router | 0.8886 | nan | 0.001209 | nan | 0.822 | 0.9795 |
| unsw | ecod_router | 0.7688 | 1 | nan | 2.654 | 0.6495 | 0.9323 |
| unsw | robust_z_router | 0.8864 | 0.953 | nan | 6.073 | 0.6385 | 0.9315 |
| unsw_late | ecod_router | 0.818 | 1 | nan | 0 | 0.9435 | 0.9842 |
| unsw_late | robust_z_router | 0.9127 | 1 | nan | 2.85 | 0.9255 | 0.9667 |
| unsw_oct | ecod_router | 0.8838 | 1 | nan | 351.1 | 0.5097 | 0.8091 |
| unsw_oct | robust_z_router | 0.9344 | 0.9674 | nan | 1641 | 0.6447 | 0.8205 |

## Change against the reference

| dataset | detector | caught_change_pts | fp_now | fp_ref | flag |
|---|---|---|---|---|---|
| kitsune_suite | ecod_router | 1.82 | 635.6 | 857.3 |  |
| kitsune_suite | robust_z_router | -0.24 | 638.4 | 528.6 |  |
| mirai | ecod_router | 0 | 0 | 0 |  |
| mirai | robust_z_router | 0 | 0 | 196.4 |  |
| nbaiot | ecod_router | 0 | 0.002159 | 0.002159 |  |
| nbaiot | robust_z_router | 0 | 0.001209 | 0.001209 |  |
| unsw | ecod_router | -15.55 | 2.654 | 10.36 | DROP |
| unsw | robust_z_router | -3.33 | 6.073 | 7.609 | DROP |
| unsw_late | ecod_router | -12.55 | 0 | 8.325 | DROP |
| unsw_late | robust_z_router | -3.16 | 2.85 | 42.15 | DROP |
| unsw_oct | ecod_router | -5.21 | 351.1 | 141.1 | DROP FP-UP |
| unsw_oct | robust_z_router | -1.67 | 1641 | 70.68 | FP-UP |
