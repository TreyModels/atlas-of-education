# COUNCIL STATE — one-screen handoff (authority persists via files)

**Owner:** Synthetic Council of Experts (research authority while the user is away; protocol §5). **Write scope:**
`08_council/` only. **Memory rule:** files are the memory; keep posts short.

## Standing gate (read these first, in order)

1. `brief_013/SUCCESS_CRITERIA.md` — amendments **A1–A10** (fit/check/holdout, tolerances, PASS/PARTIAL/FAIL/
   EQUIVALENT/PASS-CONDITIONAL, timing regime A4, asymmetry A6, alignment A7, capacity A9, floor-not-ceiling A10).
2. `brief_013/STOP_RULES.md` — **R1–R29** (incl. R13 direction bar, R14/R17 scaling caps, R23 single-curve, R24/R25
   timing alignment/event-window, R26 capacity, R27 repair budget, R28 capacity measurement, R29 floor/ceiling).
3. `brief_013/INTAKE_ACCEPTANCE.md` — every predeclaration accepted/returned by Council; missing bullet = returned.
4. `brief_013/ANCHOR_SYSTEM.md` — PHL anchor, B2 asymmetry, B3 rival order, B4 event-window verdict, B5 capacity,
   B6/B7 capacity floor-not-ceiling, portability to CHN→HKG.
5. `brief_013/UNIVERSALIZATION_MILESTONES.md` — M0–M4, crossing years, bands, censored bounds (C2), reconstruction rule.
6. `ANCHOR_SLATE.csv` — authoritative slate A1–A8; `brief_013/EXPERIMENT_SLATE.csv` legacy (E1 parked, E3 blocked,
   E4 DATA BLOCKED, E5/E7 park, E8 KILL).
7. `DECISIONS.md` — **D1–D65**; `BIG_PICTURE.md` — live KEEP/PARK/KILL list + cycle step-backs;
   `BIG_PICTURE_RULE.md` — mandatory five-line step-back each cycle.

## Where the phase stands (as of D65)

- Shadow-education phase **closed** (brief 008, loop close-out); **not re-fit**. Massification-first.
- Phase verdict: **conditional reproduction + observational equivalence**; universalization reproduction capped at
  **PARTIAL** (income-scaling repair FAILED, R27); **no further repair** without a new Council decision + predecl.
- **Anchor = PHL**, A1 **descriptive/mechanism-crossing only** (scaling reported FAIL, not fitted around); fit
  1999–2013 / holdout 2014–2024. Target = observed **crossing years and spacing** (A6: primary ≥90 2017,
  lower-secondary 2024, upper-secondary never, tertiary GER ≥50 2024–25); laws are only **candidate markers** where
  R24 alignment passes (PHL state pushes do not align; HKG 2009 and CHN 1999 do; CHN 1986/PHL 1987 do not).
- **Capacity**: measured in fiscal/delivery/enforcement sub-dimensions, enters as `law × G(C)` with observed input
  trajectory; **floor yes, ceiling no** (A10/R29); ceiling residual reported with candidate accounts or UNABLE.
- **E1** parked/unfielded; **E3** DATA BLOCKED + unverified context; **E4** DATA BLOCKED (no national-share proxy);
  portability (CHN→HKG) only after the descriptive anchor; **no direction claims** (R13/EQUIVALENT).
- Data asks (routed to user via op centre): PSA microdata returns/household; Enterprise Surveys credential module;
  real per-pupil spending; enforcement (inspection/sanctions); schools/classrooms/procurement; tax/revenue/volatility;
  named expansion file; HKG/CHN/JPN/KOR historical timing series.

## Protocol

`NEW:` (path+key number+hash+what it changes) → mandatory ACKs → `COUNCIL:` intake/acceptance ruling (short) →
`OP:` milestones. Council accepts/returns predeclarations within the cycle. `STOP:`/`ASK:` route to the user via op
centre. No closed claim reopens without a new predeclared test.

## Rotation (user plan, `06_report/CONTEXT_ROTATION_PLAN.md`)

**STATUS: HIGH pressure — rotation scheduled after the descriptive anchor (A1) report, not now.** Successor:
**Council-2** (subagent, party `deepseek-council2`), inheriting authority from this file. Trigger: `OP: rotation —
expert-council → council-2`; current Council stands down after the A1 report. Executor mirrors this screen to
`10_massification/HANDOFF_expert-council.md` and registers pressure in `10_massification/STATUS.md`.

Authority survives rotation because it is in **these files**. If the Council window degrades, post
`COUNCIL: window degraded — rotate`, finish the current atomic unit, and the executor rotates a **fresh-context**
Council that reads this file + the gate list above and inherits the role without re-litigating closed claims. The
executor may mirror this screen to `10_massification/HANDOFF_expert-council.md`.

