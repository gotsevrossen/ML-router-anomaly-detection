# regress i2 (reference: ref)

## Means per dataset and detector

| dataset | detector | detection_rate@tau | test_fpr@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 0.8691 | nan | 929.5 | 0.8791 | 0.9393 |
| kitsune_suite | hst_slog | 0.8306 | nan | 269.6 | 0.7599 | 0.8793 |
| kitsune_suite | iforest_ext_sparse_slog | 0.8246 | nan | 695.5 | 0.8973 | 0.9484 |
| kitsune_suite | kitnet | 0.9818 | nan | 1084 | 0.9418 | 0.9708 |
| kitsune_suite | mad_tail_slog | 0.7619 | nan | 115.3 | 0.7988 | 0.8992 |
| kitsune_suite | robust_z_router | 0.7495 | nan | 180 | 0.7882 | 0.8936 |
| mirai | autoencoder_slog | 1 | nan | 65.45 | 1 | 1 |
| mirai | hst_slog | 1 | nan | 65.45 | 0.9889 | 0.9944 |
| mirai | iforest_ext_sparse_slog | 1 | nan | 65.45 | 1 | 1 |
| mirai | kitnet | 1 | nan | 65.45 | 1 | 1 |
| mirai | mad_tail_slog | 1 | nan | 65.45 | 1 | 1 |
| mirai | robust_z_router | 1 | nan | 0 | 1 | 1 |
| nbaiot | autoencoder_slog | 0.7118 | 0.0008076 | nan | 0.7198 | 0.9087 |
| nbaiot | hst_slog | 0.1955 | 0.0005067 | nan | 0.2154 | 0.6831 |
| nbaiot | iforest_ext_sparse_slog | 0.6819 | 0.0006712 | nan | 0.6899 | 0.8967 |
| nbaiot | kitnet | 0.7992 | 0.000962 | nan | 0.8216 | 0.92 |
| nbaiot | mad_tail_slog | 0.8209 | 0.000593 | nan | 0.8876 | 0.9798 |
| nbaiot | robust_z_router | 0.8886 | 0.001209 | nan | 0.822 | 0.9795 |
| unsw | autoencoder_slog | 0.559 | nan | 3.83 | 0.5283 | 0.839 |
| unsw | hst_slog | 0.1471 | nan | 2.403 | 0.219 | 0.6965 |
| unsw | iforest_ext_sparse_slog | 0.4855 | nan | 4.876 | 0.4816 | 0.8318 |
| unsw | kitnet | 0.6894 | nan | 4.097 | 0.61 | 0.8357 |
| unsw | mad_tail_slog | 0.7913 | nan | 7.226 | 0.5344 | 0.8902 |
| unsw | robust_z_router | 0.6993 | nan | 5.943 | 0.6249 | 0.8816 |

## Change against the reference

| dataset | detector | caught_change_pts | fp_now | fp_ref | flag |
|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | -4.4 | 929.5 | 812.1 | DROP |
| kitsune_suite | hst_slog | -8.09 | 269.6 | 790.1 | DROP |
| kitsune_suite | iforest_ext_sparse_slog | -9.22 | 695.5 | 849 | DROP |
| kitsune_suite | kitnet | 1.82 | 1084 | 1111 |  |
| kitsune_suite | mad_tail_slog | -16.49 | 115.3 | 794.9 | DROP |
| kitsune_suite | robust_z_router | -16.2 | 180 | 894.4 | DROP |
| mirai | autoencoder_slog | 0 | 65.45 | 65.45 |  |
| mirai | hst_slog | 0 | 65.45 | 0 | FP-UP |
| mirai | iforest_ext_sparse_slog | 0 | 65.45 | 65.45 |  |
| mirai | kitnet | 0 | 65.45 | 65.45 |  |
| mirai | mad_tail_slog | 0 | 65.45 | 65.45 |  |
| mirai | robust_z_router | 0 | 0 | 65.45 |  |
| nbaiot | autoencoder_slog | 0 | 0.0008076 | 0.0008076 |  |
| nbaiot | hst_slog | 0 | 0.0005067 | 0.0005067 |  |
| nbaiot | iforest_ext_sparse_slog | 5.62 | 0.0006712 | 0.0006637 |  |
| nbaiot | kitnet | 0 | 0.000962 | 0.000962 |  |
| nbaiot | mad_tail_slog | -0 | 0.000593 | 0.0006309 |  |
| nbaiot | robust_z_router | 0 | 0.001209 | 0.001216 |  |
| unsw | autoencoder_slog | -2.14 | 3.83 | 4.56 | DROP |
| unsw | hst_slog | 12.46 | 2.403 | 1.179 | FP-UP |
| unsw | iforest_ext_sparse_slog | -1.31 | 4.876 | 4.372 |  |
| unsw | kitnet | -1.5 | 4.097 | 4.274 |  |
| unsw | mad_tail_slog | 6.75 | 7.226 | 7.226 |  |
| unsw | robust_z_router | 0.36 | 5.943 | 5.943 |  |
