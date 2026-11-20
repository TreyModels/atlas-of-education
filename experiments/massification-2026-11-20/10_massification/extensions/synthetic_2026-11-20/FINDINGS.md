# FINDINGS — synthetic-data workbench (v0 + v1)

> **SYNTHETIC. Everything this workbench generates is a declared-assumption simulation, not evidence,
> not an estimate, not a forecast, and not a model of any real country.** No causal or push/pull
> direction claim is licensed by anything below. Country labels are synthetic (`SYN00_PHL_LIKE` etc.).
> The only observed numbers encoded anywhere are the declared targets listed in
> `generator_v1/results/RUN_MANIFEST.json` (`targets_encoded`) and declared in the fact register.

**Built:** 2026-11-20. **Status:** v0 DONE (delivered 21:58), v1 DELIVERED (22:01) — **v1 passes 2 of its
6 predeclared checks**; see §4. The user's latest directive (education → economic complexity, separate from
growth) is recorded as an amendment to `MODEL_ARCHITECTURE.md` and is **not yet implemented** (v1.1 work).

---

## 1. What the workbench contains

| component | what it is | size |
|---|---|---|
| `MODEL_ARCHITECTURE.md` | the user's verbal specification, restated as a layered design directive (+ dated amendments) | 95 lines + amendments |
| `equations/EQUATION_REGISTER.csv` | every equation/relationship in the programme's massification literature layer, with status, form, parameters, implementation site | **43 rows**; 10 tagged `equation-in-literature` (candidate/definition forms included), the rest `narrative-only`, `programme-invented` or `programme-estimated` |
| `facts/STYLIZED_FACTS.csv` | the provenance-labelled facts a generator may reproduce | **53 facts**; **35 VERIFIED-FROM-DISK**, 6 SIMULATED, 5 DISPUTED, 4 MODEL-OUTPUT-NOT-FACT, 3 REPORT-ONLY-UNRELIABLE |
| `generator_v0/` | arithmetic skeleton: demand-ceiling + capacity gate + law push, one declared PHL-like country | 32 synthetic countries × 55 years (1970–2024) × 4 levels = **7,040 rows**; `FINDINGS.md`, `PARAMS.md`, `results/` |
| `generator_v1/` | layered, tiered, occupation-aware generator (takeoff regime, sector mix, job ladder, rank/queue matching, composition growth) | 30 synthetic countries × 56 years (1970–2025) × 4 levels = **6,720 rows**; `PARAMS.md`, `code/sim_v1.py`, `results/` |

Both generators use one seeded NumPy `PCG64` stream (seed 20261120), read no observed data at runtime, and write
fixed-precision CSVs so reruns are byte-identical.

## 2. v0 — arithmetic skeleton (DONE)

v0 establishes the flow/stock accounting: logistic demand ceiling, capacity gate `K^0.75`, a 0/1 law push, the
cohort-flow identity, and a declared `PHL_like` country pattern-matched to the brief (not fitted to observed
Philippine series). Its report discloses two failures rather than hiding them:

1. **C5b cross-level ladder** — primary ≥ lower ≥ upper ≥ tertiary completion holds in only **69.89%**
   (1,230/1,760) of country-years (530 violations; pairwise 86.82% / 93.52% / 84.38%). The ordering is not
   enforced by construction in v0.
2. **Within/between conflation** — v0's one demand relation does not separate within-country dynamics from
   cross-country level differences, so its "reproduction" of income scaling mixes the two margins.

v1 was specified to add the missing structure (tiers, occupations, takeoff, queue) on top of v0's skeleton, which
it does — but it does not repair the ladder violation (§4, check A).

## 3. v1 — what it actually implements (as delivered)

Layers as in `MODEL_ARCHITECTURE.md`: Layer 0 economy states (complexity-like `X`, income, urbanisation, sector
mix, four formal job rungs, three takeoff states); Layer 1 cohort-flow schooling supply (GER capped at 105,
completion from the cohort flow with a duration lag, not a product of fitted probabilities); Layer 2 rank-based
absorption into formal rungs vs the informal residual, with queueing; Layer 3 composition-weighted growth
(productivity by sector + a finite step when a worker moves to a formal rung); Layer 4 synthetic panel + a
reproduction-check table. Declared country set includes a PHL-like economy and a matched twin pair that differs
**only** in sector mix (manufacturing-biased vs office/BPO-biased).

## 4. v1 reproduction checks (predeclared A–F; frozen in `code/sim_v1.py`)

**Result: A FAIL · B FAIL · C FAIL · D FAIL · E PASS · F PASS (2/6).** This is the honest headline. The failures
are informative about which parts of the declared architecture do not yet bite; they are **not** evidence about
the world and must not be spun either way.

