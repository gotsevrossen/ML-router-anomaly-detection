# regress i3 (reference: ref)

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
| unsw_oct | autoencoder_slog | 0.6974 | 45.24 | 0.5156 | 0.784 |
| unsw_oct | hst_slog | 0.4861 | 12.83 | 0.4536 | 0.7588 |
| unsw_oct | iforest_ext_sparse_slog | 0.5287 | 63.91 | 0.2774 | 0.7303 |
| unsw_oct | kitnet | 0.8058 | 58.31 | 0.6616 | 0.8599 |
| unsw_oct | mad_tail_slog | 0.3541 | 496.1 | 0.1002 | 0.6588 |
| unsw_oct | robust_z_router | 0.8767 | 26.57 | 0.5735 | 0.803 |

## Change against the reference

| dataset | detector | caught_change_pts | fp_now | fp_ref | flag |
|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 2.87 | 815.1 | 812.1 |  |
| kitsune_suite | hst_slog | 5.45 | 560.5 | 790.1 |  |
| kitsune_suite | iforest_ext_sparse_slog | 0.93 | 744.1 | 849 |  |
| kitsune_suite | kitnet | 3.64 | 1128 | 1111 |  |
| kitsune_suite | mad_tail_slog | -3.76 | 159.6 | 794.9 | DROP |
| kitsune_suite | robust_z_router | 1.98 | 180 | 894.4 |  |
| mirai | autoencoder_slog | 0 | 65.45 | 65.45 |  |
| mirai | hst_slog | 0 | 0 | 0 |  |
| mirai | iforest_ext_sparse_slog | 0 | 65.45 | 65.45 |  |
| mirai | kitnet | 0 | 65.45 | 65.45 |  |
| mirai | mad_tail_slog | 0 | 65.45 | 65.45 |  |
| mirai | robust_z_router | 0 | 0 | 65.45 |  |
| unsw | autoencoder_slog | 10.94 | 6.878 | 4.56 | FP-UP |
| unsw | hst_slog | 10 | 1.262 | 1.179 |  |
| unsw | iforest_ext_sparse_slog | -2.56 | 4.289 | 4.372 | DROP |
| unsw | kitnet | 8.6 | 6.159 | 4.274 |  |
| unsw | mad_tail_slog | 13.02 | 7.414 | 7.226 |  |
| unsw | robust_z_router | 11.15 | 6.976 | 5.943 |  |
| unsw_oct | autoencoder_slog | -7.64 | 45.24 | 21.04 | DROP FP-UP |
| unsw_oct | hst_slog | 20.07 | 12.83 | 9.548 |  |
| unsw_oct | iforest_ext_sparse_slog | 8.72 | 63.91 | 55.48 |  |
| unsw_oct | kitnet | 5.79 | 58.31 | 55.89 |  |
| unsw_oct | mad_tail_slog | -20.63 | 496.1 | 496.9 | DROP |
| unsw_oct | robust_z_router | 0.09 | 26.57 | 24.98 |  |
