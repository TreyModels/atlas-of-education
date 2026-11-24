# REPORT — equifinality & phase sweep: 20×20 X/Y grid × {bar, quota} gates × 20 seeds

**SIMULATION ONLY — `eduengine` toy worlds; illustrative parameters; no country calibration, no empirical
validation, no causal claims.** Every number below is a property of the model output surface, not of any real
education system.

Workstream: `research/equifinality-phase-2026-11-25` (worktree `wt3/phase`).
Pre-registration: `research/records/2026-11-25-equifinality-phase/PRE_REGISTRATION.md`, commit **`078cc13`**,
committed alone **before any run** (this is the SHA to cite for everything below).
Base: `origin/research/phase-transition-2026-11-25` @ `2e58d64`. Date 2026-11-25.

---

## 1. What was requested vs what was run — and the contest-gate gap

| | requested by the brief | actually run |
|---|---|---|
| X levels | 20 | **20** |
| Y levels | 20 | **20** |
| seeds | 20 (0..19) | **20 (0..19)** |
| gate regimes | `{bar, quota, contest}` = 3 | **`{bar, quota}` = 2** |
| cells | 1,200 | **800** |
| runs | 24,000 | **16,000** |

**The missing arm is the `contest` gate: `CONTEST GATE = NOT-IMPLEMENTED`, and it was not proxied or
relabelled.** The gap is exactly one gate arm (20 × 20 × 20 = 8,000 runs). Evidence, recorded in the
pre-registration (commit `078cc13`, §3, *before* the run):

1. **No gate hook exists to subclass.** `engine/eduengine/core.py` L60–69 (`Module` base) exposes only
   `setup, supply, sector, extras, labour, after, measure, summary`. The gate decision is inlined in
   `Engine.step`; there is no gate class anywhere in the engine tree.
2. **Only two gate kinds are implemented, and a third is silently swallowed.** `core.py` gate dispatch:
   `if gate['kind'] == 'bar': ok = score >= gate['bar']` **`else:`** `# quota: seats = share x cohort size`
   (`seats = int(round(gate['share'] * p['N']))`). A `kind='contest'` dict would fall into the quota branch
   and be silently treated as quota — a silent proxy, which the brief forbids. `core.py:164` does the same
   two-way dispatch for the household's *believed* cutoff (`gate['bar'] if kind=='bar' else self.cut[m]`).
3. **`grep -rn contest` over the engine tree returns exactly one hit and it is a comment:**
   `eduengine/modules/labour.py:39: # which tiers are ranked contests (the positional race). ...`
   `worlds.py` L23–24 define `kind='bar'` and `kind='quota'` only.
4. **A third kind would also be arithmetically indistinguishable from `quota` at this design.** The engine's
   quota rule is already a fixed-seat rank tournament whose seat count is `round(share × N)`; with `N = 400`
   fixed in every cell, an absolute-seat "contest" is identical to quota unless the seat count is decoupled
   from cohort size inside `core.step` — i.e. unless an engine file is edited, which the brief and the base
   pre-registration both prohibit.

The 4 gate levels used in each regime are exactly the base pre-registration's, unchanged: `bar` =
`[bar 3.0, bar 5.5, bar 8.0, bar 11.5]`; `quota` = `[bar 3.0, quota(share 0.55, cut0 7.0),
quota(share 0.45, cut0 10.0), bar 11.5]`. The task's own contingency ("otherwise report NOT-IMPLEMENTED with
exact evidence and run only bar and quota") is the path taken.

---

## 2. Design as run (pre-registered, unchanged)

* **X = formal vacancies per cohort entrant (`vac0`)** — 20 exact geometric levels (4 s.f.):
  `0.0100, 0.01259, 0.01586, 0.01998, 0.02516, 0.03168, 0.03990, 0.05025, 0.06329, 0.07970, 0.1004, 0.1264,
  0.1592, 0.2005, 0.2525, 0.3180, 0.4005, 0.5044, 0.6352, 0.8000`.
* **Y = liquidity slack = primary fee share of median income (`fee_primary`, grades 1–6 only)** — 20 exact
  levels `0.00, 0.01, …, 0.19`; `0.00` is the fee-abolition slice.