| check | verdict | key numbers (synthetic) | reading |
|---|---|---|---|
| **A. PHL signature** (one parameterisation, no per-level rescue) | **FAIL** (2/6 components) | primary completion first ≥90 in **2011** (target 2017); lower-sec **never** reaches 90 (2023 = 76.88; target 2024); upper-sec never ≥90, max 75.96, 2024 = 75.96 ✓; tertiary GER 1971 = 16.45 ✓ → 2025 = **54.19** (target 48.1–54.1, misses by 0.09); floor→middle gap n/a; ceiling residual 14.04 ✓ | the secondary ladder compresses: lower- and upper-secondary completion converge near 76% instead of forming a 5–9y staircase. The model overshoots tertiary slightly and reaches primary "universalization" six years early. |
| **B. Literacy vs schooling-years horse race** | **FAIL** | industrialising/diversified decades (n=66): literacy −0.288 (p=0.569), schooling-years +0.073 (p=0.210) → schooling-years *is* weak (cond2 ✓) but literacy is **not positive** (cond1 ✗); pre-industrial decades (n=114): literacy **+1.781** (p<0.001), schooling-years +0.192 (p<0.001) → not flat (cond3 ✗). Occupation-structure ablation: literacy association **survives** without the rung ladder (−0.375, p=0.449) | the synthetic world puts the literacy–growth association in **pre-industrial** decades, not in takeoff — the opposite of the user's specification; and the association does not run through the occupation ladder. |
| **C. No horse race at primary** | **FAIL** (cond2 ✓) | d ln(w_formal_rung1/w_informal)/d queue pressure = **−0.340** (p<0.001) vs required \|·\|<0.15 (cond1 ✗); d ln(w_rung2/w_rung1)/d pressure = **+4.280** (p<0.01) ✓ | the rung2/rung1 credential ladder *does* rise with queue pressure (the emergent horse race), but the rung1/informal margin is not flat. N.B. the primary rung has `rank_factor == 1` **by construction** — no primary rank competition is a structural restriction, so cond1 is testing a different object (the informal-wage channel) than the architecture's claim. |
| **D. ECI gating** | **FAIL** (cond2 ✓) | interaction Δyos × X = +0.138 (p=0.557); low-X tercile slope **+0.13** pp/yr per year-of-schooling, high-X **+0.56** (ratio **4.31**, high slope significant) | gating is visible in tercile slopes (more than 4×) but the linear interaction with decade FE has no power (n=330 blocks). Gating exists in the mechanism, not in this test. |
| **E. Composition > totals** | **PASS** | twins matched 1970–2021 (cumulative graduates within **1.94%**): growth 2.79 vs 2.11 pp (diff 0.68); queue pressure 0.0002 vs 0.0050 (relative diff **96%**) | same graduate count, different sector mix → different growth and queueing. This is the one behavioural check that passes cleanly. |
| **F. Identity/accounting gate** | **PASS** | GER ∈ [2.91, 105.00]; completion ∈ [2.10, 93.26]; \|Σ sector − 1\| ≤ 2.2e-16; \|Σ occupation shares − 1\| = 0; cohort conservation max rel. err **1.98e-16**; non-negativity OK | the stock–flow bookkeeping is exact. This is the Z1-class gate v0 lacked. |

**Determinism (controller-verified 2026-11-20):** `sim_v1.py` run twice from a clean state produced results CSVs
**byte-identical to each other and to the delivered copies** (`sha256`:
`synthetic_panel_v1.csv` `d27957bef9197c7c0e9513be4644e160eb5d1e2195e7b052a32b5f88e3103a2b`,
`reproduction_checks_v1.csv` `947a2577…`, `reproduction_checks_detail_v1.csv` `a9647d02…`).

### What the failures mean, and what they do not

- The v1 failures are **calibration/identification failures of a declared model**, not empirical findings and not a
  refutation of the user's model. Check B's direction failure says the literacy channel in v1 is too general: it
  pays in the pre-industrial regime rather than specifically enabling takeoff.
- **No re-fitting to pass the checks was done and none should be done post hoc** — the checks were frozen with the
  architecture; passing them by moving parameters after seeing the verdicts would be target-chasing.
- The correct next step is a **v1.1 predeclaration** (new frozen checks, declared parameter changes) that
  (i) re-specifies the literacy channel as a takeoff condition, (ii) fixes the secondary completion ladder without
  per-level rescue, (iii) adds **education → complexity** (user directive, see `MODEL_ARCHITECTURE.md` amendment),
  and (iv) restates check C's primary-margin test to match the architecture's actual restriction. That is a Council
  decision, not a controller one.

## 5. What must not be claimed

No causal claims; no push/pull direction claims; no statement that any real education system "would" behave this
way; no forecast; no policy inference; no "the model shows" — only "the declared model, under these parameters,
produces". Synthetic panel rows are labelled `SYNTHETIC` in every record. Anything tagged DERIVED in the fact
register (e.g. the MYS proxy) is a declared approximation, not an observation.

## 6. Reproduction

```bash
VENV="/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python"
cd generator_v1/code && "$VENV" sim_v1.py            # rewrites ../results CSVs; byte-identical to delivered
cd ../../generator_v0/code && "$VENV" sim.py         # v0 panel + checks
cd ../.. && "$VENV" ../build_package.py . "SYNTHETIC workbench"   # rebuild RUN_MANIFEST.json + SHA256SUMS.txt
shasum -a 256 -c SHA256SUMS.txt
```

## 7. Provenance chain

`MODEL_ARCHITECTURE.md` (user directive) → `equations/` (what the literature actually says) → `facts/` (what may be
reproduced, with provenance labels) → v0 (accounting skeleton) → v1 (layered model, 2/6 behavioural checks pass) →
v1.1 (to be predeclared; education → complexity). Every generated row is `SYNTHETIC`; every claim in this file is
about the generator, not the world.
