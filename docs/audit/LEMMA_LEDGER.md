# LEMMA LEDGER — claim-by-claim Lean map (Atlas verification prototype)

**Owner:** `audit-runner` · **Date:** 2026-11-25 · **Host-only** (no box use)

**Machine-readable companion:** [`LEMMA_LEDGER.csv`](LEMMA_LEDGER.csv) (one row per `paper_claims.csv` claim).
**Lean source:** [`verification/lean/Atlas/Claims.lean`](../../verification/lean/Atlas/Claims.lean) (18 Lead-scoped claims, one declaration group each). **Baseline:** [`results/audit/paper_claims.csv`](../../results/audit/paper_claims.csv) (132 rows, committed).

**Binding rule:** *Lean proves the reference mathematics and the accounting/inventory identities; the Python engine is differential-tested against Lean witnesses on fixtures; numerical results remain reproducible-artifact evidence. This is not "the engine is verified".*

**No silent `sorry`:** this project contains **0 `sorry`s**. Claims that cannot be theorems are `EmpiricalClaim`/`SpecClaim` records (statement + artifact hashes + status), never asserted. Unproved ≠ false; empirical ≠ theorem. CI runs `grep sorry` and `#print axioms`.

## Scope of this ledger generation

- **Declared now:** 18 Lead-scoped claims — A-34…A-39, B-41…B-44, C-01…C-04, D-01…D-04.
- **Explicit NOT-YET-LEMMATISED:** 114 of the 132 baseline rows (listed individually below with their ids — no silent omissions).
- Extension plan: next pass adds the remaining rows in paper order; the four-kind schema and status vocabulary are stable, so adding a row is one declaration + one ledger row.

## Four statement kinds

| kind | meaning | Lean encoding | examples |
|---|---|---|---|
| 1 definition | model objects; units/domains stated; no partial functions | `structure`/`def` in `Atlas/Definitions.lean` | `Cohort`, `Gate`, `seatCount`, `Budget`, `TaxLedger`, `PrepStock`, `EqState` |
| 2 theorem | identities and finite PL math, proved | `theorem` in `Atlas/Identities.lean`, `Atlas/PlackettLuce.lean` | `budget_ledger_identity`, `prep_recursion_closed_form`, `pl_top1_sum_eq_denom`, `pl_topK_selected_sum` |
| 3 computational | numeric claims as exact re-encodings, `decide`-checked; or spec + differential contract | `theorem … := by decide` and `SpecClaim` records in `Atlas/Claims.lean` | `A34_arithmetic`, `A38_anchor_infeasible`, `B41_*`, `B42_*`, `A37_spec`, `A39_spec` |
| 4 omission/independence | inventory equation invariant to each omitted channel; recorded contradictions as `¬` | `theorem … := rfl` / `¬` in `Atlas/Claims.lean` | `classical_demand_ignores_school_supply` … `_supply_form`; `D02_paradox_not_universal` |

Counts (declared rows): 3 computational = 4, empirical (hypothesis) = 6, 4 omission/independence = 1, spec (differential contract) = 6, 2 theorem = 1.
Status counts: `computationallyChecked` = 4, `hypothesis` = 6, `proved` = 2, `specified` = 6.

## Declared claims (18)

