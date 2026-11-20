> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# WHAT WOULD COUNT AS SUPPORT — and what would count as impossible

**Scope.** This is **assumption-space mapping**. Nothing here is evidence about any country, any causal effect, or the
truth of the paper. A family that "fits" is a *sufficient assumption bundle*, not a validated theory. The runner will
produce synthetic profiles after this register lands; this file predeclares how those profiles will be read **before**
they exist.

## 1. Definitions (binding on the read-out)

- **Support (possibility)**: a family's simulated stage profile falls inside the predeclared literature range for
  **≥2 of the 10 targets in at least two countries**, with no target used as a fitted moment (HK 0.85 excluded as
  calibration; KOR no-fit). Support means "the assumption bundle can generate a profile that is indistinguishable
  from the literature on these targets" — nothing more.
- **Possibly consistent**: at least one family inside the **HKG** three-stage gradient (F2 is predicted to be), at
  least one family inside the **PHL/KHM** rows (F3 is predicted to be), and no family inside the **KOR** profile —
  i.e., consistency is **country-type contingent**, not universal.
- **Not supported**: every family outside on ≥8 of 10 targets.
- **Impossible within this space**: a target pattern that **no family** with parameter values inside its declared
  plausibility bands can produce, or that can only be produced by setting a parameter to the target (restatement), or
  that requires a family to change structure mid-run. Impossibility is a statement about the model class + assumption
  space, not about the world.
- **Evidence** (outside this exercise): measured parameter values, out-of-sample prediction, identification. Support
  is **not** evidence and must never be written up as validation.

## 2. Predeclared support criteria (declared 2026-11-20T13:52+08:00, before any runner synthetic run)

| # | Criterion | Threshold | Predicted outcome |
|---|---|---|---|
| S1 | Family-level fit on the HKG 2003 stage gradient | all three rows inside their ±5 pp bands | F2 predicted INSIDE; F5/F6 predicted on S6–7 and S4–5; F1/F4 predicted outside |
| S2 | Family-level fit on the PHL 2010 aggregate | inside [42.0, 49.9] | F3 predicted INSIDE (44); F2 boundary (42); F5/F6 inside (44/46) |
| S3 | Family-level fit on KHM primary | inside [36.3, 46.3] | F3 predicted INSIDE (45) |
| S4 | Family-level fit on KHM grade 9 | inside [63.4, 73.4] | **no family predicted inside** (F3 central 58 is the closest) |
| S5 | Family-level fit on the KOR four-stage profile | all four rows inside their bands | **impossible prediction** (no family; F6 hits KOR high only) |
| S6 | Same family fits rich and poor presets | ≥1 family inside ≥1 rich and ≥1 poor target | allowed (country-type contingency); a **single** family inside all four countries' profiles is predicted IMPOSSIBLE |
| S7 | Evidence of restatement | any parameter set to a target value, or fit performed on the targets | automatic FAIL of support for that family |

## 3. What the runner's output would mean

- **If F2 lands inside all three HKG rows and F3 inside PHL/KHM-primary** (as predicted): the assumption space
  contains at least one coherent rich-country bundle and one poor-country bundle that generate literature-consistent
  shadow profiles. Report as: *"possibly consistent, country-type contingent"*. Do **not** report as validation;
  do not generalise to KOR, KHM grade 9, or any country not in the fit.
- **If a family predicted OUTSIDE lands INSIDE** (e.g., F1 or F4 inside HKG): either (a) the prediction register's
  mapping is wrong (report the miscalibration; the assumption space is larger than mapped), or (b) the family's
  parameters are outside their plausibility bands (check and report). Do not quietly accept it as a hit.
- **If the runner produces the KOR falling profile or the KHM 68.4/41.3 pair**: the model class contains a channel the
  family mapping missed (most likely the two-margin R23 mechanism, or a teacher-sold supply structure). This is a
  **structural finding about the model**, to be reported as such — not a rescue of any incidence claim, which remains
  withdrawn by brief 008.
- **If no family lands inside ≥2 targets in ≥2 countries**: the assumption space **cannot** generate the literature
  patterns with coherent bundles — the "impossible within this space" outcome. Report it, and do not widen parameter
  bands post hoc.

## 4. What remains impossible regardless of the runner's output

1. **A validated cross-country incidence claim.** Support is synthetic; the programme's identification limits
   (brief 008) stand. No family-level fit reopens them.
2. **A single causal mechanism classification.** Families F2, F5 and F6 share predicted HKG senior-secondary values
   (72); on shadow data alone they are observationally equivalent. That is the programme's equivalence result
   reappearing inside the assumption space.
3. **A country forecast.** No family is a forecasting device; synthetic paths are conditional on the family's
   assumptions and are not projections.
4. **Any use of R13's negative education→growth estimate as a "result"** — it is a panel association from
   `RELATION_CANDIDATES.csv` (correlational/contrary evidence), not an identified effect; F7 exists to make the model
   confront it, not to settle it.

## 5. Reporting rules

- Every statement from brief 009 must carry: "assumed parameters; possibility analysis; not evidence".
- Every simulated value is conditional on its family; never compare a family's synthetic value to a country as if it
  were an estimate.
- If a family is dropped or changed after the runner runs, record the change as an amendment with a new timestamp;
  the register hash (`82c24773…`) is the predeclaration anchor.


## 4a. Economic complexity (Lead amendment) — what it can and cannot do

**Complexity is a country-level index (ECI/COI), not a mechanism.** It can legitimately:

1. **condition** the family map (a third axis next to capacity-binding): high-ECI, capacity-not-binding economies
   should look like F1/F6 (senior-gate, commercial, income-elastic); low-ECI, capacity-binding economies like F3/F7
   (teacher-sold, basic-heavy). The register rows CX-01…CX-04 encode these **direction-only** predictions.
2. **rank** countries for the runner's synthetic draws, once `04_data/complexity/` lands (currently PENDING), and
   supply a sign check: does higher ECI associate with higher senior/tertiary take-up and higher formal/complex-job
   share, with near-null at basic?

It **cannot**:

- serve as **synthetic validation**. A family that *embeds* an ECI parameter and then reproduces a shadow profile is
  reproducing its own assumption; ECI is also endogenous to education and correlated with income/capacity, so a fit
  would not identify complexity as a driver.
- be scored inside/outside: ECI is not a literature shadow target, and there is no verified ECI–tutoring coefficient
  on disk. Complexity rows are **n/a (direction-only)** by construction.
- reopen any stop rule from brief 008. If complexity data lands and the direction checks fail, that is a finding
  about the assumption space (the axis does not help), not a test of the model.

**If ECI/COI data remains absent at the runner's start:** mark the complexity axis PENDING, run the six-family map
unchanged, and record that the complexity rows were unscoreable. Do not impute ECI.
