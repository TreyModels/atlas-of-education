# Master inventory of the programme's empirical claims (Synthetic Council, task-42)

Compiled 25 Nov 2026 by `un-data` from the committed records on every verified branch (all `2026-11-23-*`,
`2026-11-24-*` and `2026-11-25-*` records) and the dashboard (`research/records/2026-11-23-dashboard/README.md`
@ `2f8993c`). Status labels: **V** verified result, **N** null, **M** model/calibrated, **D** demonstration,
**A** audit (re-examination of a known claim), **U** unresolved/contradicted. Every row names the branch @ commit
the number must be checked against; this inventory deliberately includes the records other papers did not use.

## A. Fertility block

| # | claim | number / effect | status | record @ commit |
|---|---|---|---|---|
| F1 | Schooling–fertility gradient in levels (all 8 measures) | women's years −0.129 (0.029), n=5,915/192; total −0.228 (0.042); sec −0.0213 (0.0037); all 8 negative-significant | V | corr-rebuild `161b563` |
| F2 | Same relation in decade changes | women's years +0.111 (0.045); total +0.190 (0.055); 0/8 negative-significant; 3/8 positive-significant | V | corr-rebuild `161b563` |
| F3 | Specification curve, 336 specs | 99.7% negative, 91.3% negative-significant, 0% positive-significant, median −0.475 (288 period specs) | V | corr-rebuild `161b563` |
| F4 | Transportability, 400 random 6-group re-partitions | levels negative-significant in 90% (67–100%) of groups; changes 1% (0–17%) | V | corr-rebuild `161b563` |
| F5 | Extended battery: 13,800 partitions, 342 pairs, 57.3M regressions | focal pairs levels 71–99% vs changes 0–7%; matrix-wide 0.227 [0.214,0.239] vs 0.111 [0.103,0.120]; 0/8 change measures negative-significant | V | corr-battery `9363079` |
| F6 | Future-schooling placebo | 52.9% vs 58.8% negative-significant; median −0.0179 vs −0.0224 (~90% as strong) → development gradient | V/A | corr-battery `9363079`; corr-rebuild `161b563` |
| F7 | Threshold shape (6/9-year hinges) | −0.33 / −0.09 / +0.11 (rebuild); bootstrap −0.326 [−0.405,−0.248], −0.092 [−0.175,−0.013], +0.112 [+0.057,+0.171] | V (shape) / U (hinges conventional) | corr-rebuild `161b563`; corr-battery `9363079` |
| F8 | 20-measure marriage matrix (380 links) | no marriage→fertility link survives; +0.020 marriage-age "effect" reverses to −0.027 under changes; income-levels bug fixed (127/42/24) | V/A | matrix-marriage `559a4e9` |
| F9 | UN marriage/living-arrangements data | age at marriage ~19→26 across surveys; cross-country −0.65 but within +0.007; living arrangements null; school→fertility edge null −0.0015 (0.0016) | V/N | un-marriage `b2b18d5` |
| F10 | Why fertility tracks child survival (mechanisms) | rival mechanisms observationally equivalent at country level; 7 pre-registered experiments designed | review | mechanisms `28479c1` |
| F11 | Child-mortality level vs volatility (E1) | level +0.0067 (0.0015) with trends, +0.0072 (0.0007) FE; volatility +0.0020 (0.0020) null; circular-shift p<0.005 level, p=0.29 volatility | V/N | level-volatility `935632e` |
| F12 | Long-run transition corners and ordering | 1800–1850: 41.6 child deaths/100, LE 39.7y; 1980–2024: 2.8, 70.7y, TFR 2.55; mortality leads fertility by 12y median (IQR 3–19; n=190; 78% positive) | V | transition `b13fde8` |
| F13 | Schooling's place in the transition | 2y of schooling precedes fertility decline by 15y in 67% of countries; 6y follows by 18y in 81%; long-run 52y lead is a reconstruction artefact | V | transition `b13fde8` |
| F14 | Mortality counterfactual in GPU ABM | freezing pre-antibiotic mortality removes 3.2% of the fall (range −1.8 to +8.2%); development-only arm 2.0%; pre-antibiotic arc unreachable (4.01→4.94→4.64, max 5.20/5.42) | M | transition-gpu `f9f2f18` |
| F15 | Individuation vs development-only out of sample | 24.43 vs 21.10, diff +3.32 [−3.76,+11.14], A better 3/6; GPU variant +3.80 [−2.60,+11.96] | N (tie) | dose-gpu `774085c` |
| F16 | Dose-model identification / tolerance ladder | 4/5 parameter spreads 0.87–1.01 of prior width across tolerances; career delay narrows 0.88→0.71–0.76; wide intervals = identification limit | V (negative) | dose-tolerance `baadfe6` |
| F17 | Care-work loop | care-work gradient +0.009 (t 0.17) after income +0.242 (t 2.47), urban +0.42 (t 3.38); male-care placebo +0.179 (t 2.10); manufacturing −0.189 (t −3.47) | N | care-credential `e626cb8` |
| F18 | Strong "no-off-switch" | 34/396 episodes (8.6%, upper 11.3%) rebound; 5/38 within 10y; ceiling 1.83; event study +0.035 (0.025), MDE 0.070; weak form supported | N (strong) / V (weak) | policy-foreclosure `63691a2` |
| F19 | Tipping point / critical slowing down | autocorrelation −0.025 (0.008) wrong sign; variance +0.079 (0.034) fails surrogate 0.42; diminishing returns +0.00019 (t 18.2) floor-confounded | N | early-warning `7e64f61` |
| F20 | DHS ecological gradient | primary −0.57 (0.06), secondary −1.62 (0.17), higher −2.54 (0.24); 99% of 346 surveys negative, median −1.90; cohort and pipeline attenuation *contradicted* (+0.26 (0.13), +0.13 (0.05)); individual microdata unobtainable | V (ecological) / U (micro) | dhs-micro `31ded00` |
| F21 | Credential gap (part of care record) | attainment −0.62 vs credential gap −0.15; gap turns positive in horse race; attainment/credentialed-jobs r=0.807 (n=46) | V | care-credential `e626cb8` |

