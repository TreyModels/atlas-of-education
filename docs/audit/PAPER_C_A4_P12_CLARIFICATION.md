# Paper C — A4 clarification: P12 is the no-withholding control (pre-confirmatory, no design change)

**Status: clarification for the confirmatory manifest; no design change; no compute.** In the FINAL prereg
(`PAPER_C_CONFIRMATORY_PREREG.md`, amendments A1–A3) and the screening manifest (`p12_mode=pay_gap`):

1. **P12 setting = `pay_ratio=1.2, monitoring=0.5, withhold_mode='pay_gap'`** → the pay-gap driver is
   `max(0, 1 - pay_ratio) = 0`, so **withholding h = 0 by construction**: **P12 is the no-withholding control**.
2. **Exposed arms** (where the binding assertions `withheld > 1e-3` and `own_share > 0.1` apply) are **supply A/C AND
   setting P55 only** (own access open, pay_ratio .55 ⇒ h > 0).
3. **Exempt from the assertions:** **B** (own_ban .95, market-only) and **A|P12** (no-withholding control). A failed
   exposed arm is INVALID; screening reported `invalid_cells=[]`.
4. **The confirmatory manifest must cite this A4 clarification and the frozen passer list**
   (`PAPER_C_PASSERS.json`, computed from the screening artefact `6bcc29a5…` under the T1–T4 + Holm + >6 rule).
5. If the operator ever intends **P12 = `withhold_mode='incentive'`** (h > 0), that is a *different design* and needs an
   explicit A5 amendment (the A3.3 exemption logic does not apply); screening used pay_gap.

**Runner metadata fix (D-S1):** `run_paperC_screening.py` row `assertions.exposed` now records
`supply in ('A','C') and setting == 'P55'` and the rule text states the A|P12/B exemptions explicitly (wrapper check
already applied the correct scope; this fixes metadata/rule text only — **no results change**, screening
`invalid_cells=[]`). **D-S2:** gate-level `gate[1].r` is authoritative (r=1.2 at L=.25, 1.6 at L=.45); the static spec
`params.contest_r` does not drive the treated gate — now recorded in every row (`contest_r_note`) and in the module
docstring.
