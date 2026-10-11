# nbaiot_frontrunners_s2_Samsung_SNH_1011_N_Webcam

Rows: {'benign': 52150, 'bootstrap': 26075, 'validation': 10430, 'test_benign': 15645, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6 | 0.5491 | 0.9519 | 0.9948 | 0.5874 | 0.0009588 | 0.6 | 0.5996 | 0.01056 | 1.011 |
| mad_tail_slog | 0.9994 | 0.9994 | 0.9985 | 0.9997 | 0.6273 | 6.392e-05 | 0.6 | 0.8158 | 0.02803 | 0.8984 |
| autoencoder_slog | 0.5828 | 0.5347 | 0.7951 | 0.9296 | 0.03859 | 0.0006392 | 0.5775 | 7.762 | 0.03381 | 8.566 |
| kitnet | 0.6003 | 0.6 | 0.7991 | 0.9259 | 0.1705 | 0.0002557 | 0.6 | 16.1 | 0.4619 | 6.396 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 0.9995 | 0.9995 | 0.9995 | 0.9995 |
| gafgyt/junk | 1 | 1 | 1 | 1 |
| gafgyt/scan | 1 | 1 | 0.8875 | 1 |
| gafgyt/tcp | 0.0005 | 0.0005 | 0.0005 | 0.0005 |
| gafgyt/udp | 0 | 0 | 0 | 0 |
