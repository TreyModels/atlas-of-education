# FINDINGS — SYNTHETIC education-system generator, v0

> **SYNTHETIC. This is a seeded computer model that grows data from declared equations.
> It is not calibrated evidence about the world, not a forecast, and not a fit to any
> observed country series. No observed data file is read at runtime.** The only observed
> numbers encoded are the declared targets listed in `PARAMS.md` §3. Every output row is
> labelled `SYNTHETIC`.

---

## 1. What was built

`code/sim.py` generates a panel of **32 synthetic countries × 55 years (1970–2024) × 4 school
levels = 7,040 rows**, seed **20261120**. The equations are the six declared blocks in
`PARAMS.md` §1: demography, a logistic demand ceiling with a country fixed effect, a capacity
gate `K^0.75`, a 0/1 law push, a flow/stock identity, and one declared `PHL_like` country.
The model is deterministic (`PCG64`), stdlib + NumPy only, and runs in well under a second.
The `PHL_like` country is **pattern-matched to the brief's milestone description**, not fitted
to the observed Philippine series.

The anti-double-count identity is enforced exactly. The output `cohort` is the level-specific
official-age population (`base 0–14 cohort × ω_L`, with `ω` applied **once**); `enrolment =
cohort × p`; `GER = 100 × enrolment / cohort = 100p`; `completion = s_L × p × 100`.
Across all 7,040 rows the maximum identity error is **5×10⁻⁷** for GER and **1×10⁻⁶** for
completion (6-decimal output rounding). No second cycle-length or previous-level completion
factor is applied anywhere.

---

## 2. Check results

| check | what | synthetic result | verdict |
|---|---|---|---|
| **C1** | GER ∈ [0,105] hard bound | min **0.8737**, max **100.0097**; 0 negatives, 0 above 105, 7,040 cells | **pass** |
| **C2** | between-country log-log income exponent, secondary & tertiary vs brief targets (+0.29 / +0.78, ±0.15) | secondary **+0.2819** (all) / **+0.2900** (excl PHL); tertiary **+0.7757** / **+0.7800**; R² 0.471 / 0.641 | **pass** |
| **C2b** | within-country (country+year FE) exponent vs on-disk within estimates (+0.0904 / +0.8482, ±0.15) — diagnostic | secondary **+0.4607** (diff **+0.3703**); tertiary **+0.7489** (diff **−0.0993**) | **fail** |
| **C3** | PHL-like milestone pattern | primary 90 at **2003** (2024 = 94.00); lower-sec 90 at **2016** (2024 = 92.00); upper-sec max **78.00** (<90); tertiary **15.00 → 50.83**, monotone; crosses 25 at 1996, 40 at 2016 | **pass** (with caveat) |
| **C4** | +0.10 capacity from 1990: floor (primary) vs ceiling (upper-sec) | ΔGER 2020–24: primary **+6.505**, lower **+5.938**, upper **+4.894**, tertiary **+3.992** pp; floor−ceiling **+1.611 pp** | **pass** (mechanical) |
| **C5** | hard sanity: no negative enrolment; GER/completion in [0,105]; rates in [0,1]; completion monotone in enrolment | 0 negative enrolments; GER [0.87, 100.01]; completion [0.77, 95.01]; all rates valid; within-level corr(p, comp) ≈ 1.000 | **pass** |
| **C5b** | cross-level ladder: primary ≥ lower ≥ upper ≥ tertiary completion | compliance **69.89%** (1,230/1,760); **530 violations**; pairwise 86.82% / 93.52% / 84.38% | **fail** |

`verdict` values in `reproduction_checks.csv` are exactly `pass` / `fail` (no `inconclusive`
was needed). C2b and C5b are declared diagnostic decompositions added to C2 and C5; they are
not rescues or extra passes.

---

## 3. What the declared equations *can* reproduce (and why that is not a discovery)

1. **The encoded between-country income-scaling ordering and approximate magnitudes.**
   The synthetic between-country exponents are +0.2819 (secondary) and +0.7757 (tertiary).
   This is **target encoding, not validation**: `b_sec=1.055144` and `b_ter=1.108998` were
   solved by declared bisection precisely so the 31 generic countries hit +0.29 / +0.78.
   The generator embodies the literature's assumed relations; C2 is a consistency check of
   that embodiment. It tells us the equations *can* carry those two numbers simultaneously,
   not that the world does.

2. **The PHL-like milestone pattern, with mild country effects.** Primary completion crosses
   90 in 2003, lower-secondary in 2016, upper-secondary tops out at 78.00 and never crosses
   90, and tertiary rises 15.00 → 50.83. The four solved fixed effects are all mild
   (z = 0.10, 1.28, 0.78, −0.39). The pattern is produced mainly by the declared growth path,
   the capacity path (`K0=0.75` → gate ≈1 by 2024), and the synthetic law pushes — not by an
   extreme "Philippines" dummy. This is still **pattern matching to the brief**, not evidence
   about the Philippines: the law dates are synthetic, and the growth/capacity path was chosen
   from a declared grid (PARAMS.md §5.2), not observed.