| claim | paper | kind | status | Lean declaration | claim (short) | note |
|---|---|---|---|---|---|---|
| A-34 | A | 3 computational | `computationallyChecked` | `A34_arithmetic (+ A34_empirical hypothesis)` | E8 abolition-year impact ATT(e=0) replicates on fresh hashed WDI (simple DiD): +12.322 pp vs author +12.44; F… | exact milli-pp tolerance check proved; empirical estimate is a data hypothesis |
| A-35 | A | empirical (hypothesis) | `hypothesis` | `A35_empirical` | E8 post-abolition amplification REPLICATES under CS-style group-time ATT on fresh WDI: post mean e=+1..+6 = +… | CS-style ATT numbers are data, not theorem |
| A-36 | A | empirical (hypothesis) | `hypothesis` | `A36_empirical` | Delayed secondary-bulge t* jump: fresh-WDI ATT at t* = -0.956 pp, post +0.30, Fisher p 0.251/0.384 -> no dete… | no-effect evidence (UNRESOLVED) |
| A-37 | A | spec (differential contract) | `specified` | `A37_spec` | Fee-abolition forecast (Exp 5, run e) rerun on fixed engine: abolition - persistence +17.19,+20.97,+23.37,+25… | simulation forecast: specification + differential-test contract |
| A-38 | A | 3 computational | `computationallyChecked` | `A38_anchor_infeasible` | Author's pre-abolition calibration anchor 74.88% is infeasible in the repaired world under a training-only ca… | infeasibility arithmetic in exact units |
| A-39 | A | spec (differential contract) | `specified` | `A39_spec` | Item (d) multi-seed identifiability Jacobian (frozen V540-FREEZE 4 theta x 4 moments): rank 4/4, null dim 0 a… | rank/nullity exact-matrix computable; SV/conditioning floats are artifact evidence |
| B-41 | B | 3 computational | `computationallyChecked` | `B41_HK_meets_criterion, B41_KR_TRACKED_meets_criterion, B41_KR_SINGLE_meets_criterion` | New-generation CF4a meets the pre-stated both-jurisdiction Win-Win (spend<80 AND elite Q5 below baseline): HK… | Win-Win accounting criterion proved for cited cells; welfare interpretation unproved |
| B-42 | B | 3 computational | `computationallyChecked` | `B42_CF4b_fails_spend_HK, B42_CF1b_fails_spend_HK, B42_CF3b_passes_both` | New-generation CF4b fails spend (89.99 HK / 109.70 KR-TRACKED / 117.74 KR-SINGLE), CF1b fails spend (97.25 / … | accounting values falsify the 'only pairing works' reading |
| B-43 | B | spec (differential contract) | `specified` | `B43_spec` | Provenance/correction: earlier new-gen JSONs (14fc2a31 / 697e7ca9 / cba8ee0f) had an EMPTY HK summary because… | provenance/hash-chain correction; not a mathematical proposition |
| B-44 | B | spec (differential contract) | `specified` | `B44_spec` | Substantial participation reduction under CF4a/CF3b (K-12 -13.33 pp HK / -12.98 pp KR under CF4a; G12 -10.23 … | participation deltas accounting; welfare caveat not formalizable from current data |
| C-01 | PROGRAMME | empirical (hypothesis) | `hypothesis` | `C01_empirical` | Paper C provisional anchor: Paper B canonical spec is a private-market regime - withheld h=0.00000 in HK/KR, … | provisional anchor, design-only |
| C-02 | PROGRAMME | empirical (hypothesis) | `hypothesis` | `C02_empirical` | Paper C provisional anchor: better school provision substitutes - q0 0.8->1.2 lowers K-12 tutoring participat… | provisional anchor, design-only |
| C-03 | PROGRAMME | empirical (hypothesis) | `hypothesis` | `C03_empirical` | Paper C provisional anchor: withholding regime (pay_ratio=.55, monitoring=.2, own_ban=0) -> h=0.144, own shar… | provisional anchor, design-only |
| C-04 | PROGRAMME | spec (differential contract) | `specified` | `C04_spec` | Paper C confirmatory grid (3 S x 3 L x 4 supply = 36 cells + 4 regime anchors; N=600/T=46 screening ~320 runs… | design cells + prereg requirement; no run yet |
| D-01 | PROGRAMME | 4 omission/independence | `proved` | `classical_demand_ignores_school_supply, ..._positional_seats, ..._withholding, ..._time_budget, ..._supply_form` | Paper D omissions M1-M5 (school-supplied prep S; positional fixed seats; teacher withholding/rent; student/te… | five omission/independence lemmas proved by definitional invariance |
| D-02 | PROGRAMME | 2 theorem | `proved` | `D02_paradox_not_universal` | Already-recorded contradictions (KR G9 phantom prize; expected!=realised admission; 100% seat-expansion parad… | contradiction-pattern illustration in a toy encoding; real record is artifact evidence |
| D-03 | PROGRAMME | spec (differential contract) | `specified` | `D03_spec` | Paper D divergence tests D1-D9: standard-equation prediction X vs mechanism-rich prediction Y, cell/outcome/c… | pre-registerable divergence tests, not results |
| D-04 | PROGRAMME | empirical (hypothesis) | `hypothesis` | `D04_attribution` | Inventory is an AI-generated candidate map with placeholder citations ('UIS+2', 'OECD+3', 'doi.org+4', etc.) … | citation/attribution risk is not a mathematical proposition; declared as an empirical hypothesis record, never a theorem |

## Not-yet-lemmatised claims (114)

These rows have **no Lean declaration yet** by design — explicit entries so the QA check has no silent gaps. Status: `NOT-YET-LEMMATISED`; paper claims' own evidence status is preserved in the baseline (`results/audit/paper_claims.csv`).

| claim | paper | baseline status | claim (short) |
|---|---|---|---|
| A-01 | A | VERIFIED EMPIRICAL | E8 abolition-year primary-GER ATT = +12.44 pp |
| A-02 | A | VERIFIED EMPIRICAL | E8 post mean +25.26 pp; event range +22.12..+28.56 pp (e=+1..+6) |
| A-03 | A | VERIFIED EMPIRICAL | Fisher RI p=.0001 placebo-date; p=.0003-.0006 placebo-country; 20,000 permutations |
| A-04 | A | VERIFIED EMPIRICAL | Gender differential D=-3.94 pp, 95% CI [-8.72,+0.29]; no detected sex difference |
| A-05 | A | CONTRADICTED | Flat pre-trends (-0.03,-0.13) and a clean -6-year placebo (-0.39) |
| A-06 | A | CONTRADICTED | Gender non-detection robust to inverse-variance weighting and leave-one-out; 'lifting boys and girls alike' |
| A-07 | A | AUTHOR-REPORTED | Exp 1 live-WDI t* bulge-arrival test: 7,290 obs; 2,500 permutations/scheme; honest null |
| A-08 | A | AUTHOR-REPORTED | 'These nulls prove aggregate WDI indicators lack resolution' / 'prove too coarse' |
| A-09 | A | AUTHOR-REPORTED | Exp 3: 1,640 matched runs; H2 fee x scarcity +0.1086 (CI +0.0924,+0.1248; p=1.9e-11); quota -0.0145 |
| A-10 | A | AUTHOR-REPORTED | Exp 3 provenance: base_commit 68da16e |
| A-11 | A | AUTHOR-REPORTED | Exp 3: H1 +0.3430 (Spearman -1.00); contest 2x2 +0.2013; inverted-U +0.0138/+0.1865/+0.2573/-0.0232; Table 2/Figure 2 |
| A-12 | A | AUTHOR-REPORTED | Central mechanism: fee abolition amplifies Q5-Q1 gap only under a Tullock contest gate |
| A-13 | A | AUTHOR-REPORTED | Exp 4: five independent aggregate moments; 7-param rank 5/7 cond 1.09e13; 10-param rank 5/10 cond 3.48e12 |
| A-14 | A | CONTRADICTED | The archived 10-parameter Bray ABC supports the identification claim |
| A-15 | A | AUTHOR-REPORTED | Null vectors isolate b_income (loading -0.977) and b_school_gap (-0.959) |
| A-16 | A | AUTHOR-REPORTED | Adding income micro-moments -> rank 6/7 (cond 3435.49); plus quality -> full rank 7/7 (cond 43.81) |
| A-17 | A | CONTRADICTED | 'Proves a formal structural identifiability theorem' / 'achieving full structural identification' |
| A-18 | A | CONTRADICTED | Posterior correlation condition number 447.16->23.97->8.05 as identification evidence |
| A-19 | A | AUTHOR-REPORTED | Three exact collinearities; 7-param bijection; acceptance 0.0063%->0.0192%; fresh-seed failure 58/54/53%; max\|z\| 1.1214->0.6091 |
| A-20 | A | CONTRADICTED | Synthetic Bray DGP supports the identification claim |
| A-21 | A | AUTHOR-REPORTED | Exp 5: 7-horizon RMSE 5.13/4.68 vs persistence 23.93; reduction 78.6%/80.5% |
| A-22 | A | AUTHOR-REPORTED | Exp 5 on-impact predictions +11.60/+13.48 bracket empirical +12.44 |
| A-23 | A | AUTHOR-REPORTED | Calibration: fee_public=0.150 selected on 74.88% pre-abolition GER; zero post fitting |
| A-24 | A | AUTHOR-REPORTED | Table 1 as empirical vs out-of-sample mechanistic validation |
| A-25 | A | AUTHOR-REPORTED | Simulator 'validates a mechanistic education-system simulator out-of-sample' |
| A-26 | A | AUTHOR-REPORTED | Table 3 Q1 exit decomposition (never/liquidity/choice/gate-fail; e.g. open_bar never 74.07->1.70) |
| A-27 | A | AUTHOR-REPORTED | Roughly 70% of Q1 exits liquidity; fewer than 1% gate failure |
| A-28 | A | AUTHOR-REPORTED | Fee abolition collapses Q1 non-entry 72-74 pp; tight quota gate-fail +10.39 pp; gap +8.82 vs +3.11 pp |
| A-29 | A | AUTHOR-REPORTED | Engine limitation: max_entry_age=9, zero repetition, GER capped near 98% vs 106.9% |
| A-30 | A | AUTHOR-REPORTED | Within-gate equifinality: 319,600 pairs, 176 collisions vs null mean 190.52, p=.838 |
| A-31 | A | UNRESOLVED | Author Note: open replication code/pre-registrations/audit logs archived at TreyModels/atlas-of-education |
| A-32 | A | CONTRADICTED | Archived GPU/ABC bundle can support identifiability/micro-moment claims |
| A-33 | A | CONTRADICTED | E1/Q3 robustness inference from the pooled/bootstrap selftest (declared bundle; not in received manuscript) |
| B-01 | B | AUTHOR-REPORTED | Design: 14 arms, 420 runs, 30 matched seeds, N=400, T=70 |
| B-02 | B | AUTHOR-REPORTED | Table 1 structural parameters: S=0.23 HK; S12=0.12 KR; fail='track'; own_teacher=False; higher KR delta-V |
| B-03 | B | AUTHOR-REPORTED | HK Grade-9 participation 53.8% exact match |
| B-04 | B | AUTHOR-REPORTED | HK Grade-12 participation 71.6% vs 71.8%; ramp +17.8 vs +18.0 |
| B-05 | B | AUTHOR-REPORTED | KR overall K-12 participation 76.5%, inside 75.7-78.5 corridor |
| B-06 | B | AUTHOR-REPORTED | KR Q5-Q1 gap 34.1 vs published +32.1 (84.9 vs 52.8) |
| B-07 | B | AUTHOR-REPORTED | KR Q5/Q1 spend ratio 3.19 vs published 3.4 (662k vs 192k KRW/mo) |
| B-08 | B | CONTRADICTED | Table 2 'Published Target'/'Source' attributes 32.1 pp and 3.4x to SeoulStart and calls them published/observed |
| B-09 | B | AUTHOR-REPORTED | Participation stood at 78.5% in 2023 and 75.7% in 2025 |
| B-10 | B | AUTHOR-REPORTED | HK benchmarks 53.8% (G9) / 71.8% (G12), 2011/12 survey |
| B-11 | B | AUTHOR-REPORTED | Table 3 HK 7-arm counterfactual table |
| B-12 | B | AUTHOR-REPORTED | Table 4 KR 7-arm counterfactual table |
| B-13 | B | AUTHOR-REPORTED | Figures 1-4 match handoff numbers |
| B-14 | B | CONTRADICTED | Finding 1: +50% tutoring tax backfires on spending and equity (+4.8% HK; +7.4% KR; elite 34.2%/26.0%) |
| B-15 | B | CONTRADICTED | Finding 1b: Q5/Q1 ratio jumps 11.83->16.85 (HK) and 3.19->4.13 (KR) |
| B-16 | B | CONTRADICTED | Finding 1c: Q5 elite share rises 30.0->34.2 (HK) and 24.6->26.0 (KR) |
| B-17 | B | REPRODUCED SIMULATION | Finding 2: seat expansion raises Grade-12 participation (CF2a KR +10.2 pp; CF2b 97.1/99.6) |
| B-18 | B | REPRODUCED SIMULATION | Finding 2b: seat expansion raises spend (+73.8% HK; +22.3% KR CF2b) |
| B-19 | B | CONTRADICTED | Finding 2c: seat expansion lowers Q5 elite share in both jurisdictions |
| B-20 | B | CONTRADICTED | Finding 2d: model reproduces the 2024 medical-seat shock; P(1-P) peak at S=0.50 |
| B-21 | B | CONTRADICTED | Finding 3: CF1b is the only single lever in the Win-Win quadrant |
| B-22 | B | CONTRADICTED | Only pairing wage compression with caps/seat expansion reaches the Win-Win frontier |
| B-23 | B | CONTRADICTED | Finding 3c: wage compression deep spend cuts but raises Q5 elite capture (36.3%/27.5% CF3b) |
| B-24 | B | CONTRADICTED | Finding 3d: effort caps broaden participation (K-12 51.1% HK / 86.0% KR) |
| B-25 | B | CONTRADICTED | Every lever produces identical dynamics / the exact same policy hierarchy |
| B-26 | B | CONTRADICTED | Conclusion: 'calibrated across 420 matched simulation runs ... demonstrates' |
| B-27 | B | AUTHOR-REPORTED | 2024 Korean medical-seat episode: 2,000 seats; KRW 29.2tn; 161,784 repeaters (31.0%) |
| B-28 | B | AUTHOR-REPORTED | 27% of parents cite private education costs as a fertility driver |
| B-29 | B | AUTHOR-REPORTED | 0.00% K-12 liquidity dropout presented as universal-K-12 calibration match |
| B-30 | B | AUTHOR-REPORTED | Simulated elementary 74.8% vs G9 89.3%, published Korean surveys ~86% |
| B-31 | B | AUTHOR-REPORTED | HK pure-contest Q5/Q1 ratio 11.83x steeper than surveys |
| B-32 | B | AUTHOR-REPORTED | 30 matched seeds eliminate Monte Carlo sampling noise |
| B-33 | B | CONTRADICTED | Review section 4: the 540 design lost the Korean calibration (gap 68.36 vs 32.1; ratio 18.01 vs 3.4) as a parameterisation failure |
| B-34 | B | CONTRADICTED | The 540 design is calibrated / recovers the benchmarks |
| B-35 | B | REPRODUCED SIMULATION | Pre-repair 540 CF4 verdict: CF4a fails HK equity (48.64>46.36); CF4b fails spend (90.88/88.04); only CF1b passes |
| B-36 | B | REPRODUCED SIMULATION | Repaired 540 CF4a is Win-Win in both jurisdictions (HK 70.58/23.44; KR 72.48/21.47) |
| B-37 | B | REPRODUCED SIMULATION | Repaired 540 CF4b fails spend (HK 89.98; KR 105.54) |
| B-38 | B | REPRODUCED SIMULATION | Repaired 540 CF3b is Win-Win (HK 70.88/23.64; KR 72.55/21.48) and CF1b is not (97.21/99.25) |
| B-39 | B | REPRODUCED SIMULATION | CF4 verdict is specification-dependent: 420-port V1 passes both; 540 pre-repair fails HK; 540 repaired passes both |
| X-01 | PROGRAMME | AUTHOR-REPORTED | 420-run generation (N=400/T=70) is the result behind Paper B tables |
| X-02 | PROGRAMME | REPRODUCED SIMULATION | 540-run generation (N=300/T=46) is the canonical reproduced result |
| X-03 | PROGRAMME | CONTRADICTED | Pre-repair 540 Korean gap/ratio failure is a parameterisation failure |
| X-04 | PROGRAMME | REPRODUCED SIMULATION | Repaired-engine 540 migration: participation flat, contest effort -98-99%, expected/realised 1.0000 |
| X-05 | PROGRAMME | REPRODUCED SIMULATION | CF4a Win-Win in both jurisdictions on repaired engine |
| X-06 | PROGRAMME | CONTRADICTED | CF1b is the only arm meeting the Win-Win criterion |
| X-07 | PROGRAMME | REPRODUCED SIMULATION | CF4 verdict flips with the engine repair (spec dependence) |
| X-08 | PROGRAMME | CONTRADICTED | 7-parameter ABC is identified / 5 moments pin 6 active parameters |
| X-09 | PROGRAMME | CONTRADICTED | 100% seat-expansion paradox (dSpend/dS>0 in all cells) |
| X-10 | PROGRAMME | CONTRADICTED | Archived Tullock solver is a valid general-r best response |
| X-11 | PROGRAMME | CONTRADICTED | Pooled E1/Q3 selftest separates minority-effect leakage from OVB |
| X-12 | PROGRAMME | CONTRADICTED | Country-block permutation tests the within (FE) estimand |
| X-13 | PROGRAMME | CONTRADICTED | Legacy synthetic DGP supports identification claims |
| X-14 | PROGRAMME | VALIDATED SIMULATION | Corrected crossed DGP reaches full rank 5/5 and recovers parameters |
| X-15 | PROGRAMME | VALIDATED SIMULATION | GPU and CPU agree numerically on the selftest |
| X-16 | PROGRAMME | VALIDATED SIMULATION | Gate-1 engine repairs implemented and pass contract tests |
| X-17 | PROGRAMME | UNRESOLVED | Canonical spec is frozen and Gate-2 calibration is done |
| X-18 | PROGRAMME | UNRESOLVED | GPU bundle outputs are citable scientific evidence |
| B-40 | B | REPRODUCED SIMULATION | Paper B 540 scripts/data are in hand: runner dd0b1d8d, core 618bd6dd, tutoring b2d213b6, patch, reference 851bb1df |
| X-19 | PROGRAMME | AUTHOR-REPORTED | Paper A Exp 1 (bulge t*, 7,290 obs, 2,500 permutations) is reproducible |
| X-20 | PROGRAMME | AUTHOR-REPORTED | Paper A Exp 3 (1,640-run gate architecture / H2) is reproducible |
| X-21 | PROGRAMME | AUTHOR-REPORTED | Paper A Exp 4 (masseng-tutoring Jacobian/theorem) is reproducible |
| X-22 | PROGRAMME | AUTHOR-REPORTED | Paper A Exp 5 (E8 fee-abolition shock / forecast) is reproducible |
| X-23 | PROGRAMME | AUTHOR-REPORTED | Paper B 420-generation design is reproducible |
| X-24 | PROGRAMME | REPRODUCED SIMULATION | The ABC identification audit is independently re-executable and its committed output is correct |
| X-25 | PROGRAMME | REPRODUCED SIMULATION | Paper B 540 design/CF4 reproduction can be extended to table regeneration |
| X-26 | PROGRAMME | UNRESOLVED | Paper A five intended computations (E8 event study; bulge t* with fresh hashed WDI; gate architecture >=5,000 runs with H2; multi… |
| X-27 | PROGRAMME | REPRODUCED SIMULATION | Item (c) gate-architecture: CLOSED — REPRODUCED SIMULATION. Clean JSON results/audit/newgen/gate_architecture_results.json sha256… |
| MZ-01 | PROGRAMME | UNRESOLVED | EP-1 engine probe (matched public-feedback intervention; NOT a named-theory discriminator): arms C0 / P (school_feedback=x, feedb… |
| MZ-02 | PROGRAMME | UNRESOLVED | EP-2 engine probe (own access x firm constraint 2x2, seeds 100-131): E00/E01/E10/E11; fixed own_share_financial denominator (own/… |
| MZ-03 | PROGRAMME | UNRESOLVED | Run gate: no run until (i) Paper C prereg residual fixes land + Codex protocol/Kaplan confirmation, (ii) EP-1/EP-2 probe design s… |
| MZ-04 | PROGRAMME | UNRESOLVED | Pilot-0 provenance: code-authoritative 128 runs / 16 cells (supersedes earlier 96/12 docstring mention); committed v3 has 4 regim… |
| EV-01 | PROGRAMME | UNRESOLVED | HK-vs-PH 2019 supply-form unobserved; SEA-PLM 2024 is a candidate route, not yet testable: PISA 2018/2022 has participation/hours… |
| EV-02 | PROGRAMME | UNRESOLVED | Paper C empirical leg feasible-partial (participation/hours only); supply-form/withholding predictions remain theory/simulation u… |
| EV-03 | PROGRAMME | UNRESOLVED | DHS E1-E8 cannot test the model zoo: no tutoring, learning, gate/seat, time-use, earnings or expenditure variables; they weakly c… |
| EV-04 | PROGRAMME | UNRESOLVED | D/L/V verification-status convention: D = documented snippet/committed file, L = located/access-route, V = verified item/source; … |
| X-28 | PROGRAMME | CONTRADICTED | Runner-defect class: three silent/fatal bugs found by reading raw artefacts, not summaries - (i) fee no-op (simulation index vs c… |
| X-29 | PROGRAMME | UNRESOLVED | X-27 design diagnostics: realized admission rates are NaN in the raw checkpoints and JSON (contest_candidates/seats/admitted/cont… |
| D-05 | PROGRAMME | CONTRADICTED | Citation verification of inventory section 5: 0 of equations 57-86 verified; every citation is a placeholder (UIS+2, OECD+3, hanu… |
| D-06 | PROGRAMME | UNRESOLVED | Jayachandran (2014, JDE 108:190-205) published model DOES contain withholding (school-day material m, achievement s(m,t), s_mt<0,… |
| C-05 | PROGRAMME | UNRESOLVED | Paper C confirmatory prereg re-reviewed (Amendment A1, commit c0f4eb6; file sha dd58919d...): 8 original blocking items substanti… |
| X-30 | PROGRAMME | UNRESOLVED | Lean verification methods artefact (commit 4d42101; LEAN_VERIFICATION_SCOPE sha256 9f31108e...; LEMMA_LEDGER.csv da956fc1.../LEMM… |

## Sorry ledger

**Zero `sorry`s in `verification/lean/`.** For every declared-but-unproved statement, the table below records *what would prove it* (the "sorry ledger" analogue; these are `hypothesis`/`specified` declarations, not admitted proofs).

| claim | status | why unproved | what would prove it |
|---|---|---|---|
| A-35 | `hypothesis` | empirical/world statement — not a mathematical theorem | data + CS estimator formalization (or exact fixture from the artifact); not a theorem of the model. |
| A-36 | `hypothesis` | empirical/world statement — not a mathematical theorem | same as A-35; no-effect statement requires the estimator and data. |
| A-37 | `specified` | specification only; exact proof requires data/code outside the prototype | exact-rational re-encoding of the forecast scoring function + engine fixtures; float32 internals stay out of Lean. |
| A-39 | `specified` | specification only; exact proof requires data/code outside the prototype | the exact rational Jacobian matrix as a fixture; rank/nullity provable by `decide`; SV/conditioning floats stay artifact evidence. |
| B-43 | `specified` | specification only; exact proof requires data/code outside the prototype | hash-chain provenance check in Python; not a Lean proposition. |
| B-44 | `specified` | specification only; exact proof requires data/code outside the prototype | welfare interpretation needs learning/access/teacher-workload/student-time data not in the programme; Lean records only the accounting criterion. |
| C-01 | `hypothesis` | empirical/world statement — not a mathematical theorem | a formal model of the private-market regime + a fixture showing the engine's own_ban/mode settings; design-only today. |
| C-02 | `hypothesis` | empirical/world statement — not a mathematical theorem | formal substitution channel (school-supplied prep S) in the model; Tier-1b extension. |
| C-03 | `hypothesis` | empirical/world statement — not a mathematical theorem | formal withholding/rent channel with firm-fee response; model extension + fixtures. |
| C-04 | `specified` | specification only; exact proof requires data/code outside the prototype | pre-registration + executed grid; Lean can formalize the design schema now. |
| D-03 | `specified` | specification only; exact proof requires data/code outside the prototype | pre-registration + executed divergence tests; Lean can formalize the schema now. |
| D-04 | `hypothesis` | empirical/world statement — not a mathematical theorem | primary-source citation verification (not a Lean task). |

Claims proved or computationally checked in this prototype: `budget_ledger_identity`, `tax_revenue_le_base`, `prep_recursion_closed_form`, `pl_top1_sum_eq_denom`, `pl_top1_sum_eq_min`, `pl_topK_selected_sum`, `A34_arithmetic`, `A38_anchor_infeasible`, `B41_*` (×3), `B42_*` (×3), `classical_demand_ignores_*` (×5), `D02_paradox_not_universal`.

## Axiom audit

`verification/lean/ci/lean_verify.sh` runs `#print axioms` on every proved theorem and fails if `sorryAx`, `Classical.choice`, `Lean.ofReduceBool` or `Lean.trustCompiler` appear. Last recorded output:

```
== axiom audit ==
'Atlas.budget_ledger_identity' depends on axioms: [propext]
'Atlas.tax_revenue_le_base' depends on axioms: [propext]
'Atlas.prep_recursion_closed_form' depends on axioms: [propext]
'Atlas.pl_top1_sum_eq_denom' does not depend on any axioms
'Atlas.pl_top1_sum_eq_min' depends on axioms: [propext]
'Atlas.pl_topK_selected_sum' depends on axioms: [propext]
'Atlas.Claims.A34_arithmetic' does not depend on any axioms
'Atlas.Claims.A38_anchor_infeasible' does not depend on any axioms
'Atlas.Claims.B41_HK_meets_criterion' does not depend on any axioms
'Atlas.Claims.B42_CF4b_fails_spend_HK' does not depend on any axioms
'Atlas.Claims.D02_paradox_not_universal' does not depend on any axioms
'Atlas.Claims.classical_demand_ignores_school_supply' does not depend on any axioms
'LeanStarter.gap_eq_truncated_sub' depends on axioms: [propext]
'LeanStarter.gap_pos_of_shortfall' depends on axioms: [propext]
'LeanStarter.used_plus_remaining_eq_capacity' depends on axioms: [propext]
'LeanStarter.preparation_within_elapsed' does not depend on any axioms
'LeanStarter.work_within_elapsed' does not depend on any axioms
'LeanStarter.review_within_elapsed' does not depend on any axioms
'Atlas.Model.gap_nonneg' does not depend on any axioms
'Atlas.Model.gap_eq_zero_iff_met' depends on axioms: [propext]
'Atlas.Model.gap_pos_iff_shortfall' depends on axioms: [propext]
'Atlas.Model.accepted_le_capacity' depends on axioms: [propext]
'Atlas.Model.zero_extra_input_no_increment' does not depend on any axioms
'Atlas.Model.total_input_eq_sum' does not depend on any axioms
'Atlas.Model.additive_combine_eq_sum' does not depend on any axioms
'Atlas.Model.max_not_additive' does not depend on any axioms
'Atlas.Model.budget_implies_component' does not depend on any axioms
'Atlas.Model.time_accounting_identity' does not depend on any axioms
'Atlas.Model.rank_invariant_under_common_shift' depends on axioms: [propext]
'Atlas.Model.fixed_seat_relative_rank_counterexample' does not depend on any axioms
'Atlas.Model.accepted_monotone_fixed_capacity' depends on axioms: [propext]
'Atlas.Model.complementarity_counterexample' does not depend on any axioms
'Atlas.Model.feedback_capacity_counterexample' does not depend on any axioms
axiom audit: 33 theorem lines parsed; allowed=['propext']
axiom audit OK (only allowed axioms: none/propext)
== claim declarations present ==
```

## CI and extension plan

1. **Local:** `verification/lean/ci/lean_verify.sh` — build, `sorry` scan, axiom audit, 18/18 claim ids.
2. **GitHub Actions:** `leanprover/lean-action` (toolchain from `lean-toolchain`) + `lake build`; Tier-2 Mathlib job only with `lake exe cache get`; artifacts: build log, axiom report, ledger.
3. **Ledger consistency gate:** regenerate this file with `tools/gen_lemma_ledger.py`; the QA check "every `paper_claims.csv` row has a declaration or an explicit not-yet entry" is mechanized in `LEMMA_LEDGER.csv`.
4. **Tier-2:** general-n Plackett–Luce (Mathlib) in CI; **Tier-1b:** expand omission lemmas to a typed model with explicit parameters; **Tier-3 never theorems** (numerics/DID/bootstrap stay hashed artifacts).

