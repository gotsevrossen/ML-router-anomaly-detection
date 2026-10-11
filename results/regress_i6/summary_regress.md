# regress i6

## Means per dataset and detector

| dataset | detector | detection_rate@tau | event_detection@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 0.777 | 0.9 | 698.7 | 0.5903 | 0.8048 |
| kitsune_suite | ecod_tail | 0.7588 | 0.9 | 716.7 | 0.5353 | 0.7772 |
| kitsune_suite | hst_slog | 0.7479 | 0.9 | 951.8 | 0.4965 | 0.7577 |
| kitsune_suite | iforest_ext_sparse_slog | 0.8412 | 0.9 | 950.7 | 0.5693 | 0.7835 |
| kitsune_suite | kitnet | 0.7131 | 0.8 | 700.6 | 0.6161 | 0.8071 |
| kitsune_suite | mad_tail_slog | 0.6044 | 0.9 | 36 | 0.4711 | 0.7456 |
| kitsune_suite | robust_z_router | 0.5256 | 0.8 | 492.6 | 0.5511 | 0.7749 |
| mirai | autoencoder_slog | 0.9778 | 1 | 0 | 0.9778 | 0.9888 |
| mirai | ecod_tail | 0.9778 | 1 | 0 | 0.9778 | 0.9888 |
| mirai | hst_slog | 0.9778 | 1 | 0 | 0.9778 | 0.9888 |
| mirai | iforest_ext_sparse_slog | 0.9778 | 1 | 0 | 0.9778 | 0.9888 |
| mirai | kitnet | 0.9778 | 1 | 196.4 | 0.9778 | 0.9888 |
| mirai | mad_tail_slog | 0.9778 | 1 | 0 | 0.9778 | 0.9888 |
| mirai | robust_z_router | 0.9778 | 1 | 196.4 | 0.9778 | 0.9888 |
| unsw | autoencoder_slog | 0.8236 | 0.9447 | 10.15 | 0.5162 | 0.8828 |
| unsw | ecod_tail | 0.8613 | 0.9674 | 7.561 | 0.6038 | 0.905 |
| unsw | hst_slog | 0.5323 | 0.6525 | 7.042 | 0.3298 | 0.7857 |
| unsw | iforest_ext_sparse_slog | 0.8288 | 0.9462 | 7.214 | 0.5979 | 0.8961 |
| unsw | kitnet | 0.7483 | 0.8439 | 5.165 | 0.5482 | 0.8423 |
| unsw | mad_tail_slog | 0.8166 | 0.9205 | 4.359 | 0.5923 | 0.8925 |
| unsw | robust_z_router | 0.8422 | 0.9417 | 4.829 | 0.5642 | 0.8806 |
| unsw_late | autoencoder_slog | 0.8518 | 0.98 | 41.86 | 0.6987 | 0.8606 |
| unsw_late | ecod_tail | 0.8742 | 1 | 5.229 | 0.8839 | 0.9538 |
| unsw_late | hst_slog | 0.524 | 0.62 | 38.47 | 0.5357 | 0.7715 |
| unsw_late | iforest_ext_sparse_slog | 0.8267 | 0.96 | 40.54 | 0.7726 | 0.8933 |
| unsw_late | kitnet | 0.7988 | 0.9714 | 21.5 | 0.7988 | 0.8904 |
| unsw_late | mad_tail_slog | 0.8582 | 0.98 | 1.133 | 0.8582 | 0.925 |
| unsw_late | robust_z_router | 0.8718 | 0.98 | 38.76 | 0.8072 | 0.9017 |
| unsw_oct | autoencoder_slog | 0.9306 | 0.9891 | 205.3 | 0.6147 | 0.8373 |
| unsw_oct | ecod_tail | 0.8964 | 0.9674 | 130.2 | 0.5912 | 0.8179 |
| unsw_oct | hst_slog | 0.8492 | 0.9674 | 48.42 | 0.6157 | 0.8836 |
| unsw_oct | iforest_ext_sparse_slog | 0.8291 | 0.9348 | 470.4 | 0.4744 | 0.8037 |
| unsw_oct | kitnet | 0.7144 | 0.8602 | 23.8 | 0.6799 | 0.8491 |
| unsw_oct | mad_tail_slog | 0.9084 | 0.9891 | 590.5 | 0.3455 | 0.7076 |
| unsw_oct | robust_z_router | 0.8843 | 0.9674 | 57.43 | 0.5886 | 0.8027 |