* **Fixed everywhere:** `formal_loop` world, `N = 400`, `T = 70`, `measure_from = 35`, `queue_on = True`,
  `vac_growth = 0.0`, driver-side `PrimaryFeeSchools` subclass (primary grade fee only), modules
  `[PrimaryFeeSchools, PrivateSchools, TutoringMarket, FiscalState, QueueLabour, SDG4]`.
* **Seeds** `0..19`, identical in every cell. Seeds are the only stochastic input.
* **Cells/runs:** 20 × 20 × 2 = 800 cells; **16,000 runs; 16,000 ok / 0 failed** — failures were preserved by
  construction (`ok`/`error` columns), there were none.
* Exit partition read only from `e.exits` via `aggregate_exits()` (`e.kids['reason']` is never read — it is
  all −1 by design); survivors at the horizon are the `censored` category.

---

## 3. Run metadata

| | |
|---|---|
| host | `autodl-container-a8f742b5ee-292349c5` (warm AutoDL box), `--workers 12` of a 15-CPU quota |
| python / numpy | 3.10.8 / 1.24.1 |
| started (UTC) | **2026-11-24T17:11:16Z** |
| finished (UTC) | **2026-11-24T17:29:41Z** |
| elapsed | **1,100.4 s (18.34 min)** for 16,000 runs (0.069 s/run wall) |
| output dir on box | `/root/work/equifinality_phase/` (nothing written outside it) |
| runner | `phase_sweep_full.py` sha256 `e6fe8aa8a347ae52e1b4c96ed6b906d99aaec215ccdbba054dc7e6dc17f12a05` (host == box) |
| engine (pinned by hash in the run JSON) | `worlds.py` `2e9ec71a882755d9402b9bbcf802ce4a3aeb1f32ef4ac06ef48b97fc7340e0da`; `eduengine/core.py` `2b7484a97d64bf5f498c95003dd249241373cdc25da4c4d02d59d256df59c064`; worlds.py + 14 files under `eduengine/` (15 engine hashes) + the runner, 16 code hashes in total |
| raw output | `data/phase_sweep_full_runs.csv` (6.4 MB, 16,000 rows) sha256 `3a6ef24cbee13b840be09043cc2c9fa7fb19d8fa4d6ded79ece4ac4c0449efb5` |
| per-cell summary | `data/phase_sweep_full_summary.csv` + `.json` (json sha256 `285fa796c5d7713c711655805a75a08459d7b6f812e106267cbe7b1f12ea794c`) |

**Box lease (cross-window protocol).** I read `BOX_LEASE.md` first, appended
`{"ts":"2026-11-24T17:10:59Z","window":"lead-nb/phase-sweep","action":"claim",…}` immediately before launch;
a second window claimed at `17:13:42Z` after mine, so a lease conflict existed during the run (`17:13:48Z`–~`17:20Z`,
a brief bar-arm job). Resolution: `lead-main` note `17:15:03Z` + `lead-nb` accept note `17:16:10Z`; the earlier
claim kept its job alive, nothing was killed, no second grid launched, no power/watcher action by this window.
I appended my `release` at **`2026-11-24T17:33:16Z`** with the runs/elapsed/status. The contention lengthened
wall time; it cannot change results (deterministic seeds, separate output dirs). Full entries are in
`~/neon-boot/box_lease.jsonl`.

---

## 4. Validity checks (all passed; `data/validity_checks.json`)

| check | result |
|---|---|
| Exit partition sums to 1.0, **every one of the 16,000 raw rows** (8 categories incl. `censored`) | max abs deviation **2.0e-9** (tol 1e-6) — PASS |
| Per-cell seed means recomputed from the raw runs CSV vs committed summary (2,400 values) | max abs diff **0.0** — PASS |
| `ger_sim == 1 − never_share` in every row | max abs diff **1.1e-16** — PASS |
| **Reproducibility re-run** (18 cells × 2 gates × 20 seeds = **360 runs**, 2.25% of the sweep, fresh box invocation) vs the corresponding rows of the full sweep | **360/360 rows matched, 18,360 field comparisons, 0 mismatches, max abs diff 0.0** — PASS (bit-for-bit) |

