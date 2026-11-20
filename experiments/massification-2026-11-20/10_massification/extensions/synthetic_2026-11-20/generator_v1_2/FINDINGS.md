# FINDINGS — SYNTHETIC generator v1.2 (demographic overflow, quality collapse, child-labour block)

**`LABEL: SYNTHETIC.`** Every number in this file was produced by a declared-assumption simulator. None
of it is evidence about the world, none of it is an estimate or a forecast, and none of it licenses a
causal or direction claim. No real country is modelled. The only observed series that enter numerically
are the declared PHL demographic paths (cohort and population); the observed PHL capacity/PTR/spending
series are read as a **benchmark only** and set no parameter.

Files: [`code/sim_v1_2.py`](code/sim_v1_2.py) · [`PARAMS.md`](PARAMS.md) · [`TUNE_LOG.md`](TUNE_LOG.md) ·
[`results/`](results/) · [`RUN_MANIFEST.json`](RUN_MANIFEST.json)

---

**In plain English.** I built a synthetic world of 30 fake countries running 1970–2025. A baby boom moves
through the school-age population — for the PHL-like synthetic country the boom is the **observed** PHL
cohort path, used as a declared input. Schools and teachers are built with lags from that cohort; when the
cohort runs ahead of the buildings, congestion rises and quality `Q = exp(−γ·max(0, q−1))` falls; quality
feeds survival, dropout and learning, not just intake. Families choose among four states — school, school
plus work, work, neither — using the utility structure borrowed from the Atlas `childworld` model; if
qualified demand exceeds seats, official-age children are admitted first, then over-age, and the rest are
out of school and **default to work** ("neither" is a bounded, separately reported category, not a sink).
Schooling flow also feeds economic complexity `X` with a 10-year lag, and `X` opens job rungs, so the loop
is two-way.

In that world, all five predeclared checks pass. The PHL-like country puts **primary completion past 90 %
in 2019**, **lower-secondary in 2025** (2023 is still 79.0), and **upper-secondary at 76.6 % in 2024 and
never past 90 %**; tertiary GER is 50.2 % in 2025. Primary out-of-school is 8.7 % over 2005–2015; the pupil
–teacher ratio peaks at 40.9 in 1996 and falls to 32.7 by 2024; no completion exceeds GER in the cohort
flow; and lagged primary completion raises `X` with a positive, highly significant two-way FE coefficient.
**Two things must be read before those passes:**

1. **Check (a) is scored on the UIS-convention completion series** (`m × cohort-flow`, one declared
   constant `m = 1.10`), because the on-disk PHL targets are UIS completion rates. The identity-bound
   **cohort-flow** series reaches 90 only in **2024** for primary and **never** for lower-secondary. The
   pass is therefore conditional on `m`: at `m = 1.05` primary first crosses in 2022 (FAIL); at `m = 1.12`
   upper-secondary 2024 is 78.0 (FAIL). The declared `m = 1.10` sits inside the observed PHL
   completion/GER range (0.90–1.14) but the admissible window is narrow. This is the single most important
   caveat in the file.
2. **The upper-secondary ceiling is not produced by the demographic boom.** With a flat cohort the
   PHL-like country's upper-secondary 2024 is 73.2 and still never crosses 90; the boom is load-bearing
   for the *timing* of the floor/middle and for the PTR peak, not for the ceiling. The ceiling is produced
   by the declared household work incentive at ages 15–17 plus the quality response. The asymmetry is
   therefore a **mechanism-plus-parameterisation** result, not a pure demography result.

---

## 1. Check results (frozen A–E table)

