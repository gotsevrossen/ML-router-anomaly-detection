# Vendored: Kitsune-py

- Source: https://github.com/ymirsky/Kitsune-py
- Commit: `7c8ea51e89268d9a20399dca4bf32d663e638eb4` (2026-03-24, "Merge pull request #36")
- License: MIT (see `LICENSE` here and `KitNET/LICENSE.txt`). Copyright (c) 2018 Yisroel Mirsky.
- Copied unmodified (CLAUDE.md §4: "vendor; do not rewrite it").

Copied: `KitNET/`, `AfterImage.py`, `netStat.py`, `FeatureExtractor.py`, `Kitsune.py`, `LICENSE`, `README.md`.
Left out: `example.py`, `setup.py`, `AfterImage_extrapolate.pyx` (experimental, disabled upstream), the paper PDF, the figure and the `mirai.zip` sample capture. The full clone is kept outside the repo in the `AI reserch data` folder.

Notes for the wrapper (`src/rad/models/kitsune_wrapper.py`, Phase 1c):
- `netStat.py` calls `pyximport.install()` at import time, so `cython` must be installed.
- `AfterImage.py` uses `np.Inf`, removed in NumPy 2.0. Set `np.Inf = np.inf` before importing (verified 2026-10-10: netStat yields 100 features per packet and KitNET trains and scores).
- `FeatureExtractor.py` / `Kitsune.py` read pcaps through tshark or scapy. We do not use them; the wrapper feeds our already-parsed packets to `netStat` (AfterImage features) and `KitNET` directly.
