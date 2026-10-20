# regress i11 (reference: i10)

## Means per dataset and detector

| dataset | detector | detection_rate@tau | event_detection@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|---|
| kitsune_suite | ecod_router | 0.96 | 1 | 635.6 | 0.8933 | 0.9464 |
| kitsune_suite | robust_z_router | 0.9418 | 1 | 693.2 | 0.9418 | 0.9708 |
| mirai | ecod_router | 1 | 1 | 0 | 1 | 1 |
| mirai | robust_z_router | 1 | 1 | 0 | 1 | 1 |
| unsw | ecod_router | 0.7899 | 1 | 3.098 | 0.6531 | 0.9128 |
| unsw | robust_z_router | 0.6649 | 0.9631 | 5.269 | 0.5481 | 0.8681 |
| unsw_late | ecod_router | 0.8265 | 1 | 0.7226 | 0.8606 | 0.9556 |
| unsw_late | robust_z_router | 0.689 | 0.98 | 2.348 | 0.747 | 0.9171 |
| unsw_oct | ecod_router | 0.8738 | 1 | 431.6 | 0.695 | 0.9051 |
| unsw_oct | robust_z_router | 0.941 | 1 | 758.2 | 0.6543 | 0.8597 |

## Change against the reference

| dataset | detector | caught_change_pts | fp_now | fp_ref | flag |
|---|---|---|---|---|---|
| kitsune_suite | ecod_router | 0 | 635.6 | 635.6 |  |
| kitsune_suite | robust_z_router | 0 | 693.2 | 693.2 |  |
| mirai | ecod_router | 0 | 0 | 0 |  |
| mirai | robust_z_router | 0 | 0 | 0 |  |
| unsw | ecod_router | 2.11 | 3.098 | 2.654 |  |
| unsw | robust_z_router | -0.22 | 5.269 | 2.372 | FP-UP |
| unsw_late | ecod_router | 0.85 | 0.7226 | 0 | FP-UP |
| unsw_late | robust_z_router | -2.4 | 2.348 | 0.06021 | DROP FP-UP |
| unsw_oct | ecod_router | -1 | 431.6 | 351.1 |  |
| unsw_oct | robust_z_router | -1.69 | 758.2 | 1737 |  |
