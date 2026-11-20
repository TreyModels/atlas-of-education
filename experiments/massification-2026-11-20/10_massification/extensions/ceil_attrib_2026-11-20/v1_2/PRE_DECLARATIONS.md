# PRE-DECLARATIONS — SYNTHETIC generator v1.2 (demographic overflow, quality collapse, child-labour block)

**FROZEN BEFORE THE RUN.** Written 2026-11-20 (Asia/Shanghai) from the user's directive relayed via the dashboard
(recorded as `MODEL_ARCHITECTURE.md` **Amendment A2**). No v1.2 result exists at the time of writing; the code
(`code/sim_v1_2.py`) and the parameter file (`PARAMS.md`) must be created and frozen **before** the first scored run,
and their sha256 recorded in `RUN_MANIFEST.json`. This file is not changed after results are seen. If the frozen
hashes do not match at run time the script must refuse to run.

**LABEL: SYNTHETIC. Everything a v1.2 run emits is a declared-assumption simulation — not evidence, not an estimate,
not a forecast, and not a model of any real country. No causal or direction claim.**

---

## 1. What is new relative to v1, and why

v1 reproduced the Philippine floor/middle/ceiling asymmetry **substantially by stipulating per-level PHL supply paths
interpolated through the declared completion anchors** — its own check A is labelled "PASS but target-encoded", and its
`TUNE_LOG.md` states that "one parameterisation, no per-level rescue" was **not** met, with the stipulated
upper-secondary seat cap (0.845→0.875) the load-bearing object. It also had **no demographic/quality layer at all**,
and its literacy association was **non-diagnostic** (survived both ablations).

The user's reading supplies the missing mechanism: **a baby boom moved through the school-age population; schools and
teachers were not built fast enough; seats overflowed and quality collapsed (congestion, PTR, double shifts); families
compete for places; and a child not in school is, by default, in child labour/work.**

v1.2 must therefore produce the ceiling **through the mechanism** (cohort surge + lagged capacity + quality collapse +
rationing), not through per-level anchors, and must carry a four-state household block.

## 2. Borrowed material (structure only — never values)

| element | source (read-only retrieval) | sha256 | status |
|---|---|---|---|
| four-state block `school` / `both` / `work` / `neither` + household utility decision + parameter names | `engine/childworld.py` at parent-repo HEAD (`git -C /Users/treymenefee/massification_live show HEAD:engine/childworld.py`) | `ae73adb2a6d9c75d59966390e4304437479ff310a8724093e9108e9d26a23cab` | **BORROWED-FROM-ATLAS / structural** |
| MC/age-aligned/Sobol wrappers | `engine/childworld_mc.py` (`944d1040…`), `childworld_agealigned.py`, `childworld_sobol.py` | see `MODEL_INVENTORY.md` rows #6–#7 | pattern only |

