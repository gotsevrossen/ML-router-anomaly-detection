# kitsune_suite

## Attacks caught at the validation threshold

| capture | autoencoder_slog | hst | kitnet_windows | mad_tail_slog | robust_z_router |
|---|---|---|---|---|---|
| os_scan | 1 | 1 | 1 | 1 | 1 |
| ssdp_flood | 1 | 1 | 1 | 1 | 1 |
| ssl_renegotiation | 0.9474 | 0.9211 | 1 | 0.8158 | 0.9211 |
| syn_dos | 0.8 | 1 | 1 | 1 | 1 |
| video_injection | 0.6364 | 0.4545 | 0.8182 | 0.8182 | 0.6364 |

## False alarms per day

| capture | autoencoder_slog | hst | kitnet_windows | mad_tail_slog | robust_z_router |
|---|---|---|---|---|---|
| os_scan | 270 | 270 | 360 | 90 | 270 |
| ssdp_flood | 2711 | 1864 | 2711 | 2033 | 2711 |
| ssl_renegotiation | 1080 | 360 | 1800 | 1440 | 1080 |
| syn_dos | 137.1 | 960 | 685.7 | 411.4 | 411.4 |
| video_injection | 0 | 0 | 0 | 0 | 0 |

## Captures

| capture | skipped | device | pre_attack_windows | windows | bootstrap | validation | test_benign | test_attack |
|---|---|---|---|---|---|---|---|---|
| active_wiretap | 22 pre-attack windows | nan | nan | nan | nan | nan | nan | nan |
| arp_mitm | 21 pre-attack windows | nan | nan | nan | nan | nan | nan | nan |
| fuzzing | 34 pre-attack windows | nan | nan | nan | nan | nan | nan | nan |
| os_scan | nan | 00:a0:de:f1:88:6e | 88 | 105 | 44 | 26 | 32 | 3 |
| ssdp_flood | nan | c8:00:84:2a:39:51 | 79 | 82 | 39 | 23 | 17 | 3 |
| ssl_renegotiation | nan | ac:9b:0a:fc:2d:8e | 40 | 78 | 20 | 12 | 8 | 38 |
| syn_dos | nan | c8:00:84:2a:39:51 | 101 | 106 | 50 | 30 | 21 | 5 |
| video_injection | nan | 00:a0:de:f1:88:6e | 61 | 72 | 30 | 18 | 13 | 11 |
