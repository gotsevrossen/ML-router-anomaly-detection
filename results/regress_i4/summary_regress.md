# regress i4

## Means per dataset and detector

| dataset | detector | detection_rate@tau | event_detection@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 0.9547 | 1 | 812.1 | 0.9284 | 0.964 |
| kitsune_suite | hst_slog | 0.7971 | 1 | 353.2 | 0.8791 | 0.9393 |
| kitsune_suite | iforest_ext_sparse_slog | 0.9179 | 1 | 606.5 | 0.905 | 0.9522 |
| kitsune_suite | kitnet | 1 | 1 | 1183 | 0.96 | 0.9799 |
| kitsune_suite | mad_tail_slog | 0.8892 | 1 | 132.2 | 0.8892 | 0.9451 |
| kitsune_suite | robust_z_router | 0.9155 | 1 | 36 | 0.9155 | 0.9575 |
| mirai | autoencoder_slog | 1 | 1 | 65.45 | 1 | 1 |
| mirai | hst_slog | 1 | 1 | 65.45 | 0.9889 | 0.9944 |
| mirai | iforest_ext_sparse_slog | 1 | 1 | 65.45 | 1 | 1 |
| mirai | kitnet | 1 | 1 | 0 | 1 | 1 |
| mirai | mad_tail_slog | 1 | 1 | 65.45 | 1 | 1 |
| mirai | robust_z_router | 1 | 1 | 0 | 1 | 1 |
| unsw | autoencoder_slog | 0.6606 | 0.7212 | 7.403 | 0.4831 | 0.8595 |
| unsw | hst_slog | 0.2065 | 0.3808 | 2.708 | 0.1658 | 0.6895 |
| unsw | iforest_ext_sparse_slog | 0.5835 | 0.7131 | 5.862 | 0.5628 | 0.8715 |
| unsw | kitnet | 0.8191 | 0.8356 | 5.802 | 0.611 | 0.874 |
| unsw | mad_tail_slog | 0.854 | 0.8689 | 7.235 | 0.5828 | 0.9118 |
| unsw | robust_z_router | 0.8076 | 0.8356 | 6.976 | 0.6295 | 0.9048 |
| unsw_late | autoencoder_slog | 0.6691 | 0.7914 | 39.83 | 0.6423 | 0.8493 |
| unsw_late | hst_slog | 0.2024 | 0.4238 | 37.87 | 0.3365 | 0.6973 |
| unsw_late | iforest_ext_sparse_slog | 0.679 | 0.7533 | 38.46 | 0.7803 | 0.9039 |
| unsw_late | kitnet | 0.8686 | 0.9514 | 2.32 | 0.891 | 0.9313 |
| unsw_late | mad_tail_slog | 0.8766 | 0.9514 | 4.701 | 0.8808 | 0.9624 |
| unsw_late | robust_z_router | 0.8526 | 0.9514 | 40.72 | 0.8758 | 0.9379 |
| unsw_oct | autoencoder_slog | 0.7542 | 0.8043 | 54.16 | 0.5555 | 0.792 |
| unsw_oct | hst_slog | 0.495 | 0.7115 | 16.22 | 0.3743 | 0.7362 |
| unsw_oct | iforest_ext_sparse_slog | 0.7172 | 0.8478 | 71.67 | 0.3775 | 0.7284 |
| unsw_oct | kitnet | 0.7748 | 0.896 | 29.35 | 0.7091 | 0.8669 |
| unsw_oct | mad_tail_slog | 0.3541 | 0.442 | 496.8 | 0.1002 | 0.6632 |
| unsw_oct | robust_z_router | 0.8801 | 0.959 | 29.61 | 0.5831 | 0.8018 |