3. **The floor-not-ceiling capacity shape, mechanically.** A permanent +0.10 capacity increase
   lifts primary GER by 6.505 pp, lower-secondary by 5.938, upper-secondary by 4.894, and
   tertiary by 3.992. The ordering is exactly the programme's "capacity buys the floor" shape.
   But it is close to a tautology of the declared form: effective ceiling = demand ceiling ×
   gate, and the demand ceilings are ordered primary > lower > upper > tertiary, so a
   proportional gate rise moves the higher-ceiling level more in absolute pp. C4 is not
   independent evidence for a floor mechanism.

4. **The identity and the bounds.** GER never leaves [0,105]; completion never leaves [0,105];
   no negative enrolment; within-level completion is monotone in enrolment by construction.
   The old model's double-counting failure is structurally fixed.

---

## 4. What the declared equations *cannot* reproduce (honest failures)

### 4.1 Within-country secondary income scaling (C2b): +0.46 vs +0.09

The model has **one income slope per level**, `b_L`, which drives both the between-country and
within-country margins. Calibrating `b_sec` to the between target (+0.29) forces the
within-country secondary exponent to **+0.4607**, about **5.1×** the on-disk within estimate
of **+0.0904** (which is itself insignificant, t=0.94). The on-disk data show a *weak*
within-secondary effect and a *strong* within-tertiary effect (+0.8482); the synthetic model
gives +0.4607 and +0.7489. That between/within divergence is a structural feature the
single-slope logistic cannot carry. This is the most important modelling failure in v0: the
generator can match either margin's number, not their *different* numbers.

### 4.2 The cross-level ladder (C5b): 30.1% violations

Only **69.89%** of country-years satisfy primary ≥ lower ≥ upper ≥ tertiary completion
(530/1,760 violations). Tertiary completion exceeds upper-secondary completion in **15.6%** of
country-years; lower-secondary exceeds primary in **13.2%**. The levels are independent
participation margins with independent fixed effects, so a country can have a strong tertiary
effect and a weak upper-secondary effect. The consequence is visible in the 2024 cross-section:
**17 of 32** synthetic countries have tertiary GER ≥ 50, while only **3 of 32** have
lower-secondary completion ≥ 90 and **0 of 32** have upper-secondary completion ≥ 90. That is
not a coherent schooling ladder; it is four loosely coupled series. The programme's own
"upper-secondary stalls below 90" finding is reproduced for `PHL_like` (78.0), but not as a
general ladder property.

### 4.3 The brief's targets do not match the cited on-disk file

The brief's targets are +0.29 / +0.78. `10_massification/relations/data/scaling_laws.csv`
contains **+0.2154 / +0.5666** between-country and **+0.0904 / +0.8482** within-country.
The encoded +0.78 is **+0.213** above the on-disk between tertiary estimate, outside the
declared ±0.15 tolerance. So:

- **C2 vs the brief**: pass.
- **C2 vs the CSV's between tertiary**: off by +0.209 → would be "off".
- **C2b vs the CSV's within secondary**: off by +0.370 → fail.

This is a provenance problem in the task specification, not a numerical one. The generator
does not silently reconcile the brief with the file; both are reported. If the programme's
actual target is the CSV's between-country 0.5666, then v0's tertiary exponent is wrong by
about 0.21 and the b_ter calibration would need to be redone (which would also change the
within-tertiary result). **Do not quote C2 as reproducing the on-disk scaling law without
this caveat.**

### 4.4 Other things it cannot do

- **GER > 100 is barely exercised.** Only one cell exceeds 100 (100.0097); the 105 upper bound
  is never approached. The model has no repetition/over-age mechanism, so the [0,105] band is
  satisfied but the top of it is untested. C1 is a real check of the floor and the cap, not of
  the over-age regime.
- **No reversals, crises, or stagnation.** Every driver is monotone non-decreasing (income
  growth ≥0, urban/services/spending trends ≥0, capacity non-decreasing), and the adjustment
  rule is monotone. Across all 7,040 series the minimum year-on-year GER change is **+0.0059**
  and the minimum completion change is **+0.0052** — there are **zero** negative changes. The
  model cannot produce a country that backslides, a conflict shock, or a lost decade.
- **The PHL-like tertiary take-off precedes lower-secondary universalization.** Tertiary GER
  crosses 25 in **1996**, twenty years before lower-secondary completion crosses 90 in **2016**.
  The brief's staged order (primary → lower-secondary → tertiary) holds only at the **terminal**
  milestone (tertiary 2024 ≈ 50); it does not hold for take-off. C3 is marked pass on the
  declared terminal ordering, with this caveat explicit in the check note.
- **No country-specific income slopes, no diffusion, no labour-market feedback, no teacher
  production function, no migration/foreign students.** These are declared omissions, not
  hidden parameters.
- **Balanced panel / entry timing.** Every country is observed 1970–2024. "Varying start
  dates" is implemented as country-specific `law_year` policy dates, not as an unbalanced
  entry panel.
