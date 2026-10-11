# regress_ref_nbaiot_frontrunners_Provision_PT_838_Security_Camera

Rows: {'benign': 98514, 'bootstrap': 49257, 'validation': 19702, 'test_benign': 29555, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7992 | 0.7991 | 0.9896 | 0.9988 | 0.5809 | 0.0008797 | 0.7992 | 0.9696 | 0.02889 | 1.011 |
| mad_tail_slog | 0.7906 | 0.04835 | 0.9463 | 0.9944 | 0.6049 | 0.0006767 | 0.7897 | 2.698 | 0.03755 | 0.8984 |
| autoencoder_slog | 0.7833 | 0.1533 | 0.8925 | 0.974 | 0.02534 | 0.0007105 | 0.756 | 4.435 | 0.02898 | 8.566 |
| iforest_ext_sparse_slog | 0.5757 | 0.0098 | 0.845 | 0.9416 | 0.5635 | 0.0008459 | 0.5521 | 1.492 | 0.7506 | 990.1 |
| hst_slog | 0.3521 | 0.0726 | 0.8196 | 0.883 | 0.9379 | 0.0007444 | 0.2281 | 3.736 | 0.06111 | 550.6 |
| kitnet | 0.9997 | 0.7997 | 0.9925 | 0.9992 | 0.1452 | 0.000609 | 0.7997 | 19.71 | 0.2254 | 6.252 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet |
|---|---|---|---|---|---|---|
| gafgyt/combo | 0.9995 | 0.9995 | 0.9985 | 0.9945 | 0.0985 | 0.9995 |
| gafgyt/junk | 1 | 1 | 0.9965 | 0.985 | 0.2675 | 1 |
| gafgyt/scan | 0.9935 | 0.9025 | 0.6115 | 0.003 | 0.0005 | 0.999 |
| gafgyt/tcp | 0 | 0 | 0 | 0 | 0 | 0 |
| gafgyt/udp | 0 | 0 | 0 | 0.0005 | 0 | 0 |
| mirai/ack | 0.9985 | 0.9985 | 0.974 | 0.993 | 0.4865 | 0.9985 |
| mirai/scan | 1 | 0.997 | 0.995 | 0.0015 | 0 | 1 |
| mirai/syn | 1 | 1 | 0.9945 | 0.544 | 0.3445 | 1 |
| mirai/udp | 1 | 1 | 0.9935 | 1 | 0.5125 | 1 |
| mirai/udpplain | 1 | 1 | 0.997 | 0.999 | 0.5715 | 1 |
