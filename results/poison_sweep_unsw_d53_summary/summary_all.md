# poison_sweep_unsw_d53 (all)

Window FNR on the final attack, by number of chaff days before it (d0 = no chaff):

| device | variant | rule | d0 | d1 | d3 | d4 | d7 | d8 | d12 | d14 | d15 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| samsung_camera | beh_s02_a30 | frozen | 0.683 | nan | nan | 0.7 | nan | 0.696 | 0.683 | nan | 0.683 |
| samsung_camera | beh_s02_a30 | full | 0.683 | nan | nan | 0.7 | nan | 0 | 0 | nan | 0 |
| samsung_camera | beh_s02_a30 | gated | 0.683 | nan | nan | 0.7 | nan | 0 | 0 | nan | 0 |
| samsung_camera | beh_s02_a30 | naive | 0.962 | nan | nan | 0.938 | nan | 0.888 | 0.792 | nan | 0.796 |
| samsung_camera | beh_s50_a05 | frozen | 0.683 | 0.7 | 0.683 | nan | 0.7 | nan | nan | 0.696 | nan |
| samsung_camera | beh_s50_a05 | full | 0.683 | 0.7 | 0.683 | nan | 0.7 | nan | nan | 0.288 | nan |
| samsung_camera | beh_s50_a05 | gated | 0.683 | 0.7 | 0.683 | nan | 0.7 | nan | nan | 0.288 | nan |
| samsung_camera | beh_s50_a05 | naive | 0.962 | 0.962 | 0.938 | nan | 0.912 | nan | nan | 1 | nan |
| samsung_camera | vol_s02_a30 | frozen | 0.683 | nan | nan | 0.7 | nan | 0.696 | 0.683 | nan | 0.683 |
| samsung_camera | vol_s02_a30 | full | 0.683 | nan | nan | 0.7 | nan | 0.692 | 0.683 | nan | 0.683 |
| samsung_camera | vol_s02_a30 | gated | 0.683 | nan | nan | 0.7 | nan | 0.696 | 0.683 | nan | 0.683 |
| samsung_camera | vol_s02_a30 | naive | 0.962 | nan | nan | 0.95 | nan | 0.917 | 0.9 | nan | 0.925 |
| samsung_camera | vol_s50_a05 | frozen | 0.683 | 0.7 | 0.683 | nan | 0.7 | nan | nan | 0.696 | nan |
| samsung_camera | vol_s50_a05 | full | 0.683 | 0.7 | 0.683 | nan | 0.7 | nan | nan | 0.288 | nan |
| samsung_camera | vol_s50_a05 | gated | 0.683 | 0.7 | 0.683 | nan | 0.7 | nan | nan | 0.288 | nan |
| samsung_camera | vol_s50_a05 | naive | 0.962 | 0.988 | 0.962 | nan | 0.954 | nan | nan | 0.95 | nan |
| tplink_plug | beh_s02_a30 | frozen | 0.7 | nan | nan | 0.7 | nan | 0.7 | 0.7 | nan | 0.7 |
| tplink_plug | beh_s02_a30 | full | 0.7 | nan | nan | 0 | nan | 0 | 0 | nan | 0 |
| tplink_plug | beh_s02_a30 | gated | 0.7 | nan | nan | 0 | nan | 0 | 0 | nan | 0 |
| tplink_plug | beh_s02_a30 | naive | 0.983 | nan | nan | 0.933 | nan | 0.908 | 0.875 | nan | 0.788 |
| tplink_plug | beh_s50_a05 | frozen | 0.7 | 0.7 | 0.7 | nan | 0.7 | nan | nan | 0.7 | nan |
| tplink_plug | beh_s50_a05 | full | 0.7 | 0.7 | 0.7 | nan | 0.7 | nan | nan | 0.7 | nan |
| tplink_plug | beh_s50_a05 | gated | 0.7 | 0.7 | 0.7 | nan | 0.7 | nan | nan | 0.7 | nan |
| tplink_plug | beh_s50_a05 | naive | 0.983 | 0.975 | 0.958 | nan | 0.929 | nan | nan | 0.996 | nan |
| tplink_plug | vol_s02_a30 | frozen | 0 | nan | nan | 0 | nan | 0 | 0 | nan | 0 |
| tplink_plug | vol_s02_a30 | full | 0 | nan | nan | 0 | nan | 0 | 0 | nan | 0 |
| tplink_plug | vol_s02_a30 | gated | 0 | nan | nan | 0 | nan | 0 | 0 | nan | 0 |
| tplink_plug | vol_s02_a30 | naive | 0.954 | nan | nan | 0.933 | nan | 0.65 | 0.671 | nan | 0.658 |
| tplink_plug | vol_s50_a05 | frozen | 0 | 0 | 0 | nan | 0 | nan | nan | 0 | nan |
| tplink_plug | vol_s50_a05 | full | 0 | 0 | 0 | nan | 0 | nan | nan | 0 | nan |
| tplink_plug | vol_s50_a05 | gated | 0 | 0 | 0 | nan | 0 | nan | nan | 0 | nan |
| tplink_plug | vol_s50_a05 | naive | 0.954 | 0.975 | 0.958 | nan | 0.771 | nan | nan | 0.671 | nan |

