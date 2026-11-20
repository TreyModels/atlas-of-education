# FINDINGS — EXP-7 REPRO-PATH

**`LABEL: SYNTHETIC` for every generator number; `OBSERVED` for every PHL UIS completion number.**
Council brief 022, `SYNTHESIS_022.md` §6 EXP-7 (D122 #2, rank #2). Worker **RP**, 2026-11-20.
Predeclaration `PRE_DECLARATIONS.md` sha256 `74f9d0e0…3db12`, hashed before the first run; no threshold,
year set, cell rule, κ value, class boundary or verdict word was changed after results.

**This is a descriptive/diagnostic audit. It makes no causal claim and no direction claim.** D63 remains
`UNABLE as to cause`. The v1.2 verdict `PASS-CONDITIONAL` is **audited, not re-scored**: nothing here reopens
C1–C4, nothing here re-runs a WT/DT cell, and the `m = 1.10` convention and v1.2's scope
(*crossing/endpoint placement*) are **unchanged**. The κ-link is a **declared accounting constraint**
(an observed median, never fitted), not an estimated relationship.

---

## 1. The answer in two sentences

**No — v1.2 does not reproduce the observed path: 9 of 33 observed year-level comparisons are within ±5 pp
(27.3%), against a predeclared bar of 17/33.** **Yes — the declared κ-link binds hard: 20 of 53 anchor-type
years violate `upper_t ≤ 0.949·lower_{t−3}`, and imposing it drives upper 2024 from 76.64 to 63.97
(Δ −12.67 pp), class `b2`.**

**Verdict: `ENDPOINT-ONLY` + `b2` + `BASELINE-GUARD-PASS`.**

---

## 2. Leg (a) — the path (`ENDPOINT-ONLY`, 9/33)

The construction is exactly the predeclared one: all 33 observed PHL completion cells (11 per level; the year
sets differ by level — 2003 is upper-only, 2021 is primary/lower-only), each compared with `SYN00_PHL_LIKE`
`completion_uis × 100` at the **same** year and **same** level. No interpolation, no nearest-year substitution,
no missing cells. All 33 comparisons are in `results/PATH_COMPARISONS.csv`.

- **Within ±5 pp: 9/33 (27.27%).** Bar 17/33 → **`ENDPOINT-ONLY`**. Within ±10 pp: 13/33 (39.4%).
- Median signed deviation: primary **−4.30**, lower-secondary **−29.44**, upper-secondary **−27.59** pp.
- Worst miss: upper 1999 **−36.62** pp; lower 2000 **−33.37** pp.
- By level: primary **6/11** in band, lower-secondary **0/11**, upper-secondary **3/11**.
- The run independently reproduces the Council's V1 construction **exactly** (9/33, 13/33, the three medians,
  and the −36.62 upper-1999 worst miss): this is a re-derivation, not a re-reading.

**The shape is the finding.** Split at 2020:

| window | cells | within ±5 pp | median deviation |
|---|---:|---:|---:|
| 1999–2017 (`OBSERVED` vs `SYNTHETIC`) | 22 | **2** (9.1%) | **−28.21 pp** |
| 2021–2024 (`OBSERVED` vs `SYNTHETIC`) | 11 | **7** (63.6%) | **+0.04 pp** |

So the panel is a **2021–2024 placement**, not a path. Where it matches, it matches to within a couple of
points (2024 upper **+1.61**: 76.64 synthetic vs 75.03 observed; 2024 primary **+1.70**; 2022 primary
**+0.04**). Where it does not, it is short by a generation: the 7 pre-2021 lower-secondary cells are
**27.9–33.4 pp low** and the 8 pre-2021 upper-secondary cells are **24.4–36.6 pp low**. The lower level is
**0/11** in band — it never reproduces the observed series at any year. This is V1 confirmed, not refuted.

**What this licenses.** The synthetic level statements in EXP-1/EXP-2/A3-S are readable as statements about
**2022–2024 levels and crossing years** only. They are not readable as statements about the path, and the next
model line cannot start from a "level" that is a 2022–2024 placement. Per the frozen block, that re-scopes those
statements to 2022–2024 and points the next line at the **lower** series (median −29.44 pp).

---

## 3. Leg (b) — the declared link (`b2`)

### What was done

