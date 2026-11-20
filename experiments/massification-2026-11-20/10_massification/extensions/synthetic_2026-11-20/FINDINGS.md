# FINDINGS — synthetic-data workbench (v0 + v1)

> **SYNTHETIC. Everything this workbench generates is a declared-assumption simulation, not evidence,
> not an estimate, not a forecast, and not a model of any real country.** No causal or push/pull
> direction claim is licensed by anything below. Country labels are synthetic (`SYN00_PHL_LIKE` etc.).
> The only observed numbers encoded anywhere are the declared targets listed in
> `generator_v1/RUN_MANIFEST.json` (`targets_encoded`) and in `facts/`.

**Built:** 2026-11-20. **Status:** v0 DONE; **v1 DELIVERED (authoritative)** — 6 predeclared checks:
**A PASS but target-encoded · B FAIL · C PASS (half structural) · D PASS · E PASS · F PASS.** The
authoritative v1 supersedes an earlier intermediate run of the same day whose checks read A–D FAIL / E–F PASS;
the earlier run's numbers are withdrawn (see `generator_v1/TUNE_LOG.md` for the full audit trail of what changed
between them and why). Recorded here because two versions must not coexist: the arbiter for v1 is the worker's
hash list, which the controller re-verified (two clean re-runs byte-identical; §6).

---

## 1. What the workbench contains

| component | what it is | size |
|---|---|---|
| `MODEL_ARCHITECTURE.md` | the user's verbal specification restated as a layered design directive (+ dated amendments A1: education → complexity) | 95 lines + amendments |
| `equations/EQUATION_REGISTER.csv` | every equation/relationship in the programme's massification literature layer, with status, form, parameters, implementation site | **43 rows**; 10 tagged `equation-in-literature` (candidate/definition forms included), the rest `narrative-only`, `programme-invented` or `programme-estimated` |
| `facts/STYLIZED_FACTS.csv` | the provenance-labelled facts a generator may reproduce | **53 facts**; 35 VERIFIED-FROM-DISK, 6 SIMULATED, 5 DISPUTED, 4 MODEL-OUTPUT-NOT-FACT, 3 REPORT-ONLY-UNRELIABLE (+ the completion/GER measurement note added 2026-11-20) |
| `generator_v0/` | arithmetic skeleton: demand-ceiling + capacity gate + law push, one declared PHL-like country | 32 synthetic countries × 55 years (1970–2024) × 4 levels = **7,040 rows**; `FINDINGS.md`, `PARAMS.md`, `results/` |
| `generator_v1/` | layered, tiered, occupation-aware generator (takeoff regime, sector mix, job ladder, rank/queue matching, composition growth) | 30 synthetic countries × 56 years (1970–2025) × 4 levels = **6,720 rows**; `FINDINGS.md`, `TUNE_LOG.md`, `PARAMS.md`, `RUN_MANIFEST.json`, `code/sim_v1.py`, `results/` |

Both generators use one seeded NumPy `PCG64` stream (seed 20261120), read no observed data at runtime, and write
fixed-precision CSVs so reruns are byte-identical.

## 2. v0 — arithmetic skeleton (DONE)

v0 establishes the flow/stock accounting: logistic demand ceiling, capacity gate `K^0.75`, a 0/1 law push, the
cohort-flow identity, and a declared `PHL_like` country pattern-matched to the brief (not fitted to observed
Philippine series). It discloses two failures rather than hiding them:

1. **C5b cross-level ladder** — primary ≥ lower ≥ upper ≥ tertiary completion holds in only **69.89%**
   (1,230/1,760) of country-years (530 violations; pairwise 86.82% / 93.52% / 84.38%). The ordering is not
   enforced by construction in v0.
2. **Within/between conflation** — v0's one demand relation does not separate within-country dynamics from
   cross-country level differences.

## 3. v1 — what it implements and what its predeclared checks say (authoritative)

Layers as in `MODEL_ARCHITECTURE.md`: Layer 0 economy states (complexity-like `X`, income, urbanisation, sector
mix, four formal job rungs, three takeoff states); Layer 1 cohort-flow schooling supply (GER ≤ 105, completion
from the cohort flow with a duration lag); Layer 2 rank-based absorption into formal rungs vs the informal
residual, with queueing; Layer 3 composition-weighted growth; Layer 4 synthetic panel + check table. Declared
country set includes a PHL-like economy and a matched twin pair differing **only** in sector mix.

