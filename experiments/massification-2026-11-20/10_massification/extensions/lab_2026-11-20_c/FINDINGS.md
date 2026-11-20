# Lab battery 2026-11-20_c — consolidated findings (Y1–Y5, Council-anchored)

**Status: DESCRIPTIVE / DESIGN-ONLY — no causal or direction claims; not evidence of policy effects.**
The Synthetic Council (Council-2) adjudicated battery B (`lab_2026-11-20_b`, ACCEPT-WITH-CONDITIONS) and — under
the **new standing order D89** (five anchored experiments per delivered results batch, mandatory 7-field anchoring
block, drop-first rule) — issued five experiments in `08_council/brief_017/SYNTHESIS_017.md` §D. The Lead
**predeclared them before running** (`PRE_DECLARATIONS.md`, sha256
`8b431b672bbc9679dc192e907c1db3b95e22bacad2abd6b377c68e864dc336e1`), executed them with **DeepSeek Flash workers**
(3 workers, disjoint dirs), and re-ran every script **byte-identically** (`RUN_MANIFEST.json`). The phase remains
**CLOSED** at PARTIAL/DESCRIPTIVE/EQUIVALENT (D76); none of Y1–Y5 reopens C1–C4.

## Results table (all five cells; verdicts fixed before the run)

| # | experiment | channel (Council ranking) | key estimate | predeclared verdict |
|---|---|---|---|---|
| **Y1** | ceiling-residual candidate-account screen | markets + cohort flows (#1) | income-partial ρ(ceiling, agri-share) = **−0.105** (n=30); ρ(ceiling, youth-unemp) = **+0.246**; raw agri −0.718 | **NOT SUPPORTED** — opportunity-cost account **discarded** (both predeclared conditions fail) |
| **Y2** | cross-channel lead-lag constraint (schooling ↔ markets) | schooling ↔ markets (#4) | strongest |partial r| = **0.208** (schooling→market, lag 1, n=700, 30 countries); 0/24 cells reach 0.25; reverse direction −0.057…+0.090 | **NOT SUPPORTED** — interaction not detectable (EQUIVALENT reinforced; description only, R13-safe) |
| **Y3** | capacity floor-not-ceiling observed check (6 systems) | government (#3) | ρ(ΔPTR-improvement, floor) = **+0.50** (n=5, boundary); ρ(ΔPTR-improvement, ceiling) = **+0.60** (n=6) | **NOT SUPPORTED** — not separable (ceiling fails \|ρ\|<0.50) |
| **Y4** | world-society rival false-positive check (null model) | rival comparison / A5b (#2) | null (median-year crossings) falsely crosses **4** never-crossed systems at the upper-secondary 90 margin, of which **2 evidence-backed** (CHN final 79.39, PHL 66.05); 4/4 90-levels: 7 false cells (4 evidence-backed) | **DISTINGUISHED** — the null does generate upper-secondary crossings the record lacks (supports the D77 scoping) |
| **Y5** | portability design data-completeness audit (CHN/HKG) | cohort flows / scaling (#5, drop-first) | **6/6** D75 inputs present on disk for both countries (12/12 rows); **0 NEW-ASK** | **DATA-COMPLETE** — a future transfer run is not blocked on data (still needs a Council decision + predecl) |

## What each result does to the write-up (the discriminating actions the Council predeclared)

1. **Y1 — discard the opportunity-cost account.** The raw agri-share association with the tertiary ceiling is
   strong (−0.718) but **almost entirely absorbed by the income control** (−0.105), and youth unemployment enters
   with the wrong (positive) sign. Under the frozen rule the account is **UNABLE/discarded** from D63's candidate
   list. The 6-system raw check points the other way (tertiary GER × agri −0.714, n=6) and is **left standing as a
   disclosed tension**, not interpreted. Net: the ceiling residual's candidate list shrinks; the write-up reports
   the account as discarded under this screen (not as evidence the mechanism is absent).
2. **Y2 — no detectable lead-lag.** Zero-order correlations are large (0.49–0.71) but are shared-trend artefacts;
   after the predeclared own-lag-1 control no cell reaches 0.25 (max 0.208), and the reverse direction is flat. The
   write-up must say the schooling↔market interaction is **not detectable cross-sectionally** — reinforcing
   EQUIVALENT — and the model is **not** required to reproduce a lead-lag the data do not show.
3. **Y3 — capacity floor/ceiling not separable at n=6.** Floor ρ hits the 0.50 bar exactly, but the ceiling ρ is
   0.60 (fails the <0.50 condition), so the A10/R29 "floor not ceiling" reading gets **no observed support** here;
   the write-up keeps A10 as a model-side ruling only, with the D64 crude-proxy caveat. **Disclosed fragility:**
   leave-one-system-out swings floor ρ over 0.0–0.8 and ceiling ρ over 0.3–0.9; both conditions hold together only
   when dropping JPN — the one system whose floor is UNABLE. Not presented as marginal support.
4. **Y4 — the rival null is distinguished on the upper-secondary margin.** A "cross at the cross-system median
   year" null would manufacture upper-secondary ≥90 crossings for systems the record shows never crossing (2
   evidence-backed: CHN 79.39, PHL 66.05). This **supports** the D77 sharpened scoping that the rival field's
   emptiness rests on ordering/spacing **and** the upper-secondary non-crossing. Caveat disclosed: the upper-secondary
   null year rests on **one** dated non-censored crossing (HKG 2011.5); the verdict does not depend on the
   data-absent JPN case or the untestable KHM case.
5. **Y5 — the CHN/HKG transfer is data-complete.** All six D75 inputs are present on disk for both countries;
   `SCHOOL_EXPANSION.csv` is PHL-only but is not a D75 input for the transfer. **No new data ask**; the held queue
   (PSA microdata, WB Enterprise Surveys, annual capacity/enforcement, real per-pupil spending, subnational sector
   employment, named expansion file) is **reaffirmed HELD — nothing sent**. Design-only: a future portability run
   still requires a new Council decision and predeclaration under the six D75 constraints (R20/R22).

## Council process this cycle (what the user asked for)

- The Council was convened **after** the results batch, did the mandatory five-line step-back
  (`BIG_PICTURE_RULE.md`), adjudicated battery B (**ACCEPT-WITH-CONDITIONS**, re-deriving X10 ρ = −0.443627,
  17/17 and X11 ρ = −0.621524, 17/17 independently), and issued **exactly five anchored experiments** with the
  7-field anchoring block and a **drop-first** (Y5). Decisions **D88–D92** are in `08_council/DECISIONS.md`;
  the standing order is institutionalised in `06_report/NEXT_WINDOW_PROMPT.md`.
- **Drift check:** battery B was the third consecutive mostly-measurement batch; two red flags were recorded and
  the Council directed the five experiments at the write-up's **open descriptive items** (ceiling residual,
  capacity ruling, rival scoping) and a **declared future path** (portability design) — not at re-opening the
  verdict. **Critical path remains the A1/phase write-up** (D91); Y1–Y5 exist to tighten it.
- **No external message was sent** (bridge writes time out; files are the memory — D87). All data external
  requests remain HELD pending user approval.

## Limits

Small n throughout (Y3 n=5–6 systems; Y4's upper-secondary null rests on one dated crossing; Y1 six-system check
n=4–6 raw); all Y1/Y2/Y3 cells are **derived/observed descriptive correlations**, not identified effects; Y5 is
design-only and makes no portability claim; Y4 is null-model scoring, not a rival fit. No causal language; no
push/pull direction claim; the closed phase's verdict is untouched.
