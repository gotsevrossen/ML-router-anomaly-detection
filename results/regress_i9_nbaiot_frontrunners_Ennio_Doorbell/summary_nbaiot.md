# regress_i9_nbaiot_frontrunners_Ennio_Doorbell

Rows: {'benign': 39100, 'bootstrap': 19550, 'validation': 7820, 'test_benign': 11730, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6001 | 0.6001 | 0.945 | 0.9942 | 0.581 | 0.00324 | 0.9995 | 0.537 | 0.01666 | 1.011 |
| ecod_router | 0.6 | 0.6 | 0.839 | 0.9831 | 0.6952 | 0.002643 | 0.6003 | 0.5652 | 0.03499 | 174.7 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 0.9995 | 0.9995 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 0.999 | 0.999 |
| gafgyt/tcp | 0.9995 | 0.001 |
| gafgyt/udp | 0.9995 | 0.002 |
