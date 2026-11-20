# FINDINGS — EXP-1 CEIL-ATTRIB: which account carries the PHL upper-secondary ceiling?

**`LABEL: SYNTHETIC` for every generator number; `OBSERVED` for the PHL UIS completion series.**
EXP-1 of Council brief 021 (D112 #1), SYNTHESIS_021 §4. Worker CA, 2026-11-20.
Predeclaration: [`PRE_DECLARATIONS.md`](PRE_DECLARATIONS.md) — sha256
`ed9b31b9cfa24ffa3a2285cb769ad9ecae899e392f77ac648e3c55b7dbfef64f`, **hashed and recorded
before any run**. No threshold, bar, lag rule or verdict rule was changed after results.

Files: [`code/run_ceil_attrib.py`](code/run_ceil_attrib.py) ·
[`results/CEIL_ATTRIB_RESULTS.csv`](results/CEIL_ATTRIB_RESULTS.csv) ·
[`results/CEIL_ATTRIB_DETAIL.csv`](results/CEIL_ATTRIB_DETAIL.csv) ·
[`results/ABLATION_PANEL.csv`](results/ABLATION_PANEL.csv) ·
[`RUN_MANIFEST.json`](RUN_MANIFEST.json)

---

**In plain English.** The observed Philippine upper-secondary completion rate tracks the
lower-secondary completion rate **three years earlier** (ratio 0.889–1.072, mostly ≈0.93–0.97).
In 7 of the 8 usable observed pairs the ratio `upper_t / lower_{t−3}` lies in the predeclared
band [0.90, 1.10], so **Test B is `PIPELINE-CONSISTENT`**: the observed "upper ceiling" is
consistent with being inherited from the lower-secondary pipeline one stage earlier, rather than
being an independent upper gate. That **reclassifies** D63's object from "upper gate" to "lower
pipeline"; D63 stays **UNABLE as to cause**.

The synthetic generator tells a less clean story. Under the frozen Test A bars, all three
mechanism ablations move synthetic upper UIS 2024 by ≥ 2.0 pp (γ = 0 **+2.64 pp**, work
incentive off **+6.27 pp**, flat cohort **−3.47 pp**), **but** the calibration knobs also move it
by ≥ 2.0 pp (`m = 1.05` **−3.48 pp**, build-out −5 y **+2.08 pp**, build-out +5 y **−7.56 pp**).
The mechanism-carried clause requires every calibration move to be < 1.0 pp, and the
calibration-carried clause requires every mechanism move to be < 2.0 pp; **neither holds.
Test A is `MIXED`.** v1.2's claim that the ceiling is *produced by the mechanism* is therefore
**not licensed** by this experiment — but the ceiling is also **not** declared a calibration
artefact. Under the declared ordered matrix rule, Test B reaches its bar, so the overall
CEIL-ATTRIB decision is **`PIPELINE-CONSISTENT`** for the observed residual, with Test A
recorded as `MIXED` on the synthetic side.

---

## 1. What was run

1. **Predeclaration first.** `PRE_DECLARATIONS.md` contains the SYNTHESIS_021 §4 EXP-1 three-account
   matrix and both tests **verbatim**, the operational definition of every ablation, the lag/pair
   rule, the verdict vocabulary and a no-threshold-change statement. It was written and hashed
   (sha256 above) before the code ran.
2. **Baseline invariance.** An **unmodified byte-identical copy** of
   `generator_v1_2/code/sim_v1_2.py` (sha `61123aa9…55e7c`) plus a byte-identical copy of the
   frozen v1.2 spec (sha `fde18d40…5f16`, so the code's own hash guard passes) and `PARAMS.md`
   was run inside this experiment directory. It reproduced
   `results/synthetic_panel_v1_2.csv` **byte-for-byte** (sha
   `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac`, `cmp` and sha256
   identical; rows 6 720). The variant driver with no switch also reproduced the same panel
   bytes, so every ablation difference is the switch, not the driver.
3. **Test A** then measured `SYN00_PHL_LIKE` upper **UIS-convention** completion in 2024 under
   each declared in-memory switch. **Test B** computed the observed PHL ratio at the declared
   3-year lag with the declared ±1 y-nearest-observation pair rule.

Ablations were **declared variants on the unmodified copy**, applied to all 30 countries with the
same seed and the same shock realisations. The frozen `generator_v1_2/` was never written to; the
scored run is unchanged; nothing was re-fitted.

---

## 2. Test A — synthetic ablation (`SYNTHETIC`)

`synthetic upper UIS 2024` = `m × cohort-flow completion`, percent. Baseline = 76.639 pp.
Δ is the absolute deviation from baseline, in percentage points.

| variant | mechanism / calibration | upper UIS 2024 | Δ (pp) | bar | contributes |
|---|---|---:|---:|---|---|
| baseline | reference | 76.639 | 0.000 | — | — |
| γ = 0 | mechanism | 79.276 | **+2.637** | ≥ 2.0 | **hit** |
| household work incentive off | mechanism | 82.909 | **+6.270** | ≥ 2.0 | **hit** |
| flat cohort (1970 level) | mechanism | 73.168 | **−3.471** | ≥ 2.0 | **hit** |
| m = 1.05 | calibration | 73.155 | **−3.484** | < 1.0 or ≥ 2.0 | **calibration move ≥ 2.0** |
| m = 1.10 | calibration (reference) | 76.639 | 0.000 | — | reference |
| m = 1.12 | calibration | 78.033 | +1.393 | < 1.0 or ≥ 2.0 | between bars |
| build-out −5 y (all levels) | calibration | 78.719 | **+2.080** | < 1.0 or ≥ 2.0 | **calibration move ≥ 2.0** |
| build-out +5 y (all levels) | calibration | 69.078 | **−7.562** | < 1.0 or ≥ 2.0 | **calibration move ≥ 2.0** |
| build-out −5 y (upper only) | sensitivity | 78.719 | +2.080 | — | not verdict-bearing |
| build-out +5 y (upper only) | sensitivity | 73.720 | −2.919 | — | not verdict-bearing |

**Frozen Test A rule applied.**
- Mechanism ablations at/over 2.0 pp: **3 of 3** (bar: ≥ 2) → mechanism clause satisfied.
- Calibration moves: max |Δ| = **7.562 pp** (bar for calibration-carried: ≥ 2.0) → calibration
  clause satisfied.
- But `mechanism-carried` also requires **every** calibration move **< 1.0 pp**, which is false
  (three of four calibration variants move ≥ 2.0 pp).
- And `calibration-carried` requires **every** mechanism ablation **< 2.0 pp**, which is also false
  (all three are ≥ 2.0 pp).

**Test A verdict: `MIXED`.** Neither exclusive account is carried by the frozen bars. This is a
legitimate, declared outcome — not a failure of the run, and not something to re-tune.

**Reading.** The synthetic 2024 upper level is **jointly** mechanism- and calibration-sensitive.
The mechanism clearly does work in this parameterisation (the work incentive alone is worth
+6.27 pp; γ = 0 +2.64 pp; the boom −3.47 pp), but the level is not *uniquely* attributable to it:
the measurement convention `m = 1.05` and build-out timing shifts move it by more than the
mechanism bar's calibration tolerance. The `MIXED` verdict is robust to the build-out-level
ambiguity (the upper-only ±5 y shift is +2.08/−2.92 pp, still ≥ 2.0) and to reading the m sweep as
a range rather than as deviations (the m = 1.05→1.12 range is 4.88 pp). **No rescue was applied.**

**Implementation cross-check against the frozen design-phase diagnostics** (v1.2 `FINDINGS.md` §2).
The declared switches reproduce the frozen diagnostic table: flat cohort gives upper 2024 =
**73.17** (frozen 73.17); γ = 0 gives upper **max ≤ 2024 = 80.74** (frozen 80.74; its 2024 value is
79.28 — the frozen table's column is the max, Test A's statistic is the 2024 value); and the m
sweep gives **73.16 / 76.64 / 78.03** (frozen 73.16 / 76.64 / 78.03). This confirms the ablations
are the declared variants, not approximations.

**Design-phase context (why this is not surprising).** `TUNE_LOG.md` D3 discloses that the
upper-secondary build-out centre was moved from 2014 to 2010 (with `cover_hi` 0.95→1.00 and
`surv_max` 0.96→0.90) in the design phase specifically to bring upper UIS 2024 into [73, 77].
Test A's build-out sensitivity (+2.08 / −7.56 pp) is consistent with that disclosure. The synthetic
2024 level is therefore a **calibrated placement as well as a mechanism output**, which is exactly
what the frozen Test A bars detect as `MIXED`. This is reported as context, not as a new test.

**Descriptive (post-hoc, not verdict-bearing).** In **every** declared variant the upper series
still never reaches 90 by 2024 (max ≤ 82.91 pp under work-off; baseline max 76.64). The
*existence* of a sub-90 ceiling is robust across the declared ablations; it is the *level* that is
not uniquely attributable. That observation did not enter the verdict.

---

## 3. Test B — observed PHL pipeline ratio (`OBSERVED`)

Declared lag = **3 years**; for each observed upper year use the lower value at exactly `t−3`, else
the nearest observed lower year within ±1 y, else drop the pair. Ratio = `upper_t / lower_{t−3}`
(percent ÷ percent).

| upper year | upper completion | lower year used | lower completion | ratio | in [0.90, 1.10]? |
|---:|---:|---:|---:|---:|---|
| 2003 | 61.729 | 2000 | 65.027 | 0.949 | **in** |
| 2004 | 60.362 | 2000 | 65.027 | 0.928 | **in** |
| 2008 | 64.090 | 2004 | 66.084 | 0.970 | **in** |
| 2010 | 66.123 | 2008 | 67.960 | 0.973 | **in** |
| 2013 | 67.470 | 2010 | 71.097 | 0.949 | **in** |
| 2017 | 76.433 | 2013 | 71.270 | 1.072 | **in** |
| 2023 | 71.929 | 2021 | 80.896 | **0.889** | **below 0.90** |
| 2024 | 75.025 | 2021 | 80.896 | 0.927 | **in** |

- Pairs: **n = 8** (the 2022 upper observation is dropped: its `t−3 = 2019` target has no lower
  observation within 2018–2020).
- In band: **7 / 8 = 0.875** → bar `≥ 2/3` **met**.
- Below 0.90: **1 / 8 = 0.125** → gate-loss bar `≥ 2/3` **not met**.

**Test B verdict: `PIPELINE-CONSISTENT`.**

**Sensitivity (declared, not verdict-changing).**

| lag / rule | n | in band | share | below 0.90 | verdict |
|---|---:|---:|---:|---:|---|
| **lag 3 (verdict)** | **8** | **7** | **0.875** | 1 | **`PIPELINE-CONSISTENT`** |
| lag 2 | 7 | 4 | 0.571 | 3 | `UNDETERMINED` |
| lag 4 | 7 | 6 | 0.857 | 1 | `PIPELINE-CONSISTENT` |
| lag 3, nearest lower at any distance (no drop) | 11 | 9 | 0.818 | 2 | `PIPELINE-CONSISTENT` |

The verdict is therefore robust to the pair-dropping rule (0.818 with all 11 pairs) and to a
4-year lag (0.857), but **not** to a 2-year lag (0.571, undetermined). The 3-year lag was declared
in advance; the 2-year result is reported as sensitivity only and does not change the verdict.

**Descriptive flag (not a verdict change).** The only out-of-band pair is the most recent
non-2024 one: 2023 upper (71.93) over 2021 lower (80.90) = 0.889. The observed upper series is
non-monotonic (2017 = 76.43 → 2022 = 68.28 → 2024 = 75.03) while the lower series rises
monotonically after 2021. If the 2022 pair is forced in with the nearest lower observation it is
also below 0.90 (0.844). On the declared bar this is one pair out of eight — not gate-loss — but
it is recorded because the recent end of the series is where a future gate-loss signal would
first appear. No direction-of-causation claim is made and none is licensed.

**Lag provenance.** `SE.PRM.DURS` = 6 for PHL throughout; `SE.SEC.DURS` = 4 (1970–2016), 5 (2017),
6 (2018–2024). WDI's secondary duration measures the whole secondary stage, not the
lower-secondary stage alone; the 3-year lag is the **declared** brief value, consistent with the
lower-secondary stage length used by v1.2 (`DUR = (6, 3, 3, 4)`) and with an ISCED
lower-secondary stage of three years. The duration series is recorded as provenance, not used to
re-derive or re-optimise the lag.

---

## 4. Declared decision-matrix outcome

The three-account matrix of SYNTHESIS_021 §4 (copied verbatim in `PRE_DECLARATIONS.md`), with the
ordered rule declared in advance (§7 of the predeclaration):

| Test B | Test A | overall | matrix cell |
|---|---|---|---|
| **`PIPELINE-CONSISTENT`** | **`MIXED`** | **`PIPELINE-CONSISTENT`** | **(a)** |

**Matrix (a) outcome.** The D63 residual is **reclassified** as **lower-pipeline inheritance**.
D63 stays **UNABLE as to cause**. The object moves from "upper gate" to "lower pipeline". **No
demand/exit-cost claim** is made. The Test A `MIXED` result is recorded as a caveat on the
synthetic side: v1.2's mechanism-attribution claim is **not established** by Test A (it is neither
mechanism-carried nor calibration-carried under the frozen bars), and v1.2 is **not** re-tuned.

(The overall token follows Test B because Test B locates the *observed* residual while Test A
attributes the *synthetic* 2024 level; that precedence was fixed in `PRE_DECLARATIONS.md` §7
before the run, following matrix cell (a)'s wording, which is conditioned on Test B alone.)

---

## 5. What this does and does not license

**Licensed (and only this).**

1. **Reclassification of D63's location.** The observed PHL upper-secondary completion rate is
   consistent with being inherited from the lower-secondary pipeline three years earlier
   (7/8 pairs in [0.90, 1.10]). The "upper ceiling" is, on this diagnostic, a lower-pipeline
   phenomenon at the observed level.
2. **A recorded, legitimate `MIXED` on the synthetic side.** Under the frozen Test A bars the
   synthetic 2024 upper level is jointly mechanism- and calibration-sensitive; neither exclusive
   account is carried.
3. **A determinism and invariance result.** The frozen scored panel is reproduced byte-for-byte
   from the copy, and the whole experiment re-runs byte-identically (two runs, all result files
   `cmp`-identical).

**Not licensed — do not read the result as any of these.**

- **D63 is not "explained".** It is *reclassified* in location at most. The cause of the observed
  pattern — why the lower pipeline sits where it does — is untouched. D63 remains **UNABLE as to
  cause**.
- **No causal or direction claim.** Test B is a ratio diagnostic on 8 observed pairs; it says
  nothing about why lower completion is what it is, about demand, returns, exits or policy.
- **v1.2's ceiling claim is not rescued.** Test A is `MIXED`, so v1.2's "the mechanism produces
  the ceiling" is **not** licensed by this experiment. Equally, v1.2 is **not** declared a
  calibration artefact: `CALIBRATION-CARRIED` also fails. The honest state is "jointly sensitive,
  not uniquely attributed".
- **No re-fit.** No parameter was changed after results; the ablations are declared variants on an
  unmodified copy; the scored run is unchanged.
- **No C1–C4 reopening; WT4 is not re-scored.** This experiment does not touch the closed claims
  or the WT battery's scoring.
- **No use of the synthetic level as evidence about the Philippines.** `SYN00_PHL_LIKE` is a
  declared parameterisation, not the Philippines. The observed series is used as an observed input
  diagnostic (Test B), not to validate the generator.
- **No forecast.** The 2023 out-of-band pair is a descriptive flag, not a prediction that a
  gate-loss will appear.

A mixed or undetermined outcome would have been a legitimate finding; here Test A is mixed and
Test B is pipeline-consistent, and the overall decision is the matrix (a) reclassification, not a
new mechanism claim.

---

## 6. Determinism and reproduction

- Baseline invariance: `cmp` and sha256 identical to the frozen
  `results/synthetic_panel_v1_2.csv` (`14729c51…acf5ac`); also reproduced from the variant driver
  with no switch.
- Full run twice (`results/` and `results/determinism_run2/`): `CEIL_ATTRIB_RESULTS.csv`,
  `CEIL_ATTRIB_DETAIL.csv`, `ABLATION_PANEL.csv`, `EVIDENCE.json` and the baseline panel are all
  **byte-identical** (`cmp`).
- The driver adds no RNG; the only randomness is the frozen generator's single seeded PCG64
  stream (seed `20261120`), drawn in the frozen order, identical across variants. No wall-clock,
  OS entropy, network or external data in any output.
- All hashes are in [`RUN_MANIFEST.json`](RUN_MANIFEST.json).

---

## 7. What could not be implemented / limits

- **No causal identification.** Test B has 8 pairs and no declared uncertainty or significance
  inference; none is claimed. Test A is a synthetic ablation, non-diagnostic about the real world.
- **"Household work incentive off" is one declared operationalisation**: zero child market-work
  earnings (`w_child = farm = 0`), leaving the work state available at zero earnings. Removing the
  work state entirely, or switching off other household parameters, would be **different declared
  variants** and was not run. The chosen operationalisation is stated in full in the
  predeclaration.
- **Build-out timing level ambiguity.** The frozen text does not say which level's build-out
  timing shifts; the whole-schedule ±5 y shift is the verdict-bearing reading and the upper-only
  shift is reported as sensitivity. The Test A verdict does not depend on this choice (both move
  ≥ 2.0 pp; `m = 1.05` alone already breaks the < 1.0 pp clause).
- **The `m` sweep includes `m = 1.05`, which v1.2's own FINDINGS §1.2 places outside the
  admissible `m ≈ 1.09–1.11` window.** The frozen EXP-1 bar includes it, so it is used; this is
  precisely why Test A is `MIXED` rather than mechanism-carried. No post-hoc narrowing of the m
  sweep was applied.
- **The 3-year lag is declared, not estimated.** The WDI duration series does not directly give a
  lower-secondary stage length; the declared lag is recorded with its provenance and was not
  re-derived from the observed ratios.
- **Only the PHL series is used.** No cross-country or subnational extension; no external data; no
  web.
- **No writes outside `ceil_attrib_2026-11-20/`.** The frozen `generator_v1_2/`, the v1.2 spec, the
  data files and the rest of the repository are read-only here.

---

## 8. The 3–5 most decision-relevant numbers

1. **Test B: 7/8 observed pairs in [0.90, 1.10]; 2024 ratio 0.927; verdict `PIPELINE-CONSISTENT`.**
2. **Test A: mechanism ablations +2.64 / +6.27 / −3.47 pp (3/3 hit the ≥ 2.0 bar); calibration
   moves up to 7.56 pp; verdict `MIXED`.**
3. **Overall CEIL-ATTRIB: `PIPELINE-CONSISTENT` — D63's object moves from "upper gate" to "lower
   pipeline"; D63 stays UNABLE as to cause.**
4. **Baseline invariance: byte-identical frozen panel (`14729c51…acf5ac`); two-run determinism
   byte-identical.**
5. **The sub-90 upper ceiling survives every declared variant (max 82.91 pp under work-off), so the
   ceiling's existence is robust; its 2024 level is not uniquely attributable.**
