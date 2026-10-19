# regress_i10_nbaiot_frontrunners_SimpleHome_XCS7_1002_WHT_Security_Camera

Rows: {'benign': 46585, 'bootstrap': 23292, 'validation': 9317, 'test_benign': 13976, 'test_attack': 20000, 'features': 105}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7982 | 0.7975 | 0.9898 | 0.9989 | 0.5809 | 0.001789 | 0.998 | 1.365 | 0.02094 | 0.9229 |
| ecod_router | 0.7975 | 0.7954 | 0.9808 | 0.998 | 0.7061 | 0.0005009 | 0.7975 | 0.7111 | 0.04223 | 159.6 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 1 | 1 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 0.998 | 0.992 |
| gafgyt/tcp | 1 | 0.0005 |
| gafgyt/udp | 1 | 0.0005 |
| mirai/ack | 1 | 1 |
| mirai/scan | 0.9825 | 0.9825 |
| mirai/syn | 1 | 1 |
| mirai/udp | 1 | 1 |
| mirai/udpplain | 1 | 1 |
