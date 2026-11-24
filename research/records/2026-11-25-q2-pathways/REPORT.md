# Q2 — Country pathway comparisons: pair benchmark, audit, and a small case set

Branch `research/q2-pathways-2026-11-25`; record `research/records/2026-11-25-q2-pathways/`. Owner:
panel-matrix. Pre-registration: `PRE_REGISTRATION.md`, committed before any analysis (first commit `9af03b1`).
**This is a descriptive path comparison, not a causal design. No causal inference is drawn from time ordering,
matching similarity or outcome gaps.** Ties, failed cases and counterexamples are published.

## 1. Question

Do countries with similar 1980 starting conditions (attainment, fertility, income, urbanisation) take different
1990-2010 education and fertility paths, and what does a small set of matched pairs/triads look like when checked
against independent sources? The pair benchmark is a smoke test; the audit is the substance; the case set is an
illustration of paths, not a test of mechanisms.

## 2. Inputs and provenance

- Panel: `data/long_run_panel.csv`, copied verbatim from the Codex handoff bundle. **SHA-256
  `cd30d7ea7beb77b63de092c53f9b143065b94651f1ac95535ac70eebb3280f2d`** (matches the handoff letter; 42,959 rows,
  197 country codes, annual 1800-2023 with gaps).
- Pair script: `scripts/country_pairs.py`, copied verbatim; SHA-256
  `fbc4fda4e7a82fe5d7740f3409f39ae2d2d310baae5e9e1ddf155433f6a2d51b`.
- Farming series: `data/emp_agri.json` from the project panel on the box (7,845 country-year observations,
  first year **1991**, last 2024), SHA-256 `0957d15f9d3d92d0791241d74d65924f5acb0f74f80bcb5d70fd47a800182da5`.
  It is **WDI/ILO-modelled**, not observed; no earlier values exist in the series and none were invented.
- Environment: box `autodl3` (region-9), `/root/work/repo`, `/root/miniconda3/bin/python`, `pandas 2.3.3`,
  `numpy 2.2.6`, `scipy 1.15.3`, `OPENBLAS_NUM_THREADS=1`, `LD_LIBRARY_PATH=/root/miniconda3/lib` (the box's
  OpenBLAS needed the explicit path in this session; recorded as a deviation). CPU only; seconds per run.

**Series labels (fixed in the pre-registration, kept here).** `tfr_observed_1950plus` is the **observed**
births-based TFR; `mean_years_schooling`, `gdp_pc_maddison_1990int`, `urban_share_pct`, `child_mortality_per100`,
`life_expectancy_years` are **reconstructed** series (Barro-Lee/Wittgenstein, Maddison, WUP-type); `effective_fertility`
is **modelled** expected surviving children and is **not** used as an outcome (Codex F01/F03). "Similar baseline"
means similar on these reconstructions, not historical identity.

## 3. Smoke test — reproduced exactly

Command: `python scripts/country_pairs.py --panel data/long_run_panel.csv --baseline 1980 --start 1990 --end 2010
--out results/smoke`. Output (`results/smoke/pairs_metadata.json`): **105 baseline-complete countries, 52 disjoint
pairs, 1 unpaired country (YEM), 52 pairs with both 1990-2010 schooling changes, 52 pairs with both TFR changes**,
input SHA-256 as above. This matches the handoff letter exactly; no deviation to explain. Pair list, raw
diagnostics and stdout are committed.

## 4. Audit

### 4.1 Baseline coverage and selection
Panel: 197 country codes. At 1980: schooling present for **109**, TFR for **197**, GDP for **161**, urbanisation
for **197**; complete on all four = **105**. The matched sample is close to the full panel on every feature:
differences are −0.003 SD (schooling), −0.105 SD (TFR), +0.097 SD (log GDP), +0.133 SD (urbanisation) — all below
the pre-specified 0.5 SD flag, so the selection is **modest but real** (the sample still omits 92 country codes,
mostly those without 1980 schooling or GDP data). Tables: `results/audit/audit_coverage_features.csv`,
`audit_selection.csv`.

### 4.2 Matching sensitivity (pre-specified alternatives)
| matching | pairs | overlap with primary | median baseline distance | median schooling gap | median TFR gap |
|---|---|---|---|---|---|
| primary: greedy Euclidean (z-scores) | 52 | 52/52 | 0.462 | 0.620 | 0.2375 |
| greedy Manhattan | 52 | **11/52 (21.2%)** | 3.075 | 0.615 | 0.350 |
| greedy Mahalanobis | 52 | **15/52 (28.8%)** | 0.834 | 0.795 | 0.406 |
| three-feature (drop TFR) | 52 | 32/52 (61.5%) | 0.340 | 0.615 | 0.389 |
| 2-opt-improved Mahalanobis (approx. optimal) | 52 | **15/52 (28.8%)** | 0.840 | 0.815 | 0.376 |

