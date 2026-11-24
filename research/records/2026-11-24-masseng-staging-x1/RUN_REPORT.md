# RUN REPORT — X1 exposure-matched sequencing + X3 feedback-elasticity surface (task-27)

**EXPLORATORY. SIMULATION ONLY — stipulated `eduengine` toy worlds, not fitted to any country.
No causal language, no confirmatory claim, no empirical inference. Rural migration is not
simulated (rural = household attribute + extra schooling cost + lower tutoring-firm access).**

**X1 falsifier verdict first: CONFIRMED on the exposure-sensitive formal-share metric — the
apparent "school-first vs jobs-first" advantage does NOT survive exposure matching** (the
unmatched −5.4 pp formal-share gap collapses to −0.13…+0.56 pp, i.e. 2–12 % of its size, once
cumulative education-share and vacancy exposure are equalised). The completion/equity side shows
no material sequencing effect before or after matching. A model-internal timing effect does
appear on public quality (`q_pub`, education-first lowers it by 2.4–7.1 pp under matched totals)
and on tutoring — reported as toy-model dynamics, **not** as a sequencing claim.

**X3 verdict: the feedback-elasticity assumption does not rescue the sequencing claim.** Across
`job_elasticity ∈ {0,.25,.5,.75,1}` there are **no sign reversals**; the sequencing contrast is
mostly **NULL** on completion/equity metrics (9–11 of 13 metrics), with only the mechanically
exposed `formal_share_gdp` robust (negative, −5.4…−4.8 pp); the both-early-vs-neither contrast is
robust on 10–13/13 metrics. Report of the full surface is in `audit_tables/summary_x3.json`.

Pre-registration: `PRE_REGISTRATION_masseng_staging_x1_x3.md`, commit **`e3a3975`**, committed
**before** the driver and before any run. Branch `research/masseng-staging-x1-2026-11-24`
(additive from audit head `ff84e75`). Engine used unmodified (`engine/worlds.py`,
`engine/eduengine/`); no Codex branch rewritten.

---

## 1. Execution, provenance, and one declared invalidation

| item | value |
|---|---|
| server | region-42 (`root@region-42.seetacloud.com:54585`), 96 cores, `/root/miniconda3/bin/python` 3.10.8, NumPy 2.2.6, SciPy 1.15.3 via `PYTHONPATH=/root/work/masseng-codex-deps` |
| workers | **20** for every run (declared bound; the two 4,096-draw Bayesian screens had finished at 13:00Z, ~1 min before our launches; nothing was killed, no interference) |
| engine hashes (server == committed `ff84e75` tree == the audited staging server copies) | `engine/worlds.py 2e9ec71a…`; `engine/eduengine/core.py 2b7484a9…` (all modules hashed in each result JSON) |
| driver hashes | **corrected run:** `run_x1_x3.py 0253dcc4…`; **invalid run 1:** `f9c8da4e…` |
| exact commands (also in `run_meta.txt`) | X1: `PYTHONPATH=/root/work/masseng-codex-deps python run_x1_x3.py --experiment x1 --workers 20 --out results_x1_EXPLORATORY_corrected.json > x1_corrected.log 2>&1`; X3: `… --experiment x3 --workers 20 --out results_x3_EXPLORATORY.json > x3.log 2>&1` |
| X1 run 1 (13:01:10Z) | 720 runs, **elapsed 73.825 s** — output `results_x1_EXPLORATORY.json` (sha256 `e860b727…`), **INVALID for the primary analysis** (see below). Run 1 is committed unchanged as `results_x1_EXPLORATORY.json`; the server also keeps a byte-identical copy named `results_x1_v1_INVALID_matched_arms_not_exposure_matched.json` (same sha256), not duplicated in git |
| X1 corrected (13:05:35Z) | 720 runs, **elapsed 72.593 s** — `results_x1_EXPLORATORY_corrected.json` sha256 **`a4892cb7…`** |
| X3 (13:03:10Z) | 800 runs, **elapsed 81.283 s** — `results_x3_EXPLORATORY.json` sha256 **`2a4a8c1c…`** |
| seeds | 0–19 for every cell (no seed selection) |
| preservation | every output written with exclusive creation; run 1 was copied to an explicitly labelled INVALID file (not overwritten) before the corrected run; the committed run-1 JSON is byte-identical; logs and `run_meta.txt` kept |