| check | verdict | key numbers (synthetic) | reading |
|---|---|---|---|
| **A. PHL signature** | **PASS — but target-encoded** | primary first ≥90 **2017**; lower-sec first ≥90 **2024** (2023 = 87.2); upper-sec never ≥90, max **75.1**, 2024 = 75.1; tertiary GER **15.3 → 50.3** (1971→2025); floor→middle gap **7 y**; ceiling residual **14.9 pp** | the PHL-like country's four level-specific supply paths (survival + seat capacity) are **interpolated through the declared PHL-01/02/03 anchors**. A1/A2/A3/A4(1971) are therefore produced by the encoding, **not predicted**, and the architecture's "one parameterisation, no per-level rescue" clause is **NOT met**. Emergent: A5 (7 y gap), A6 (14.9 pp residual), the tertiary 2025 endpoint, the never-crossing, and that one path set yields all six together. |
| **B. Literacy vs schooling-years horse race** | **FAIL (2 of 3 conditions)** | pooled decade-FE n=180: `b_lit` = **+2.37** (p<1e-4), `b_yos` = **+0.26** (p<1e-4); takeoff ablation `b_lit` = **+2.29**; full job-ladder ablation `b_lit` = **+2.10** | the headline pattern holds and schooling-years is weak ✓✓, but the association **survives the removal of its own mechanism** (condition B3 fails). The pattern is over-determined and **not diagnostic** of the takeoff/occupation structure. In the pre-industrial subsample literacy–growth is *positive* (+1.75), while within industrialising/diversified it is slightly negative (r = −0.15). |
| **C. No horse race at primary** | **PASS (half structural)** | primary-margin return vs queue pressure = **−0.485** (with literacy control); credential ladder `w_rung2/w_rung1` vs pressure = **+4.757** (p<1e-6); without the literacy control the primary margin falls (−0.495) | no *positive* rank premium at the primary margin, and the lower-secondary+ ladder does widen with queue pressure. Caveat: the rung-1 rank factor is 1.0 **by construction**, so the flatness is a design restriction, not an emergent result; the negative number without the control is the informal-productivity channel, not a rank premium. |
| **D. ECI gating** | **PASS** | counterfactual +10 % schooling push: Δgrowth per unit X(1980) = **+0.022 pp** (p = 5.8e-8); high-X tercile **+0.029 pp** vs low-X **+0.005 pp** (ratio **6.2**) | a schooling push buys ~6× more growth where the higher rungs exist. Tested as an experiment (the architecture's own wording), not as an unstable panel interaction. |
| **E. Composition > totals** | **PASS** | twins matched 1970–2025 (cumulative graduates within **1.41%**): growth **3.10 % vs 2.50 %** (diff 0.60 pp); queue pressure **0.0001 vs 0.0028** (95 % apart) | same graduate count, different sector mix → different growth and queueing. The one controlled comparison that passes cleanly. |
| **F. Identity/accounting gate** | **PASS** | GER ∈ [2.83, 105.0]; completion ∈ [2.10, 95.11]; \|Σ sector − 1\| ≤ 2.2e-16; \|Σ occupation shares − 1\| = 0; cohort conservation max rel. err **2.05e-16**; non-negativity OK | exact stock–flow bookkeeping (the Z1-class gate v0 lacked). |

## 4. What is load-bearing — and why v1 is a demonstration, not a test

The worker's audit trail (`generator_v1/TUNE_LOG.md`) and ablation results converge on one uncomfortable finding:

- **The upper-secondary seat cap is load-bearing.** Set the cap at 0.845–0.875 and the ceiling is arithmetically
  incapable of crossing 90 whatever the floor does; put the ceiling on the *same growth path* as the floor
  (0.58 → 1.00, as lower-secondary has) and the anchor asymmetry disappears entirely. Nothing else — not the
  queue, the rank premium, the takeoff switch or the sector mix — is close in power.
- **But the seat cap is stipulated, not derived** (from CAP-04 "capacity buys the floor, not the ceiling", which the
  fact register itself labels a model-side ruling the data cannot separate at n = 6). So the honest statement is:
  **v1 reproduces the asymmetry substantially by assuming the asymmetry.** The second most load-bearing object is
  the declared PHL floor survival path, which is interpolated through the anchors and therefore target-encoded.
- **The rung ladder is not load-bearing for the level association** (check B's ablations) but *is* load-bearing for
  the marginal return (check D). Both can be true; together they are the most useful output: the ladder governs the
  **marginal return** to more schooling, not the **level** association between literacy and growth.
- **A synthetic horse-race PASS is non-diagnostic unless the ablation fails** — adopted as a standing rule for v1.1.

## 5. A real measurement insight produced by the exercise (recorded to the fact register)

The generator cannot produce completion above gross enrolment: in a cohort-flow identity, completion is a share of
the **entering** cohort and can never exceed the entering GER (v1 tops out at 94.0 primary / 90.4 lower-secondary).
But the observed Philippine series does exceed it — verified from disk (`10_massification/data/
UNIVERSALIZATION_SERIES.csv`, `data/gmr_observed_6countries_1970_2024.csv`, 2024): **primary completion 98.30 on
GER 94.03; lower-secondary completion 92.41 on secondary GER 85.29; upper-secondary completion 75.03.** The
coherent explanation is that the UIS completion rate is measured on children **3–5 years above grade age**, not on
the GER age band — i.e. it is a different denominator, not a different reality.

Consequence for the whole programme: **"universalisation" is measure-dependent.** GER-based and completion-based
crossing dates are not interchangeable (the ambiguity `facts/MUST_REPRODUCE.md` R2 flags), and any completion/GER
ratio comparison in the programme must state which denominator it uses. This also explains part of the old model's
over-scale GER artefact. Recorded in `facts/STYLIZED_FACTS.md` §12 and `10_massification/data/
DATA_NOTES_MASSIFICATION.md`.

## 6. Verification at packaging (controller, 2026-11-20)

- Authoritative v1 file hashes re-verified against the worker's list: `sim_v1.py` `a03fa0cb…`, `PARAMS.md`
  `9052e85b…`, `FINDINGS.md` `9f6569e6…`, `TUNE_LOG.md` `730f6c4e…`, `RUN_MANIFEST.json` `f9e3640e…`,
  `synthetic_panel_v1.csv` `cf8dfbcb…`, `reproduction_checks_v1.csv` `0914e3c7…`,
  `reproduction_checks_detail_v1.csv` `fcbc7255…`.
- Two fresh runs of `sim_v1.py` into separate output directories: **byte-identical to each other and to the
  delivered CSVs** (`cmp` on all three results files).
- No observed data file is read at runtime; every output row carries `label = SYNTHETIC`.

## 7. What must not be claimed

No causal claims; no push/pull direction claims; no statement that any real education system "would" behave this
way; no forecast; no policy inference; no "the model shows" — only "the declared model, under these parameters,
produces". Check A is target-encoded and must never be quoted as a successful prediction. Check B's headline pattern
is non-diagnostic. `mys_proxy`-style derived proxies are labelled where used.

## 8. Reproduction

```bash
VENV="/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python"
cd generator_v1/code && "$VENV" sim_v1.py            # rewrites ../results CSVs; byte-identical to delivered
cd ../../generator_v0/code && "$VENV" sim.py         # v0 panel + checks
cd ../.. && "$VENV" ../build_package.py . "SYNTHETIC workbench"   # rebuild RUN_MANIFEST.json + SHA256SUMS.txt
shasum -a 256 -c SHA256SUMS.txt
```

## 9. Provenance chain and v1.1 requirements

`MODEL_ARCHITECTURE.md` (user directive) → `equations/` (what the literature actually says) → `facts/` (what may be
reproduced, with provenance labels) → v0 (accounting skeleton) → v1 (layered model; A target-encoded, B
non-diagnostic, C structural, D/E/F genuine) → v1.1 (to be predeclared).

**v1.1 predeclaration must** (a) add the **education → complexity** channel (schooling flow raises `X` with a 5–10 y
lag, so `X` is not only a function of income/urbanisation); (b) **remove the per-level PHL anchor interpolation** so
the "one parameterisation, no per-level rescue" clause is actually tested; (c) state that a synthetic horse-race
PASS is **non-diagnostic unless the ablation fails**; and (d) derive the upper-secondary seat capacity from the
economy side (who hires upper-secondary completers) rather than stipulating it. That is a Council decision, not a
controller one.