The pre-registered falsifier **fires**: the primary pair set overlaps <50% with two alternatives (Manhattan
21.2%, Mahalanobis/2-opt 28.8%). The specific pairs are therefore **matching-dependent**; only conclusions that
survive across matchings (median gaps of similar size) are interpretable. The Hungarian/optimal-assignment variant
could not be run as specified: networkx is absent on the box and the MILP formulation did not solve within the
session limit, so a deterministic 2-opt local search on Mahalanobis distances is reported **as an approximation**
and is labelled as a deviation. Sources: `results/audit/audit_matching_sensitivity.csv`.

### 4.3 Random-matching yardstick (descriptive, not a p-value)
1,000 random disjoint pairings of the same 105 countries (seed 71201; same 52-pair/1-unpaired structure). The
observed matched pairs are **not unusually divergent**:
- median absolute schooling gap: observed **0.82 years**; random median **0.825**; share of random draws whose
  median is at least as large as observed **52.4%** (random 2.5-97.5% range 0.60-1.045);
- median absolute TFR gap: observed **0.77**; random median **0.773**; share ≥ observed **50.3%**.

In other words, matching on 1980 similarity does **not** produce larger 1990-2010 divergence than random pairing
in this sample. This is the central honest null of Q2: the pair benchmark describes paths, but it does not show
that similar starts produce unusually divergent outcomes. Source: `results/audit/audit_random_yardstick.json`.

### 4.4 Farming employment where dated
`emp_agri.json` begins in **1991**; 1990 is absent. Per the pre-registration no earlier values were invented and
no backcasting was done. For the case countries, the 1991→2010 changes in the **modelled** agricultural employment
share are: ECU +0.7 pp, ZAF −4.7, SWZ −2.9, ZWE **+14.5**, FIN −4.3, ITA −4.7, BEN −2.8, SLE +0.6. The ZWE
increase is a warning against reading the series as "farm exodus": Zimbabwe's agricultural share rose while its
schooling stock rose, which is a collapse of non-agricultural employment, not structural transformation. Source:
`results/audit/audit_farming_dated.csv`.

## 5. Selection flow and case set

Flow: 197 panel codes → 105 baseline-complete (1980, four features, GDP>0) → 52 disjoint pairs + 1 unpaired (YEM)
→ 52 pairs with both outcomes. Holdout split by baseline-distance rank: even pairs = half A (hypothesis-generating),
odd = half B (case-checking); 26 pairs each. **All** rule-based candidates and the attempted triad are reported.

| rule | candidate(s) | half | used? |
|---|---|---|---|
| 1. divergent close (largest summed gap, close pairs) | **SWZ-ZWE** (gap 6.09 SD), ECU-ZAF (4.34) | A, **B** | SWZ-ZWE published as exploratory (half A); **ECU-ZAF** as the half-B case |
| 2. convergent close (smallest gap) | HKG-ISL (0.43), **FIN-ITA** (0.48), **BEN-SLE** (0.51) | B, **B**, **B** | **FIN-ITA** and **BEN-SLE** published (both half B) |
| 3. divergent distant (largest gap, far pairs) | DZA-IRN (7.14), KWT-VEN (6.25), HTI-MOZ (4.52) | A, A, A | **unattempted under the holdout rule** (no half-B candidate); reported, not replaced |
| 4. triad | SWZ-ZWE + nearest neighbour **YEM** (distance 1.80) | A | **rejected**: YEM is the unpaired country and 1.80 is far outside the close-pair range; not a valid triad |
| 5. counterexample | BEN-SLE (predicted divergence, observed convergence) and the random-yardstick result | B | published |

So the case set is **four pairs** (ECU-ZAF, SWZ-ZWE, FIN-ITA, BEN-SLE) plus one **rejected triad**. The
divergent-distant rule is reported unattempted, not silently substituted.

## 6. Case table and independent checks

Panel values are reconstructed (`mean_years_schooling`) and observed TFR (`tfr_observed_1950plus`). Independent
checks use the World Bank WDI API (queried in-session; `results/independent_source_checks.csv`): TFR
(`SP.DYN.TFRT.IN`) matches the panel's observed TFR **exactly** for all four cases (1990 and 2010); the modelled
agri-share (`SL.AGR.EMPL.ZS`) confirms the 1991-2010 changes above; schooling is cross-checked with WDI enrolment
indicators, which are a **different construct** from mean years of schooling and are labelled as such.

