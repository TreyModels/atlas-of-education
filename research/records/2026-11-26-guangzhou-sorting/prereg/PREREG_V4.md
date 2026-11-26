# Pre-registration v4: informant corrections (Guangzhou sorting model)

Written 2026-11-26 23:15 CST, before running. Model `gz_v4.py` (v3.1 + changes below), sweep `run_v4.py`, analysis
`analyze_v4.py`. ILLUSTRATIVE SIMULATION. Source of the changes: informant A field record (`fieldnotes/INFORMANT_A_2026-11-26.md`).

## Changes from v3.1
1. Pre-gate tutoring survives the ban: wealth-weighted take-up PRE_SHARE, of which BAN_RED is removed by the 2021 ban; takers gain PRE_EFF in skill at 15 (fades with DECAY like other head-start inputs).
2. Academic-track share 45-65% (informant: about 50%).
3. Senior-2 re-banding is by performance for only REBAND_PERF of pupils; the rest keep their band (subject-combination regrouping).
4. Post-gate tutoring at both tails of the academic skill distribution (bottom and top 20% weighted 4x the middle) and by wealth: term tutoring (TERM_SHARE; three times higher without boarding) and holiday tutoring (HOL_SHARE); each adds POST_EFF to the gaokao.
5. Full-time institution route: pupils in the weaker half of the academic track from families able to pay FT_COST (140,000 yuan/yr small class) with under 50% of income; FT_SHARE of the cohort; they lose in-school class effects and gain FT_EFF (sign unknown).

## Scenarios per draw (common random numbers)
- CURRENT: ban as drawn, boarding, partial re-banding, term + holiday tutoring, full-time route.
- OLD (pre-2021 regime): BAN_RED = 0, no boarding (term tutoring x3), no re-banding.
- BAN_PERFECT: BAN_RED = 1 (no pre-gate tutoring).
- TIME_CONTROL: no term, holiday or full-time tutoring after the gate.

## Ranges (400 LHS draws, seed 20261129, n = 40,000)
v3.1 ranges for shared parameters (SCHOOL_VA 0-0.5) plus: ACAD 0.45-0.65; PRE_SHARE 0.2-0.6; BAN_RED 0-0.6; PRE_EFF 0-0.3;
REBAND_PERF 0-0.5; TERM_SHARE 0.02-0.15; HOL_SHARE 0.2-0.6; POST_EFF 0-0.2; FT_SHARE 0-0.05; FT_EFF -0.2 to 0.3.

## Claims (fixed now)
- **V1** The current system is fairer at equal talent than the pre-2021 regime even with tutoring persisting: EO_local(CURRENT) < EO_local(OLD) in >= 90% of draws.
- **V2** Post-gate tutoring still leaks wealth: EO_local(TIME_CONTROL) < EO_local(CURRENT) in >= 80%.
- **V3** Pre-gate tutoring still leaks wealth: EO_local(BAN_PERFECT) < EO_local(CURRENT) in >= 80%.
- Descriptive: which leak is larger (share of draws); EO_local by head-start-fade bins and the fade values where the median crosses 1.10 and 1.30; EO at equal zhongkao and unconditional; effect of the full-time route by sign of FT_EFF; non-hukou cohort destinations.
V2 and V3 are partly built in (each channel has a non-negative effect drawn from a range starting at 0); the reported quantity is their size.