**Caveats that travel with the borrow (from the programme's review; do not paper over):** childworld was
"**Not run** in this audit (only inspected)"; its observation equation **is not the ILO child-labour definition**; its
values are **stylised**; `childworld_mc` **v1 failed the India composition test**; its baseline **"neither" share 0.421
was flagged for validation**. Hence: **no childworld prior, posterior, country target or output number enters v1.2 as a
parameter.** Only the four-state structure, the decision-variable list and the utility form are borrowed, and every
instance is labelled `BORROWED-FROM-ATLAS / structural` in `PARAMS.md` and in the code header.

**Declared deviations from childworld:**
1. **No free "neither" sink** (user directive): out-of-school children **default to work/child labour**. "Neither" is
   a bounded declared option (domestic care / marriage / disability / inaccessible school) whose share is reported; it
   may not absorb a residual.
2. **Rationing** (families compete for seats) is added: childworld is demand-only; v1.2 has a supply cap per level.
3. **Child-labour definition:** declared as "any market work under 15; work at 15–17 in a declared hazardous share; and
   school-plus-work under 12" — the childworld/camchild definition, explicitly **not** claimed to be the ILO statistical
   definition. Reported as a separate series from model "work".
4. **Time structure:** one-year cohort ageing (v1 convention), cohort inflow from the **observed declared path** (§3),
   not from a fertility model.

## 3. Declared inputs (observed; never fitted at runtime)

| input | file | use |
|---|---|---|
| PHL cohort / population path | `10_massification/data/UNIVERSALIZATION_SERIES.csv` (`cohort_population_0_14`, `population_total`, PHL) | **declared** annual school-age cohort path; the baby-boom shape enters here |
| PHL school expansion / teachers / PTR | `10_massification/data/SCHOOL_EXPANSION.csv` | declared capacity and PTR paths (lag structure) |
| PHL state capacity / delivery | `10_massification/data/STATE_CAPACITY.csv` | declared delivery multiplier for seat/teacher build |
| completion / GER targets for checks | `10_massification/data/UNIVERSALIZATION_SERIES.csv`, `data/gmr_observed_6countries_1970_2024.csv` | **scored against**, never encoded per level |

Synthetic countries (declared): `SYN00_PHL_LIKE` (boom path, narrow office sector), `SYN01_TWIN_MFG` /
`SYN02_TWIN_OFFICE` (twins, identical except sector mix), `SYN10_BOOM` / `SYN11_FLAT` / `SYN12_DECLINE` (declared cohort
paths — boom / flat / decline, otherwise identical) so the mechanism can be seen to matter. 30 synthetic countries
overall, 1970–2025, 4 levels, as v1.

## 4. Declared model changes

- **Layer 1b (demographics).** Cohort size at each level and year is a **declared input path** (no fitting, no
  fertility model). The boom is a property of the input, not of the model.
- **Layer 1c (capacity → congestion → quality).** Seats and teachers per level are built with a declared lag
  (capacity response coefficient and lag declared in `PARAMS.md`). Congestion
  `q_{L,t} = cohort_{L,t} / seats_{L,t}`; class size and PTR are declared functions of `q`; **quality index**
  `Q_{L,t} = exp(−γ·max(0, q_{L,t} − 1))` with declared `γ ≥ 0`. **Quality feeds completion, dropout and learning, not
  just intake** (declared functional form in `PARAMS.md`; no rescaling to hit check A).
- **Layer 2b (household four-state block + rationing).** For each child, the borrowed utility comparison over
  `{school, both, work, neither}` using declared `y_med, w_child, farm, compat, v0, decay, cost, neither, girl_care, haz`
  values. Qualified demand exceeding seats is **rationed by a declared rule: official-age children are admitted first,
  then over-age, until seats fill; the remainder are out of school and default to work.** Rationing uses the seeded
  RNG only for ties, declared.
- **Layer 3 (growth and complexity).** v1's growth/composition logic is retained; the Amendment-A1
  **education → complexity** channel is added: `X_t = f(X_{t−1}, Δschooling_flow_{t−lag})` with a declared elasticity
  and lag 5–10 years, so schooling flow raises `X` (and `X` continues to open rungs). Parameters declared, not fitted.

## 5. Checks (frozen; scored in `results/reproduction_checks_v1_2.csv`)

**(a) PHL ceiling/asymmetry from the mechanism, with NO per-level anchor interpolation.** PASS iff all of:
primary completion first ≥90 within **±3 years of 2017**; lower-secondary first ≥90 within **±3 years of 2024**
(and < 90 in 2023); upper-secondary **never** ≥90 by 2024 with 2024 completion in **[73.0, 77.0]**; tertiary GER 2025 in
**[48.1, 54.1]**; **and** code inspection confirms **one declared supply rule applied to every country and level**
(no PHL-specific override variables, no per-level anchor arrays). PASS is void if any override exists.

**(b) Out-of-school / child-labour shares plausible and cohort-responsive.** PASS iff: PHL-like model out-of-school
rate (primary) in 2005–2015 lies in **[5 %, 20 %]**; the share of out-of-school children in work/child labour is
**≥ 0.50 in every country-year** (the user's default: not in school ⇒ work); and the declared-path comparison shows
**boom countries have higher mean out-of-school rates than flat/decline countries by ≥ 2 pp** over 1990–2015.

**(c) Congestion rises during the boom then falls.** PASS iff the PHL-like pupil–teacher ratio **peaks in 1990–2010**
at least **10 % above** its 2024 value and **2024 < peak** (shape test; exact series from the model, compared with the
on-disk PHL PTR path only as a declared benchmark, not encoded).

**(d) Accounting identity, with the disclosed measurement issue.** In cohort-flow accounting, model
**completion ≤ GER × (1 + 1e-9)** in every country-year-level (a completion > GER result is a code bug, not a
finding). If the model also reports a UIS-convention completion (`× declared measurement factor m`), then `m` is a
**single declared constant** (not per level/country) and both series are written out. PASS iff the identity holds and
no undeclared factor exists.

**(e) Education → complexity channel present.** PASS iff, in the synthetic panel, the two-way FE coefficient of
**lagged primary-completion flow on `X`** is **positive with p < 0.05** at the declared lag (5 or 10 years), and the
same sign holds in the 5-year-block spec.

**Verdict rule:** checks are PASS/FAIL as above; a FAIL is reported, not rescued. **No parameter may be changed after
this file is frozen to flip a check.** A v1.2 that cannot pass (a) without anchors must report that the asymmetry
requires the stipulated capacity path — which is a finding about the generator, not about the world.

## 6. Output contract and determinism

`code/sim_v1_2.py` (new), `PARAMS.md` (all declared values, frozen before run, sha256 in the manifest),
`results/synthetic_panel_v1_2.csv` (one row per country-year-level; `label = SYNTHETIC`), `results/
reproduction_checks_v1_2.csv` (checks a–e with component numbers), `results/reproduction_checks_detail_v1_2.csv`,
`RUN_MANIFEST.json` (hashes of this predeclaration, code, PARAMS, data inputs, results; seed; check summary),
`FINDINGS.md` (written after the run, including FAILs). Determinism: one NumPy `PCG64` stream, seed **20261120**, no
wall-clock/OS entropy, floats at `%.10g`; **two clean runs must be byte-identical**.

## 7. What a v1.2 result cannot claim

No evidence about the Philippines or any country; no causal claim; no direction claim; no policy claim. The boom
path, the capacity lag, the quality function and the household utilities are **declared assumptions**. A PASS on
check (a) means "this parameterisation can produce the pattern through the declared mechanism", not "the Philippines
produced it this way". The borrowed childworld elements are **structural only** and carry the caveats in §2.
