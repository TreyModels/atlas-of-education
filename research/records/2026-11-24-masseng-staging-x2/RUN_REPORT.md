# RUN REPORT — X2 gate/tutoring inequality factorial + X4 honest-split aggregate test (task-28)

**EXPLORATORY. X2 = SIMULATION ONLY on stipulated `eduengine` toy worlds (no country fit, no
causal language; rural migration not simulated — rural is a household attribute + `rural_cost`
+ lower tutoring-firm access). X4 = observed aggregates only, no simulation, no causal claim.
No confirmatory claims; no E1 comparison.**

**X2 falsifier verdict FIRST: NOT CONFIRMED — quota gates DO raise gate-prep tutoring** (+17.6 to
+21.1 pp overall; +23.8 to +28.9 pp at gate-adjacent grades; gate-concentrated by +9.0 to +9.6 pp
DiD), and they **widen the top-vs-bottom tutoring gap** (+13.0 to +14.5 pp) instead of leaving
inequality neutral. The original-claim falsifier fails; the quota tutoring jump is **both**
gate arithmetic **and** inequality-relevant. One secondary pre-declared hypothesis was falsified in
the opposite direction: raising rural tutoring access did **not** reduce the wealth gap — it
widened it (+7.9 pp bar, +9.4 pp quota).

**X4 verdict NEXT: FAIL / NO EVIDENCE (not insufficient — the honest split is feasible: 40
training / 21 validation countries).** The pre-registered education-vs-jobs ordering score does
not beat persistence or pooled trend out of sample (paired MAE vs persistence −2.49, 90 % CI
[−5.76, +0.77]; vs pooled trend −0.67, [−2.04, +0.66]) and its coefficient is not positive in the
expected direction (b1 = −2.05, 90 % CI [−4.44, +0.87]). All four robustness specs likewise
FAIL_NO_EVIDENCE. **The aggregate data do not support the staging implication at this honest
split; no window or split was hunted and no match was forced.**

Pre-registration: `PRE_REGISTRATION_masseng_staging_x2_x4.md`, commit **`0b6e324`**, committed
before code and before any run. Branch `research/masseng-staging-x2-2026-11-24` (additive from
`fef7428`). Engine used unmodified (`engine/worlds.py 2e9ec71a…`,
`engine/eduengine/core.py 2b7484a9…` — identical to the audited staging server copies).

---

## 1. Execution and provenance

| item | value |
|---|---|
| server | region-42, 96 cores, Python 3.10.8, NumPy 2.2.6, SciPy 1.15.3 via `PYTHONPATH=/root/work/masseng-codex-deps` |
| workers | 20 (declared bound) for X2; X4 is a single-process statistical analysis |
| X2 command | `PYTHONPATH=/root/work/masseng-codex-deps python run_x2.py --workers 20 --out results_x2_EXPLORATORY.json > x2.log 2>&1` |
| X2 result | **240 runs, elapsed 24.549 s** (launched 13:13:27Z, done 13:13:52Z); sha256 **`1b2494c6…`**; analysis `audit_tables/summary_x2.json` sha256 **`caaa69e5…`** |
| X4 command | `PYTHONPATH=/root/work/masseng-codex-deps python run_x4.py --out results_x4.json > x4_final.log 2>&1` |
| X4 result | 5 pre-declared specs, all run, seconds of CPU; sha256 **`685a3a3b…`** |
| driver hashes | `run_x2.py a16368b4…`; `run_x4.py 197652ba…`; `analyze_x2.py 591fe8ed…`; extraction `extract_x4_panel.py` + `x4_input/x4_panel.csv 01590120…`, provenance `b63b2147…` |
| X4 failures disclosed | run 1: `KeyError: 'lsc_2004'` (analysis column naming) — no model fitted, no result, traceback `x4_v1_failure.log`; run 2: `KeyError: 'ARG'` (split map built from non-existent `lsc_*` columns) — no model fitted, no result, traceback `x4_v2_failure.log`. Both are code bugs, logged in the pre-registration deviations before the successful run; windows, split rule, scores, benchmarks, thresholds and decision rule were **not** changed. The successful run is `x4_final.log` → `results_x4.json`. |
| preservation | fresh files only (exclusive creation); old results untouched; no engine edits; no Codex-branch rewrite. |

---

## 2. X2 — gate/quota × tutoring inequality factorial (240 runs, 2×3×2×20 seeds)

Design: `formal_loop`, N=400 children/cohort, T=70, cohorts 35–44 measured, no events,
`job_elasticity=0`; gates {bar, quota} × `rural_firm_access` {0.2, 0.4, 0.8} × `own_ban`
{off, full} × 20 seeds. Material threshold 1 pp; 90 % seed-bootstrap CIs (4,000 draws); all
contrasts paired by seed.

