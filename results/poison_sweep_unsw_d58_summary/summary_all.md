# poison_sweep_unsw_d58 (all)

Window FNR on the final attack, by number of chaff days before it (d0 = no chaff):

| device | variant | rule | d0 | d1 | d3 | d4 | d7 | d8 | d12 | d14 | d15 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| samsung_camera | beh_s02_a30 | full | 0.683 | nan | nan | 0.7 | nan | 0.692 | 0.683 | nan | 0.683 |
| samsung_camera | beh_s02_a30 | gated | 0.683 | nan | nan | 0.7 | nan | 0.692 | 0.683 | nan | 0.683 |
| samsung_camera | beh_s50_a05 | full | 0.683 | 0.7 | 0.683 | nan | 0.7 | nan | nan | 0.288 | nan |
| samsung_camera | beh_s50_a05 | gated | 0.683 | 0.7 | 0.683 | nan | 0.7 | nan | nan | 0.288 | nan |
| samsung_camera | vol_s02_a30 | full | 0.683 | nan | nan | 0.7 | nan | 0.692 | 0.683 | nan | 0.683 |
| samsung_camera | vol_s02_a30 | gated | 0.683 | nan | nan | 0.7 | nan | 0.696 | 0.683 | nan | 0.683 |
| samsung_camera | vol_s50_a05 | full | 0.683 | 0.7 | 0.683 | nan | 0.7 | nan | nan | 0.288 | nan |
| samsung_camera | vol_s50_a05 | gated | 0.683 | 0.7 | 0.683 | nan | 0.7 | nan | nan | 0.288 | nan |

Window FNR reaching 50% (day = first sampled launch day; the crossing lies in (prev_day, day]):

| device | variant | rule | status | day | prev_day | chaff_packets | chaff_frac | fnr_at_0 |
|---|---|---|---|---|---|---|---|---|
| samsung_camera | beh_s02_a30 | full | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | beh_s02_a30 | gated | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | beh_s50_a05 | full | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | beh_s50_a05 | gated | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | vol_s02_a30 | full | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | vol_s02_a30 | gated | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | vol_s50_a05 | full | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | vol_s50_a05 | gated | baseline | nan | nan | nan | nan | 0.6833 |

All levels and the event-level FNR: `crossings_all.csv`; per-run values: `curves_all.csv`.
