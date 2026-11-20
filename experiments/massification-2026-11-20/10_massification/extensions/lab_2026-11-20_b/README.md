# Lab battery 2026-11-20_b — 15 predeclared experiments (5 clusters × 3)

**Status: ILLUSTRATIVE/DESCRIPTIVE — no causal or direction claims; not evidence of policy effects.**
Extension of `lab_2026-11-20/` (E1–E10) into five post-secondary questions. The massification phase remains
**CLOSED** at PARTIAL/DESCRIPTIVE/EQUIVALENT (`06_report/MASSIFICATION_CLOSEOUT.md`, D76); this battery extends the
descriptive evidence base and does **not** reopen C1–C4.

- **`PRE_DECLARATIONS.md`** — 15 experiments (X1–X15), declared proxies, estimators, thresholds, falsifiers and
  verdict vocabulary, **frozen before any run**; sha256 recorded in `RUN_MANIFEST.json`.
- **`RESULTS.csv`** — one row per experiment with the predeclared verdict (all 15, including nulls and failures)
  **plus three `run_tag=amendment_B1` rows** for the disclosed post-hoc cluster-5 amendment (18 rows total; the
  predeclared rows stand as the formal result).
- **`FINDINGS.md`** — consolidated findings with per-cluster detail, Lead adjudications/disclosures and limits.
- **`RUN_MANIFEST.json`** — predeclaration + data + code + results hashes, seeds, environment, per-cluster
  determinism re-run results.
- **`SHA256SUMS.txt`** — every artefact in this folder.
- **`cluster_1_absorption/` … `cluster_5_fragmentation_sim/`** — per-cluster predeclared work: `code/run.py`,
  `results/*.csv`, `CLUSTER_RESULTS.csv`, `FINDINGS.md`, `RUN_MANIFEST.json`; cluster 5 additionally carries
  `code/amendment_b1.py`, `results/AMENDMENT_B1/` and `CLUSTER_RESULTS_AMENDMENT_B1.csv`.

## The five clusters

| cluster | experiments | question | labels |
|---|---|---|---|
| 1 post-secondary absorption | X1–X3 | does tertiary expansion co-move with formal/graduate absorption (declared proxies), 6 systems and 30 countries | observed/derived |
| 2 tertiary crossing structure | X4–X6 | are tertiary milestones (≥15%, ≥50% GER) the same economic-structure package as secondary crossings, or a different one | observed/derived |
| 3 geo-size scaling | X7–X9 | population/urban size and the predeclared number-of-markets proxy vs tertiary/secondary GER; HKG vs CHN/PHL/KHM (small-n caveats) | observed/derived |
| 4 regional post-secondary proxy | X10–X12 | PHL 17 regions × cohorts vs national tertiary expansion — **regional tertiary enrolment is unobserved; attainment proxies only** | observed/derived |
| 5 geo-fragmentation simulation | X13–X15 | does splitting a system into more regions/markets delay or smooth the ceiling crossing — **SIMULATED toy** | simulated |

## Run

```
PY="/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python"
cd 10_massification/extensions/lab_2026-11-20_b
for d in cluster_*; do "$PY" "$d/code/run.py"; done
```

Each cluster script is deterministic (fixed seeds) and reads only data already on disk under
`10_massification/data/` and `09_relations/data/`. Cluster 5 reads no data and is a **stipulated toy simulation**
(not calibrated, not evidence, no historical test).

## Declared proxies (predeclared, `derived`)

`ABSORB_F` = wage-and-salaried employment share; `ABSORB_S` = services employment share; `QUEUE` = BA+ attainment
share ÷ wage-share × 100 (degree-holders per 100 formal jobs); `MARKETS` = urban population in millions (one
"market" per 1M urban residents). None of these is a measured absorption rate or an actual count of markets.
