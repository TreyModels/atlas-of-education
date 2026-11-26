# Pre-registration: Guangzhou sorting model (talent vs skill), robustness study

Written 2026-11-26, before the sweep below was run. Model: `gz_talent.py` (sha256 recorded in `sweep_manifest.json`).
Status of all results: ILLUSTRATIVE SIMULATION. Synthetic pupils; no parameter is calibrated to Guangzhou microdata.

## Question
For pupils of equal talent, how much does family wealth change who reaches the academic track, a top class,
and an elite university, in (a) the current cohort (tutoring banned before the gate, boarding, re-banding at senior 2)
versus (b) a ~2015 cohort (tutoring legal, no re-banding)? Which mechanism carries the remaining gap?

## Primary measure
EO_uni: elite-university rate of richer two-fifths / poorer two-fifths, among top-fifth talent, averaged over
10 talent bins (1.00 = level). Secondary: EO_track, EO_topband_entry, concentration index of elite university over
wealth rank, share of high-talent pupils from the poorest-fifth zones in a top class at senior 2.

## Design
2,000 Latin-hypercube draws over the uncertain parameters (ranges below), seed 20261126. Each draw runs four
scenarios with common random numbers: CURRENT (reband, no tutoring), NO_REBAND, EQUAL_ZONES (zone teacher effect 0),
COHORT_2015 (pre-gate tutoring PRE_TUT > 0, post-gate tutoring POST_TUT > 0, no reband). n = 40,000 pupils per run.

| parameter | meaning | range |
|---|---|---|
| TAL_WEALTH | talent-wealth correlation | 0 - 0.3 |
| ZONE_TEACH | zone-school teacher effect on skill at 15 (SD per SD) | 0.05 - 0.5 |
| HOME | home inputs (SD per SD log wealth) | 0 - 0.3 |
| DECAY | share of pre-gate head start that fades by senior 2 | 0 - 0.9 |
| GROW | talent-driven learning in senior high | 0.2 - 0.8 |
| CLASS_EFF | top-band class effect (dossier 0.44) | 0.2 - 0.6 |
| SCHOOL_EFF | school value-added per tier (dossier 0-0.2) | 0 - 0.2 |
| NOISE | exam measurement noise (SD) | 0.2 - 0.6 |
| SEG | residential segregation | 0.3 - 0.8 |
| ACAD | academic-track share | 0.55 - 0.75 |
| PRE_TUT | 2015 cohort only: legal pre-gate tutoring effect | 0 - 0.3 |
| POST_TUT | 2015 cohort only: post-gate tutoring effect | 0 - 0.15 |

## Claims and decision rules (fixed now)
- **C1 Track gate level.** CURRENT EO_track in [0.95, 1.05] in >= 95% of draws. (Partly built in: track is decided by
  zhongkao score, and high-talent pupils mostly clear a 55-75% line.)
- **C2 Re-banding narrows the university gap.** EO_uni(CURRENT) < EO_uni(NO_REBAND) in >= 95% of draws.
- **C3 Re-banding lifts weak-zone high-talent pupils.** Top-class share at senior 2 rises by >= 5 points vs NO_REBAND in >= 95%.
- **C4 Current cohort fairer than 2015.** EO_uni(CURRENT) < EO_uni(COHORT_2015) in >= 95%. Direction partly built in
  (2015 adds wealth-linked tutoring and drops re-banding); the reported result is the size of the gap.
- **C5 Zone teachers carry most of the remaining gap.** (EO_uni(CURRENT) - EO_uni(EQUAL_ZONES)) / (EO_uni(CURRENT) - 1)
  >= 0.5 in >= 80% of draws (draws with EO_uni(CURRENT) - 1 < 0.02 excluded and counted).
- **Descriptive (no threshold).** Distribution of CURRENT EO_uni; which parameters most explain it (rank correlations).

A claim that misses its threshold is reported as NOT SUPPORTED, not re-tuned. Any change after running is logged as an
amendment with its reason.

## Not modelled (documented costs and limits)
Family time cut to one day a week; phone/WeChat restrictions; tablet costs; graduate unemployment; vocational-track
quality (about 35-40% of the cohort); hukou quota (separate model); teacher-quality data beyond the dossier's RD estimates.