- **The "PHL-like" label is a pattern target, not the Philippines.** The synthetic law dates
  (1990/1995/2005/2015) are not the observed statutory dates; the growth path (2.0%/yr) and
  capacity path (K0=0.75) were chosen from a declared grid to land 15 → 50. It should never be
  read as a calibrated PHL model.

---

## 5. Which parameters do the most work / which assumption is load-bearing

**Target-driven parameters.** `b_sec=1.055144` and `b_ter=1.108998` are the load-bearing
encoded numbers. They are larger than a naive `e/(1−p)` calculation because the logistic
compression and the country fixed-effect dispersion attenuate the cross-country slope; the
bisection has to push `b` up to recover +0.29/+0.78. Changing the target (e.g. to the CSV's
0.5666 for tertiary) would lower `b_ter` and change the within-tertiary result too. These
parameters are doing exactly the work they were asked to do — which is why C2 is not evidence.

**`C_MEAN` and the level ordering.** `C_MEAN = (0.92, 0.72, 0.50, 0.32)` sets the ordering of
the demand ceilings. It is what makes C4's floor > ceiling result come out the "right" way,
and it is a pure design choice. If the ceilings were flat or reversed, C4 would fail.

**PHL growth and `K0`.** The 15 → 50 tertiary path is sensitive to the synthetic growth path:
the declared grid (PARAMS.md §5.2) spans 36.5 → 57.0 across growth 1.0–2.2% and K0 0.55–0.75.
The chosen (K0=0.75, growth=2.0%) gives 50.83. This is a design choice matched to the brief's
~50, not an estimate of PHL growth.

**The most load-bearing assumptions** are:
- **A1 (one logistic ceiling, one `b_L` per level)** — this is what forces the between/within
  conflation and produces the C2b failure. It is also what makes the model inspectable.
- **A2 (independent level fixed effects)** — this is what produces the C5b ladder failures and
  the 17/32-tertiary-vs-3/32-lower inconsistency. A correlated country effect across levels
  would reduce (not necessarily eliminate) the violations; it was not imposed, because the
  failures are informative.
- **A3/A4 (one-time `ω`, completion identity)** — the anti-double-count fix. This is the part
  the old model got wrong; v0 enforces it exactly, and the identity errors are at rounding
  level.
- **A5 (capacity gate)** — the supply mechanism behind C4; its `κ=0.75` and the additive push
  are declared, not estimated.

---

## 6. Determinism and reproduction

`code/verify_and_manifest.py` ran `sim.py` twice into separate directories and compared every
`results/*.csv` byte for byte:

- **byte_identical = True**; run1 and run2 SHA-256 sets are equal.
- Runtime ≈ **0.25 s per full run** (well under 60 s).
- Seed **20261120**; fixed draw order; fixed bisection counts (50 for `b`, 60 for PHL e);
  `%.6f` output formatting.

Recorded hashes (full values in `RUN_MANIFEST.json`):

| file | SHA-256 (first 16) | bytes |
|---|---|---|
| `results/synthetic_panel.csv` | `e97297d48f528c8f` | 860,087 |
| `results/reproduction_checks.csv` | `ab3079fcb8ff1988` | 5,011 |
| `results/calibration_log.csv` | `f4f315adb8784905` | 19,380 |
| `results/capacity_counterfactual.csv` | `40ea9ece4a128c53` | 320 |
| `code/sim.py` | `b076da69e62e81ba` | — |

`RUN_MANIFEST.json` records `data_files_read: []`, the target citation
(`10_massification/relations/data/scaling_laws.csv`, citation only), Python 3.11.17, NumPy
2.4.6, all parameters, the solved `PHL_e`, and the two-run hash comparison.

---

## 7. Bottom line

Version 0 is a **transparent target-encoding machine**. It reproduces what it was told to
reproduce — the between-country income exponents (as encoded), the PHL-like milestone pattern
(with mild fixed effects), the floor > ceiling capacity shape (mechanically), and the
flow/stock bounds (by construction). It fails on the margins it was not designed to carry:

1. **C2b**: the within-country secondary exponent is +0.46, not +0.09 — one slope cannot carry
   both margins.
2. **C5b**: the cross-level ladder fails in 30.1% of country-years; tertiary massification
   outruns lower-secondary universalization in the synthetic panel.
3. **The brief/CSV target mismatch**: the encoded +0.78 is +0.213 above the cited file's
   between-country +0.5666, so C2 passes the brief but would fail the on-disk target.
4. **No reversals and no GER > 105**: the model is a monotone, bounded world; it cannot
   reproduce crises, stagnation, or the over-age regime.

That is the honest result: the generator is useful as a *falsification scaffold* — a machine
that can be asked which regularities survive its declared equations — not as evidence about
education systems. The load-bearing choices are the single income slope per level (A1), the
independence of levels (A2), and the target numbers themselves (which do not exactly match the
cited file). Tuning any of them post hoc to rescue a check would defeat the purpose.
