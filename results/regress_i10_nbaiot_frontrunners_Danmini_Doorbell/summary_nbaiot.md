# regress_i10_nbaiot_frontrunners_Danmini_Doorbell

Rows: {'benign': 49548, 'bootstrap': 24774, 'validation': 9909, 'test_benign': 14865, 'test_attack': 20000, 'features': 105}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0.8002 | 0.9969 | 0.9997 | 0.581 | 0.0006727 | 1 | 0.5737 | 0.01289 | 0.9229 |
| ecod_router | 0.8002 | 0.8002 | 0.9885 | 0.9988 | 0.7048 | 0.0003364 | 0.8002 | 0.4533 | 0.02446 | 150.4 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 1 | 1 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 1 | 1 |
| gafgyt/tcp | 0.9995 | 0.001 |
| gafgyt/udp | 1 | 0.001 |
| mirai/ack | 1 | 1 |
| mirai/scan | 1 | 1 |
| mirai/syn | 1 | 1 |
| mirai/udp | 1 | 1 |
| mirai/udpplain | 1 | 1 |
