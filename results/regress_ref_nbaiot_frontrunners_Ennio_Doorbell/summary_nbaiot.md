# regress_ref_nbaiot_frontrunners_Ennio_Doorbell

Rows: {'benign': 39100, 'bootstrap': 19550, 'validation': 7820, 'test_benign': 11730, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6001 | 0.6001 | 0.945 | 0.9942 | 0.581 | 0.00324 | 0.9995 | 0.4224 | 0.01087 | 1.011 |
| mad_tail_slog | 0.6 | 0 | 0.9389 | 0.9935 | 0.6094 | 0.001364 | 0.6 | 0.6347 | 0.0235 | 0.8984 |
| autoencoder_slog | 0.4585 | 0.3989 | 0.7721 | 0.9577 | 0.04717 | 0.0005115 | 0.4238 | 2.443 | 0.02865 | 8.566 |
| iforest_ext_sparse_slog | 0.4043 | 0 | 0.7505 | 0.9674 | 0.7071 | 0.0005115 | 0.0067 | 0.7105 | 0.8278 | 860.9 |
| hst_slog | 0.0015 | 0.0013 | 0.4999 | 0.753 | 0.9528 | 0.0005115 | 0.0013 | 1.649 | 0.06579 | 550.6 |
| kitnet | 0.6001 | 0.5998 | 0.7991 | 0.9668 | 0.1479 | 0.0005115 | 0.6 | 12.07 | 0.3558 | 7.111 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet |
|---|---|---|---|---|---|---|
| gafgyt/combo | 0.9995 | 0.9995 | 0.9965 | 0.0135 | 0.0005 | 0.9995 |
| gafgyt/junk | 1 | 1 | 0.999 | 0.0195 | 0.0015 | 1 |
| gafgyt/scan | 0.999 | 0.998 | 0.1225 | 0 | 0.003 | 0.998 |
| gafgyt/tcp | 0.9995 | 0.001 | 0.001 | 0 | 0.001 | 0.001 |
| gafgyt/udp | 0.9995 | 0.0015 | 0 | 0.0005 | 0.0005 | 0.0015 |
