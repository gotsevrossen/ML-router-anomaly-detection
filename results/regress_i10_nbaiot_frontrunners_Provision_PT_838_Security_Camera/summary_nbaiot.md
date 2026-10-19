# regress_i10_nbaiot_frontrunners_Provision_PT_838_Security_Camera

Rows: {'benign': 98514, 'bootstrap': 49257, 'validation': 19702, 'test_benign': 29555, 'test_attack': 20000, 'features': 105}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9983 | 0.7983 | 0.9941 | 0.999 | 0.5809 | 0.001252 | 0.9983 | 1.044 | 0.01244 | 0.9229 |
| ecod_router | 0.7998 | 0.7997 | 0.9824 | 0.9981 | 0.702 | 0.001387 | 0.7998 | 0.8514 | 0.02731 | 159.6 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 0.9995 | 0.9995 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 0.986 | 0.999 |
| gafgyt/tcp | 0.9995 | 0 |
| gafgyt/udp | 0.999 | 0.001 |
| mirai/ack | 0.999 | 0.9985 |
| mirai/scan | 1 | 1 |
| mirai/syn | 1 | 1 |
| mirai/udp | 1 | 1 |
| mirai/udpplain | 1 | 1 |
