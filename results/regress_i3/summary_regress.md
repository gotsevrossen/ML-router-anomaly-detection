# regress i3 (reference: i2)

## Means per dataset and detector

| dataset | detector | detection_rate@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 0.9418 | 815.1 | 0.9284 | 0.964 |
| kitsune_suite | hst_slog | 0.966 | 560.5 | 0.6888 | 0.8436 |
| kitsune_suite | iforest_ext_sparse_slog | 0.926 | 744.1 | 0.9102 | 0.9549 |
| kitsune_suite | kitnet | 1 | 1128 | 0.96 | 0.9799 |
| kitsune_suite | mad_tail_slog | 0.8892 | 159.6 | 0.926 | 0.9628 |
| kitsune_suite | robust_z_router | 0.9313 | 180 | 0.9155 | 0.9575 |
| mirai | autoencoder_slog | 1 | 65.45 | 1 | 1 |
| mirai | hst_slog | 1 | 0 | 1 | 1 |
| mirai | iforest_ext_sparse_slog | 1 | 65.45 | 1 | 1 |
| mirai | kitnet | 1 | 65.45 | 1 | 1 |
| mirai | mad_tail_slog | 1 | 65.45 | 1 | 1 |
| mirai | robust_z_router | 1 | 0 | 1 | 1 |
| unsw | autoencoder_slog | 0.6898 | 6.878 | 0.4873 | 0.8608 |
| unsw | hst_slog | 0.1225 | 1.262 | 0.1792 | 0.6581 |
| unsw | iforest_ext_sparse_slog | 0.4731 | 4.289 | 0.4374 | 0.8542 |
| unsw | kitnet | 0.7904 | 6.159 | 0.5828 | 0.865 |
| unsw | mad_tail_slog | 0.854 | 7.414 | 0.5828 | 0.9104 |
| unsw | robust_z_router | 0.8071 | 6.976 | 0.6295 | 0.9047 |

## Change against the reference

| dataset | detector | caught_change_pts | fp_now | fp_ref | flag |
|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 7.27 | 815.1 | 929.5 |  |
| kitsune_suite | hst_slog | 13.54 | 560.5 | 269.6 | FP-UP |
| kitsune_suite | iforest_ext_sparse_slog | 10.14 | 744.1 | 695.5 |  |
| kitsune_suite | kitnet | 1.82 | 1128 | 1084 |  |
| kitsune_suite | mad_tail_slog | 12.73 | 159.6 | 115.3 |  |
| kitsune_suite | robust_z_router | 18.18 | 180 | 180 |  |
| mirai | autoencoder_slog | 0 | 65.45 | 65.45 |  |
| mirai | hst_slog | 0 | 0 | 65.45 |  |
| mirai | iforest_ext_sparse_slog | 0 | 65.45 | 65.45 |  |
| mirai | kitnet | 0 | 65.45 | 65.45 |  |
| mirai | mad_tail_slog | 0 | 65.45 | 65.45 |  |
| mirai | robust_z_router | 0 | 0 | 0 |  |
| unsw | autoencoder_slog | 13.08 | 6.878 | 3.83 | FP-UP |
| unsw | hst_slog | -2.47 | 1.262 | 2.403 | DROP |
| unsw | iforest_ext_sparse_slog | 13.53 | 4.289 | 2.493 | FP-UP |
| unsw | kitnet | 10.11 | 6.159 | 4.097 | FP-UP |
| unsw | mad_tail_slog | 30.93 | 7.414 | 6.998 |  |
| unsw | robust_z_router | 10.79 | 6.976 | 5.943 |  |