Nothing in the generator was edited. A **byte-identical copy** of the frozen panel
(`14729c51…acf5ac`, 6 720 rows) was taken into this directory, and the single declared constraint
`upper_t ≤ κ·lower_{t−3}` with **κ = 0.949** was applied **in memory** as a projection
`upper_t ← min(upper_t, κ·lower_{t−3})`, on `SYN00_PHL_LIKE` only, for the 53 years that have a `lower` value
three years earlier (1973–2025; 1970–1972 are `NOT-SCORABLE` and were **not** imputed). No other level, year or
parameter was touched. κ was **not** re-estimated: the provenance check re-derives the 8 observed PHL pairs
and gets median **0.94914** (→ 0.949) and pre-2018 median **0.95956** (→ 0.960), both matching the declared values.

### What it shows

| quantity | value |
|---|---|
| scored anchor-type cells | 53 (t = 1973…2025) |
| **violations before** | **20/53** — every year **2006–2025**, continuous |
| violations after the projection | 0/53 (implementation check) |
| largest excess above the bound | **+18.31 pp (2022)** |
| tightest slack before 2006 | −21.93 pp (the early path is far *below* the bound) |
| anchor years with `upper/lower_{t−3} > 1.10` | **12** (2013–2024), max ratio **1.2661 (2022)** — V2 re-derived |
| upper 2024, unlinked | **76.6391** |
| `lower 2021` used for the 2024 bound | **67.4073** |
| bound `0.949 × 67.4073` | **63.9695** (= the block's 0.949 × 67.41 = 63.9) |
| upper 2024, linked | **63.9695** |
| Δ 2024 | **−12.6695 pp** |
| ratio 2024 (`upper_2024 / lower_2021`) | **1.136955** |

**Class evaluation, all three reported:**

- **b1** (upper 2024 in [73,77]) — **FALSE**: 63.97 < 73.
- **b2** (upper 2024 < 71) — **TRUE**: 63.97 < 71.
- **b3** (|Δ| < 1.0 pp) — **FALSE**: |Δ| = 12.67 pp.

Predeclared precedence is b2 > b3 > b1, so the class is **`b2`** and it is not a knife-edge result. The
non-verdict-bearing sensitivity κ = 0.960 gives upper 2024 = **64.71** (Δ −11.93) — also `b2`. The class does
not depend on which of the two declared κ values is used.

**Read literally, as the block defines it:** the link binds, and **the binding defect is the lower series, not
the upper ceiling**. The arithmetic is transparent: to hold upper 2024 at its delivered 76.64 under κ = 0.949,
lower-secondary 2021 would have had to be **76.64 / 0.949 = 80.76** (`OBSERVED` 2021 value: 80.90 — i.e. the
observed lower series *would* support the delivered upper value). The generator's lower 2021 is **67.41**,
**13.35 pp short**. So the generator's 2024 upper endpoint is *not* inherited from its own lower pipeline; it is
produced by the upper block.

### What the baseline guard shows

- **G1** frozen panel sha256 = `14729c51…acf5ac` — matches the declared value.
- **G2** the copy analysed here (`results/BASELINE_UNLINKED_PANEL.csv`, 5 086 014 bytes) is **byte-identical**.
- **G3** the 112 anchor upper/lower cells read from the copy equal the frozen original, cell for cell.
- **G4** `sim_v1_2.py` (`61123aa9…`), `PARAMS.md`, `RUN_MANIFEST.json` and the panel all have the **same sha256
  after the run as before it**; nothing under `generator_v1_2/` was written.

**`BASELINE-GUARD-PASS`.** The block's falsifier (non-byte-identical baseline, or any parameter moved besides
the declared κ) is **not** triggered: exactly one thing was changed, and it was the declared κ projection.

---

## 4. What this says about the generator's capability to hold a pipeline

**It currently has no cross-level accounting at all.** The upper block and the lower block are not tied
together: for 20 of 53 anchor-type years — continuously from 2006 through 2025 — the synthetic panel completes
upper secondary for cohorts that, three years earlier, had not completed lower secondary at the rate the
delivered upper value requires. This is not a small calibration offset: the largest excess is **+18.3 pp**, and
in 12 of those years the ratio exceeds the observed PHL maximum (1.072), reaching **1.266**. The observed
series never exceeds 1.072 across its 11 pairs × 3 levels.

**The one endpoint v1.2 does match is not the pipeline's endpoint.** Under the declared link the 2024 upper
value falls to 63.97 — **11.06 pp below** the `OBSERVED` 75.03. So the ceiling that v1.2 delivers at 2024 is
**stipulated by its own upper block**, not inherited from a lower-secondary cohort flow. The match at 2024 and
the miss everywhere else are therefore the *same* fact seen twice: the panel is placed at the end of the period,
and the placement is made by the upper block.

