# regress_i10_nbaiot_frontrunners_Ecobee_Thermostat

Rows: {'benign': 13113, 'bootstrap': 6556, 'validation': 2622, 'test_benign': 3935, 'test_attack': 20000, 'features': 105}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8001 | 0.8001 | 0.9642 | 0.9963 | 0.5895 | 0.0005083 | 0.8001 | 0.1381 | 0.01191 | 0.9229 |
| ecod_router | 0.8001 | 0.8001 | 0.8995 | 0.9575 | 0.6954 | 0.00305 | 0.8001 | 0.1263 | 0.02138 | 159.6 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 1 | 1 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 1 | 1 |
| gafgyt/tcp | 0.0005 | 0.0005 |
| gafgyt/udp | 0.0005 | 0.0005 |
| mirai/ack | 1 | 1 |
| mirai/scan | 1 | 1 |
| mirai/syn | 1 | 1 |
| mirai/udp | 1 | 1 |
| mirai/udpplain | 1 | 1 |