Window FNR reaching 50% (day = first sampled launch day; the crossing lies in (prev_day, day]):

| device | variant | rule | status | day | prev_day | chaff_packets | chaff_frac | fnr_at_0 |
|---|---|---|---|---|---|---|---|---|
| samsung_camera | beh_s02_a30 | frozen | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | beh_s02_a30 | full | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | beh_s02_a30 | gated | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | beh_s02_a30 | naive | baseline | nan | nan | nan | nan | 0.9625 |
| samsung_camera | beh_s50_a05 | frozen | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | beh_s50_a05 | full | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | beh_s50_a05 | gated | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | beh_s50_a05 | naive | baseline | nan | nan | nan | nan | 0.9625 |
| samsung_camera | vol_s02_a30 | frozen | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | vol_s02_a30 | full | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | vol_s02_a30 | gated | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | vol_s02_a30 | naive | baseline | nan | nan | nan | nan | 0.9625 |
| samsung_camera | vol_s50_a05 | frozen | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | vol_s50_a05 | full | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | vol_s50_a05 | gated | baseline | nan | nan | nan | nan | 0.6833 |
| samsung_camera | vol_s50_a05 | naive | baseline | nan | nan | nan | nan | 0.9625 |
| tplink_plug | beh_s02_a30 | frozen | baseline | nan | nan | nan | nan | 0.7 |
| tplink_plug | beh_s02_a30 | full | baseline | nan | nan | nan | nan | 0.7 |
| tplink_plug | beh_s02_a30 | gated | baseline | nan | nan | nan | nan | 0.7 |
| tplink_plug | beh_s02_a30 | naive | baseline | nan | nan | nan | nan | 0.9833 |
| tplink_plug | beh_s50_a05 | frozen | baseline | nan | nan | nan | nan | 0.7 |
| tplink_plug | beh_s50_a05 | full | baseline | nan | nan | nan | nan | 0.7 |
| tplink_plug | beh_s50_a05 | gated | baseline | nan | nan | nan | nan | 0.7 |
| tplink_plug | beh_s50_a05 | naive | baseline | nan | nan | nan | nan | 0.9833 |
| tplink_plug | vol_s02_a30 | frozen | not_reached | nan | nan | nan | nan | 0 |
| tplink_plug | vol_s02_a30 | full | not_reached | nan | nan | nan | nan | 0 |
| tplink_plug | vol_s02_a30 | gated | not_reached | nan | nan | nan | nan | 0 |
| tplink_plug | vol_s02_a30 | naive | baseline | nan | nan | nan | nan | 0.9542 |
| tplink_plug | vol_s50_a05 | frozen | not_reached | nan | nan | nan | nan | 0 |
| tplink_plug | vol_s50_a05 | full | not_reached | nan | nan | nan | nan | 0 |
| tplink_plug | vol_s50_a05 | gated | not_reached | nan | nan | nan | nan | 0 |
| tplink_plug | vol_s50_a05 | naive | baseline | nan | nan | nan | nan | 0.9542 |

All levels and the event-level FNR: `crossings_all.csv`; per-run values: `curves_all.csv`.
