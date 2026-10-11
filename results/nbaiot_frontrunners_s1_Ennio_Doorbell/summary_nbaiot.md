# nbaiot_frontrunners_s1_Ennio_Doorbell

Rows: {'benign': 39100, 'bootstrap': 19550, 'validation': 7820, 'test_benign': 11730, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6002 | 0.6002 | 0.9451 | 0.9942 | 0.581 | 0.00324 | 0.9997 | 0.7374 | 0.01469 | 1.011 |
| mad_tail_slog | 0.6005 | 0 | 0.9392 | 0.9936 | 0.6094 | 0.001364 | 0.6005 | 0.995 | 0.03439 | 0.8984 |
| autoencoder_slog | 0.4589 | 0.3993 | 0.7725 | 0.9578 | 0.04717 | 0.0005115 | 0.4236 | 7.623 | 0.0382 | 8.566 |
| kitnet | 0.6005 | 0.6004 | 0.7992 | 0.9668 | 0.1479 | 0.0005115 | 0.6005 | 18.34 | 0.483 | 7.111 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 1 | 1 |
| gafgyt/junk | 0.9995 | 0.9995 | 0.998 | 0.9995 |
| gafgyt/scan | 1 | 1 | 0.12 | 1 |
| gafgyt/tcp | 0.999 | 0.002 | 0 | 0.002 |
| gafgyt/udp | 1 | 0.001 | 0 | 0.001 |
