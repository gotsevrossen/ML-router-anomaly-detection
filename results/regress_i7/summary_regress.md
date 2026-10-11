# regress i7 (reference: i5)

## Means per dataset and detector

| dataset | detector | detection_rate@tau | event_detection@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 0.96 | 1 | 946.4 | 0.9495 | 0.9746 |
| kitsune_suite | ecod_tail | 0.9418 | 1 | 857.3 | 0.9155 | 0.9575 |
| kitsune_suite | hst_slog | 0.8727 | 1 | 1133 | 0.72 | 0.8593 |
| kitsune_suite | iforest_ext_sparse_slog | 0.9495 | 1 | 1047 | 0.926 | 0.9628 |
| kitsune_suite | kitnet | 1 | 1 | 1238 | 0.96 | 0.9799 |
| kitsune_suite | mad_tail_slog | 0.926 | 1 | 150.2 | 0.926 | 0.9628 |
| kitsune_suite | robust_z_router | 0.9442 | 1 | 528.6 | 0.926 | 0.9628 |
| mirai | autoencoder_slog | 1 | 1 | 65.45 | 1 | 1 |
| mirai | ecod_tail | 1 | 1 | 0 | 1 | 1 |
| mirai | hst_slog | 1 | 1 | 65.45 | 0.9889 | 0.9944 |
| mirai | iforest_ext_sparse_slog | 1 | 1 | 65.45 | 1 | 1 |
| mirai | kitnet | 1 | 1 | 196.4 | 1 | 1 |
| mirai | mad_tail_slog | 1 | 1 | 65.45 | 1 | 1 |
| mirai | robust_z_router | 1 | 1 | 196.4 | 1 | 1 |
| unsw | autoencoder_slog | 0.8804 | 0.9447 | 13.1 | 0.5529 | 0.9036 |
| unsw | ecod_tail | 0.9242 | 0.9674 | 11.16 | 0.6344 | 0.9336 |
| unsw | hst_slog | 0.5535 | 0.6791 | 8.013 | 0.2315 | 0.7471 |
| unsw | iforest_ext_sparse_slog | 0.8757 | 0.9462 | 9.182 | 0.616 | 0.9178 |
| unsw | kitnet | 0.8285 | 0.8439 | 6.964 | 0.6037 | 0.8725 |
| unsw | mad_tail_slog | 0.8799 | 0.9023 | 7.595 | 0.6363 | 0.9233 |
| unsw | robust_z_router | 0.9197 | 0.9417 | 7.609 | 0.6141 | 0.9127 |
| unsw_late | autoencoder_slog | 0.9076 | 0.98 | 44.6 | 0.7256 | 0.8802 |
| unsw_late | ecod_tail | 0.9444 | 1 | 8.321 | 0.9567 | 0.9863 |
| unsw_late | hst_slog | 0.5425 | 0.62 | 38.94 | 0.3802 | 0.7315 |
| unsw_late | iforest_ext_sparse_slog | 0.884 | 0.96 | 41.97 | 0.8083 | 0.9146 |
| unsw_late | kitnet | 0.8854 | 0.9714 | 22.99 | 0.8854 | 0.9289 |
| unsw_late | mad_tail_slog | 0.8792 | 0.9514 | 4.998 | 0.9427 | 0.9645 |
| unsw_late | robust_z_router | 0.9443 | 0.98 | 42.15 | 0.8765 | 0.9356 |
| unsw_oct | autoencoder_slog | 0.9771 | 0.9891 | 222.9 | 0.6389 | 0.8487 |
| unsw_oct | ecod_tail | 0.9359 | 0.9674 | 135.6 | 0.6014 | 0.8196 |
| unsw_oct | hst_slog | 0.8707 | 0.9674 | 51.24 | 0.6157 | 0.8861 |
| unsw_oct | iforest_ext_sparse_slog | 0.8519 | 0.9348 | 479.6 | 0.4491 | 0.7703 |
| unsw_oct | kitnet | 0.7861 | 0.896 | 46.77 | 0.6892 | 0.8613 |
| unsw_oct | mad_tail_slog | 0.9129 | 0.9891 | 596.4 | 0.3407 | 0.7073 |
| unsw_oct | robust_z_router | 0.9511 | 0.9783 | 70.68 | 0.5972 | 0.803 |

## Change against the reference

| dataset | detector | caught_change_pts | fp_now | fp_ref | flag |
|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 0.53 | 946.4 | 812.1 |  |
| kitsune_suite | ecod_tail | 4.21 | 857.3 | 687 |  |
| kitsune_suite | hst_slog | 7.56 | 1133 | 353.2 | FP-UP |
| kitsune_suite | iforest_ext_sparse_slog | 3.16 | 1047 | 606.5 | FP-UP |
| kitsune_suite | kitnet | 0 | 1238 | 1183 |  |
| kitsune_suite | mad_tail_slog | 3.68 | 150.2 | 132.2 |  |
| kitsune_suite | robust_z_router | 2.87 | 528.6 | 36 | FP-UP |
| mirai | autoencoder_slog | 0 | 65.45 | 65.45 |  |
| mirai | ecod_tail | 0 | 0 | 0 |  |
| mirai | hst_slog | 0 | 65.45 | 65.45 |  |
| mirai | iforest_ext_sparse_slog | 0 | 65.45 | 65.45 |  |
| mirai | kitnet | 0 | 196.4 | 0 | FP-UP |
| mirai | mad_tail_slog | 0 | 65.45 | 65.45 |  |
| mirai | robust_z_router | 0 | 196.4 | 0 | FP-UP |
| unsw | autoencoder_slog | 21.98 | 13.1 | 7.403 | FP-UP |
| unsw | ecod_tail | 17.18 | 11.16 | 8.045 |  |
| unsw | hst_slog | 34.7 | 8.013 | 2.708 | FP-UP |
| unsw | iforest_ext_sparse_slog | 29.22 | 9.182 | 5.862 | FP-UP |
| unsw | kitnet | 0.94 | 6.964 | 5.802 |  |
| unsw | mad_tail_slog | 2.58 | 7.595 | 7.235 |  |
| unsw | robust_z_router | 11.21 | 7.609 | 6.976 |  |
| unsw_late | autoencoder_slog | 23.86 | 44.6 | 39.83 |  |
| unsw_late | ecod_tail | 9.41 | 8.321 | 4.695 | FP-UP |
| unsw_late | hst_slog | 34.02 | 38.94 | 37.87 |  |
| unsw_late | iforest_ext_sparse_slog | 20.5 | 41.97 | 38.46 |  |
| unsw_late | kitnet | 1.68 | 22.99 | 2.32 | FP-UP |
| unsw_late | mad_tail_slog | 0.27 | 4.998 | 4.701 |  |
| unsw_late | robust_z_router | 9.17 | 42.15 | 40.72 |  |
| unsw_oct | autoencoder_slog | 22.29 | 222.9 | 54.16 | FP-UP |
| unsw_oct | ecod_tail | 17.51 | 135.6 | 21.13 | FP-UP |
| unsw_oct | hst_slog | 37.57 | 51.24 | 16.22 | FP-UP |
| unsw_oct | iforest_ext_sparse_slog | 13.47 | 479.6 | 71.67 | FP-UP |
| unsw_oct | kitnet | 1.13 | 46.77 | 29.35 | FP-UP |
| unsw_oct | mad_tail_slog | 55.87 | 596.4 | 496.8 |  |
| unsw_oct | robust_z_router | 7.1 | 70.68 | 29.61 | FP-UP |