| check | verdict | headline numbers |
|---|---|---|
| **A** PHL asymmetry from the mechanism, no per-level anchors | **PASS** | UIS completion: primary first ≥90 **2019**; lower first ≥90 **2025** (2023 = **79.04**); upper max ≤2024 = **76.64**, 2024 = **76.64**, never ≥90; tertiary GER 2025 = **50.23**. Supply-rule code audit: 3 functions, **0** country branches, **0** per-level year-indexed anchor arrays, **0** forbidden tokens. |
| **B** OOS / child labour plausible and cohort-responsive | **PASS** | PHL primary OOS 2005–2015 mean **8.72 %**; worst country-year work share of OOS **0.918** (child-labour share of OOS minimum **0.599**); mean OOS 1990–2015 boom **27.10** vs flat **21.11** vs decline **17.26** pp (boom − max = **+5.99 pp**). |
| **C** PTR peaks in the boom then falls | **PASS** | PHL primary PTR peak **40.93 in 1996**; 2024 = **32.66**; peak/2024 = **1.253**; 2024 < peak. Observed benchmark (not encoded): 33.7 (1995) → 29.1 (2017). |
| **D** completion ≤ GER identity | **PASS** | cohort-flow completion ≤ GER × (1+1e−9): **0 violations** in 6 720 rows (worst margin −2.19e−02). `m = 1.10` is one declared constant; both series written out. |
| **E** education → complexity | **PASS** | two-way FE (country + year), X on primary completion flow lag 10: **b = +0.828** (se 0.055, **p < 1e−4**, n = 1 380); 5-year-block FE: **b = +0.744** (p = 1.7e−08, n = 300). Same sign. |

Component-level detail is in `results/reproduction_checks_detail_v1_2.csv`.

### 1.1 Check (a) sub-conditions

| sub-condition | required | model |
|---|---|---|
| A1 primary UIS first ≥90 | 2014–2020 | **2019** |
| A2 lower UIS first ≥90 | 2021–2027, and 2023 < 90 | **2025**, 2023 = **79.04** |
| A3 upper UIS never ≥90 by 2024; 2024 in [73, 77] | max < 90, 2024 ∈ [73, 77] | max **76.64**, 2024 **76.64** |
| A4 tertiary GER 2025 | [48.1, 54.1] | **50.23** |
| A5 one supply rule, no country/per-level override | code inspection | **PASS** |

The cohort-flow series, for transparency: primary first ≥90 in **2024**, lower **never** by 2025, upper
never. If a reader insists that check (a) be scored on the identity-bound cohort-flow series rather than
the UIS series, **check (a) fails**. That is stated here rather than hidden; see §4.

### 1.2 Measurement-factor sensitivity (why the check (a) PASS is conditional)

Using the frozen run's cohort-flow series and varying only the declared constant `m`:

| m | primary first ≥90 | lower first ≥90 | upper 2024 |
|---|---|---|---|
| 1.00 | 2024 (FAIL) | never (FAIL) | 69.67 (FAIL < 73) |
| 1.03 | 2023 (FAIL) | never (FAIL) | 71.76 (FAIL < 73) |
| 1.05 | 2022 (FAIL) | never (FAIL) | 73.16 |
| 1.08 | 2021 (FAIL) | 2025 | 75.25 |
| **1.10** | **2019 (PASS)** | **2025** | **76.64 (PASS)** |
| 1.12 | 2018 | 2025 | 78.03 (FAIL > 77) |
| 1.15 | 2016 | 2025 | 80.12 (FAIL > 77) |

Only `m ≈ 1.09–1.11` satisfies A1 and A3 simultaneously. **Correction (Council brief 021 N4 / D110):** the earlier
text listed "1.136 (upper 2018)" among the observed ratios — that is **not a same-year observed ratio** (upper completion
is not observed in 2018; 1.136 = 75.025 upper completion 2024 ÷ 66.046 upper GER 2018, the same cross-year class as the
WT5 error). The admissible same-year completion/GER ratios are 0.925 (primary 2017), 0.901 (lower 2017), 1.094
(upper 2017) and 1.045 (primary 2024) — i.e. the UIS convention is **not a stable constant** in the observed data, and
`completion/GER` is not the quantity `m` converts (m is a declared translation from the cohort-flow series to the UIS
convention). **`m = 1.10` is therefore a declared CONVENTION, not an estimated constant**, and it is doing real work:
this is a **knife-edge** pass, stated as such.

---

## 2. What the mechanism is doing (diagnostics, not scored checks)

These ablations were run in the design phase by changing one declared object in memory; they are reported
so a reader can see which layer carries which result. They are **not** part of the frozen check set and
do not change the scored run.

| scenario | primary first ≥90 (UIS) | lower first ≥90 | upper max ≤2024 | PTR peak |
|---|---|---|---|---|
| **baseline** (observed PHL cohort) | **2019** | **2025** | **76.64** | **40.93** |
| flat cohort (no boom; 1970 level) | 2014 | never | 73.17 | 34.08 |
| `γ = 0` (no quality response to congestion) | 1976 | 2024 | 80.74 | 40.93 |
| `surv_theta = 0` (quality not fed to completion) | 1976 | 2024 | 80.74 | 40.93 |

