# nbaiot_improved_Philips_B120N10_Baby_Monitor

Rows: {'benign': 175240, 'bootstrap': 87620, 'validation': 35048, 'test_benign': 52572, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| hst_slog | 0.0005 | 0 | 0.5104 | 0.8457 | 0.9928 | 0.0007989 | 0 | 21.93 | 0.1925 | 550.6 |
| hst_proj | 0.04545 | 0.0269 | 0.5841 | 0.923 | 0.9555 | 0.0006277 | 0.04285 | 18.12 | 0.1988 | 565.2 |
| autoencoder_slog | 0.7977 | 0.7802 | 0.9546 | 0.9952 | 0.02501 | 0.000875 | 0.7974 | 28.94 | 0.08554 | 8.566 |
| iforest_ext_slog | 0.504 | 0.4542 | 0.8456 | 0.9785 | 0.6748 | 0.0007228 | 0.4681 | 7.223 | 0.9987 | 5509 |
| iforest_ext_sparse_slog | 0.6667 | 0.4746 | 0.865 | 0.9719 | 0.6751 | 0.001065 | 0.6682 | 3.711 | 0.9796 | 776.7 |
| mad_tail_slog | 0.9996 | 0.7997 | 0.9989 | 0.9998 | 0.649 | 0.0007799 | 0.9995 | 6.523 | 0.06625 | 0.8984 |
| kitnet | 0.9997 | 0.7999 | 0.9972 | 0.9996 | 0.1537 | 0.000875 | 0.9997 | 160.9 | 1.101 | 6.178 |
| fusion | 0.7994 | 0.7887 | 0.9422 | 0.9939 | 0.7836 | 0.0007609 | 0.7992 | 44.97 | 0.3528 | 780 |

## Detection rate at tau, per attack

| attack | hst_slog | hst_proj | autoencoder_slog | iforest_ext_slog | iforest_ext_sparse_slog | mad_tail_slog | kitnet | fusion |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0 | 0.0005 | 0.999 | 0.9975 | 0.997 | 0.999 | 0.999 | 0.999 |
| gafgyt/junk | 0 | 0 | 1 | 0.9955 | 0.997 | 1 | 1 | 1 |
| gafgyt/scan | 0 | 0 | 0.9745 | 0 | 0.031 | 1 | 1 | 0.992 |
| gafgyt/tcp | 0 | 0 | 0.0005 | 0 | 0 | 0.9985 | 0.9985 | 0.0005 |
| gafgyt/udp | 0 | 0 | 0 | 0 | 0 | 0.999 | 0.999 | 0 |
| mirai/ack | 0 | 0 | 1 | 0.659 | 0.999 | 0.999 | 1 | 1 |
| mirai/scan | 0 | 0 | 1 | 0.0045 | 0.6595 | 1 | 1 | 1 |
| mirai/syn | 0 | 0 | 1 | 0.796 | 0.9985 | 1 | 1 | 1 |
| mirai/udp | 0 | 0 | 1 | 0.703 | 1 | 1 | 1 | 1 |
| mirai/udpplain | 0 | 0.428 | 1 | 0.525 | 0.9995 | 0.9995 | 1 | 1 |
