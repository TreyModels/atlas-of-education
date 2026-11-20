# RESULTS BRIEF 003 — FINAL results adjudication (E18b, E13c, batch B, E21)

- **sent by / date:** lead, 2026-11-20 ~13:00 Asia/Shanghai
- **purpose:** adjudicate the *final* numbers (all of which landed after brief 002) and sign off the
  report's claim/withdraw language. Brief 002 saw only the provisional E13b and no E18b.
- **what this informs:** the final `SUMMARY_FOR_TREY.md` and what may go to Bjørn.
- **follow-up cycle expected?** no — this is the closing adjudication.

## 1. Artifacts (all executed, all in the package)

| artifact | path | status |
|---|---|---|
| Plain-language report (current draft) | `SUMMARY_FOR_TREY.md` | draft, needs your sign-off |
| Batch A records incl. E18b, E13c, E21 | `05_experiments/EXPERIMENTS.md`; `runs/{E18b,E13c,E21}/findings.txt` | completed |
| Batch A summary table | `05_experiments/SUMMARY_TABLE.csv` (17 rows, 15 completed) | completed |
| Batch B records | `05b_experiments/EXPERIMENTS_B.md`; `runs/{B1,B2_B3,B4,B5}/findings.txt` | completed |
| Batch B summary | `05b_experiments/SUMMARY_TABLE_B.csv` (188 estimate rows) | completed |
| Manifests | `RUN_MANIFEST.json`, `05_experiments/RUN_MANIFEST.json`, `05b_experiments/RUN_MANIFEST_B.json` | completed |
| Council briefs 001/002 | `08_council/brief_001/`, `brief_002/` | completed |

## 2. Final claims table (replaces brief 002's C10/C17 rows)

| ID | claim | type | key numbers | verdict requested |
|---|---|---|---|---|
| F1 | **Graduate-supply claim survives as formal-access**, not absolute income | simulation | surplus Δformal\|dip −0.1511 (0.0217); level-matched rival +0.0085 / +0.0095 / −0.0054 at σ=0.5/1/2; Δincome rival +0.125 at σ=2; degree income matched only at σ=2 (2.706 vs 2.926) | ESTABLISHED (conditional), SIMULATION-ONLY? |
| F2 | E13b's income contradiction was a **level artefact**; B1's σ=0.5 firing corner is numerically unstable (baseline ratio 0.022–0.055, degree income 1.0–42.4 across seeds) | simulation | B1: σ=1.0 −0.010/−0.015 (noise); σ=2.0 +0.042/+0.070 | consistent with F1? |
| F3 | **E18b: C10 withdrawn — substitution appears** when support damps tutoring's marginal value | simulation | paid spend vs ban-only: −1,291.5 (2sd 92); targeted −341.4 (2sd 149); capacity-capped −1,241.2 (2sd 101); completion equal/higher | correct to withdraw? is the linear-damping substitution channel fair, or a best-case construction? |
| F4 | Therefore the **Double Reduction direction is unidentified**: additive/universal support intensifies the race (+18% spend), substitutive support crowds it out | simulation | E18 +723; E18b −1,291 / −341 / −1,241 | what may the paper say about China? |
| F5 | Floor/race at 4 reps: floor's persistence contribution ≤ seed noise; ranking → intensification; allocation knockout mixed (only lottery distinguishable) | simulation | ranked −0.039/−0.064/−0.049; unranked +0.151/+0.036/+0.630; B3 cutoff+random +0.037 (n.s.) | is the floor/race decomposition still the paper's strongest plank? |
| F6 | Long-run massification requires a supplied trend in this model class | simulation | EXO entry 0.22→0.55; ENDO 0.404→0.020; smoothed 0.218→0.108 | does this undercut the massification claim? |
| F7 | External benchmark: PH model levels roughly right, **shape wrong** | simulation vs observed | PH primary MAE 3.4 pp, secondary 12.6, tertiary 5.4; corr −0.33/−0.40; Korea preset tertiary 41.0 vs 93.7 | what may be claimed for the Philippines? |
| F8 | Batch B5: detailed domestic reader dominates on error but **certification demand falls** (predeclared half-claim contradicted); foreign-recognition sign is a parameter artifact | simulation | error 0.045 vs 0.411; certification demand 0.062 vs 0.217; foreign coverage +0.105 | keep or withdraw the information claim? |

## 3. Rivals

- **Matched-elasticity competitive CES** (level-matched in E13c): it wins on absolute income and loses
  on formal access. **Yoo (2003)**: wins on the bar sweep. **GXL (2017)**: competes on actor/pipeline
  results. The key question for you: is the formal-access margin a *fair* discriminating outcome, or
  does it survive only because the rival world hires by productivity and therefore has no rationing?

## 4. Questions to the Council (≤6)

1. **F1/F2:** Does the level-matched formal-access claim survive scrutiny, given degree income could be
   matched only at σ=2 and the E13b/B1/σ=0.5 corner is unstable? Exact language you would sign off on?
2. **F3:** Is the linear-damping substitution channel a fair test, or a best-case construction for
   Trey? Should E18b's "C10 withdrawn" stand, or is the honest verdict "unidentified"?
3. **F4:** What may the paper say about China/Double Reduction now — one sentence, with its caveat?
4. **F5/F6:** Is the floor/race decomposition still the strongest plank, and does F6 (supplied trend)
   require withdrawing any massification trajectory claim from the paper?
5. **F7:** The PH model misses the shape of the observed expansion but gets levels roughly right. What
   is the defensible claim, and what must be labelled uncalibrated?
6. **Closing:** give the final publishable claim, the final withdrawal list, and the 3 experiments that
   would most raise credibility (arms/estimand/threshold/cost). This is the sign-off.

## 5. Known limitations

- Degree-income level-matching only at σ=2 (E13c); B1 not blind; E14/E15/E19 pilot-strength reps.
- E18b's substitution channel is a declared linear damping, not an estimated CES.
- E21 uses observed cells only but harmonises three UIS/WDI layers; no calibration was done.
- Hong Kong data blocked; no atlas-engine cells ran (batch C is starting them now).
- All experiment numbers are simulated; none is causal evidence.

## 6. Out of scope

- `01_sources/`, `fleet.nosync/`, `00_handoff/papers/` beyond orientation.

## 7. Budget

- **deadline:** ~15 minutes.
- **output:** reviews + deliberation + synthesis; synthesis ≤900 words.
- This is the **closing sign-off**: no further cycle is expected.