## B. Massification block

| # | claim | number / effect | status | record @ commit |
|---|---|---|---|---|
| M1 | Grouping multiverse, 400 groupings | 38,420,908 regressions; no driver robust in every grouping; electricity strong under country effects, dead under country trends (+0.07 baseline; +16.05 is one specification); paid employment clean null; child mortality/life expectancy the only robust links (fertility side) | V/N | grouping-multiverse-400 `1152cec` |
| M2 | Multiverse resolution arithmetic | lone link needs ~5,440 draws; a 30-link cluster ~182; at 400 draws 35 links certified via Benjamini–Hochberg cluster | V (method) | methods-multiverse-paper `f9673a9`; novelty `390db8d` |
| M3 | Gap-filled panel | 61/544 links change significance over 55 links, zero sign flips; 6 unreliable, 13 coverage-driven, 18 precision-only; 127/45/35 significant (observed 127/42/24) | V/A | imputed-matrix `5e4602b`; imputed-panel |
| M4 | Added controls | 217 cells changed; 120 pure composition, 94 genuine; conclusions unchanged or strengthened; 3 sign flips are collinearity artefacts | V/A | controls `5ea58af` |
| M5 | Supply vs demand for schooling | decomposition of enrolment growth; demand-side development dominates; supply-side (school construction) not identified as driver | V | supply-demand `963e5e5` |
| M6 | "Schools before factories": schooling precedes agricultural labour release | 61/64 country cases; late-industrialiser regularity, not universal law; **ordering figure: strict schooling-first 37.5% [26.6–50.0], simultaneous 31.3%; the source JSON's 68.75% counted ties as schooling-first and is NOT used** | V (assembly) / **U (69% figure)** | historical-sequence `ab658c7`; subsistence-v2 `ce66cfc`; paper-massification `753e102` |
| M7 | Agricultural floor / Boppart joint model | agricultural subsistence constraint quantifies a floor; joint model rejects pure demand story | M | subsistence `41f6429`; subsistence-v2 `ce66cfc` |
| M8 | Scaling laws of education/occupations | Heaps exponent 0.333 (0.011), 151 countries, 11,712 points (z=−5.9 vs 0.4 benchmark); no universalisation regime break (Welch p=0.22); education–income exponents shrink within countries (secondary 0.215→0.090) | A (audit) / N (new negative) | scaling `fd691a6` |
| M9 | GPU engine scale/robustness | 66.8M simulated women per launch (12.7s); batch-layout dependence up to 1.13 births documented | D | cuda-scale `e600763` |
| M10 | Credential inflation | attainment −0.62, credential gap −0.15; saturation test fails; +0.81 correlation | A | care-credential `e626cb8` |

## C. Synthesis records and prior novelty work

| # | deliverable | status | record @ commit |
|---|---|---|---|
| P1 | Paper F — levels-vs-changes/transportability audit | DRAFT pushed (bf3997b; fixes 2864528); audited INCREMENTAL new assembly | paper-fertility `2864528` |
| P2 | Paper M — "Schools before factories" omnibus massification synthesis | DRAFT pushed (17,371 words); sequencing assembly | paper-massification `753e102` |
| P3 | Paper N1/N2 — nulls and multiverse resolution arithmetic | DRAFT pushed (28cf691) | paper-nulls `28cf691` |
| P4 | Paper S / BOPPART sections — scaling audit and transition/individuation sections | section drafts pushed (`cuda-scale`, `90feb1e`) | paper-scaling `24 Nov`; paper-boppart `90feb1e` |
| P5 | Earlier novelty ledger | 4 new / 8 incremental / 11 known; three defensible contributions (multiverse arithmetic; power-calibrated trend audit; GPU transition counterfactual, then pending) | novelty `390db8d` |
| P6 | Independent lit audit | Paper F INCREMENTAL; Paper M sequencing INCREMENTAL-NEW; per-claim prior-work maps | lit-audit `2026-11-24` |

## D. Measurement and infrastructure claims (not paper candidates, listed for completeness)

| # | claim | status | record @ commit |
|---|---|---|---|
| X1 | GPU engine reproduces CPU reference exactly with new channels off; 66.8M women/launch; 5.1–5.3M women/s | D | cuda-scale `e600763`; dose-gpu `774085c` |
| X2 | Particle-filter ABC produced a degenerate posterior (ESS ≈1/600); rejection sampling fixed it | D (methods lesson) | dose-gpu `774085c` |
| X3 | Circular-shift permutation vs year-shuffle: year-shuffle is anti-conservative; circular-shift preserves autocorrelation | D (methods lesson) | un-marriage `b2b18d5`; level-volatility `935632e` |
| X4 | UN marriage data are obtainable (403 was a UA block, not access denial) | D | un-marriage `b2b18d5` |
| X5 | Income must be logged; handoff 126/45/25 counts came from a levels bug | D | matrix-marriage `559a4e9` |

**Inventory totals: 21 fertility claims, 10 massification claims, 6 synthesis records, 5 infrastructure claims.**
No claim in this inventory is rated NEW CORRELATION; the classification and killing are in `CANDIDATES.md` and
`DECISION.md`. The sequencing ordering percentage is the only **U** that has already been retracted by its own
paper (M6): any candidate that cites "69%" or "68.75%" is rejected on sight.
