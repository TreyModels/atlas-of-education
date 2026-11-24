# E1 — Grouping multiverse at R = 1200: full BH/BY verdicts, split-halves, localisation

**Status: COMPLETE.** 1,200 / 1,200 random draws + 1 real pass; total wall **5,426.8 s** on the 8-CPU cgroup
of `autodl3`; all 1,201 per-replicate checkpoints valid. Branch
`research/e1-multiverse-1200-2026-11-25`; record `research/records/2026-11-25-e1-multiverse/`.
Pre-registration was committed **before any multiverse run** (`f0459cb`); pilot/deviation note at `a32adcc`.
Estimator is unchanged from the committed run (`research/grouping-multiverse-400-2026-11-23` @ `1152cec`):
17 WDI variables, 136 unordered pairs × 2 specifications = 272 links, 50 real groupings in 8 families,
10-year change, own starting level, controls log GDP per head and urbanisation, country and decade fixed
effects, country-clustered SEs, with and without a country trend. CPU only; the GPU engine was not used.

## Headline answers

**(a) Does the BY-certified tier change with R? — Yes, but only for the heterogeneity family.** The
dependence-robust Benjamini–Yekutieli procedure certifies **zero links at R = 20, 74, 400 and 800 in all four
procedures**, and it still certifies **zero for the up, down and sign-flip families at R = 1200**. At
**R = 1200 the heterogeneity family certifies 32 links under BY** (first BY-certifying rank 29; 32 links at
the 1/1201 floor). So the methods paper's statement "BY certifies zero at 400 draws" is **R-dependent**: the
dependence-robust tier remains zero for upward/downward/sign-flipping links at 1,200 draws, but the
heterogeneity cluster crosses the BY step-up line at 1,200. This is arithmetic, not a new calibration: the
BY first-step threshold falls as R rises, and the floor cluster (32) is large enough at 1,200 to clear the
BY line at rank 29. Under the committed 136-parity convention the same pattern appears (BY het = 39 at
1,200; up/down/flip 0/0/0).

**CORRECTION (see `ERRATUM.md` §A):** the "up/down/flip 0/0/0" clause is wrong under the 136-parity convention —
`results/summary_by_R.json` `families.1200.*.certified_BY136` gives **up 25, down 15, sign-flip 0** (heterogeneity
39 is correct). Original text left visible.

**(b) How many "robust" links are group-concentrated? — 1 of 5.** The five robust-everywhere links are
`gdppc_log→urban`, `agri_va→gdppc_log`, `life_exp→fertility`, `u5mr→life_exp`, `u5mr→fertility` (recomputed at
R = 1200 with the unchanged rule). Leave-one-country-out pooled estimates with the unchanged estimator show
that only `gdppc_log→urban` is group-concentrated under the pre-registered rule (excluding its top five
countries — BWA, GNQ, OMN, LBY, LBR — changes |b| by more than 50%, although |t| stays above 1.96 at 2.47).
Of the **32 BY-certified heterogeneity links, 20 (63%) are group-concentrated** by the same rule.

## BH and BY counts by R (272-link family, conservative `(1+c)/(1+R)` p-values)

| R | family | floor | links at floor | BH cert | BY cert | first rank BH | first rank BY | BY cert (136 parity) |
|---|---|---|---|---|---|---|---|---|
| 20 | up | 0.04762 | 59 | 0 | 0 | — | — | 0 |
| 20 | down | 0.04762 | 51 | 0 | 0 | — | — | 0 |
| 20 | flip | 0.04762 | 38 | 0 | 0 | — | — | 0 |
| 20 | het | 0.04762 | 70 | 0 | 0 | — | — | 0 |
| 74 | up | 0.01333 | 41 | 0 | 0 | — | — | 0 |
| 74 | down | 0.01333 | 28 | 0 | 0 | — | — | 0 |
| 74 | flip | 0.01333 | 29 | 0 | 0 | — | — | 0 |
| 74 | het | 0.01333 | 52 | 0 | 0 | — | — | 0 |
| 400 | up | 0.00249 | 30 | **35** | 0 | 14 | — | 0 |
| 400 | down | 0.00249 | 19 | **19** | 0 | 14 | — | 0 |
| 400 | flip | 0.00249 | 15 | **15** | 0 | 14 | — | 0 |
| 400 | het | 0.00249 | 39 | **53** | 0 | 14 | — | 39 |
| 800 | up | 0.00125 | 19 | **41** | 0 | 7 | — | 19 |
| 800 | down | 0.00125 | 16 | **20** | 0 | 7 | — | 0 |
| 800 | flip | 0.00125 | 13 | **17** | 0 | 7 | — | 0 |
| 800 | het | 0.00125 | 34 | **53** | 0 | 7 | — | 41 |
| 1200 | up | 0.00083 | 17 | **41** | 0 | 5 | — | 25 |
| 1200 | down | 0.00083 | 15 | **23** | 0 | 5 | — | 15 |
| 1200 | flip | 0.00083 | 12 | **20** | 0 | 5 | — | 0 |
| 1200 | het | 0.00083 | 32 | **53** | **32** | 5 | **29** | 39 |

