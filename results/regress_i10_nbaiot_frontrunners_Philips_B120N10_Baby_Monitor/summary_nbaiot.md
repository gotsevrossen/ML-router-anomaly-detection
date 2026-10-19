# regress_i10_nbaiot_frontrunners_Philips_B120N10_Baby_Monitor

Rows: {'benign': 175240, 'bootstrap': 87620, 'validation': 35048, 'test_benign': 52572, 'test_attack': 20000, 'features': 105}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9995 | 0.7997 | 0.994 | 0.9993 | 0.5809 | 0.0009701 | 0.9995 | 2.19 | 0.01304 | 0.9229 |
| ecod_router | 0.7998 | 0.7997 | 0.9824 | 0.9981 | 0.7104 | 0.002245 | 0.9997 | 1.74 | 0.03899 | 159.6 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 0.999 | 0.9995 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 1 | 1 |
| gafgyt/tcp | 0.9985 | 0.9985 |
| gafgyt/udp | 0.999 | 0.999 |
| mirai/ack | 0.999 | 1 |
| mirai/scan | 1 | 1 |
| mirai/syn | 1 | 1 |
| mirai/udp | 1 | 1 |
| mirai/udpplain | 0.9995 | 1 |
