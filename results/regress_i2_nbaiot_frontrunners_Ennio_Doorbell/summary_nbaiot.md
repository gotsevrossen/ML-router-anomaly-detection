# regress_i2_nbaiot_frontrunners_Ennio_Doorbell

Rows: {'benign': 39100, 'bootstrap': 19550, 'validation': 7820, 'test_benign': 11730, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6001 | 0.6001 | 0.945 | 0.9942 | 0.581 | 0.00324 | 0.9995 | 0.6443 | 0.01653 | 1.011 |
| mad_tail_slog | 0.6 | 0 | 0.9483 | 0.9944 | 0.6094 | 0.001023 | 0.6 | 1.098 | 0.04485 | 0.8984 |
| autoencoder_slog | 0.4585 | 0.3989 | 0.7721 | 0.9577 | 0.04717 | 0.0005115 | 0.4238 | 3.468 | 0.04522 | 8.566 |
| iforest_ext_sparse_slog | 0.402 | 0.003 | 0.7471 | 0.9663 | 0.68 | 0.0005115 | 0.3986 | 1.234 | 0.9763 | 888.8 |
| hst_slog | 0.0015 | 0.0013 | 0.4999 | 0.753 | 0.9528 | 0.0005115 | 0.0013 | 3.304 | 0.1384 | 550.6 |
| kitnet | 0.6001 | 0.5998 | 0.7991 | 0.9668 | 0.1479 | 0.0005115 | 0.6 | 28.26 | 0.7919 | 7.111 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet |
|---|---|---|---|---|---|---|
| gafgyt/combo | 0.9995 | 0.9995 | 0.9965 | 0.993 | 0.0005 | 0.9995 |
| gafgyt/junk | 1 | 1 | 0.999 | 0.995 | 0.0015 | 1 |
| gafgyt/scan | 0.999 | 0.998 | 0.1225 | 0.0035 | 0.003 | 0.998 |
| gafgyt/tcp | 0.9995 | 0.001 | 0.001 | 0.001 | 0.001 | 0.001 |
| gafgyt/udp | 0.9995 | 0.0015 | 0 | 0.0005 | 0.0005 | 0.0015 |
