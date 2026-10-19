# regress_i9_nbaiot_frontrunners_Samsung_SNH_1011_N_Webcam

Rows: {'benign': 52150, 'bootstrap': 26075, 'validation': 10430, 'test_benign': 15645, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5998 | 0.5814 | 0.9534 | 0.995 | 0.5867 | 0.0008949 | 0.5998 | 0.6208 | 0.01735 | 1.011 |
| ecod_router | 0.5998 | 0.5911 | 0.9111 | 0.9906 | 0.7089 | 0.0006392 | 0.5998 | 0.6067 | 0.03381 | 174.7 |

## Detection rate at tau, per attack

| attack | robust_z_router | ecod_router |
|---|---|---|
| gafgyt/combo | 0.999 | 0.999 |
| gafgyt/junk | 1 | 1 |
| gafgyt/scan | 1 | 1 |
| gafgyt/tcp | 0 | 0 |
| gafgyt/udp | 0 | 0 |