Sources: `results/summary_by_R.json` → `families.<R>.<proc>` (counts, floor, `first_rank_BH`,
`first_rank_BY`, parity fields); `results/table` rendering in `results/analysis1200.log`. The flip family is
"more sign-flipping than random" (the committed direction); the pre-registration's "<=" reading is reported
as a sensitivity and certifies 0 at every R (`sensitivity_flip_less_*` fields).

**What changes and what does not.** BH up grows 35 → 41, down 19 → 23, flip 15 → 20 from R = 400 to 1,200,
while the heterogeneity count is flat at 53. BY is zero at every R for up/down/flip; only heterogeneity
changes, at 1,200. This is the methods paper's strict-tier range updated with the new draw budget:
**BY 0/0/0/0 at R ≤ 800; BY 0/0/0/32 at R = 1200 (up/down/flip/het).**

## R = 400 reproduction of the committed headline

`results/repro400.json`: certified BH counts are **35 / 19 / 15 / 53** (up/down/flip/het), **identical to the
committed `headline.json`**; robust count **5 vs committed 5**; per-link real significance share
`share_TR` differs from the committed `edge_table400.csv` by **max 5.0e-7** (median 4.4e-8). The one declared
deviation is the panel vintage: the deterministic real pass reproduces the committed pooled t-statistics to
**max |Δt| = 3.97e-5**, median 7.5e-7 (`results/panelcheck.json`), because `final400.pkl` and the old
box/panel are lost and the new box's WDI panel is a later pull. This is a reproduction-with-vintage-difference,
not bit-identical; no adjustment was applied. Panel sha256 for the 17 variables + `meta.json`:
`results/panel_hashes.txt`.

## Determinism and integrity

- Replicate 7 recomputed from scratch in a fresh process is **bit-identical** in z, Qp and flip to its
  checkpoint (`z=True Qp=True flip=True`, wall 62.2 s) — the same check as the committed
  `determinism_check.py`.
- All 1,201 checkpoint files load with the expected shapes `(179,544)` / `(50,544)` / `(50,544)`;
  min/max size 526,732 / 545,392 bytes; total 0.63 GB. Per-file sha256: `results/reps_sha256.txt`.
- Runtime: 1,201 draws in 5,426.8 s = **4.52 s/draw effective** on 8 workers; per-draw worker wall mean
  37.8 s, median 36.4 s, max 136.2 s (the real pass), min 31.1 s (`results/progress.log`,
  `results/run_meta.txt`). The pilot's higher average (13.1 s/draw) was dominated by the real pass.
  **CORRECTION (see `ERRATUM.md` §B):** the minimum worker wall is **31.045 s** (`results/progress.log`, column 2;
  rounds/truncates to **31.0 s**), not 31.1 s. Original text left visible.
- No failed draws, no resume events, no discarded runs. `q2_audit.py` seen on the box belongs to a different
  record (`/root/work/repo/research/records/2026-11-25-q2-pathways`), was **not** touched or killed, and was
  no longer running at the final check.

## Split halves at R = 1200

Two disjoint halves, draws 1–600 and 601–1,200 (`results/split_halves.json`):

- Up-procedure empirical p rank correlation between halves: **0.9965**.
- BH-certified counts, half A / half B: up **34 / 38**, down **21 / 23**, flip **15 / 21**, het **53 / 51**.
- **BY certifies zero in both halves for every family** (with R = 600 the BY step-up rank is far above the
  floor cluster), so BY Jaccard is 0 by construction. The full-R BY heterogeneity certification at 1,200 is a
  property of the pooled 1,200-draw floor cluster, not of either half alone — reported as such rather than as
  an individual-link stability claim.
- Reading: **verdict counts are stable, individual-link certification is less stable** (flip half-counts
  15 vs 21 is the widest gap). The strict tier is a cluster-level statement, and the split shares support that
  reading.

## Group localisation (leave-one-country-out, unchanged estimator)

`results/group_localisation.json` / `.csv`. For each selected link, the pooled trend-specification estimate is
recomputed excluding one country at a time, then excluding the five countries with the largest |Δb| jointly.
A link is "group-concentrated" if the top-5 removal flips significance or changes |b| by more than 50%.

| robust link | b | t | top-5 countries | top-5 share of Σ|Δb| | t after top-5 removal | concentrated |
|---|---|---|---|---|---|---|
| gdppc_log → urban | 2.317 | 3.98 | BWA, GNQ, OMN, LBY, LBR | 0.22 | 2.47 | **yes** |
| agri_va → gdppc_log | −0.00412 | −2.63 | NER, GHA, RWA, BWA, GUY | 0.25 | −3.30 | no |
| life_exp → fertility | −0.0482 | −6.06 | RWA, CAF, DZA, CHN, SOM | 0.29 | −8.69 | no |
| u5mr → life_exp | −0.0266 | −3.04 | KHM, OMN, ZMB, RWA, BWA | 0.30 | −4.46 | no |
| u5mr → fertility | 0.00611 | 5.39 | KHM, CAF, SOM, DZA, RWA | 0.34 | 7.26 | no |

