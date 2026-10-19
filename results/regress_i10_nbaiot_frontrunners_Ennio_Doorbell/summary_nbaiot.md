# regress_i10_nbaiot_frontrunners_Ennio_Doorbell

Rows: {'benign': 39100, 'bootstrap': 19550, 'validation': 7820, 'test_benign': 11730, 'test_attack': 10000, 'features': 105}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5999 | 0.5999 | 0.9466 | 0.9942 | 0.581 | 0.00324 | 0.9993 | 0.4989 | 0.01432 | 0.9229 |
| ecod_router | 0.5998 | 0.5998 | 0.8697 | 0.9863 | 0.6952 | 0.002643 | 0.6002 | 0.3602 | 0.02326 | 159.6 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 0.9995 | 0.9995 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 0.999 | 0.9985 |
| gafgyt/tcp | 0.9995 | 0.001 |
| gafgyt/udp | 0.9985 | 0.002 |
