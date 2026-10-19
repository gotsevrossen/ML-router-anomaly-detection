# regress i10 (reference: i9)

## Means per dataset and detector

| dataset | detector | detection_rate@tau | event_detection@tau | test_fpr@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|---|---|
| kitsune_suite | ecod_router | 0.96 | 1 | nan | 635.6 | 0.8933 | 0.9464 |
| kitsune_suite | robust_z_router | 0.9418 | 1 | nan | 693.2 | 0.9418 | 0.9708 |
| mirai | ecod_router | 1 | 1 | nan | 0 | 1 | 1 |
| mirai | robust_z_router | 1 | 1 | nan | 0 | 1 | 1 |
| nbaiot | ecod_router | 0.7997 | nan | 0.001428 | nan | 0.7552 | 0.9515 |
| nbaiot | robust_z_router | 0.8883 | nan | 0.001243 | nan | 0.8217 | 0.9796 |
| unsw | ecod_router | 0.7688 | 1 | nan | 2.654 | 0.6495 | 0.9323 |
| unsw | robust_z_router | 0.6671 | 0.9631 | nan | 2.372 | 0.5822 | 0.8867 |
| unsw_late | ecod_router | 0.818 | 1 | nan | 0 | 0.9435 | 0.9842 |
| unsw_late | robust_z_router | 0.713 | 1 | nan | 0.06021 | 0.8408 | 0.9277 |
| unsw_oct | ecod_router | 0.8838 | 1 | nan | 351.1 | 0.5097 | 0.8091 |
| unsw_oct | robust_z_router | 0.9579 | 1 | nan | 1737 | 0.4543 | 0.7379 |

## Change against the reference

| dataset | detector | caught_change_pts | fp_now | fp_ref | flag |
|---|---|---|---|---|---|
| kitsune_suite | ecod_router | 0 | 635.6 | 635.6 |  |
| kitsune_suite | robust_z_router | 0 | 693.2 | 638.4 |  |
| mirai | ecod_router | 0 | 0 | 0 |  |
| mirai | robust_z_router | 0 | 0 | 0 |  |
| nbaiot | ecod_router | -6.68 | 0.001428 | 0.002159 | DROP |
| nbaiot | robust_z_router | -0.03 | 0.001243 | 0.001209 |  |
| unsw | ecod_router | 0 | 2.654 | 2.654 |  |
| unsw | robust_z_router | -21.93 | 2.372 | 6.073 | DROP |
| unsw_late | ecod_router | -0 | 0 | 0 |  |
| unsw_late | robust_z_router | -19.97 | 0.06021 | 2.85 | DROP |
| unsw_oct | ecod_router | 0 | 351.1 | 351.1 |  |
| unsw_oct | robust_z_router | 2.35 | 1737 | 1641 |  |
