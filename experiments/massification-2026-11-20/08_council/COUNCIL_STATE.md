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

## Next 3 actions (cycle 11, brief 019 — hysteresis-paper intake)

1. **Relay the ruling + WT slate** (Lead): paper = **candidate rival frame** (sixth A5 rival + D63 ceiling-residual
   account, still UNABLE); copy the WT1–WT5 anchoring blocks from `brief_019/SYNTHESIS_019.md` §C verbatim; **drop-first
   = WT5**. Dispatch WT1/WT2/WT4/WT3 in parallel (disjoint write scopes); WT5 = design-only note.
2. **Fold the rival into the write-up** (lit): re-label "signalling/MMI" → "credential hysteresis (signalling +
   exit-cost)" in the A5 rival field; cite the paper as a theoretical candidate (author blank), never as validated;
   keep the external credential facts (39% overeducation, ~45% surplus-return, BPO ~1.9M) on the external-review rows
   only.
3. **Hold the model gate** (Council): no architecture layer until WT1 AND WT3 both return non-null; then the
   complementarity→persistence term is added only as a declared, ablation-tested assumption (R4/R27, D81-2). Record
   WT1/WT3 outcomes in `DECISIONS.md`; no direction claim, no C1–C4 reopening. **No external message sent this cycle**
   (bridge times out; files are the memory — D87).

## Next 3 actions (cycle 12, brief 020 — assembly-paper intake; D102–D105)

1. **Dispatch the WT and DT slates in parallel** (Lead/executor): copy the WT1–WT5 blocks from
   `brief_019/SYNTHESIS_019.md` §C and the DT1–DT5 blocks from `brief_020/SYNTHESIS_020.md` §C **verbatim** into frozen
   predeclarations; disjoint write scopes; deterministic scripts; HELD parts named and never fabricated (WT2 wage
   premium, WT5 PHL/KHM participation, DT3 behavioural data). Drop-first: WT5, DT3.
2. **Write-up wiring** (lit): re-label the A5 rival field "signalling/MMI" → "credential hysteresis (signalling +
   exit-cost)", cite the hysteresis paper as theoretical candidate only (author blank, never validated), add the
   combined theory-frame section (`scaffold/induction/exit-cost/shadow-at-gates`) labelled THEORY / DECLARED-ASSUMPTION,
   and keep the external credential facts on the external-review rows only.
3. **Hold both model gates** (Council): (a) **no exit-cost/complementarity layer** until WT1 AND WT3 both return
   non-null — then only a declared, ablation-tested term (R4/R27, D81-2); (b) **no induction naming** until DT1 AND DT2
   both return non-null. Record WT/DT outcomes in `DECISIONS.md`; no direction claim; no C1–C4 reopening. **No external
   message sent this cycle** (bridge times out; files are the memory — D87).

## Next 3 actions (cycle 13, brief 021 — WT/DT adjudication + SR-9; D108–D113)

1. **Merge + dispatch** (Lead): D108–D113 are merged. Copy the five anchoring blocks verbatim from
   `brief_021/SYNTHESIS_021.md` §4; predeclare; dispatch **EXP-1 CEIL-ATTRIB and EXP-3 M1-NER first**, EXP-2 A3-D
   **after CEIL-ATTRIB**, EXP-4 A3-S (v1.3 shadow build) after the v1.2.1 addendum is delivered; **EXP-5 ASYM-K is
   drop-first** (not dispatched unless capacity remains). Enforce D113b: no further paper-test slate this phase.
2. **Fix the record items before the next model run** (Lead): (i) v1.2 FINDINGS §1.2 — delete/repair the cross-year
   "1.136 (upper 2018)" ratio and restate `m = 1.10` as a **convention** with the 1.09–1.11 window; (ii)
   `MODEL_ARCHITECTURE.md` Amendment A4 — relabel A1/A3 from "theory-grounded" to "candidate grounding — PARKED per
   D104; no theory citation"; (iii) HKG checklist SR-2 path status note (reads predecl-only `v1_2/`; delivered artifacts
   are in `generator_v1_2/`); (iv) WT record corrections (WT4 fragility sentence; WT2 VOID annotation).