**1 of 5 robust links is group-concentrated; 20 of the 32 BY-certified heterogeneity links are
group-concentrated** (`n_robust_group_concentrated` / `n_by_group_concentrated` in the JSON summary).

## Commands, seeds and environment

```bash
# box autodl3; /root/work/e1; CPU-only, 8-core cgroup, 60 GB
export GM_R=20  GM_NPROC=8 GM_OUT=/root/work/e1/out
/root/miniconda3/bin/python scripts/panelcheck.py            # panel hashes + real-pass reproduction
/root/miniconda3/bin/python scripts/run_e1.py               # pilot R=20 (resumable)
export GM_R=1200
nohup /root/miniconda3/bin/python scripts/run_e1.py > logs/run1200.log 2>&1 &
/root/miniconda3/bin/python scripts/analyse_e1.py           # BH/BY ladder, split halves, repro400
/root/miniconda3/bin/python scripts/group_localisation.py
/root/miniconda3/bin/python scripts/make_report_tables.py
```

Seeds: replicate r uses `numpy.random.default_rng(1000 + r)`, r = 1..1200, exactly as the committed run
(so r = 1..400 are the committed draws). Code: unchanged `gm_core.py` from `1152cec`; our runner
`scripts/run_e1.py`, analysis `scripts/analyse_e1.py`, localisation `scripts/group_localisation.py`.
Checkpoints (0.63 GB) are **not** committed; they remain at `/root/work/e1/out/reps/` until the box is
shut down, with sha256 manifest `results/reps_sha256.txt`; they are regenerated by the `run_e1.py` command
above (resumable, same seeds, ~90 min on 8 cores).

## Deviations, failures, uncertainty

1. **Panel vintage (declared before scaling):** new-box WDI panel reproduces committed pooled t-stats to
   3.97e-5; R=400 BH counts nevertheless match exactly and share_TR differs by ≤5e-7.
2. **Flip-family direction (declared):** the pre-registration wrote the sign-flip family as "real flip rate
   ≤ null"; the committed analysis and the substantive object are "real flip rate ≥ null" (flips *more* than
   random). Primary results use ≥ (matching `analyse400.py`); the ≤ direction is retained as a sensitivity
   and certifies 0 at every R (`sensitivity_flip_less_*`). This was corrected before the final report and
   is the only analysis-direction change.
3. **Uncertainty:** the empirical p floor is 1/(R+1); BH/BY arithmetic is conditional on the dependence
   assumption (the 272 tests share draws); the conservative `(1+c)/(1+R)` convention is primary, with the
   liberal `c/R` counts reported in `summary_by_R.json` (e.g. at 1,200: BH up 41 conservative vs 41 liberal;
   BY het 32 conservative vs 37 liberal). Split-half and localisation results are descriptive.
4. **Data tier:** observed World Bank WDI series only; no imputation, reconstruction or synthetic data in
   this analysis. GPU engine not used (CPU-only), so no batch layout applies.

## Traceability (number → committed file → field)

| number | file | field |
|---|---|---|
| draws completed / wall time | `results/run_meta.txt` | `total_wall`, `R`; `results/progress.log` last line |
| BH/BY counts and ranks by R | `results/summary_by_R.json` | `families.<R>.<proc>.certified_BH`, `.certified_BY`, `.first_rank_BH`, `.first_rank_BY`, `.n_floor`, `.certified_BY136` |
| per-link p/BH q/BY q at each R | `results/verdict_by_R.csv` | `p_<proc>_R<R>`, `qBH_...`, `qBY_...`, `certBY_...` |
| R=400 reproduction | `results/repro400.json` | `certified_BH_ours`, `certified_BH_committed`, `max_abs_share_TR_diff`, `robust_*` |
| split halves | `results/split_halves.json` | `up_p_rank_correlation`, `family_agreement.*` |
| group localisation | `results/group_localisation.json` / `.csv` | `summary.*`, `robust[]`, `by[]` |
| panel provenance | `results/panel_hashes.txt`, `results/panelcheck.json` | hashes; `max_abs_diff` |
| checkpoint integrity | `results/reps_sha256.txt` | one sha256 per replicate file |

## Box shutdown

E1 compute and analysis are finished; no `run_e1.py` process is alive. The only other job seen earlier,
`q2_audit.py`, belongs to another record and was not touched; it was absent at the final check. **The box is
ready to be shut down once Trey confirms no other task needs it** (I did not kill another task's process or
power off the instance unilaterally).
