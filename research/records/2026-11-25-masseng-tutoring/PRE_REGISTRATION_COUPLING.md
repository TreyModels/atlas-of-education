# PRE-REGISTRATION — coupling the first-pass shadow-education block into MASSENG v5 R1 (PHL)

Written 2026-11-24/25, **before** the coupled grid was executed (the design, switch semantics, grid and decision
rules below were fixed before the 53-config run; the record was committed after the run, as in the repo's
practice). This is a **bounded first-pass coupling prototype**, not a paper. SIMULATION only; no causal claims.

## Question

If the first-pass household shadow-education demand block (branch `research/shadow-equations-2026-11-25` @
`fdc8da0`) is attached to the **actual** PHL massification engine (MASSENG v5 R1, `fit_R1.json`), (a) does the
engine keep working and reproduce its own baseline when the module is switched off, (b) what does the module
change in the massification system (enrolment, progression, credential stocks, household spending), and (c) which
parts of the wider four-piece chain (affordability, learning, gates, jobs) can the engine actually represent?

## Base and branch

- Base: `research/codex-masseng-staging-2026-11-24` @ `bac3a7c`. New additive branch
  `research/masseng-tutoring-2026-11-25` (never rewrite the base).
- Engine: `research/masseng-v6/model/masseng/engine5.py` (the package the committed PHL v5 fit uses). **Not
  modified** — the module is a subclass in a new file `masseng/tutoring.py`.
- Baseline parameters: `outputs/PHL/v5/fit_R1.json` (the "full v5" rival: `b_h, b_p, b_r, lam` + base fit).

## Declared design

1. **Tutoring demand** is the ported four-option MNL (none / own-teacher / other-teacher / commercial) of
   `shadow_model.py` + `bray_reality_check.py`, with the variables the engine cannot carry dropped (individual
   ability, household school-quality draw, own-teacher quality, urban/rural) and school quality replaced by a
   declared level-specific resource proxy.
2. **Learning channel**: no learning-production state exists in v5. Tutoring enters the engine's *existing*
   linear transition index as a declared achievement shift `delta = ln(odds_multiplier) * participation`, added
   to `base[L]` (which feeds the existing within-level progression probability `pc` and level-entry probability
   `pe`). No score equation is invented. `odds_multiplier ∈ {1.05, 1.10, 1.20}`; 1.0 = no learning effect.
3. **Financing channel**: expected tutoring outlay (declared reference fee 3% of GDPpc per tutored pupil-year,
   scaled 0.5/1.0/2.0) enters the engine's existing household burden term `-kappa*log(1+burden)`.
   Because the fitted `c_scale` was matched to FIES *total* household education spending, which already contains
   any shadow-education outlays, this can double count; the financing channel is therefore a separate arm, not
   the headline.
4. **Gate**: v5 R1 has no score bar and no quota. The only limited-places mechanism used is the engine's declared
   public upper-secondary seat-share rule, set to the sourced 2019 SHS public share 0.529. It is a **declared
   supply-share counterfactual, not observed capacity**.
5. **Credential→pay**: absent from v5. Only credential stocks/flows are reported.
6. **Seeds**: MASSENG v5 is deterministic. A "seed" is one draw of the unestimated demand *shape* parameters from
   a declared ±20% band; the single calibrated intercept `b0` is re-solved for each draw to keep the declared PHL
   participation anchor. Seed 0 = the anchor (no shape perturbation). This is parameter uncertainty, not sampling.
7. **Calibration**: exactly one parameter (`b0`) is calibrated to the **mean** of the PHL 2010 survey Grade 6
   (40.7%) and Grade 10 (46.5%) tutoring-participation rates, i.e. 43.6%, at the reference fee. The survey is a
   small purposive sample (De Castro & de Guzman 2010, via Bray & Lykins 2012; 1,235 pupils, 23 schools) and is
   not nationally representative. The two grades are then read as an external check, never as validation.
8. **Demand-mix anchor**: the demand *shape* parameters are the closest-to-Bray draw from the ported six-school
   demand-mix check (50,000 prior draws). That check is Cambodian data and is used only as a demand-mix check.

## Grid (declared)

| arm | fee | own-teacher ban | outlay in burden | learning multiplier | quality proxy | gate |
|---|---|---|---|---|---|---|
| OFF | 1.0 | off | — | — | spend | off |
| main ON grid | 0.5 / 1.0 / 2.0 | off / on | on / off | 1.10 | spend | off |
| learning sensitivity | 1.0 | off | on | 1.0 / 1.05 / 1.10 / 1.20 | spend | off |
| quality robustness | 1.0 | off | on | 1.10 | teacher provision | off |
| gate arm | 1.0 | off | on | 1.10 | spend | public-SHS share 0.529 |
| OFF gate reference | 1.0 | off | — | — | spend | public-SHS share 0.529 |

3 parameter-uncertainty draws per ON cell; 53 runs in total (plus the pristine `Model5` baseline computed in the
same process). Deterministic given seeds; no random numbers enter the engine.

## Acceptance / decision rules (fixed before the run)

- **A1 (hard)** Switch OFF must reproduce `Model5` **bit-for-bit** on a full 1940–2024 run and a short 2000–2024
  run: every array byte-identical, only the added diagnostics key permitted to differ.
- **A2** The module must be monotone where the ported equations imply it: participation falls with the fee;
  removing the own-teacher option lowers participation and zeroes the own share.
- **A3** Reality check has three declared comparisons, each reported pass/fail:
  (i) PHL held-out fit consistency (retrospective/inspected data — **not validation**): three-GER and per-series
  held-out RMSE change vs the untouched R1 baseline;
  (ii) Bray six-school patterns as a **demand-mix check only**, not PHL validation;
  (iii) PHL 2010 tutoring participation by grade as an external survey check, not reused for calibration.
- **A4** No causal language; every parameter that is not estimated is labelled declared; every mechanism the
  engine cannot represent is listed, not invented.

## Stop rules

If the switch-off identity fails, or the demand/financing links cannot be made with engine-internal objects
without inventing a module (score gate, labour market, rural/urban), report the boundary and stop rather than
fabricate the link.