Pre-registered tolerance context: the median seed-level SD of `ger_sim` is **0.236 pp**, so the 0.5 pp
near-equality tolerance is ≈ 2.1× the median seed noise — near-equality is a real constraint, not noise.

---

## 5. EQUIFINALITY RESULTS (primary deliverable)

### 5.1 Definition (exactly as pre-registered, commit `078cc13`)

A pair of distinct cells `(a,b)` is **equifinal** iff, on **seed-mean** cell values (20 seeds),
all in **percentage points** (100 × share), `Δ` absolute and direction-agnostic:

```
|ΔGER_sim| < 0.5 pp   AND   ( |Δliq_share| > 25 pp   OR   |Δtut_rate| > 20 pp )
GER_sim = 1 − never_enrolled_share   (DECLARED simulated participation, NOT an empirical GER)
```

Families: **within-gate (primary)** = bar–bar + quota–quota pairs = 79,800 + 79,800 = **159,600**;
**cross-gate (secondary)** = bar × quota = **160,000**. Together every unordered pair of distinct cells =
C(800,2) = **319,600** — the scan is exhaustive and was cross-checked against an explicit double loop over
all 319,600 pairs (counts identical; assertion in `analyze_equifinality.py`).

### 5.2 Headline result

> **Verdict (pre-registered reading rule): NO EVIDENCE OF EQUIFINALITY BEYOND CHANCE.**
> Observed within-gate qualifying pairs **176** ≤ permutation-null 97.5th percentile **221.0**
> (null mean **190.52**, SD 15.73, max 247, one-sided **p = 0.838**, observed/null-mean ratio **0.92**).

In words: near-identical simulated participation with a very different exclusion composition or
shadow-education uptake **does occur in the toy world (176 within-gate pairs are catalogue-able)**, but it
occurs **less often than if the three outcomes were unrelated to each other and to position** — the surface is
*positively coupled*: where participation is near-equal, the composition of who is excluded tends also to be
near-equal. This is the "smooth coupled surface" outcome, not an equifinality landscape.

| family | observed | null mean | null SD | null 97.5th pct | ratio | one-sided p |
|---|---|---|---|---|---|---|
| **within-gate (primary)** | **176** | 190.52 | 15.73 | 221.0 | 0.92 | **0.838** |
| — bar (primary) | 161 | 170.22 | 14.87 | 199.0 | 0.95 | 0.738 |
| — quota (primary) | 15 | 20.30 | 4.46 | 29.0 | 0.74 | 0.900 |
| cross-gate (secondary) | 4,132 | 3,908.13 | 60.94 | 4,030.0 | **1.057** | **0.001** |
| all pairs (total) | 4,308 | 4,098.66 | 63.58 | 4,229.0 | 1.051 | 0.001 |

*The null* is the pre-registered one: for each of **1,000 permutations** (rng `default_rng(20261125+k)`),
within each gate regime the 400 cell labels of each of the three outcome vectors were **independently
permuted**, and the identical pair predicate/thresholds were recomputed. It preserves each metric's marginal
distribution and each cell's coordinates while destroying the joint structure the conjunction exploits.
Full distribution in `data/equifinality_null.json`.

**Cross-gate pairs are a different phenomenon, reported separately and not pooled into the verdict.** The
4,132 cross-gate pairs are 97.2% driven by `|Δtut_rate| > 20 pp` alone, and the reason is visible in the
marginals: tutoring is **22.0–30.5 pp under `bar`** but **34.6–57.3 pp under `quota`** — a discrete gate-regime
effect on shadow education. So a bar cell and a quota cell with near-identical participation can trivially have
≥20 pp tutoring gaps. The small excess over the null (ratio 1.06) is consistent with that regime contrast; it
is **not** evidence of a smooth equifinality landscape, and the pre-registered primary family deliberately
excludes it for exactly this reason.

### 5.3 Where the qualifying pairs are

* Distinct cells involved (primary): **89 of 800**. Max partner count of a single cell: **15**, at
  `bar / x = 0.5044 / y = 0.01` and `bar / x = 0.5044 / y = 0.02`.