**Declared invalidation (transparent):** the first X1 implementation defined the two dose-matched
arms with one-way step events but **without end events**, so the early intervention stayed on for
all 70 years; its emitted exposure check was `matched_school_first` 21.0/9.44 and
`matched_jobs_first` 18.36/11.2 edu-share-/vacancy-years, **not the declared 18.36/9.44 for both**.
That run is **not exposure-matched** and is **not interpreted**. The fix (logged in the
pre-registration's deviations log **before** the corrected run) adds year-48 revert events
(`education_revert`→0.18, `vacancy_revert`→0.08) so each intervention is treated exactly 48 years;
the corrected run's exposure check is exactly **18.36 / 9.44 for all three matched arms**. Only the
pre-declared arms and seeds were rerun; no arms, seeds or thresholds were changed. X3 was
unaffected (it uses only the four original schedules) and ran once.

---

## 2. X1 — exposure-matched sequencing (primary result)

Arms (cumulative 70-year exposure): unmatched `school_first` 19.2/8.8, `jobs_first` 17.4/10.0
(the audit contrast); **matched** `matched_school_first`, `matched_jobs_first`,
`matched_simultaneous` all at **18.36 education-share-years / 9.44 vacancy-years** (48 treated
years each, opposite timing, with the early spell reverted at year 48); calendar-shift placebos
`shifted_school_first` 18.0/8.0, `shifted_jobs_first` 16.2/9.2.

Primary contrast = **`matched_school_first − matched_jobs_first`** (equal total exposure, opposite
order). Seed-level paired differences, 20 seeds, 4,000-draw bootstrap; 90 % CIs. Material
thresholds pre-declared: 0.5 pp completion; 2 pp for exposure/equity metrics; matched ≈0 =
90 % CI includes 0 **and** |matched| ≤ 0.25 |unmatched|.

| metric (per condition) | unmatched `school_first − jobs_first` | **matched** `matched_school − matched_jobs` | matched/unmatched |
|---|---|---|---|
| `formal_share_gdp` — fb0/bar | **−5.41 pp** [−5.57, −5.24], 0+/20− | **−0.13 pp** [−0.36, +0.10], 9+/11− | **0.02** |
| `formal_share_gdp` — fb0/quota | −5.24 pp, 0+/20− | +0.13 pp [−0.08, +0.34] | **0.02** |
| `formal_share_gdp` — fb1/bar | −5.19 pp, 0+/20− | +0.45 pp [+0.12, +0.80], 10+/10− | **0.09** |
| `formal_share_gdp` — fb1/quota | −4.78 pp, 0+/20− | +0.56 pp [+0.23, +0.86] | **0.12** |
| `q_pub` — fb0/bar | −2.16 pp, 0+/20− | **−7.07 pp** [−7.20, −6.94], 0+/20− | 3.3× (same sign) |
| `q_pub` — fb0/quota | −1.57 pp | **−4.47 pp** [−4.58, −4.36] | 2.9× |
| `q_pub` — fb1/bar | −1.59 pp | **−3.15 pp** [−3.29, −3.01] | 2.0× |
| `q_pub` — fb1/quota | −1.34 pp | **−2.36 pp** [−2.45, −2.28] | 1.8× |
| `tut_rate` — fb0/bar | +0.46 pp | **+0.95 pp** [+0.86, +1.04], 20+/0− | 2.1× |
| `tut_rate` — fb0/quota | −0.29 pp | **+2.16 pp** [+2.01, +2.32], 20+/0− | material |
| `tut_rate` — fb1/bar | +0.47 pp | +0.56 pp [+0.47, +0.64] | 1.2× |
| `tut_rate` — fb1/quota | −0.05 pp | +1.46 pp [+1.30, +1.61] | 32× (small base) |
| completion_lower — all conditions | −0.22…+0.02 pp, not material, sign-unstable | −0.03…+0.14 pp, not material | — |
| completion_upper — all conditions | not material | ≤ +0.40 pp, not material | — |
| completion_tertiary — all conditions | not material | ≤ +0.26 pp, not material | — |
| completion_primary — fb0/bar | −0.21 pp (not material) | −0.51 pp [−0.80, −0.20] (material) | category B only here |
| placebo `shifted_school − shifted_jobs` on `formal_share_gdp` | — | −6.22/−6.23/−7.56/−6.89 pp (all **outside** the unmatched 90 % CI) | calendar-sensitive |

**Pre-declared decision categories (strict rule):**
- Exposure-sensitive family (`formal_share_gdp`, `edu_gdp`, `q_pub`): **A** in 2 conditions
  (feedback 0: matched formal-share CI includes 0 and ratio ≤0.25), **D** in 2 conditions
  (feedback 1: residual +0.45…+0.56 pp is small (ratio ≤0.12) but its CI excludes 0) →
  overall by the strict ≥3/4 rule: `inconsistent`. **By the pre-declared material magnitude
  criterion the falsifier is confirmed:** exposure matching removes **88–98 %** of the formal-share
  contrast. `q_pub`, however, does **not** behave like the other exposure metrics: under matched
  totals education-first lowers public quality by 2.4–7.1 pp (same sign, larger than unmatched) —
  the fiscal loop means early jobs raise revenue and hence quality earlier.
- Completion/equity family: **B** in 1 condition (fb0/bar, `completion_primary`), **C** in 2
  (no material unmatched effect), **D** in 1 → by the strict ≥3/4 rule `inconsistent`; but on all
  four completion metrics the matched contrasts are **< 0.5 pp and not material**, so **no
  completion sequencing effect survives or appears**.
- The pre-declared **anticipated outcome** ("A on exposure-sensitive family; C on
  completion/equity") is supported **on magnitude** for `formal_share_gdp` and entirely for
  completion, but the strict binary A/≈0 rule is not met on `q_pub`/`edu_gdp` and the feedback=1
  formal-share residuals; the strict overall labels are reported above rather than massaged.
- **Placebo:** shifting the calendar by +10 years changes the formal-share contrast from −5.2…−5.4 pp
  to −6.2…−7.6 pp (outside the unmatched CI) and collapses the `q_pub` contrast to ≈0 in the
  feedback=1 arms → calendar/cohort-window position is itself a material driver of the unmatched
  contrast. The unmatched "order" effect is therefore **doubly confounded** (dose + calendar).

**Reading (exploratory, stipulated worlds only):** the audited staging claim that early
school-funding vs early jobs produces a completion/formal-share difference is **not supported as a
sequencing effect**: most of the formal-share gap is cumulative exposure/revenue, completion shows
no material effect at any stage, and calendar position changes the answer. The matched design does
surface a model-internal fiscal-timing dynamic (education-first lowers public quality; jobs-first
raises it early through the tax base) and a gate-prep tutoring response — flagged for follow-up,
not as evidence about real systems.

---

## 3. X3 — feedback-elasticity surface

Grid: `job_elasticity ∈ {0, 0.25, 0.5, 0.75, 1.0}` × 4 original schedules × 2 gates × 20 seeds =
800 runs; full surface in `audit_tables/summary_x3.json` (means and 90 % CIs per cell).
Verdicts (pre-declared: ROBUST = material, same sign at every elasticity; REVERSAL = material sign
change; NULL = never material; MIXED otherwise):

| contrast | ROBUST | NULL | MIXED | REVERSAL |
|---|---|---|---|---|
| `school_first − jobs_first`, bar gates | 1 (`formal_share_gdp`, −5.36…−5.19 pp across elasticities) | 9 | 3 | **0** |
| `school_first − jobs_first`, quota gates | 1 (`formal_share_gdp`, −5.24…−4.78 pp) | 11 | 1 | **0** |
| `simultaneous − none`, bar gates | 13 | 0 | 0 | **0** |
| `simultaneous − none`, quota gates | 10 | 2 (completion lower/upper — quota caps) | 1 | **0** |

- **Falsifier (conclusions reverse across the elasticity grid): NOT triggered — zero reversals.**
  However, the sequencing contrast is **not robustly non-null either**: completion/equity metrics
  are NULL or MIXED at every elasticity (only `completion_lower` under bar gates is MIXED, with
  means −0.20…−0.69 pp and consistent negative sign but not material at every elasticity). The one
  robust sequencing difference is the mechanically exposed `formal_share_gdp` (early jobs →
  cumulative vacancy exposure), which is exactly the exposure artifact X1 removes.
- The **both-early vs neither** contrast is robust to the feedback assumption on 10–13/13 metrics
  (e.g. bar gates: formal share +17.3…+17.6 pp, `q_pub` +17.5…+20.2 pp, lower completion
  +5.4…+5.6 pp, tutoring −2.8…−3.3 pp; quota gates: tertiary −1.6…−2.5 pp, tutoring +2.6…+4.2 pp).
  This is a dose/level contrast in a toy model, not a historical statement.
- **Conclusion:** the education-to-jobs feedback assumption changes magnitudes (e.g. bar-gate
  `q_pub` effect decays 20.2→17.5 pp as elasticity rises) but does not create, erase or reverse any
  sequencing conclusion. No point on the surface is selected as "the" answer.

---

## 4. Wall times, cost, and server state

| run | runs | script elapsed | wall (launch→output) | workers |
|---|---|---|---|---|
| X1 run 1 (invalid) | 720 | 73.825 s | 13:01:10 → ~13:02:30Z | 20 |
| X3 | 800 | 81.283 s | 13:03:10 → ~13:04:35Z | 20 |
| X1 corrected (primary) | 720 | 72.593 s | 13:05:35 → ~13:06:55Z | 20 |

Total model compute ≈ 227.7 s across 2,240 runs (~0.102 s/run wall at 20 workers; ~2.0 CPU-s/run,
higher than the audit's staging estimate because N=400/T=70 and 20 concurrent workers with the
rest of the host busy). **The two 4,096-draw Bayesian screens completed at 13:00Z, before our
launches** (observed status: main ESS 88.7/4096, holdout GER RMSE 8.340 vs persistence 6.600;
expanded ESS 20.6/4096, RMSE 6.478 vs 6.600; expanded log retains logistic-overflow warnings).
Nothing was killed; our runs used a bounded 20-worker pool. Lead owns those screens' interpretation.

---

## 5. Caveats (binding)

1. **Synthetic/stipulated** toy worlds (`eduengine` `formal_loop`), not fitted to any country; the
   event years/values are stipulated, not observed dates or effect sizes.
2. **No causal language**: even the matched contrast identifies only a model-internal timing
   difference; matching total exposure removes the audit's confound but does not create exogenous
   variation.
3. **Rural migration is not simulated** (rural = household attribute + `rural_cost` + lower
   tutoring-firm access); no urbanisation, remittances, spatial job access or composition change.
4. **No empirical claim** about massification sequences; no comparison with observed country
   histories or with E1's 1.8 %.
5. The invalid X1 run 1 is preserved and not interpreted; the corrected run is the primary.
6. Small Monte Carlo (20 seeds); thresholds and decision rules were pre-declared and are reported
   exactly, including where the strict rule and the magnitude evidence diverge.
7. No quality/tutoring/employer data are involved; `mpl_primary` is an assumed anchor.

---

## 6. Files and hashes

- `results_x1_EXPLORATORY_corrected.json` — **`a4892cb7…`** (primary X1)
- `results_x1_EXPLORATORY.json` — **`e860b727…`** (run 1, invalid; server also keeps the byte-identical
  `results_x1_v1_INVALID_matched_arms_not_exposure_matched.json` copy; not duplicated in git)
- `results_x3_EXPLORATORY.json` — **`2a4a8c1c…`**
- `audit_tables/summary_x1.json`, `audit_tables/summary_x3.json` (pre-declared analysis)
- `run_x1_x3.py` (corrected, `0253dcc4…`), `analyze_x1_x3.py`, `x1.log`, `x1_corrected.log`,
  `x3.log`, `run_meta.txt`, `PRE_REGISTRATION_masseng_staging_x1_x3.md`
- Commits: prereg `e3a3975`; driver `4ae0317`; fix+deviation `cf76bca`; results/report (this
  commit) on branch `research/masseng-staging-x1-2026-11-24`, additive from `ff84e75`.
