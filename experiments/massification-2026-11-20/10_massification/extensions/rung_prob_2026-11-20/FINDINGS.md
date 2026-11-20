# FINDINGS — EXP-9 RUNG-PROB: is the ceiling demand-derivable from either probability?

**LABEL: SYNTHETIC / DECLARED.** Every number below comes from the frozen declared-assumption
generator; no real country is modelled or measured. **No causal and no direction claim.** This is a
bracket test of one declared object, not evidence about any education system or labour market.

## The one-paragraph answer

**No. The ceiling is not demand-derivable from either probability the model actually has.** With one
declared substitution each and everything else frozen, the school-gate probability
(`P = pi0(g2) ≈ 0.999`) drives upper-secondary UIS completion in 2024 to **95.04548615** — **+18.4064
pp** vs the demand-OFF baseline and **16.0455 pp outside** the `[71,79]` band — and the job-rung
absorption (`P = rung4_emp/rung4_demand`, anchor median **0.151**) drives it to **42.12562430** —
**−34.5135 pp** vs baseline and **28.8744 pp below** the band. Both arms are ablation-live (18.41 pp
and 34.51 pp, both above the 3.0 pp D81 bar), so the block is not decorative in either arm; it simply
cannot produce the ceiling from either probability. The falsifier fires: **both arms outside
`[71,79]` → `NOT DEMAND-DERIVABLE`**. The **A3 line is KILLED, not parked**, and the taste parameter
is recorded as **irreducible without a fit**. No threshold, band, bar, arm or parameter was changed
after any result was seen. This negative was the pre-declared expectation.

## 1. The two arms (single substitution each, all else frozen)

| arm | `P(advance at L=2)` | upper 2024 | in `[71,79]`? | distance from band | ablation vs OFF | D81 (≥3.0 pp) | arm verdict |
|---|---|---:|---|---:|---:|---|---|
| baseline OFF (v1.3 world) | none (block OFF) | **76.63908112** | yes | 0 | — | — | INFO |
| **A** | `pi0(g2)` ≈ **0.999** | **95.04548615** | **no** (above) | **+16.0455** above 79 | **+18.4064** | 18.41 → NON-DECORATIVE | **NOT DEMAND-DERIVABLE** |
| **B** | `rung4_emp/rung4_demand` (anchor median **0.151**) | **42.12562430** | **no** (below) | **−28.8744** below 71 | **−34.5135** | 34.51 → NON-DECORATIVE | **NOT DEMAND-DERIVABLE** |

- **Overall verdict: `NOT DEMAND-DERIVABLE`.** `both_arms_outside_band = TRUE`, falsifier triggered.
- Arm A is the frozen v1.4 ON arm, re-derived here, not assumed: its panel matches the frozen v1.4
  panel byte-for-byte (guard G2). It overshoots by the same **+18.4064 pp** A3-D measured (V7a: the
  “+18.05 pp” in the A3-D record is the distance above the band **edge 77**, not the delta vs
  baseline; the delta and the ablation are +18.4064).
- Arm B is one substitution: the frozen `demand_values()` is called with `gs[2]["pi0"]` replaced by
  the frozen v1.2 panel ratio for the same synthetic country and calendar year. `R_gate`, access,
  wages, costs, migration and remittance terms are unchanged; no RNG is drawn. The substitution is
  defined in 1 580 of 1 680 country-years; in the 100 cells with `rung4_demand = 0` (all pre-2006,
  **none** in `SYN00_PHL_LIKE`) the declared fallback leaves `pi0(g2)` in place. The fallback is
  therefore **inert for the scored anchor**; the arm-B self-check asserts zero anchor fallbacks.

## 2. Baseline guard — byte-identical, PASS

| guard | written panel | sha256 | expected (frozen) | result |
|---|---|---|---|---|
| **G1** demand-OFF | `results/panels/synthetic_panel_v1_4_demand_off.csv` | `47d4b082f4ba5838…` | `47d4b082f4ba5838…` (v1.3) | **byte-identical** |
| **G2** arm A ON (no substitution) | `results/panels/synthetic_panel_v1_4_demand_on_armA.csv` | `ffecd450514cf825…` | `ffecd450514cf825…` (v1.4 ON) | **byte-identical** |

The unmodified arm reproduces the frozen v1.4 panel, and the demand-OFF run reproduces the frozen
v1.3 panel, **byte-for-byte**. `guard_verdict = PASS`, so the arm values are scored.

## 3. Why the numbers land where they do (anchor `SYN00_PHL_LIKE`, upper secondary)

| year | arm B `P` | arm B `v_D` | arm B demand share | OFF demand share |
|---:|---:|---:|---:|---:|
| 1980 | 0.012463 | 0.047731 | 0.324721 | 0.807255 |
| 2000 | 0.067757 | 0.065626 | 0.333256 | 0.804591 |
| 2020 | 0.166102 | 0.226146 | 0.433039 | 0.804871 |
| 2024 | 0.185365 | 0.298076 | 0.480185 | 0.800311 |