**Pre-declared hypothesis results.**

| hypothesis | pre-declared rule | observed | verdict |
|---|---|---|---|
| **H1 gate-prep**: quota raises tutoring vs bar (ban off) | tut_rate and gate-adjacent tutoring material-positive in ≥2/3 access levels | access 0.2/0.4/0.8: tut_rate **+17.60/+18.75/+21.08 pp** (all CIs exclude 0); gate-adjacent **+23.82/+25.66/+28.87 pp** — both positive in **3/3** | **H1 SUPPORTED; falsifier NOT confirmed** |
| **H1b ban**: own-teacher ban reduces tutoring | material-negative in ≥2/3 access levels for both gates | bar: −13.5/−12.5/−11.0 pp; quota: −22.6/−19.1/−11.8 pp, all material-negative | **H1b SUPPORTED** |
| **H2 inequality**: quota widens top-vs-bottom tutoring gap | material-positive in ≥2/3 access levels (ban off) | gap quota−bar **+13.01/+13.62/+14.48 pp** at access 0.2/0.4/0.8, all CIs exclude 0 | **H2 SUPPORTED; falsifier NOT confirmed** |
| **H3 access gradient**: higher rural access reduces the wealth gap | material-negative in **both** gates | access0.8−access0.2 gap **+7.91 pp (bar), +9.38 pp (quota)** — positive, CIs exclude 0 | **H3 FALSIFIED (opposite sign)** |
| **Gate-specificity DiD**: quota effect on gate-adjacent minus non-gate grades | material-positive ⇒ gate-concentrated | **+9.03/+9.33/+9.58 pp** at access 0.2/0.4/0.8, all material-positive | **gate-concentrated component present** |

**Absolute tutoring levels (ban off, mean over seeds):** bar/access0.2 `tut_rate` 0.240, gate-adjacent
0.299; quota/access0.2 0.416 / 0.538; quota/access0.8 0.484 / 0.614. **Completion effects of
quota vs bar (ban off):** lower −11.7…−12.3 pp, upper −13.5…−14.5 pp, tertiary −9.8…−10.9 pp (quota
caps completion, gate arithmetic), while the **wealth completion gap narrows** (−15.3…−16.2 pp)
because the quota caps all quintiles; rural/urban lower-completion parity moves −6.6…0.0 pp.

**Reading (toy model only):** the audit's question — is the quota tutoring jump "gate arithmetic
or inequality-relevant?" — has answer **both**: it is gate-concentrated (DiD material positive,
consistent with gates mechanically raising gate-prep demand and capping completion) **and** it is
inequality-relevant (quota widens the top-vs-bottom tutoring gap by 13–14.5 pp, and raising rural
tutoring access widens rather than narrows the wealth gap in this model). The own-teacher ban
reduces tutoring substantially but does not remove the gate response. No causal/empirical reading
is made: these are stipulated toy worlds.

---

## 3. X4 — honest-split aggregate observed-data staging test (no simulation)

Design (frozen before analysis): committed WDI/UIS aggregates (massification-panel branch
`7d25322e…`), national countries only, complete-case only; predictor window 1991–2004 (midpoint
1998); outcome window 2004–2018; deterministic honest split (national ISO3 sorted, every third
validation): **40 training / 21 validation** complete-case countries; primary score = timing-order
`S_order` (training-only z-scoring); model = OLS `Δlsc(2004→2018) ~ 1 + S_order + lsc(2004)`;
benchmarks = persistence (Δ=0) and pooled trend (training-mean Δ); paired country-level MAE,
4,000-draw bootstrap, 90 % CIs.

**Primary result (pre-registered).**

| quantity | value |
|---|---|
| training / validation countries | 40 / 21 |
| model MAE | **8.81 pp** |
| persistence MAE | 11.30 pp |
| pooled-trend MAE | 9.48 pp |
| paired MAE, model − persistence | **−2.49** [−5.76, +0.77] (90 % CI includes 0) |
| paired MAE, model − pooled trend | **−0.67** [−2.04, +0.66] (includes 0) |
| score coefficient b1 (expected >0) | **−2.05** [−4.44, +0.87] (CI includes 0; sign opposite to expectation) |
| **decision** | **FAIL_NO_EVIDENCE** (`beats_persistence=False`, `beats_pooled_trend=False`, `b1_positive_ci_excludes_zero=False`) |