* Composition of the 176 primary pairs: `x` differs only **35**, `y` differs only **0**, both differ **141**;
  qualified via liquidity alone **161 (91.5%)**, via tutoring alone **15 (8.5%)**, via both **0**.
  Mean `|ΔGER|` 0.278 pp; mean `|Δliq|` 24.92 pp; mean `|Δtut|` 6.10 pp.
* The largest within-gate composition gaps at near-identical participation are **|Δliq| = 28.09 pp** and
  **|Δtut| = 20.36 pp** — i.e. the qualifying set is *thin*: it just clears the ≥25 pp / ≥20 pp bars. Compare
  the cross-gate tutoring contrast, which reaches 33 pp.

**Top 10 primary (within-gate) pairs**, ranked by `|Δliq| + |Δtut|` (full 176 in
`data/equifinality_pairs.csv`, top 50 in `data/equifinality_top50.csv`; all values pp):

| # | gate | cell A (x, y) | GER_A | liq_A | tut_A | cell B (x, y) | GER_B | liq_B | tut_B | ΔGER | Δliq | Δtut |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | bar | 0.0100, 0.00 | 99.11 | 4.53 | 27.84 | 0.5044, 0.00 | 99.54 | 32.62 | 22.16 | +0.43 | **+28.1** | −5.7 |
| 2 | bar | 0.0100, 0.00 | 99.11 | 4.53 | 27.84 | 0.5044, 0.01 | 99.18 | 32.62 | 22.25 | +0.07 | **+28.1** | −5.6 |
| 3 | bar | 0.0100, 0.01 | 98.54 | 4.65 | 27.99 | 0.5044, 0.02 | 98.69 | 32.47 | 22.35 | +0.15 | **+27.8** | −5.6 |
| 4 | bar | 0.0100, 0.00 | 99.11 | 4.53 | 27.84 | 0.5044, 0.02 | 98.69 | 32.47 | 22.35 | −0.42 | **+27.9** | −5.5 |
| 5 | bar | 0.01259, 0.00 | 99.14 | 4.66 | 27.51 | 0.5044, 0.00 | 99.54 | 32.62 | 22.16 | +0.40 | **+28.0** | −5.3 |
| 6 | bar | 0.01586, 0.00 | 99.14 | 4.66 | 27.51 | 0.5044, 0.00 | 99.54 | 32.62 | 22.16 | +0.40 | **+28.0** | −5.3 |
| 7 | bar | 0.0100, 0.01 | 98.54 | 4.65 | 27.99 | 0.5044, 0.03 | 98.15 | 32.31 | 22.38 | −0.39 | **+27.7** | −5.6 |
| 8 | bar | 0.0100, 0.02 | 97.84 | 4.79 | 28.11 | 0.5044, 0.03 | 98.15 | 32.31 | 22.38 | +0.31 | **+27.5** | −5.7 |
| 9 | bar | 0.01259, 0.00 | 99.14 | 4.66 | 27.51 | 0.5044, 0.01 | 99.18 | 32.62 | 22.25 | +0.05 | **+28.0** | −5.3 |
| 10 | bar | 0.01586, 0.00 | 99.14 | 4.66 | 27.51 | 0.5044, 0.01 | 99.18 | 32.62 | 22.25 | +0.05 | **+28.0** | −5.3 |

The structure of the qualifying set is clear and worth recording: it is the **X-extreme contrast at the
abolition/low-fee end of Y** — tight formal-job bottleneck (`vac0 ≈ 0.01`, liquidity exits ≈ 4.5%) vs slack
(`vac0 ≈ 0.50`, liquidity exits ≈ 32.6%) — at nearly identical simulated participation (≈99%). Direction is
reported as observed (high-vacancy cells have *higher* liquidity-exit shares at near-equal participation); this
is a descriptive property of the toy world, **not** a causal claim and **not** an empirical regularity.
`y`-only differences never qualify: fee changes participation monotonically, so near-equal participation
cannot come from a fee change alone in this grid.

### 5.4 Cell-level context (seed means, 800 cells, pp)

