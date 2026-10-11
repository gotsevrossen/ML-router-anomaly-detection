# nbaiot_fixes_Provision_PT_737E_Security_Camera

Rows: {'benign': 62154, 'bootstrap': 31077, 'validation': 12430, 'test_benign': 18647, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window |
|---|---|---|---|---|---|---|---|---|---|
| iforest | 0.00125 | 0 | 0.5298 | 0.6964 | 0.7285 | 0.0009653 | 0.00035 | 0.8101 | 0.01949 |
| iforest_headroom | 0.1433 | 0.00455 | 0.5729 | 0.7837 | 0.6484 | 0.001019 | 0.1433 | 0.5603 | 0.04727 |
| iforest_extended | 0.8002 | 0.7973 | 0.8988 | 0.9701 | 0.6317 | 0.0008044 | 0.8002 | 0.8044 | 0.8545 |
| mad | 0 | 0 | 0.4975 | 0.4737 | 0.9984 | 0.000858 | 0 | 0.405 | 0.009696 |
| mad_tail | 0.7998 | 0.7973 | 0.8995 | 0.9735 | 0.6961 | 0.0008044 | 0.7995 | 0.4757 | 0.01019 |
| hst | 0.04085 | 0.04085 | 0.5308 | 0.8053 | 0.9309 | 0.002145 | 0.04085 | 3.368 | 0.1144 |
| autoencoder | 0.8002 | 0.698 | 0.9504 | 0.9948 | 0.01457 | 0.0009117 | 0.8002 | 10.4 | 0.02396 |

## Detection rate at tau, per attack

| attack | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| gafgyt/junk | 0 | 0.001 | 1 | 0 | 0.9935 | 0 | 1 |
| gafgyt/scan | 0.0005 | 0.0015 | 1 | 0 | 1 | 0.0005 | 1 |
| gafgyt/tcp | 0 | 0.001 | 0.0015 | 0 | 0.0015 | 0 | 0.0015 |
| gafgyt/udp | 0 | 0 | 0.0005 | 0 | 0 | 0 | 0.0005 |
| mirai/ack | 0 | 0.497 | 1 | 0 | 1 | 0 | 1 |
| mirai/scan | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| mirai/syn | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| mirai/udp | 0 | 0.457 | 1 | 0 | 1 | 0 | 1 |
| mirai/udpplain | 0.003 | 0.4755 | 1 | 0 | 1 | 0.408 | 1 |
