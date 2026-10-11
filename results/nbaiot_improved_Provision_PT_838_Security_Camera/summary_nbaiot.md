# nbaiot_improved_Provision_PT_838_Security_Camera

Rows: {'benign': 98514, 'bootstrap': 49257, 'validation': 19702, 'test_benign': 29555, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| hst_slog | 0.3521 | 0.0726 | 0.8196 | 0.883 | 0.9379 | 0.0007444 | 0.2281 | 18.28 | 0.2555 | 550.6 |
| hst_proj | 0.1252 | 0.04705 | 0.6232 | 0.8167 | 0.9213 | 0.000812 | 0.1233 | 10.67 | 0.2246 | 565.2 |
| autoencoder_slog | 0.7833 | 0.1533 | 0.8925 | 0.974 | 0.02534 | 0.0007105 | 0.756 | 23.89 | 0.08288 | 8.566 |
| iforest_ext_slog | 0.7426 | 0.091 | 0.8835 | 0.9866 | 0.5584 | 0.0006429 | 0.6905 | 4.961 | 0.9516 | 6859 |
| iforest_ext_sparse_slog | 0.5757 | 0.0098 | 0.845 | 0.9416 | 0.5635 | 0.0008459 | 0.5521 | 2.353 | 0.9381 | 990.1 |
| mad_tail_slog | 0.7906 | 0.04835 | 0.9463 | 0.9944 | 0.6049 | 0.0006767 | 0.7897 | 2.405 | 0.04809 | 0.8984 |
| kitnet | 0.9997 | 0.7997 | 0.9925 | 0.9992 | 0.1452 | 0.000609 | 0.7997 | 42.92 | 0.4242 | 6.252 |
| fusion | 0.7922 | 0.0483 | 0.9469 | 0.9944 | 0.7653 | 0.0006767 | 0.7763 | 13.1 | 0.1512 | 690.1 |

## Detection rate at tau, per attack

| attack | hst_slog | hst_proj | autoencoder_slog | iforest_ext_slog | iforest_ext_sparse_slog | mad_tail_slog | kitnet | fusion |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0.0985 | 0.0035 | 0.9985 | 0.9925 | 0.9945 | 0.9995 | 0.9995 | 0.9995 |
| gafgyt/junk | 0.2675 | 0.0025 | 0.9965 | 0.9845 | 0.985 | 1 | 1 | 1 |
| gafgyt/scan | 0.0005 | 0.0005 | 0.6115 | 0.2905 | 0.003 | 0.9025 | 0.999 | 0.7795 |
| gafgyt/tcp | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gafgyt/udp | 0 | 0 | 0 | 0 | 0.0005 | 0 | 0 | 0.0005 |
| mirai/ack | 0.4865 | 0.2885 | 0.974 | 0.998 | 0.993 | 0.9985 | 0.9985 | 0.9985 |
| mirai/scan | 0 | 0 | 0.995 | 0.9895 | 0.0015 | 0.997 | 1 | 0.985 |
| mirai/syn | 0.3445 | 0 | 0.9945 | 0.6495 | 0.544 | 1 | 1 | 1 |
| mirai/udp | 0.5125 | 0.424 | 0.9935 | 1 | 1 | 1 | 1 | 1 |
| mirai/udpplain | 0.5715 | 0.514 | 0.997 | 1 | 0.999 | 1 | 1 | 1 |
