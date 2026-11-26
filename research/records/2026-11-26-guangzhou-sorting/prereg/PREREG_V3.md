# Pre-registration v3: teachers, classes, zhibiao and hukou (Guangzhou sorting model)

Written 2026-11-26 before running. Model `gz_v3.py`, sweep `run_v3.py`, analysis `analyze_v3.py` (hashes in `v3_manifest.json`).
ILLUSTRATIVE SIMULATION: synthetic pupils; parameters are ranges from the Guangzhou dossiers or stated assumptions.

## Measures
- EO_local: elite-university rate, richer two-fifths / poorer two-fifths, among local-hukou top-fifth talent, averaged over 10 talent bins.
- HUKOU_ratio: same, local / non-hukou (top-fifth talent, 10 bins). 1.00 = no hukou gap at equal talent.
- NH_hiTal_{public, private, exit}: where top-fifth-talent non-hukou pupils go after the zhongkao.
- SUB_conc: concentration index over wealth of 12-year public subsidy per child (primary 19,600/yr public vs 5,000
  purchased place; junior 32,100 vs 6,000; high school 41,500 public academic, 38,400 vocational, 0 private or exit).
- Equation checks against model truth: E35 naive elite-school gap / true school VA gap; E159 between-school variance
  share / true VA share; E36 linear-in-means peer coefficient; E152 fuzzy RD at the open elite cutoff.

## Design
800 LHS draws, seed 20261127, n = 40,000 pupils. Scenarios per draw (common random numbers): CURRENT, NO_QUOTA
(QUOTA = 1), EQUAL_MIGRANT (QUOTA = 1, MINBAN_PEN = 0), NO_REBAND, NO_ZHIBIAO.

| parameter | range | basis |
|---|---|---|
| TEACH_SD (junior and senior) | 0.15 - 0.45 | dossier teacher effects 0.17-0.5; 0.4 reproduces 8-11% within-school share |
| TEACH_ZONE | 0 - 0.25 | between-school teacher gap (assumption) |
| HOME | 0 - 0.3 | home inputs (assumption) |
| DECAY | 0 - 0.9 | fade of pre-gate head start (unknown) |
| TAL_WEALTH | 0 - 0.3 | (assumption) |
| SCHOOL_VA | 0 - 0.2 | RD school-label effects |
| TOP_TEACH | 0.2 - 0.4 | top-band teacher premium |
| PEER | 0.05 - 0.25 | top-band peer premium (TOP_TEACH + PEER ~ 0.44 magnet-class RD) |
| ZHIBIAO | 0.3 - 0.6 | ~50% of seats to each junior school |
| NONHUKOU | 0.10 - 0.40 | (unknown; key) |
| QUOTA | 0.08 - 0.20 | 8-15% / 8-18% / 8-20% |
| MINBAN_PEN | 0 - 0.3 | (assumption) |
| NH_WEALTH | -0.6 - 0 | (assumption) |
| NOISE | 0.25 - 0.5 | exam noise |

## Claims and rules (fixed now)
- **H1 The quota is the main hukou barrier at equal talent.** HUKOU_ratio(NO_QUOTA) < HUKOU_ratio(CURRENT) in >= 95% of draws,
  and (CURRENT - NO_QUOTA) >= (NO_QUOTA - EQUAL_MIGRANT) in >= 80%.
- **H2 Zhibiao narrows the local wealth gap.** EO_local(CURRENT) < EO_local(NO_ZHIBIAO) in >= 90%.
- **H3 Re-banding narrows the local wealth gap.** EO_local(CURRENT) < EO_local(NO_REBAND) in >= 90%.
- **Q1 School fixed effects overstate.** E35 naive gap >= 5 x true VA gap in >= 95% (draws with SCHOOL_VA < 0.02 counted as passing if naive > 0.1).
- **Q2 Variance shares overstate.** E159 between-school share >= 10 x true VA share in >= 95%.
- **Q3 RD understates the school label.** E152 estimate < true school VA gap in >= 90% (big-fish-little-pond).
- **Q4 The peer-effect sign depends on the banding rule.** E36 coefficient is positive under CURRENT and lower under NO_REBAND in >= 80%.
- Descriptive (no threshold): distributions of EO_local, HUKOU_ratio, NH_hiTal destinations, SUB_conc, subsidy gap local - non-hukou.

A claim below its threshold is reported NOT SUPPORTED. Changes after running are amendments with reasons.

## Not modelled
Family time, phones, boarding costs to families; returning-home pupils' outcomes elsewhere; vocational quality;
graduate labour market; children left behind (never in Guangzhou); quality of teaching in private high schools beyond VA = 0.

## Amendment 1 (2026-11-26, after the v3 run, before the v3.1 run; prompted by external review)
Reason: the admissions rules in v3 did not match Guangzhou's 2026 and 2027-2029 rules. Changes in `gz_v3.py` (v3.1):
zhibiao seats are restricted to Guangzhou-hukou pupils, allocated per junior school in proportion to eligible pupils,
require a minimum score (top ZB_FLOOR of the cohort, swept 0.2-0.4), and unused seats revert to open admission; open
elite admission caps non-hukou pupils at QUOTA of elite seats. SCHOOL_VA range widened from 0-0.2 to 0-0.5 so that
results are not conditional on a near-zero school effect. Same claims and thresholds are re-scored on 400 new draws
(seed 20261128). Added descriptive outputs: fairness at equal zhongkao score and unconditional; non-hukou outcomes as
shares of the whole non-hukou cohort. The v3 results stand as recorded; v3.1 is reported beside them, not in place of them.
