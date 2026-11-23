# Novelty review — is any of this session's work genuinely new?

Worker `novelty-review`, branch `research/novelty-2026-11-23`, 23 November 2026. Task-14.

**What this is.** An external literature check on the session's candidate findings, starting with Dr. Menefee's
suspicion that the electricity result may be a known thing in new clothes. The deliverable is a ledger, not a
paper: one row per claim, closest prior work, what is new, and a verdict (NEW / INCREMENTAL / KNOWN).

**Bottom line.** Most of today's findings are **not new to the field** — they are replications, corrections, or
new-to-us results. Three things are genuinely defensible as contributions:

1. **The multiverse resolution arithmetic** — the design rule that how many random groupings you need depends on
   how many links pile up at the p-value floor (a lone link needs ~5,440 draws; a cluster of 30 needs ~182; at
   400 draws 35 links were certified because a 30-link cluster cleared Benjamini-Hochberg). Built from known
   statistics, but the explicit rule and the demonstration appear unstated. Strongest novelty candidate.
2. **The power-calibrated trend audit of cross-country education-development links** — the "trend kills it"
   critique is textbook panel econometrics, but pairing the full link matrix with a purpose-built power
   simulation and reporting the result as an interval ("cannot be separated from development at this power")
   rather than a null is a real increment, and the single-specification +16.05 case is a clean caution.
3. **The full-transition GPU counterfactual** (pending) — if the individual-level simulation of the
   pre-antibiotic-to-collapse arc runs and validates, with a no-mortality-decline counterfactual, that is a new
   *demonstration*. It is not a new theory: demographic transition models and historical microsimulation are
   decades old (SOCSIM, 1970s).

**What we must not claim.** That electricity does not drive schooling (the micro literature is large and mostly
positive; our result is the standard common-trend warning, and the cross-country prior art exists). That child
survival drives fertility (that hypothesis is from 1976). That individuation is refuted (we tested one
poor-fitting model with unidentified strengths). That anything here is causal identification. Or "first" — use
"we are not aware of".

**Files.** `NOVELTY_LEDGER.md` (full ledger, plain words, A-F priorities), `refs.md` (citations with
verified/unverified status).

**Verification caveat.** The Mac's web path was degraded during this review: Crossref's API, direct journal
pages and GitHub were unreachable, and fetching journal pages failed. Citations were checked through `web_search`
results only. Anything marked `[unverified]` in `refs.md` should be checked against the publisher before it goes
into a paper.
