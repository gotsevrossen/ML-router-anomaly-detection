# regress ref

## Means per dataset and detector

| dataset | detector | detection_rate@tau | test_fpr@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 0.9131 | nan | 812.1 | 0.9232 | 0.9614 |
| kitsune_suite | hst_slog | 0.9115 | nan | 790.1 | 0.7033 | 0.8509 |
| kitsune_suite | iforest_ext_sparse_slog | 0.9167 | nan | 849 | 0.8763 | 0.9378 |
| kitsune_suite | kitnet | 0.9636 | nan | 1111 | 0.9418 | 0.9708 |
| kitsune_suite | mad_tail_slog | 0.9268 | nan | 794.9 | 0.871 | 0.9352 |
| kitsune_suite | robust_z_router | 0.9115 | nan | 894.4 | 0.8921 | 0.9458 |
| mirai | autoencoder_slog | 1 | nan | 65.45 | 1 | 1 |
| mirai | hst_slog | 1 | nan | 0 | 1 | 1 |
| mirai | iforest_ext_sparse_slog | 1 | nan | 65.45 | 1 | 1 |
| mirai | kitnet | 1 | nan | 65.45 | 1 | 1 |
| mirai | mad_tail_slog | 1 | nan | 65.45 | 1 | 1 |
| mirai | robust_z_router | 1 | nan | 65.45 | 1 | 1 |
| nbaiot | autoencoder_slog | 0.7118 | 0.0008076 | nan | 0.7198 | 0.9087 |
| nbaiot | hst_slog | 0.1955 | 0.0005067 | nan | 0.2154 | 0.6831 |
| nbaiot | iforest_ext_sparse_slog | 0.6257 | 0.0006637 | nan | 0.6782 | 0.8978 |
| nbaiot | kitnet | 0.7992 | 0.000962 | nan | 0.8216 | 0.92 |
| nbaiot | mad_tail_slog | 0.8209 | 0.0006309 | nan | 0.8876 | 0.9787 |
| nbaiot | robust_z_router | 0.8886 | 0.001216 | nan | 0.822 | 0.9793 |
| unsw | autoencoder_slog | 0.5804 | nan | 4.56 | 0.5226 | 0.839 |
| unsw | hst_slog | 0.02248 | nan | 1.179 | 0.04301 | 0.632 |
| unsw | iforest_ext_sparse_slog | 0.4986 | nan | 4.372 | 0.4318 | 0.8386 |
| unsw | kitnet | 0.7044 | nan | 4.274 | 0.6203 | 0.8425 |
| unsw | mad_tail_slog | 0.7238 | nan | 7.226 | 0.4825 | 0.8505 |
| unsw | robust_z_router | 0.6957 | nan | 5.943 | 0.6247 | 0.882 |
| unsw_oct | autoencoder_slog | 0.7737 | nan | 21.04 | 0.6062 | 0.8151 |
| unsw_oct | hst_slog | 0.2854 | nan | 9.548 | 0.3003 | 0.6624 |
| unsw_oct | iforest_ext_sparse_slog | 0.4415 | nan | 55.48 | 0.3063 | 0.7511 |
| unsw_oct | kitnet | 0.748 | nan | 55.89 | 0.6376 | 0.8471 |
| unsw_oct | mad_tail_slog | 0.5605 | nan | 496.9 | 0.1002 | 0.7501 |
| unsw_oct | robust_z_router | 0.8758 | nan | 24.98 | 0.6553 | 0.8454 |
