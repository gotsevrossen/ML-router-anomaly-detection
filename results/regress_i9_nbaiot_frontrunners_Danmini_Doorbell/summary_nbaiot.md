# regress_i9_nbaiot_frontrunners_Danmini_Doorbell

Rows: {'benign': 49548, 'bootstrap': 24774, 'validation': 9909, 'test_benign': 14865, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0.8002 | 0.9963 | 0.9996 | 0.581 | 0.00074 | 1 | 0.9957 | 0.02004 | 1.011 |
| ecod_router | 1 | 0.8002 | 0.9959 | 0.9996 | 0.7048 | 0.003162 | 1 | 0.8142 | 0.04282 | 165.6 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 1 | 1 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 1 | 1 |
| gafgyt/tcp | 0.9995 | 0.9995 |
| gafgyt/udp | 1 | 1 |
| mirai/ack | 1 | 1 |
| mirai/scan | 1 | 1 |
| mirai/syn | 1 | 1 |
| mirai/udp | 1 | 1 |
| mirai/udpplain | 1 | 1 |