| gate | GER_sim | liquidity exits | tutoring | completion_lower | never-enrolled | censored at horizon |
|---|---|---|---|---|---|---|
| bar | 80.08 – 99.97 (med 91.21) | 2.55 – 32.62 | 22.03 – 30.52 | 57.75 – 77.27 | 0.03 – 19.92 | 25.95 – 34.08 |
| quota | 80.54 – 100.00 (med 91.87) | 2.87 – 22.48 | 34.57 – 57.26 | 54.54 – 55.01 | 0.001 – 19.46 | 25.49 – 29.16 |

The `quota` gate binds as designed (mean realised pass rate 0.917 at the lower-secondary gate, index 1, and 0.963 at the upper-secondary
gate, index 2; endogenous cutoffs settle at ≈10.15 and ≈13.49), whereas the four `bar` thresholds are near-non-binding in practice (mean
pass rates 0.995–0.999). This is reported as a **property of the design**, not repaired post hoc: the bar arm is
therefore closer to an open-access arm than a tournament arm in these cells, and the quota arm carries the
selection. `censored` is 25–34% of the measured population in every cell (children still in the state at
`T = 70`), which is why `GER_sim = 1 − never_enrolled` is the declared participation measure.

---

## 6. Secondary outcome — `completion_lower`

Pre-registered descriptive pairing (`|ΔGER_sim| < 0.5 pp` **and** `|Δcompletion_lower| > 20 pp`, within gate):
**0 qualifying pairs in both gates** (`data/equifinality_completion_lower_pairs.csv` is header-only). Within a
gate regime, lower-secondary completion does not separate at fixed participation: it co-moves tightly with
participation (bar: 57.75–77.27 pp; quota: 54.54–55.01 pp — the quota admission rule pins completion almost
exactly across the whole X×Y plane). No verdict is attached; this is a descriptive secondary outcome.

---

## 7. Descriptive phase-boundary diagnostics (NO verdict — that belongs to the sibling phase-transition lane)

Cheap grid edge statistics, `J_edge = |ΔM| / σ_med` over the 760 axis-adjacent cell pairs per gate,
`sharpness = J_max / median(J_edge)`, gate contrast `C = mean J_edge(bar) / mean J_edge(quota)`:

| metric | gate | mean J_edge | J_max | sharpness | C |
|---|---|---|---|---|---|
| GER_sim | bar | 2.53 | 18.10 | 8.15 | 0.95 |
| GER_sim | quota | 2.66 | 19.18 | 8.80 | |
| liquidity | bar | 3.31 | 28.14 | 29.50 | 1.42 |
| liquidity | quota | 2.33 | 14.99 | 13.72 | |
| tutoring | bar | 1.26 | 3.64 | 4.07 | 0.61 |
| tutoring | quota | 2.06 | 18.05 | 28.34 | |

Read descriptively only: the sharpest grid edge in this design is the **liquidity-share** edge under `bar`
(J_max 28.1, sharpness 29.5), i.e. the same X-extreme contrast that produces the top equifinal pairs; the
tutoring edge is sharpest under `quota` (J_max 18.0, sharpness 28.3). **No phase-transition verdict is made in
this record** — the pre-registered decision rule for that belongs to the sibling phase-transition workstream;
these numbers are provided so that lane can cite them.

---

## 8. Caveats and what this does NOT say

* **Toy world, no calibration.** `eduengine`'s parameters are illustrative; nothing here is an estimate for any
  country, period, or policy. No causal reading of fees, vacancies, or exam gates is possible from this design.
* **`GER_sim` is declared, not observed.** It is `1 − never_enrolled_share` on the measured population
  (cohorts ≥ 35 plus horizon-censored survivors), a simulated participation measure — not a UIS/empirical GER.
* **No contest arm** (see §1). The intended three-regime contrast is two-regime; conclusions about "contest vs
  quota vs bar" cannot be drawn. `bar` is near-open-access (pass rates ≈0.995–0.999), `quota` carries the
  selection — so the gate-regime factor is effectively "selection vs little selection" here.
* **Thresholds are pre-registered and strict.** The qualifying set is thin at the thresholds (max within-gate
  |Δliq| 28.1 pp, |Δtut| 20.4 pp), and the count is calibrated against a label-permutation null rather than
  tested against a causal hypothesis. One could report "176 pairs" alone and over-read it; the null says the
  count is *at or below chance*, and that is the pre-registered reading.