Reading:

- **The quality channel is the main driver of the primary crossing date.** With `γ = 0` primary crosses
  90 in 1976 instead of 2019: congestion-driven quality collapse is what delays universal primary
  completion by four decades in this parameterisation. That is the user's mechanism, and it is
  load-bearing.
- **The boom drives the PTR peak and delays primary.** A flat cohort gives a PTR peak of 34.1 (not
  40.9) and an earlier primary crossing (2014). The demographic surge is what makes the teacher stock lag
  and the ratio peak.
- **The boom is *not* what creates the upper-secondary ceiling.** With a flat cohort upper-secondary
  2024 is 73.2 and still never crosses 90; with `γ = 0` it is 80.7 and still does not cross. The ceiling
  comes from the household work incentive at 15–17 (upper demand ≈ 0.80) plus quality. **If the reader's
  question is "does a baby boom produce a completion ceiling?", this parameterisation answers: not by
  itself — it produces the floor/middle timing and the congestion, and the ceiling needs the
  child-work/quality block.**
- **The post-2015 cohort decline is load-bearing for the lower-secondary crossing.** With a flat cohort
  lower-secondary never reaches 90 by 2025; the crossing depends on coverage/quality improving as the
  cohort falls after 2015.

---

## 3. What passed, what is fragile

**Passed as predeclared:** A, B, C, D, E. No check was rescued by changing a parameter after the freeze.

**Fragile, in order of how easily a reader could overturn the pass:**

1. **`m = 1.10` and check (a).** The admissible window is `m ≈ 1.09–1.11`. The declared convention is
   defensible but it is the pivot of the headline pass. A reader who prefers `m = 1.05` should record
   check (a) as **FAIL (primary 2022; lower never)**.
2. **The lower-secondary crossing year.** 2025 with 2023 = 79.04. The build-out width is 5 years and the
   centre 2024, so the crossing is intentionally sharp; a small change in the declared width moves the
   first-crossing year by 1–3 years. The ±3 window gives slack, but this is a calibrated date, not a robust
   prediction.
3. **The upper band [73, 77].** 2024 = 76.64 is inside but near the top; `m = 1.12` or a slightly higher
   survival maximum pushes it out. The series is still rising after 2024 (not scored).
4. **The PTR level.** The model's peak (40.9) is ~20 % above the observed PHL benchmark (33.7 in 1995);
   the check only tests the **shape** (peak in 1990–2010, ≥10 % above 2024). The level is not calibrated
   and should not be compared to the observed series as a level.
5. **Check (e).** Strong in this parameterisation (b = 0.83, p < 1e−4), but the channel is declared, and
   the regression is a within-country association in a synthetic panel — it is not a causal test and says
   nothing about the real education → complexity relation.

---

## 4. Load-bearing assumptions (ranked)

1. **The measurement convention `m = 1.10`.** It is the gateway to check (a). It is one declared constant,
   applied to every level and country; there is no per-level factor. But it is a convention, not an
   estimate, and the observed PHL ratios are not constant (§1.2).
2. **The household work incentive at ages 15–17** (declared `v0`, `decay`, `w_child`, `compat`, `cost`,
   `neither`). Upper-secondary demand is ≈0.80 of the cohort; that, plus quality, is what holds the
   ceiling at ~77. If `v0`/`decay` were higher or the child wage lower, the ceiling would move. The ceiling
   is *not* a stipulated per-level seat cap of the v1 kind — the declared upper coverage **target** rises to
   1.0 (actual ≈0.89 by 2025) and admission is demand-bound — but it is still a declared behavioural
   parameterisation.
3. **The declared capacity build-out timing** (`seat_t50`, `cover_hi`, `seat_width`). These set the
   crossing years and were calibrated during design (disclosed in `TUNE_LOG.md`). They are level-specific
   structural constants of **one rule**, identical for all 30 countries, with no observed anchor
   interpolation and no PHL-specific override.
4. **The teacher hiring lag and delivery build-out.** These produce the PTR peak in 1996; without the lag
   the ratio would not have the hump.
5. **The education → X channel** (`x_edu_level = 0.40`, lag 10). Strong and stable in the panel; it is a
   declared elasticity, not an estimate.

---

## 5. Honest caveats

