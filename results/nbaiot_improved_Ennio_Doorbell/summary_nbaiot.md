# nbaiot_improved_Ennio_Doorbell

Rows: {'benign': 39100, 'bootstrap': 19550, 'validation': 7820, 'test_benign': 11730, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| hst_slog | 0.0015 | 0.0013 | 0.4999 | 0.753 | 0.9508 | 0.000682 | 0.0015 | 6.319 | 0.1969 | 550.6 |
| hst_proj | 0.3988 | 0 | 0.7294 | 0.7805 | 0.08832 | 0.0007673 | 0.3988 | 4.14 | 0.1964 | 565.2 |
| autoencoder_slog | 0.4585 | 0.3989 | 0.7721 | 0.9577 | 0.04545 | 0.000682 | 0.4573 | 16.97 | 0.07369 | 8.566 |
| iforest_ext_slog | 0.5961 | 0 | 0.829 | 0.9821 | 0.5849 | 0.0007673 | 0.5877 | 2.533 | 1.448 | 6334 |
| iforest_ext_sparse_slog | 0.4043 | 0 | 0.7505 | 0.9674 | 0.6289 | 0.000682 | 0.4008 | 2.463 | 1.521 | 860.9 |
| mad_tail_slog | 0.6 | 0 | 0.9389 | 0.9935 | 0.6094 | 0.001364 | 0.6 | 1.336 | 0.07089 | 0.8984 |
| kitnet | 0.6001 | 0.5998 | 0.7991 | 0.9668 | 0.142 | 0.000682 | 0.6 | 51.03 | 1.456 | 7.111 |
| fusion | 0.4594 | 0 | 0.7604 | 0.9703 | 0.7281 | 0.0007673 | 0.4251 | 12.27 | 0.3352 | 620.5 |

## Detection rate at tau, per attack

| attack | hst_slog | hst_proj | autoencoder_slog | iforest_ext_slog | iforest_ext_sparse_slog | mad_tail_slog | kitnet | fusion |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0.0005 | 0.995 | 0.9965 | 0.9995 | 0.9995 | 0.9995 | 0.9995 | 0.9965 |
| gafgyt/junk | 0.0015 | 0.9985 | 0.999 | 1 | 0.9985 | 1 | 1 | 0.9985 |
| gafgyt/scan | 0.004 | 0.0005 | 0.29 | 0.9375 | 0.0045 | 0.998 | 0.998 | 0.13 |
| gafgyt/tcp | 0.001 | 0 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 | 0.0005 |
| gafgyt/udp | 0.0005 | 0 | 0 | 0.0005 | 0.0005 | 0.0015 | 0.0015 | 0 |
