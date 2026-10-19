# regress_i9_nbaiot_frontrunners_Provision_PT_838_Security_Camera

Rows: {'benign': 98514, 'bootstrap': 49257, 'validation': 19702, 'test_benign': 29555, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7992 | 0.7991 | 0.9896 | 0.9988 | 0.5809 | 0.0008797 | 0.7992 | 2.086 | 0.0196 | 1.011 |
| ecod_router | 0.7997 | 0.7997 | 0.9662 | 0.9964 | 0.7077 | 0.000609 | 0.7997 | 1.117 | 0.03275 | 174.7 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 0.9995 | 0.9995 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 0.9935 | 0.999 |
| gafgyt/tcp | 0 | 0 |
| gafgyt/udp | 0 | 0 |
| mirai/ack | 0.9985 | 0.9985 |
| mirai/scan | 1 | 1 |
| mirai/syn | 1 | 1 |
| mirai/udp | 1 | 1 |
| mirai/udpplain | 1 | 1 |
