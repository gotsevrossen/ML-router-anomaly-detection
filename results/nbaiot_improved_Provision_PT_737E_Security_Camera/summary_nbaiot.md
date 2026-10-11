# nbaiot_improved_Provision_PT_737E_Security_Camera

Rows: {'benign': 62154, 'bootstrap': 31077, 'validation': 12430, 'test_benign': 18647, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| hst_slog | 0.216 | 0.0114 | 0.6942 | 0.8624 | 0.9414 | 0.0009653 | 0.216 | 9.305 | 0.2045 | 550.6 |
| hst_proj | 0.6448 | 0.2926 | 0.8403 | 0.8868 | 0.9307 | 0.0006435 | 0.6391 | 7.439 | 0.1892 | 565.2 |
| autoencoder_slog | 0.7749 | 0.6328 | 0.8942 | 0.9772 | 0.02773 | 0.0008044 | 0.7698 | 18.35 | 0.08284 | 8.566 |
| iforest_ext_slog | 0.7951 | 0.5427 | 0.9848 | 0.9984 | 0.5836 | 0.001073 | 0.7986 | 3.801 | 1.187 | 7080 |
| iforest_ext_sparse_slog | 0.6937 | 0.1734 | 0.8776 | 0.987 | 0.5874 | 0.00118 | 0.6987 | 3.215 | 1.222 | 1001 |
| mad_tail_slog | 0.9994 | 0.7148 | 0.9954 | 0.9995 | 0.6135 | 0.0009653 | 0.9994 | 1.989 | 0.06992 | 0.8984 |
| kitnet | 0.9999 | 0.8002 | 0.993 | 0.9993 | 0.1447 | 0.0007508 | 0.9999 | 56.18 | 1.013 | 6.498 |
| fusion | 0.9996 | 0.7048 | 0.9953 | 0.9995 | 0.7719 | 0.0009653 | 0.9995 | 20.63 | 0.3747 | 647.5 |

## Detection rate at tau, per attack

| attack | hst_slog | hst_proj | autoencoder_slog | iforest_ext_slog | iforest_ext_sparse_slog | mad_tail_slog | kitnet | fusion |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0.032 | 0.897 | 1 | 1 | 1 | 1 | 1 | 1 |
| gafgyt/junk | 0.095 | 0.7655 | 0.9995 | 0.997 | 1 | 0.995 | 1 | 0.996 |
| gafgyt/scan | 0.003 | 0.014 | 0.716 | 0.9875 | 0.0145 | 1 | 1 | 1 |
| gafgyt/tcp | 0.001 | 0 | 0.001 | 0.0015 | 0.0015 | 0.9995 | 0.9995 | 0.9995 |
| gafgyt/udp | 0 | 0 | 0 | 0 | 0.0005 | 0.9995 | 0.9995 | 0.9995 |
| mirai/ack | 0.527 | 0.9465 | 0.9945 | 1 | 0.9995 | 1 | 1 | 1 |
| mirai/scan | 0.0035 | 0.9665 | 0.992 | 1 | 0.9915 | 1 | 1 | 1 |
| mirai/syn | 0.007 | 0.821 | 0.996 | 1 | 0.9795 | 1 | 1 | 1 |
| mirai/udp | 0.5425 | 1 | 0.9995 | 1 | 1 | 1 | 1 | 1 |
| mirai/udpplain | 0.9485 | 0.9805 | 0.999 | 1 | 1 | 1 | 1 | 1 |