Point-estimate MAE is lower than both benchmarks, but the paired country-level uncertainty does not
establish a beat, and the ordering coefficient is not positive. **Falsifier confirmed: the
model-implied ordering does not beat persistence/trend out of sample ⇒ no evidence for the model's
staging implication in these aggregates.**

**Pre-declared robustness (reported, no decision authority; all FAIL_NO_EVIDENCE):**

| spec | n train/valid | b1 [90 % CI] | model / persistence / trend MAE | paired vs persistence [90 % CI] | paired vs trend [90 % CI] |
|---|---|---|---|---|---|
| S_net instead of S_order | 41/22 | +1.40 [−2.90, +6.22] | 9.68 / 11.92 / 9.68 | −2.24 [−5.18, +0.75] | −0.002 [−0.95, +0.94] |
| window C (1995–2005 → 2005–2019) | 49/23 | −1.17 [−3.68, +1.62] | 7.91 / 10.06 / 8.13 | −2.16 [−4.61, +0.18] | −0.22 [−0.92, +0.45] |
| outcome secondary NER | 23/18 | +0.56 [−2.82, +5.45] | 8.33 / 9.85 / 8.26 | −1.52 [−3.61, +0.85] | +0.07 [−1.72, +1.81] |
| job proxy −Δagricultural share | 40/21 | −2.20 [−4.78, +0.96] | 8.70 / 11.30 / 9.48 | −2.60 [−5.86, +0.66] | −0.78 [−2.20, +0.60] |

**Not insufficient evidence:** the split and windows were feasible and fixed in advance (40/21
complete cases; thresholds ≥20/≥10); the design was not re-chosen after seeing outcomes. The result
is a genuine negative finding at aggregate level, with the binding construct caveat that observed
data contain only attainment/enrolment aggregates — no child-work 4-state decomposition, no
tutoring/learning — so this tests a thin observable implication, not the full model.

**Bugs disclosed (no results from failed runs):** see §1. Both failures occurred before any model
fit; traces preserved; only column/split naming was fixed, no design change.

---

## 4. Wall times, cost, server state

| run | runs | elapsed | wall | workers |
|---|---|---|---|---|
| X2 | 240 | **24.549 s** | 13:13:27 → 13:13:52Z | 20 |
| X2 analysis | — | a few s | on box | single |
| X4 (final) | 5 specs (61/63/72/41/61 complete cases) | seconds | 13:16Z | single |

Total model compute ≈25 s at 20 workers; X4 is CPU-seconds. The two 4,096-draw Bayesian screens
had already completed earlier (Lead owns their audit); no jobs were killed; box load was ~17 from
co-tenant work; our pool was bounded at 20. Nothing server-only is required by this task.

---

## 5. Caveats (binding)

1. **X2 is synthetic/stipulated** toy worlds — not fitted to any country; gate/ban/access parameters
   are declared scenario values, not estimates; no causal or empirical claim. **Rural migration is
   not simulated** (rural attribute + cost + tutoring access only), so the H3/inequality results are
   within a fixed rural-urban population.
2. **X4 is aggregate-only and exploratory**: net enrolment, completion, wage-share proxies; no
   child-work/tutoring/learning constructs; PHL-style post-1995 data were inspected elsewhere, so
   this is retrospective; no causal claim; no confirmatory claim.
3. No p-values are used as evidence; uncertainty is Monte Carlo (X2 seeds) or country-bootstrap
   (X4). Thresholds/decision rules were pre-declared and are reported exactly, including where a
   pre-declared expectation (H3, X4 direction) was contradicted.
4. X4's two failed runs are preserved and were not interpreted; no window/split hunting.
5. No comparison with E1's 1.8 %; no theory ranking.

## 6. Files, hashes, commits

- `results_x2_EXPLORATORY.json` — **`1b2494c6…`**; `audit_tables/summary_x2.json` — **`caaa69e5…`**
- `results_x4.json` — **`685a3a3b…`**; `x4_input/x4_panel.csv` — `01590120…`; `x4_input/provenance.json` — `b63b2147…`
- logs: `x2.log`, `analyze_x2.log`, `x4_final.log`, `x4_v1_failure.log`, `x4_v2_failure.log`, `run_meta.txt`
- code: `run_x2.py` (`a16368b4…`), `run_x4.py` (`197652ba…`), `analyze_x2.py` (`591fe8ed…`), `extract_x4_panel.py`
- prereg `0b6e324`; code/data `0bdb0df`; failures/fixes `df74e4c`, `1a85173`, `4dfe3ed`; results/report (this commit)
  on branch `research/masseng-staging-x2-2026-11-24`, additive from `fef7428`.
