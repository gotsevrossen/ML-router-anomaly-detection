# regress_i9_nbaiot_frontrunners_SimpleHome_XCS7_1002_WHT_Security_Camera

Rows: {'benign': 46585, 'bootstrap': 23292, 'validation': 9317, 'test_benign': 13976, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7998 | 0.7975 | 0.9901 | 0.999 | 0.5809 | 0.001789 | 0.9997 | 0.8651 | 0.02243 | 1.011 |
| ecod_router | 0.9992 | 0.7954 | 0.9947 | 0.9994 | 0.7061 | 0.002147 | 0.9992 | 0.8186 | 0.04414 | 174.7 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 1 | 1 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 0.998 | 0.994 |
| gafgyt/tcp | 1 | 0.9995 |
| gafgyt/udp | 1 | 1 |
| mirai/ack | 1 | 1 |
| mirai/scan | 0.999 | 0.999 |
| mirai/syn | 1 | 1 |
| mirai/udp | 1 | 1 |
| mirai/udpplain | 1 | 1 |
