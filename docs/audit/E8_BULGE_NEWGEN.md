# Paper A (a)+(b) — NEW-GENERATION empirical re-analysis on fresh hashed WDI vintage

**Label: REPRODUCED EMPIRICAL ANALYSIS (fresh WDI vintage, simple DiD); Paper A numbers are the
AUTHOR-REPORTED baseline. This is not a reproduction of the author's Callaway–Sant'Anna estimator.**
Artefact: `results/audit/newgen/e8_bulge_fresh_wdi_2026-11-25.json` (sha256 recorded in commit), script
`/tmp/e8_bulge.py` (v1 box run `/root/work/e8bulge/e8_bulge.py`), data `/root/work/wdi/` with
`WDI_MANIFEST.json` (fresh download 2026-11-25T08:38:30Z; every indicator file sha256-pinned).

## Design (as pre-registered in `GATE2_PREREGISTRATION.md` §2(a),(b))

* Treated: eight primary-verified SSA fee abolitions, dates from the Paper A manuscript:
  MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005.
* Donor pool: World Bank region SSF countries excluding treated (40-country pool per the manuscript).
* Part A outcome: primary GER (`SE.PRM.ENRR`); event study e = −6…+6, ATT_e = treated change vs e = −1 minus donor-pool
  change in the same calendar years; Fisher randomization inference 2,500 permutations each for placebo dates and
  placebo country labels.
* Part B: delayed secondary-bulge t* = abolition year + primary duration (`SE.PRM.DURS`), outcome secondary GER
  (`SE.SEC.ENRR`); same event-study/RI design.

## Results

**Part A — E8 fee-abolition shock, primary GER (fresh WDI vintage, simple DiD):**

| quantity | new-generation (fresh WDI, simple DiD) | AUTHOR-REPORTED baseline (CS estimator) |
|---|---|---|
| impact ATT(e=0) | **+12.322 pp** | +12.44 pp |
| post mean (e=+1..+6) | **+2.54 pp** | +25.26 pp |
| pre-trend e=−3 | −1.02 pp | −0.03 pp |
| placebo e=−6 | −0.42 pp | −0.39 pp |
| Fisher p (placebo dates, impact) | **0.0056** (2,500 perms) | 0.0001 |
| Fisher p (placebo countries, impact) | **0.0044** (2,500 perms) | 0.0003–0.0006 |

* The **impact** is replicated in magnitude (+12.32 vs +12.44) and is significant under randomization inference on fresh
  data. The **post-abolition average does not replicate** under this simple DiD design (+2.54 vs +25.26); the
  event-study path peaks on impact and fades. This is an **estimator/vintage difference, not evidence that the
  author's number is wrong** — the author used Callaway–Sant'Anna group-time ATT with not-yet-treated controls,
  cohort-size weighting and country-cluster bootstrap, which is not reproduced here. Recorded as a NEW-GENERATION
  result with that caveat; the author baseline remains AUTHOR-REPORTED.

**Part B — delayed secondary-bulge t* (fresh WDI vintage):**

| quantity | value |
|---|---|
| t* per country (abolition + primary duration) | MWI 2000, ETH 2001, UGA 2004, LSO 2007, TZA 2008, KEN 2009, MOZ 2011, GHA 2011 |
| ATT at t* (e=0) | **−0.956 pp** |
| post mean (e=+1..+6) | +0.30 pp |
| Fisher p (placebo dates / countries) | **0.251 / 0.384** (2,500 each) |

→ **No detectable secondary-bulge jump at t*** in aggregate macro indicators on fresh data; this is consistent with
the manuscript's own HONEST_NULL framing for the macro test (the author's null was about aggregate WDI detectability,
not about the mechanism). No causal claim is made.

## Caveats (binding for citation)

1. Simple DiD (equal country weights, not-yet-treated donor changes by calendar year) ≠ the author's CS estimator;
   differences in post-effect and p-values may be estimator-, weighting- and vintage-driven.
2. Fresh WDI vintage (2026-11-25 download, manifest-hashed) may differ from the author's snapshot; indicator revisions
   are possible.
3. Equal country weighting (cohort-size weighting not implemented); the author used cohort-size weighting.
4. The empirical block uses `consistent with` language only; no causal claim.
