# Pre-registration v6: Guangzhou against its own idea of merit, against a stylised Hong Kong, and the rich routes

Written 2026-11-27 00:10 CST before running. Model `gz_v5.py` (with stylised Hong Kong levers ELITE_BUY and ZONE_ADMIT added,
default 0), sweep `run_v6.py`; 400 LHS draws over the v5 ranges, seed 20261201, n = 40,000. ILLUSTRATIVE SIMULATION.

## The author's argument, stated as testable claims
The author's position: by China's own understanding of merit, Guangzhou's system is remarkably fair; fairer than Hong
Kong, where neighbourhood and money buy access; the routes rich families choose work less well than they think; and the
double reduction works on its own terms. The model is used to see whether that position survives its own assumptions.

## Scenarios (same pupils per draw)
CURRENT (Guangzhou 2026); OLD (pre-2021: no ban, day schools, no re-banding); HK_STYLE (stylised Hong Kong: open
tutoring market, day schools, no re-banding, no zhibiao, no hukou, 20% of elite seats obtained by paying (direct-subsidy
schools), elite admission weighted 0.3 SD per SD on the school net, no art/Hong Kong routes); BAN_PERFECT; TIME_CONTROL.
HK_STYLE is a caricature built from Guangzhou's own population and parameters; it is not a calibrated Hong Kong.

## Claims and thresholds (fixed now)
- **M1 Fair by its own terms.** "Same score, same chance": among local pupils with the same zhongkao score, richer vs
  poorer elite-university ratio (EO_equal_zk) <= 1.10 in >= 80% of draws (CURRENT).
- **M2 Fairer than the stylised Hong Kong.** EO at equal talent (EO_local) lower in CURRENT than HK_STYLE in >= 90% of
  draws, and the unconditional ratio (EO_uncond) lower in >= 90%.
- **M3 Rich routes work less than their price suggests.** For the richest fifth, post-gate tutoring plus the full-time
  route raise own elite admission by < 5 percentage points per 100,000 yuan spent in >= 80% of draws (cutoff held fixed).
- **M4 Double reduction on its own terms.** Built in by construction for take-up and spending (BAN_RED > 0 cuts pre-gate
  tutoring). Reported: change in pre-gate take-up, household tutoring spending and EO_local, OLD vs CURRENT and CURRENT vs
  BAN_PERFECT. Empirical evidence must come from outside the model (e.g. CIEFR household survey: off-campus academic
  tutoring 36.1% in 2017 to 13.5% in 2023).

A claim below threshold is reported NOT SUPPORTED and the paper's argument is narrowed accordingly.

## Amendment 1 (00:20 CST, after one test draw at parameter midpoints, before the sweep)
A bug in partial re-banding (introduced in v4) let the number of pupils in top classes exceed the fixed top-band share:
pupils kept their entry band unless redrawn, while redrawn pupils could also join. Fixed in gz_v5.py and gz_v4.py with a
composite rank (REBAND_PERF x senior-1 rank + (1 - REBAND_PERF) x zhongkao rank), which keeps band sizes fixed. The v4
and v5 recorded results were produced with the bug and are superseded where they overlap with this sweep (CURRENT, OLD,
BAN_PERFECT, TIME_CONTROL). Claims and thresholds unchanged.