- **This is not a test of the mechanism.** The declared parameters were calibrated in the design phase so
  that the single mechanism can produce the frozen pattern. A PASS means "this parameterisation can
  produce the pattern through the declared mechanism", not "the mechanism is the true one" and not "the
  Philippines did it this way". The design log is in `TUNE_LOG.md`; the distinction from v1 is that there
  is no per-level anchor interpolation and no PHL-specific supply override, not that the parameters are
  innocent of the targets.
- **The child-labour block is an aggregate representative household**, not a micro-simulation. There is no
  age-by-gender-by-household heterogeneity beyond the half-girl weighting in the "neither" utility. The
  child-labour definition is the childworld/camchild definition — **not** the ILO statistical definition.
- **The observed PHL cohort path starts in 1995.** 1970–1994 and 2025 are declared extrapolations. The
  "boom" shape in the model's early decades is therefore partly an extrapolation.
- **The model's primary UIS completion reaches 100 % by 2024** (observed 98.3 %) — a ceiling artifact of
  `m × cohort-flow` clipping. It is not used as a check.
- **Over-age admission.** GER can exceed 100 through over-age entrants while official-age OOS remains
  positive; that is deliberate (it is the observed PHL configuration), but a reader should not read GER as
  "share of children in school".
- **No real country.** `SYN00_PHL_LIKE` is a declared parameterisation intended to resemble a published
  signature, not the Philippines.
- **No policy, causal or direction claim.** Nothing here says anything about what a government should do.

---

## 6. The 3–5 most decision-relevant numbers

1. **Upper-secondary 2024 UIS completion = 76.64 %, and the series never reaches 90 % by 2024** (max
   76.64). The ceiling is produced by the child-work/quality block, not by the boom (flat-cohort ablation:
   73.2 %, still never 90).
2. **Primary first ≥90 = 2019; lower-secondary = 2025** (2023 = 79.04) — both inside the frozen ±3
   windows, but only with the UIS convention `m = 1.10`. At `m = 1.05` primary is 2022 and **check (a)
   fails**.
3. **PTR peak = 40.93 in 1996, 2024 = 32.66 (+25.3 %)**; the boom, not the quality function, creates the
   hump (flat-cohort peak 34.1).
4. **Boom − flat out-of-school = +5.99 pp** over 1990–2015 (27.10 vs 21.11 vs decline 17.26), and PHL
   primary OOS = 8.72 % over 2005–2015. The out-of-school block is cohort-responsive.
5. **Education → complexity: b = +0.828 (p < 1e−4), 5-year block b = +0.744 (p = 1.7e−8).** The declared
   channel is present and identifiable; it is not a causal estimate.

---

## 7. Reproduction

- One NumPy `PCG64` stream, seed `20261120`; no wall-clock or OS entropy in any output; floats `%.10g`.
- Two clean runs into separate directories produced **byte-identical** `synthetic_panel_v1_2.csv`,
  `reproduction_checks_v1_2.csv`, `reproduction_checks_detail_v1_2.csv` and `RUN_MANIFEST.json`
  (`cmp` evidence in `results/determinism_note.md`).
- The script refuses to run if `v1_2/PRE_DECLARATIONS.md`'s sha256 changes; the frozen hash is
  `fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16`.
- `RUN_MANIFEST.json` records the sha256 of the predeclaration, code, `PARAMS.md`, the five input data
  files, the three results files, the seed, the parameter block, the borrow ledger and the check summary.

---

## 8. What I could not implement / did not do

- **Check (a) on the cohort-flow series.** The cohort-flow series does not reach the 2017/2024 targets;
  only the UIS-convention series does. I report both and score on UIS, with the sensitivity table in
  §1.2. I did **not** add a per-level factor to make the cohort series hit the targets.
- **A fertility model.** The cohort path is a declared input, as the frozen spec requires; there is no
  endogenous demographic response.
- **Micro household heterogeneity / ILO child labour.** The block is aggregate and the child-labour
  definition is declared, not ILO.
- **A derived upper-secondary ceiling.** The ceiling is demand/quality-driven in this parameterisation,
  but the demand parameters are declared, not derived from who hires upper-secondary completers. That
  remains the v1 critique and is not resolved here.
- **No edits outside `generator_v1_2/`.** The predeclaration, the v1 files, the data files and the rest of
  the repository are untouched (read-only).