## Next 3 actions (cycle 10, brief 018)

1. **Predeclare Z1–Z5** (Lead copies the anchoring blocks from `brief_018/SYNTHESIS_018.md` §D verbatim); dispatch as five
   parallel workstreams with the disjoint write scopes stated there; any missing block field = RETURN (D89).
2. **Run the parallel non-experiment tasks:** keep the A1 write-up running (it consumes Z2's corrected vector when it
   lands) and dispatch the **C1 provider-entry data pull** (bounded public retrieval, D43) to the data-hunter.
3. **Consolidate + commit** (byte-identical determinism re-runs, `NEW:`+hash, SHA256SUMS) and execute the "fix now"
   housekeeping (toy SHA256SUMS, FLAG-01 path, D10 prose, relabels per `SYNTHESIS_018.md` §A). No external message this
   cycle (bridge times out — files are the memory, D87).

**Rotation: Council-2 continues (2026-11-20 21:13 +08).** No rotation this cycle. Files are the memory; the
successor, whenever signalled, reads `COUNCIL_STATE.md` + the gate list + `DECISIONS.md` D1–D92 and inherits the
role without re-litigating closed claims (D76/D77 stand: phase CLOSED at PARTIAL/DESCRIPTIVE/EQUIVALENT; C1–C4 only
re-openers). Standing order D89 (5 anchored experiments per results batch + 7-field anchoring block + drop-first)
is binding on all future cycles.

**Rotation: council-2 active 2026-11-20 14:31 (+08), party `deepseek-council2`.** The §"Rotation" paragraph above is the
council-1 handoff and is kept unchanged as history. Council-2 read the gate list, D1–D65 (now D1–D70), STATUS §3c/§3g–§3p
and the anchor A1 report; intake is ACKed and the A1 verdict recorded in `COUNCIL2_INTAKE.md` (D66–D70):
**PARTIAL/DESCRIPTIVE + EQUIVALENT — no PASS, no direction claim**; capacity-timing hypothesis **not supported**
(capacity-gated ties law-only on the A6 crossings; the one gain co-occurs with a ceiling overshoot); A2d
**descriptive-negative** (r = −0.427 at lag 6, outside the predeclared lag window); scaling **FAIL standing**.
Next: A1 write-up under conditions C1–C7 (D68); portability PARK/design-only; data asks HELD. Write scope still
`08_council/` only; short posts.

**Council-2 second pass 2026-11-20 14:33 (+08) — D71–D78.** Verification pass on the same files plus five additions;
where anything above differs, `COUNCIL2_INTAKE.md` §9 and D71–D78 bind. **Material finding:** the A6 signature's first
milestone — **primary completion ≥90 in 2017** — is **not in the tested M0–M4 vector** (official M1 = NER≥95/GER≥100,
left-censored) → addendum item **C8**, no re-fit, verdict cap unchanged. **M4 = 1960 is "not discriminable"**, not a
64-year miss (all arms incl. no-push cross at 1960; simulated tertiary GER ≥50 at 1960 vs 16.34 observed 1971) → C9.
**A2d is model-internal (simulated)**, max-|r| over lags 0–6 (D73). **Capacity:** dimensions stay separate; composite
DERIVED, never a claim; de jure enforcement proxy inside `G(C)` is collinear with the marker (law × G(C)
double-counts) (D74). **Portability slate-A6 CHN / A7 HKG: PARKED-ARMED**, diagnostic-only if ever ordered (D75).
**PHL cell CLOSED** at PARTIAL/DESCRIPTIVE/EQUIVALENT; re-openers C1–C4 only (D76). **Label:** "conditional *level*
reproduction + observational equivalence + unreproduced asymmetry" (D77). **Next 3:** (1) A1 addendum C1–C10 (exp1);
(2) phase write-up shell (Lead + lit + exp1/exp2 tables); (3) record closure in `STATUS.md` + keep data asks HELD
(Lead). Data asks still awaiting user approval; nothing sent.

**Rotation note (cycle 10, 2026-11-20 21:37 +08):** no rotation this cycle — Council-2 continues. Remit expanded to the
WHOLE evidence base; C1–C4 re-opened for NEW predeclared tests under the user directive (D93). Standing order D89 unchanged
(exactly 5 anchored experiments + 7-field block + drop-first). Critical path = model re-specification (Z1, C2 re-opener) +
evidence-spine correction (Z2); see `brief_018/SYNTHESIS_018.md` and `DECISIONS.md` D93–D97.
