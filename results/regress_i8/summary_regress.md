# regress i8

## Means per dataset and detector

| dataset | detector | detection_rate@tau | event_detection@tau | test_fpr@tau | false_alarms_per_day | tpr@fpr=0.001 | pauc@0.01 |
|---|---|---|---|---|---|---|---|
| kitsune_suite | autoencoder_slog | 0.96 | 1 | nan | 946.4 | 0.9495 | 0.9746 |
| kitsune_suite | ecod_router | 0.9418 | 1 | nan | 857.3 | 0.9155 | 0.9575 |
| kitsune_suite | ecod_tail | 0.9418 | 1 | nan | 857.3 | 0.9155 | 0.9575 |
| kitsune_suite | hst_slog | 0.8727 | 1 | nan | 1133 | 0.72 | 0.8593 |
| kitsune_suite | iforest_ext_sparse_slog | 0.9495 | 1 | nan | 1047 | 0.926 | 0.9628 |
| kitsune_suite | kitnet | 1 | 1 | nan | 1238 | 0.96 | 0.9799 |
| kitsune_suite | mad_tail_slog | 0.926 | 1 | nan | 150.2 | 0.926 | 0.9628 |
| kitsune_suite | robust_z_router | 0.9442 | 1 | nan | 528.6 | 0.926 | 0.9628 |
| mirai | autoencoder_slog | 1 | 1 | nan | 65.45 | 1 | 1 |
| mirai | ecod_router | 1 | 1 | nan | 0 | 1 | 1 |
| mirai | ecod_tail | 1 | 1 | nan | 0 | 1 | 1 |
| mirai | hst_slog | 1 | 1 | nan | 65.45 | 0.9889 | 0.9944 |
| mirai | iforest_ext_sparse_slog | 1 | 1 | nan | 65.45 | 1 | 1 |
| mirai | kitnet | 1 | 1 | nan | 196.4 | 1 | 1 |
| mirai | mad_tail_slog | 1 | 1 | nan | 65.45 | 1 | 1 |
| mirai | robust_z_router | 1 | 1 | nan | 196.4 | 1 | 1 |
| nbaiot | autoencoder_slog | 0.7118 | nan | 0.0008076 | nan | 0.7198 | 0.9087 |
| nbaiot | ecod_router | 0.8665 | nan | 0.002159 | nan | 0.8443 | 0.9593 |
| nbaiot | ecod_tail | 0.8443 | nan | 0.002303 | nan | 0.8443 | 0.9583 |
| nbaiot | hst_slog | 0.1955 | nan | 0.0005067 | nan | 0.2154 | 0.6831 |
| nbaiot | iforest_ext_sparse_slog | 0.6819 | nan | 0.0006712 | nan | 0.6899 | 0.8967 |
| nbaiot | kitnet | 0.7992 | nan | 0.000962 | nan | 0.8216 | 0.92 |
| nbaiot | mad_tail_slog | 0.8209 | nan | 0.000593 | nan | 0.8876 | 0.9798 |
| nbaiot | robust_z_router | 0.8886 | nan | 0.001209 | nan | 0.822 | 0.9795 |
| unsw | autoencoder_slog | 0.8804 | 0.9447 | nan | 13.1 | 0.5529 | 0.9036 |
| unsw | ecod_router | 0.9243 | 0.9674 | nan | 10.36 | 0.6482 | 0.934 |
| unsw | ecod_tail | 0.9242 | 0.9674 | nan | 11.16 | 0.6344 | 0.9336 |
| unsw | hst_slog | 0.5535 | 0.6791 | nan | 8.013 | 0.2315 | 0.7471 |
| unsw | iforest_ext_sparse_slog | 0.8757 | 0.9462 | nan | 9.182 | 0.616 | 0.9178 |
| unsw | kitnet | 0.8285 | 0.8439 | nan | 6.964 | 0.6037 | 0.8725 |
| unsw | mad_tail_slog | 0.8799 | 0.9023 | nan | 7.595 | 0.6363 | 0.9233 |
| unsw | robust_z_router | 0.9197 | 0.9417 | nan | 7.609 | 0.6141 | 0.9127 |
| unsw_late | autoencoder_slog | 0.9076 | 0.98 | nan | 44.6 | 0.7256 | 0.8802 |
| unsw_late | ecod_router | 0.9436 | 1 | nan | 8.325 | 0.9559 | 0.9822 |
| unsw_late | ecod_tail | 0.9444 | 1 | nan | 8.321 | 0.9567 | 0.9863 |
| unsw_late | hst_slog | 0.5425 | 0.62 | nan | 38.94 | 0.3802 | 0.7315 |
| unsw_late | iforest_ext_sparse_slog | 0.884 | 0.96 | nan | 41.97 | 0.8083 | 0.9146 |
| unsw_late | kitnet | 0.8854 | 0.9714 | nan | 22.99 | 0.8854 | 0.9289 |
| unsw_late | mad_tail_slog | 0.8792 | 0.9514 | nan | 4.998 | 0.9427 | 0.9645 |
| unsw_late | robust_z_router | 0.9443 | 0.98 | nan | 42.15 | 0.8765 | 0.9356 |
| unsw_oct | autoencoder_slog | 0.9771 | 0.9891 | nan | 222.9 | 0.6389 | 0.8487 |
| unsw_oct | ecod_router | 0.9359 | 0.9674 | nan | 141.1 | 0.583 | 0.8155 |
| unsw_oct | ecod_tail | 0.9359 | 0.9674 | nan | 135.6 | 0.6014 | 0.8196 |
| unsw_oct | hst_slog | 0.8707 | 0.9674 | nan | 51.24 | 0.6157 | 0.8861 |
| unsw_oct | iforest_ext_sparse_slog | 0.8519 | 0.9348 | nan | 479.6 | 0.4491 | 0.7703 |
| unsw_oct | kitnet | 0.7861 | 0.896 | nan | 46.77 | 0.6892 | 0.8613 |
| unsw_oct | mad_tail_slog | 0.9129 | 0.9891 | nan | 596.4 | 0.3407 | 0.7073 |
| unsw_oct | robust_z_router | 0.9511 | 0.9783 | nan | 70.68 | 0.5972 | 0.803 |