| case | baseline distance | schooling 1990→2010 (panel) | TFR 1990→2010 (panel; WDI) | agri share 1991→2010 (modelled) | independent check / note |
|---|---|---|---|---|---|
| **ECU-ZAF** (divergent close, half B) | 0.411 | ECU 7.23→8.02 (**+0.79**); ZAF 6.89→9.89 (**+3.00**) | ECU 3.68→2.615 (3.68→2.615); ZAF 3.724→2.445 (3.724→2.445) | ECU 29.1→29.8 (+0.7); ZAF 9.4→4.8 (−4.7) | WDI secondary GER: ECU 56.0 (2000)→91.6 (2010); ZAF 67.8 (1990)→86.6 (2010). Paths diverged in schooling, **converged in fertility**. |
| **SWZ-ZWE** (divergent close, half A, exploratory) | 0.430 | SWZ 5.28→5.33 (**+0.05**); ZWE 5.97→7.86 (**+1.89**) | SWZ 5.295→3.375 (5.295→3.375); ZWE 4.876→4.04 (4.876→4.04) | SWZ 17.2→14.3 (−2.9); ZWE 47.7→62.2 (**+14.5**) | WDI secondary GER: SWZ 43.3 (2000)→64.6 (2010); ZWE 45.2 (1990)→40.0 (2000). Zimbabwe's 1980s schooling expansion and 2000s crisis fit the divergence in schooling; the **rising** agricultural share contradicts a simple "farm exodus" reading. |
| **FIN-ITA** (convergent close, half B) | 0.364 | FIN 8.56→10.71 (+2.15); ITA 8.32→10.71 (+2.39) | FIN 1.776→1.863; ITA 1.331→1.443 | FIN 8.9→4.6 (−4.3); ITA 8.4→3.8 (−4.7) | WDI TFR exact; both post-transition fertility paths flat/rising. Comprehensive-school reforms (Finland 1970s, Italy 1962 middle school) are consistent with the shared attainment path but are not identified here. |
| **BEN-SLE** (convergent close, half B; counterexample) | 0.253 | BEN 2.24→4.57 (+2.33); SLE 2.17→4.28 (+2.11) | BEN 6.741→5.452; SLE 6.567→5.327 | BEN 46.6→43.7 (−2.8); SLE 64.3→64.9 (+0.6) | WDI primary completion: BEN 17.6 (1990)→62.6 (2010); SLE primary GER 51.1 (1990)→63.3 (2000). Similar attainment and fertility paths **despite** very different agricultural shares — a counterexample to a common-path story. |

Historical context was read from secondary sources in-session (South Africa's 20-year review
`dpme.gov.za/publications/20%20Years%20Review`, Ecuador's CESCR state report via `ecoi.net`, a Finnish
comprehensive-school dissertation via `db-thueringen.de`, a comparative compulsory-schooling-reform appendix via
Springer). **These historical details are secondary-source summaries, not primary-document verification**, and are
labelled as such.

## 7. What this supports and what it cannot

**Supports (descriptive):** a reproducible pair benchmark (105/52/1/52); a transparent audit showing the matched
pairs are matching-dependent; a random-matching yardstick showing the matched pairs are **not** unusually
divergent; dated (modelled) farming series used without backcasting; four matched cases plus a rejected triad and
an unattempted rule, all published.
**Cannot support:** any claim that similar starting conditions cause divergent paths; any causal reading of
schooling/fertility/labour ordering; a general statement about "countries" from 105 selected cases; any claim that
Zimbabwe's schooling expansion "caused" its fertility or labour changes (the case is shown as a path with
contradictory indicators, not a mechanism). The panel's schooling series is reconstructed and **shows tension**
with WDI enrolment in two cases (ECU's panel attainment rises little while WDI secondary GER rises strongly;
ZWE's panel attainment rises while WDI secondary GER falls to 2000) — a limitation of the reconstructed stock,
recorded rather than hidden.

## 8. Limitations

Selected 1980 complete cases (105 of 197 codes); baseline similarity is similarity on reconstructions, not
historical identity; matched pairs are not independent; greedy matching is not globally optimal and the pair set
is sensitive to the metric; the optimal-assignment variant was approximated (2-opt); the farming series is modelled
and starts in 1991; the historical checks are secondary sources; the case set is illustrative and deliberately
includes failures. No causal inference is made anywhere.

## 9. Deviations from the pre-registration

1. **Optimal matching**: the pre-specified Hungarian/optimal variant was not available (no networkx; MILP exceeded
   the session limit). Replaced by deterministic 2-opt local search on Mahalanobis distances, labelled
   "approximate optimal". The greedy Mahalanobis result is unchanged and is reported alongside.
2. **Farming start year**: `emp_agri.json` begins in 1991, not 1990. No earlier values were invented; the table
   uses 1991→2010 and labels the series modelled.
3. **Environment**: the box required `LD_LIBRARY_PATH=/root/miniconda3/lib` for numpy/OpenBLAS in this session;
   recorded for reproduction. No analysis was run on a different machine.

## 10. Files

`PRE_REGISTRATION.md` (first commit); `scripts/country_pairs.py` (verbatim benchmark) and `scripts/q2_audit.py`
(coverage, alternatives, random yardstick, cases, farming); `data/long_run_panel.csv`, `data/emp_agri.json`;
`results/smoke/`; `results/audit/` (`pairs_primary.csv`, `pairs_with_halves.csv`, `audit_coverage_features.csv`,
`audit_selection.csv`, `audit_matching_sensitivity.csv`, `audit_random_yardstick.json`, `case_candidates.json`,
`audit_farming_dated.csv`, `audit_summary.json`); `results/independent_source_checks.csv` (World Bank API values).
Reproduction: `OPENBLAS_NUM_THREADS=1 LD_LIBRARY_PATH=/root/miniconda3/lib python scripts/q2_audit.py --panel
data/long_run_panel.csv --out results/audit`.
