# regress i3

## Means per dataset and detector

| dataset | detector | detection_rate@tau | event_detection@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 0.9418 | 1 | 815.1 | 0.9284 | 0.964 |
| kitsune_suite | hst_slog | 0.966 | 1 | 560.5 | 0.6888 | 0.8436 |
| kitsune_suite | iforest_ext_sparse_slog | 0.926 | 1 | 744.1 | 0.9102 | 0.9549 |
| kitsune_suite | kitnet | 1 | 1 | 1128 | 0.96 | 0.9799 |
| kitsune_suite | mad_tail_slog | 0.8892 | 1 | 159.6 | 0.926 | 0.9628 |
| kitsune_suite | robust_z_router | 0.9313 | 1 | 180 | 0.9155 | 0.9575 |
| mirai | autoencoder_slog | 1 | 1 | 65.45 | 1 | 1 |
| mirai | hst_slog | 1 | 1 | 0 | 1 | 1 |
| mirai | iforest_ext_sparse_slog | 1 | 1 | 65.45 | 1 | 1 |
| mirai | kitnet | 1 | 1 | 65.45 | 1 | 1 |
| mirai | mad_tail_slog | 1 | 1 | 65.45 | 1 | 1 |
| mirai | robust_z_router | 1 | 1 | 0 | 1 | 1 |
| unsw | autoencoder_slog | 0.6898 | 0.7295 | 6.878 | 0.4873 | 0.8608 |
| unsw | hst_slog | 0.1225 | 0.2868 | 1.262 | 0.1792 | 0.6581 |
| unsw | iforest_ext_sparse_slog | 0.4731 | 0.6755 | 4.289 | 0.4374 | 0.8542 |
| unsw | kitnet | 0.7904 | 0.8189 | 6.159 | 0.5828 | 0.865 |
| unsw | mad_tail_slog | 0.854 | 0.8689 | 7.414 | 0.5828 | 0.9104 |
| unsw | robust_z_router | 0.8071 | 0.8356 | 6.976 | 0.6295 | 0.9047 |
| unsw_late | autoencoder_slog | 0.6691 | 0.7914 | 39.83 | 0.6423 | 0.8493 |
| unsw_late | hst_slog | 0.2024 | 0.4238 | 37.87 | 0.3365 | 0.6973 |
| unsw_late | iforest_ext_sparse_slog | 0.679 | 0.7533 | 38.46 | 0.7803 | 0.9039 |
| unsw_late | kitnet | 0.8686 | 0.9514 | 2.32 | 0.891 | 0.9313 |
| unsw_late | mad_tail_slog | 0.8766 | 0.9514 | 4.701 | 0.8808 | 0.9624 |
| unsw_late | robust_z_router | 0.8526 | 0.9514 | 40.72 | 0.8758 | 0.9379 |
| unsw_oct | autoencoder_slog | 0.6974 | 0.8152 | 45.24 | 0.5156 | 0.784 |
| unsw_oct | hst_slog | 0.4861 | 0.7609 | 12.83 | 0.4536 | 0.7588 |
| unsw_oct | iforest_ext_sparse_slog | 0.5287 | 0.8804 | 63.91 | 0.2774 | 0.7303 |
| unsw_oct | kitnet | 0.8058 | 0.8767 | 58.31 | 0.6616 | 0.8599 |
| unsw_oct | mad_tail_slog | 0.3541 | 0.442 | 496.1 | 0.1002 | 0.6588 |
| unsw_oct | robust_z_router | 0.8767 | 0.959 | 26.57 | 0.5735 | 0.803 |