The declared taste value at L=2 is `v_2 = v0·decay² = 0.78608`. In 2024, arm A's demand value is
`v_D = 1.93935` (≈2.5× the taste value), which drives the demand share to 0.9925 and completion to
95.05. Arm B's is `v_D = 0.29808` (≈0.38× the taste value), which holds the demand share at 0.4802 and
completion at 42.13. The two candidate probabilities therefore **bracket** the taste value, but
neither is close enough: the ceiling is produced by a taste level that is neither probability's
demand value. The job-rung absorption is especially small in the early decades (0.0016 in 1970,
0.0125 in 1980, 0.068 in 2000) because the formal top rung barely exists then; substituting it
suppresses upper-secondary demand for decades, which is why the undershoot is much larger than the
raw 0.151/0.999 ratio would suggest at a single year.

**No fit was performed.** There almost certainly exists some `P` between 0.151 and 0.999 that would
drive upper 2024 into `[71,79]` — but choosing it would be exactly the fitted “demand parameter” that
R4/R27 forbids, and the brief's test is whether **either probability the model actually has** works,
not whether some fitted probability could. None was searched for.

## 4. Verdict and disposition

- **`NOT DEMAND-DERIVABLE`.** The falsifier condition is met: both arms fall outside `[71,79]`.
- **The A3 line is `KILLED`, not parked.** No further demand re-specification is admitted this phase.
  Both outcomes were declared to end the parked state (SYNTHESIS_022 §6 EXP-9.2); this is the
  negative branch.
- **The taste parameter is recorded as irreducible without a fit.** The ceiling in v1.2/v1.3/v1.4
  remains a declared-taste phenomenon. A v1.5 demand block is **not** licensed by this test.
- **A negative is the expected outcome**, not a failed experiment: the block itself declared that the
  informative arm (B) must undershoot by arithmetic.

## 5. Closed-claim check (binding)

- **A3-D's `FALSIFIED` verdict stands.** EXP-9 is **not** a rescue, re-run, re-score or re-litigation
  of A3-D; it is a new declared object as D116 required. The A3-D numbers appear only as the arm-A
  result.
- **No fitted demand parameter (R4/R27).** No value was chosen by looking at `[71,79]`; the band, the
  3.0 pp bar and the two probabilities are copied from the block. The arm-B probability is a frozen
  panel column, not an estimate.
- **No causal or direction claim.** The result is about a declared synthetic generator. It does not
  say demand is weak, absent or unimportant; it does not say returns do or do not drive schooling
  anywhere.
- **Migration / remittance stays DECLARED / NOT-VERIFIED.** No literature coefficient is inserted;
  the channel is not used to explain any result, and the substitution does not touch it.
- **The “no demand falsified” language stays banned.** What failed in A3-D was the demand channel's
  **specification** — a demand block attached to a non-binding gate — **not demand as a phenomenon**.
  Demand is revealed and strong; the generator's single-gate household block has no dimensionally
  neutral slot for it. EXP-9 sharpens that: even the model's *other* probability (the job-rung
  absorption V8 identified) does not reproduce the ceiling, because it is not a school-advance
  probability and its level is far below the taste value the ceiling needs.
- **No C1–C4 reopening; no WT/DT re-run; D63 remains `UNABLE` as to cause; the phase verdict is
  untouched.**

## 6. Determinism and integrity

- One PCG64 stream, `seed = 20261120` (inherited from v1.2/v1.3/v1.4); the substitution draws no
  random number; floats at `%.10g`; no wall-clock or absolute path in any output.
- Two clean runs into separate directories: **0 `cmp` failures** across `RUNG_PROB_RESULTS.csv`,
  `RUNG_PROB_ARMS.csv`, `BASELINE_GUARD.json`, all three panels and `RUN_MANIFEST.json`.
- The frozen v1.4 code copy is byte-identical (`6e4a6761…`), the v1.3 base copy is byte-identical
  (`70ae8f0e…`), and no file outside this directory was written.
- The runner refuses to run if `PRE_DECLARATIONS.md` (`1cd399dd…`), the frozen code copy or the base
  copy no longer match their frozen hashes.

## 7. Limits (what this does not test)

- It does **not** test a bimodal/scarce-gate demand model, a scarcity-based `P`, a different
  credential→rung destination mapping, or any re-specified demand object. Those would be new declared
  objects, and the block explicitly admits no further demand re-specification this phase after a
  failure.
- Arm B uses the **economy-wide** rung-4 absorption from the frozen v1.2 panel as the household's
  advance probability; that is V8's declared object, not a behavioural estimate of a household's
  perceived probability. The result is conditional on that declared reading.
- The rung-4 ratio is defined only where `rung4_demand > 0`; the 100/1 680 fallback cells are early
  years and are inert for the anchor, but they mean arm B is a declared composite rule, not a single
  number applied uniformly to all cells.
- No claim is made about the real PHL, HKG or KHM systems, or about any causal direction.

## 8. Bottom line for the Council

The bracket test was executed and is clean: both guards byte-identical, both arms deterministic,
both arms ablation-live, neither in band. **The ceiling is not demand-derivable from the school-gate
probability (overshoots by 18.41 pp) or from the job-rung absorption (undershoots by 34.51 pp). The
A3 demand line is KILLED, not parked.** The taste parameter is recorded as irreducible without a fit;
no fitted demand parameter was introduced; the migration/remittance channel remains
DECLARED/NOT-VERIFIED and unused; A3-D's FALSIFIED verdict stands without rescue. The failure is a
**specification** failure of the demand block, not evidence that demand does not matter.
