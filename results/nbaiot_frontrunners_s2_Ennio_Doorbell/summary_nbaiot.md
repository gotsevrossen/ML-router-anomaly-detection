# nbaiot_frontrunners_s2_Ennio_Doorbell

Rows: {'benign': 39100, 'bootstrap': 19550, 'validation': 7820, 'test_benign': 11730, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6005 | 0.6005 | 0.9452 | 0.9943 | 0.581 | 0.00324 | 1 | 0.3974 | 0.01043 | 1.011 |
| mad_tail_slog | 0.6005 | 0 | 0.9392 | 0.9936 | 0.6094 | 0.001364 | 0.6005 | 0.512 | 0.02452 | 0.8984 |
| autoencoder_slog | 0.4581 | 0.3985 | 0.7728 | 0.9578 | 0.04717 | 0.0005115 | 0.4248 | 5.549 | 0.03138 | 8.566 |
| kitnet | 0.6005 | 0.6004 | 0.7992 | 0.9668 | 0.1479 | 0.0005115 | 0.6005 | 13.72 | 0.3702 | 7.111 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.996 | 1 |
| gafgyt/junk | 1 | 1 | 0.9975 | 1 |
| gafgyt/scan | 1 | 1 | 0.13 | 1 |
| gafgyt/tcp | 1 | 0.0015 | 0.0005 | 0.0015 |
| gafgyt/udp | 1 | 0.001 | 0 | 0.001 |
