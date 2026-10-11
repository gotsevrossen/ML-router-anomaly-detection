# regress i1

## Means per dataset and detector

| dataset | detector | detection_rate@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 0.8691 | 929.5 | 0.8791 | 0.9393 |
| kitsune_suite | hst_slog | 0.8306 | 269.6 | 0.7599 | 0.8793 |
| kitsune_suite | iforest_ext_sparse_slog | 0.8804 | 804.4 | 0.8868 | 0.9431 |
| kitsune_suite | kitnet | 0.9818 | 1084 | 0.9418 | 0.9708 |
| kitsune_suite | mad_tail_slog | 0.9268 | 794.9 | 0.871 | 0.9352 |
| kitsune_suite | robust_z_router | 0.9115 | 894.4 | 0.8921 | 0.9458 |
| mirai | autoencoder_slog | 1 | 65.45 | 1 | 1 |
| mirai | hst_slog | 1 | 65.45 | 0.9889 | 0.9944 |
| mirai | iforest_ext_sparse_slog | 1 | 65.45 | 1 | 1 |
| mirai | kitnet | 1 | 65.45 | 1 | 1 |
| mirai | mad_tail_slog | 1 | 65.45 | 1 | 1 |
| mirai | robust_z_router | 1 | 65.45 | 1 | 1 |
| unsw | autoencoder_slog | 0.559 | 3.83 | 0.5283 | 0.839 |
| unsw | hst_slog | 0.1471 | 2.403 | 0.219 | 0.6965 |
| unsw | iforest_ext_sparse_slog | 0.5507 | 5.962 | 0.4527 | 0.8421 |
| unsw | kitnet | 0.6894 | 4.097 | 0.61 | 0.8357 |
| unsw | mad_tail_slog | 0.791 | 7.226 | 0.5485 | 0.8854 |
| unsw | robust_z_router | 0.6911 | 4.816 | 0.6266 | 0.8806 |
