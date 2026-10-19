# regress_i10_nbaiot_frontrunners_SimpleHome_XCS7_1003_WHT_Security_Camera

Rows: {'benign': 19528, 'bootstrap': 9764, 'validation': 3905, 'test_benign': 5859, 'test_attack': 20000, 'features': 105}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7998 | 0.7998 | 0.9896 | 0.9989 | 0.581 | 0.0006827 | 0.7998 | 0.3666 | 0.01254 | 0.9229 |
| ecod_router | 0.7998 | 0.7997 | 0.9527 | 0.995 | 0.6934 | 0.0003414 | 0.7997 | 0.2603 | 0.03647 | 159.6 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 0.9985 | 0.9985 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 0.9995 | 0.9995 |
| gafgyt/tcp | 0.0005 | 0.0005 |
| gafgyt/udp | 0 | 0 |
| mirai/ack | 1 | 1 |
| mirai/scan | 0.9995 | 0.9995 |
| mirai/syn | 1 | 1 |
| mirai/udp | 1 | 1 |
| mirai/udpplain | 1 | 0.9995 |