* **Null choice matters and is declared.** The permutation null destroys the joint (GER, liq, tut) dependence.
  It is the reference the prereg fixed; an alternative null preserving the joint structure would ask a
  different question and was not pre-registered.
* **Multiple comparisons**: the scan is exhaustive over the whole grid by design (no post-hoc cell selection),
  so no alpha adjustment is applied to the pair count; the null distribution provides the chance reference.
* **Missing mechanisms** (as in the base prereg): migration/emigration, rural–urban sorting/residential choice,
  remittances/kin transfers, country calibration, teacher labour supply outside the pay/monitoring channel,
  informal/formal composition beyond queue vs competitive.

---

## 9. Files, hashes, reproduction

Committed in `research/records/2026-11-25-equifinality-phase/` (SIMULATION label in every JSON metadata block
and in `data/README_LABEL.txt` for the headerless CSV artefacts):

| file | what |
|---|---|
| `PRE_REGISTRATION.md` | prereg, commit `078cc13` (before any run) |
| `phase_sweep_full.py` | runner (sha256 `e6fe8aa8…f12a05`); 20×20×{bar,quota}×20 |
| `analyze_equifinality.py` | exhaustive pair search + 1,000-perm null (sha256 `63c960dc…d7795e12`) |
| `validate_run.py` | independent validity checks (sha256 `bb6fe868…ad08a05c`) |
| `data/phase_sweep_full_runs.csv` | **all 16,000 seed-level rows** (6.4 MB, sha256 `3a6ef24c…c4449efb5`), `ok`/`error` included |
| `data/phase_sweep_full_summary.csv` / `.json` | 800 per-cell seed means + SDs + gate diagnostics + engine/code hashes |
| `data/equifinality_pairs.csv` | **every** qualifying pair (176 primary + 4,132 cross-gate) with coordinates and signed Δ |
| `data/equifinality_top50.csv`, `…_top50_crossgate.csv` | top 50 per family |
| `data/equifinality_null.json`, `data/equifinality_report.json` | null distributions, verdict, diagnostics |
| `data/equifinality_completion_lower_pairs.csv` | secondary pairing (0 rows) |
| `data/validity_checks.json` | partition / cell-mean / definition / reproducibility results |
| `data/repro_subset_runs.csv`, `data/repro_subset_summary.json` | the 360-run determinism re-run |
| `data/analysis_manifest.json`, `data/analysis_stdout.json`, `data/run.log`, `data/run_started_utc.txt` | provenance |

Reproduction: `python phase_sweep_full.py --engine-root <engine> --out <dir> --workers 12 --seeds 20 --gate all`
then `python analyze_equifinality.py --run-json data/phase_sweep_full_summary.json --runs-csv
data/phase_sweep_full_runs.csv --out data --n-perms 1000` and `python validate_run.py`. The engine is pinned by
the 16 sha256 hashes recorded in the run JSON; the analysis is a pure function of the committed CSV/JSON.

---

## 10. Deviation log (nothing re-tuned after seeing data)

1. **Contest arm not run** — pre-registered in `078cc13` §3 before any run; requested 24,000 → run 16,000
   (−8,000 runs, one gate arm); evidence in §1. Not proxied, not relabelled.
2. **Reproducibility subset** — the prereg promised "a 0.5% random subset if affordable"; the actual check was
   **18 cells / 360 runs = 2.25%** of the sweep, exceeding the declared minimum (bit-for-bit match, §4).
3. **Box contention** — a second window's brief bar-arm job overlapped mine for ~6 min (lease conflict raised
   and resolved by note, §3); no result impact (deterministic seeds, separate output dirs). Wall time quoted
   is the contended time.
4. **Analysis host** — host venv python 3.10.2 / numpy 2.2.6; analysis is a pure function of the committed
   box artefacts, and per-cell means were verified exactly against the raw box CSV (§4).
5. **Boundary diagnostics** included because they were cheap (prereg §8.2), descriptive only, no verdict (§7).
6. No engine file was edited; no power/reboot/watcher/timer action; no other deviations.

---

**SIMULATION ONLY — `eduengine` toy worlds; illustrative parameters; no causal or empirical claims.**
