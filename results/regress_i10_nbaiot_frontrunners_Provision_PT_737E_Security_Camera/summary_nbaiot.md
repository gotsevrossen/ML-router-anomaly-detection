# regress_i10_nbaiot_frontrunners_Provision_PT_737E_Security_Camera

Rows: {'benign': 62154, 'bootstrap': 31077, 'validation': 12430, 'test_benign': 18647, 'test_attack': 20000, 'features': 105}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8001 | 0.8001 | 0.9867 | 0.9985 | 0.5809 | 0.00118 | 0.8001 | 1.088 | 0.01162 | 0.9229 |
| ecod_router | 0.8002 | 0.8002 | 0.9889 | 0.9988 | 0.7032 | 0.001394 | 0.9999 | 0.6885 | 0.03036 | 159.6 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 1 | 1 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 1 | 1 |
| gafgyt/tcp | 0.001 | 0.9995 |
| gafgyt/udp | 0 | 0.9995 |
| mirai/ack | 1 | 1 |
| mirai/scan | 1 | 1 |
| mirai/syn | 1 | 1 |
| mirai/udp | 1 | 1 |
| mirai/udpplain | 1 | 1 |
