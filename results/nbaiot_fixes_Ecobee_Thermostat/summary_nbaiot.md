# nbaiot_fixes_Ecobee_Thermostat

Rows: {'benign': 13113, 'bootstrap': 6556, 'validation': 2622, 'test_benign': 3935, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window |
|---|---|---|---|---|---|---|---|---|---|
| iforest | 0.00035 | 0.0003 | 0.6429 | 0.9182 | 0.6981 | 0.001017 | 0.00035 | 1.81 | 0.04446 |
| iforest_headroom | 0.0035 | 5e-05 | 0.6489 | 0.8536 | 0.6327 | 0.001271 | 0.09945 | 0.5249 | 0.1072 |
| iforest_extended | 0.7999 | 0.7999 | 0.9476 | 0.9945 | 0.622 | 0.003812 | 0.8001 | 0.8265 | 0.8261 |
| mad | 0 | 0 | 0.4975 | 0.4737 | 0.9986 | 0.001525 | 0 | 0.1264 | 0.0225 |
| mad_tail | 0.8 | 0.8 | 0.8995 | 0.962 | 0.6268 | 0.005845 | 0.8001 | 0.1959 | 0.02019 |
| hst | 0.7966 | 0.0699 | 0.8761 | 0.9343 | 0.8811 | 0.002541 | 0.7983 | 1.445 | 0.1061 |
| autoencoder | 0.8001 | 0.7991 | 0.9617 | 0.996 | 0.008725 | 0.005083 | 1 | 54.07 | 0.03738 |

## Detection rate at tau, per attack

| attack | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0 | 0 | 1 | 0 | 1 | 1 | 1 |
| gafgyt/junk | 0.0005 | 0.0015 | 1 | 0 | 1 | 1 | 1 |
| gafgyt/scan | 0.0025 | 0.0025 | 1 | 0 | 1 | 0.989 | 1 |
| gafgyt/tcp | 0 | 0 | 0.0005 | 0 | 0.0005 | 0 | 1 |
| gafgyt/udp | 0.0005 | 0.0005 | 0.0005 | 0 | 0.0005 | 0.0005 | 1 |
| mirai/ack | 0 | 0.2255 | 1 | 0 | 1 | 0.9975 | 1 |
| mirai/scan | 0 | 0 | 1 | 0 | 1 | 0.997 | 1 |
| mirai/syn | 0 | 0 | 1 | 0 | 1 | 1 | 1 |
| mirai/udp | 0 | 0.067 | 1 | 0 | 1 | 0.999 | 1 |
| mirai/udpplain | 0 | 0.6975 | 1 | 0 | 1 | 0.9995 | 1 |