That is a **capability** statement, not a causal one. The generator can produce an upper-series level; it cannot
yet produce one that is *accounted for* by its own lower series. Whether the real PHL ceiling is produced this
way is precisely what this diagnostic cannot say — no direction claim is made, and none is implied by the ratio.

**Caveat carried with the result.** κ = 0.949 is the observed **median**, not the observed **maximum** (1.072).
A median-placed necessary-condition constraint is expected to censor a panel that sits above the observed
distribution; the informative numbers are therefore *how many* years are censored (20/53), *where* the
censoring starts (2006), and *what 2024 becomes* (63.97), not the mere existence of violations. The start is
smooth — 2005 sits 0.69 pp below the bound, 2006 is 0.13 pp above it — so "first violation 2006" is a crossing,
not a break; the margin then widens to +18.31 pp by 2022. The 0.960 sensitivity shows the class is stable.

---

## 5. What this means for the v1.5 BIMODAL-GATE predeclaration

EXP-7 is the gate. It returns **three binding conditions** on that predeclaration, and one prohibition.

1. **The pipeline link must be built into v1.5 as a structural constraint, not post-processed.** A post-hoc
   projection cannot be ablation-tested under D81 the way an in-model constraint can: censoring 20 of 53 years
   *after* the model has run tells you the model overshot, but it does not make the upper level a function of the
   lower cohort one stage earlier. v1.5 must carry `upper_t ≤ κ·lower_{t−3}` (or its equivalent cohort-accounting
   identity) **inside** the transition each year, with κ as a **declared system input** (never fitted), so that the
   upper level is *inherited* rather than clipped.
2. **v1.2's 2024 endpoint may not be carried into v1.5 as a ceiling target or as evidence of inheritance.** The
   endpoint survives only while the upper block is free; under the declared link it drops 12.67 pp. Any v1.5
   predeclaration that states a ceiling claim on the strength of v1.2's 76.64 would be re-using a number that this
   audit shows is not pipeline-supported.
3. **v1.5's level claims must be scored on the path, not on an endpoint.** Leg (a) shows the panel matches only in
   2021–2024 (7/11 cells, median +0.04 pp) and misses 20 of 22 earlier cells (median −28.21 pp). A v1.5
   predeclaration that scores only 2024 would repeat the placement error at larger cost. The natural predeclared
   bar is the same shape as this one: a **count over the observed year-level cells**, not a single-year tolerance.

**Prohibition.** Because leg (a) returns `ENDPOINT-ONLY`, no v1.5 predeclaration may be *justified* by v1.2's
level path, and no synthetic level statement from EXP-1/EXP-2/A3-S may be cited outside 2022–2024. The v1.2 label
narrows to **crossing/endpoint placement**; `m = 1.10` and that scope are otherwise unchanged.

**What EXP-7 does *not* decide.** It does not say where the v1.5 gate should sit (that is EXP-8 GATE-LOCUS), it
does not test whether the ratio is a system object (EXP-6 PIPE-LOO), and it does not touch the demand line
(EXP-9). The frozen dependency order still holds: EXP-7 → EXP-6 → EXP-8 → EXP-9 → EXP-10.

---

## 6. Discipline and reproducibility

- **No re-fit, no tuning, no threshold change.** κ = 0.949 declared from the observed median before the run and
  verified afterwards; the class boundaries [73,77] / <71 / |Δ|<1.0 and the precedence b2 > b3 > b1 were fixed in
  the predeclaration; the 33 cells and the 53 scored years were fixed in the predeclaration.
- **No causal or direction claim anywhere.** D63 remains `UNABLE as to cause`.
- **No missing cell was imputed.** 1970–1972 are `NOT-SCORABLE`; zero synthetic cells were missing in leg (a);
  zero observed cells were added or dropped.
- **Determinism.** The script is RNG-free and timestamp-free. Run twice into `results/` and
  `results/determinism_run2/`; all six artifacts (`PATH_COMPARISONS.csv`, `KAPPA_LINK.csv`,
  `REPRO_PATH_RESULTS.csv`, `BASELINE_GUARD.json`, `console.txt`, `BASELINE_UNLINKED_PANEL.csv`) compare
  **byte-identical**.
- **No writes outside this directory.** No generator file was written; no web; the server was not touched.
