# nbaiot_fixes_Philips_B120N10_Baby_Monitor

Rows: {'benign': 175240, 'bootstrap': 87620, 'validation': 35048, 'test_benign': 52572, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window |
|---|---|---|---|---|---|---|---|---|---|
| iforest | 0 | 0 | 0.4975 | 0.8052 | 0.8241 | 0.0006848 | 0 | 3.274 | 0.04487 |
| iforest_headroom | 0 | 0 | 0.4992 | 0.8561 | 0.7854 | 0.0006277 | 0 | 2.749 | 0.154 |
| iforest_extended | 0.7998 | 0.7997 | 0.9849 | 0.9984 | 0.7526 | 0.0007418 | 0.7998 | 1.719 | 0.8513 |
| mad | 0 | 0 | 0.4975 | 0.4737 | 0.9944 | 0.0006467 | 0 | 1.157 | 0.01184 |
| mad_tail | 0.9995 | 0.7997 | 0.997 | 0.9996 | 0.72 | 0.000875 | 0.9995 | 1.2 | 0.01171 |
| hst | 0 | 0 | 0.5447 | 0.9025 | 0.9943 | 0.0006848 | 0 | 9.094 | 0.1071 |
| autoencoder | 0.7997 | 0.7656 | 0.9744 | 0.9972 | 0.01535 | 0.0008369 | 0.7995 | 9.545 | 0.01533 |

## Detection rate at tau, per attack

| attack | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0 | 0 | 0.999 | 0 | 0.999 | 0 | 0.999 |
| gafgyt/junk | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| gafgyt/scan | 0 | 0 | 1 | 0 | 1 | 0 | 0.9975 |
| gafgyt/tcp | 0 | 0 | 0 | 0 | 0.9985 | 0 | 0 |
| gafgyt/udp | 0 | 0 | 0 | 0 | 0.999 | 0 | 0 |
| mirai/ack | 0 | 0 | 0.9995 | 0 | 0.999 | 0 | 0.999 |
| mirai/scan | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| mirai/syn | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| mirai/udp | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| mirai/udpplain | 0 | 0 | 0.9995 | 0 | 0.9995 | 0 | 0.9995 |