3. **Gate the HKG run** (Council + Lead): SR-9 is AUTHORISE-WITH-CONDITIONS. Execute only when **H1** (M1-NER construct
   equivalence: |stock−flow| ≤ 2.0 pp in the 85–95 band and ≤1 y crossing difference) and H2–H6 hold; verify checklist
   §2 hashes + determinism; report `BLOCKED-*` as a terminal state and `TRANSFER-FAILS` as the informative outcome.
   No HKG/portability/phase-verdict claim. **No external message sent this cycle** (D87).

## Next 3 actions (cycle 14, brief 022 — model-line adjudication + post-H1 HKG; D117–D125)

1. **Merge + run the slate in dependency order** (Lead): D117–D123 merged; copy the EXP-6…EXP-10 blocks verbatim from
   `brief_022/SYNTHESIS_022.md` §6; **predeclare EXP-7 first** (does v1.2 reproduce the observed path; κ-link test),
   then EXP-6, EXP-8, EXP-9; **EXP-10 is drop-first** (HKG stock-object design; D120 governs, run-ready not run).
   Re-derive every block number from disk before freeze (D113a).
2. **Record the user corrections and the theory frame** (Lead): D124 (no "demand falsified"; bimodal two-tier A5
   requirement; HELD seat-utilisation data ask) and D125 (one-way ratchet macro-principle — declared theory, no
   reverse term, shocks as declared inputs, strong claim untestable). `synthetic_2026-11-20/THEORY_FRAME.md` and
   `MODEL_ARCHITECTURE.md` A4/A5 carry them; **no reversal diagnostic may be proposed as reachable**, any future one
   must be predeclared and labelled descriptive.
3. **Freeze the v1.5 BIMODAL-GATE predeclaration before any run** (Lead): two-tier gates (open-access seats that can
   go untaken + rationed high-quality gates incl. the rung-4 credential queue), explicit outside option, κ-link
   precondition, no free taste parameter, checks (a)–(e) from D124, no-re-fit guard; HELD data named, never
   fabricated; no re-tune of A3-D, no fitting to the known outcome. **No external message sent this cycle** (D87).

## Next 3 actions (cycle 15, brief 023 — model-line adjudication + v1.5 defect rulings; D132–D137)

1. **Predeclare and run the slate in the binding order** (Lead): copy EXP-11/EXP-12/EXP-13/EXP-14/EXP-15 blocks verbatim
   from `brief_023/SYNTHESIS_023.md` §6; **EXP-11 KAPPA-FWD, EXP-12 FLOOR-CLOSE, EXP-13 LOWER-DEF in parallel first**;
   **EXP-14 V16-REPAIR only after EXP-11 and EXP-13 return** (carry D134's three design obligations and the child-wage
   re-specification verbatim); **EXP-15 CONV-REG last or dropped**. Re-derive every block number from disk before freeze
   (D113a; VERIFICATION_023.csv).
2. **Record the per-system κ register + A10 scope + DEFER-HKG** (Lead): κ = PHL 0.9491 / KOR 0.9898 / KHM 0.5950 / CHN
   0.7222 (CHN not forward-usable); "capacity buys the floor" is conditional on the declared `phys_cap = 1.15` convention
   until FLOOR-CLOSE; HKG is **DEFER-HKG** (the predeclared reversion fired; the frozen EXP-10 design artifact is kept
   but un-fires nothing; a new Council decision is required). The HELD ask queue is complete and named (D135) — no proxy
   substitution.
3. **Repair, don't re-tune** (Lead): V16 carries D134's obligations — bound completion units with survival explicit;
   declared projection order + propagation ledger + counterfactual-identity guard; locate Tier O quality at the
   return/take-up margin; test the child-wage shock in A10 (κ OFF) on the pre-cap object; every leg names its arm by the
   full switch tuple; retire the (b) family for the successor in favour of EXP-7's ≥17/33 bar. **No external message sent
   this cycle** (D87).

## Next 3 actions (cycle 16, brief 024 — observed-path failure ruled; D142–D147)

1. **Predeclare and run EXP-16 and EXP-17 in parallel** (Lead): copy their blocks verbatim from
   `brief_024/SYNTHESIS_024.md` §5; **EXP-16 PARTPROV is count-blind** (the driver must refuse to run if the observed
   file is opened; no 33-cell count may be computed); **EXP-17 JOINT-COVER** reports λ* and adopts nothing; then
   **EXP-18 PART-REPAIR only if EXP-16 returns `DUPLICATED-PRIMITIVES` or `MIXED`** (its closing rule: bar missed →
   generator line closes at representation-only, line becomes (b)+(c)); **EXP-19 after EXP-17**; **EXP-20 last or
   dropped**. Re-derive every block number from disk before freeze (D113a; VERIFICATION_024.csv).
2. **Apply the four authoring rules to every new predeclaration** (Lead): precedence stated; resolution pretest (a leg
   that cannot move ≥1 object is UNFIRABLE-BY-DESIGN, not scored as FAIL); arm tuple + capability lint (build fails if a
   named object cannot exist in the named arm); count-blind diagnostics. Parks stand: A3 KILLED; exit-cost/induction
   PARKED; HKG DEFER-HKG; C1–C4 closed; phase verdict untouched. No proxy substitution outside EXP-19; HELD named.
3. **Record and report** (Lead): the observed-path failure is localised to the participation margin; the repair
   artifacts are closed as artifacts (no re-run/re-tune); the per-system κ register is descriptive only; the HKG design
   is preserved unrun. Any successor generator is predeclared only after EXP-16 returns and only under the tree. **No
   external message sent this cycle** (D87).

## Immediate next state (post-generator; awaiting Council cycle 17)

1. **Generator line closed at representation-only** (D150); repair artifacts closed; no successor predeclared. The
   programme's live outputs are the representation capability, the per-system κ descriptive register, the v1.2
   placement label, the localised participation-margin failure, and the measurement position (required coverage
   DECLARED; places HELD; EXP-19 PROXY-SILENT).
2. **Council cycle 17** is being convened to adjudicate EXP-16 (MIXED, EXP-18 licensed), EXP-17 (SINGLE-LEVER-IDENTIFIED,
   λ* not adopted), EXP-18 (PATH-FAILED, closing rule fired), EXP-19 (PROXY-SILENT) and to issue the post-generator five
   (D89). **EXP-20 USE-REG remains drop-first.**
3. **No re-run/re-score, no new generator, no proxy substitution, no proxy adoption, no HKG run** before that ruling.
   HELD list unchanged (D146/D151). Parks: A3 KILLED; exit-cost/induction PARKED; HKG DEFER; D63 UNABLE; phase verdict
   (D76/D77) untouched.

## Next 3 actions (cycle 17, brief 025 — closing record ruled; D152–D159)

1. **Predeclare and run the descriptive-consolidation slate** (Lead): copy blocks verbatim from
   `brief_025/SYNTHESIS_025.md` §6; **EXP-21 CONV-REG first** (rank #1; the register is the precondition for every level
   sentence; identification gate: <3 same-year pairs = THIN, no label), then **EXP-22 PART-MARGIN-DESC**,
   **EXP-23 D63-BOUNDS**, **EXP-24 KAPPA-WRITE**, and **EXP-25 V-SPINE last or dropped** (drop-first; second cut EXP-24).
   Re-derive every block number from disk before freeze (D113a; VERIFICATION_025.csv). **Sunset clause:** if the
   deliverables are not on disk by the next cycle, the descriptive line reverts to the existing closeout.
2. **Enforce the seven authoring rules (D158) in every new predeclaration** — hash enforcement at verdict time; object
   identity before comparison; register before sentence; level-symmetric legs; class tags; banned sentences register;
   REQUIRED-STATE/DERIVED label discipline. **No successor generator** (forbidden re-entries named in D154); no proxy
   against the required state; no experiment against a HELD object; HELD list unchanged (D157); D63 UNABLE; HKG DEFER;
   parks stand.
3. **Write-up posture** (Lead): the phase write-up shell predates the closed line (0 occurrences of v1.5/v1.6/v1.7/
   bimodal/κ/WINDOW-ONLY; headline "Conditional level reproduction…") — EXP-25 must replace it with the closed-line
   state, the single-tier representation sentence, the class tags, the REQUIRED-STATE provenance and the banned-sentence
   register. **No external message sent this cycle** (D87).
